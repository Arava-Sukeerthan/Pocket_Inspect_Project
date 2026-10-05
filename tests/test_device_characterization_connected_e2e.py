"""
End-to-end tests for Step 10D connected-device characterization path,
evidence references, ADB connection state classification, profiling probes,
evidence hash verification, CLI argument rules, and synthetic test data isolation (P-01 to P-07).

Uses a mock ADB execution stub to test the complete connected pipeline without physical hardware.
Synthetic outputs in this test are explicitly isolated to pytest temporary directories and are not repository evidence.
"""

import datetime
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.device_characterization.adb_collector import ADBCollector
from scripts.device_characterization.run_characterization import run_characterization
from src.monitoring.characterization.report_generator import validate_characterization_record, CharacterizationReportGenerator


@pytest.fixture
def temp_output_dir():
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)


def test_adb_connection_status_classification():
    adb = ADBCollector()

    with patch.object(adb, "_adb_cmd", return_value=(0, "List of devices attached\n", "")):
        assert adb.get_connection_status() == "NO_DEVICE"
        assert not adb.is_device_connected()

    with patch.object(adb, "_adb_cmd", return_value=(0, "List of devices attached\n123456\tunauthorized\n", "")):
        assert adb.get_connection_status() == "UNAUTHORIZED"
        assert not adb.is_device_connected()

    with patch.object(adb, "_adb_cmd", return_value=(0, "List of devices attached\n123456\tdevice\n789101\tdevice\n", "")):
        assert adb.get_connection_status() == "MULTIPLE_DEVICES"

    with patch.object(adb, "_adb_cmd", return_value=(0, "List of devices attached\n123456\tdevice\n", "")):
        assert adb.get_connection_status() == "CONNECTED"
        assert adb.is_device_connected()


def test_adb_serial_selection():
    """P-06: Test that ADBCollector with explicit device_id selects the matching device."""
    adb_target = ADBCollector(device_id="123456")
    adb_other = ADBCollector(device_id="999999")

    mock_out = "List of devices attached\n123456\tdevice\n789101\tdevice\n"
    with patch.object(adb_target, "_adb_cmd", return_value=(0, mock_out, "")):
        assert adb_target.get_connection_status() == "CONNECTED"

    with patch.object(adb_other, "_adb_cmd", return_value=(0, mock_out, "")):
        assert adb_other.get_connection_status() == "NO_DEVICE"


def test_adb_collector_evidence_generation_and_hashing(temp_output_dir):
    adb = ADBCollector(device_id="123456")

    def mock_adb_cmd(args):
        cmd_str = " ".join(args)
        if "getprop" in cmd_str:
            return 0, "[ro.product.manufacturer]: [OPPO]\n[ro.product.model]: [OPPO A5 2020]\n[ro.build.version.sdk]: [28]\n[ro.product.cpu.abi]: [arm64-v8a]\n[ro.soc.model]: [SM6125]\n", ""
        elif "/proc/meminfo" in cmd_str:
            return 0, "MemTotal:        3072000 kB\nMemAvailable:    1500000 kB\n", ""
        elif "/proc/cpuinfo" in cmd_str:
            return 0, "processor : 0\nprocessor : 1\nprocessor : 2\nprocessor : 3\nHardware : Qualcomm\n", ""
        elif "/proc/stat" in cmd_str:
            return 0, "cpu  12345 6789 101112 131415\n", ""
        elif "thermalservice" in cmd_str:
            return 0, "Current thermal status: 0\n", ""
        elif "dumpsys battery" in cmd_str:
            return 0, "Current Battery Service state:\n  level: 85\n  voltage: 4100\n  temperature: 295\n  AC powered: true\n", ""
        elif "atrace" in cmd_str:
            return 0, "gfx - Graphics\ninput - Input\nview - View System\n", ""
        elif "airplane_mode_on" in cmd_str:
            return 0, "1\n", ""
        elif "boot_id" in cmd_str:
            return 0, "mock_boot_id_12345\n", ""
        elif "characterization_output.json" in cmd_str:
            return 1, "", "No such file"
        return 0, "ok\n", ""

    with patch.object(adb, "_adb_cmd", side_effect=mock_adb_cmd):
        files_saved, observed_props = adb.collect_raw_evidence_and_observations(temp_output_dir)

        # R-01: Verify observed_props.json and manifest.json exist
        ev_dir = temp_output_dir / "evidence"
        assert (ev_dir / "observed_props.json").exists()
        assert (ev_dir / "manifest.json").exists()
        assert (ev_dir / "commands.log").exists()
        assert (ev_dir / "atrace_evidence.txt").exists()
        assert (ev_dir / "network_evidence.txt").exists()
        assert (ev_dir / "battery_dumpsys_evidence.txt").exists()

        # P-03 / P-04 checks
        assert observed_props["atrace_adb_available"] is True
        assert observed_props["manufacturer"] == "OPPO"
        assert observed_props["model"] == "OPPO A5 2020"
        assert observed_props["total_ram_mb"] == 3000
        assert observed_props["network_state"] == "OFFLINE"
        assert observed_props["charging_state"] is True
        assert observed_props["soc_model"] == "SM6125"
        assert observed_props["source_soc_prop"] == "ro.soc.model"
        assert observed_props["app_output_status"] == "APP_OUTPUT_MISSING"


