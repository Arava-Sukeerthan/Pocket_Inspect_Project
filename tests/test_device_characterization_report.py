"""
Unit tests for Step 10D Device Characterization Report Generator and Schema Validation after Post-Merge Audit.

Validates findings F-02, F-05, F-14:
- F-02: Date mismatch between run_id and started_at date is rejected.
- F-05: Verified records without real evidence files on disk fail validation.
- F-14: Overwriting existing characterization.json raises FileExistsError.
"""

import hashlib
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

    # Now create the evidence file and manifest.json -> validation passes
    ev_dir = output_dir / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    content = b"sample evidence data"
    (ev_dir / "non_existent.txt").write_bytes(content)
    manifest_data = [{
        "relative_path": "evidence/non_existent.txt",
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "created_at": "2026-10-05T10:00:02Z"
    }]
    manifest_bytes = json.dumps(manifest_data, indent=2).encode("utf-8")
    (ev_dir / "manifest.json").write_bytes(manifest_bytes)
    record["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
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


def test_r09_battery_current_ambiguous_unit_and_safety():
    """R-09: Unit safety for battery current. Unannotated ambiguous units must NOT be marked VERIFIED."""
    from src.monitoring.characterization.collectors import BatteryTelemetryCollector, RuntimeState, ReportStatus

    collector = BatteryTelemetryCollector()

    # 1. Explicit mA -> interface demonstrated, but sign convention / update rate are not checked in Step 10D:
    #    REQUIRES PILOT VALIDATION, never VERIFIED (correction round, protocol §3 VERIFIED definition).
    res_ma = collector.collect({"battery_current_now": 150, "battery_current_unit": "mA", "is_real_device_observation": True})
    curr_res = next(r for r in res_ma.results if r.metric == "battery_current_now")
    assert curr_res.value == 150.0
    assert curr_res.verified is False
    assert curr_res.report_status == ReportStatus.REQUIRES_PILOT_VALIDATION.value

    # 2. Explicit uA -> converted to mA, same classification
    res_ua = collector.collect({"battery_current_now": 150000, "battery_current_unit": "uA", "is_real_device_observation": True})
    curr_res = next(r for r in res_ua.results if r.metric == "battery_current_now")
    assert curr_res.value == 150.0
    assert curr_res.verified is False
    assert curr_res.report_status == ReportStatus.REQUIRES_PILOT_VALIDATION.value

    # 3. Ambiguous 5000 (no unit metadata) -> MUST NOT be marked VERIFIED!
    res_amb = collector.collect({"battery_current_now": 5000, "is_real_device_observation": True})
    curr_res = next(r for r in res_amb.results if r.metric == "battery_current_now")
    assert curr_res.value == 5000.0
    assert curr_res.verified is False  # UNVERIFIED
    assert curr_res.report_status == ReportStatus.AVAILABLE.value

    # 4. Zero current with known unit -> UNVERIFIED
    res_zero = collector.collect({"battery_current_now": 0, "battery_current_unit": "mA", "is_real_device_observation": True})
    curr_res = next(r for r in res_zero.results if r.metric == "battery_current_now")
    assert curr_res.value == 0.0
    assert curr_res.verified is False  # UNVERIFIED

    # 5. Missing current -> NOT_TESTED
    res_miss = collector.collect({})
    curr_res = next(r for r in res_miss.results if r.metric == "battery_current_now")
    assert curr_res.state == RuntimeState.NOT_TESTED.value

    # 6. Malformed current ("abc") -> ERROR
    res_mal = collector.collect({"battery_current_now": "abc", "battery_current_unit": "mA", "is_real_device_observation": True})
    curr_res = next(r for r in res_mal.results if r.metric == "battery_current_now")
    assert curr_res.state == RuntimeState.ERROR.value
    assert curr_res.verified is False
    assert "Malformed" in (curr_res.error_message or "")

    # 7. Implausibly large current (1,000,000 mA) -> ERROR
    res_large = collector.collect({"battery_current_now": 1000000, "battery_current_unit": "mA", "is_real_device_observation": True})
    curr_res = next(r for r in res_large.results if r.metric == "battery_current_now")
    assert curr_res.state == RuntimeState.ERROR.value
    assert curr_res.verified is False


def test_p07_probe_failure_semantics_e2e(tmp_path):
    """P-07: Verify that failed attempted probes return state ERROR across all dimensions."""
    import unittest.mock
    from scripts.device_characterization.adb_collector import ADBCollector
    from src.monitoring.characterization.collectors import (
        DeviceIdentityCollector,
        AndroidCapabilityCollector,
        MemoryTelemetryCollector,
        CPUTelemetryCollector,
        GPUTelemetryCollector,
        BatteryTelemetryCollector,
        RuntimeState,
    )

    adb = ADBCollector(device_id="FAILURE_DEVICE_01")

    # Force all probes to fail
    def mock_failing_adb_cmd(args):
        cmd_str = " ".join(args)
        return 1, "", f"Command failed: {cmd_str}"

    with unittest.mock.patch.object(adb, "_adb_cmd", side_effect=mock_failing_adb_cmd):
        with unittest.mock.patch.object(adb, "read_file", return_value=(False, "Read error")):
            _, props = adb.collect_raw_evidence_and_observations(tmp_path)

            # DeviceIdentity: getprop & meminfo failed
            id_collector = DeviceIdentityCollector()
            dev_id = id_collector.collect(props)
            mfr_res = next(r for r in dev_id.observed if r.metric == "manufacturer")
            ram_res = next(r for r in dev_id.observed if r.metric == "total_ram_mb")
            assert mfr_res.state == RuntimeState.ERROR.value
            assert ram_res.state == RuntimeState.ERROR.value

            # AndroidCapability: getprop failed
            android_collector = AndroidCapabilityCollector()
            android_cap = android_collector.collect(props)
            api_res = next(r for r in android_cap.results if r.metric == "api_level")
            assert api_res.state == RuntimeState.ERROR.value

            # Memory: meminfo failed
            mem_collector = MemoryTelemetryCollector()
            mem_cap = mem_collector.collect(props)
            avail_res = next(r for r in mem_cap.results if r.metric == "available_memory_mb")
            assert avail_res.state == RuntimeState.ERROR.value

            # CPU: cpufreq failed
            cpu_collector = CPUTelemetryCollector()
            cpu_cap = cpu_collector.collect(props)
            freq_res = next(r for r in cpu_cap.results if r.metric == "cpu_scaling_cur_freq")
            assert freq_res.state == RuntimeState.ERROR.value

            # GPU: kgsl failed
            gpu_collector = GPUTelemetryCollector()
            gpu_cap = gpu_collector.collect(props)
            gpu_clk_res = next(r for r in gpu_cap.results if r.metric == "gpu_clock_hz")
            assert gpu_clk_res.state == RuntimeState.ERROR.value

            # Battery: dumpsys battery failed
            bat_collector = BatteryTelemetryCollector()
            bat_cap = bat_collector.collect(props)
            bat_lvl_res = next(r for r in bat_cap.results if r.metric == "battery_level_percent")
            assert bat_lvl_res.state == RuntimeState.ERROR.value

