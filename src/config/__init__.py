"""
Config module: confirmatory-readiness guard for configuration files under `configs/`.
"""
from src.config.confirmatory_guard import (
    UnresolvedConfigError,
    confirmatory_blockers,
    load_confirmatory_config,
    require_confirmatory_ready,
)

__all__ = [
    "UnresolvedConfigError",
    "confirmatory_blockers",
    "load_confirmatory_config",
    "require_confirmatory_ready",
]
