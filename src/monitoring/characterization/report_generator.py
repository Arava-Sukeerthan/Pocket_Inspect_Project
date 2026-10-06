"""
CharacterizationReportGenerator for Step 10D.

Validates run output records against `device_characterization_schema.json`,
maps runtime states to report statuses, updates `device_capability_matrix.md`,
prevents silent run overwrites, validates evidence file existence,
and enforces two-run separate-day and reboot stability criteria.

Step 10D sign-off gate (R-08, protocol §2 and §9 criterion 2): `evaluate_variant_signoff()` allows
sign-off only when `variant_check` is VERIFIED and its nearest variant is the required variant.
A MISMATCH, AMBIGUOUS, ERROR or NOT_TESTED variant check blocks sign-off. run_status is not changed.
"""

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jsonschema

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

            return {
                "status": "VALID",
                "run_file": str(run_file),
                "readme_file": str(readme_file),
                "errors": [],
                "variant_signoff": evaluate_variant_signoff(run_record),
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

        gate = evaluate_variant_signoff(run_record)
        lines += [
            "",
            "## Step 10D Sign-off Gate (R-08 RAM variant check)",
            "",
            f"- **Variant sign-off**: `{'ALLOWED' if gate['signoff_allowed'] else 'BLOCKED'}`",
            f"- **Reason**: {gate['reason']}",
            "- This gate is one of the protocol §9 criteria; it does not by itself sign off Step 10D.",
        ]
        return "\n".join(lines) + "\n"

    def update_device_capability_matrix(self, run_record: Dict[str, Any]):
        """Updates research/experiments/device_capability_matrix.md with observed evidence."""
        if not self.matrix_path.exists():
            return

        content = self.matrix_path.read_text(encoding="utf-8")

        # Update observed status rows if real evidence exists
        obs_map = {}
        for item in run_record.get("device_identity", {}).get("observed", []):
            obs_map[item["metric"]] = item
        for t in run_record.get("telemetry", []):
            for res in t.get("results", []):
                obs_map[res["metric"]] = res

        # Replace NOT YET VERIFIED status in matrix table rows when verified evidence exists
        for metric, res in obs_map.items():
            if res.get("verified") and res.get("evidence_ref"):
                rep_st = res.get("report_status", "VERIFIED")
                ev_ref = res.get("evidence_ref")
                # Pattern for replacing placeholder status in markdown tables
                pattern = rf"(\|\s*{re.escape(metric)}\s*\|.*?\|)\s*NOT YET VERIFIED\s*\|\s*—\s*\|"
                replacement = rf"\1 {rep_st} | `{ev_ref}` |"
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        self.matrix_path.write_text(content, encoding="utf-8")

    def compare_repeat_runs(self, run1: Dict[str, Any], run2: Dict[str, Any]) -> Dict[str, Any]:
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

        # 5. Compare telemetry capabilities
        tel1_map = {t["dimension"]: {r["metric"]: r["state"] for r in t.get("results", [])} for t in run1.get("telemetry", [])}
        tel2_map = {t["dimension"]: {r["metric"]: r["state"] for r in t.get("results", [])} for t in run2.get("telemetry", [])}

        for dim, metrics1 in tel1_map.items():
            metrics2 = tel2_map.get(dim, {})
            for m_name, st1 in metrics1.items():
                st2 = metrics2.get(m_name)
                if st1 != st2:
                    discrepancies.append(f"Telemetry state mismatch [{dim}/{m_name}]: Run 1={st1}, Run 2={st2}")

        # 6. R-08 sign-off gate: both runs must confirm the required RAM variant.
        #    Reported separately so that `stable` keeps its repeatability meaning.
        gate1 = evaluate_variant_signoff(run1)
        gate2 = evaluate_variant_signoff(run2)
        variant_ok = gate1["signoff_allowed"] and gate2["signoff_allowed"]

        return {
            "stable": len(discrepancies) == 0,
            "discrepancies": discrepancies,
            "variant_signoff": {"run1": gate1, "run2": gate2},
            "signoff_allowed": len(discrepancies) == 0 and variant_ok,
        }
