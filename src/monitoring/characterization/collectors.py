"""
Collector implementations for Step 10D device characterization.

Implements collectors 1-11 for checking device identity, Android capabilities,
battery, memory, CPU, GPU, thermal, camera, inference backends, profiling,
and energy measurement feasibility.

Strictly follows the status/value separation and no-fake-zeros rules:
- F-03: Missing inputs / unexecuted probes yield state=NOT_TESTED (never UNAVAILABLE or ERROR).
- F-04: API level is NEVER assumed (api_level=None yields NOT_TESTED).
- F-05: verified=True ONLY for real device observations with existing evidence references.
- F-10: Error preservation (implausible values set state=ERROR with raw value retained).
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


def _determine_state_and_verification(
    props: Dict[str, Any],
    key: str,
    evidence_key: Optional[str] = None
) -> Tuple[str, bool, Optional[str]]:
    """Helper to determine state, verified flag, and evidence_ref for a property."""
    is_real_device = bool(props.get("is_real_device_observation", False))
    val = props.get(key)
    
    if key not in props:
        return RuntimeState.NOT_TESTED.value, False, None
    if val is None:
        # Key present but value is None (unsupported/unavailable probe result)
        return RuntimeState.UNAVAILABLE.value, False, None
    
    # Value present
    state = RuntimeState.AVAILABLE.value
    verified = is_real_device
    evidence_ref = f"evidence/observed_props.json#{evidence_key or key}" if verified else None
    return state, verified, evidence_ref


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
        observed_results: List[CapabilityResult] = []

        # Manufacturer
        obs_mfr = props.get("manufacturer") or props.get("ro.product.manufacturer")
        state_mfr, ver_mfr, ev_mfr = _determine_state_and_verification(
            props, "manufacturer" if "manufacturer" in props else "ro.product.manufacturer"
        )
        if "manufacturer" not in props and "ro.product.manufacturer" not in props:
            state_mfr = RuntimeState.NOT_TESTED.value
            ver_mfr = False
            ev_mfr = None

        observed_results.append(CapabilityResult(
            metric="manufacturer",
            state=state_mfr,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_mfr), verified=ver_mfr),
            value=obs_mfr if state_mfr == RuntimeState.AVAILABLE.value else None,
            source="Build.MANUFACTURER / getprop",
            verified=ver_mfr,
            verification_method="device_observation",
            observed_at=now if ver_mfr else None,
            evidence_ref=ev_mfr,
        ))

        # Model
        obs_model = props.get("model") or props.get("ro.product.model")
        state_model = RuntimeState.AVAILABLE.value if obs_model else (
            RuntimeState.UNAVAILABLE.value if ("model" in props or "ro.product.model" in props) else RuntimeState.NOT_TESTED.value
        )
        ver_model = bool(props.get("is_real_device_observation") and obs_model)
        ev_model = "evidence/getprop_evidence.txt#ro.product.model" if ver_model else None

        observed_results.append(CapabilityResult(
            metric="model",
            state=state_model,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_model), verified=ver_model),
            value=obs_model if state_model == RuntimeState.AVAILABLE.value else None,
            source="Build.MODEL / getprop",
            verified=ver_model,
            verification_method="device_observation",
            observed_at=now if ver_model else None,
            evidence_ref=ev_model,
        ))

        # Total RAM
        total_ram_mb = props.get("total_ram_mb")
        state_ram = RuntimeState.AVAILABLE.value if total_ram_mb is not None else (
            RuntimeState.UNAVAILABLE.value if "total_ram_mb" in props else RuntimeState.NOT_TESTED.value
        )
        ver_ram = bool(props.get("is_real_device_observation") and total_ram_mb is not None)
        ev_ram = "evidence/meminfo_evidence.txt#total_ram_mb" if ver_ram else None

        observed_results.append(CapabilityResult(
            metric="total_ram_mb",
            state=state_ram,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_ram), verified=ver_ram),
            value=total_ram_mb if state_ram == RuntimeState.AVAILABLE.value else None,
            unit="MB",
            source="ActivityManager.MemoryInfo.totalMem / /proc/meminfo",
            verified=ver_ram,
            verification_method="device_observation",
            observed_at=now if ver_ram else None,
            evidence_ref=ev_ram,
        ))

        # SoC Model (P-04 provenance check)
        obs_soc = props.get("soc_model") or props.get("ro.soc.model")
        source_soc_prop = props.get("source_soc_prop")
        state_soc = RuntimeState.AVAILABLE.value if obs_soc else (
            RuntimeState.UNAVAILABLE.value if ("soc_model" in props or "ro.soc.model" in props or "source_soc_prop" in props) else RuntimeState.NOT_TESTED.value
        )
        ver_soc = bool(props.get("is_real_device_observation") and obs_soc)
        
        if ver_soc and obs_soc:
            if source_soc_prop == "ro.soc.model":
                ev_soc = "evidence/getprop_evidence.txt#ro.soc.model"
            elif source_soc_prop == "ro.board.platform":
                ev_soc = "evidence/getprop_evidence.txt#ro.board.platform"
            elif source_soc_prop in ("Hardware (/proc/cpuinfo)", "hardware"):
                ev_soc = "evidence/cpuinfo_evidence.txt#Hardware"
            else:
                ev_soc = "evidence/getprop_evidence.txt#ro.soc.model"
        else:
            ev_soc = None

        observed_results.append(CapabilityResult(
            metric="soc_model",
            state=state_soc,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_soc), verified=ver_soc),
            value=obs_soc if state_soc == RuntimeState.AVAILABLE.value else None,
            source=f"Build.SOC_MODEL / {source_soc_prop or 'getprop'}",
            min_api=31,
            verified=ver_soc,
            verification_method="device_observation",
            observed_at=now if ver_soc else None,
            evidence_ref=ev_soc,
        ))

        # GPU Renderer
        obs_gpu = props.get("gpu_renderer") or props.get("gles_renderer")
        state_gpu = RuntimeState.AVAILABLE.value if obs_gpu else (
            RuntimeState.UNAVAILABLE.value if ("gpu_renderer" in props or "gles_renderer" in props) else RuntimeState.NOT_TESTED.value
        )
        ver_gpu = bool(props.get("is_real_device_observation") and obs_gpu)
        ev_gpu = "evidence/observed_props.json#gpu_renderer" if ver_gpu else None

        observed_results.append(CapabilityResult(
            metric="gpu_renderer",
            state=state_gpu,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_gpu), verified=ver_gpu),
            value=obs_gpu if state_gpu == RuntimeState.AVAILABLE.value else None,
            source="GLES20.glGetString(GL_RENDERER) / EGL",
            verified=ver_gpu,
            verification_method="device_observation",
            observed_at=now if ver_gpu else None,
            evidence_ref=ev_gpu,
        ))

        # Variant check (3 GB RAM variant, expected nominal range 2700 MB - 3300 MB)
        if total_ram_mb is not None:
            if 2700 <= total_ram_mb <= 3300:
                variant_val = f"3 GB variant verified (observed total RAM: {total_ram_mb} MB)"
                ver_v = bool(props.get("is_real_device_observation"))
                variant_res = CapabilityResult(
                    metric="variant_check",
                    state=RuntimeState.AVAILABLE.value,
                    report_status=ReportStatus.VERIFIED.value if ver_v else ReportStatus.AVAILABLE.value,
                    value=variant_val,
                    unit="variant",
                    source="MemoryInfo.totalMem RAM range check",
                    verified=ver_v,
                    verification_method="observed_ram_range_verification",
                    observed_at=now if ver_v else None,
                    evidence_ref="evidence/meminfo_evidence.txt#ram_variant_check" if ver_v else None,
                    notes="Observed RAM matches the required 3 GB experimental platform variant.",
                )
            else:
                variant_val = f"DISAGREEMENT: Observed RAM {total_ram_mb} MB does not match 3 GB variant range (2700-3300 MB)"
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
                state=RuntimeState.NOT_TESTED.value,
                report_status=ReportStatus.NOT_YET_VERIFIED.value,
                value=None,
                unit="variant",
                source="MemoryInfo.totalMem RAM range check",
                verified=False,
                verification_method="observed_ram_range_verification",
                notes="Total RAM not yet observed on device.",
            )

        # Determine P-01 run-specific identity_match_status
        obs_mfr_u = str(obs_mfr).upper() if obs_mfr else ""
        obs_model_u = str(obs_model).upper() if obs_model else ""
        obs_soc_u = str(obs_soc).upper() if obs_soc else ""

        if obs_model or obs_mfr:
            model_match = ("A5" in obs_model_u and "2020" in obs_model_u) or ("CPH1931" in obs_model_u) or (obs_model_u == known.model.upper())
            mfr_match = ("OPPO" in obs_mfr_u) or not obs_mfr
            soc_match = ("665" in obs_soc_u) or ("SM6125" in obs_soc_u) or not obs_soc

            if model_match and mfr_match and soc_match:
                id_match = "MATCH"
            else:
                id_match = "MISMATCH"
        else:
            id_match = "UNKNOWN"

        return DeviceIdentity(
            device_unit_id=self.device_unit_id,
            known_specification=known,
            observed=observed_results,
            variant_check=variant_res,
            identity_match_status=id_match,
        )


class AndroidCapabilityCollector:
    """Collector 2: AndroidCapabilityCollector.
    Checks release version, API level, security patch, and platform services.
    """

    def collect(self, android_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = android_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []

        api_level = props.get("api_level")
        state_api = RuntimeState.AVAILABLE.value if api_level is not None else (
            RuntimeState.UNAVAILABLE.value if "api_level" in props else RuntimeState.NOT_TESTED.value
        )
        ver_api = is_real and api_level is not None
        results.append(CapabilityResult(
            metric="api_level",
            state=state_api,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_api), verified=ver_api),
            value=api_level if state_api == RuntimeState.AVAILABLE.value else None,
            source="Build.VERSION.SDK_INT",
            verified=ver_api,
            verification_method="device_observation",
            observed_at=now if ver_api else None,
            evidence_ref="evidence/getprop_evidence.txt#ro.build.version.sdk" if ver_api else None,
        ))

        rel_version = props.get("release_version")
        state_rel = RuntimeState.AVAILABLE.value if rel_version else (
            RuntimeState.UNAVAILABLE.value if "release_version" in props else RuntimeState.NOT_TESTED.value
        )
        ver_rel = is_real and bool(rel_version)
        results.append(CapabilityResult(
            metric="release_version",
            state=state_rel,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_rel), verified=ver_rel),
            value=rel_version if state_rel == RuntimeState.AVAILABLE.value else None,
            source="Build.VERSION.RELEASE",
            verified=ver_rel,
            verification_method="device_observation",
            observed_at=now if ver_rel else None,
            evidence_ref="evidence/getprop_evidence.txt#ro.build.version.release" if ver_rel else None,
        ))

        services = ["PowerManager", "HardwarePropertiesManager", "CameraManager", "ActivityManager", "BatteryManager"]
        for svc in services:
            key = f"service_{svc}"
            avail = props.get(key)
            if key not in props:
                state_svc = RuntimeState.NOT_TESTED.value
            elif avail is True:
                state_svc = RuntimeState.AVAILABLE.value
            else:
                state_svc = RuntimeState.UNAVAILABLE.value
            
            ver_svc = is_real and state_svc == RuntimeState.AVAILABLE.value
            results.append(CapabilityResult(
                metric=key,
                state=state_svc,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_svc), verified=ver_svc),
                value=f"{svc} available" if state_svc == RuntimeState.AVAILABLE.value else None,
                source=f"Context.getSystemService({svc})",
                verified=ver_svc,
                verification_method="service_get_check",
                observed_at=now if ver_svc else None,
                evidence_ref=f"evidence/android_app_evidence.json#{key}" if ver_svc else None,
            ))

        return TelemetryCapability(
            dimension="android",
            results=results,
            resource_state_input=False,
            reliability="NOT YET VERIFIED",
        )


class BatteryTelemetryCollector:
    """Collector 3: BatteryTelemetryCollector.
    Checks battery level, percentage, voltage, temperature, health, current, counters.
    F-10: Implausible values set state=ERROR with raw values retained.
    P-07: Failed probe returns state=ERROR.
    R-09: Raw 0 current is NOT verified. Unit conversions >10,000 uA handled.
    """

    def collect(self, battery_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = battery_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []
        probe_err_bat = props.get("probe_error_battery")

        # Battery level (%)
        if "battery_level_percent" not in props and "level" not in props:
            if probe_err_bat:
                state_lvl = RuntimeState.ERROR.value
                err_lvl = probe_err_bat
                val_lvl = None
                ev_lvl = "evidence/commands.log#probe_error_battery"
            else:
                state_lvl = RuntimeState.NOT_TESTED.value
                err_lvl = None
                val_lvl = None
                ev_lvl = None
        else:
            raw_lvl = props.get("battery_level_percent") if "battery_level_percent" in props else props.get("level")
            if raw_lvl is None:
                state_lvl = RuntimeState.UNAVAILABLE.value
                err_lvl = None
                val_lvl = None
                ev_lvl = None
            elif isinstance(raw_lvl, (int, float)) and 0 <= raw_lvl <= 100:
                state_lvl = RuntimeState.AVAILABLE.value
                err_lvl = None
                val_lvl = int(raw_lvl)
                ev_lvl = "evidence/battery_dumpsys_evidence.txt#battery_level_percent" if (is_real and state_lvl == RuntimeState.AVAILABLE.value) else None
            else:
                state_lvl = RuntimeState.ERROR.value
                err_lvl = f"Implausible battery level value observed: {raw_lvl}"
                val_lvl = None
                ev_lvl = None

        ver_lvl = is_real and state_lvl == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_level_percent",
            state=state_lvl,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_lvl), verified=ver_lvl),
            value=val_lvl,
            unit="percent",
            source="BatteryManager.EXTRA_LEVEL / ACTION_BATTERY_CHANGED / dumpsys battery",
            verified=ver_lvl,
            verification_method="battery_broadcast_check",
            observed_at=now if ver_lvl else None,
            evidence_ref=ev_lvl,
            error_message=err_lvl,
        ))

        # Battery voltage (mV)
        if "battery_voltage" not in props and "voltage_mv" not in props:
            if probe_err_bat:
                state_volt = RuntimeState.ERROR.value
                err_volt = probe_err_bat
                val_volt = None
                ev_volt = "evidence/commands.log#probe_error_battery"
            else:
                state_volt = RuntimeState.NOT_TESTED.value
                err_volt = None
                val_volt = None
                ev_volt = None
        else:
            raw_volt = props.get("battery_voltage") if "battery_voltage" in props else props.get("voltage_mv")
            if raw_volt is None:
                state_volt = RuntimeState.UNAVAILABLE.value
                err_volt = None
                val_volt = None
                ev_volt = None
            elif isinstance(raw_volt, (int, float)) and 2000 <= raw_volt <= 5000:
                state_volt = RuntimeState.AVAILABLE.value
                err_volt = None
                val_volt = float(raw_volt)
                ev_volt = "evidence/battery_dumpsys_evidence.txt#battery_voltage" if (is_real and state_volt == RuntimeState.AVAILABLE.value) else None
            else:
                state_volt = RuntimeState.ERROR.value
                err_volt = f"Implausible battery voltage value observed: {raw_volt} mV"
                val_volt = None
                ev_volt = None

        ver_volt = is_real and state_volt == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_voltage",
            state=state_volt,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_volt), verified=ver_volt),
            value=val_volt,
            unit="mV",
            source="BatteryManager.EXTRA_VOLTAGE / dumpsys battery",
            verified=ver_volt,
            verification_method="battery_broadcast_check",
            observed_at=now if ver_volt else None,
            evidence_ref=ev_volt,
            error_message=err_volt,
        ))

        # Battery temperature (°C)
        if "battery_temperature" not in props and "temperature_c" not in props:
            if probe_err_bat:
                state_temp = RuntimeState.ERROR.value
                err_temp = probe_err_bat
                val_temp = None
                ev_temp = "evidence/commands.log#probe_error_battery"
            else:
                state_temp = RuntimeState.NOT_TESTED.value
                err_temp = None
                val_temp = None
                ev_temp = None
        else:
            raw_temp = props.get("battery_temperature") if "battery_temperature" in props else props.get("temperature_c")
            if raw_temp is None:
                state_temp = RuntimeState.UNAVAILABLE.value
                err_temp = None
                val_temp = None
                ev_temp = None
            elif isinstance(raw_temp, (int, float)) and -20 <= raw_temp <= 80:
                state_temp = RuntimeState.AVAILABLE.value
                err_temp = None
                val_temp = float(raw_temp)
                ev_temp = "evidence/battery_dumpsys_evidence.txt#battery_temperature" if (is_real and state_temp == RuntimeState.AVAILABLE.value) else None
            else:
                state_temp = RuntimeState.ERROR.value
                err_temp = f"Implausible battery temperature value observed: {raw_temp} degC"
                val_temp = None
                ev_temp = None

        ver_temp = is_real and state_temp == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_temperature",
            state=state_temp,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_temp), verified=ver_temp),
            value=val_temp,
            unit="degC",
            source="BatteryManager.EXTRA_TEMPERATURE / dumpsys battery",
            verified=ver_temp,
            verification_method="battery_broadcast_check",
            observed_at=now if ver_temp else None,
            evidence_ref=ev_temp,
            error_message=err_temp,
        ))

        # Battery current now (mA / uA) — R-09 explicit handling
        if "battery_current_now" not in props and "current_now_ua" not in props and "current_now_ma" not in props:
            if probe_err_bat:
                state_curr = RuntimeState.ERROR.value
                val_curr = None
                ver_curr = False
                err_curr = probe_err_bat
                notes_curr = f"Battery probe failed: {probe_err_bat}"
                ev_curr = "evidence/commands.log#probe_error_battery"
            else:
                state_curr = RuntimeState.NOT_TESTED.value
                val_curr = None
                ver_curr = False
                err_curr = None
                notes_curr = "Current probe not executed."
                ev_curr = None
        else:
            curr_raw = props.get("battery_current_now") if "battery_current_now" in props else props.get("current_now_ma")
            curr_ua = props.get("current_now_ua")
            sentinel = props.get("current_now_is_sentinel", False)
            err_curr = None

            if sentinel or (curr_raw is None and curr_ua is None):
                state_curr = RuntimeState.UNAVAILABLE.value
                val_curr = None
                ver_curr = False
                notes_curr = "Current property is unsupported or sentinel value returned."
                ev_curr = None
            else:
                raw_val = curr_raw if curr_raw is not None else curr_ua
                # Unit conversion check: if absolute raw value > 10,000, convert uA -> mA
                if abs(raw_val) > 10000:
                    converted_ma = float(raw_val) / 1000.0
                else:
                    converted_ma = float(raw_val)

                if abs(converted_ma) > 10000:
                    state_curr = RuntimeState.ERROR.value
                    val_curr = None
                    ver_curr = False
                    err_curr = f"Implausible battery current value: {raw_val} (converted: {converted_ma} mA)"
                    notes_curr = f"Implausible battery current value: {raw_val}"
                    ev_curr = None
                elif converted_ma == 0.0:
                    # R-09: Zero current cannot be verified as valid physical measurement
                    state_curr = RuntimeState.AVAILABLE.value
                    val_curr = 0.0
                    ver_curr = False  # CANNOT BE VERIFIED
                    notes_curr = "Observed battery current reading is 0. Flagged as potential driver sentinel zero (unverified)."
                    ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now"
                else:
                    state_curr = RuntimeState.AVAILABLE.value
                    val_curr = converted_ma
                    ver_curr = is_real
                    notes_curr = f"Raw current reading: {raw_val}, converted to {converted_ma} mA."
                    ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now" if ver_curr else None

        results.append(CapabilityResult(
            metric="battery_current_now",
            state=state_curr,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_curr), verified=ver_curr),
            value=val_curr,
            unit="mA",
            source="BatteryManager.BATTERY_PROPERTY_CURRENT_NOW / dumpsys battery",
            verified=ver_curr,
            verification_method="battery_property_check",
            observed_at=now if (ver_curr or state_curr == RuntimeState.AVAILABLE.value) else None,
            evidence_ref=ev_curr,
            error_message=err_curr,
            notes=notes_curr,
        ))

        # Battery charge counter (uAh)
        if "battery_charge_counter" not in props and "charge_counter_uah" not in props:
            if probe_err_bat:
                state_chg = RuntimeState.ERROR.value
                val_chg = None
                err_chg = probe_err_bat
                ev_chg = "evidence/commands.log#probe_error_battery"
            else:
                state_chg = RuntimeState.NOT_TESTED.value
                val_chg = None
                err_chg = None
                ev_chg = None
        else:
            chg = props.get("battery_charge_counter") if "battery_charge_counter" in props else props.get("charge_counter_uah")
            sentinel_chg = props.get("charge_counter_is_sentinel", False)
            if sentinel_chg or chg is None:
                state_chg = RuntimeState.UNAVAILABLE.value
                val_chg = None
                err_chg = None
                ev_chg = None
            else:
                state_chg = RuntimeState.AVAILABLE.value
                val_chg = int(chg)
                err_chg = None
                ev_chg = "evidence/battery_dumpsys_evidence.txt#battery_charge_counter" if is_real else None

        ver_chg = is_real and state_chg == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="battery_charge_counter",
            state=state_chg,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_chg), verified=ver_chg),
            value=val_chg,
            unit="uAh",
            source="BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER",
            verified=ver_chg,
            verification_method="battery_property_check",
            observed_at=now if ver_chg else None,
            evidence_ref=ev_chg,
            error_message=err_chg,
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
    P-03: Uses canonical available_memory_mb key.
    P-07: Probe failures set state=ERROR.
    """

    def collect(self, memory_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = memory_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []
        probe_err_mem = props.get("probe_error_meminfo")

        # Available RAM (P-03 canonical key)
        if "available_memory_mb" not in props and "avail_mem_mb" not in props:
            if probe_err_mem:
                state_avail = RuntimeState.ERROR.value
                val_avail = None
                err_avail = probe_err_mem
                ev_avail = "evidence/commands.log#probe_error_meminfo"
            else:
                state_avail = RuntimeState.NOT_TESTED.value
                val_avail = None
                err_avail = None
                ev_avail = None
        else:
            avail_mb = props.get("available_memory_mb") if "available_memory_mb" in props else props.get("avail_mem_mb")
            state_avail = RuntimeState.AVAILABLE.value if avail_mb is not None else RuntimeState.UNAVAILABLE.value
            val_avail = avail_mb if state_avail == RuntimeState.AVAILABLE.value else None
            err_avail = None
            ev_avail = "evidence/meminfo_evidence.txt#available_memory_mb" if (is_real and state_avail == RuntimeState.AVAILABLE.value) else None

        ver_avail = is_real and state_avail == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="available_memory_mb",
            state=state_avail,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_avail), verified=ver_avail),
            value=val_avail,
            unit="MB",
            source="ActivityManager.MemoryInfo.availMem / /proc/meminfo",
            verified=ver_avail,
            verification_method="memory_info_check",
            observed_at=now if ver_avail else None,
            evidence_ref=ev_avail,
            error_message=err_avail,
        ))

        # Low Memory Flag
        if "low_memory_flag" not in props:
            if probe_err_mem:
                state_low = RuntimeState.ERROR.value
                val_low = None
                err_low = probe_err_mem
                ev_low = "evidence/commands.log#probe_error_meminfo"
            else:
                state_low = RuntimeState.NOT_TESTED.value
                val_low = None
                err_low = None
                ev_low = None
        else:
            low_flag = props.get("low_memory_flag")
            state_low = RuntimeState.AVAILABLE.value if low_flag is not None else RuntimeState.UNAVAILABLE.value
            val_low = low_flag if state_low == RuntimeState.AVAILABLE.value else None
            err_low = None
            ev_low = "evidence/meminfo_evidence.txt#lowMemory" if (is_real and state_low == RuntimeState.AVAILABLE.value) else None

        ver_low = is_real and state_low == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="low_memory_flag",
            state=state_low,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_low), verified=ver_low),
            value=val_low,
            source="ActivityManager.MemoryInfo.lowMemory",
            verified=ver_low,
            verification_method="memory_info_check",
            observed_at=now if ver_low else None,
            evidence_ref=ev_low,
            error_message=err_low,
        ))

        # App Heap Allocated
        if "app_heap_allocated_mb" not in props:
            state_app = RuntimeState.NOT_TESTED.value
            val_app = None
        else:
            app_heap = props.get("app_heap_allocated_mb")
            state_app = RuntimeState.AVAILABLE.value if app_heap is not None else RuntimeState.UNAVAILABLE.value
            val_app = app_heap if state_app == RuntimeState.AVAILABLE.value else None

        ver_app = is_real and state_app == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="app_heap_allocated_mb",
            state=state_app,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_app), verified=ver_app),
            value=val_app,
            unit="MB",
            source="Runtime.totalMemory() - freeMemory()",
            verified=ver_app,
            verification_method="runtime_heap_check",
            observed_at=now if ver_app else None,
            evidence_ref="evidence/memory_props.json#app_heap" if ver_app else None,
        ))

        # PSI Memory Pressure
        if "psi_memory_readable" not in props:
            state_psi = RuntimeState.NOT_TESTED.value
            val_psi = None
        else:
            psi = props.get("psi_memory_readable")
            if psi is True:
                state_psi = RuntimeState.AVAILABLE.value
                val_psi = "PSI readable"
            elif psi is False:
                state_psi = RuntimeState.PERMISSION_REQUIRED.value
                val_psi = None
            else:
                state_psi = RuntimeState.UNAVAILABLE.value
                val_psi = None

        ver_psi = is_real and state_psi == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="psi_memory_pressure",
            state=state_psi,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_psi), verified=ver_psi),
            value=val_psi,
            source="/proc/pressure/memory",
            verified=ver_psi,
            verification_method="file_read_check",
            observed_at=now if ver_psi else None,
            evidence_ref="evidence/memory_props.json#psi" if ver_psi else None,
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
    P-03: Uses canonical cpu_scaling_cur_freq key.
    P-07: Probe failures set state=ERROR.
    """

    def collect(self, cpu_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = cpu_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []

        # CPU Core Count
        probe_err_cpu = props.get("probe_error_cpuinfo")
        if "core_count" not in props:
            if probe_err_cpu:
                state_cores = RuntimeState.ERROR.value
                val_cores = None
                err_cores = probe_err_cpu
                ev_cores = "evidence/commands.log#probe_error_cpuinfo"
            else:
                state_cores = RuntimeState.NOT_TESTED.value
                val_cores = None
                err_cores = None
                ev_cores = None
        else:
            cores = props.get("core_count")
            state_cores = RuntimeState.AVAILABLE.value if cores is not None else RuntimeState.UNAVAILABLE.value
            val_cores = cores if state_cores == RuntimeState.AVAILABLE.value else None
            err_cores = None
            ev_cores = "evidence/cpuinfo_evidence.txt#processor_count" if (is_real and state_cores == RuntimeState.AVAILABLE.value) else None

        ver_cores = is_real and state_cores == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="cpu_core_count",
            state=state_cores,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_cores), verified=ver_cores),
            value=val_cores,
            unit="cores",
            source="Runtime.availableProcessors() / /sys/devices/system/cpu/possible",
            verified=ver_cores,
            verification_method="cpu_sysfs_check",
            observed_at=now if ver_cores else None,
            evidence_ref=ev_cores,
            error_message=err_cores,
        ))

        # CPU scaling cur freq (P-03 canonical key)
        probe_err_freq = props.get("probe_error_cpufreq")
        if "cpu_scaling_cur_freq" not in props and "cur_freq_khz" not in props:
            if probe_err_freq:
                state_freq = RuntimeState.ERROR.value
                val_freq = None
                err_freq = probe_err_freq
                ev_freq = "evidence/commands.log#probe_error_cpufreq"
            else:
                state_freq = RuntimeState.NOT_TESTED.value
                val_freq = None
                err_freq = None
                ev_freq = None
        else:
            freq = props.get("cpu_scaling_cur_freq") if "cpu_scaling_cur_freq" in props else props.get("cur_freq_khz")
            state_freq = RuntimeState.AVAILABLE.value if freq is not None else RuntimeState.UNAVAILABLE.value
            val_freq = freq if state_freq == RuntimeState.AVAILABLE.value else None
            err_freq = None
            ev_freq = "evidence/cpufreq_evidence.txt#scaling_cur_freq" if (is_real and state_freq == RuntimeState.AVAILABLE.value) else None

        ver_freq = is_real and state_freq == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="cpu_scaling_cur_freq",
            state=state_freq,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_freq), verified=ver_freq),
            value=val_freq,
            unit="kHz",
            source="/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq",
            verified=ver_freq,
            verification_method="cpufreq_sysfs_check",
            observed_at=now if ver_freq else None,
            evidence_ref=ev_freq,
            error_message=err_freq,
        ))

        # App CPU time
        if "app_cpu_time_ms" not in props:
            state_app_cpu = RuntimeState.NOT_TESTED.value
            val_app_cpu = None
        else:
            app_cpu = props.get("app_cpu_time_ms")
            state_app_cpu = RuntimeState.AVAILABLE.value if app_cpu is not None else RuntimeState.UNAVAILABLE.value
            val_app_cpu = app_cpu if state_app_cpu == RuntimeState.AVAILABLE.value else None

        ver_app_cpu = is_real and state_app_cpu == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="app_cpu_time",
            state=state_app_cpu,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_app_cpu), verified=ver_app_cpu),
            value=val_app_cpu,
            unit="ms",
            source="Process.getElapsedCpuTime() / /proc/self/stat",
            verified=ver_app_cpu,
            verification_method="process_stat_check",
            observed_at=now if ver_app_cpu else None,
            evidence_ref="evidence/cpu_props.json#app_cpu_time" if ver_app_cpu else None,
        ))

        # Device-wide CPU utilization via ADB /proc/stat
        probe_err_stat = props.get("probe_error_proc_stat")
        if "proc_stat_readable_via_adb" not in props:
            if probe_err_stat:
                state_proc = RuntimeState.ERROR.value
                val_proc = None
                cond_proc = None
                ver_proc = False
                err_proc = probe_err_stat
                ev_proc = "evidence/commands.log#probe_error_proc_stat"
            else:
                state_proc = RuntimeState.NOT_TESTED.value
                val_proc = None
                cond_proc = None
                ver_proc = False
                err_proc = None
                ev_proc = None
        else:
            proc_adb = props.get("proc_stat_readable_via_adb")
            if proc_adb is True:
                state_proc = RuntimeState.AVAILABLE.value
                val_proc = "Readable via host ADB"
                cond_proc = "HOST ADB SHELL"
                ver_proc = is_real
                err_proc = None
                ev_proc = "evidence/proc_stat_evidence.txt" if is_real else None
            else:
                state_proc = RuntimeState.PERMISSION_REQUIRED.value
                val_proc = None
                cond_proc = "HOST ADB SHELL"
                ver_proc = False
                err_proc = None
                ev_proc = None

        results.append(CapabilityResult(
            metric="device_wide_cpu_utilization",
            state=state_proc,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_proc), verified=ver_proc, condition=cond_proc),
            value=val_proc,
            source="/proc/stat via ADB shell",
            condition=cond_proc,
            verified=ver_proc,
            verification_method="adb_shell_proc_stat_check",
            observed_at=now if ver_proc else None,
            evidence_ref=ev_proc,
            error_message=err_proc,
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
    P-03: Uses canonical gpu_clock_hz key.
    P-07: Probe failures set state=ERROR.
    """

    def collect(self, gpu_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        props = gpu_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []
        probe_err_gpu = props.get("probe_error_gpu")

        if "renderer" not in props and "gles_renderer" not in props:
            state_rend = RuntimeState.NOT_TESTED.value
            val_rend = None
        else:
            renderer = props.get("renderer") or props.get("gles_renderer")
            state_rend = RuntimeState.AVAILABLE.value if renderer else RuntimeState.UNAVAILABLE.value
            val_rend = renderer if state_rend == RuntimeState.AVAILABLE.value else None

        ver_rend = is_real and state_rend == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_vendor_renderer",
            state=state_rend,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_rend), verified=ver_rend),
            value=val_rend,
            source="GLES20.glGetString(GL_RENDERER)",
            verified=ver_rend,
            verification_method="gles_string_check",
            observed_at=now if ver_rend else None,
            evidence_ref="evidence/android_app_evidence.json#gpu_renderer" if ver_rend else None,
        ))

        # GPU clock frequency (P-03 canonical key)
        if "gpu_clock_hz" not in props and "gpu_freq_hz" not in props:
            if probe_err_gpu:
                state_freq = RuntimeState.ERROR.value
                val_freq = None
                err_freq = probe_err_gpu
                ev_freq = "evidence/commands.log#probe_error_gpu"
            else:
                state_freq = RuntimeState.NOT_TESTED.value
                val_freq = None
                err_freq = None
                ev_freq = None
        else:
            gpu_freq = props.get("gpu_clock_hz") if "gpu_clock_hz" in props else props.get("gpu_freq_hz")
            state_freq = RuntimeState.AVAILABLE.value if gpu_freq is not None else RuntimeState.UNAVAILABLE.value
            val_freq = gpu_freq if state_freq == RuntimeState.AVAILABLE.value else None
            err_freq = None
            ev_freq = "evidence/gpu_evidence.txt#gpuclk" if (is_real and state_freq == RuntimeState.AVAILABLE.value) else None

        ver_freq = is_real and state_freq == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_clock_hz",
            state=state_freq,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_freq), verified=ver_freq),
            value=val_freq,
            unit="Hz",
            source="/sys/class/kgsl/kgsl-3d0/gpuclk",
            verified=ver_freq,
            verification_method="kgsl_sysfs_check",
            observed_at=now if ver_freq else None,
            evidence_ref=ev_freq,
            error_message=err_freq,
        ))

        if "gpu_utilization_percent" not in props:
            state_util = RuntimeState.NOT_TESTED.value
            val_util = None
        else:
            gpu_util = props.get("gpu_utilization_percent")
            state_util = RuntimeState.AVAILABLE.value if gpu_util is not None else RuntimeState.UNAVAILABLE.value
            val_util = gpu_util if state_util == RuntimeState.AVAILABLE.value else None

        ver_util = is_real and state_util == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="gpu_utilization",
            state=state_util,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_util), verified=ver_util),
            value=val_util,
            unit="percent",
            source="/sys/class/kgsl/kgsl-3d0/gpubusy",
            verified=ver_util,
            verification_method="kgsl_busy_check",
            observed_at=now if ver_util else None,
            evidence_ref="evidence/kgsl_evidence.txt#gpubusy" if ver_util else None,
            notes="UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE unless root/custom driver permissions exist.",
        ))

        return TelemetryCapability(
            dimension="gpu",
            results=results,
            resource_state_input=False,
            reliability="NOT YET VERIFIED",
        )


