"""
Unit tests for Step 10D Device Characterization Report Generator and Schema Validation.

Validates:
- JsonSchema validation for characterization records.
- Report generation on host.
- Multi-run directory structure preservation and non-overwrite checks.
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

ROOT = Path(__file__).resolve().parent.parent


def _build_dummy_run_record(run_id="run_test_001"):
    res_avail = CapabilityResult(
        metric="battery_voltage",
        state=RuntimeState.AVAILABLE.value,
        report_status=ReportStatus.AVAILABLE.value,
        value=3850.0,
        unit="mV",
        source="sysfs",
    )
    res_unavail = CapabilityResult(
        metric="gpu_utilization",
        state=RuntimeState.UNAVAILABLE.value,
        report_status=ReportStatus.UNAVAILABLE.value,
        value=None,
        unit="percent",
        source="sysfs",
        error_message="Sysfs node not present",
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
        started_at="2026-10-05T12:00:00Z",
        app_version="1.0.0-characterization",
        git_commit="24aa0f0",
        device_identity=dummy_identity,
        telemetry=dummy_telemetry,
        camera=[],
        backends=[],
        profiling=[],
        thermal=dummy_thermal,
        energy=dummy_energy,
        conditions={"ambient_temperature_c": 25.0},
    )
    return run.to_dict()


def test_validate_characterization_record_schema():
    """Test schema validation against device_characterization_schema.json."""
    valid_record = _build_dummy_run_record("run_valid_001")
    errors = validate_characterization_record(valid_record)
    assert errors == []

    # Inject fake zero into unavailable metric
    invalid_record = _build_dummy_run_record("run_invalid_001")
    invalid_record["telemetry"][0]["results"][1]["value"] = 0.0  # fake zero on UNAVAILABLE metric!
    errors = validate_characterization_record(invalid_record)
    assert len(errors) > 0
    assert any("violates no-fake-zeros rule" in err for err in errors)


def test_report_generator_run_creation(tmp_path):
    """Test characterization report generator run directory creation and artifact output."""
    generator = CharacterizationReportGenerator()
    record = _build_dummy_run_record("test_run_001")
    output_dir = tmp_path / "run_test_run_001"
    res = generator.process_run(record, output_dir=output_dir)

    assert res["status"] == "VALID"
    assert output_dir.exists()

    json_path = output_dir / "characterization.json"
    assert json_path.exists()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["run_id"] == "test_run_001"


def test_multi_run_non_overwrite(tmp_path):
    """Verify that multiple characterization runs do not overwrite existing run directories."""
    generator = CharacterizationReportGenerator()
    rec1 = _build_dummy_run_record("run_1_20261005")
    rec2 = _build_dummy_run_record("run_2_20261006")

    dir1 = tmp_path / "run_run_1_20261005"
    dir2 = tmp_path / "run_run_2_20261006"

    res1 = generator.process_run(rec1, output_dir=dir1)
    res2 = generator.process_run(rec2, output_dir=dir2)

    assert dir1.exists()
    assert dir2.exists()
    assert res1["run_file"] != res2["run_file"]
