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

from src.monitoring.characterization.energy_evidence import (
    select_energy_level,
    selection_basis,
    unmet_selection_requirements,
)
from src.monitoring.characterization.ram_variant import (
    AMBIGUOUS as RAM_AMBIGUOUS,
    INVALID as RAM_INVALID,
    MATCH as RAM_MATCH,
    classify_ram_variant,
    load_ram_variant_spec,
    validate_ram_variant_spec,
)
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


def _is_app_derived(props: Dict[str, Any], metric: str) -> bool:
    """True only when the final value of `metric` was supplied by the Android app (P5-01)."""
    return props.get(f"{metric}_is_app_derived") is True


def _app_metric_state(props: Dict[str, Any], metric: str) -> Optional[Dict[str, Any]]:
    """Non-AVAILABLE state reported by the Android app for `metric`, if any (P5-02 / P5-03)."""
    states = props.get("app_metric_states")
    if isinstance(states, dict) and isinstance(states.get(metric), dict):
        return states[metric]
    return None


APP_EVIDENCE = "evidence/android_app_evidence.json"
HOST_ADB = "HOST ADB SHELL"
GETPROP_SDK_EVIDENCE = "evidence/getprop_evidence.txt#ro.build.version.sdk"
COMMANDS_LOG = "evidence/commands.log"
VALID_STATES = {s.value for s in RuntimeState}

# Probe outcome (host_probes) -> runtime state. Absent path is UNAVAILABLE, a refused read PERMISSION_REQUIRED.
_OUTCOME_STATE = {
    "READABLE": RuntimeState.AVAILABLE.value,
    "ABSENT": RuntimeState.UNAVAILABLE.value,
    "PERMISSION_DENIED": RuntimeState.PERMISSION_REQUIRED.value,
    "ERROR": RuntimeState.ERROR.value,
}


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _make(
    metric: str,
    state: str,
    *,
    is_real: bool,
    source: str,
    verification_method: str,
    value: Any = None,
    unit: Optional[str] = None,
    evidence_ref: Optional[str] = None,
    condition: Optional[str] = None,
    pilot: bool = False,
    verifiable: bool = True,
    min_api: Optional[int] = None,
    error_message: Optional[str] = None,
    notes: Optional[str] = None,
) -> CapabilityResult:
    """Builds one record with the protocol §3 mapping applied consistently.

    - verified only for a real, unconditional, non-pilot AVAILABLE observation with evidence (and `verifiable`);
    - a condition (host ADB, ...) gives CONDITIONALLY AVAILABLE, never VERIFIED;
    - `pilot` (interface demonstrated, semantics pending E0) gives REQUIRES PILOT VALIDATION, only for AVAILABLE;
    - evidence and timestamps are only attached to real-device observations;
    - a non-AVAILABLE state always carries value None (no fake zeros).
    """
    available = state == RuntimeState.AVAILABLE.value
    ev = evidence_ref if is_real else None
    cond = condition if state in (RuntimeState.AVAILABLE.value, RuntimeState.PERMISSION_REQUIRED.value) else None
    verified = bool(is_real and available and not cond and not pilot and verifiable and ev)
    report = map_runtime_state_to_report_status(
        RuntimeState(state), verified=verified, condition=cond, pilot_validation=bool(pilot and available)
    )
    return CapabilityResult(
        metric=metric,
        state=state,
        report_status=report.value,
        value=value if available else None,
        unit=unit,
        source=source,
        min_api=min_api,
        condition=cond,
        verified=verified,
        verification_method=verification_method,
        evidence_ref=ev,
        observed_at=_now() if (is_real and state != RuntimeState.NOT_TESTED.value) else None,
        error_message=error_message,
        notes=notes,
    )


def _app_collected(props: Dict[str, Any]) -> bool:
    return props.get("app_output_status") == "APP_OUTPUT_COLLECTED"


def _app_rec(props: Dict[str, Any], metric: str) -> Optional[Dict[str, Any]]:
    recs = props.get("app_records")
    return recs.get(metric) if isinstance(recs, dict) else None


def _join_notes(*parts: Optional[str]) -> Optional[str]:
    text = " ".join(p for p in parts if p)
    return text or None


_UNSET = object()


def _app_result(
    props: Dict[str, Any],
    metric: str,
    *,
    source: str,
    verification_method: str,
    record: Any = _UNSET,
    anchor: Optional[str] = None,
    unit: Optional[str] = None,
    min_api: Optional[int] = None,
    condition: Optional[str] = None,
    pilot: bool = False,
    verifiable: bool = True,
    notes: Optional[str] = None,
    record_name: Optional[str] = None,
) -> CapabilityResult:
    """Record for a metric whose only source is the Android app report (A2/Phase B probes).

    The app's own state is preserved (P5-02/P5-03 rule). The evidence always cites the app file, never a host file.
    - app output not retrieved (APP_OUTPUT_MISSING / not connected) -> NOT_TESTED;
    - app output retrieval failed (APP_OUTPUT_ERROR) -> ERROR (an attempted probe that failed);
    - app report without this record (older app build) -> NOT_TESTED, explained in notes;
    - AVAILABLE without a value, or an unknown state -> ERROR (inconsistent app output).
    """
    is_real = bool(props.get("is_real_device_observation", False))
    name = record_name or metric
    ref = f"{APP_EVIDENCE}#{anchor or metric}"
    common = dict(is_real=is_real, source=source, verification_method=verification_method, unit=unit, min_api=min_api)
    status = props.get("app_output_status")
    if status == "APP_OUTPUT_ERROR":
        return _make(name, RuntimeState.ERROR.value, evidence_ref=f"{COMMANDS_LOG}#app_output", **common,
                     error_message="Android app output could not be retrieved or parsed (APP_OUTPUT_ERROR).")
    if not _app_collected(props):
        return _make(name, RuntimeState.NOT_TESTED.value, **common,
                     notes=f"Android app output not collected ({status or 'no connected app run'}); probe not executed.")
    rec = _app_rec(props, metric) if record is _UNSET else record
    if rec is None:
        return _make(name, RuntimeState.NOT_TESTED.value, **common,
                     notes=f"The Android app report contains no '{metric}' record (app build without this probe).")
    state = rec.get("state")
    app_notes = rec.get("notes")
    if state not in VALID_STATES:
        return _make(name, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                     error_message=f"Android app reported an unrecognised state {state!r} for '{metric}'.")
    if state == RuntimeState.AVAILABLE.value:
        if rec.get("value") is None:
            return _make(name, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                         error_message=f"Android app reported '{metric}' AVAILABLE without a value (inconsistent output).")
        return _make(name, state, value=rec.get("value"), evidence_ref=ref, condition=condition, pilot=pilot,
                     verifiable=verifiable, notes=_join_notes(notes, app_notes), **common)
    return _make(name, state, evidence_ref=ref, error_message=rec.get("error_message"),
                 notes=_join_notes(app_notes, notes), **common)


def _host_outcome_result(
    metric: str,
    probe: Optional[Dict[str, Any]],
    *,
    is_real: bool,
    source: str,
    verification_method: str,
    evidence_file: str,
    value: Any = None,
    unit: Optional[str] = None,
    pilot_note: Optional[str] = None,
) -> CapabilityResult:
    """Record from one host file probe outcome (READABLE / ABSENT / PERMISSION_DENIED / ERROR).

    READABLE through host adb is CONDITIONALLY AVAILABLE (condition HOST ADB SHELL), never VERIFIED.
    A refused read under host adb has no known unlocking condition, so it stays PERMISSION_REQUIRED (report UNAVAILABLE).
    """
    if not probe or probe.get("outcome") not in _OUTCOME_STATE:
        return _make(metric, RuntimeState.NOT_TESTED.value, is_real=is_real, source=source,
                     verification_method=verification_method, unit=unit, notes="Host probe not executed.")
    outcome = probe["outcome"]
    state = _OUTCOME_STATE[outcome]
    notes = {
        "READABLE": pilot_note,
        "ABSENT": f"{probe.get('target')} does not exist on this device.",
        "PERMISSION_DENIED": f"Reading {probe.get('target')} was refused even through host adb.",
        "ERROR": None,
    }[outcome]
    return _make(
        metric, state, is_real=is_real, source=source, verification_method=verification_method,
        value=value if state == RuntimeState.AVAILABLE.value else None, unit=unit,
        evidence_ref=f"evidence/{evidence_file}", condition=HOST_ADB if state == RuntimeState.AVAILABLE.value else None,
        error_message=f"Unexpected probe result for {probe.get('target')}" if outcome == "ERROR" else None,
        notes=notes,
    )


def _resolve_gpu_renderer(props: Dict[str, Any]) -> Dict[str, Any]:
    """Single authoritative GPU renderer observation (A8), shared by gpu_renderer and gpu_vendor_renderer.

    Priority: the app's EGL GL_RENDERER/GL_VENDOR (protocol interface); otherwise host SurfaceFlinger GLES line
    (host ADB condition). Returns the fields needed to build either record.
    """
    is_real = bool(props.get("is_real_device_observation", False))
    app = _app_rec(props, "gpu_renderer") if _app_collected(props) else None
    if app and app.get("state") == RuntimeState.AVAILABLE.value and isinstance(app.get("value"), dict) \
            and app["value"].get("renderer"):
        v = app["value"]
        return dict(state=RuntimeState.AVAILABLE.value, renderer=v.get("renderer"), vendor=v.get("vendor"),
                    version=v.get("version"), source="EGL14/GLES20 glGetString(GL_RENDERER, GL_VENDOR) (android app)",
                    evidence_ref=f"{APP_EVIDENCE}#gpu_renderer", condition=None, error=None, notes=None)
    host = props.get("host_gles")
    if isinstance(host, dict) and host.get("renderer"):
        app_note = (f"App EGL probe state: {app.get('state')}." if app else "App EGL probe result not available.")
        return dict(state=RuntimeState.AVAILABLE.value, renderer=host["renderer"], vendor=host.get("vendor"),
                    version=host.get("version"), source="adb shell dumpsys SurfaceFlinger (GLES line)",
                    evidence_ref="evidence/gpu_renderer_evidence.txt", condition=HOST_ADB, error=None,
                    notes=app_note)
    if app and app.get("state") in VALID_STATES:
        return dict(state=app["state"] if app["state"] != RuntimeState.AVAILABLE.value else RuntimeState.ERROR.value,
                    renderer=None, vendor=None, version=None,
                    source="EGL14/GLES20 glGetString(GL_RENDERER) (android app)",
                    evidence_ref=f"{APP_EVIDENCE}#gpu_renderer", condition=None,
                    error=app.get("error_message") or (None if app["state"] != RuntimeState.AVAILABLE.value
                                                       else "App reported AVAILABLE without a renderer string."),
                    notes=app.get("notes"))
    if props.get("probe_error_surfaceflinger") and not _app_collected(props):
        return dict(state=RuntimeState.ERROR.value, renderer=None, vendor=None, version=None,
                    source="adb shell dumpsys SurfaceFlinger", evidence_ref=f"{COMMANDS_LOG}#probe_error_surfaceflinger",
                    condition=None, error=props["probe_error_surfaceflinger"], notes=None)
    legacy = props.get("gpu_renderer") or props.get("gles_renderer") or props.get("renderer")
    if legacy:
        return dict(state=RuntimeState.AVAILABLE.value, renderer=legacy, vendor=None, version=None,
                    source="GLES20.glGetString(GL_RENDERER)", evidence_ref="evidence/observed_props.json#gpu_renderer",
                    condition=None, error=None, notes=None)
    notes = None
    if "host_gles" in props:
        notes = "Host SurfaceFlinger output had no GLES line; app EGL probe result not available."
    return dict(state=RuntimeState.NOT_TESTED.value, renderer=None, vendor=None, version=None,
                source="EGL GL_RENDERER / dumpsys SurfaceFlinger", evidence_ref=None, condition=None, error=None,
                notes=notes)


