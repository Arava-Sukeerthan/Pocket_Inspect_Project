"""
Unit tests for Step 10D Device Characterization Report Generator and Schema Validation after Post-Merge Audit.

Validates findings F-02, F-05, F-14:
- F-02: Date mismatch between run_id and started_at date is rejected.
- F-05: Verified records without real evidence files on disk fail validation.
- F-14: Overwriting existing characterization.json raises FileExistsError.
"""

import json
import pytest
from pathlib import Path
from src.monitoring.characterization.models import (
    CapabilityResult,
    RuntimeState,
    ReportStatus,
    DeviceIdentity,
    KnownSpecification,
    TelemetryCapability,
    ThermalCapability,
    EnergyCapability,
    CharacterizationRun,
)
from src.monitoring.characterization.report_generator import (
    CharacterizationReportGenerator,
    validate_characterization_record,
)
from scripts.device_characterization.run_characterization import run_characterization

ROOT = Path(__file__).resolve().parent.parent


def _build_dummy_run_record(run_id="run_20261005_100000", is_dry_run=True):
    res_avail = CapabilityResult(
        metric="battery_voltage",
        state=RuntimeState.AVAILABLE.value,
        report_status=ReportStatus.AVAILABLE.value,
        value=3850.0,
        unit="mV",
        source="sysfs",
        verified=False,
    )
    res_unavail = CapabilityResult(
        metric="gpu_utilization",
        state=RuntimeState.UNAVAILABLE.value,
        report_status=ReportStatus.UNAVAILABLE.value,
        value=None,
        unit="percent",
        source="sysfs",
        error_message="Sysfs node not present",
        verified=False,
    )
    dummy_spec = KnownSpecification()
    dummy_identity = DeviceIdentity(
        device_unit_id="OPPO_CPH2015_001",
        known_specification=dummy_spec,
        observed=[res_avail],
        variant_check=res_avail,
    )
    dummy_telemetry = [
        TelemetryCapability(
            dimension="battery",
            results=[res_avail, res_unavail],
            resource_state_input=False,
        )
    ]
    dummy_thermal = ThermalCapability(
        thermal_status_api=res_unavail,
        temperature_sources=[res_avail],
        frequency_capping_observable=res_unavail,
        external_surface_probe=res_unavail,
    )
    dummy_energy = EnergyCapability(
        E1_battery_side_reference=res_unavail,
        E2_supply_powered_session=res_unavail,
        E3_software_counters=res_avail,
        selected_level="E-3",
        absolute_energy_claimed=False,
    )
    run = CharacterizationRun(
        run_id=run_id,
        started_at="2026-10-05T10:00:00Z",
        app_version="1.0.0-characterization",
        git_commit="3a60717",
        device_identity=dummy_identity,
        telemetry=dummy_telemetry,
        camera=[],
        backends=[],
        profiling=[],
        thermal=dummy_thermal,
        energy=dummy_energy,
        conditions={
            "ambient_temperature_c": 25.0,
            "adb_connected": not is_dry_run,
            "is_dry_run": is_dry_run,
        },
    )
    return run.to_dict()


def test_validate_characterization_record_schema():
    """Test schema validation against device_characterization_schema.json."""
    valid_record = _build_dummy_run_record("run_20261005_100000")
    errors = validate_characterization_record(valid_record)
    assert errors == []

    # Inject fake zero into unavailable metric
    invalid_record = _build_dummy_run_record("run_20261005_100001")
    invalid_record["telemetry"][0]["results"][1]["value"] = 0.0  # fake zero!
    errors = validate_characterization_record(invalid_record)
    assert len(errors) > 0
    assert any("violates no-fake-zeros rule" in err for err in errors)


def test_f05_verified_requires_existing_evidence_file(tmp_path):
    """F-05: verified=True requires that evidence_ref points to an existing file on disk."""
    record = _build_dummy_run_record("run_20261005_100002", is_dry_run=False)
    # Mark a metric as verified with a non-existent evidence file
    record["device_identity"]["observed"][0]["verified"] = True
    record["device_identity"]["observed"][0]["report_status"] = "VERIFIED"
    record["device_identity"]["observed"][0]["evidence_ref"] = "evidence/non_existent.txt#key"
    record["conditions"]["adb_connected"] = True
    record["conditions"]["is_dry_run"] = False

    output_dir = tmp_path / "run_20261005_100002"
    output_dir.mkdir(parents=True)
    errors = validate_characterization_record(record, output_dir=output_dir)
    assert len(errors) > 0
    assert any("does not exist on disk" in err for err in errors)

    # Now create the evidence file -> validation passes
    ev_dir = output_dir / "evidence"
    ev_dir.mkdir(parents=True)
    (ev_dir / "non_existent.txt").write_text("sample evidence data", encoding="utf-8")
    errors_ok = validate_characterization_record(record, output_dir=output_dir)
    assert errors_ok == []


def test_f14_process_run_overwrite_guard(tmp_path):
    """F-14: process_run into an existing run directory raises FileExistsError."""
    generator = CharacterizationReportGenerator()
    record = _build_dummy_run_record("run_20261005_100003")
    output_dir = tmp_path / "run_20261005_100003"
    
    # First pass: succeeds
    res1 = generator.process_run(record, output_dir=output_dir)
    assert res1["status"] == "VALID"
    assert (output_dir / "characterization.json").exists()

    # Second pass into same directory without overwrite=True: raises FileExistsError
    with pytest.raises(FileExistsError, match="Silent overwrite is refused"):
        generator.process_run(record, output_dir=output_dir)


def test_f02_date_mismatch_rejection(tmp_path):
    """F-02: run_id with date mismatch against actual start time date raises ValueError."""
    cfg_path = ROOT / "configs" / "device_characterization.yaml"
    # Passing run_id with future date (e.g. 20991231) raises ValueError
    with pytest.raises(ValueError, match="does not match actual start time date"):
        run_characterization(cfg_path, run_id="run_20991231_100000", dry_run=True, results_dir=tmp_path)
