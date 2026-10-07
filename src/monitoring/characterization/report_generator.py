"""
CharacterizationReportGenerator for Step 10D.

Validates run output records against `device_characterization_schema.json`,
maps runtime states to report statuses, updates `device_capability_matrix.md`,
prevents silent run overwrites, validates evidence file existence,
and enforces two-run separate-day and reboot stability criteria.

R-08 variant gate (protocol §2, §9 criterion 2): `evaluate_variant_signoff()` passes only when
`variant_check` is VERIFIED and its nearest variant is the required variant. It is ONE §9 criterion.
Full §9 sign-off (coverage, variant, D-10, D-16, human review gate) is evaluated by signoff.py and written to
step10d_signoff.json in the run directory; software never marks the review gate satisfied. run_status is not changed.
"""

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jsonschema

from src.monitoring.characterization.coverage import check_matrix_coverage
from src.monitoring.characterization.ram_variant import MATCH as RAM_MATCH, load_ram_variant_spec

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCHEMA_PATH = ROOT / "research" / "experiments" / "device_characterization_schema.json"
MATRIX_PATH = ROOT / "research" / "experiments" / "device_capability_matrix.md"


def load_schema() -> Dict[str, Any]:
    """Loads device_characterization_schema.json."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_variant_signoff(run_record: Dict[str, Any], required_variant: Optional[str] = None) -> Dict[str, Any]:
    """R-08 sign-off gate for one run. Allowed only for a VERIFIED variant_check whose nearest
    variant is the required variant (from configs/device_characterization.yaml)."""
    required = required_variant or load_ram_variant_spec()["required_variant"]
    vc = (run_record.get("device_identity") or {}).get("variant_check") or {}
    value = vc.get("value") if isinstance(vc.get("value"), dict) else {}
    classification = value.get("classification")
    nearest = value.get("nearest_variant")
    allowed = (
        vc.get("verified") is True
        and vc.get("report_status") == "VERIFIED"
        and classification == RAM_MATCH
        and nearest == required
    )
    if allowed:
        reason = f"variant_check VERIFIED: nearest nominal variant is the required {required}."
    elif not vc:
        reason = "variant_check missing."
    elif vc.get("state") != "AVAILABLE":
        reason = f"variant_check state is {vc.get('state')}; the required {required} variant is not confirmed."
    elif classification and classification != RAM_MATCH:
        reason = f"variant_check is {classification} (nearest: {nearest}); the required {required} variant is not confirmed."
    else:
        reason = f"variant_check is not VERIFIED; the required {required} variant is not confirmed."
    return {
        "signoff_allowed": allowed,
        "required_variant": required,
        "classification": classification,
        "nearest_variant": nearest,
        "reason": reason,
    }


def evaluate_step10d_signoff(run_record: Dict[str, Any], review_confirmed: bool = False) -> Dict[str, Any]:
    from src.monitoring.characterization.signoff import evaluate_step10d_signoff as _full
    return _full(run_record, review_confirmed=review_confirmed)


def validate_characterization_record(
    record: Dict[str, Any],
    output_dir: Optional[Path] = None
) -> List[str]:
    """Validates a characterization run record against the schema, null-value rule,
    evidence file existence, and manifest SHA-256 evidence integrity.
    """
    errors: List[str] = []

    # 1. JSON schema validation
    schema = load_schema()
    try:
        jsonschema.validate(instance=record, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation error: {e.message} at path {'/'.join(str(p) for p in e.path)}")
    except jsonschema.SchemaError as e:
        errors.append(f"Schema error: {e.message}")

    # 2. Check run conditions
    conditions = record.get("conditions", {})
    adb_connected = conditions.get("adb_connected", False)
    is_dry_run = conditions.get("is_dry_run", False) or not adb_connected

    # Track verified evidence
    verified_refs: List[str] = []

    # 3. Programmatic no-fake-zeros & evidence file checks
    def _check_result(res: Dict[str, Any], path: str):
        if not isinstance(res, dict):
            return
        state = res.get("state")
        val = res.get("value")
        verified = res.get("verified", False)
        report_status = res.get("report_status")
        ev_ref = res.get("evidence_ref")

        condition = res.get("condition")
        if report_status == "REQUIRES PILOT VALIDATION" and state != "AVAILABLE":
            errors.append(f"{path}: REQUIRES PILOT VALIDATION requires a demonstrated interface (state AVAILABLE), got '{state}'")
        if report_status == "CONDITIONALLY AVAILABLE" and not condition:
            errors.append(f"{path}: CONDITIONALLY AVAILABLE requires a recorded condition")
        if verified is True and condition:
            errors.append(f"{path}: verified=True with condition '{condition}' (condition-gated values are CONDITIONALLY AVAILABLE)")
        # A1: every evidence reference, verified or not, must name a file that exists in the run directory.
        if output_dir and ev_ref and verified is not True:
            if not (output_dir / ev_ref.split("#")[0]).exists():
                errors.append(f"{path}: evidence_ref file '{output_dir / ev_ref.split('#')[0]}' does not exist on disk")

        if state and state != "AVAILABLE":
            if val is not None:
                errors.append(f"{path}: state '{state}' has non-null value '{val}' (violates no-fake-zeros rule)")
            if verified is True:
                errors.append(f"{path}: state '{state}' has verified=True (only AVAILABLE state can be verified)")
        
        if verified is True:
            if state != "AVAILABLE":
                errors.append(f"{path}: verified=True requires state AVAILABLE")
            if report_status != "VERIFIED":
                errors.append(f"{path}: verified=True requires report_status VERIFIED")
            if not ev_ref:
                errors.append(f"{path}: verified=True requires evidence_ref")
            if is_dry_run:
                errors.append(f"{path}: verified=True is forbidden when adb_connected=False / is_dry_run=True")

            if ev_ref:
                verified_refs.append(ev_ref)

            # Check if evidence file actually exists on disk
            if output_dir and ev_ref:
                rel_path = ev_ref.split("#")[0]
                full_ev_path = output_dir / rel_path
                if not full_ev_path.exists():
                    errors.append(f"{path}: evidence_ref file '{full_ev_path}' does not exist on disk")

    def _scan(obj: Any, path: str):
        if isinstance(obj, dict):
            if "metric" in obj and "state" in obj:
                _check_result(obj, path)
            for k, v in obj.items():
                _scan(v, f"{path}/{k}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                _scan(item, f"{path}[{idx}]")

    _scan(record, "root")

    # 4. P-05: Manifest SHA-256 evidence integrity verification
    if output_dir:
        manifest_file = output_dir / "evidence" / "manifest.json"
        
        if adb_connected or verified_refs:
            if not manifest_file.exists():
                errors.append(f"Required evidence manifest.json missing from '{output_dir / 'evidence'}' (P-05 requirement)")

        if manifest_file.exists():
            try:
                manifest_bytes = manifest_file.read_bytes()
                actual_manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
                record_manifest_sha = record.get("manifest_sha256")
                
                if not record_manifest_sha and (adb_connected or verified_refs):
                    errors.append("Missing required 'manifest_sha256' in characterization record (P-05 requirement)")
                elif record_manifest_sha and record_manifest_sha != actual_manifest_sha:
                    errors.append(
                        f"Manifest SHA-256 mismatch: record manifest_sha256 '{record_manifest_sha}' "
                        f"does not match actual manifest.json SHA-256 '{actual_manifest_sha}' (P-05 tampering error)"
                    )

                manifest_entries = json.loads(manifest_bytes.decode("utf-8"))
                for entry in manifest_entries:
                    rel_p = entry.get("relative_path")
                    expected_sha = entry.get("sha256")
                    if rel_p and expected_sha:
                        full_p = output_dir / rel_p
                        if not full_p.exists():
                            errors.append(f"Manifest evidence file missing: {rel_p}")
                        else:
                            actual_sha = hashlib.sha256(full_p.read_bytes()).hexdigest()
                            if actual_sha != expected_sha:
                                errors.append(
                                    f"Evidence integrity failure for '{rel_p}': SHA-256 mismatch "
                                    f"(expected {expected_sha}, got {actual_sha})"
                                )
            except Exception as e:
                errors.append(f"Failed to read/verify evidence manifest: {str(e)}")

    return errors


def _record_states(run: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Flattened {record path: state} over every capability record of a run."""
    out: Dict[str, Optional[str]] = {}
    ident = run.get("device_identity") or {}
    for r in ident.get("observed", []):
        out[f"identity/{r.get('metric')}"] = r.get("state")
    if ident.get("variant_check"):
        out["identity/variant_check"] = ident["variant_check"].get("state")
    for t in run.get("telemetry", []):
        for r in t.get("results", []):
            out[f"telemetry/{t.get('dimension')}/{r.get('metric')}"] = r.get("state")
    thermal = run.get("thermal") or {}
    for k, v in thermal.items():
        if isinstance(v, dict):
            out[f"thermal/{k}"] = v.get("state")
    for r in thermal.get("temperature_sources", []) or []:
        out[f"thermal/temperature_sources/{r.get('metric')}"] = r.get("state")
    out["thermal/selected_thermal_source"] = thermal.get("selected_thermal_source")
    for cam in run.get("camera", []):
        for r in cam.get("results", []) + [cam.get("manual_control_honoured") or {}]:
            out[f"camera/{cam.get('camera_id')}/{r.get('metric')}"] = r.get("state")
    for b in run.get("backends", []):
        for k in ("availability", "graph_load", "inference_execution", "delegation", "probability_output"):
            if k in b:
                out[f"backend/{b.get('backend')}/{k}"] = (b.get(k) or {}).get("state")
        for r in b.get("quantization_support") or []:
            out[f"backend/{b.get('backend')}/{r.get('metric')}"] = r.get("state")
    for r in run.get("profiling", []):
        out[f"profiling/{r.get('metric')}"] = r.get("state")
    energy = run.get("energy") or {}
    for k in ("E1_battery_side_reference", "E2_supply_powered_session", "E3_software_counters"):
        out[f"energy/{k}"] = (energy.get(k) or {}).get("state")
    out["energy/selected_level"] = energy.get("selected_level")
    return out