def cpufreq_policy_result(props: Dict[str, Any], metric: str, files: Tuple[str, ...], source: str,
                          verification_method: str, value_text: Optional[str] = None,
                          pilot_note: Optional[str] = None) -> CapabilityResult:
    """Record from the per-policy cpufreq probe (A7): AVAILABLE (host ADB) when every file in `files` is readable
    for at least one policy. Observability only: no throttling or capping behaviour is inferred."""
    is_real = bool(props.get("is_real_device_observation", False))
    probe = props.get("cpufreq_policy_probe")
    ev = "evidence/cpufreq_policy_evidence.json"
    common = dict(is_real=is_real, source=source, verification_method=verification_method)
    if not isinstance(probe, dict):
        return _make(metric, RuntimeState.NOT_TESTED.value, **common, notes="Host cpufreq policy probe not executed.")
    listing = probe.get("listing_outcome")
    if listing != "READABLE":
        state = _OUTCOME_STATE.get(listing, RuntimeState.ERROR.value)
        return _make(metric, state, evidence_ref=ev, **common,
                     error_message="cpufreq policy directory listing failed" if state == RuntimeState.ERROR.value else None,
                     notes=None if state == RuntimeState.ERROR.value else f"cpufreq policy directory: {listing}.")
    policies = probe.get("policies") or {}
    if not policies:
        return _make(metric, RuntimeState.UNAVAILABLE.value, evidence_ref=ev, **common,
                     notes="No policyN directories under the configured cpufreq policy directory.")
    readable = {pol: {f: files_[f]["value"] for f in files}
                for pol, files_ in policies.items()
                if all((files_.get(f) or {}).get("outcome") == "READABLE" for f in files)}
    if readable:
        return _make(metric, RuntimeState.AVAILABLE.value, value=value_text or readable, unit=None if value_text else "kHz",
                     evidence_ref=ev, condition=HOST_ADB, **common,
                     notes=_join_notes(f"Readable for policies: {', '.join(sorted(readable))}.", pilot_note))
    outcomes = {(files_.get(f) or {}).get("outcome") for files_ in policies.values() for f in files}
    if "PERMISSION_DENIED" in outcomes:
        state = RuntimeState.PERMISSION_REQUIRED.value
    elif outcomes == {"ABSENT"}:
        state = RuntimeState.UNAVAILABLE.value
    else:
        state = RuntimeState.ERROR.value
    return _make(metric, state, evidence_ref=ev, **common,
                 error_message="cpufreq policy files could not be read" if state == RuntimeState.ERROR.value else None,
                 notes=f"Per-policy outcomes: {sorted(o for o in outcomes if o)}.")


