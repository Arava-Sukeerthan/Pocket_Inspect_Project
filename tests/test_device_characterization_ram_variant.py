"""
R-08 RAM variant check (approved 2026-10-06): nearest nominal capacity in MiB, ties AMBIGUOUS,
only a 3 GB nearest variant is VERIFIED, any other outcome blocks Step 10D sign-off.

The end-to-end tests patch only the ADB transport and the connection state; the parser, collectors,
report generator and validation are the production code. All device values here are synthetic.
"""

import datetime
import json
import re
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from scripts.device_characterization.adb_collector import ADBCollector
from scripts.device_characterization.run_characterization import run_characterization
from src.monitoring.characterization.collectors import DeviceIdentityCollector
from src.monitoring.characterization.ram_variant import (
    AMBIGUOUS, INVALID, MATCH, MISMATCH, classify_ram_variant, load_ram_variant_spec,
)
from src.monitoring.characterization.report_generator import (
    CharacterizationReportGenerator, evaluate_variant_signoff,
)

CONFIG = Path("configs/device_characterization.yaml")
SPEC = load_ram_variant_spec()


# ---------------------------------------------------------------------------
# Specification
# ---------------------------------------------------------------------------

def test_approved_specification_in_config():
    spec = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["ram_variant_check"]
    assert spec == {"unit": "MiB", "required_variant": "3 GB",
                    "nominal_ram_mib": {"3 GB": 3072, "4 GB": 4096, "6 GB": 6144}}


def test_protocol_states_the_configured_values():
    protocol = Path("research/experiments/device_characterization_protocol.md").read_text(encoding="utf-8")
    bullet = next(line for line in protocol.splitlines() if line.startswith("- **Variant check parameters (R-08"))
    for name, mib in SPEC["nominal_ram_mib"].items():
        assert f"{name} = {mib}" in bullet
    assert "an observed value of 3584 or 5120" in bullet
    assert "in MiB" in bullet
    assert "`ram_variant_check`" in bullet


def test_no_fixed_window_remains_in_collector():
    src = Path("src/monitoring/characterization/collectors.py").read_text(encoding="utf-8")
    assert not re.search(r"2700\s*<=|<=\s*3300|2400\s*<=|<=\s*3500", src)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ram, classification, nearest, nominal", [
    (3072, MATCH, "3 GB", 3072),
    (4096, MISMATCH, "4 GB", 4096),
    (6144, MISMATCH, "6 GB", 6144),
    (3583, MATCH, "3 GB", 3072),
    (3585, MISMATCH, "4 GB", 4096),
    (5119, MISMATCH, "4 GB", 4096),
    (5121, MISMATCH, "6 GB", 6144),
    (2642, MATCH, "3 GB", 3072),
    (2000, MATCH, "3 GB", 3072),
    (1, MATCH, "3 GB", 3072),
    (6145, MISMATCH, "6 GB", 6144),
    (12288, MISMATCH, "6 GB", 6144),
])
def test_nearest_nominal_classification(ram, classification, nearest, nominal):
    cls = classify_ram_variant(ram, SPEC)
    assert cls["classification"] == classification
    assert cls["nearest_variant"] == nearest
    assert cls["nominal_ram_mib"] == nominal
    assert cls["observed_ram_mib"] == ram
    assert cls["required_variant"] == "3 GB"
    assert cls["unit"] == "MiB"


@pytest.mark.parametrize("ram, tied", [(3584, ["3 GB", "4 GB"]), (5120, ["4 GB", "6 GB"])])
def test_midpoint_tie_is_ambiguous(ram, tied):
    cls = classify_ram_variant(ram, SPEC)
    assert cls["classification"] == AMBIGUOUS
    assert cls["nearest_variant"] is None
    assert cls["nominal_ram_mib"] is None
    assert cls["tied_variants"] == tied


@pytest.mark.parametrize("ram", [0, -1, -3072, None, "2642", True])
def test_non_positive_or_non_numeric_is_invalid(ram):
    cls = classify_ram_variant(ram, SPEC)
    assert cls["classification"] == INVALID
    assert cls["nearest_variant"] is None


# ---------------------------------------------------------------------------
# Collector records
# ---------------------------------------------------------------------------

