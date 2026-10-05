"""
Collector implementations for Step 10D device characterization.

Implements collectors 1-11 for checking device identity, Android capabilities,
battery, memory, CPU, GPU, thermal, camera, inference backends, profiling,
and energy measurement feasibility.

Strictly follows the status/value separation and no-fake-zeros rules.
"""

import os
import sys
import time
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.monitoring.characterization.models import (
    CapabilityResult,
    RuntimeState,
    ReportStatus,
    map_runtime_state_to_report_status,
    KnownSpecification,
    DeviceIdentity,
    TelemetryCapability,
    CameraCapability,
    BackendCapability,
    ThermalCapability,
    EnergyCapability,
)


class DeviceIdentityCollector:
    """Collector 1: DeviceIdentityCollector.
    Checks device unit ID, known specifications, observed identity properties,
    and performs the 3 GB RAM variant verification check.
    """

    def __init__(self, device_unit_id: str = "OPPO_A5_2020_UNIT_01"):
        self.device_unit_id = device_unit_id

    def collect(self, observed_props: Optional[Dict[str, Any]] = None) -> DeviceIdentity:
        known = KnownSpecification()
        props = observed_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Build list of observed identity capability results
        observed_results: List[CapabilityResult] = []

        # Manufacturer
        obs_mfr = props.get("manufacturer") or props.get("ro.product.manufacturer")
        state_mfr = RuntimeState.AVAILABLE.value if obs_mfr else RuntimeState.UNAVAILABLE.value
        observed_results.append(CapabilityResult(
            metric="manufacturer",
            state=state_mfr,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_mfr), verified=bool(obs_mfr)),
            value=obs_mfr if obs_mfr else None,
            source="Build.MANUFACTURER / getprop",
            verified=bool(obs_mfr),
            verification_method="device_observation",
            observed_at=now if obs_mfr else None,
            evidence_ref="observed_props.json#manufacturer" if obs_mfr else None,
        ))

        # Model
        obs_model = props.get("model") or props.get("ro.product.model")
        state_model = RuntimeState.AVAILABLE.value if obs_model else RuntimeState.UNAVAILABLE.value
        observed_results.append(CapabilityResult(
            metric="model",
            state=state_model,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_model), verified=bool(obs_model)),
            value=obs_model if obs_model else None,
            source="Build.MODEL / getprop",
            verified=bool(obs_model),
            verification_method="device_observation",
            observed_at=now if obs_model else None,
            evidence_ref="observed_props.json#model" if obs_model else None,
        ))

        # Total RAM
        total_ram_mb = props.get("total_ram_mb")
        state_ram = RuntimeState.AVAILABLE.value if total_ram_mb is not None else RuntimeState.UNAVAILABLE.value
        observed_results.append(CapabilityResult(
            metric="total_ram_mb",
            state=state_ram,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_ram), verified=total_ram_mb is not None),
            value=total_ram_mb if total_ram_mb is not None else None,
            unit="MB",
            source="ActivityManager.MemoryInfo.totalMem / /proc/meminfo",
            verified=total_ram_mb is not None,
            verification_method="device_observation",
            observed_at=now if total_ram_mb is not None else None,
            evidence_ref="observed_props.json#total_ram_mb" if total_ram_mb is not None else None,
        ))

        # SoC Model
        obs_soc = props.get("soc_model") or props.get("ro.soc.model")
        state_soc = RuntimeState.AVAILABLE.value if obs_soc else RuntimeState.UNAVAILABLE.value
        observed_results.append(CapabilityResult(
            metric="soc_model",
            state=state_soc,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_soc), verified=bool(obs_soc)),
            value=obs_soc if obs_soc else None,
            source="Build.SOC_MODEL (API>=31) / /proc/cpuinfo",
            min_api=31,
            verified=bool(obs_soc),
            verification_method="device_observation",
            observed_at=now if obs_soc else None,
            evidence_ref="observed_props.json#soc_model" if obs_soc else None,
        ))

        # GPU Renderer
        obs_gpu = props.get("gpu_renderer") or props.get("gles_renderer")
        state_gpu = RuntimeState.AVAILABLE.value if obs_gpu else RuntimeState.UNAVAILABLE.value
        observed_results.append(CapabilityResult(
            metric="gpu_renderer",
            state=state_gpu,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_gpu), verified=bool(obs_gpu)),
            value=obs_gpu if obs_gpu else None,
            source="GLES20.glGetString(GL_RENDERER) / EGL",
            verified=bool(obs_gpu),
            verification_method="device_observation",
            observed_at=now if obs_gpu else None,
            evidence_ref="observed_props.json#gpu_renderer" if obs_gpu else None,
        ))

        # Variant check (3 GB RAM variant)
        if total_ram_mb is not None:
            # 3 GB RAM is typically ~2700 MB - 3100 MB usable RAM
            if 2400 <= total_ram_mb <= 3500:
                variant_val = "3 GB variant verified (observed total RAM: %d MB)" % total_ram_mb
                variant_res = CapabilityResult(
                    metric="variant_check",
                    state=RuntimeState.AVAILABLE.value,
                    report_status=ReportStatus.VERIFIED.value,
                    value=variant_val,
                    unit="variant",
                    source="MemoryInfo.totalMem RAM range check",
                    verified=True,
                    verification_method="observed_ram_range_verification",
                    observed_at=now,
                    evidence_ref="observed_props.json#ram_variant_check",
                    notes="Observed RAM matches the required 3 GB experimental platform variant.",
                )
            else:
                variant_val = "DISAGREEMENT: Observed RAM %d MB does not match 3 GB variant range (2400-3500 MB)" % total_ram_mb
                variant_res = CapabilityResult(
                    metric="variant_check",
                    state=RuntimeState.AVAILABLE.value,
                    report_status=ReportStatus.AVAILABLE.value,
                    value=variant_val,
                    unit="variant",
                    source="MemoryInfo.totalMem RAM range check",
                    verified=False,
                    verification_method="observed_ram_range_verification",
                    observed_at=now,
                    notes="RAM variant check indicates non-3GB device variant.",
                )
        else:
            variant_res = CapabilityResult(
                metric="variant_check",
                state=RuntimeState.UNAVAILABLE.value,
                report_status=ReportStatus.UNAVAILABLE.value,
                value=None,
                unit="variant",
                source="MemoryInfo.totalMem RAM range check",
                verified=False,
                verification_method="observed_ram_range_verification",
                notes="Total RAM not yet observed on device.",
            )

        return DeviceIdentity(
            device_unit_id=self.device_unit_id,
            known_specification=known,
            observed=observed_results,
            variant_check=variant_res,
        )