class DeviceIdentityCollector:
    """Collector 1: DeviceIdentityCollector.
    Checks device unit ID, known specifications, observed identity properties,
    and performs the 3 GB RAM variant verification check (R-08 nearest-nominal rule).

    `total_ram_mb` holds MiB (host floor(MemTotal_kB / 1024), app floor(totalMem / 1,048,576)).
    The variant specification comes from `ram_variant_check` in configs/device_characterization.yaml.
    """

    def __init__(self, device_unit_id: str = "OPPO_A5_2020_UNIT_01",
                 ram_variant_spec: Optional[Dict[str, Any]] = None):
        self.device_unit_id = device_unit_id
        self.ram_variant_spec = (
            validate_ram_variant_spec(ram_variant_spec) if ram_variant_spec else load_ram_variant_spec()
        )

    def collect(self, observed_props: Optional[Dict[str, Any]] = None) -> DeviceIdentity:
        known = KnownSpecification()
        props = observed_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        observed_results: List[CapabilityResult] = []

        probe_err_prop = props.get("probe_error_getprop")
        probe_err_mem = props.get("probe_error_meminfo")

        # Manufacturer
        obs_mfr = props.get("manufacturer") or props.get("ro.product.manufacturer")
        if "manufacturer" not in props and "ro.product.manufacturer" not in props:
            if probe_err_prop:
                state_mfr = RuntimeState.ERROR.value
                ver_mfr = False
                err_mfr = probe_err_prop
                ev_mfr = "evidence/commands.log#probe_error_getprop"
            else:
                state_mfr = RuntimeState.NOT_TESTED.value
                ver_mfr = False
                err_mfr = None
                ev_mfr = None
        else:
            state_mfr, ver_mfr, ev_mfr = _determine_state_and_verification(
                props, "manufacturer" if "manufacturer" in props else "ro.product.manufacturer"
            )
            if ver_mfr and _is_app_derived(props, "manufacturer"):
                ev_mfr = f"{APP_EVIDENCE}#manufacturer"
            err_mfr = None

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
            error_message=err_mfr,
        ))

        # Model
        obs_model = props.get("model") or props.get("ro.product.model")
        if "model" not in props and "ro.product.model" not in props:
            if probe_err_prop:
                state_model = RuntimeState.ERROR.value
                ver_model = False
                err_model = probe_err_prop
                ev_model = "evidence/commands.log#probe_error_getprop"
            else:
                state_model = RuntimeState.NOT_TESTED.value
                ver_model = False
                err_model = None
                ev_model = None
        else:
            state_model = RuntimeState.AVAILABLE.value if obs_model else RuntimeState.UNAVAILABLE.value
            ver_model = bool(props.get("is_real_device_observation") and obs_model)
            err_model = None
            if not ver_model:
                ev_model = None
            elif _is_app_derived(props, "model"):
                ev_model = f"{APP_EVIDENCE}#model"
            else:
                ev_model = "evidence/getprop_evidence.txt#ro.product.model"

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
            error_message=err_model,
        ))

        # Total RAM
        total_ram_mb = props.get("total_ram_mb")
        if "total_ram_mb" not in props:
            if probe_err_mem:
                state_ram = RuntimeState.ERROR.value
                ver_ram = False
                err_ram = probe_err_mem
                ev_ram = "evidence/commands.log#probe_error_meminfo"
            else:
                state_ram = RuntimeState.NOT_TESTED.value
                ver_ram = False
                err_ram = None
                ev_ram = None
        else:
            state_ram = RuntimeState.AVAILABLE.value if total_ram_mb is not None else RuntimeState.UNAVAILABLE.value
            ver_ram = bool(props.get("is_real_device_observation") and total_ram_mb is not None)
            err_ram = None
            if _is_app_derived(props, "total_ram_mb"):
                ev_ram = f"{APP_EVIDENCE}#total_ram_mb" if ver_ram else None
            else:
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
            error_message=err_ram,
        ))

        # SoC Model (P-04 provenance check)
        obs_soc = props.get("soc_model") or props.get("ro.soc.model")
        source_soc_prop = props.get("source_soc_prop")
        state_soc = RuntimeState.AVAILABLE.value if obs_soc else (
            RuntimeState.UNAVAILABLE.value if ("soc_model" in props or "ro.soc.model" in props or "source_soc_prop" in props) else RuntimeState.NOT_TESTED.value
        )
        ver_soc = bool(props.get("is_real_device_observation") and obs_soc)
        
        if ver_soc and obs_soc:
            if _is_app_derived(props, "soc_model"):
                ev_soc = f"{APP_EVIDENCE}#soc_model"
            elif source_soc_prop == "ro.soc.model":
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

        # GPU renderer (A8): one authoritative observation shared with GPUTelemetryCollector.
        gpu = _resolve_gpu_renderer(props)
        observed_results.append(_make(
            "gpu_renderer", gpu["state"], is_real=bool(props.get("is_real_device_observation")),
            source=gpu["source"], verification_method="gles_renderer_string_check",
            value={"renderer": gpu["renderer"], "vendor": gpu["vendor"], "version": gpu["version"]}
            if gpu["state"] == RuntimeState.AVAILABLE.value else None,
            evidence_ref=gpu["evidence_ref"], condition=gpu["condition"], error_message=gpu["error"],
            notes=gpu["notes"],
        ))

        # Storage (matrix §1): StatFs on the data partition, app only.
        observed_results.append(_app_result(props, "storage_total_bytes", record_name="storage_total",
                                            source="StatFs(Environment.getDataDirectory()).getTotalBytes()",
                                            verification_method="statfs_check", unit="bytes"))

        # Variant check (R-08): nearest nominal capacity, unit MiB; see ram_variant.py and the config.
        if total_ram_mb is not None:
            total_ram_mib = total_ram_mb
            cls = classify_ram_variant(total_ram_mib, self.ram_variant_spec)
            required = cls["required_variant"]
            is_real_obs = bool(props.get("is_real_device_observation"))
            # Evidence cites the source that actually supplied the RAM value (P5-01).
            ev_variant_src = (
                f"{APP_EVIDENCE}#total_ram_mb" if _is_app_derived(props, "total_ram_mb")
                else "evidence/meminfo_evidence.txt#ram_variant_check"
            )
            common = dict(
                metric="variant_check",
                unit="variant",
                source="MemoryInfo.totalMem / MemTotal nearest-nominal variant check (R-08)",
                verification_method="nearest_nominal_variant",
            )
            if cls["classification"] == RAM_INVALID:
                variant_res = CapabilityResult(
                    state=RuntimeState.ERROR.value,
                    report_status=map_runtime_state_to_report_status(RuntimeState.ERROR, verified=False),
                    value=None,
                    verified=False,
                    evidence_ref=ev_variant_src if is_real_obs else None,
                    error_message=f"Observed total RAM {total_ram_mib!r} MiB cannot be classified (non-positive or non-numeric).",
                    notes="Variant check could not be performed; blocks Step 10D sign-off.",
                    **common,
                )
            elif cls["classification"] == RAM_MATCH:
                ver_v = is_real_obs
                variant_res = CapabilityResult(
                    state=RuntimeState.AVAILABLE.value,
                    report_status=ReportStatus.VERIFIED.value if ver_v else ReportStatus.AVAILABLE.value,
                    value=cls,
                    verified=ver_v,
                    observed_at=now if ver_v else None,
                    evidence_ref=ev_variant_src if ver_v else None,
                    notes=(f"Observed {total_ram_mib} MiB is nearest the {required} nominal "
                           f"({cls['nominal_ram_mib']} MiB): matches the required experimental variant."),
                    **common,
                )
            else:
                if cls["classification"] == RAM_AMBIGUOUS:
                    finding = (f"Observed {total_ram_mib} MiB is equidistant from "
                               f"{' and '.join(cls['tied_variants'])}: AMBIGUOUS, not assigned to either variant.")
                else:
                    finding = (f"Observed {total_ram_mib} MiB is nearest the {cls['nearest_variant']} nominal "
                               f"({cls['nominal_ram_mib']} MiB), not the required {required}: MISMATCH.")
                variant_res = CapabilityResult(
                    state=RuntimeState.AVAILABLE.value,
                    report_status=ReportStatus.AVAILABLE.value,
                    value=cls,
                    verified=False,
                    observed_at=now,
                    evidence_ref=ev_variant_src if is_real_obs else None,
                    notes=f"{finding} Blocks Step 10D sign-off (protocol §2, §9); other variants are never substitutes.",
                    **common,
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

        probe_err_prop = props.get("probe_error_getprop")
        api_level = props.get("api_level")
        if "api_level" not in props:
            if probe_err_prop:
                state_api = RuntimeState.ERROR.value
                err_api = probe_err_prop
                ev_api = "evidence/commands.log#probe_error_getprop"
            else:
                state_api = RuntimeState.NOT_TESTED.value
                err_api = None
                ev_api = None
        else:
            state_api = RuntimeState.AVAILABLE.value if api_level is not None else RuntimeState.UNAVAILABLE.value
            err_api = None
            ev_api = "evidence/getprop_evidence.txt#ro.build.version.sdk" if (is_real and state_api == RuntimeState.AVAILABLE.value) else None

        ver_api = is_real and state_api == RuntimeState.AVAILABLE.value
        results.append(CapabilityResult(
            metric="api_level",
            state=state_api,
            report_status=map_runtime_state_to_report_status(RuntimeState(state_api), verified=ver_api),
            value=api_level if state_api == RuntimeState.AVAILABLE.value else None,
            source="Build.VERSION.SDK_INT",
            verified=ver_api,
            verification_method="device_observation",
            observed_at=now if ver_api else None,
            evidence_ref=ev_api,
            error_message=err_api,
        ))

        rel_version = props.get("release_version")
        if "release_version" not in props:
            if probe_err_prop:
                state_rel = RuntimeState.ERROR.value
                err_rel = probe_err_prop
                ev_rel = "evidence/commands.log#probe_error_getprop"
            else:
                state_rel = RuntimeState.NOT_TESTED.value
                err_rel = None
                ev_rel = None
        else:
            state_rel = RuntimeState.AVAILABLE.value if rel_version else RuntimeState.UNAVAILABLE.value
            err_rel = None
            ev_rel = "evidence/getprop_evidence.txt#ro.build.version.release" if (is_real and state_rel == RuntimeState.AVAILABLE.value) else None

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
            evidence_ref=ev_rel,
            error_message=err_rel,
        ))

        # Build identity from getprop (host): security patch and fingerprint (matrix §1 Build, §2 Security patch).
        for metric, key, prop in (("security_patch", "security_patch", "ro.build.version.security_patch"),
                                  ("build_fingerprint", "build_fingerprint", "ro.build.fingerprint")):
            if key not in props:
                st = RuntimeState.ERROR.value if probe_err_prop else RuntimeState.NOT_TESTED.value
                results.append(_make(metric, st, is_real=is_real, source=f"getprop {prop}",
                                     verification_method="device_observation",
                                     evidence_ref=f"{COMMANDS_LOG}#probe_error_getprop" if probe_err_prop else None,
                                     error_message=probe_err_prop or None))
            else:
                val = props.get(key)
                st = RuntimeState.AVAILABLE.value if val else RuntimeState.UNAVAILABLE.value
                results.append(_make(metric, st, is_real=is_real, value=val, source=f"getprop {prop}",
                                     verification_method="device_observation",
                                     evidence_ref=f"evidence/getprop_evidence.txt#{prop}",
                                     notes=None if val else f"{prop} is empty or not set on this build."))

        # Platform services (B1): obtained and exercised by the app. The app's state is preserved, including
        # PERMISSION_REQUIRED (e.g. HardwarePropertiesManager outside device-owner/VR mode); a service object
        # existing is never taken as proof that its operations are permitted.
        services = {
            "PowerManager": "getSystemService(POWER_SERVICE) + isPowerSaveMode()",
            "HardwarePropertiesManager": "getSystemService(HARDWARE_PROPERTIES_SERVICE) + getDeviceTemperatures()",
            "CameraManager": "getSystemService(CAMERA_SERVICE) + getCameraIdList()",
            "ActivityManager": "getSystemService(ACTIVITY_SERVICE) + getMemoryInfo()",
            "BatteryManager": "getSystemService(BATTERY_SERVICE) + getIntProperty(BATTERY_PROPERTY_CAPACITY)",
        }
        for svc, op in services.items():
            key = f"service_{svc}"
            if key in props and not _app_collected(props):
                # Legacy/mock input path: a plain boolean; never verified without the app evidence file.
                st = RuntimeState.AVAILABLE.value if props.get(key) is True else RuntimeState.UNAVAILABLE.value
                results.append(_make(key, st, is_real=False, value=f"{svc} available", source=op,
                                     verification_method="service_get_check"))
                continue
            results.append(_app_result(props, key, source=op, verification_method="service_operation_check"))

        results.append(_app_result(props, "power_save_mode", source="PowerManager.isPowerSaveMode()",
                                   verification_method="service_operation_check"))
        cam_list = _app_rec(props, "camera_id_list")
        cam_probe = _app_rec(props, "camera_probe")
        use_probe = cam_list is None and cam_probe is not None
        results.append(_app_result(props, "camera_id_list", record=cam_probe if use_probe else cam_list,
                                   anchor="camera_probe" if use_probe else "camera_id_list",
                                   source="CameraManager.getCameraIdList()", verification_method="camera_id_list_check"))

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
                if _is_app_derived(props, "battery_level_percent"):
                    ev_lvl = "evidence/android_app_evidence.json#battery_level_percent" if (is_real and state_lvl == RuntimeState.AVAILABLE.value) else None
                else:
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
                if _is_app_derived(props, "battery_voltage"):
                    ev_volt = "evidence/android_app_evidence.json#battery_voltage" if (is_real and state_volt == RuntimeState.AVAILABLE.value) else None
                else:
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
                if _is_app_derived(props, "battery_temperature"):
                    ev_temp = "evidence/android_app_evidence.json#battery_temperature" if (is_real and state_temp == RuntimeState.AVAILABLE.value) else None
                else:
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

        # Battery current now (mA / uA) — R-09 explicit unit safety
        probe_err_curr = props.get("probe_error_battery_current") or probe_err_bat
        if "battery_current_now" not in props and "current_now_ua" not in props and "current_now_ma" not in props:
            if probe_err_curr:
                state_curr = RuntimeState.ERROR.value
                val_curr = None
                ver_curr = False
                err_curr = probe_err_curr
                notes_curr = f"Battery current probe failed: {probe_err_curr}"
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
            explicit_unit = props.get("battery_current_unit") or ("uA" if curr_ua is not None else ("mA" if props.get("current_now_ma") is not None else None))
            err_curr = None

            if sentinel or (curr_raw is None and curr_ua is None and not probe_err_curr):
                state_curr = RuntimeState.UNAVAILABLE.value
                val_curr = None
                ver_curr = False
                notes_curr = "Current property is unsupported or sentinel value returned."
                ev_curr = None
            elif probe_err_curr:
                state_curr = RuntimeState.ERROR.value
                val_curr = None
                ver_curr = False
                err_curr = probe_err_curr
                notes_curr = f"Battery current probe failed: {probe_err_curr}"
                ev_curr = "evidence/commands.log#probe_error_battery"
            else:
                raw_val = curr_raw if curr_raw is not None else curr_ua

                # 1. Parse validation: check if raw_val is non-numeric / malformed
                try:
                    num_val = float(raw_val)
                except (ValueError, TypeError):
                    state_curr = RuntimeState.ERROR.value
                    val_curr = None
                    ver_curr = False
                    err_curr = f"Malformed battery current value: '{raw_val}'"
                    notes_curr = f"Battery current value '{raw_val}' cannot be parsed as numeric."
                    ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now" if is_real else None
                    num_val = None

                if num_val is not None:
                    # R-09: Check unit explicitly — DO NOT infer purely from numeric magnitude cutoff!
                    if explicit_unit in ("mA", "milliamperes", "milliamps"):
                        converted_ma = num_val
                        unit_known = True
                    elif explicit_unit in ("uA", "µA", "microamperes", "microamps"):
                        converted_ma = num_val / 1000.0
                        unit_known = True
                    else:
                        # Ambiguous unit (not explicitly established from evidence)
                        converted_ma = num_val
                        unit_known = False

                    if abs(converted_ma) > 10000 and unit_known:
                        state_curr = RuntimeState.ERROR.value
                        val_curr = None
                        ver_curr = False
                        err_curr = f"Implausible battery current value: {raw_val} (converted: {converted_ma} mA)"
                        notes_curr = f"Implausible battery current value: {raw_val}"
                        ev_curr = None
                    elif not unit_known:
                        # R-09 / F-05: Never mark battery current VERIFIED when unit cannot be established from evidence, and set unit = None!
                        state_curr = RuntimeState.AVAILABLE.value
                        val_curr = converted_ma
                        ver_curr = False  # MANDATORY: UNVERIFIED
                        unit_curr = None  # F-05: DO NOT output unit = "mA" when unit is unknown!
                        notes_curr = f"Battery current unit cannot be conclusively established from raw value {raw_val} without explicit unit metadata (unverified)."
                        ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now" if is_real else None
                    elif converted_ma == 0.0:
                        # R-09: Zero current with known unit cannot be verified as valid physical measurement
                        state_curr = RuntimeState.AVAILABLE.value
                        val_curr = 0.0
                        ver_curr = False  # UNVERIFIED
                        unit_curr = "mA"
                        notes_curr = "Observed battery current reading is 0. Flagged as potential driver sentinel zero (unverified)."
                        ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now" if is_real else None
                    else:
                        # Interface demonstrated; sign convention and update rate are not checked in Step 10D,
                        # so the value is REQUIRES PILOT VALIDATION rather than VERIFIED (protocol §3, B2).
                        state_curr = RuntimeState.AVAILABLE.value
                        val_curr = converted_ma
                        ver_curr = False
                        pilot_curr = True
                        unit_curr = "mA"
                        notes_curr = (f"Raw current reading: {raw_val} ({explicit_unit}), converted to {converted_ma} mA. "
                                      "Sign convention and update rate: REQUIRES PILOT VALIDATION.")
                        ev_curr = "evidence/battery_dumpsys_evidence.txt#battery_current_now" if is_real else None

        host_current = CapabilityResult(
            metric="battery_current_now",
            state=state_curr,
            report_status=map_runtime_state_to_report_status(
                RuntimeState(state_curr), verified=ver_curr,
                pilot_validation=bool(locals().get("pilot_curr")) and state_curr == RuntimeState.AVAILABLE.value),
            value=val_curr,
            unit=unit_curr if 'unit_curr' in locals() else None,
            source="BatteryManager.BATTERY_PROPERTY_CURRENT_NOW / dumpsys battery",
            verified=ver_curr,
            verification_method="battery_property_check",
            observed_at=now if (ver_curr or state_curr == RuntimeState.AVAILABLE.value) else None,
            evidence_ref=ev_curr,
            error_message=err_curr,
            notes=notes_curr,
        )
        results.append(self._battery_property_current(props, host_current, "battery_property_current_now",
                                                      "battery_current_now",
                                                      "BatteryManager.getIntProperty(BATTERY_PROPERTY_CURRENT_NOW)",
                                                      dumpsys_field="current now"))
        results.append(self._battery_property_current(props, None, "battery_property_current_average",
                                                      "battery_current_average",
                                                      "BatteryManager.getIntProperty(BATTERY_PROPERTY_CURRENT_AVERAGE)"))
        results.append(self._charge_counter(props))
        results.append(self._energy_counter(props))
        results.extend(self._status_records(props))
        return TelemetryCapability(
            dimension="battery",
            results=results,
            resource_state_input=True,
            reliability="REQUIRES PILOT VALIDATION",
        )


    # --- Battery helpers -------------------------------------------------------------------------------
    @staticmethod
    def _dumpsys_ran(props: Dict[str, Any]) -> bool:
        return isinstance(props.get("battery_dumpsys_fields"), list)

    def _battery_property_current(self, props: Dict[str, Any], host_result: Optional[CapabilityResult],
                                  app_metric: str, metric: str, source: str,
                                  dumpsys_field: Optional[str] = None) -> CapabilityResult:
        """BATTERY_PROPERTY_CURRENT_* (B2). The app's BatteryManager property is the protocol interface and is
        preferred; the host dumpsys value (R-09 handling) is used only when the app did not report the property.
        A value in uA (API contract) that is non-zero is REQUIRES PILOT VALIDATION (sign/update rate), never VERIFIED.
        """
        is_real = bool(props.get("is_real_device_observation", False))
        rec = _app_rec(props, app_metric) if _app_collected(props) else None
        if rec is not None:
            ref = f"{APP_EVIDENCE}#{app_metric}"
            common = dict(is_real=is_real, source=f"{source} (android app)", verification_method="battery_property_check")
            if rec.get("state") == RuntimeState.AVAILABLE.value:
                raw = rec.get("value")
                if not isinstance(raw, (int, float)) or isinstance(raw, bool):
                    return _make(metric, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                                 error_message=f"Non-numeric {app_metric} value from the app: {raw!r}")
                ma = raw / 1000.0  # BatteryManager current properties are documented in microamperes
                if abs(ma) > 10000:
                    return _make(metric, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                                 error_message=f"Implausible battery current value: {raw} uA")
                if raw == 0:
                    return _make(metric, RuntimeState.AVAILABLE.value, value=0.0, unit="mA", evidence_ref=ref,
                                 verifiable=False, **common,
                                 notes="Property returned 0: possible unsupported-zero; not verified (R-09).")
                return _make(metric, RuntimeState.AVAILABLE.value, value=ma, unit="mA", evidence_ref=ref, pilot=True,
                             **common, notes=f"Raw {raw} uA (API unit) converted to mA. Sign convention and update "
                                             "rate: REQUIRES PILOT VALIDATION.")
            return _app_result(props, app_metric, record_name=metric, source=f"{source} (android app)",
                               verification_method="battery_property_check", unit="mA")
        if host_result is not None and host_result.state != RuntimeState.NOT_TESTED.value:
            return host_result
        if host_result is not None and dumpsys_field and self._dumpsys_ran(props):
            # Host dumpsys ran but this build does not print the field; the BatteryManager property was not
            # probed by the app. Not a device fact about the property, so it stays NOT_TESTED, explicitly.
            return _make(metric, RuntimeState.NOT_TESTED.value, is_real=is_real, source=source,
                         verification_method="battery_property_check",
                         evidence_ref="evidence/battery_dumpsys_evidence.txt",
                         notes=f"dumpsys battery executed but does not print '{dumpsys_field}' on this build; "
                               "the BatteryManager property itself was not probed (no app record).")
        if host_result is not None:
            return host_result
        return _app_result(props, app_metric, record_name=metric, source=f"{source} (android app)",
                           verification_method="battery_property_check", unit="mA")

    def _charge_counter(self, props: Dict[str, Any]) -> CapabilityResult:
        """BATTERY_PROPERTY_CHARGE_COUNTER (uAh): app property preferred, else dumpsys 'Charge counter' (A3).
        A non-zero reading demonstrates the interface; monotonic change during discharge is REQUIRES PILOT VALIDATION.
        """
        is_real = bool(props.get("is_real_device_observation", False))
        metric = "battery_charge_counter"

        def _classify(raw: Any, ref: str, source: str) -> CapabilityResult:
            common = dict(is_real=is_real, source=source, verification_method="battery_property_check", unit="uAh",
                          evidence_ref=ref)
            if not isinstance(raw, int) or isinstance(raw, bool):
                return _make(metric, RuntimeState.ERROR.value, **common, error_message=f"Non-integer charge counter {raw!r}")
            if raw == 0:
                return _make(metric, RuntimeState.AVAILABLE.value, value=0, verifiable=False, **common,
                             notes="Charge counter reads 0: possible unsupported-zero; not verified.")
            if raw < 0:
                return _make(metric, RuntimeState.ERROR.value, **common, error_message=f"Negative charge counter {raw}")
            return _make(metric, RuntimeState.AVAILABLE.value, value=raw, pilot=True, **common,
                         notes="Single reading. Monotonic change during discharge: REQUIRES PILOT VALIDATION.")

        rec = _app_rec(props, "battery_property_charge_counter") if _app_collected(props) else None
        if rec is not None:
            if rec.get("state") == RuntimeState.AVAILABLE.value:
                return _classify(rec.get("value"), f"{APP_EVIDENCE}#battery_property_charge_counter",
                                 "BatteryManager.getIntProperty(BATTERY_PROPERTY_CHARGE_COUNTER) (android app)")
            return _app_result(props, "battery_property_charge_counter", record_name=metric, unit="uAh",
                               source="BatteryManager.getIntProperty(BATTERY_PROPERTY_CHARGE_COUNTER) (android app)",
                               verification_method="battery_property_check")
        if props.get("charge_counter_is_sentinel"):
            return _make(metric, RuntimeState.UNAVAILABLE.value, is_real=is_real, unit="uAh",
                         source="BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER",
                         verification_method="battery_property_check", notes="Unsupported sentinel returned.")
        host_src = "dumpsys battery 'Charge counter' (BatteryService health info)"
        if props.get("probe_error_battery_charge_counter"):
            return _make(metric, RuntimeState.ERROR.value, is_real=is_real, unit="uAh", source=host_src,
                         verification_method="battery_property_check",
                         evidence_ref="evidence/battery_dumpsys_evidence.txt",
                         error_message=props["probe_error_battery_charge_counter"])
        for key in ("battery_charge_counter", "charge_counter_uah"):
            if key in props:
                raw = props[key]
                if raw is None:
                    return _make(metric, RuntimeState.UNAVAILABLE.value, is_real=is_real, unit="uAh", source=host_src,
                                 verification_method="battery_property_check")
                return _classify(raw, "evidence/battery_dumpsys_evidence.txt#Charge counter", host_src)
        if props.get("probe_error_battery"):
            return _make(metric, RuntimeState.ERROR.value, is_real=is_real, unit="uAh", source=host_src,
                         verification_method="battery_property_check",
                         evidence_ref=f"{COMMANDS_LOG}#probe_error_battery", error_message=props["probe_error_battery"])
        if self._dumpsys_ran(props):
            return _make(metric, RuntimeState.NOT_TESTED.value, is_real=is_real, unit="uAh", source=host_src,
                         verification_method="battery_property_check",
                         evidence_ref="evidence/battery_dumpsys_evidence.txt",
                         notes="dumpsys battery executed but prints no 'Charge counter' field on this build; "
                               "the BatteryManager property itself was not probed (no app record).")
        return _make(metric, RuntimeState.NOT_TESTED.value, is_real=is_real, unit="uAh", source=host_src,
                     verification_method="battery_property_check")

    def _energy_counter(self, props: Dict[str, Any]) -> CapabilityResult:
        """BATTERY_PROPERTY_ENERGY_COUNTER (nWh), app only. Long.MIN_VALUE sentinel -> UNAVAILABLE (set by the app)."""
        rec = _app_rec(props, "battery_property_energy_counter") if _app_collected(props) else None
        pilot = bool(rec and rec.get("state") == RuntimeState.AVAILABLE.value and rec.get("value") not in (0, None))
        verifiable = not (rec and rec.get("value") == 0)
        return _app_result(props, "battery_property_energy_counter", record_name="battery_energy_counter",
                           unit="nWh", pilot=pilot, verifiable=verifiable,
                           source="BatteryManager.getLongProperty(BATTERY_PROPERTY_ENERGY_COUNTER) (android app)",
                           verification_method="battery_property_check",
                           notes="Accuracy relative to an external reference: REQUIRES PILOT VALIDATION (D-16)." if pilot else None)

    _HEALTH = {1: "UNKNOWN", 2: "GOOD", 3: "OVERHEAT", 4: "DEAD", 5: "OVER_VOLTAGE", 6: "UNSPECIFIED_FAILURE", 7: "COLD"}
    _STATUS = {1: "UNKNOWN", 2: "CHARGING", 3: "DISCHARGING", 4: "NOT_CHARGING", 5: "FULL"}

    def _status_records(self, props: Dict[str, Any]) -> List[CapabilityResult]:
        """Charging state / plug type and health / status from dumpsys battery (host). Fields that the build
        does not print are never defaulted."""
        is_real = bool(props.get("is_real_device_observation", False))
        out: List[CapabilityResult] = []
        fields = props.get("battery_dumpsys_fields")
        err = props.get("probe_error_battery")
        src = "dumpsys battery (ACTION_BATTERY_CHANGED state)"
        for metric, needed in (("battery_charging_state", "status"), ("battery_health_status", "health")):
            if not isinstance(fields, list):
                st = RuntimeState.ERROR.value if err else RuntimeState.NOT_TESTED.value
                out.append(_make(metric, st, is_real=is_real, source=src, verification_method="battery_broadcast_check",
                                 evidence_ref=f"{COMMANDS_LOG}#probe_error_battery" if err else None, error_message=err))
                continue
            if needed not in fields:
                out.append(_make(metric, RuntimeState.UNAVAILABLE.value, is_real=is_real, source=src,
                                 verification_method="battery_broadcast_check",
                                 evidence_ref="evidence/battery_dumpsys_evidence.txt",
                                 notes=f"dumpsys battery prints no '{needed}' field on this build."))
                continue
            if metric == "battery_charging_state":
                code = props.get("battery_status_code")
                value = {"status_code": code, "status": self._STATUS.get(code),
                         "plug_source": props.get("plugged_source")}
            else:
                code = props.get("battery_health_code")
                value = {"health_code": code, "health": self._HEALTH.get(code),
                         "status_code": props.get("battery_status_code")}
            if code is None:
                out.append(_make(metric, RuntimeState.ERROR.value, is_real=is_real, source=src,
                                 verification_method="battery_broadcast_check",
                                 evidence_ref="evidence/battery_dumpsys_evidence.txt",
                                 error_message=f"'{needed}' field present but not an integer"))
                continue
            out.append(_make(metric, RuntimeState.AVAILABLE.value, is_real=is_real, value=value, source=src,
                             verification_method="battery_broadcast_check",
                             evidence_ref=f"evidence/battery_dumpsys_evidence.txt#{needed}"))
        return out


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
            if _is_app_derived(props, "available_memory_mb"):
                ev_avail = "evidence/android_app_evidence.json#available_memory_mb" if (is_real and state_avail == RuntimeState.AVAILABLE.value) else None
            else:
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

        # ActivityManager.MemoryInfo.lowMemory / threshold (B3): app-only. /proc/meminfo has no such field.
        results.append(_app_result(props, "low_memory_flag", source="ActivityManager.MemoryInfo.lowMemory",
                                   verification_method="memory_info_check", unit="boolean",
                                   notes="Behaviour under memory pressure (D-13, ColorOS): REQUIRES PILOT VALIDATION."))
        results.append(_app_result(props, "memory_threshold_mb", source="ActivityManager.MemoryInfo.threshold",
                                   verification_method="memory_info_check", unit="MB"))
        results.append(_app_result(props, "app_heap_allocated_mb", source="Runtime.totalMemory() - Runtime.freeMemory()",
                                   verification_method="runtime_heap_check", unit="MB"))
        results.append(_app_result(props, "app_pss_kb", source="Debug.getMemoryInfo(Debug.MemoryInfo).getTotalPss()",
                                   verification_method="process_memory_check", unit="kB"))

        # PSI memory pressure (A5): host probe of the configured /proc/pressure/memory path.
        psi_probe = props.get("psi_memory_probe")
        kernel = props.get("kernel_release")
        results.append(_host_outcome_result(
            "psi_memory_pressure", psi_probe, is_real=is_real,
            source=f"{(psi_probe or {}).get('target', '/proc/pressure/memory')} via adb shell"
                   + (f" (kernel {kernel})" if kernel else ""),
            verification_method="file_read_check", evidence_file="psi_memory_evidence.json",
            value="PSI memory file readable", pilot_note="Readability only; meaning as a resource-state input "
                                                         "REQUIRES PILOT VALIDATION. App readability not tested.",
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

        # Host sysfs read through adb: CONDITIONALLY AVAILABLE (HOST ADB SHELL), never VERIFIED (§12).
        results.append(_make(
            "cpu_scaling_cur_freq", state_freq, is_real=is_real, value=val_freq, unit="kHz",
            source="cpu0 scaling_cur_freq via adb shell (configs probes.cpufreq_sysfs_pattern)",
            verification_method="cpufreq_sysfs_check", condition=HOST_ADB,
            evidence_ref=ev_freq if state_freq != RuntimeState.AVAILABLE.value else "evidence/cpufreq_evidence.txt#scaling_cur_freq",
            error_message=err_freq,
            notes="Read through host adb; app readability not tested." if state_freq == RuntimeState.AVAILABLE.value else None,
        ))
        results.append(cpufreq_policy_result(props, "cpu_frequency_limits", ("scaling_max_freq", "cpuinfo_max_freq"),
                                             "cpufreq policy scaling_max_freq / cpuinfo_max_freq via adb shell",
                                             "cpufreq_limits_check"))

        # Process CPU time (B4): app only; not a utilisation figure.
        results.append(_app_result(props, "app_cpu_time", source="Process.getElapsedCpuTime()",
                                   verification_method="process_cpu_time_check", unit="ms",
                                   notes="Process CPU time of the characterization app; not interpreted as utilisation."))

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
                ver_proc = False  # condition-gated: CONDITIONALLY AVAILABLE, never VERIFIED (§12)
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
            observed_at=now if (is_real and state_proc != RuntimeState.NOT_TESTED.value) else None,
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

        # gpu_vendor_renderer is derived from the same single observation as device_identity gpu_renderer (A8).
        gpu = _resolve_gpu_renderer(props)
        rend_val = (f"{gpu['vendor']} / {gpu['renderer']}" if gpu["vendor"] else gpu["renderer"]) \
            if gpu["state"] == RuntimeState.AVAILABLE.value else None
        results.append(_make(
            "gpu_vendor_renderer", gpu["state"], is_real=is_real, value=rend_val, source=gpu["source"],
            verification_method="gles_renderer_string_check", evidence_ref=gpu["evidence_ref"],
            condition=gpu["condition"], error_message=gpu["error"],
            notes=_join_notes("Derived from the same observation as device_identity gpu_renderer.", gpu["notes"]),
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

        # Host kgsl sysfs read: CONDITIONALLY AVAILABLE (HOST ADB SHELL), never VERIFIED (§12). A clock value is
        # never a utilisation figure.
        results.append(_make(
            "gpu_clock_hz", state_freq, is_real=is_real, value=val_freq, unit="Hz",
            source="kgsl gpuclk via adb shell (configs probes.kgsl_gpu_clock_path)",
            verification_method="kgsl_sysfs_check", condition=HOST_ADB,
            evidence_ref=ev_freq if state_freq != RuntimeState.AVAILABLE.value else "evidence/gpu_evidence.txt#gpuclk",
            error_message=err_freq,
        ))

        # GPU busy counters (A6): readability of the configured kgsl gpubusy node only.
        busy = props.get("gpu_busy_probe")
        results.append(_host_outcome_result(
            "gpu_utilization", busy, is_real=is_real,
            source=f"{(busy or {}).get('target', 'kgsl gpubusy')} via adb shell",
            verification_method="kgsl_busy_readability_check", evidence_file="gpu_busy_evidence.json",
            value="kgsl gpubusy counters readable",
            pilot_note="Readability of raw busy/total counters only; no utilisation value is derived. Meaning as a "
                       "utilisation signal REQUIRES PILOT VALIDATION.",
        ))
        if results[-1].state == RuntimeState.UNAVAILABLE.value:
            results[-1].notes = _join_notes(results[-1].notes, "UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE.")

        # GPU memory: readability of the configured candidate KGSL allocation nodes only. The value is the raw
        # integer of each readable node, as reported; no unit, capacity or dedicated-GPU-memory claim is made.
        mem = props.get("gpu_memory_probe")
        mem_values = {p["target"]: p["value"] for p in (mem or {}).get("paths", [])
                      if p.get("outcome") == "READABLE" and isinstance(p.get("value"), int)}
        if mem and mem.get("outcome") == "READABLE" and not mem_values:
            mem = dict(mem, outcome="ERROR")  # inconsistent probe record: readable without a parsed integer
        mem_source = f"{(mem or {}).get('target', 'kgsl memory nodes')} via adb shell"
        if mem:
            # Notes name only the paths that produced the aggregate outcome.
            focus = [p["target"] for p in mem.get("paths", []) if p.get("outcome") == mem.get("outcome")]
            mem = dict(mem, target=", ".join(focus) or mem.get("target"))
        results.append(_host_outcome_result(
            "gpu_memory", mem, is_real=is_real, source=mem_source,
            verification_method="kgsl_memory_readability_check", evidence_file="gpu_memory_evidence.json",
            value=mem_values or None,
            pilot_note="Raw integer content of the readable KGSL node(s), as reported. Unit and meaning are not "
                       "validated; this is driver allocation accounting in shared system RAM, not dedicated GPU "
                       "memory. Per-path outcomes are in the evidence file.",
        ))
        if results[-1].state == RuntimeState.UNAVAILABLE.value:
            results[-1].notes = _join_notes(results[-1].notes, "UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE.")

        results.append(_app_result(props, "gpu_vulkan_support",
                                   source="PackageManager.hasSystemFeature(FEATURE_VULKAN_HARDWARE_VERSION / LEVEL)",
                                   verification_method="system_feature_check"))

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

        # P5-02: a non-AVAILABLE state reported by the app is preserved, never upgraded.
        err_status_api = None
        app_status_api = _app_metric_state(props, "thermal_status_api")
        app_state_value = app_status_api.get("state") if app_status_api else None
        if app_state_value in {s.value for s in RuntimeState} and app_state_value != RuntimeState.AVAILABLE.value:
            status_api_state = app_state_value
            status_api_val = None
            err_status_api = app_status_api.get("error_message")

        ver_status_api = is_real and status_api_state == RuntimeState.AVAILABLE.value
        if app_status_api and status_api_state == app_state_value:
            ev_status_api = f"{APP_EVIDENCE}#thermal_status_api" if is_real else None
        elif _is_app_derived(props, "thermal_status_api"):
            ev_status_api = f"{APP_EVIDENCE}#thermal_status_api" if ver_status_api else None
        elif status_api_state == RuntimeState.API_UNSUPPORTED.value:
            # The evidence for API_UNSUPPORTED is the observed installed API level.
            ev_status_api = GETPROP_SDK_EVIDENCE if is_real else None
        else:
            ev_status_api = "evidence/thermal_evidence.txt" if ver_status_api else None

        res_status_api = CapabilityResult(
            metric="thermal_status_api",
            state=status_api_state,
            report_status=map_runtime_state_to_report_status(RuntimeState(status_api_state), verified=ver_status_api),
            value=status_api_val,
            source="PowerManager.getCurrentThermalStatus()",
            min_api=29,
            verified=ver_status_api,
            verification_method="power_manager_thermal_status_check",
            observed_at=now if (is_real and status_api_state != RuntimeState.NOT_TESTED.value) else None,
            evidence_ref=ev_status_api,
            error_message=err_status_api,
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
            observed_at=now if (is_real and headroom_state != RuntimeState.NOT_TESTED.value) else None,
            evidence_ref=(GETPROP_SDK_EVIDENCE if (is_real and headroom_state == RuntimeState.API_UNSUPPORTED.value)
                          else ("evidence/thermal_evidence.txt" if ver_headroom else None)),
            notes=("Installed API level is below the interface minimum (API 30)."
                   if headroom_state == RuntimeState.API_UNSUPPORTED.value else None),
        )

        # Temperature sources
        temp_sources: List[CapabilityResult] = []

        # Battery temperature source (A4): derived from the battery temperature observation itself, citing the
        # same evidence (host dumpsys or app), instead of a separate flag nobody set.
        temp_sources.append(self._battery_temperature_source(props))
        state_batt_t = temp_sources[-1].state

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

        # Host sysfs read through adb: CONDITIONALLY AVAILABLE; zone type names are in the evidence file and no
        # zone is assumed to be the SoC temperature.
        temp_sources.append(_make(
            "thermal_zones_sysfs", state_zones, is_real=is_real, value=val_zones, unit="zones",
            source="thermal zone type/temp via adb shell (configs probes.thermal_sysfs_pattern)",
            verification_method="thermal_zone_sysfs_read_check", condition=HOST_ADB,
            evidence_ref=ev_zones if state_zones != RuntimeState.AVAILABLE.value else "evidence/thermal_evidence.txt#thermal_zones",
            error_message=err_zones,
            notes=("Zone type names recorded in the evidence; no zone is assumed to be SoC temperature."
                   if state_zones == RuntimeState.AVAILABLE.value else None),
        ))

        # Frequency-capping observability (A7, protocol §5.7 C): per-policy current, scaling-max and hardware-max
        # frequencies readable. Readability does not establish throttling behaviour.
        res_freq_cap = cpufreq_policy_result(
            props, "frequency_capping_observable", ("scaling_cur_freq", "scaling_max_freq", "cpuinfo_max_freq"),
            "cpufreq policy scaling_cur_freq / scaling_max_freq / cpuinfo_max_freq via adb shell",
            "cpufreq_capping_observability_check",
            value_text="Per-policy scaling_cur_freq, scaling_max_freq and cpuinfo_max_freq readable",
            pilot_note="Observability only (no load applied in Step 10D). Interpreting scaling_max_freq below "
                       "cpuinfo_max_freq as thermal capping REQUIRES PILOT VALIDATION.",
        )
        state_cap = res_freq_cap.state

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


    def _battery_temperature_source(self, props: Dict[str, Any]) -> CapabilityResult:
        is_real = bool(props.get("is_real_device_observation", False))
        common = dict(is_real=is_real, verification_method="battery_temperature_check", unit="degC")
        raw = props.get("battery_temperature", props.get("temperature_c"))
        if raw is not None:
            if isinstance(raw, (int, float)) and not isinstance(raw, bool) and -20 <= raw <= 80:
                app = _is_app_derived(props, "battery_temperature")
                return _make("temperature_battery", RuntimeState.AVAILABLE.value, value=float(raw),
                             source="BatteryManager EXTRA_TEMPERATURE" + (" (android app)" if app else " via dumpsys battery"),
                             evidence_ref=(f"{APP_EVIDENCE}#battery_temperature" if app
                                           else "evidence/battery_dumpsys_evidence.txt#battery_temperature"),
                             notes="Same observation as the battery_temperature record.", **common)
            return _make("temperature_battery", RuntimeState.ERROR.value, source="BatteryManager EXTRA_TEMPERATURE",
                         error_message=f"Implausible battery temperature value observed: {raw} degC", **common)
        if "battery_temp_available" in props:  # legacy/mock input path
            st = RuntimeState.AVAILABLE.value if props["battery_temp_available"] is True else RuntimeState.UNAVAILABLE.value
            return _make("temperature_battery", st, value="BatteryManager EXTRA_TEMPERATURE", is_real=False,
                         source="BatteryManager broadcast", verification_method="battery_temperature_check", unit="degC")
        if props.get("probe_error_battery"):
            return _make("temperature_battery", RuntimeState.ERROR.value, source="BatteryManager EXTRA_TEMPERATURE",
                         evidence_ref=f"{COMMANDS_LOG}#probe_error_battery", error_message=props["probe_error_battery"],
                         **common)
        return _make("temperature_battery", RuntimeState.NOT_TESTED.value, source="BatteryManager EXTRA_TEMPERATURE",
                     **common)

    def collect_listener(self, thermal_props: Optional[Dict[str, Any]] = None) -> TelemetryCapability:
        """Thermal-status listener registration (protocol §5.1: status API and listener), app only."""
        props = thermal_props or {}
        listener = _app_result(props, "thermal_status_listener",
                               source="PowerManager.addThermalStatusListener() / removeThermalStatusListener()",
                               verification_method="listener_registration_check", min_api=29,
                               notes="Registration only; callback delivery under thermal change is not exercised in Step 10D.")
        return TelemetryCapability(dimension="thermal", results=[listener], resource_state_input=True,
                                   reliability="REQUIRES PILOT VALIDATION")


class CameraCapabilityCollector:
    """Collector 8: CameraCapabilityCollector (protocol P3, §5.3).

    Camera IDs come only from the app's CameraManager.getCameraIdList() record; they are never generated from a
    count, and lens facing is never defaulted. Per-camera characteristics come from CameraCharacteristics in the
    app. The host `dumpsys media.camera` parse is a cross-check only (noted, never a substitute).

    Manual control (advertised vs honoured): the app reports the requested and CaptureResult values; the host
    classifies them with the tolerances in configs/device_characterization.yaml (`camera_manual_control_check`).
    Manual control is AVAILABLE only when the check ran and matched; never claimed from advertisement alone.
    """

    # Per-camera metrics reported by the app, in report order (manual_control_honoured is handled separately).
    PER_CAMERA_METRICS = (
        ("hardware_level", "CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL", None),
        ("available_capabilities", "CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES", None),
        ("manual_exposure_advertised", "REQUEST_AVAILABLE_CAPABILITIES contains MANUAL_SENSOR", None),
        ("stream_configurations", "CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP", None),
        ("ae_target_fps_ranges", "CameraCharacteristics.CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES", "fps"),
        ("af_available_modes", "CameraCharacteristics.CONTROL_AF_AVAILABLE_MODES", None),
        ("lens_min_focus_distance", "CameraCharacteristics.LENS_INFO_MINIMUM_FOCUS_DISTANCE", "diopters"),
        ("exposure_time_range_ns", "CameraCharacteristics.SENSOR_INFO_EXPOSURE_TIME_RANGE", "ns"),
        ("sensitivity_range", "CameraCharacteristics.SENSOR_INFO_SENSITIVITY_RANGE", "ISO"),
        ("awb_available_modes", "CameraCharacteristics.CONTROL_AWB_AVAILABLE_MODES", None),
        ("ae_lock_available", "CameraCharacteristics.CONTROL_AE_LOCK_AVAILABLE", None),
        ("awb_lock_available", "CameraCharacteristics.CONTROL_AWB_LOCK_AVAILABLE", None),
        ("physical_camera_ids", "CameraCharacteristics.getPhysicalCameraIds() (API 28)", None),
        ("video_profiles", "CamcorderProfile.hasProfile(cameraId, QUALITY_*)", None),
        ("capture_sensor_timestamp", "CaptureResult.SENSOR_TIMESTAMP (manual-control capture)", "ns"),
    )

    def __init__(self, manual_control_check: Optional[Dict[str, Any]] = None):
        self.check_cfg = manual_control_check if manual_control_check is not None else _load_camera_check_config()
        for key in ("exposure_time_relative_tolerance", "sensitivity_relative_tolerance"):
            v = self.check_cfg.get(key)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0:
                raise ValueError(f"camera_manual_control_check.{key} must be a non-negative number (got {v!r})")

    def collect(self, camera_props: Optional[Dict[str, Any]] = None) -> List[CameraCapability]:
        props = camera_props or {}
        is_real = bool(props.get("is_real_device_observation", False))
        id_rec = _app_rec(props, "camera_id_list") if _app_collected(props) else None
        camera_ids: Optional[List[str]] = None
        if id_rec and id_rec.get("state") == RuntimeState.AVAILABLE.value and isinstance(id_rec.get("value"), list):
            camera_ids = [str(c) for c in id_rec["value"]]
        if camera_ids:
            return [self._camera(props, cid, is_real) for cid in camera_ids]
        return [self._unidentified(props, is_real, id_rec)]

    # -- no identified cameras -----------------------------------------------------------------------------
    def _unidentified(self, props: Dict[str, Any], is_real: bool, id_rec: Optional[Dict[str, Any]]) -> CameraCapability:
        """One placeholder entry, camera_id "UNIDENTIFIED", when no camera ID list was observed. It carries the
        reason (app probe state, host failure, not tested) and never a generated ID or facing."""
        src = "CameraManager.getCameraIdList()"
        probe = _app_rec(props, "camera_probe") if _app_collected(props) else None
        if id_rec and id_rec.get("state") == RuntimeState.AVAILABLE.value:
            base = _make("camera_availability", RuntimeState.UNAVAILABLE.value, is_real=is_real, source=src,
                         verification_method="camera_id_list_check", evidence_ref=f"{APP_EVIDENCE}#camera_id_list",
                         notes="getCameraIdList() returned no camera.")
        elif id_rec or probe:
            rec = id_rec or probe
            base = _app_result(props, "camera_availability", record=rec,
                               anchor="camera_id_list" if id_rec else "camera_probe", source=src,
                               verification_method="camera_id_list_check")
            if base.state == RuntimeState.ERROR.value and not base.error_message:
                base.error_message = "Android app camera probe failed"
        elif props.get("probe_error_camera"):
            base = _make("camera_availability", RuntimeState.ERROR.value, is_real=is_real, source=src,
                         verification_method="camera_id_list_check", evidence_ref=f"{COMMANDS_LOG}#probe_error_camera",
                         error_message=props["probe_error_camera"])
        else:
            base = _app_result(props, "camera_id_list", record_name="camera_availability", source=src,
                               verification_method="camera_id_list_check")
        results = [base]
        # When the camera probe as a whole was attempted and failed (ERROR), or the camera service/cameras are
        # absent (UNAVAILABLE) or refused (PERMISSION_REQUIRED), every per-camera check inherits that state and its
        # evidence (P5-03). Only when nothing was attempted do they stay NOT_TESTED.
        inherited = base.state in (RuntimeState.ERROR.value, RuntimeState.UNAVAILABLE.value,
                                   RuntimeState.PERMISSION_REQUIRED.value)

        def dependent(metric: str, source: str, unit: Optional[str], method: str) -> CapabilityResult:
            if inherited:
                return _make(metric, base.state, is_real=is_real, source=source, unit=unit, verification_method=method,
                             evidence_ref=base.evidence_ref, error_message=base.error_message,
                             notes=_join_notes("Inherited from the camera probe (no camera ID observed).", base.notes))
            return _make(metric, RuntimeState.NOT_TESTED.value, is_real=is_real, source=source, unit=unit,
                         verification_method=method, notes="No camera ID was observed, so no per-camera check ran.")

        for metric, source, unit in self.PER_CAMERA_METRICS:
            results.append(dependent(metric, source, unit, "camera_characteristics_check"))
        honoured = dependent("manual_control_honoured", "CaptureResult advertised-vs-honoured check", None,
                             "capture_result_honoured_check")
        return CameraCapability(camera_id="UNIDENTIFIED", lens_facing=None, results=results,
                                manual_control_honoured=honoured)

    # -- one identified camera -----------------------------------------------------------------------------
    def _camera(self, props: Dict[str, Any], cid: str, is_real: bool) -> CameraCapability:
        recs = (props.get("app_camera_records") or {}).get(cid, {})
        host = (props.get("host_camera_dumpsys") or {}).get(cid)

        def app_metric(metric: str, source: str, unit: Optional[str] = None, **kw: Any) -> CapabilityResult:
            return _app_result(props, metric, record=recs.get(metric), anchor=f"camera_telemetry/{cid}/{metric}",
                               source=f"{source} (ID {cid})", verification_method="camera_characteristics_check",
                               unit=unit, **kw)

        facing = app_metric("lens_facing", "CameraCharacteristics.LENS_FACING")
        if facing.state == RuntimeState.AVAILABLE.value and host and host.get("lens_facing"):
            agree = host["lens_facing"] == facing.value
            facing.notes = _join_notes(facing.notes, f"Host dumpsys cross-check: {host['lens_facing']} "
                                                     f"({'agrees' if agree else 'DISAGREES'}).")
        results = [facing]
        for metric, source, unit in self.PER_CAMERA_METRICS:
            res = app_metric(metric, source, unit)
            if metric == "manual_exposure_advertised" and res.state == RuntimeState.AVAILABLE.value and res.value is not True:
                # "Not advertised" is UNAVAILABLE, never AVAILABLE with a false value.
                res = _make(metric, RuntimeState.UNAVAILABLE.value, is_real=is_real, source=res.source,
                            verification_method=res.verification_method,
                            evidence_ref=f"{APP_EVIDENCE}#camera_telemetry/{cid}/{metric}",
                            notes="MANUAL_SENSOR is not advertised.")
            if metric == "available_capabilities" and res.state == RuntimeState.AVAILABLE.value and host \
                    and host.get("available_capabilities"):
                res.notes = _join_notes(res.notes, f"Host dumpsys cross-check lists: {host['available_capabilities']}.")
            results.append(res)
        advertised = next(r for r in results if r.metric == "manual_exposure_advertised")
        honoured = self._honoured(props, cid, recs.get("manual_control_honoured"), advertised, is_real)
        return CameraCapability(camera_id=cid,
                                lens_facing=facing.value if facing.state == RuntimeState.AVAILABLE.value else None,
                                results=results, manual_control_honoured=honoured)

    def _honoured(self, props: Dict[str, Any], cid: str, rec: Optional[Dict[str, Any]],
                  advertised: CapabilityResult, is_real: bool) -> CapabilityResult:
        metric = "manual_control_honoured"
        ref = f"{APP_EVIDENCE}#camera_telemetry/{cid}/{metric}"
        common = dict(is_real=is_real, source=f"CaptureResult vs requested manual exposure/sensitivity (ID {cid})",
                      verification_method="capture_result_honoured_check")
        if rec is None or rec.get("state") != RuntimeState.AVAILABLE.value:
            res = _app_result(props, metric, record=rec, anchor=f"camera_telemetry/{cid}/{metric}",
                              source=common["source"], verification_method=common["verification_method"])
            if res.state == RuntimeState.UNAVAILABLE.value and advertised.state != RuntimeState.AVAILABLE.value:
                res.notes = _join_notes(res.notes, "Manual control is not advertised, so it is not honoured.")
            return res
        if advertised.state != RuntimeState.AVAILABLE.value:
            return _make(metric, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                         error_message="Capture check reported although MANUAL_SENSOR is not advertised (inconsistent).")
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        keys = ("requested_exposure_time_ns", "reported_exposure_time_ns", "requested_sensitivity", "reported_sensitivity")
        if not all(isinstance(v.get(k), (int, float)) and not isinstance(v.get(k), bool) for k in keys):
            return _make(metric, RuntimeState.ERROR.value, evidence_ref=ref, **common,
                         error_message="Capture check record lacks requested/reported exposure and sensitivity values.")
        exp_tol = self.check_cfg["exposure_time_relative_tolerance"]
        iso_tol = self.check_cfg["sensitivity_relative_tolerance"]

        def within(req: float, rep: float, tol: float) -> bool:
            return req > 0 and abs(rep - req) <= tol * req

        exp_ok = within(v["requested_exposure_time_ns"], v["reported_exposure_time_ns"], exp_tol)
        iso_ok = within(v["requested_sensitivity"], v["reported_sensitivity"], iso_tol)
        detail = (f"exposure requested {v['requested_exposure_time_ns']} ns, reported {v['reported_exposure_time_ns']} ns; "
                  f"sensitivity requested {v['requested_sensitivity']}, reported {v['reported_sensitivity']} "
                  f"(tolerances: exposure {exp_tol}, sensitivity {iso_tol}).")
        if exp_ok and iso_ok:
            return _make(metric, RuntimeState.AVAILABLE.value, value="CaptureResult matched the requested manual "
                         "exposure time and sensitivity", evidence_ref=ref, notes=detail, **common)
        return _make(metric, RuntimeState.UNAVAILABLE.value, evidence_ref=ref, **common,
                     notes=f"Advertised but NOT HONOURED: {detail}")


def _load_camera_check_config() -> Dict[str, Any]:
    import yaml  # local import: only needed when no explicit settings are passed
    cfg_path = Path(__file__).resolve().parents[3] / "configs" / "device_characterization.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    check = cfg.get("camera_manual_control_check")
    if not isinstance(check, dict):
        raise ValueError("configs/device_characterization.yaml lacks camera_manual_control_check")
    return check


def _load_backend_check_config() -> Dict[str, Any]:
    import yaml  # local import: only needed when no explicit settings are passed
    cfg_path = Path(__file__).resolve().parents[3] / "configs" / "device_characterization.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    check = cfg.get("inference_backend_check")
    if not isinstance(check, dict):
        raise ValueError("configs/device_characterization.yaml lacks inference_backend_check")
    return check


def validate_backend_check_config(check: Dict[str, Any]) -> None:
    """Rejects an incomplete `inference_backend_check` block instead of defaulting any researcher parameter."""
    from src.monitoring.characterization import reference_graph as rg
    backends = check.get("backends")
    if not isinstance(backends, dict) or not backends:
        raise ValueError("inference_backend_check.backends must list the approved backends")
    for name, spec in backends.items():
        if not isinstance(spec, dict) or spec.get("artifact_format") not in rg.FORMATS or not spec.get("requested_delegate"):
            raise ValueError(f"inference_backend_check.backends.{name} needs artifact_format (tflite/onnx) and requested_delegate")
    variants = [check.get("primary_variant")] + list(check.get("quantization_variants") or [])
    if not set(variants) <= set(rg.VARIANTS) or len(set(variants)) != len(variants):
        raise ValueError(f"inference_backend_check variants must be distinct members of {rg.VARIANTS}")
    if not isinstance((check.get("reference_graph") or {}).get("artifacts"), dict):
        raise ValueError("inference_backend_check.reference_graph.artifacts (pinned SHA-256) is required")
    rules = check.get("output_validation") or {}
    needed = {"float": ("max_abs_error", "probability_sum_tolerance"),
              "int8": ("output_scale", "max_abs_error_lsb", "probability_sum_tolerance_lsb")}
    for cls, keys in needed.items():
        for k in keys:
            v = (rules.get(cls) or {}).get(k)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0:
                raise ValueError(f"inference_backend_check.output_validation.{cls}.{k} must be a non-negative number")


# A TFLite/NNAPI accelerator cannot be identified through the Java APIs (device enumeration needs the NDK, API 29).
NNAPI_LIMITATION = ("NNAPI accelerator identity is not observable through the Java APIs (device enumeration needs the "
                    "NDK, API >= 29); below API 29 the NNAPI CPU reference implementation cannot be excluded.")


class InferenceBackendCapabilityCollector:
    """Collector 9: InferenceBackendCapabilityCollector (protocol §4 P4, §5.4, §5.5; matrix §5).

    Capability only: NO latency, accuracy or throughput is measured or reported. The Android app
    (BackendProbes.kt) reports raw observations per backend; this collector decides every status:
    - availability: runtime library initialised and the requested delegate/provider constructed or listed;
    - graph_load / inference_execution: the pinned reference graph (SHA-256 checked) loaded / executed once;
    - probability_output: the single output-validity rule (reference_graph.validate_output, config tolerances);
    - delegation: the requested delegate/provider observed active (TFLite execution-plan length below the graph
      node count; ONNX Runtime profile kernels executed by the requested provider). Accepting a delegate is never
      taken as delegation; an unobservable delegation is NOT_TESTED;
    - quantization_support: one record per quantization variant (load + inference + valid output).
    Scope, graph identity and tolerances come from configs/device_characterization.yaml (inference_backend_check).
    """

    def __init__(self, check_config: Optional[Dict[str, Any]] = None):
        self.cfg = check_config if check_config is not None else _load_backend_check_config()
        validate_backend_check_config(self.cfg)

    def collect(self, backend_props: Optional[Dict[str, Any]] = None) -> List[BackendCapability]:
        props = backend_props or {}
        return [self._backend(props, name, spec) for name, spec in self.cfg["backends"].items()]

    # ------------------------------------------------------------------
    def _backend(self, props: Dict[str, Any], name: str, spec: Dict[str, Any]) -> BackendCapability:
        is_real = bool(props.get("is_real_device_observation", False))
        recs = (props.get("app_backend_records") or {}).get(name)
        recs = recs if isinstance(recs, dict) else {}
        base = f"backend_capability/{name}"
        primary = self.cfg["primary_variant"]
        limitations: List[str] = []
        if spec["requested_delegate"] in ("NNAPI", "NnapiExecutionProvider"):
            limitations.append(NNAPI_LIMITATION)
        if spec["artifact_format"] == "tflite":
            limitations.append("TFLite delegation is observed through the execution-plan length: it shows that nodes "
                               "were delegated, but not the exact delegated-node or partition count.")

        availability, runtime_info = self._availability(props, name, spec, recs.get("backend_runtime"), base)
        runtime_version = runtime_info.get("runtime_version") if runtime_info else None
        if availability.state == RuntimeState.AVAILABLE.value and runtime_version is None:
            limitations.append("Runtime version not reported by the runtime (recorded as null, not inferred).")

        evaluated = {v: self._variant(props, name, spec, v, recs, base, is_real)
                     for v in [primary] + list(self.cfg["quantization_variants"])}
        main = evaluated[primary]
        quant = [self._quantization(v, evaluated[v], is_real) for v in self.cfg["quantization_variants"]]
        return BackendCapability(
            backend=name,
            availability=availability,
            graph_load=main["load"],
            inference_execution=main["inference"],
            probability_output=main["output"],
            delegation=main["delegation"],
            quantization_support=quant,
            runtime_version=runtime_version,
            runtime_version_source=runtime_info.get("runtime_version_source") if runtime_info else None,
            reference_graph_hash=main["artifact"].get("sha256_reported") if main["artifact"].get("match") else None,
            reference_graph_artifacts={v: e["artifact"] for v, e in evaluated.items()},
            delegation_evidence={v: e["evidence"] for v, e in evaluated.items()},
            known_limitations=limitations,
        )

    def _availability(self, props, name, spec, rec, base) -> Tuple[CapabilityResult, Optional[Dict[str, Any]]]:
        source = f"Runtime library initialisation and delegate/provider construction ({name})"
        res = _app_result(props, "backend_runtime", record=rec, anchor=f"{base}/backend_runtime",
                          source=source, verification_method="backend_init_check", record_name="backend_availability")
        if res.state != RuntimeState.AVAILABLE.value:
            return res, None
        info = res.value if isinstance(res.value, dict) else {}
        if info.get("requested_delegate") != spec["requested_delegate"]:
            return _make("backend_availability", RuntimeState.ERROR.value, is_real=True, source=source,
                         verification_method="backend_init_check", evidence_ref=res.evidence_ref,
                         error_message=f"App requested delegate {info.get('requested_delegate')!r}, config expects "
                                       f"{spec['requested_delegate']!r}."), None
        version = info.get("runtime_version") or "version not reported"
        detail = {"GPU": f"GPU delegate constructed (compatibility list: {info.get('gpu_compatibility_list_supported')})",
                  "NNAPI": "NNAPI delegate constructed",
                  "NnapiExecutionProvider": f"NNAPI listed by the runtime ({info.get('available_providers')})"}
        value = f"{spec.get('runtime_family', name)} {version} initialised"
        if spec["requested_delegate"] in detail:
            value += f"; {detail[spec['requested_delegate']]}"
        res.value = value + " (delegation is verified separately)."
        res.notes = _join_notes(res.notes, f"Declared dependency: {info.get('declared_dependency')}.")
        return res, info

    def _variant(self, props, name, spec, variant, recs, base, is_real) -> Dict[str, Any]:
        from src.monitoring.characterization import reference_graph as rg
        fmt = spec["artifact_format"]
        artifact = rg.artifact_name(fmt, variant)
        pinned = self.cfg["reference_graph"]["artifacts"]
        anchor = f"{base}/reference_graph_check/{variant}"
        ref = f"{APP_EVIDENCE}#{anchor}"
        tag = f"{name}, {variant}"
        art: Dict[str, Any] = {"artifact": artifact, "sha256_pinned": pinned.get(artifact), "sha256_reported": None,
                               "match": None}
        ev: Dict[str, Any] = {"requested_backend": name, "requested_delegate": spec["requested_delegate"],
                              "mechanism": None, "observed": None, "delegated": None, "cpu_fallback": None,
                              "partitions": None, "evidence_ref": None}

        def mk(metric, state, method, value=None, notes=None, error=None, verifiable=True):
            return _make(metric, state, is_real=is_real, source=f"Reference graph {artifact} ({tag})",
                         verification_method=method, value=value, evidence_ref=ref, notes=notes,
                         error_message=error, verifiable=verifiable)

        def not_reached(metric, method, why):
            return mk(metric, RuntimeState.NOT_TESTED.value, method, notes=f"Not evaluated: {why}.")

        rec = recs.get(f"reference_graph_check/{variant}")
        gate = _app_result(props, "reference_graph_check", record=rec, anchor=anchor,
                           source=f"Reference graph {artifact} ({tag})", verification_method="reference_graph_load_check",
                           record_name="graph_load")
        out = {"artifact": art, "evidence": ev}
        if gate.state != RuntimeState.AVAILABLE.value:
            out.update(load=gate,
                       inference=_retag(gate, "inference_execution", "reference_graph_inference_check"),
                       output=_retag(gate, "probability_output_validity", "reference_graph_output_check"),
                       delegation=_retag(gate, "backend_delegation", "delegation_observation"))
            ev["evidence_ref"] = gate.evidence_ref
            return out
        val = gate.value if isinstance(gate.value, dict) else {}
        ev["evidence_ref"] = ref
        art["sha256_reported"] = val.get("artifact_sha256")
        art["match"] = (val.get("artifact") == artifact and val.get("artifact_sha256") == pinned.get(artifact)
                        and val.get("manifest_sha256") == pinned.get(rg.MANIFEST_NAME))
        expected_nodes = rg.graph_node_counts()[fmt][variant]
        mismatch = None
        if not art["match"]:
            mismatch = (f"artifact identity mismatch: app loaded {val.get('artifact')} sha256 {val.get('artifact_sha256')} "
                        f"(manifest {val.get('manifest_sha256')}); pinned {pinned.get(artifact)}")
        elif val.get("requested_backend") != name or val.get("requested_delegate") != spec["requested_delegate"]:
            mismatch = (f"app ran backend {val.get('requested_backend')!r} / delegate {val.get('requested_delegate')!r}; "
                        f"config expects {name!r} / {spec['requested_delegate']!r}")
        elif (val.get("delegation") or {}).get("graph_node_count") not in (None, expected_nodes):
            mismatch = f"app graph node count {(val.get('delegation') or {}).get('graph_node_count')} != {expected_nodes}"
        if mismatch:
            out.update(load=mk("graph_load", RuntimeState.ERROR.value, "reference_graph_load_check", error=mismatch),
                       inference=not_reached("inference_execution", "reference_graph_inference_check", mismatch),
                       output=not_reached("probability_output_validity", "reference_graph_output_check", mismatch),
                       delegation=not_reached("backend_delegation", "delegation_observation", mismatch))
            return out

        load, infer = val.get("load") or {}, val.get("inference") or {}
        if load.get("ok") is True:
            out["load"] = mk("graph_load", RuntimeState.AVAILABLE.value, "reference_graph_load_check",
                             value=f"{artifact} (sha256 {art['sha256_reported']}) loaded with {spec['requested_delegate']} requested")
        else:
            out["load"] = mk("graph_load", RuntimeState.ERROR.value, "reference_graph_load_check",
                             error=load.get("error") or "graph load not reported (inconsistent app output)")
        if out["load"].state != RuntimeState.AVAILABLE.value:
            out["inference"] = not_reached("inference_execution", "reference_graph_inference_check", "graph did not load")
        elif infer.get("ok") is True:
            out["inference"] = mk("inference_execution", RuntimeState.AVAILABLE.value, "reference_graph_inference_check",
                                  value="One inference on the deterministic manifest input completed",
                                  notes="Capability check only; no latency, throughput or accuracy recorded.")
        else:
            out["inference"] = mk("inference_execution", RuntimeState.ERROR.value, "reference_graph_inference_check",
                                  error=infer.get("error") or "inference not reported (inconsistent app output)")

        if out["inference"].state != RuntimeState.AVAILABLE.value:
            out["output"] = not_reached("probability_output_validity", "reference_graph_output_check", "inference did not run")
        else:
            ok, problems, measured = rg.validate_output(val.get("output"), variant, self.cfg["output_validation"])
            summary = (f"{measured.get('rule')}; measured max abs error {measured.get('max_abs_error')}, "
                       f"probability sum {measured.get('probability_sum')}")
            if ok:
                out["output"] = mk("probability_output_validity", RuntimeState.AVAILABLE.value,
                                   "reference_graph_output_check", value="Valid probability output: shape [1, 4], finite, "
                                   "in [0, 1], sum and values within tolerance of the float64 reference", notes=summary)
            else:
                out["output"] = mk("probability_output_validity", RuntimeState.UNAVAILABLE.value,
                                   "reference_graph_output_check", notes="Output INVALID: " + "; ".join(problems) + f" ({summary}).")

        out["delegation"] = self._delegation(spec, val, out, ev, mk, not_reached, expected_nodes)
        return out

    def _delegation(self, spec, val, out, ev, mk, not_reached, expected_nodes) -> CapabilityResult:
        d = val.get("delegation") or {}
        requested = spec["requested_delegate"]
        nnapi = requested in ("NNAPI", "NnapiExecutionProvider")
        method = "delegation_observation"
        ev["mechanism"] = d.get("mechanism")
        for k in ("nnapi_errno", "nnapi_has_errors", "log_lines"):
            if k in d:
                ev[k] = d[k]
        if out["load"].state != RuntimeState.AVAILABLE.value:
            return not_reached("backend_delegation", method, "graph did not load")
        verifiable = not nnapi
        note_nnapi = NNAPI_LIMITATION if nnapi else None
        if d.get("mechanism") == "tflite_execution_plan_length":
            plan = d.get("execution_plan_length")
            ev.update(graph_node_count=expected_nodes, execution_plan_length=plan)
            if not isinstance(plan, int) or isinstance(plan, bool):
                return mk("backend_delegation", RuntimeState.NOT_TESTED.value, method,
                          notes="Delegation not observable: execution-plan length unavailable "
                                f"({d.get('execution_plan_error') or 'not reported'}).")
            if plan < expected_nodes:
                ev.update(observed=requested, delegated=True, cpu_fallback=False if plan == 1 else None)
                shape = ("all nodes in one delegate kernel (no CPU fallback)" if plan == 1 else
                         f"{plan} plan entries: several partitions or CPU-fallback nodes (not distinguishable)")
                return mk("backend_delegation", RuntimeState.AVAILABLE.value, method, verifiable=verifiable,
                          value=f"{requested} active: execution plan {plan} entr{'y' if plan == 1 else 'ies'} for a "
                                f"{expected_nodes}-node graph; {shape}", notes=note_nnapi)
            ev.update(observed="none observed", delegated=False, cpu_fallback=True)
            return mk("backend_delegation", RuntimeState.UNAVAILABLE.value, method,
                      notes=f"{requested} took no multi-node partition: execution plan length {plan} = graph node "
                            f"count {expected_nodes}. A single-node delegate partition cannot be distinguished from "
                            "CPU execution by this measure.")
        if d.get("mechanism") == "ort_profile_node_provider":
            kernels = d.get("kernels")
            if out["inference"].state != RuntimeState.AVAILABLE.value:
                return not_reached("backend_delegation", method, "inference did not run, so no kernel was profiled")
            if not isinstance(kernels, list) or not kernels:
                return mk("backend_delegation", RuntimeState.NOT_TESTED.value, method,
                          notes=f"Delegation not observable: no profiled kernel ({d.get('profile_error') or 'empty profile'}).")
            by_provider: Dict[str, int] = {}
            for k in kernels:
                p = (k or {}).get("provider")
                by_provider[str(p)] = by_provider.get(str(p), 0) + 1
            n_req = by_provider.get(requested, 0)
            others = {p: n for p, n in by_provider.items() if p != requested}
            ev.update(kernels_by_provider=by_provider, observed=sorted(by_provider), delegated=n_req > 0,
                      cpu_fallback=bool(others), partitions=n_req if nnapi else None)
            if n_req:
                fb = f"; other providers: {others}" if others else "; no other provider executed a kernel"
                return mk("backend_delegation", RuntimeState.AVAILABLE.value, method, verifiable=verifiable,
                          value=f"{requested} executed {n_req} of {sum(by_provider.values())} profiled kernel(s){fb}",
                          notes=note_nnapi)
            return mk("backend_delegation", RuntimeState.UNAVAILABLE.value, method,
                      notes=f"No profiled kernel ran on {requested}; executed providers: {by_provider}.")
        return mk("backend_delegation", RuntimeState.ERROR.value, method,
                  error=f"Unknown or missing delegation mechanism {d.get('mechanism')!r} (inconsistent app output).")

    @staticmethod
    def _quantization(variant: str, e: Dict[str, Any], is_real: bool) -> CapabilityResult:
        metric = f"quantization_{variant}"
        for stage in ("load", "inference", "output"):
            r: CapabilityResult = e[stage]
            if r.state != RuntimeState.AVAILABLE.value:
                return _retag(r, metric, "reference_graph_variant_check",
                              notes=f"{variant} variant: {stage} stage is {r.state}.")
        d = e["delegation"]
        return _make(metric, RuntimeState.AVAILABLE.value, is_real=is_real, source=e["output"].source,
                     verification_method="reference_graph_variant_check", evidence_ref=e["output"].evidence_ref,
                     value=f"{variant} variant loaded, executed and produced a valid output",
                     notes=f"Delegation for this variant: {d.state} ({d.value or d.notes or d.error_message}).")


def _retag(r: CapabilityResult, metric: str, method: str, notes: Optional[str] = None) -> CapabilityResult:
    """Copy of a non-AVAILABLE record under another metric name (same state, evidence and messages)."""
    return CapabilityResult(metric=metric, state=r.state, report_status=r.report_status, value=None, unit=None,
                            source=r.source, min_api=r.min_api, condition=r.condition, verified=False,
                            verification_method=method, evidence_ref=r.evidence_ref, observed_at=r.observed_at,
                            error_message=r.error_message, notes=_join_notes(r.notes, notes))


class ProfilingCapabilityCollector:
    """Collector 10: ProfilingCapabilityCollector.
    Checks clock sources, timer overhead, Android Trace API, ADB tracing availability.
    """

    def collect(self, profiling_props: Optional[Dict[str, Any]] = None) -> List[CapabilityResult]:
        props = profiling_props or {}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        is_real = bool(props.get("is_real_device_observation", False))
        results: List[CapabilityResult] = []

        # Clock sources (B9): monotonicity, resolution and call overhead measured by the app. Clock
        # characterization only (protocol P5); not a benchmark and not a performance result.
        nano = _app_result(props, "system_nano_time",
                           source="System.nanoTime() / SystemClock.elapsedRealtimeNanos()",
                           verification_method="clock_source_check", unit="ns",
                           notes="Clock characterization only; no benchmark-quality precision is claimed.")
        if nano.state == RuntimeState.AVAILABLE.value:
            v = nano.value if isinstance(nano.value, dict) else {}
            clocks = [v.get(k) for k in ("system_nano_time", "elapsed_realtime_nanos")]
            if not all(isinstance(c, dict) and c.get("monotonic") is True for c in clocks):
                nano = _make("system_nano_time", RuntimeState.ERROR.value, is_real=is_real, unit="ns",
                             source=nano.source, verification_method=nano.verification_method,
                             evidence_ref=f"{APP_EVIDENCE}#system_nano_time",
                             error_message="Clock check did not report both clocks as monotonic.")
        results.append(nano)

        # android.os.Trace (B10): a successful API call establishes availability only. VERIFIED would require
        # the section to appear in a captured system trace, which is not performed here.
        results.append(_app_result(props, "android_trace_api",
                                   source="android.os.Trace.beginSection/endSection; Trace.isEnabled (API 29)",
                                   verification_method="trace_api_call_check", verifiable=False,
                                   notes="API call succeeded only; section visibility in a captured trace is not verified."))

        if "atrace_adb_available" not in props:
            state_atrace = RuntimeState.NOT_TESTED.value
            val_atrace = None
            cond_atrace = None
            ver_atrace = False
        else:
            atrace = props.get("atrace_adb_available")
            if atrace is True:
                state_atrace = RuntimeState.AVAILABLE.value
                val_atrace = "atrace category listing via ADB succeeded"
                cond_atrace = "HOST ADB SHELL"
                ver_atrace = False  # condition-gated, and a category listing is not a captured trace
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
            observed_at=now if (is_real and state_atrace != RuntimeState.NOT_TESTED.value) else None,
            evidence_ref="evidence/atrace_evidence.txt" if (is_real and state_atrace != RuntimeState.NOT_TESTED.value) else None,
            notes=("atrace --list_categories succeeded; capturing a trace across USB disconnection (D-16 B) "
                   "is not tested here." if state_atrace == RuntimeState.AVAILABLE.value else None),
        ))

        return results


class EnergyMeasurementCapabilityChecker:
    """Collector 11: EnergyMeasurementCapabilityChecker (protocol §6, D-16 hierarchy).

    - E-1 / E-2 are physical checks recorded by the researcher in the evidence file named by
      `energy_feasibility_evidence` (configs/device_characterization.yaml). Not assessed -> NOT_TESTED;
      assessed -> EXTERNAL_REQUIRED (REQUIRES EXTERNAL INSTRUMENTATION) citing that file. Never inferred.
    - E-3 is derived from the run's battery counter records (current now, charge counter, energy counter):
      a demonstrated counter -> AVAILABLE / REQUIRES PILOT VALIDATION (agreement, D-16); all unsupported ->
      UNAVAILABLE; otherwise NOT_TESTED.
    - selected_level follows energy_evidence.select_energy_level(): a preferred level is never skipped while it
      is unassessed, so software counters alone never select E-3; E-1 needs every E-1 requirement including the
      researcher's safety sign-off, E-2 every E-2 requirement including non-charging evidence. Absolute energy is
      never claimed.
    """

    COUNTER_METRICS = ("battery_current_now", "battery_charge_counter", "battery_energy_counter")

    def collect(self, energy_props: Optional[Dict[str, Any]] = None,
                battery_results: Optional[List[CapabilityResult]] = None) -> EnergyCapability:
        props = energy_props or {}
        is_real = bool(props.get("is_real_device_observation", False))
        evidence = props.get("energy_feasibility") or {}
        data = evidence.get("data") if isinstance(evidence, dict) else None
        errors = evidence.get("errors") if isinstance(evidence, dict) else None
        ev_ref = props.get("energy_feasibility_evidence_ref")

        e1 = self._level(
            "E1_battery_side_reference", data, errors, ev_ref,
            source="Researcher physical inspection: battery-side external reference (power analyser bypass)",
            describe=lambda d: (f"feasible={d.get('feasible')}, reference_validated={d.get('reference_validated')}, "
                                f"safety_signoff={d.get('safety_signoff')}, instrument={d.get('instrument_model')}; "
                                "unmet selection requirements: "
                                f"{unmet_selection_requirements('E1_battery_side_reference', d) or 'none'}"),
        )
        e2 = self._level(
            "E2_supply_powered_session", data, errors, ev_ref,
            source="Researcher session: external meter on a supply-powered session with charging excluded",
            describe=lambda d: (f"feasible={d.get('feasible')}, reference_validated={d.get('reference_validated')}, "
                                f"non_charging_verified={d.get('non_charging_verified')}, meter={d.get('meter_model')}; "
                                "unmet selection requirements: "
                                f"{unmet_selection_requirements('E2_supply_powered_session', d) or 'none'}"),
        )
        e3, e3_available = self._software_counters(battery_results, is_real)

        selected = select_energy_level(
            (data or {}).get("E1_battery_side_reference"), (data or {}).get("E2_supply_powered_session"), e3_available
        ) if data else None

        return EnergyCapability(
            E1_battery_side_reference=e1,
            E2_supply_powered_session=e2,
            E3_software_counters=e3,
            selected_level=selected,
            absolute_energy_claimed=False,  # FIXED FALSE
            selection_basis=selection_basis(data),
        )

    @staticmethod
    def _level(key: str, data: Optional[Dict[str, Any]], errors: Optional[List[str]], ev_ref: Optional[str],
               source: str, describe) -> CapabilityResult:
        common = dict(is_real=True, source=source, verification_method="researcher_feasibility_record")
        if errors:
            return _make(key, RuntimeState.ERROR.value, evidence_ref=ev_ref, **common,
                         error_message="Energy feasibility evidence file is invalid: " + "; ".join(errors))
        level = (data or {}).get(key)
        if not level:
            return _make(key, RuntimeState.NOT_TESTED.value, **common,
                         notes="No researcher energy-feasibility evidence configured (energy_feasibility_evidence: null).")
        if level.get("assessed") is not True:
            return _make(key, RuntimeState.NOT_TESTED.value, evidence_ref=ev_ref, **common,
                         notes="Researcher evidence file marks this level as not yet assessed.")
        return _make(key, RuntimeState.EXTERNAL_REQUIRED.value, evidence_ref=f"{ev_ref}#{key}" if ev_ref else None,
                     **common, notes=f"Assessed by {level.get('assessed_by')} on {level.get('assessed_on')}: {describe(level)}.")

    def _software_counters(self, battery_results: Optional[List[CapabilityResult]],
                           is_real: bool) -> Tuple[CapabilityResult, Optional[bool]]:
        source = "BatteryManager CURRENT_NOW / CHARGE_COUNTER / ENERGY_COUNTER (battery telemetry records)"
        common = dict(is_real=is_real, source=source, verification_method="software_counter_derivation")
        if not battery_results:
            return _make("E3_software_counters", RuntimeState.NOT_TESTED.value, **common,
                         notes="Battery counter records not available to this check."), None
        by_metric = {r.metric: r for r in battery_results if r.metric in self.COUNTER_METRICS}
        demonstrated = [r for r in by_metric.values()
                        if r.state == RuntimeState.AVAILABLE.value and r.value not in (0, 0.0, None)]
        if demonstrated:
            first = demonstrated[0]
            return _make("E3_software_counters", RuntimeState.AVAILABLE.value, is_real=is_real,
                         value=f"Software counters demonstrated: {', '.join(r.metric for r in demonstrated)}",
                         source=source, verification_method="software_counter_derivation",
                         evidence_ref=first.evidence_ref, pilot=True,
                         notes="Relative software comparison only; NO absolute energy claimed. Agreement with an "
                               "external reference: REQUIRES PILOT VALIDATION (D-16; threshold not yet decided)."), True
        states = {m: r.state for m, r in by_metric.items()}
        unsupported = (RuntimeState.UNAVAILABLE.value, RuntimeState.API_UNSUPPORTED.value)
        if len(by_metric) == len(self.COUNTER_METRICS) and all(st in unsupported for st in states.values()):
            ref = next((r.evidence_ref for r in by_metric.values() if r.evidence_ref), None)
            return _make("E3_software_counters", RuntimeState.UNAVAILABLE.value, evidence_ref=ref, **common,
                         notes=f"All software counters unsupported: {states}."), False
        return _make("E3_software_counters", RuntimeState.NOT_TESTED.value, **common,
                     notes=f"No software counter demonstrated yet; counter states: {states}."), None