class CharacterizationReportGenerator:
    """Generates schema-valid characterization outputs without mutating authoritative research specs."""

    def __init__(self, schema_path: Optional[Path] = None, matrix_path: Optional[Path] = None):
        self.schema_path = schema_path or SCHEMA_PATH
        self.matrix_path = matrix_path or MATRIX_PATH

    def process_run(
        self,
        run_record: Dict[str, Any],
        output_dir: Path,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """Validates run record and saves schema-valid JSON files in output_dir.
        P-01: A single characterization run NEVER mutates the authoritative device_capability_matrix.md.
        R-11: Writes files atomically via temp files, flush/fsync, and rename.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        run_file = output_dir / "characterization.json"

        if run_file.exists() and not overwrite:
            raise FileExistsError(f"Characterization output file '{run_file}' already exists. Silent overwrite is refused (F-14).")

        errors = validate_characterization_record(run_record, output_dir=output_dir)
        if errors:
            raise ValueError(f"Characterization record failed validation:\n" + "\n".join(errors))

        tmp_run_file = output_dir / "characterization.json.tmp"
        tmp_readme_file = output_dir / "README.md.tmp"
        readme_file = output_dir / "README.md"

        try:
            with open(tmp_run_file, "w", encoding="utf-8") as f:
                json.dump(run_record, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            tmp_run_file.replace(run_file)

            summary_md = self._generate_markdown_summary(run_record)
            with open(tmp_readme_file, "w", encoding="utf-8") as f:
                f.write(summary_md)
                f.flush()
                os.fsync(f.fileno())

            tmp_readme_file.replace(readme_file)

            # P-01: Do NOT call self.update_device_capability_matrix(run_record) automatically!
            # Matrix mutation is forbidden for single runs. Run outputs remain isolated in output_dir.

            # §9: criterion-1 coverage and the full sign-off evaluation, written beside the run (the schema-bound
            # characterization.json is not extended). The review gate is never satisfied by software.
            signoff = evaluate_step10d_signoff(run_record)
            coverage = check_matrix_coverage(run_record)
            signoff_file = output_dir / "step10d_signoff.json"
            tmp_signoff = output_dir / "step10d_signoff.json.tmp"
            with open(tmp_signoff, "w", encoding="utf-8") as f:
                json.dump({"run_id": run_record.get("run_id"), "signoff": signoff, "coverage": coverage}, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            tmp_signoff.replace(signoff_file)

            return {
                "status": "VALID",
                "run_file": str(run_file),
                "readme_file": str(readme_file),
                "signoff_file": str(signoff_file),
                "errors": [],
                "variant_signoff": evaluate_variant_signoff(run_record),
                "signoff": signoff,
            }
        except Exception:
            if tmp_run_file.exists():
                tmp_run_file.unlink(missing_ok=True)
            if tmp_readme_file.exists():
                tmp_readme_file.unlink(missing_ok=True)
            if run_file.exists() and not overwrite:
                run_file.unlink(missing_ok=True)
            raise

    def _generate_markdown_summary(self, run_record: Dict[str, Any]) -> str:
        run_id = run_record.get("run_id", "unknown")
        started = run_record.get("started_at", "unknown")
        repeat_idx = run_record.get("repeat_index", 1)
        cond = run_record.get("conditions", {})

        lines = [
            f"# Device Characterization Report — Run {run_id}",
            "",
            f"- **Start Time (UTC)**: `{started}`",
            f"- **Repeat Index**: `{repeat_idx}`",
            f"- **ADB Connected**: `{cond.get('adb_connected', False)}`",
            f"- **Boot ID**: `{cond.get('boot_id', 'unknown')}`",
            "",
            "## Summary of Telemetry Capabilities",
            "",
            "| Dimension / Metric | State | Value | Report Status | Source | Evidence |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        def _format_row(res: Dict[str, Any]):
            m = res.get("metric", "unknown")
            st = res.get("state", "unknown")
            val = str(res.get("value")) if res.get("value") is not None else "null"
            rep_st = res.get("report_status", "unknown")
            src = res.get("source", "unknown")
            ev = res.get("evidence_ref") or "—"
            lines.append(f"| {m} | {st} | {val} | {rep_st} | {src} | {ev} |")

        for item in run_record.get("device_identity", {}).get("observed", []):
            _format_row(item)
        variant_check = run_record.get("device_identity", {}).get("variant_check")
        if variant_check:
            _format_row(variant_check)
        for t in run_record.get("telemetry", []):
            for res in t.get("results", []):
                _format_row(res)

        thermal = run_record.get("thermal", {})
        for key in ("thermal_status_api", "thermal_headroom_api", "frequency_capping_observable", "external_surface_probe"):
            if isinstance(thermal.get(key), dict):
                _format_row(thermal[key])
        for res in thermal.get("temperature_sources", []):
            _format_row(res)
        for cam in run_record.get("camera", []):
            for res in cam.get("results", []) + [cam.get("manual_control_honoured")]:
                if res:
                    _format_row(dict(res, metric=f"camera[{cam.get('camera_id')}].{res.get('metric')}"))
        for b in run_record.get("backends", []):
            for key in ("availability", "graph_load", "inference_execution", "probability_output", "delegation"):
                if b.get(key):
                    _format_row(dict(b[key], metric=f"{b['backend']}.{b[key].get('metric')}"))
            for res in b.get("quantization_support") or []:
                _format_row(dict(res, metric=f"{b['backend']}.{res.get('metric')}"))
        for res in run_record.get("profiling", []):
            _format_row(res)
        energy = run_record.get("energy", {})
        for key in ("E1_battery_side_reference", "E2_supply_powered_session", "E3_software_counters"):
            if isinstance(energy.get(key), dict):
                _format_row(energy[key])

        gate = evaluate_variant_signoff(run_record)
        full = evaluate_step10d_signoff(run_record)
        crit = full["criteria"]
        lines += [
            "",
            f"- **Selected thermal source (D-10)**: `{thermal.get('selected_thermal_source')}`",
            f"- **Selected energy level (D-16)**: `{energy.get('selected_level')}`; absolute energy claimed: `False`",
            "",
            "## Step 10D Sign-off (protocol §9)",
            "",
            f"- **Criterion 1, matrix coverage**: `{'PASS' if crit['criterion_1_matrix_coverage']['passed'] else 'FAIL'}` "
            f"({crit['criterion_1_matrix_coverage']['rows_failed']} of {crit['criterion_1_matrix_coverage']['rows_total']} "
            "rows failing; details in `step10d_signoff.json`)",
            f"- **Criterion 2, R-08 variant check**: `{'PASS' if gate['signoff_allowed'] else 'FAIL'}`",
            f"  - **Variant sign-off**: `{'ALLOWED' if gate['signoff_allowed'] else 'BLOCKED'}`",
            f"  - **Reason**: {gate['reason']}",
            f"- **Criterion 3, D-10 thermal source**: `{'PASS' if crit['criterion_3_d10_thermal_source']['passed'] else 'FAIL'}` "
            f"({crit['criterion_3_d10_thermal_source']['reason']})",
            f"- **Criterion 3, D-16 energy level**: `{'PASS' if crit['criterion_3_d16_energy_level']['passed'] else 'FAIL'}` "
            f"({'; '.join(crit['criterion_3_d16_energy_level']['problems']) or 'decided from evidence'})",
            f"- **Criterion 4, review gate**: `{crit['criterion_4_review_gate']['status']}` (never satisfied by software)",
            f"- **Step 10D sign-off**: `{'ALLOWED' if full['signoff_allowed'] else 'NOT ALLOWED'}`",
        ]
        return "\n".join(lines) + "\n"

    def compare_repeat_runs(self, run1: Dict[str, Any], run2: Dict[str, Any],
                            review_confirmed: bool = False) -> Dict[str, Any]:
        """Compares two characterization runs for stability, separate calendar dates, and reboot proof."""
        discrepancies: List[str] = []

        # 1. Require real device observations in both runs
        cond1 = run1.get("conditions", {})
        cond2 = run2.get("conditions", {})
        if not cond1.get("adb_connected") or not cond2.get("adb_connected"):
            discrepancies.append("Repeat stability comparison requires adb_connected=True in both runs.")

        # 2. Date check: separate calendar dates required
        date1 = run1.get("started_at", "")[:10]  # YYYY-MM-DD
        date2 = run2.get("started_at", "")[:10]
        if date1 == date2:
            discrepancies.append(f"Repeat runs must occur on separate calendar days (got {date1} for both runs).")

        # 3. Reboot check: distinct boot IDs or uptime drop required
        boot1 = cond1.get("boot_id")
        boot2 = cond2.get("boot_id")
        if boot1 and boot2 and boot1 == boot2:
            discrepancies.append("Repeat runs must have different boot IDs indicating phone reboot between runs.")

        # 4. Compare observed total RAM
        ram1 = next((r.get("value") for r in run1.get("device_identity", {}).get("observed", []) if r.get("metric") == "total_ram_mb"), None)
        ram2 = next((r.get("value") for r in run2.get("device_identity", {}).get("observed", []) if r.get("metric") == "total_ram_mb"), None)
        if ram1 != ram2:
            discrepancies.append(f"Observed total_ram_mb differs between runs: Run 1={ram1}, Run 2={ram2}")

        # 5. Compare the capability state of every record in every phase (protocol §4: each phase repeated).
        states1, states2 = _record_states(run1), _record_states(run2)
        for key in sorted(set(states1) | set(states2)):
            st1, st2 = states1.get(key), states2.get(key)
            if st1 != st2:
                discrepancies.append(f"Capability state mismatch [{key}]: Run 1={st1}, Run 2={st2}")

        # 6. §9 sign-off for each run. `stable` keeps its repeatability meaning; `variant_gate_passed` is the R-08
        #    criterion only; `signoff_allowed` is the full §9 result (coverage, variant, D-10, D-16, review gate)
        #    for both runs plus stability. The review gate is never satisfied by software.
        gate1 = evaluate_variant_signoff(run1)
        gate2 = evaluate_variant_signoff(run2)
        variant_ok = gate1["signoff_allowed"] and gate2["signoff_allowed"]
        full1 = evaluate_step10d_signoff(run1, review_confirmed=review_confirmed)
        full2 = evaluate_step10d_signoff(run2, review_confirmed=review_confirmed)

        return {
            "stable": len(discrepancies) == 0,
            "discrepancies": discrepancies,
            "variant_signoff": {"run1": gate1, "run2": gate2},
            "variant_gate_passed": len(discrepancies) == 0 and variant_ok,
            "signoff": {"run1": full1, "run2": full2},
            "signoff_allowed": len(discrepancies) == 0 and full1["signoff_allowed"] and full2["signoff_allowed"],
        }