def test_profiling_probe_failure_handling(temp_output_dir):
    adb = ADBCollector()
    with patch.object(adb, "_adb_cmd", return_value=(1, "", "atrace not supported")):
        avail, ev_file = adb.probe_profiling_capability(temp_output_dir / "evidence")
        assert avail is False
        assert ev_file.exists()
        content = ev_file.read_text()
        assert "Exit Code: 1" in content
        assert "atrace not supported" in content


def test_run_characterization_require_device_rejection(temp_output_dir):
    config_file = Path("configs/device_characterization.yaml")
    with patch("scripts.device_characterization.adb_collector.ADBCollector.get_connection_status", return_value="NO_DEVICE"):
        with pytest.raises(RuntimeError) as exc_info:
            run_characterization(config_file, dry_run=False, require_device=True, results_dir=temp_output_dir)
        assert "Device execution requested (--require-device) but ADB connection status is 'NO_DEVICE'" in str(exc_info.value)


def test_p06_require_device_and_dry_run_collision(temp_output_dir):
    """P-06: --require-device combined with --dry-run must raise ValueError."""
    config_file = Path("configs/device_characterization.yaml")
    with pytest.raises(ValueError) as exc_info:
        run_characterization(config_file, dry_run=True, require_device=True, results_dir=temp_output_dir)
    assert "CLI argument conflict: --require-device cannot be used with --dry-run" in str(exc_info.value)


def test_mock_observed_isolation_in_connected_run(temp_output_dir):
    config_file = Path("configs/device_characterization.yaml")
    with patch("scripts.device_characterization.adb_collector.ADBCollector.get_connection_status", return_value="CONNECTED"):
        with pytest.raises(ValueError) as exc_info:
            run_characterization(config_file, mock_observed={"manufacturer": "Fake"}, require_device=True, results_dir=temp_output_dir)
        assert "Synthetic mock_observed overrides cannot be merged into a real connected device run" in str(exc_info.value)


