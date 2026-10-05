"""
End-to-end tests for Step 10D connected-device characterization path,
evidence references, ADB connection state classification, and profiling probes (R-01, R-02, R-03, R-12).

Uses a mock ADB execution stub to test the complete connected pipeline without physical hardware.
Synthetic outputs in this test are explicitly classified as TEST/MOCK and are not repository evidence.
"""

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

        # R-02: Verify atrace probe succeeded and set flag
        assert observed_props["atrace_adb_available"] is True
        assert observed_props["manufacturer"] == "OPPO"
        assert observed_props["model"] == "OPPO A5 2020"
        assert observed_props["total_ram_mb"] == 3000
        assert observed_props["network_state"] == "OFFLINE"
        assert observed_props["charging_state"] is True


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
            run_characterization(config_file, dry_run=False, require_device=True)
        assert "Device execution requested (--require-device) but ADB connection status is 'NO_DEVICE'" in str(exc_info.value)


def test_mock_observed_isolation_in_connected_run(temp_output_dir):
    config_file = Path("configs/device_characterization.yaml")
    with patch("scripts.device_characterization.adb_collector.ADBCollector.get_connection_status", return_value="CONNECTED"):
        with pytest.raises(ValueError) as exc_info:
            run_characterization(config_file, mock_observed={"manufacturer": "Fake"}, require_device=True)
        assert "Synthetic mock_observed overrides cannot be merged into a real connected device run" in str(exc_info.value)


def test_full_connected_path_schema_and_evidence_validation(temp_output_dir):
    config_file = Path("configs/device_characterization.yaml")
    run_id = "run_20261005_120000"

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
            ev_dir / "observed_props.json",
            ev_dir / "manifest.json",
        ]
        for f in files:
            f.write_text("mock evidence content\n", encoding="utf-8")

        (ev_dir / "observed_props.json").write_text(json.dumps(mock_adb_props), encoding="utf-8")
        return files, mock_adb_props

    tmp_matrix = temp_output_dir / "device_capability_matrix.md"
    tmp_matrix.write_text(Path("research/experiments/device_capability_matrix.md").read_text(encoding="utf-8"), encoding="utf-8")

    with patch("scripts.device_characterization.adb_collector.ADBCollector.get_connection_status", return_value="CONNECTED"):
        with patch("scripts.device_characterization.adb_collector.ADBCollector.collect_raw_evidence_and_observations", side_effect=mock_collect):
            with patch("src.monitoring.characterization.report_generator.MATRIX_PATH", tmp_matrix):
                out_dir, run_dict = run_characterization(config_file, run_id=run_id, overwrite=True)

                # Validate that output directory and characterization.json exist
                run_file = out_dir / "characterization.json"
                assert run_file.exists()

                # Perform schema & evidence file validation
                errors = validate_characterization_record(run_dict, output_dir=out_dir)
                assert errors == [], f"Validation failed for connected run: {errors}"

                # Verify that verified records cite existing evidence files
                observed = run_dict["device_identity"]["observed"]
                mfr_item = next(item for item in observed if item["metric"] == "manufacturer")
                assert mfr_item["verified"] is True
                assert mfr_item["report_status"] == "VERIFIED"
                assert (out_dir / mfr_item["evidence_ref"].split("#")[0]).exists()