class ThermalTelemetryCollector:
    """Collector 7: ThermalTelemetryCollector.
    Checks thermal status API (API>=29), thermal headroom API (API>=30), thermal zones,
    frequency capping, and selects D-10 thermal source based on evidence.
    F-04: API level is NEVER assumed (api_level=None -> NOT_TESTED).
    """

    def collect(self, thermal_props: Optional[Dict[str, Any]] = None) -> ThermalCapability:
        props = thermal_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))

        api_level = props.get("api_level")

        # Thermal status API (API >= 29)
        if api_level is None:
            status_api_state = RuntimeState.NOT_TESTED.value
            status_api_val = None
        elif api_level < 29:
            status_api_state = RuntimeState.API_UNSUPPORTED.value
            status_api_val = None
        else:
            status_api_avail = props.get("thermal_status_api_available")
            if status_api_avail is True:
                status_api_state = RuntimeState.AVAILABLE.value
                status_api_val = "PowerManager.getCurrentThermalStatus() functional"
            elif status_api_avail is False:
                status_api_state = RuntimeState.UNAVAILABLE.value
                status_api_val = None
            else:
                status_api_state = RuntimeState.NOT_TESTED.value
                status_api_val = None

        ver_status_api = is_real and status_api_state == RuntimeState.AVAILABLE.value
        res_status_api = CapabilityResult(
            metric="thermal_status_api",
            state=status_api_state,
            report_status=map_runtime_state_to_report_status(RuntimeState(status_api_state), verified=ver_status_api),
            value=status_api_val,
            source="PowerManager.getCurrentThermalStatus()",
            min_api=29,
            verified=ver_status_api,
            verification_method="power_manager_thermal_status_check",
            observed_at=now if ver_status_api else None,
            evidence_ref="evidence/thermal_evidence.json#status_api" if ver_status_api else None,
        )

        # Thermal headroom API (API >= 30)
        if api_level is None:
            headroom_state = RuntimeState.NOT_TESTED.value
            headroom_val = None
        elif api_level < 30:
            headroom_state = RuntimeState.API_UNSUPPORTED.value
            headroom_val = None
        else:
            headroom_api_avail = props.get("thermal_headroom_api_available")
            if headroom_api_avail is True:
                headroom_state = RuntimeState.AVAILABLE.value
                headroom_val = "PowerManager.getThermalHeadroom() functional"
            elif headroom_api_avail is False:
                headroom_state = RuntimeState.UNAVAILABLE.value
                headroom_val = None
            else:
                headroom_state = RuntimeState.NOT_TESTED.value
                headroom_val = None

        ver_headroom = is_real and headroom_state == RuntimeState.AVAILABLE.value
        res_headroom_api = CapabilityResult(
            metric="thermal_headroom_api",
            state=headroom_state,
            report_status=map_runtime_state_to_report_status(RuntimeState(headroom_state), verified=ver_headroom),
            value=headroom_val,
            source="PowerManager.getThermalHeadroom()",
            min_api=30,
            verified=ver_headroom,
            verification_method="power_manager_thermal_headroom_check",
            observed_at=now if ver_headroom else None,
            evidence_ref="evidence/thermal_evidence.json#headroom_api" if ver_headroom else None,
        )

        # Temperature sources
        temp_sources: List[CapabilityResult] = []

        # Battery temperature source
        if "battery_temp_available" not in props:
            state_batt_t = RuntimeState.NOT_TESTED.value
            val_batt_t = None
        else:
            batt_t = props.get("battery_temp_available")
            state_batt_t = RuntimeState.AVAILABLE.value if batt_t is True else RuntimeState.UNAVAILABLE.value
            val_batt_t = "BatteryManager EXTRA_TEMPERATURE" if state_batt_t == RuntimeState.AVAILABLE.value else None

        ver_batt_t = is_real and state_batt_t == RuntimeState.AVAILABLE.value
        temp_sources.append(CapabilityResult(
            metric="temperature_battery",
            state=state_batt_t,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_batt_t), verified=ver_batt_t),
            value=val_batt_t,
            unit="degC",
            source="BatteryManager broadcast",
            verified=ver_batt_t,
            verification_method="battery_temperature_check",
            observed_at=now if ver_batt_t else None,
            evidence_ref="evidence/battery_evidence.json#temperature" if ver_batt_t else None,
        ))

        # Thermal zones sysfs
        probe_err_th = props.get("probe_error_thermal")
        if "thermal_zones_readable_count" not in props:
            if probe_err_th:
                state_zones = RuntimeState.ERROR.value
                val_zones = None
                err_zones = probe_err_th
                ev_zones = "evidence/commands.log#probe_error_thermal"
            else:
                state_zones = RuntimeState.NOT_TESTED.value
                val_zones = None
                err_zones = None
                ev_zones = None
        else:
            z_count = props.get("thermal_zones_readable_count", 0)
            state_zones = RuntimeState.AVAILABLE.value if z_count > 0 else RuntimeState.UNAVAILABLE.value
            val_zones = f"{z_count} thermal zones readable" if state_zones == RuntimeState.AVAILABLE.value else None
            err_zones = None
            ev_zones = "evidence/thermal_evidence.txt#thermal_zones" if (is_real and state_zones == RuntimeState.AVAILABLE.value) else None

        ver_zones = is_real and state_zones == RuntimeState.AVAILABLE.value
        temp_sources.append(CapabilityResult(
            metric="thermal_zones_sysfs",
            state=state_zones,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_zones), verified=ver_zones),
            value=val_zones,
            unit="zones",
            source="/sys/class/thermal/thermal_zone*",
            verified=ver_zones,
            verification_method="thermal_zone_sysfs_read_check",
            observed_at=now if ver_zones else None,
            evidence_ref=ev_zones,
            error_message=err_zones,
        ))

        # Frequency capping observable
        if "frequency_capping_observable" not in props:
            state_cap = RuntimeState.NOT_TESTED.value
            val_cap = None
        else:
            fc = props.get("frequency_capping_observable")
            state_cap = RuntimeState.AVAILABLE.value if fc is True else RuntimeState.UNAVAILABLE.value
            val_cap = "Observed scaling_max_freq drops" if state_cap == RuntimeState.AVAILABLE.value else None

        ver_cap = is_real and state_cap == RuntimeState.AVAILABLE.value
        res_freq_cap = CapabilityResult(
            metric="frequency_capping_observable",
            state=state_cap,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_cap), verified=ver_cap),
            value=val_cap,
            source="cpufreq scaling_max_freq vs scaling_boost_freq / cpuinfo_max_freq",
            verified=ver_cap,
            verification_method="cpufreq_capping_check",
            observed_at=now if ver_cap else None,
            evidence_ref="evidence/cpufreq_evidence.txt#capping" if ver_cap else None,
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

        # D-10 Thermal source selection from evidence
        if status_api_state == RuntimeState.AVAILABLE.value:
            selected_source = "platform_thermal_status"
        elif status_api_state in (RuntimeState.API_UNSUPPORTED.value, RuntimeState.UNAVAILABLE.value) and (
            state_batt_t == RuntimeState.AVAILABLE.value or state_zones == RuntimeState.AVAILABLE.value
        ):
            selected_source = "fallback_temperature_and_frequency_capping"
        else:
            selected_source = None

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
        is_real = bool(props.get("is_real_device_observation", False))

        camera_ids = props.get("camera_ids", ["0"])
        results_list: List[CameraCapability] = []

        for cid in camera_ids:
            cam_info = props.get(f"camera_{cid}", {})
            res_cam: List[CapabilityResult] = []
            probe_err_cam = props.get("probe_error_camera")

            # Hardware level
            if "hardware_level" not in cam_info:
                if probe_err_cam:
                    state_hw = RuntimeState.ERROR.value
                    val_hw = None
                    err_hw = probe_err_cam
                    ev_hw = "evidence/commands.log#probe_error_camera"
                else:
                    state_hw = RuntimeState.NOT_TESTED.value
                    val_hw = None
                    err_hw = None
                    ev_hw = None
            else:
                hw_level = cam_info.get("hardware_level")
                state_hw = RuntimeState.AVAILABLE.value if hw_level else RuntimeState.UNAVAILABLE.value
                val_hw = hw_level if state_hw == RuntimeState.AVAILABLE.value else None
                err_hw = None
                ev_hw = f"evidence/camera_{cid}_evidence.json#hardware_level" if (is_real and state_hw == RuntimeState.AVAILABLE.value) else None

            ver_hw = is_real and state_hw == RuntimeState.AVAILABLE.value
            res_cam.append(CapabilityResult(
                metric="hardware_level",
                state=state_hw,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_hw), verified=ver_hw),
                value=val_hw,
                source=f"CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL (ID {cid})",
                verified=ver_hw,
                verification_method="camera_characteristics_check",
                observed_at=now if ver_hw else None,
                evidence_ref=ev_hw,
                error_message=err_hw,
            ))

            # Manual exposure control advertised
            if "manual_exposure_advertised" not in cam_info:
                state_exp = RuntimeState.NOT_TESTED.value
                val_exp = None
            else:
                man_exp = cam_info.get("manual_exposure_advertised")
                state_exp = RuntimeState.AVAILABLE.value if man_exp is True else RuntimeState.UNAVAILABLE.value
                val_exp = "MANUAL_SENSOR capability advertised" if state_exp == RuntimeState.AVAILABLE.value else None

            ver_exp = is_real and state_exp == RuntimeState.AVAILABLE.value
            res_cam.append(CapabilityResult(
                metric="manual_exposure_advertised",
                state=state_exp,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_exp), verified=ver_exp),
                value=val_exp,
                source=f"CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES (ID {cid})",
                verified=ver_exp,
                verification_method="camera_capabilities_check",
                observed_at=now if ver_exp else None,
                evidence_ref=f"evidence/camera_{cid}_evidence.json#manual_exposure" if ver_exp else None,
            ))

            # Advertised vs Honoured check for manual control
            if "manual_control_honoured" not in cam_info:
                state_hon = RuntimeState.NOT_TESTED.value
                val_hon = None
            else:
                honoured = cam_info.get("manual_control_honoured")
                if honoured is True:
                    state_hon = RuntimeState.AVAILABLE.value
                    val_hon = "CaptureResult confirms set exposure/ISO honoured"
                elif honoured is False:
                    state_hon = RuntimeState.UNAVAILABLE.value
                    val_hon = None
                else:
                    state_hon = RuntimeState.NOT_TESTED.value
                    val_hon = None

            ver_hon = is_real and state_hon == RuntimeState.AVAILABLE.value
            res_honoured = CapabilityResult(
                metric="manual_control_honoured",
                state=state_hon,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_hon), verified=ver_hon),
                value=val_hon,
                source=f"CaptureResult metadata verification (ID {cid})",
                verified=ver_hon,
                verification_method="capture_result_honoured_check",
                observed_at=now if ver_hon else None,
                evidence_ref=f"evidence/camera_{cid}_evidence.json#manual_control_honoured" if ver_hon else None,
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
        is_real = bool(props.get("is_real_device_observation", False))

        backends = ["TFLite_CPU", "TFLite_GPU", "TFLite_NNAPI", "ONNXRuntime_CPU", "ONNXRuntime_NNAPI"]
        out: List[BackendCapability] = []

        for b_name in backends:
            b_info = props.get(b_name, {})

            if "available" not in b_info:
                state_avail = RuntimeState.NOT_TESTED.value
                val_avail = None
            else:
                avail = b_info.get("available")
                state_avail = RuntimeState.AVAILABLE.value if avail is True else RuntimeState.UNAVAILABLE.value
                val_avail = f"{b_name} runtime available" if state_avail == RuntimeState.AVAILABLE.value else None

            ver_avail = is_real and state_avail == RuntimeState.AVAILABLE.value
            res_avail = CapabilityResult(
                metric="backend_availability",
                state=state_avail,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_avail), verified=ver_avail),
                value=val_avail,
                source=f"Runtime library initialization ({b_name})",
                verified=ver_avail,
                verification_method="backend_init_check",
                observed_at=now if ver_avail else None,
                evidence_ref=f"evidence/backend_{b_name}_evidence.json#availability" if ver_avail else None,
            )

            if "delegation_working" not in b_info:
                state_deleg = RuntimeState.NOT_TESTED.value
                val_deleg = None
            else:
                deleg = b_info.get("delegation_working")
                state_deleg = RuntimeState.AVAILABLE.value if deleg is True else RuntimeState.UNAVAILABLE.value
                val_deleg = f"{b_name} delegate loaded" if state_deleg == RuntimeState.AVAILABLE.value else None

            ver_deleg = is_real and state_deleg == RuntimeState.AVAILABLE.value
            res_deleg = CapabilityResult(
                metric="backend_delegation",
                state=state_deleg,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_deleg), verified=ver_deleg),
                value=val_deleg,
                source=f"Delegate / EP load check ({b_name})",
                verified=ver_deleg,
                verification_method="delegate_load_check",
                observed_at=now if ver_deleg else None,
                evidence_ref=f"evidence/backend_{b_name}_evidence.json#delegation" if ver_deleg else None,
            )

            if "probability_output_valid" not in b_info:
                state_prob = RuntimeState.NOT_TESTED.value
                val_prob = None
            else:
                prob = b_info.get("probability_output_valid")
                state_prob = RuntimeState.AVAILABLE.value if prob is True else RuntimeState.UNAVAILABLE.value
                val_prob = "Finite float output, correct shape, softmax sum ~= 1.0" if state_prob == RuntimeState.AVAILABLE.value else None

            ver_prob = is_real and state_prob == RuntimeState.AVAILABLE.value
            res_prob = CapabilityResult(
                metric="probability_output_validity",
                state=state_prob,
                report_status=map_runtime_state_to_report_status(RuntimeState(state_prob), verified=ver_prob),
                value=val_prob,
                source=f"Reference graph output validation ({b_name})",
                verified=ver_prob,
                verification_method="reference_graph_output_check",
                observed_at=now if ver_prob else None,
                evidence_ref=f"evidence/backend_{b_name}_evidence.json#probability_output" if ver_prob else None,
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
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []

        if "system_nano_time_available" not in props:
            state_nano = RuntimeState.NOT_TESTED.value
            val_nano = None
        else:
            nano = props.get("system_nano_time_available")
            state_nano = RuntimeState.AVAILABLE.value if nano is True else RuntimeState.UNAVAILABLE.value
            val_nano = "System.nanoTime() / SystemClock.elapsedRealtimeNanos() functional" if state_nano == RuntimeState.AVAILABLE.value else None

        ver_nano = is_real and state_nano == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="system_nano_time",
            state=state_nano,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_nano), verified=ver_nano),
            value=val_nano,
            unit="ns",
            source="System.nanoTime() / SystemClock.elapsedRealtimeNanos()",
            verified=ver_nano,
            verification_method="clock_source_check",
            observed_at=now if ver_nano else None,
            evidence_ref="evidence/profiling_evidence.json#nano_time" if ver_nano else None,
        ))

        if "android_trace_api_available" not in props:
            state_trace = RuntimeState.NOT_TESTED.value
            val_trace = None
        else:
            tr = props.get("android_trace_api_available")
            state_trace = RuntimeState.AVAILABLE.value if tr is True else RuntimeState.UNAVAILABLE.value
            val_trace = "android.os.Trace beginSection/endSection functional" if state_trace == RuntimeState.AVAILABLE.value else None

        ver_trace = is_real and state_trace == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="android_trace_api",
            state=state_trace,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_trace), verified=ver_trace),
            value=val_trace,
            source="android.os.Trace",
            verified=ver_trace,
            verification_method="trace_api_check",
            observed_at=now if ver_trace else None,
            evidence_ref="evidence/profiling_evidence.json#trace_api" if ver_trace else None,
        ))

        if "atrace_adb_available" not in props:
            state_atrace = RuntimeState.NOT_TESTED.value
            val_atrace = None
            cond_atrace = None
            ver_atrace = False
        else:
            atrace = props.get("atrace_adb_available")
            if atrace is True:
                state_atrace = RuntimeState.AVAILABLE.value
                val_atrace = "atrace / systrace / perfetto via ADB available"
                cond_atrace = "HOST ADB SHELL"
                ver_atrace = is_real
            else:
                state_atrace = RuntimeState.UNAVAILABLE.value
                val_atrace = None
                cond_atrace = None
                ver_atrace = False

        results.append(CapabilityResult(
            metric="adb_atrace_profiling",
            state=state_atrace,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_atrace), verified=ver_atrace, condition=cond_atrace),
            value=val_atrace,
            source="ADB shell atrace / perfetto",
            condition=cond_atrace,
            verified=ver_atrace,
            verification_method="adb_atrace_check",
            observed_at=now if ver_atrace else None,
            evidence_ref="evidence/atrace_evidence.txt" if ver_atrace else None,
        ))

        return results