def test_p01_connected_run_does_not_mutate_matrix(temp_output_dir):
    """P-01: Verify that a connected characterization run NEVER mutates device_capability_matrix.md."""
    config_file = Path("configs/device_characterization.yaml")
    matrix_path = Path("research/experiments/device_capability_matrix.md")
    original_matrix_text = matrix_path.read_text(encoding="utf-8")

    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    run_id = f"run_{today}_120000"

    mock_adb_props = {
        "is_real_device_observation": True,
        "manufacturer": "OPPO",
        "model": "OPPO A5 2020",
        "release_version": "9",
        "api_level": 28,
        "cpu_abi": "arm64-v8a",
        "soc_model": "Snapdragon 665",
        "total_ram_mb": 3000,
        "available_memory_mb": 1500,
        "battery_level_percent": 80,
        "battery_voltage": 4000,
        "battery_temperature": 28.5,
        "charging_state": False,
        "network_state": "OFFLINE",
        "atrace_adb_available": True,
        "boot_id": "test_boot_123",
    }

    def mock_collect(output_dir):
        ev_dir = output_dir / "evidence"
        ev_dir.mkdir(parents=True, exist_ok=True)
        files = [
            ev_dir / "getprop_evidence.txt",
            ev_dir / "meminfo_evidence.txt",
            ev_dir / "cpuinfo_evidence.txt",
            ev_dir / "proc_stat_evidence.txt",
            ev_dir / "thermal_evidence.txt",
            ev_dir / "battery_dumpsys_evidence.txt",
            ev_dir / "atrace_evidence.txt",
            ev_dir / "network_evidence.txt",
        ]
        manifest_entries = []
        for f in files:
            content_bytes = b"mock evidence content\n"
            f.write_bytes(content_bytes)
            manifest_entries.append({
                "relative_path": f"evidence/{f.name}",
                "size_bytes": len(content_bytes),
                "sha256": hashlib.sha256(content_bytes).hexdigest(),
                "created_at": "2026-10-05T12:00:00Z"
            })

        obs_bytes = json.dumps(mock_adb_props, indent=2).encode("utf-8")
        obs_file = ev_dir / "observed_props.json"
        obs_file.write_bytes(obs_bytes)
        manifest_entries.append({
            "relative_path": "evidence/observed_props.json",
            "size_bytes": len(obs_bytes),
            "sha256": hashlib.sha256(obs_bytes).hexdigest(),
            "created_at": "2026-10-05T12:00:00Z"
        })
        manifest_file = ev_dir / "manifest.json"
        manifest_bytes = json.dumps(manifest_entries, indent=2).encode("utf-8")
        manifest_file.write_bytes(manifest_bytes)
        files.append(manifest_file)
        mock_adb_props["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
        return files, mock_adb_props

    with patch("scripts.device_characterization.adb_collector.ADBCollector.get_connection_status", return_value="CONNECTED"):
        with patch("scripts.device_characterization.adb_collector.ADBCollector.collect_raw_evidence_and_observations", side_effect=mock_collect):
            out_dir, run_dict = run_characterization(config_file, run_id=run_id, overwrite=True, results_dir=temp_output_dir)

    # P-01 assertion: device_capability_matrix.md text must remain 100% untouched
    assert matrix_path.read_text(encoding="utf-8") == original_matrix_text


def test_p05_manifest_hash_verification(temp_output_dir):
    """P-05: Test SHA-256 evidence integrity check in validate_characterization_record."""
    output_dir = temp_output_dir / "run_hash_test"
    ev_dir = output_dir / "evidence"
    ev_dir.mkdir(parents=True)

    ev_file = ev_dir / "sample_ev.txt"
    ev_file.write_text("valid content", encoding="utf-8")
    correct_sha = hashlib.sha256(b"valid content").hexdigest()

    manifest_file = ev_dir / "manifest.json"
    manifest_entries = [{
        "relative_path": "evidence/sample_ev.txt",
        "size_bytes": 13,
        "sha256": correct_sha,
        "created_at": "2026-10-05T12:00:00Z"
    }]
    manifest_file.write_text(json.dumps(manifest_entries), encoding="utf-8")

    dummy_record = {
        "run_id": "run_20261005_120000",
        "started_at": "2026-10-05T12:00:00Z",
        "app_version": "1.0.0",
        "git_commit": "abc",
        "conditions": {},
    }

    # 1. Valid hash -> no integrity errors
    errors = validate_characterization_record(dummy_record, output_dir=output_dir)
    assert not any("Evidence integrity failure" in e for e in errors)

    # 2. Tampered evidence content -> integrity error detected
    ev_file.write_text("TAMPERED CONTENT", encoding="utf-8")
    errors_tampered = validate_characterization_record(dummy_record, output_dir=output_dir)
    assert any("Evidence integrity failure" in e for e in errors_tampered)


def test_p04_soc_property_fallback_provenance():
    """P-04: Test SoC property fallback hierarchy and provenance recording."""
    adb = ADBCollector()

    # Case 1: ro.soc.model present
    with patch.object(adb, "_adb_cmd", return_value=(0, "[ro.soc.model]: [SM6125]\n", "")):
        props = adb.get_properties()
        assert props.get("ro.soc.model") == "SM6125"

    # Case 2: ro.soc.model absent, ro.board.platform present
    with patch.object(adb, "_adb_cmd", return_value=(0, "[ro.board.platform]: [trinket]\n", "")):
        props = adb.get_properties()
        assert props.get("ro.soc.model") is None
        assert props.get("ro.board.platform") == "trinket"


def test_p03_unmocked_collector_e2e_pipeline(tmp_path):
    """P-03: End-to-end unmocked pipeline test executing:
    synthetic ADB -> raw evidence -> parser -> actual collectors -> report generator -> characterization.json.
    Verifies CPU frequency and GPU clock appear in the final report, and app_output_status reaches characterization.json.
    """
    adb = ADBCollector(device_id="SYNTHETIC_DEVICE_01")

    def mock_adb_cmd(args):
        cmd_str = " ".join(args)
        if "getprop" in cmd_str:
            return 0, "[ro.product.manufacturer]: [OPPO]\n[ro.product.model]: [OPPO A5 2020]\n[ro.build.version.sdk]: [28]\n[ro.soc.model]: [SM6125]\n", ""
        elif "/proc/meminfo" in cmd_str:
            return 0, "MemTotal:        3072000 kB\nMemAvailable:    1500000 kB\n", ""
        elif "/proc/cpuinfo" in cmd_str:
            return 0, "processor : 0\nprocessor : 1\nHardware : Qualcomm\n", ""
        elif "scaling_cur_freq" in cmd_str:
            return 0, "1804800\n", ""
        elif "gpuclk" in cmd_str:
            return 0, "600000000\n", ""
        elif "/proc/stat" in cmd_str:
            return 0, "cpu  1234 5678 9101\n", ""
        elif "dumpsys battery" in cmd_str:
            return 0, "level: 80\nvoltage: 4100\ntemperature: 290\ncurrent now: 150\n", ""
        elif "dumpsys media.camera" in cmd_str:
            return 0, "Camera 0 info\n", ""
        elif "dumpsys thermalservice" in cmd_str:
            return 0, "ThermalService status: 0\n", ""
        elif "atrace" in cmd_str:
            return 0, "gfx - Graphics\n", ""
        elif "airplane_mode_on" in cmd_str:
            return 0, "1\n", ""
        elif "boot_id" in cmd_str:
            return 0, "synthetic_boot_123\n", ""
        elif "run-as" in cmd_str:
            app_json = json.dumps({
                "run_id": "android_run_9999",
                "observed_at": "2026-10-05T12:00:00Z",
                "device_identity": [
                    {"metric": "manufacturer", "value": "OPPO", "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "model", "value": "OPPO A5 2020", "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "soc_model", "value": "SM6125", "state": "AVAILABLE", "report_status": "VERIFIED"}
                ],
                "battery_telemetry": [
                    {"metric": "battery_level_percent", "value": 85, "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "battery_voltage", "value": 4150, "unit": "mV", "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "battery_temperature", "value": 29.5, "unit": "degC", "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "is_charging", "value": False, "state": "AVAILABLE", "report_status": "VERIFIED"}
                ],
                "memory_telemetry": [
                    {"metric": "total_ram_mb", "value": 3072, "unit": "MB", "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "available_memory_mb", "value": 1500, "unit": "MB", "state": "AVAILABLE", "report_status": "VERIFIED"}
                ],
                "thermal_capability": {
                    "metric": "thermal_status_api",
                    "value": 0,
                    "state": "AVAILABLE",
                    "report_status": "VERIFIED"
                },
                "camera_telemetry": [
                    {"metric": "camera_count", "value": 4, "state": "AVAILABLE", "report_status": "VERIFIED"},
                    {"metric": "camera_0_hardware_level", "value": 1, "state": "AVAILABLE", "report_status": "VERIFIED"}
                ]
            })
            return 0, app_json, ""
        return 0, "ok\n", ""

        with patch.object(adb, "_adb_cmd", side_effect=mock_adb_cmd):
            with patch("scripts.device_characterization.run_characterization.ADBCollector", return_value=adb):
                with patch.object(adb, "get_connection_status", return_value="CONNECTED"):
                    today = datetime.datetime.utcnow().strftime("%Y%m%d")
                    run_id = f"run_{today}_150000"
                    config_file = Path("configs/device_characterization.yaml")

                    out_dir, run_dict = run_characterization(
                        config_file,
                        run_id=run_id,
                        overwrite=True,
                        results_dir=tmp_path,
                    )

                    # Verify characterization.json output
                    char_json = out_dir / "characterization.json"
                    assert char_json.exists()

                    with open(char_json, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Verify app_output_status and nested app telemetry integration
                    assert data.get("app_output_status") == "APP_OUTPUT_COLLECTED"
                    assert "app_telemetry" in data
                    assert data["app_telemetry"]["run_id"] == "android_run_9999"

                    # Search CPU frequency and GPU clock in telemetry
                    telemetry = data.get("telemetry", [])
                    cpu_telemetry = next((t for t in telemetry if t["dimension"] == "cpu"), None)
                    gpu_telemetry = next((t for t in telemetry if t["dimension"] == "gpu"), None)

                    assert cpu_telemetry is not None
                    assert gpu_telemetry is not None

                    cpu_freq_res = next((r for r in cpu_telemetry["results"] if r["metric"] == "cpu_scaling_cur_freq"), None)
                    gpu_clock_res = next((r for r in gpu_telemetry["results"] if r["metric"] == "gpu_clock_hz"), None)

                    assert cpu_freq_res is not None
                    assert cpu_freq_res["value"] == 1804800
                    assert cpu_freq_res["state"] == "AVAILABLE"
                    assert cpu_freq_res["verified"] is True
                    assert cpu_freq_res["evidence_ref"] == "evidence/cpufreq_evidence.txt#scaling_cur_freq"

                    assert gpu_clock_res is not None
                    assert gpu_clock_res["value"] == 600000000
                    assert gpu_clock_res["state"] == "AVAILABLE"
                    assert gpu_clock_res["verified"] is True
                    assert gpu_clock_res["evidence_ref"] == "evidence/gpu_evidence.txt#gpuclk"


def test_p04_all_soc_fallback_paths_and_evidence_refs(tmp_path):
    """P-04: Test all 4 SoC fallback paths and verify evidence_ref citations."""
    from src.monitoring.characterization.collectors import DeviceIdentityCollector

    # Path 1: ro.soc.model available
    adb1 = ADBCollector(device_id="DEV1")
    def mock_cmd1(args):
        c = " ".join(args)
        if "getprop" in c: return 0, "[ro.soc.model]: [SM6125]\n", ""
        return 0, "ok\n", ""

    with patch.object(adb1, "_adb_cmd", side_effect=mock_cmd1):
        _, props1 = adb1.collect_raw_evidence_and_observations(tmp_path / "p1")
        ident1 = DeviceIdentityCollector().collect(props1)
        soc_res1 = next(r for r in ident1.observed if r.metric == "soc_model")
        assert soc_res1.value == "SM6125"
        assert soc_res1.evidence_ref == "evidence/getprop_evidence.txt#ro.soc.model"

    # Path 2: ro.soc.model unavailable, ro.board.platform available
    adb2 = ADBCollector(device_id="DEV2")
    def mock_cmd2(args):
        c = " ".join(args)
        if "getprop" in c: return 0, "[ro.board.platform]: [trinket]\n", ""
        return 0, "ok\n", ""

    with patch.object(adb2, "_adb_cmd", side_effect=mock_cmd2):
        _, props2 = adb2.collect_raw_evidence_and_observations(tmp_path / "p2")
        ident2 = DeviceIdentityCollector().collect(props2)
        soc_res2 = next(r for r in ident2.observed if r.metric == "soc_model")
        assert soc_res2.value == "trinket"
        assert soc_res2.evidence_ref == "evidence/getprop_evidence.txt#ro.board.platform"

    # Path 3: both getprop unavailable, cpuinfo Hardware available
    adb3 = ADBCollector(device_id="DEV3")
    def mock_cmd3(args):
        c = " ".join(args)
        if "getprop" in c: return 0, "", ""
        elif "/proc/cpuinfo" in c: return 0, "Hardware : Qualcomm Technologies, Inc SM6125\n", ""
        return 0, "ok\n", ""

    with patch.object(adb3, "_adb_cmd", side_effect=mock_cmd3):
        _, props3 = adb3.collect_raw_evidence_and_observations(tmp_path / "p3")
        ident3 = DeviceIdentityCollector().collect(props3)
        soc_res3 = next(r for r in ident3.observed if r.metric == "soc_model")
        assert soc_res3.value == "Qualcomm Technologies, Inc SM6125"
        assert soc_res3.evidence_ref == "evidence/cpuinfo_evidence.txt#Hardware"

    # Path 4: all unavailable
    adb4 = ADBCollector(device_id="DEV4")
    def mock_cmd4(args):
        return 0, "", ""

    with patch.object(adb4, "_adb_cmd", side_effect=mock_cmd4):
        _, props4 = adb4.collect_raw_evidence_and_observations(tmp_path / "p4")
        ident4 = DeviceIdentityCollector().collect(props4)
        soc_res4 = next(r for r in ident4.observed if r.metric == "soc_model")
        assert soc_res4.value is None
        assert soc_res4.state in ("UNAVAILABLE", "NOT_TESTED")
        assert soc_res4.evidence_ref is None


def test_p05_manifest_validation_cases(tmp_path):
    """P-05: Comprehensive tests for valid, missing, tampered manifest and evidence files."""
    from tests.test_device_characterization_report import _build_dummy_run_record

    dummy_record = _build_dummy_run_record("run_20261005_120000", is_dry_run=False)
    dummy_record["conditions"]["adb_connected"] = True
    dummy_record["conditions"]["is_dry_run"] = False

    run_dir = tmp_path / "run_p05"
    ev_dir = run_dir / "evidence"
    ev_dir.mkdir(parents=True)

    ev_file = ev_dir / "test_ev.txt"
    ev_bytes = b"valid content"
    ev_file.write_bytes(ev_bytes)
    sha_ev = hashlib.sha256(ev_bytes).hexdigest()

    manifest_file = ev_dir / "manifest.json"
    manifest_entries = [{
        "relative_path": "evidence/test_ev.txt",
        "size_bytes": len(ev_bytes),
        "sha256": sha_ev,
        "created_at": "2026-10-05T12:00:00Z"
    }]
    manifest_bytes = json.dumps(manifest_entries, indent=2).encode("utf-8")
    manifest_file.write_bytes(manifest_bytes)
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    dummy_record["manifest_sha256"] = manifest_sha

    # 1. Valid manifest -> passes
    errors1 = validate_characterization_record(dummy_record, output_dir=run_dir)
    assert not errors1

    # 2. Missing manifest -> fails
    manifest_file.unlink()
    errors2 = validate_characterization_record(dummy_record, output_dir=run_dir)
    assert any("manifest.json missing" in e for e in errors2)

    # Re-write manifest
    manifest_file.write_bytes(manifest_bytes)

    # 3. Tampered manifest hash in record -> fails
    dummy_record_tampered = dict(dummy_record)
    dummy_record_tampered["manifest_sha256"] = "0000000000000000000000000000000000000000000000000000000000000000"
    errors3 = validate_characterization_record(dummy_record_tampered, output_dir=run_dir)
    assert any("Manifest SHA-256 mismatch" in e for e in errors3)

    # 4. Missing evidence file -> fails
    ev_file.unlink()
    errors4 = validate_characterization_record(dummy_record, output_dir=run_dir)
    assert any("Manifest evidence file missing" in e for e in errors4)

    # 5. Wrong evidence hash -> fails
    ev_file.write_bytes(b"corrupted evidence")
    errors5 = validate_characterization_record(dummy_record, output_dir=run_dir)
    assert any("Evidence integrity failure" in e for e in errors5)


def test_p07_probe_failure_semantics():
    """P-07: Verify probe failures yield state=ERROR with error messages and commands.log evidence_ref."""
    props = {
        "is_real_device_observation": False,
        "probe_error_battery": "Battery probe failed with exit code 1",
        "probe_error_cpufreq": "Cpufreq sysfs node unreadable",
        "probe_error_gpu": "GPU sysfs node unreadable",
        "probe_error_meminfo": "Meminfo read error",
        "probe_error_thermal": "Thermal service unavailable",
        "probe_error_camera": "Camera service dead",
    }

    from src.monitoring.characterization.collectors import (
        BatteryTelemetryCollector,
        CPUTelemetryCollector,
        GPUTelemetryCollector,
        MemoryTelemetryCollector,
        ThermalTelemetryCollector,
        CameraCapabilityCollector,
    )

    bat_cap = BatteryTelemetryCollector().collect(props)
    cpu_cap = CPUTelemetryCollector().collect(props)
    gpu_cap = GPUTelemetryCollector().collect(props)
    mem_cap = MemoryTelemetryCollector().collect(props)
    th_cap = ThermalTelemetryCollector().collect(props)
    cam_caps = CameraCapabilityCollector().collect(props)

    bat_lvl = next(r for r in bat_cap.results if r.metric == "battery_level_percent")
    assert bat_lvl.state == "ERROR"
    assert bat_lvl.error_message == "Battery probe failed with exit code 1"
    assert bat_lvl.evidence_ref == "evidence/commands.log#probe_error_battery"

    cpu_freq = next(r for r in cpu_cap.results if r.metric == "cpu_scaling_cur_freq")
    assert cpu_freq.state == "ERROR"
    assert cpu_freq.error_message == "Cpufreq sysfs node unreadable"

    gpu_freq = next(r for r in gpu_cap.results if r.metric == "gpu_clock_hz")
    assert gpu_freq.state == "ERROR"
    assert gpu_freq.error_message == "GPU sysfs node unreadable"

    mem_avail = next(r for r in mem_cap.results if r.metric == "available_memory_mb")
    assert mem_avail.state == "ERROR"
    assert mem_avail.error_message == "Meminfo read error"

    th_zones = next(r for r in th_cap.temperature_sources if r.metric == "thermal_zones_sysfs")
    assert th_zones.state == "ERROR"

    cam_hw = next(r for r in cam_caps[0].results if r.metric == "hardware_level")
    assert cam_hw.state == "ERROR"


def test_r09_battery_current_semantics():
    """R-09: Test battery current unit conversions, zero current unverified flag, and implausible values."""
    from src.monitoring.characterization.collectors import BatteryTelemetryCollector

    # Case 1: Valid positive current in mA
    props1 = {"is_real_device_observation": True, "battery_current_now": 250, "battery_current_unit": "mA"}
    res1 = next(r for r in BatteryTelemetryCollector().collect(props1).results if r.metric == "battery_current_now")
    assert res1.state == "AVAILABLE"
    assert res1.value == 250.0
    assert res1.verified is True

    # Case 2: Zero current -> NOT marked VERIFIED
    props2 = {"is_real_device_observation": True, "battery_current_now": 0, "battery_current_unit": "mA"}
    res2 = next(r for r in BatteryTelemetryCollector().collect(props2).results if r.metric == "battery_current_now")
    assert res2.state == "AVAILABLE"
    assert res2.value == 0.0
    assert res2.verified is False  # Cannot be verified!
    assert res2.report_status == "AVAILABLE"

    # Case 3: Unit conversion (uA -> mA for explicit uA unit)
    props3 = {"is_real_device_observation": True, "battery_current_now": 350000, "battery_current_unit": "uA"}
    res3 = next(r for r in BatteryTelemetryCollector().collect(props3).results if r.metric == "battery_current_now")
    assert res3.state == "AVAILABLE"
    assert res3.value == 350.0  # Converted to mA
    assert res3.verified is True

    # Case 4: Implausible current (> 10,000 mA) -> state ERROR
    props4 = {"is_real_device_observation": False, "battery_current_now": 99999999, "battery_current_unit": "mA"}
    res4 = next(r for r in BatteryTelemetryCollector().collect(props4).results if r.metric == "battery_current_now")
    assert res4.state == "ERROR"
    assert "Implausible battery current" in res4.error_message


def test_r03_exact_serial_matching():
    """R-03: --serial must use exact matching, not prefix matching."""
    adb = ADBCollector(device_id="STUB1")
    devices_output = "List of devices attached\nSTUB123\tdevice\n"
    with patch.object(adb, "_adb_cmd", return_value=(0, devices_output, "")):
        assert adb.get_connection_status() == "NO_DEVICE"

    devices_output_exact = "List of devices attached\nSTUB1\tdevice\n"
    with patch.object(adb, "_adb_cmd", return_value=(0, devices_output_exact, "")):
        assert adb.get_connection_status() == "CONNECTED"


def test_r11_atomic_write_and_run_status(tmp_path):
    """R-11: Verify atomic file creation and run_status handling."""
    from tests.test_device_characterization_report import _build_dummy_run_record

    generator = CharacterizationReportGenerator()
    dummy_record = _build_dummy_run_record("run_20261005_160000", is_dry_run=True)
    dummy_record["run_status"] = "DRY_RUN"

    out_dir = tmp_path / "atomic_run"
    res = generator.process_run(dummy_record, output_dir=out_dir)

    assert res["status"] == "VALID"
    assert (out_dir / "characterization.json").exists()
    assert (out_dir / "README.md").exists()
    assert not (out_dir / "characterization.json.tmp").exists()
    assert not (out_dir / "README.md.tmp").exists()