class AndroidCapabilityCollector:
    """Collector 2: AndroidCapabilityCollector.
    Checks release version, API level, security patch, and platform services.
    """

    def collect(self, android_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = android_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        api_level = props.get("api_level")
        state_api = RuntimeState.AVAILABLE.value if api_level is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="api_level",
            state=state_api,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_api), verified=api_level is not None),
            value=api_level if api_level is not None else None,
            source="Build.VERSION.SDK_INT",
            verified=api_level is not None,
            verification_method="device_observation",
            observed_at=now if api_level is not None else None,
            evidence_ref="android_props.json#api_level" if api_level is not None else None,
        ))

        rel_version = props.get("release_version")
        state_rel = RuntimeState.AVAILABLE.value if rel_version else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="release_version",
            state=state_rel,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_rel), verified=bool(rel_version)),
            value=rel_version if rel_version else None,
            source="Build.VERSION.RELEASE",
            verified=bool(rel_version),
            verification_method="device_observation",
            observed_at=now if rel_version else None,
            evidence_ref="android_props.json#release_version" if rel_version else None,
        ))

        services = ["PowerManager", "HardwarePropertiesManager", "CameraManager", "ActivityManager", "BatteryManager"]
        for svc in services:
            avail = props.get(f"service_{svc}")
            state_svc = RuntimeState.AVAILABLE.value if avail is True else (
                RuntimeState.UNAVAILABLE.value if avail is False else RuntimeState.NOT_TESTED.value
            )
            results.append(CapabilityResult(
                metric=f"service_{svc}",
                state=state_svc,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_svc), verified=avail is True),
                value=f"{svc} available" if avail is True else None,
                source=f"Context.getSystemService({svc})",
                verified=avail is True,
                verification_method="service_get_check",
                observed_at=now if avail is True else None,
                evidence_ref=f"android_props.json#service_{svc}" if avail is True else None,
            ))

        return TelemetryCapability(
            dimension="android",
            results=results,
            resource_state_input=False,
            reliability="NOT YET VERIFIED",
        )


