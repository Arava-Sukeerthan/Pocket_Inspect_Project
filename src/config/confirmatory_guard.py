"""
Confirmatory-readiness guard for configuration files.

A configuration may be used for a confirmatory run only when it declares itself resolved in a `config_status`
block:

    config_status:
      confirmatory_ready: true
      unresolved_placeholders: {}

`unresolved_placeholders` maps a dotted key to the reason it is unresolved. The guard fails closed: a missing or
malformed `config_status` block is rejected. The guard holds no threshold and no key list of its own, and it never
supplies, defaults or replaces a value; which keys are unresolved is declared in the configuration file.

The guard does not decide whether a declared value is correct. Resolving a placeholder is a research decision
recorded in `research/experiments/pre_data_collection_decision_register.md`.
"""
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

STATUS_KEY = "config_status"


class UnresolvedConfigError(ValueError):
    """Raised when a configuration is not ready for confirmatory use."""


def confirmatory_blockers(config: Any) -> List[str]:
    """Reasons `config` cannot be used for a confirmatory run. An empty list means it is ready."""
    if not isinstance(config, dict):
        return ["configuration is not a mapping"]
    status = config.get(STATUS_KEY)
    if not isinstance(status, dict):
        return [f"`{STATUS_KEY}` block is missing or not a mapping"]
    blockers: List[str] = []
    if status.get("confirmatory_ready") is not True:
        blockers.append(f"`{STATUS_KEY}.confirmatory_ready` is not true")
    placeholders = status.get("unresolved_placeholders")
    if not isinstance(placeholders, dict):
        blockers.append(f"`{STATUS_KEY}.unresolved_placeholders` is missing or not a mapping")
    else:
        blockers.extend(f"unresolved placeholder `{key}`: {reason}" for key, reason in placeholders.items())
    return blockers


def require_confirmatory_ready(config: Any, source: str = "configuration") -> None:
    """Raises UnresolvedConfigError when `config` is not ready for confirmatory use."""
    blockers = confirmatory_blockers(config)
    if blockers:
        raise UnresolvedConfigError(f"{source} rejected for confirmatory use: " + "; ".join(blockers))


def load_confirmatory_config(path: Union[str, Path]) -> Dict[str, Any]:
    """Loads a YAML configuration for a confirmatory run, rejecting it when it is not ready."""
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    require_confirmatory_ready(config, source=str(path))
    return config
