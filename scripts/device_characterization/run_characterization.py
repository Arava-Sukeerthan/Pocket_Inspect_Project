"""
Step 10D: Host-side characterization CLI entry point.

Orchestrates device characterization collectors, collects raw ADB evidence
if connected, executes mock/observed capability checks, validates run against
device_characterization_schema.json, saves output to research/results/device_characterization/<run_id>/,
and updates device_capability_matrix.md.
"""

import argparse
import datetime
import json
import os
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


def run_characterization(
    config_path: Path,
    run_id: Optional[str] = None,
    repeat_index: int = 1,
    mock_observed: Optional[dict] = None
) -> Tuple[Path, dict]:
    """Runs a characterization pass and writes schema-valid output."""
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    if not run_id:
        run_id = f"run_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    unit_id = cfg.get("device_unit_id", "OPPO_A5_2020_UNIT_01")
    output_dir = ROOT / cfg.get("output", {}).get("results_directory", "research/results/device_characterization") / run_id

    # ADB check
    adb = ADBCollector()
    adb_connected = adb.is_device_connected()
    adb_props = {}
    if adb_connected:
        adb_props = adb.get_properties()
        adb.collect_raw_evidence(output_dir / "evidence")

    # Combine adb props and mock props
    props = {}
    if mock_observed:
        props.update(mock_observed)
    if adb_props:
        props.update({
            "manufacturer": adb_props.get("ro.product.manufacturer"),
            "model": adb_props.get("ro.product.model"),
            "release_version": adb_props.get("ro.build.version.release"),
            "api_level": int(adb_props.get("ro.build.version.sdk", 28)) if adb_props.get("ro.build.version.sdk") else None,
            "proc_stat_readable_via_adb": True,
            "atrace_adb_available": True,
        })

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

    run = CharacterizationRun(
        run_id=run_id,
        started_at=now_str,
        repeat_index=repeat_index,
        app_version="1.0.0-characterization",
        git_commit="24aa0f0-impl",
        host_tool_versions={"python": sys.version.split()[0]},
        device_identity=dev_ident,
        telemetry=[battery_cap, memory_cap, cpu_cap, gpu_cap],
        camera=camera_caps,
        backends=backend_caps,
        profiling=profiling_caps,
        thermal=thermal_cap,
        energy=energy_cap,
        conditions={
            "charging": props.get("charging", False),
            "network": "OFFLINE",
            "usb_connected": adb_connected,
            "adb_connected": adb_connected,
        },
    )

    run_dict = run.to_dict()

    # Process and validate using report generator
    generator = CharacterizationReportGenerator()
    res = generator.process_run(run_dict, output_dir)

    return output_dir, run_dict


def main():
    parser = argparse.ArgumentParser(description="Step 10D Device Characterization CLI")
    parser.add_argument("--config", type=str, default="configs/device_characterization.yaml", help="Path to config YAML")
    parser.add_argument("--run-id", type=str, default=None, help="Optional run ID")
    parser.add_argument("--repeat-index", type=int, default=1, help="Repeat index (1 or 2)")
    args = parser.parse_args()

    cfg_path = ROOT / args.config
    out_dir, run_dict = run_characterization(cfg_path, args.run_id, args.repeat_index)
    print(f"Characterization run completed successfully.")
    print(f"Output saved to: {out_dir}")
    print(f"Run ID: {run_dict['run_id']}")


if __name__ == "__main__":
    main()