class BatteryTelemetryCollector:
    """Collector 3: BatteryTelemetryCollector.
    Checks battery percentage, voltage, temperature, health, current, counters.
    Handles sentinel values (e.g. Integer.MIN_VALUE or 0 when unsupported).
    """

    def collect(self, battery_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = battery_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        # Battery level (%)
        level = props.get("level")
        state_lvl = RuntimeState.AVAILABLE.value if level is not None and 0 <= level <= 100 else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_level_percent",
            state=state_lvl,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_lvl), verified=state_lvl == RuntimeState.AVAILABLE.value),
            value=level if state_lvl == RuntimeState.AVAILABLE.value else None,
            unit="percent",
            source="BatteryManager.EXTRA_LEVEL / ACTION_BATTERY_CHANGED",
            verified=state_lvl == RuntimeState.AVAILABLE.value,
            verification_method="battery_broadcast_check",
            observed_at=now if state_lvl == RuntimeState.AVAILABLE.value else None,
            evidence_ref="battery_props.json#level" if state_lvl == RuntimeState.AVAILABLE.value else None,
        ))

        # Battery voltage (mV)
        voltage = props.get("voltage_mv")
        state_volt = RuntimeState.AVAILABLE.value if voltage is not None and voltage > 0 else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_voltage",
            state=state_volt,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_volt), verified=state_volt == RuntimeState.AVAILABLE.value),
            value=voltage if state_volt == RuntimeState.AVAILABLE.value else None,
            unit="mV",
            source="BatteryManager.EXTRA_VOLTAGE",
            verified=state_volt == RuntimeState.AVAILABLE.value,
            verification_method="battery_broadcast_check",
            observed_at=now if state_volt == RuntimeState.AVAILABLE.value else None,
            evidence_ref="battery_props.json#voltage" if state_volt == RuntimeState.AVAILABLE.value else None,
        ))

        # Battery temperature (°C)
        temp_c = props.get("temperature_c")
        state_temp = RuntimeState.AVAILABLE.value if temp_c is not None and -20 <= temp_c <= 80 else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_temperature",
            state=state_temp,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_temp), verified=state_temp == RuntimeState.AVAILABLE.value),
            value=temp_c if state_temp == RuntimeState.AVAILABLE.value else None,
            unit="degC",
            source="BatteryManager.EXTRA_TEMPERATURE / 10.0",
            verified=state_temp == RuntimeState.AVAILABLE.value,
            verification_method="battery_broadcast_check",
            observed_at=now if state_temp == RuntimeState.AVAILABLE.value else None,
            evidence_ref="battery_props.json#temperature" if state_temp == RuntimeState.AVAILABLE.value else None,
        ))

        # Battery current now (mA)
        # Handle sentinel values: Integer.MIN_VALUE or 0 when unsupported
        current_ma = props.get("current_now_ma")
        sentinel = props.get("current_now_is_sentinel", False)
        state_curr = RuntimeState.AVAILABLE.value if (current_ma is not None and not sentinel) else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_current_now",
            state=state_curr,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_curr), verified=state_curr == RuntimeState.AVAILABLE.value),
            value=current_ma if state_curr == RuntimeState.AVAILABLE.value else None,
            unit="mA",
            source="BatteryManager.BATTERY_PROPERTY_CURRENT_NOW",
            verified=state_curr == RuntimeState.AVAILABLE.value,
            verification_method="battery_property_check",
            observed_at=now if state_curr == RuntimeState.AVAILABLE.value else None,
            evidence_ref="battery_props.json#current_now" if state_curr == RuntimeState.AVAILABLE.value else None,
            notes="Sentinel or unsupported readings are assigned state UNAVAILABLE with value=null.",
        ))

        # Battery charge counter (uAh)
        charge_counter = props.get("charge_counter_uah")
        sentinel_chg = props.get("charge_counter_is_sentinel", False)
        state_chg = RuntimeState.AVAILABLE.value if (charge_counter is not None and not sentinel_chg) else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_charge_counter",
            state=state_chg,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_chg), verified=state_chg == RuntimeState.AVAILABLE.value),
            value=charge_counter if state_chg == RuntimeState.AVAILABLE.value else None,
            unit="uAh",
            source="BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER",
            verified=state_chg == RuntimeState.AVAILABLE.value,
            verification_method="battery_property_check",
            observed_at=now if state_chg == RuntimeState.AVAILABLE.value else None,
            evidence_ref="battery_props.json#charge_counter" if state_chg == RuntimeState.AVAILABLE.value else None,
        ))

        return TelemetryCapability(
            dimension="battery",
            results=results,
            resource_state_input=True,
            reliability="REQUIRES PILOT VALIDATION",
        )


