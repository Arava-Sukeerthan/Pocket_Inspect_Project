"""
Tests for the confirmatory-readiness guard (`src.config`).

`configs/default_config.yaml` is a Phase 1 scaffold whose confidence, thermal and battery values are unresolved
placeholders. A confirmatory load must reject it, and the guard must fail closed on a missing status block.
"""
from pathlib import Path

import pytest
import yaml

from src.config import (
    UnresolvedConfigError,
    confirmatory_blockers,
    load_confirmatory_config,
    require_confirmatory_ready,
)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "configs" / "default_config.yaml"
PLACEHOLDER_KEYS = {
    "uncertainty.confidence_threshold",
    "adaptation.thermal_limit_celsius",
    "adaptation.battery_low_threshold_pct",
}
READY = {"config_status": {"confirmatory_ready": True, "unresolved_placeholders": {}}}


def _default():
    return yaml.safe_load(DEFAULT_CONFIG.read_text(encoding="utf-8"))


def test_default_config_declares_the_three_placeholders():
    status = _default()["config_status"]
    assert status["confirmatory_ready"] is False
    assert set(status["unresolved_placeholders"]) == PLACEHOLDER_KEYS


def test_declared_placeholder_keys_exist_in_default_config():
    config = _default()
    for dotted in config["config_status"]["unresolved_placeholders"]:
        section, key = dotted.split(".")
        assert key in config[section], dotted


def test_default_config_rejected_for_confirmatory_use():
    with pytest.raises(UnresolvedConfigError) as excinfo:
        load_confirmatory_config(DEFAULT_CONFIG)
    for key in PLACEHOLDER_KEYS:
        assert key in str(excinfo.value)


@pytest.mark.parametrize("config", [
    None,
    [],
    {},
    {"uncertainty": {"confidence_threshold": 0.5}},
    {"config_status": "ready"},
    {"config_status": {"confirmatory_ready": True}},
    {"config_status": {"confirmatory_ready": "true", "unresolved_placeholders": {}}},
    {"config_status": {"confirmatory_ready": False, "unresolved_placeholders": {}}},
    {"config_status": {"confirmatory_ready": True, "unresolved_placeholders": {"a.b": "pending"}}},
])
def test_guard_fails_closed(config):
    assert confirmatory_blockers(config)
    with pytest.raises(UnresolvedConfigError):
        require_confirmatory_ready(config)


def test_resolved_config_accepted(tmp_path):
    assert confirmatory_blockers(READY) == []
    path = tmp_path / "resolved.yaml"
    path.write_text(yaml.safe_dump(READY), encoding="utf-8")
    assert load_confirmatory_config(path) == READY


def test_guard_does_not_modify_the_config():
    config = _default()
    with pytest.raises(UnresolvedConfigError):
        require_confirmatory_ready(config)
    assert config == _default()
