"""
RAM variant classification for the Step 10D variant check (R-08, protocol §2).

The specification (nominal capacities, unit, required variant) is read from
`configs/device_characterization.yaml` (`ram_variant_check`); this module holds no numeric values.

Rule (approved by the researcher on 2026-10-06):
- The observed RAM (MiB) is compared with every nominal capacity (MiB).
- The candidate variant is the one at the smallest absolute distance.
- An exact tie between two nominals is AMBIGUOUS and is never assigned to either variant.
- Nearest == required variant -> MATCH; nearest == any other variant -> MISMATCH.
- A non-positive or non-numeric observation is INVALID (it cannot be classified).

Nominal capacities are classification references, not measurements.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = ROOT / "configs" / "device_characterization.yaml"

MATCH = "MATCH"
MISMATCH = "MISMATCH"
AMBIGUOUS = "AMBIGUOUS"
INVALID = "INVALID"


def load_ram_variant_spec(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Loads and checks the `ram_variant_check` block of the device characterization config."""
    with open(config_path or CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    spec = cfg.get("ram_variant_check")
    if not spec:
        raise ValueError(f"'ram_variant_check' is not defined in {config_path or CONFIG_PATH}")
    return validate_ram_variant_spec(spec)


def validate_ram_variant_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    nominal = spec.get("nominal_ram_mib")
    required = spec.get("required_variant")
    if spec.get("unit") != "MiB":
        raise ValueError("ram_variant_check.unit must be 'MiB'")
    if not isinstance(nominal, dict) or len(nominal) < 2:
        raise ValueError("ram_variant_check.nominal_ram_mib must map at least two variants to MiB")
    for name, value in nominal.items():
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"nominal capacity for {name!r} must be a positive integer MiB value")
    if required not in nominal:
        raise ValueError("ram_variant_check.required_variant must be one of nominal_ram_mib")
    return spec


def classify_ram_variant(observed_ram_mib: Any, spec: Dict[str, Any]) -> Dict[str, Any]:
    """Classifies an observed RAM value (MiB) against the nominal variant capacities.

    Returns a dict with `classification` (MATCH, MISMATCH, AMBIGUOUS or INVALID), `nearest_variant`,
    `observed_ram_mib`, `nominal_ram_mib`, `required_variant`, `unit` and, for a tie, `tied_variants`.
    """
    nominal: Dict[str, int] = spec["nominal_ram_mib"]
    required = spec["required_variant"]
    result: Dict[str, Any] = {
        "classification": INVALID,
        "nearest_variant": None,
        "observed_ram_mib": observed_ram_mib,
        "nominal_ram_mib": None,
        "required_variant": required,
        "unit": "MiB",
    }
    if isinstance(observed_ram_mib, bool) or not isinstance(observed_ram_mib, (int, float)) or observed_ram_mib <= 0:
        return result

    distances = {name: abs(observed_ram_mib - value) for name, value in nominal.items()}
    best = min(distances.values())
    nearest = sorted(name for name, d in distances.items() if d == best)
    if len(nearest) > 1:
        result["classification"] = AMBIGUOUS
        result["tied_variants"] = nearest
        return result

    variant = nearest[0]
    result["nearest_variant"] = variant
    result["nominal_ram_mib"] = nominal[variant]
    result["classification"] = MATCH if variant == required else MISMATCH
    return result