class MemoryTelemetryCollector:
    """Collector 4: MemoryTelemetryCollector.
    Checks total/available RAM, threshold, low-memory flag, app memory, process memory.
    """

    def collect(self, memory_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = memory_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        avail_mem_mb = props.get("avail_mem_mb")
        state_avail = RuntimeState.AVAILABLE.value if avail_mem_mb is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="available_memory_mb",
            state=state_avail,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_avail), verified=avail_mem_mb is not None),
            value=avail_mem_mb if avail_mem_mb is not None else None,
            unit="MB",
            source="ActivityManager.MemoryInfo.availMem",
            verified=avail_mem_mb is not None,
            verification_method="memory_info_check",
            observed_at=now if avail_mem_mb is not None else None,
            evidence_ref="memory_props.json#avail_mem_mb" if avail_mem_mb is not None else None,
        ))

        low_mem_flag = props.get("low_memory_flag")
        state_low = RuntimeState.AVAILABLE.value if low_mem_flag is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="low_memory_flag",
            state=state_low,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_low), verified=low_mem_flag is not None),
            value=low_mem_flag if low_mem_flag is not None else None,
            source="ActivityManager.MemoryInfo.lowMemory",
            verified=low_mem_flag is not None,
            verification_method="memory_info_check",
            observed_at=now if low_mem_flag is not None else None,
            evidence_ref="memory_props.json#low_memory_flag" if low_mem_flag is not None else None,
        ))

        app_heap_mb = props.get("app_heap_allocated_mb")
        state_app = RuntimeState.AVAILABLE.value if app_heap_mb is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="app_heap_allocated_mb",
            state=state_app,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_app), verified=app_heap_mb is not None),
            value=app_heap_mb if app_heap_mb is not None else None,
            unit="MB",
            source="Runtime.totalMemory() - freeMemory()",
            verified=app_heap_mb is not None,
            verification_method="runtime_heap_check",
            observed_at=now if app_heap_mb is not None else None,
            evidence_ref="memory_props.json#app_heap_allocated_mb" if app_heap_mb is not None else None,
        ))

        psi_readable = props.get("psi_memory_readable")
        state_psi = RuntimeState.AVAILABLE.value if psi_readable is True else (
            RuntimeState.PERMISSION_REQUIRED.value if psi_readable is False else RuntimeState.UNAVAILABLE.value
        )
        results.append(CapabilityResult(
            metric="psi_memory_pressure",
            state=state_psi,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_psi), verified=psi_readable is True),
            value="PSI readable" if psi_readable is True else None,
            source="/proc/pressure/memory",
            verified=psi_readable is True,
            verification_method="file_read_check",
            observed_at=now if psi_readable is True else None,
            evidence_ref="memory_props.json#psi" if psi_readable is True else None,
        ))

        return TelemetryCapability(
            dimension="memory",
            results=results,
            resource_state_input=True,
            reliability="REQUIRES PILOT VALIDATION",
        )


class CPUTelemetryCollector:
    """Collector 5: CPUTelemetryCollector.
    Checks CPU core count, frequencies, app CPU time, device-wide CPU utilization.
    """

    def collect(self, cpu_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = cpu_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        core_count = props.get("core_count")
        state_cores = RuntimeState.AVAILABLE.value if core_count is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="cpu_core_count",
            state=state_cores,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_cores), verified=core_count is not None),
            value=core_count if core_count is not None else None,
            unit="cores",
            source="Runtime.availableProcessors() / /sys/devices/system/cpu/possible",
            verified=core_count is not None,
            verification_method="cpu_sysfs_check",
            observed_at=now if core_count is not None else None,
            evidence_ref="cpu_props.json#core_count" if core_count is not None else None,
        ))

        cur_freq_khz = props.get("cur_freq_khz")
        state_freq = RuntimeState.AVAILABLE.value if cur_freq_khz is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="cpu_scaling_cur_freq",
            state=state_freq,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_freq), verified=cur_freq_khz is not None),
            value=cur_freq_khz if cur_freq_khz is not None else None,
            unit="kHz",
            source="/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq",
            verified=cur_freq_khz is not None,
            verification_method="cpufreq_sysfs_check",
            observed_at=now if cur_freq_khz is not None else None,
            evidence_ref="cpu_props.json#scaling_cur_freq" if cur_freq_khz is not None else None,
        ))

        app_cpu_time_ms = props.get("app_cpu_time_ms")
        state_app_cpu = RuntimeState.AVAILABLE.value if app_cpu_time_ms is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="app_cpu_time",
            state=state_app_cpu,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_app_cpu), verified=app_cpu_time_ms is not None),
            value=app_cpu_time_ms if app_cpu_time_ms is not None else None,
            unit="ms",
            source="Process.getElapsedCpuTime() / /proc/self/stat",
            verified=app_cpu_time_ms is not None,
            verification_method="process_stat_check",
            observed_at=now if app_cpu_time_ms is not None else None,
            evidence_ref="cpu_props.json#app_cpu_time" if app_cpu_time_ms is not None else None,
        ))

        # Device-wide CPU utilization: app read of /proc/stat is restricted on Android 8+
        proc_stat_adb = props.get("proc_stat_readable_via_adb")
        state_proc = RuntimeState.AVAILABLE.value if proc_stat_adb is True else RuntimeState.PERMISSION_REQUIRED.value
        cond_proc = "HOST ADB SHELL" if proc_stat_adb is True else None
        results.append(CapabilityResult(
            metric="device_wide_cpu_utilization",
            state=state_proc,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_proc), verified=proc_stat_adb is True, condition=cond_proc),
            value="Readable via host ADB" if proc_stat_adb is True else None,
            source="/proc/stat via ADB shell",
            condition=cond_proc,
            verified=proc_stat_adb is True,
            verification_method="adb_shell_proc_stat_check",
            observed_at=now if proc_stat_adb is True else None,
            evidence_ref="cpu_props.json#proc_stat_adb" if proc_stat_adb is True else None,
            notes="App-level read of /proc/stat is PERMISSION_REQUIRED on Android 8+ SELinux.",
        ))

        return TelemetryCapability(
            dimension="cpu",
            results=results,
            resource_state_input=True,
            reliability="REQUIRES PILOT VALIDATION",
        )


