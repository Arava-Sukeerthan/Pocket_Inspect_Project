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
    return errors


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
            for ef in data[key].get("evidence_files") or []:
                if not (base / ef).exists():
                    errors.append(f"{key}: listed evidence file not found: {ef}")
    return {"configured": True, "path": str(path), "text": text, "data": data if not errors else None,
            "errors": errors}


def select_energy_level(e1: Optional[Dict[str, Any]], e2: Optional[Dict[str, Any]],
                        e3_counters_available: Optional[bool]) -> Optional[str]:
    """D-16 hierarchy. Returns "E-1", "E-2", "E-3" or None; never skips an unassessed preferred level."""
    if not e1 or e1.get("assessed") is not True:
        return None
    if e1.get("feasible") is True:
        return "E-1" if e1.get("reference_validated") is True else None
    # E-1 assessed and not achievable on this device.
    if not e2 or e2.get("assessed") is not True:
        return None
    if e2.get("feasible") is True:
        if e2.get("reference_validated") is True and e2.get("non_charging_verified") is True:
            return "E-2"
        return None
    # E-1 and E-2 both assessed and not achievable: the software-counter fallback, if demonstrated.
    return "E-3" if e3_counters_available is True else None
