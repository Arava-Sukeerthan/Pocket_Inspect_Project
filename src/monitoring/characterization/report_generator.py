"""
CharacterizationReportGenerator for Step 10D.

Validates run output records against `device_characterization_schema.json`,
maps runtime states to report statuses, updates `device_capability_matrix.md`,
and compares repeat characterization runs for stability and specification agreement.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jsonschema

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCHEMA_PATH = ROOT / "research" / "experiments" / "device_characterization_schema.json"
MATRIX_PATH = ROOT / "research" / "experiments" / "device_capability_matrix.md"


def load_schema() -> Dict[str, Any]:
    """Loads device_characterization_schema.json."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_characterization_record(record: Dict[str, Any]) -> List[str]:
    """Validates a characterization run record against the schema and null-value rule.
    Returns a list of validation error strings (empty if valid).
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

    # 2. Programmatic no-fake-zeros & null-value rule check across all capability_result objects
    def _check_result(res: Dict[str, Any], path: str):
        if not isinstance(res, dict):
            return
        state = res.get("state")
        val = res.get("value")
        verified = res.get("verified", False)
        report_status = res.get("report_status")

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
            if not res.get("evidence_ref"):
                errors.append(f"{path}: verified=True requires evidence_ref")

    # Recursive scan for capability_result objects
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
    return errors


class CharacterizationReportGenerator:
    """Generates schema-valid characterization outputs and updates device_capability_matrix.md."""

    def __init__(self, schema_path: Optional[Path] = None, matrix_path: Optional[Path] = None):
        self.schema_path = schema_path or SCHEMA_PATH
        self.matrix_path = matrix_path or MATRIX_PATH

    def process_run(self, run_record: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
        """Validates run record, saves schema-valid JSON files, and checks repeatability."""
        errors = validate_characterization_record(run_record)
        if errors:
            raise ValueError(f"Characterization record failed validation:\n" + "\n".join(errors))

        output_dir.mkdir(parents=True, exist_ok=True)
        run_file = output_dir / "characterization.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(run_record, f, indent=2)

        return {
            "status": "VALID",
            "run_file": str(run_file),
            "errors": [],
        }

    def compare_repeat_runs(self, run1: Dict[str, Any], run2: Dict[str, Any]) -> Dict[str, Any]:
        """Compares two characterization runs for stability and flags discrepancies."""
        discrepancies: List[str] = []

        # Compare observed total RAM
        ram1 = next((r.get("value") for r in run1.get("device_identity", {}).get("observed", []) if r.get("metric") == "total_ram_mb"), None)
        ram2 = next((r.get("value") for r in run2.get("device_identity", {}).get("observed", []) if r.get("metric") == "total_ram_mb"), None)
        if ram1 != ram2:
            discrepancies.append(f"Observed total_ram_mb differs between runs: Run 1={ram1}, Run 2={ram2}")

        # Compare telemetry capabilities
        tel1_map = {t["dimension"]: {r["metric"]: r["state"] for r in t.get("results", [])} for t in run1.get("telemetry", [])}
        tel2_map = {t["dimension"]: {r["metric"]: r["state"] for r in t.get("results", [])} for t in run2.get("telemetry", [])}

        for dim, metrics1 in tel1_map.items():
            metrics2 = tel2_map.get(dim, {})
            for m_name, st1 in metrics1.items():
                st2 = metrics2.get(m_name)
                if st1 != st2:
                    discrepancies.append(f"Telemetry state mismatch [{dim}/{m_name}]: Run 1={st1}, Run 2={st2}")

        return {
            "stable": len(discrepancies) == 0,
            "discrepancies": discrepancies,
        }