class GPUTelemetryCollector:
    """Collector 6: GPUTelemetryCollector.
    Checks GPU identification, utilization, frequency, and sysfs readability.
    If unavailable, state is UNAVAILABLE with value=null.
    """

    def collect(self, gpu_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = gpu_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        renderer = props.get("renderer")
        state_rend = RuntimeState.AVAILABLE.value if renderer else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_vendor_renderer",
            state=state_rend,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_rend), verified=bool(renderer)),
            value=renderer if renderer else None,
            source="GLES20.glGetString(GL_RENDERER)",
            verified=bool(renderer),
            verification_method="gles_string_check",
            observed_at=now if renderer else None,
            evidence_ref="gpu_props.json#renderer" if renderer else None,
        ))

        gpu_freq = props.get("gpu_freq_hz")
        state_freq = RuntimeState.AVAILABLE.value if gpu_freq is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_frequency",
            state=state_freq,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_freq), verified=gpu_freq is not None),
            value=gpu_freq if gpu_freq is not None else None,
            unit="Hz",
            source="/sys/class/kgsl/kgsl-3d0/gpuclk",
            verified=gpu_freq is not None,
            verification_method="kgsl_sysfs_check",
            observed_at=now if gpu_freq is not None else None,
            evidence_ref="gpu_props.json#gpu_freq" if gpu_freq is not None else None,
        ))

        # GPU utilization is expected UNAVAILABLE through standard Android platform interfaces
        gpu_util = props.get("gpu_utilization_percent")
        state_util = RuntimeState.AVAILABLE.value if gpu_util is not None else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_utilization",
            state=state_util,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_util), verified=gpu_util is not None),
            value=gpu_util if gpu_util is not None else None,
            unit="percent",
            source="/sys/class/kgsl/kgsl-3d0/gpubusy",
            verified=gpu_util is not None,
            verification_method="kgsl_busy_check",
            observed_at=now if gpu_util is not None else None,
            evidence_ref="gpu_props.json#gpu_util" if gpu_util is not None else None,
            notes="UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE unless root/custom driver permissions exist.",
        ))

        return TelemetryCapability(
            dimension="gpu",
            results=results,
            resource_state_input=False,  # Unusable as resource_state_input if unavailable
            reliability="NOT YET VERIFIED",
        )


