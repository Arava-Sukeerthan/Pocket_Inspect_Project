"""
Step 10D §9 criterion 1: device_capability_matrix.md coverage check.

Criterion: "every item in device_capability_matrix.md has a non-default status with evidence".

The authoritative matrix is parsed (it is never modified). Each matrix row is mapped to the report records that
answer it by configs/device_capability_coverage.yaml. A row passes only when every mapped record exists in the
run, has a non-default status (not NOT_TESTED / ERROR / NOT YET VERIFIED) and carries evidence. Rows whose
matrix status is fixed by the specification itself (e.g. "REQUIRES EXTERNAL INSTRUMENTATION") pass on that basis.

Failures are explicit and never suppressed:
- UNMAPPED_ROW: a matrix row with no mapping entry (matrix changed, mapping not updated);
- STALE_MAPPING: a mapping entry for a row that no longer exists in the matrix;
- NO_COLLECTOR: the row has no collector yet (reason recorded in the mapping);
- NOT_IN_APPROVED_SCOPE: the row's `scope` list in configs/device_characterization.yaml is empty (nothing approved
  to characterise). The row still fails: the protocol status vocabulary has no out-of-scope status, so it stays
  NOT YET VERIFIED until the researcher decides how §9 treats it;
- MISSING_RECORD / NOT_TESTED / ERROR / DEFAULT_STATUS / NO_EVIDENCE: per mapped record.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
MATRIX_PATH = ROOT / "research" / "experiments" / "device_capability_matrix.md"
COVERAGE_CONFIG_PATH = ROOT / "configs" / "device_capability_coverage.yaml"
CHARACTERIZATION_CONFIG_PATH = ROOT / "configs" / "device_characterization.yaml"


def _scope_list(dotted: str) -> List[Any]:
    """Value of a dotted key in configs/device_characterization.yaml (must be a list)."""
    node: Any = yaml.safe_load(CHARACTERIZATION_CONFIG_PATH.read_text(encoding="utf-8")) or {}
    for part in dotted.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    if not isinstance(node, list):
        raise ValueError(f"coverage scope '{dotted}' is not a list in {CHARACTERIZATION_CONFIG_PATH.name}")
    return node

DEFAULT_STATUS = "NOT YET VERIFIED"
FAILING_STATES = ("NOT_TESTED", "ERROR")


def _clean(cell: str) -> str:
    cell = re.sub(r"[`*]", "", cell)
    return re.sub(r"\s+", " ", cell).strip()


def parse_matrix(path: Path = MATRIX_PATH) -> List[Dict[str, str]]:
    """Returns one entry per data row of every table in sections 1-9 of the matrix.

    Row id: "<section number>/<first cell>", plus "/<second cell>" in section 3, whose rows are keyed by
    Dimension and Metric. `status` is the cell under the "Status" column.
    """
    rows: List[Dict[str, str]] = []
    section: Optional[str] = None
    header: Optional[List[str]] = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\d+)\.", line)
        if m:
            section = m.group(1)
            header = None
            continue
        if line.startswith("## "):
            section = None
            header = None
            continue
        if not section or not line.startswith("|"):
            if not line.startswith("|"):
                header = None
            continue
        cells = [_clean(c) for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        key_cells = cells[:2] if section == "3" else cells[:1]
        status_idx = header.index("Status") if "Status" in header else None
        rows.append({
            "section": section,
            "row_id": "/".join([section] + key_cells),
            "status": cells[status_idx] if status_idx is not None and status_idx < len(cells) else "",
        })
    return rows


def load_coverage_config(path: Path = COVERAGE_CONFIG_PATH) -> Dict[str, Any]:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg.get("rows"), dict):
        raise ValueError(f"{path}: 'rows' mapping missing")
    return cfg


# ---------------------------------------------------------------------------
# Record resolution
# ---------------------------------------------------------------------------

def _by_metric(results: List[Dict[str, Any]], metric: str) -> List[Dict[str, Any]]:
    return [r for r in results or [] if isinstance(r, dict) and r.get("metric") == metric]


def resolve_records(run: Dict[str, Any], ref: str) -> List[Dict[str, Any]]:
    """Resolves one mapping reference to the matching report records.

    Syntax: identity:<metric> | telemetry:<dimension>/<metric> | thermal:<field> |
    thermal:temperature_sources/<metric> | camera:*/<metric> | backend:<name>/<field> | profiling:<metric> |
    energy:<field>.
    """
    kind, _, rest = ref.partition(":")
    if kind == "identity":
        ident = run.get("device_identity") or {}
        if rest == "variant_check":
            return [ident["variant_check"]] if ident.get("variant_check") else []
        return _by_metric(ident.get("observed"), rest)
    if kind == "telemetry":
        dim, _, metric = rest.partition("/")
        return [r for t in run.get("telemetry") or [] if t.get("dimension") == dim
                for r in _by_metric(t.get("results"), metric)]
    if kind == "thermal":
        thermal = run.get("thermal") or {}
        if rest.startswith("temperature_sources/"):
            return _by_metric(thermal.get("temperature_sources"), rest.split("/", 1)[1])
        return [thermal[rest]] if isinstance(thermal.get(rest), dict) else []
    if kind == "camera":
        _, _, metric = rest.partition("/")
        out: List[Dict[str, Any]] = []
        for cam in run.get("camera") or []:
            if metric == "manual_control_honoured":
                out.append(cam.get("manual_control_honoured"))
            else:
                found = _by_metric(cam.get("results"), metric)
                # A camera lacking the record still counts, as a missing record.
                out.extend(found or [{"metric": metric, "_missing": True, "_camera": cam.get("camera_id")}])
        return [r for r in out if r]
    if kind == "backend":
        name, _, field = rest.partition("/")
        return [b[field] for b in run.get("backends") or [] if b.get("backend") == name and isinstance(b.get(field), dict)]
    if kind == "profiling":
        return _by_metric(run.get("profiling"), rest)
    if kind == "energy":
        energy = run.get("energy") or {}
        return [energy[rest]] if isinstance(energy.get(rest), dict) else []
    raise ValueError(f"Unknown coverage reference kind in '{ref}'")


def _record_problem(rec: Dict[str, Any]) -> Optional[str]:
    if rec.get("_missing"):
        return "MISSING_RECORD"
    if rec.get("state") in FAILING_STATES:
        return rec["state"]
    if rec.get("report_status") in (DEFAULT_STATUS, None):
        return "DEFAULT_STATUS"
    if not rec.get("evidence_ref"):
        return "NO_EVIDENCE"
    return None


def check_matrix_coverage(run: Dict[str, Any], matrix_path: Path = MATRIX_PATH,
                          config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Evaluates §9 criterion 1 for one run record. Returns a machine-readable result."""
    cfg = config if config is not None else load_coverage_config()
    mapping: Dict[str, Any] = cfg["rows"]
    matrix_rows = parse_matrix(matrix_path)
    matrix_ids = {r["row_id"] for r in matrix_rows}
    rows_out: List[Dict[str, Any]] = []

    for row in matrix_rows:
        rid = row["row_id"]
        entry = mapping.get(rid)
        result: Dict[str, Any] = {"row_id": rid, "matrix_status": row["status"], "records": []}
        if entry is None:
            result.update(passed=False, problem="UNMAPPED_ROW")
        elif entry.get("specification_fixed"):
            if row["status"].upper().startswith(DEFAULT_STATUS):
                result.update(passed=False, problem="SPECIFICATION_ROW_HAS_DEFAULT_STATUS")
            else:
                check = entry.get("check")
                ok = True
                if check == "absolute_energy_not_claimed":
                    ok = (run.get("energy") or {}).get("absolute_energy_claimed") is False
                result.update(passed=ok, problem=None if ok else "SPECIFICATION_CHECK_FAILED",
                              basis="matrix status fixed by the specification")
        elif not entry.get("records"):
            in_scope = _scope_list(entry["scope"]) if entry.get("scope") else None
            problem = "NOT_IN_APPROVED_SCOPE" if in_scope == [] else "NO_COLLECTOR"
            result.update(passed=False, problem=problem, reason=entry.get("reason"))
        else:
            problems: List[str] = []
            for ref in entry["records"]:
                found = resolve_records(run, ref)
                if not found:
                    problems.append(f"{ref}: MISSING_RECORD")
                    result["records"].append({"ref": ref, "problem": "MISSING_RECORD"})
                    continue
                for rec in found:
                    prob = _record_problem(rec)
                    result["records"].append({
                        "ref": ref, "metric": rec.get("metric"), "camera_id": rec.get("_camera"),
                        "state": rec.get("state"), "report_status": rec.get("report_status"),
                        "evidence_ref": rec.get("evidence_ref"), "problem": prob,
                    })
                    if prob:
                        problems.append(f"{ref}: {prob}")
            result.update(passed=not problems, problem="; ".join(problems) or None)
        rows_out.append(result)

    for rid in sorted(set(mapping) - matrix_ids):
        rows_out.append({"row_id": rid, "matrix_status": None, "records": [], "passed": False,
                         "problem": "STALE_MAPPING"})

    failed = [r for r in rows_out if not r["passed"]]
    return {
        "criterion": "Step 10D protocol §9 criterion 1: every matrix item has a non-default status with evidence",
        "matrix": str(matrix_path.relative_to(ROOT)) if matrix_path.is_relative_to(ROOT) else str(matrix_path),
        "passed": not failed,
        "rows_total": len(rows_out),
        "rows_passed": len(rows_out) - len(failed),
        "rows_failed": len(failed),
        "rows": rows_out,
    }