def _variant(props):
    return DeviceIdentityCollector(ram_variant_spec=SPEC).collect(props).variant_check


@pytest.mark.parametrize("ram", [2642, 3072, 3583])
def test_3gb_nearest_is_verified_with_host_evidence(ram):
    vc = _variant({"is_real_device_observation": True, "total_ram_mb": ram})
    assert vc.state == "AVAILABLE"
    assert vc.report_status == "VERIFIED"
    assert vc.verified is True
    assert vc.value["nearest_variant"] == "3 GB"
    assert vc.value["observed_ram_mib"] == ram
    assert vc.value["nominal_ram_mib"] == 3072
    assert vc.evidence_ref == "evidence/meminfo_evidence.txt#ram_variant_check"


def test_3gb_from_app_fallback_cites_app_evidence():
    vc = _variant({"is_real_device_observation": True, "total_ram_mb": 2642, "total_ram_mb_is_app_derived": True})
    assert vc.verified is True
    assert vc.evidence_ref == "evidence/android_app_evidence.json#total_ram_mb"


def test_3gb_nearest_without_real_device_is_not_verified():
    vc = _variant({"is_real_device_observation": False, "total_ram_mb": 2642})
    assert vc.state == "AVAILABLE"
    assert vc.verified is False
    assert vc.report_status != "VERIFIED"
    assert vc.evidence_ref is None


@pytest.mark.parametrize("ram, nearest", [(3585, "4 GB"), (4096, "4 GB"), (5121, "6 GB"), (6144, "6 GB"), (12288, "6 GB")])
def test_other_variant_is_mismatch_not_error(ram, nearest):
    vc = _variant({"is_real_device_observation": True, "total_ram_mb": ram})
    assert vc.state == "AVAILABLE"
    assert vc.report_status == "AVAILABLE"
    assert vc.verified is False
    assert vc.error_message is None
    assert vc.value["classification"] == MISMATCH
    assert vc.value["nearest_variant"] == nearest
    assert vc.value["observed_ram_mib"] == ram
    assert "Blocks Step 10D sign-off" in vc.notes
    assert vc.evidence_ref == "evidence/meminfo_evidence.txt#ram_variant_check"


@pytest.mark.parametrize("ram", [3584, 5120])
def test_tie_is_ambiguous_not_verified(ram):
    vc = _variant({"is_real_device_observation": True, "total_ram_mb": ram})
    assert vc.state == "AVAILABLE"
    assert vc.verified is False
    assert vc.report_status == "AVAILABLE"
    assert vc.value["classification"] == AMBIGUOUS
    assert vc.value["nearest_variant"] is None


@pytest.mark.parametrize("ram", [0, -5])
def test_non_positive_ram_is_error_without_value(ram):
    vc = _variant({"is_real_device_observation": True, "total_ram_mb": ram})
    assert vc.state == "ERROR"
    assert vc.value is None
    assert vc.verified is False
    assert "cannot be classified" in vc.error_message


def test_missing_ram_keeps_not_tested():
    vc = _variant({"is_real_device_observation": True})
    assert vc.state == "NOT_TESTED"
    assert vc.value is None


# ---------------------------------------------------------------------------
# Sign-off gate
# ---------------------------------------------------------------------------

def _record(ram, real=True):
    ident = DeviceIdentityCollector(ram_variant_spec=SPEC).collect(
        {"is_real_device_observation": real, "total_ram_mb": ram} if ram is not None else {"is_real_device_observation": real}
    )
    return {"device_identity": ident.to_dict(), "conditions": {"adb_connected": real}}


@pytest.mark.parametrize("ram, allowed", [
    (2642, True), (3583, True), (3584, False), (3585, False), (4096, False), (5120, False), (6144, False), (0, False), (None, False),
])
def test_signoff_requires_verified_3gb(ram, allowed):
    gate = evaluate_variant_signoff(_record(ram))
    assert gate["signoff_allowed"] is allowed
    assert gate["required_variant"] == "3 GB"


def test_signoff_blocked_without_real_device():
    assert evaluate_variant_signoff(_record(2642, real=False))["signoff_allowed"] is False


