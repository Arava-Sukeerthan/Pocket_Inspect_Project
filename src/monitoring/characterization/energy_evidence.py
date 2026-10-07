"""
Researcher-provided energy-feasibility evidence for Step 10D (protocol §6, D-16).

E-1 (battery-side external reference) and E-2 (supply-powered external session) are physical checks done by the
researcher. This module only loads and validates the researcher's file
(template: configs/energy_feasibility_evidence_template.yaml); it never fills, infers or defaults a field.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

LEVEL_KEYS = ("E1_battery_side_reference", "E2_supply_powered_session")
_BOOL_FIELDS = {
    "E1_battery_side_reference": ("assessed", "reference_validated", "safety_signoff"),
    "E2_supply_powered_session": ("assessed", "reference_validated", "non_charging_verified"),
}
# Researcher evidence files listed per level; every listed file must exist and is copied into the run.
EVIDENCE_LIST_FIELDS = ("evidence_files", "non_charging_evidence_files")
# Instrument field each level must name before it can be selected.
_INSTRUMENT_FIELD = {"E1_battery_side_reference": "instrument_model", "E2_supply_powered_session": "meter_model"}


def validate_energy_evidence(data: Any) -> List[str]:
    """Returns a list of problems; an empty list means the file is structurally valid."""
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["energy feasibility evidence must be a mapping"]
    for key in LEVEL_KEYS:
        level = data.get(key)
        if not isinstance(level, dict):
            errors.append(f"{key}: missing section")
            continue
        for field in _BOOL_FIELDS[key]:
            if not isinstance(level.get(field), bool):
                errors.append(f"{key}.{field} must be true or false")
        for field in EVIDENCE_LIST_FIELDS:
            if field in level and not isinstance(level.get(field), list):
                errors.append(f"{key}.{field} must be a list of file paths")
        if level.get("assessed") is True:
            if level.get("feasible") not in (True, False):
                errors.append(f"{key}.feasible must be true or false once assessed")
            for field in ("assessed_by", "assessed_on"):
                if not level.get(field):
                    errors.append(f"{key}.{field} is required once assessed")
            if not isinstance(level.get("evidence_files"), list) or not level.get("evidence_files"):
                errors.append(f"{key}.evidence_files must list at least one file once assessed")
        if level.get("reference_validated") is True and level.get("feasible") is not True:
            errors.append(f"{key}.reference_validated cannot be true unless feasible is true")
        if key == "E1_battery_side_reference" and level.get("reference_validated") is True \
                and level.get("safety_signoff") is not True:
            # Protocol §8: battery-terminal work requires the researcher's safety decision before it is attempted.
            errors.append(f"{key}.reference_validated cannot be true without safety_signoff (protocol §8)")
        if key == "E2_supply_powered_session" and level.get("non_charging_verified") is True \
                and not level.get("non_charging_evidence_files"):
            errors.append(f"{key}.non_charging_verified requires non_charging_evidence_files "
                          "(battery status and current logs of the supply-powered session, protocol §6)")
    return errors


def unmet_selection_requirements(key: str, level: Optional[Dict[str, Any]]) -> List[str]:
    """Every requirement level `key` still misses before it may be SELECTED (empty list = selectable).

    E-1: assessed, feasible, reference_validated, safety_signoff, assessed_by, assessed_on, instrument_model and at
    least one evidence file. E-2: assessed, feasible, reference_validated, non_charging_verified, assessed_by,
    assessed_on, meter_model, at least one evidence file and at least one non-charging evidence file.
    Software never fills any of these; a missing field is an unmet requirement.
    """
    level = level if isinstance(level, dict) else {}
    flags = ["assessed", "feasible", "reference_validated"]
    flags.append("safety_signoff" if key == "E1_battery_side_reference" else "non_charging_verified")
    missing = [f for f in flags if level.get(f) is not True]
    missing += [f for f in ("assessed_by", "assessed_on", _INSTRUMENT_FIELD[key]) if not level.get(f)]
    lists = ["evidence_files"] + (["non_charging_evidence_files"] if key == "E2_supply_powered_session" else [])
    missing += [f for f in lists if not isinstance(level.get(f), list) or not level.get(f)]
    return missing


def selection_basis(data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """The researcher fields the selection used, per level, plus the unmet requirements (recorded in the run)."""
    if not isinstance(data, dict):
        return None
    keep = ("assessed", "feasible", "reference_validated", "safety_signoff", "non_charging_verified",
            "assessed_by", "assessed_on", "instrument_model", "meter_model") + EVIDENCE_LIST_FIELDS
    out: Dict[str, Any] = {}
    for key in LEVEL_KEYS:
        level = data.get(key) if isinstance(data.get(key), dict) else {}
        entry = {f: level.get(f) for f in keep if f in level}
        entry["unmet_selection_requirements"] = unmet_selection_requirements(key, level)
        out[key] = entry
    return out


def load_energy_evidence(path: Optional[str], root: Path) -> Dict[str, Any]:
    """Loads the researcher file named in the config.

    Returns {"configured": bool, "path": str|None, "text": str|None, "data": dict|None, "errors": [..]}.
    A missing or invalid file is reported as errors, never replaced by defaults.
    """
    if not path:
        return {"configured": False, "path": None, "text": None, "data": None, "errors": []}
    full = (root / path) if not Path(path).is_absolute() else Path(path)
    if not full.exists():
        return {"configured": True, "path": str(path), "text": None, "data": None,
                "errors": [f"energy feasibility evidence file not found: {path}"]}
    text = full.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return {"configured": True, "path": str(path), "text": text, "data": None, "errors": [f"invalid YAML: {e}"]}
    errors = validate_energy_evidence(data)
    if not errors:
        base = full.parent
        for key in LEVEL_KEYS:
            for field in EVIDENCE_LIST_FIELDS:
                for ef in data[key].get(field) or []:
                    if not (base / ef).exists():
                        errors.append(f"{key}: listed {field} file not found: {ef}")
    return {"configured": True, "path": str(path), "text": text, "data": data if not errors else None,
            "errors": errors}


def select_energy_level(e1: Optional[Dict[str, Any]], e2: Optional[Dict[str, Any]],
                        e3_counters_available: Optional[bool]) -> Optional[str]:
    """D-16 hierarchy. Returns "E-1", "E-2", "E-3" or None; never skips an unassessed preferred level.

    - E-1 is selected only when every E-1 requirement holds (unmet_selection_requirements, incl. safety_signoff).
    - E-1 assessed and feasible but incomplete (e.g. no safety sign-off, not validated): nothing is selected; the
      hierarchy does not fall through to E-2, because E-1 is not ruled out.
    - E-2 is considered only after E-1 is assessed and found not feasible; it is selected only when every E-2
      requirement holds (incl. non-charging verification and its evidence).
    - E-3 only after E-1 and E-2 are both assessed and not feasible, and only with demonstrated software counters.
    """
    if not e1 or e1.get("assessed") is not True:
        return None
    if e1.get("feasible") is True:
        return "E-1" if not unmet_selection_requirements("E1_battery_side_reference", e1) else None
    if e1.get("feasible") is not False:
        return None
    # E-1 assessed and not achievable on this device.
    if not e2 or e2.get("assessed") is not True:
        return None
    if e2.get("feasible") is True:
        return "E-2" if not unmet_selection_requirements("E2_supply_powered_session", e2) else None
    if e2.get("feasible") is not False:
        return None
    # E-1 and E-2 both assessed and not achievable: the software-counter fallback, if demonstrated.
    return "E-3" if e3_counters_available is True else None