class ThermalTelemetryCollector:
    """Collector 7: ThermalTelemetryCollector.
    Checks thermal status API (API>=29), thermal headroom API (API>=30), thermal zones,
    frequency capping, and selects D-10 thermal source.
    """

    def collect(self, thermal_props: Optional[Dict[str, Any]] = None) -> ThermalCapability:
        props = thermal_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Thermal status API (API >= 29)
        status_api_avail = props.get("thermal_status_api_available")
        api_level = props.get("api_level", 28)
        if api_level < 29:
            status_api_state = RuntimeState.API_UNSUPPORTED.value
            status_api_val = None
        elif status_api_avail is True:
            status_api_state = RuntimeState.AVAILABLE.value
            status_api_val = "PowerManager.getCurrentThermalStatus() functional"
        else:
            status_api_state = RuntimeState.UNAVAILABLE.value
            status_api_val = None

        res_status_api = CapabilityResult(
            metric="thermal_status_api",
            state=status_api_state,
            report_status=map_runtime_state_to_report_status(RuntimeState(status_api_state), verified=status_api_state == RuntimeState.AVAILABLE.value),
            value=status_api_val,
            source="PowerManager.getCurrentThermalStatus()",
            min_api=29,
            verified=status_api_state == RuntimeState.AVAILABLE.value,
            verification_method="power_manager_thermal_status_check",
            observed_at=now if status_api_state == RuntimeState.AVAILABLE.value else None,
            evidence_ref="thermal_props.json#status_api" if status_api_state == RuntimeState.AVAILABLE.value else None,
        )

        # Thermal headroom API (API >= 30)
        headroom_api_avail = props.get("thermal_headroom_api_available")
        if api_level < 30:
            headroom_state = RuntimeState.API_UNSUPPORTED.value
            headroom_val = None
        elif headroom_api_avail is True:
            headroom_state = RuntimeState.AVAILABLE.value
            headroom_val = "PowerManager.getThermalHeadroom() functional"
        else:
            headroom_state = RuntimeState.UNAVAILABLE.value
            headroom_val = None

        res_headroom_api = CapabilityResult(
            metric="thermal_headroom_api",
            state=headroom_state,
            report_status=map_runtime_state_to_report_status(RuntimeState(headroom_state), verified=headroom_state == RuntimeState.AVAILABLE.value),
            value=headroom_val,
            source="PowerManager.getThermalHeadroom()",
            min_api=30,
            verified=headroom_state == RuntimeState.AVAILABLE.value,
            verification_method="power_manager_thermal_headroom_check",
            observed_at=now if headroom_state == RuntimeState.AVAILABLE.value else None,
            evidence_ref="thermal_props.json#headroom_api" if headroom_state == RuntimeState.AVAILABLE.value else None,
        )

        # Temperature sources
        temp_sources: List[CapabilityResult] = []

        # Battery temperature source
        batt_temp_avail = props.get("battery_temp_available")
        state_batt_t = RuntimeState.AVAILABLE.value if batt_temp_avail is True else RuntimeState.UNAVAILABLE.value
        temp_sources.append(CapabilityResult(
            metric="temperature_battery",
            state=state_batt_t,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_batt_t), verified=batt_temp_avail is True),
            value="BatteryManager EXTRA_TEMPERATURE" if batt_temp_avail is True else None,
            unit="degC",
            source="BatteryManager broadcast",
            verified=batt_temp_avail is True,
            verification_method="battery_temperature_check",
            observed_at=now if batt_temp_avail is True else None,
            evidence_ref="thermal_props.json#battery_temp" if batt_temp_avail is True else None,
        ))

        # Thermal zones sysfs
        zones_count = props.get("thermal_zones_readable_count", 0)
        state_zones = RuntimeState.AVAILABLE.value if zones_count > 0 else RuntimeState.UNAVAILABLE.value
        temp_sources.append(CapabilityResult(
            metric="thermal_zones_sysfs",
            state=state_zones,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_zones), verified=zones_count > 0),
            value=f"{zones_count} thermal zones readable" if zones_count > 0 else None,
            unit="zones",
            source="/sys/class/thermal/thermal_zone*",
            verified=zones_count > 0,
            verification_method="thermal_zone_sysfs_read_check",
            observed_at=now if zones_count > 0 else None,
            evidence_ref="thermal_props.json#thermal_zones" if zones_count > 0 else None,
        ))

        # Frequency capping observable
        freq_capping = props.get("frequency_capping_observable")
        state_cap = RuntimeState.AVAILABLE.value if freq_capping is True else RuntimeState.UNAVAILABLE.value
        res_freq_cap = CapabilityResult(
            metric="frequency_capping_observable",
            state=state_cap,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_cap), verified=freq_capping is True),
            value="Observed scaling_max_freq drops" if freq_capping is True else None,
            source="cpufreq scaling_max_freq vs scaling_boost_freq / cpuinfo_max_freq",
            verified=freq_capping is True,
            verification_method="cpufreq_capping_check",
            observed_at=now if freq_capping is True else None,
            evidence_ref="thermal_props.json#freq_capping" if freq_capping is True else None,
        )

        # External surface probe
        res_ext_probe = CapabilityResult(
            metric="external_surface_probe",
            state=RuntimeState.EXTERNAL_REQUIRED.value,
            report_status=ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION.value,
            value=None,
            unit="degC",
            source="External thermocouple / infrared surface probe",
            verified=False,
            verification_method="external_instrument_check",
            notes="Requires external contact thermocouple or calibrated infrared thermal camera.",
        )

        # D-10 Thermal source selection
        if status_api_state == RuntimeState.AVAILABLE.value:
            selected_source = "platform_thermal_status"
        else:
            selected_source = "fallback_temperature_and_frequency_capping"

        return ThermalCapability(
            thermal_status_api=res_status_api,
            thermal_headroom_api=res_headroom_api,
            temperature_sources=temp_sources,
            frequency_capping_observable=res_freq_cap,
            external_surface_probe=res_ext_probe,
            selected_thermal_source=selected_source,
        )


class CameraCapabilityCollector:
    """Collector 8: CameraCapabilityCollector.
    Checks camera IDs, hardware levels, formats/sizes, FPS ranges, manual controls,
    and checks advertised-vs-honoured manual controls via CaptureResult.
    """

    def collect(self, camera_props: Optional[Dict[str, Any]] = None) -> List[CameraCapability]:
        props = camera_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        camera_ids = props.get("camera_ids", ["0"])
        results_list: List[CameraCapability] = []

        for cid in camera_ids:
            cam_info = props.get(f"camera_{cid}", {})
            res_cam: List[CapabilityResult] = []

            # Hardware level
            hw_level = cam_info.get("hardware_level")
            state_hw = RuntimeState.AVAILABLE.value if hw_level else RuntimeState.UNAVAILABLE.value
            res_cam.append(CapabilityResult(
                metric="hardware_level",
                state=state_hw,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_hw), verified=bool(hw_level)),
                value=hw_level if hw_level else None,
                source=f"CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL (ID {cid})",
                verified=bool(hw_level),
                verification_method="camera_characteristics_check",
                observed_at=now if hw_level else None,
                evidence_ref=f"camera_{cid}_props.json#hardware_level" if hw_level else None,
            ))

            # Manual exposure control advertised
            man_exp = cam_info.get("manual_exposure_advertised")
            state_exp = RuntimeState.AVAILABLE.value if man_exp is True else RuntimeState.UNAVAILABLE.value
            res_cam.append(CapabilityResult(
                metric="manual_exposure_advertised",
                state=state_exp,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_exp), verified=man_exp is True),
                value="MANUAL_SENSOR capability advertised" if man_exp is True else None,
                source=f"CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES (ID {cid})",
                verified=man_exp is True,
                verification_method="camera_capabilities_check",
                observed_at=now if man_exp is True else None,
                evidence_ref=f"camera_{cid}_props.json#manual_exposure" if man_exp is True else None,
            ))

            # Advertised vs Honoured check for manual control
            honoured = cam_info.get("manual_control_honoured")
            state_hon = RuntimeState.AVAILABLE.value if honoured is True else (
                RuntimeState.UNAVAILABLE.value if honoured is False else RuntimeState.NOT_TESTED.value
            )
            res_honoured = CapabilityResult(
                metric="manual_control_honoured",
                state=state_hon,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_hon), verified=honoured is True),
                value="CaptureResult confirms set exposure/ISO honoured" if honoured is True else None,
                source=f"CaptureResult metadata verification (ID {cid})",
                verified=honoured is True,
                verification_method="capture_result_honoured_check",
                observed_at=now if honoured is True else None,
                evidence_ref=f"camera_{cid}_props.json#manual_control_honoured" if honoured is True else None,
                notes="Distinguishes advertised capabilities from actually honoured camera capture parameters.",
            )

            results_list.append(CameraCapability(
                camera_id=cid,
                lens_facing=cam_info.get("lens_facing", "BACK"),
                results=res_cam,
                manual_control_honoured=res_honoured,
            ))

        return results_list