def test_repeat_comparison_reports_signoff_separately_from_stability():
    gen = CharacterizationReportGenerator()

    def run(ram, date, boot):
        r = _record(ram)
        r.update(started_at=f"{date}T10:00:00Z", telemetry=[])
        r["conditions"] = {"adb_connected": True, "boot_id": boot}
        return r

    ok = gen.compare_repeat_runs(run(2642, "2026-10-07", "b1"), run(2642, "2026-10-08", "b2"))
    assert ok["stable"] is True and ok["signoff_allowed"] is True

    mismatch = gen.compare_repeat_runs(run(4096, "2026-10-07", "b1"), run(4096, "2026-10-08", "b2"))
    assert mismatch["stable"] is True          # repeatability meaning unchanged
    assert mismatch["signoff_allowed"] is False
    assert mismatch["variant_signoff"]["run1"]["classification"] == MISMATCH


# ---------------------------------------------------------------------------
# End to end: synthetic ADB transport -> production pipeline -> characterization.json
# ---------------------------------------------------------------------------

def _run_with_memtotal(tmp_path, memtotal_kb, fail=()):
    adb = ADBCollector(device_id="SYNTHETIC_R08")

    def transport(args):
        cmd = " ".join(args)
        if any(f in cmd for f in fail):
            return 1, "", f"synthetic failure: {cmd}"
        if cmd == "shell getprop":
            return 0, "[ro.product.manufacturer]: [OPPO]\n[ro.product.model]: [CPH1931]\n[ro.build.version.sdk]: [29]\n", ""
        if "/proc/meminfo" in cmd:
            return 0, f"MemTotal:        {memtotal_kb} kB\nMemAvailable:    1000000 kB\n", ""
        if "boot_id" in cmd:
            return 0, "synthetic_boot_r08\n", ""
        return 1, "", "No such file or directory"

    run_id = f"run_{datetime.datetime.utcnow().strftime('%Y%m%d')}_170000"
    with patch.object(adb, "_adb_cmd", side_effect=transport):
        with patch("scripts.device_characterization.run_characterization.ADBCollector", return_value=adb):
            with patch.object(adb, "get_connection_status", return_value="CONNECTED"):
                out_dir, _ = run_characterization(CONFIG, run_id=run_id, overwrite=True, results_dir=tmp_path)
    data = json.loads((out_dir / "characterization.json").read_text(encoding="utf-8"))
    readme = (out_dir / "README.md").read_text(encoding="utf-8")
    return data, readme


def test_e2e_2642_mib_is_verified_3gb_and_signoff_allowed(tmp_path):
    data, readme = _run_with_memtotal(tmp_path, 2642 * 1024 + 512)   # floor(kB/1024) = 2642 MiB
    vc = data["device_identity"]["variant_check"]
    assert vc["report_status"] == "VERIFIED" and vc["verified"] is True
    assert vc["value"] == {"classification": "MATCH", "nearest_variant": "3 GB", "observed_ram_mib": 2642,
                           "nominal_ram_mib": 3072, "required_variant": "3 GB", "unit": "MiB"}
    assert vc["evidence_ref"] == "evidence/meminfo_evidence.txt#ram_variant_check"
    assert data["run_status"] == "COMPLETE"
    assert "**Variant sign-off**: `ALLOWED`" in readme


def test_e2e_4gb_mismatch_blocks_signoff_but_not_run_status(tmp_path):
    data, readme = _run_with_memtotal(tmp_path, 3700 * 1024)
    vc = data["device_identity"]["variant_check"]
    assert vc["state"] == "AVAILABLE" and vc["verified"] is False
    assert vc["value"]["classification"] == "MISMATCH" and vc["value"]["nearest_variant"] == "4 GB"
    assert data["run_status"] == "COMPLETE"
    assert "**Variant sign-off**: `BLOCKED`" in readme


def test_e2e_meminfo_failure_is_not_a_mismatch(tmp_path):
    data, readme = _run_with_memtotal(tmp_path, 2642 * 1024, fail=("/proc/meminfo",))
    vc = data["device_identity"]["variant_check"]
    assert vc["state"] == "NOT_TESTED"
    assert vc["value"] is None
    assert data["run_status"] == "FAILED"     # meminfo is a mandatory probe (P5-05), unchanged
    assert "**Variant sign-off**: `BLOCKED`" in readme