class EnergyMeasurementCapabilityChecker:
    """Collector 11: EnergyMeasurementCapabilityChecker.
    Evaluates E-1 (battery-side external), E-2 (supply-powered session), E-3 (software relative counters).
    F-12: Unassessed feasibility stays NOT_TESTED. selected_level requires evidence.
    """

    def collect(self, energy_props: Optional[Dict[str, Any]] = None) -> EnergyCapability:
        props = energy_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))

        # E-1 Battery-side reference
        if "E1_feasible" not in props:
            state_e1 = RuntimeState.NOT_TESTED.value
            rep_e1 = ReportStatus.NOT_YET_VERIFIED.value
            notes_e1 = "Physical battery terminal access feasibility not yet assessed."
        else:
            e1 = props.get("E1_feasible")
            state_e1 = RuntimeState.EXTERNAL_REQUIRED.value
            rep_e1 = ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION.value
            notes_e1 = "Requires physical battery terminal access and safety sign-off." if e1 else "Infeasible battery-side access."

        res_e1 = CapabilityResult(
            metric="E1_battery_side_reference",
            state=state_e1,
            report_status=rep_e1,
            value=None,
            source="External power meter (e.g. Monsoon / Yokogawa / Keysight)",
            verified=False,
            verification_method="external_hardware_feasibility_check",
            notes=notes_e1,
        )

        # E-2 Supply-powered session
        if "E2_feasible" not in props:
            state_e2 = RuntimeState.NOT_TESTED.value
            rep_e2 = ReportStatus.NOT_YET_VERIFIED.value
            notes_e2 = "Supply-powered session feasibility not yet assessed."
        else:
            e2 = props.get("E2_feasible")
            state_e2 = RuntimeState.EXTERNAL_REQUIRED.value
            rep_e2 = ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION.value
            notes_e2 = "USB battery charging current must be accounted for or isolated." if e2 else "Infeasible USB supply-powered session."

        res_e2 = CapabilityResult(
            metric="E2_supply_powered_session",
            state=state_e2,
            report_status=rep_e2,
            value=None,
            source="External USB power meter / inline power monitor",
            verified=False,
            verification_method="external_usb_meter_check",
            notes=notes_e2,
        )

        # E-3 Software relative counters
        if "E3_counters_available" not in props:
            state_e3 = RuntimeState.NOT_TESTED.value
            val_e3 = None
        else:
            e3 = props.get("E3_counters_available")
            state_e3 = RuntimeState.AVAILABLE.value if e3 is True else RuntimeState.UNAVAILABLE.value
            val_e3 = "BatteryManager software current/charge counters readable" if state_e3 == RuntimeState.AVAILABLE.value else None

        ver_e3 = is_real and state_e3 == RuntimeState.AVAILABLE.value
        res_e3 = CapabilityResult(
            metric="E3_software_counters",
            state=state_e3,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_e3), verified=ver_e3),
            value=val_e3,
            source="BatteryManager BATTERY_PROPERTY_CURRENT_NOW / CHARGE_COUNTER",
            verified=ver_e3,
            verification_method="software_counter_check",
            observed_at=now if ver_e3 else None,
            evidence_ref="evidence/battery_dumpsys_evidence.txt#E3_counters" if ver_e3 else None,
            notes="Relative software comparison only; NO absolute energy claimed.",
        )

        # Level selection based on explicit evidence
        selected_level = None
        if props.get("E1_feasible") is True:
            selected_level = "E-1"
        elif props.get("E2_feasible") is True:
            selected_level = "E-2"
        elif props.get("E3_counters_available") is True:
            selected_level = "E-3"

        return EnergyCapability(
            E1_battery_side_reference=res_e1,
            E2_supply_powered_session=res_e2,
            E3_software_counters=res_e3,
            selected_level=selected_level,
            absolute_energy_claimed=False,  # FIXED FALSE
        )