class InferenceBackendCapabilityCollector:
    """Collector 9: InferenceBackendCapabilityCollector.
    Checks backend availability, delegation (GPU/NNAPI), probability output validity.
    NO latency, accuracy, or throughput benchmarking is performed or reported.
    """

    def collect(self, backend_props: Optional[Dict[str, Any]] = None) -> List[BackendCapability]:
        props = backend_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        backends = ["TFLite_CPU", "TFLite_GPU", "TFLite_NNAPI", "ONNXRuntime_CPU", "ONNXRuntime_NNAPI"]
        out: List[BackendCapability] = []

        for b_name in backends:
            b_info = props.get(b_name, {})

            avail = b_info.get("available")
            state_avail = RuntimeState.AVAILABLE.value if avail is True else RuntimeState.UNAVAILABLE.value
            res_avail = CapabilityResult(
                metric="backend_availability",
                state=state_avail,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_avail), verified=avail is True),
                value=f"{b_name} runtime available" if avail is True else None,
                source=f"Runtime library initialization ({b_name})",
                verified=avail is True,
                verification_method="backend_init_check",
                observed_at=now if avail is True else None,
                evidence_ref=f"backend_{b_name}_props.json#availability" if avail is True else None,
            )

            deleg = b_info.get("delegation_working")
            state_deleg = RuntimeState.AVAILABLE.value if deleg is True else RuntimeState.UNAVAILABLE.value
            res_deleg = CapabilityResult(
                metric="backend_delegation",
                state=state_deleg,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_deleg), verified=deleg is True),
                value=f"{b_name} delegate loaded" if deleg is True else None,
                source=f"Delegate / EP load check ({b_name})",
                verified=deleg is True,
                verification_method="delegate_load_check",
                observed_at=now if deleg is True else None,
                evidence_ref=f"backend_{b_name}_props.json#delegation" if deleg is True else None,
            )

            prob = b_info.get("probability_output_valid")
            state_prob = RuntimeState.AVAILABLE.value if prob is True else RuntimeState.UNAVAILABLE.value
            res_prob = CapabilityResult(
                metric="probability_output_validity",
                state=state_prob,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_prob), verified=prob is True),
                value="Finite float output, correct shape, softmax sum ~= 1.0" if prob is True else None,
                source=f"Reference graph output validation ({b_name})",
                verified=prob is True,
                verification_method="reference_graph_output_check",
                observed_at=now if prob is True else None,
                evidence_ref=f"backend_{b_name}_props.json#probability_output" if prob is True else None,
                notes="Capability check only; no latency, throughput or accuracy benchmarking performed.",
            )

            out.append(BackendCapability(
                backend=b_name,
                runtime_version=b_info.get("version"),
                availability=res_avail,
                delegation=res_deleg,
                probability_output=res_prob,
                quantization_support=[],
                reference_graph_hash=b_info.get("reference_graph_hash"),
                known_limitations=b_info.get("known_limitations", []),
            ))

        return out


