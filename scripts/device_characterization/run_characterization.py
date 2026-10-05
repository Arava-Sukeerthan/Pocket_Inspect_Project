"""
Step 10D: Host-side characterization CLI entry point.

Orchestrates device characterization collectors, collects raw ADB evidence
from the physical OPPO A5 2020 if connected, parses raw evidence files,
validates run against device_characterization_schema.json, saves output
to research/results/device_characterization/<run_id>/, and updates device_capability_matrix.md.
"""

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List

import yaml

# Ensure project root is on python path
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.monitoring.characterization.collectors import (
    DeviceIdentityCollector,
    AndroidCapabilityCollector,
    BatteryTelemetryCollector,
    MemoryTelemetryCollector,
    CPUTelemetryCollector,
    GPUTelemetryCollector,
    ThermalTelemetryCollector,
    CameraCapabilityCollector,
    InferenceBackendCapabilityCollector,
    ProfilingCapabilityCollector,
    EnergyMeasurementCapabilityChecker,
)
from src.monitoring.characterization.models import CharacterizationRun
from src.monitoring.characterization.report_generator import CharacterizationReportGenerator
from scripts.device_characterization.adb_collector import ADBCollector


def _get_git_commit() -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT)
        if res.returncode == 0:
            commit = res.stdout.strip()
            status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=ROOT)
            if status_res.stdout.strip():
                commit += "-dirty"
            return commit
    except Exception:
        pass
    return "unknown_commit"


def _hash_file(path: Path) -> str:
    if path.exists():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return "unknown_hash"


def run_characterization(
    config_path: Path,
    run_id: Optional[str] = None,
    repeat_index: int = 1,
    mock_observed: Optional[dict] = None,
    dry_run: bool = False,
    require_device: bool = False,
    overwrite: bool = False,
) -> Tuple[Path, dict]:
    """Runs a characterization pass and writes schema-valid output."""
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    now_utc = datetime.datetime.utcnow()
    now_str = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    today_str = now_utc.strftime("%Y%m%d")

    if not run_id:
        run_id = f"run_{now_utc.strftime('%Y%m%d_%H%M%S')}"

    # F-02 / R-11: Date mismatch check between run_id and actual start time date
    if "_" in run_id:
        date_part = run_id.split("_")[1]
        if len(date_part) == 8 and date_part.isdigit() and date_part != today_str:
            raise ValueError(
                f"Run ID date '{date_part}' does not match actual start time date '{today_str}' (F-02 date mismatch error). "
                "Fake future-dated run folders are strictly forbidden."
            )

    unit_id = cfg.get("device_unit_id", "OPPO_A5_2020_UNIT_01")
    results_base = ROOT / cfg.get("output", {}).get("results_directory", "research/results/device_characterization")
    output_dir = results_base / run_id

    # F-14 / R-11: Silent overwrite guard
    run_file = output_dir / "characterization.json"
    if run_file.exists() and not overwrite:
        raise FileExistsError(f"Run directory '{output_dir}' already contains characterization.json. Silent overwrite refused (F-14).")

    # ADB check & raw evidence collection
    adb = ADBCollector()
    conn_status = adb.get_connection_status()

    # R-03 / R-10: Connection state handling and device requirement check
    if require_device and conn_status != "CONNECTED":
        raise RuntimeError(
            f"Device execution requested (--require-device) but ADB connection status is '{conn_status}' (R-03 error). "
            "Connected-device execution cannot silently fall back to dry run."
        )

    adb_connected = (conn_status == "CONNECTED") and not dry_run

    if adb_connected and mock_observed:
        raise ValueError("Synthetic mock_observed overrides cannot be merged into a real connected device run (R-10 isolation failure).")

    props: Dict[str, Any] = {}
    if mock_observed and not adb_connected:
        props.update(mock_observed)

    if adb_connected:
        evidence_files, observed_adb_props = adb.collect_raw_evidence_and_observations(output_dir)
        props.update(observed_adb_props)
    else:
        props["is_real_device_observation"] = False

    # Execute all 11 capability collectors
    dev_ident = DeviceIdentityCollector(unit_id).collect(props)
    android_cap = AndroidCapabilityCollector().collect(props)
    battery_cap = BatteryTelemetryCollector().collect(props)
    memory_cap = MemoryTelemetryCollector().collect(props)
    cpu_cap = CPUTelemetryCollector().collect(props)
    gpu_cap = GPUTelemetryCollector().collect(props)
    thermal_cap = ThermalTelemetryCollector().collect(props)
    camera_caps = CameraCapabilityCollector().collect(props)
    backend_caps = InferenceBackendCapabilityCollector().collect(props)
    profiling_caps = ProfilingCapabilityCollector().collect(props)
    energy_cap = EnergyMeasurementCapabilityChecker().collect(props)

    dev_ident.observed.extend(android_cap.results)

    boot_id = props.get("boot_id", "unknown")
    git_commit = _get_git_commit()
    config_hash = _hash_file(config_path)

    run = CharacterizationRun(
        run_id=run_id,
        started_at=now_str,
        repeat_index=repeat_index,
        app_version="1.0.0-characterization",
        git_commit=git_commit,
        host_tool_versions={
            "python": sys.version.split()[0],
            "adb": adb.get_adb_version(),
            "config_sha256": config_hash,
        },
        device_identity=dev_ident,
        telemetry=[battery_cap, memory_cap, cpu_cap, gpu_cap],
        camera=camera_caps,
        backends=backend_caps,
        profiling=profiling_caps,
        thermal=thermal_cap,
        energy=energy_cap,
        conditions={
            "charging": props.get("charging_state"),
            "network": props.get("network_state", "NOT_TESTED"),
            "usb_connected": adb_connected,
            "adb_connected": adb_connected,
            "adb_connection_status": conn_status,
            "boot_id": boot_id,
            "is_dry_run": not adb_connected,
        },
    )

    run_dict = run.to_dict()

    # Process and validate using report generator (R-11 atomic write)
    generator = CharacterizationReportGenerator()
    res = generator.process_run(run_dict, output_dir=output_dir, overwrite=overwrite)

    return output_dir, run_dict


def main():
    parser = argparse.ArgumentParser(description="Step 10D Device Characterization CLI")
    parser.add_argument("--config", type=str, default="configs/device_characterization.yaml", help="Path to config YAML")
    parser.add_argument("--run-id", type=str, default=None, help="Optional run ID")
    parser.add_argument("--repeat-index", type=int, default=1, help="Repeat index (1 or 2)")
    parser.add_argument("--dry-run", action="store_true", help="Execute dry run without connected device")
    parser.add_argument("--require-device", action="store_true", help="Fail if connected device is unavailable (prevent dry-run fallback)")
    parser.add_argument("--overwrite", action="store_true", help="Force overwrite existing run directory")
    args = parser.parse_args()

    cfg_path = ROOT / args.config
    out_dir, run_dict = run_characterization(
        cfg_path,
        run_id=args.run_id,
        repeat_index=args.repeat_index,
        dry_run=args.dry_run,
        require_device=args.require_device,
        overwrite=args.overwrite
    )
    print(f"Characterization run completed successfully.")
    print(f"Output saved to: {out_dir}")
    print(f"Run ID: {run_dict['run_id']}")


if __name__ == "__main__":
    main()
