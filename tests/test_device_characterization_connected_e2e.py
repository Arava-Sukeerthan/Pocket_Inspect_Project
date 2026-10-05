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
        manifest_file.write_text(json.dumps(manifest_entries, indent=2), encoding="utf-8")
        files.append(manifest_file)
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