class ProfilingCapabilityCollector:
    """Collector 10: ProfilingCapabilityCollector.
    Checks clock sources, timer overhead, Android Trace API, ADB tracing availability.
    """

    def collect(self, profiling_props: Optional[Dict[str, Any]] = None) -> List[CapabilityResult]:
        props = profiling_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        results: List[CapabilityResult] = []

        nano_time = props.get("system_nano_time_available")
        state_nano = RuntimeState.AVAILABLE.value if nano_time is True else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="system_nano_time",
            state=state_nano,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_nano), verified=nano_time is True),
            value="System.nanoTime() / SystemClock.elapsedRealtimeNanos() functional" if nano_time is True else None,
            unit="ns",
            source="System.nanoTime() / SystemClock.elapsedRealtimeNanos()",
            verified=nano_time is True,
            verification_method="clock_source_check",
            observed_at=now if nano_time is True else None,
            evidence_ref="profiling_props.json#nano_time" if nano_time is True else None,
        ))

        trace_api = props.get("android_trace_api_available")
        state_trace = RuntimeState.AVAILABLE.value if trace_api is True else RuntimeState.UNAVAILABLE.value
        results.append(CapabilityResult(
            metric="android_trace_api",
            state=state_trace,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_trace), verified=trace_api is True),
            value="android.os.Trace beginSection/endSection functional" if trace_api is True else None,
            source="android.os.Trace",
            verified=trace_api is True,
            verification_method="trace_api_check",
            observed_at=now if trace_api is True else None,
            evidence_ref="profiling_props.json#trace_api" if trace_api is True else None,
        ))

        atrace_adb = props.get("atrace_adb_available")
        state_atrace = RuntimeState.AVAILABLE.value if atrace_adb is True else RuntimeState.UNAVAILABLE.value
        cond_atrace = "HOST ADB SHELL" if atrace_adb is True else None
        results.append(CapabilityResult(
            metric="adb_atrace_profiling",
            state=state_atrace,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_atrace), verified=atrace_adb is True, condition=cond_atrace),
            value="atrace / systrace / perfetto via ADB available" if atrace_adb is True else None,
            source="ADB shell atrace / perfetto",
            condition=cond_atrace,
            verified=atrace_adb is True,
            verification_method="adb_atrace_check",
            observed_at=now if atrace_adb is True else None,
            evidence_ref="profiling_props.json#atrace_adb" if atrace_adb is True else None,
        ))

        return results


class EnergyMeasurementCapabilityChecker:
    """Collector 11: EnergyMeasurementCapabilityChecker.
    Evaluates E-1 (battery-side external), E-2 (supply-powered session), E-3 (software relative counters).
    Outputs selected_level from evidence. absolute_energy_claimed is FIXED false.
    """

    def collect(self, energy_props: Optional[Dict[str, Any]] = None) -> EnergyCapability:
        props = energy_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # E-1 Battery-side reference
        e1_feat = props.get("E1_feasible")
        state_e1 = RuntimeState.EXTERNAL_REQUIRED.value if e1_feat is False or e1_feat is None else RuntimeState.AVAILABLE.value
        res_e1 = CapabilityResult(
            metric="E1_battery_side_reference",
            state=state_e1,
            report_status=ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION.value,
            value="Feasible with external power meter + battery terminal access" if e1_feat is True else None,
            source="External power meter (e.g. Monsoon / Yokogawa / Keysight)",
            verified=False,
            verification_method="external_hardware_feasibility_check",
            notes="Requires physical battery terminal access and safety sign-off.",
        )

        # E-2 Supply-powered session
        e2_feat = props.get("E2_feasible")
        state_e2 = RuntimeState.EXTERNAL_REQUIRED.value if e2_feat is False or e2_feat is None else RuntimeState.AVAILABLE.value
        res_e2 = CapabilityResult(
            metric="E2_supply_powered_session",
            state=state_e2,
            report_status=ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION.value,
            value="Feasible with external USB power meter during controlled session" if e2_feat is True else None,
            source="External USB power meter / inline power monitor",
            verified=False,
            verification_method="external_usb_meter_check",
            notes="USB battery charging current must be accounted for or isolated.",
        )

        # E-3 Software relative counters
        e3_avail = props.get("E3_counters_available")
        state_e3 = RuntimeState.AVAILABLE.value if e3_avail is True else RuntimeState.UNAVAILABLE.value
        res_e3 = CapabilityResult(
            metric="E3_software_counters",
            state=state_e3,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_e3), verified=e3_avail is True),
            value="BatteryManager software current/charge counters readable" if e3_avail is True else None,
            source="BatteryManager BATTERY_PROPERTY_CURRENT_NOW / CHARGE_COUNTER",
            verified=e3_avail is True,
            verification_method="software_counter_check",
            observed_at=now if e3_avail is True else None,
            evidence_ref="energy_props.json#E3_counters" if e3_avail is True else None,
            notes="Relative software comparison only; NO absolute energy claimed.",
        )

        # Level selection based on evidence
        selected_level = props.get("selected_level")
        if not selected_level:
            if e1_feat is True:
                selected_level = "E-1"
            elif e2_feat is True:
                selected_level = "E-2"
            elif e3_avail is True:
                selected_level = "E-3"
            else:
                selected_level = None

        return EnergyCapability(
            E1_battery_side_reference=res_e1,
            E2_supply_powered_session=res_e2,
            E3_software_counters=res_e3,
            selected_level=selected_level,
            absolute_energy_claimed=False,  # FIXED FALSE
        )
