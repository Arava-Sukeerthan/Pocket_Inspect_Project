"""
Step 10D correction round (post NOT_TESTED audit): host probes, app -> host bridge, evidence integrity,
status mapping, D-16 energy hierarchy, §9 coverage and sign-off, historical-run protection.

Every end-to-end test drives the real pipeline (run_characterization -> ADB parser -> bridge -> collectors ->
validator -> sign-off) through a synthetic ADB transport. Synthetic values are test fixtures only; nothing here is
a device observation.
"""

import copy
import datetime
import json
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from scripts.device_characterization.adb_collector import ADBCollector, load_probe_config
from scripts.device_characterization.run_characterization import run_characterization
from src.monitoring.characterization import host_probes
from src.monitoring.characterization.collectors import (
    BatteryTelemetryCollector,
    CameraCapabilityCollector,
    EnergyMeasurementCapabilityChecker,
)
from src.monitoring.characterization.coverage import check_matrix_coverage, parse_matrix, load_coverage_config
from src.monitoring.characterization.energy_evidence import select_energy_level, validate_energy_evidence
from src.monitoring.characterization.models import (
    CapabilityResult,
    ReportStatus,
    RuntimeState,
    map_runtime_state_to_report_status,
)
from src.monitoring.characterization.report_generator import (
    CharacterizationReportGenerator,
    validate_characterization_record,
)
from src.monitoring.characterization.signoff import evaluate_step10d_signoff

CONFIG = Path("configs/device_characterization.yaml")
APP_EV = "evidence/android_app_evidence.json"


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------

def item(metric, state="AVAILABLE", value=None, unit=None, error_message=None, camera_id=None, notes=None):
    d = {"metric": metric, "state": state, "report_status": "AVAILABLE" if state == "AVAILABLE" else "UNAVAILABLE"}
    for k, v in (("value", value), ("unit", unit), ("error_message", error_message), ("camera_id", camera_id),
                 ("notes", notes)):
        if v is not None:
            d[k] = v
    return d


def camera_records(cid, facing="BACK", manual=True, honoured=None):
    recs = [
        item("lens_facing", value=facing, camera_id=cid),
        item("hardware_level", value=1, camera_id=cid),
        item("available_capabilities", value=["BACKWARD_COMPATIBLE"] + (["MANUAL_SENSOR"] if manual else []),
             camera_id=cid),
        (item("manual_exposure_advertised", value=True, camera_id=cid) if manual
         else item("manual_exposure_advertised", "UNAVAILABLE", camera_id=cid, notes="MANUAL_SENSOR is not advertised")),
        item("stream_configurations", value={"format_35": ["640x480"]}, camera_id=cid),
        item("ae_target_fps_ranges", value=[[15, 30]], camera_id=cid),
        item("af_available_modes", value=[0, 1], camera_id=cid),
        item("lens_min_focus_distance", value=10.0, camera_id=cid),
        item("exposure_time_range_ns", value=[100000, 400000000], camera_id=cid),
        item("sensitivity_range", value=[100, 1600], camera_id=cid),
        item("awb_available_modes", value=[0, 1], camera_id=cid),
        item("ae_lock_available", value=True, camera_id=cid),
        item("awb_lock_available", value=True, camera_id=cid),
        item("physical_camera_ids", value=[], camera_id=cid),
        item("video_profiles", value={"QUALITY_HIGH": True}, camera_id=cid),
        item("capture_sensor_timestamp", value=123456789, camera_id=cid),
    ]
    if honoured is not None:
        recs.append(dict(honoured, camera_id=cid))
    elif manual:
        recs.append(item("manual_control_honoured", camera_id=cid, value={
            "requested_exposure_time_ns": 16666666, "reported_exposure_time_ns": 16666666,
            "requested_sensitivity": 850, "reported_sensitivity": 850, "frames_compared": 5}))
    else:
        recs.append(item("manual_control_honoured", "UNAVAILABLE", camera_id=cid,
                         notes="MANUAL_SENSOR is not advertised"))
    return recs


def full_app(**overrides):
    """App report in the new (correction-round) format, as CharacterizationRunner.kt writes it."""
    app = {
        "run_id": "android_run_correction",
        "observed_at": "2026-10-07T12:00:00Z",
        "device_identity": [item("manufacturer", value="OPPO"), item("model", value="CPH1931"),
                            item("soc_model", "API_UNSUPPORTED"), item("storage_total_bytes", value=53687091200)],
        "memory_telemetry": [item("total_ram_mb", value=2642), item("available_memory_mb", value=900),
                             item("low_memory_flag", value=False), item("memory_threshold_mb", value=216),
                             item("app_heap_allocated_mb", value=3), item("app_pss_kb", value=24000)],
        "thermal_capability": [item("thermal_status_api", value=0), item("thermal_status_listener", value="ok")],
        "battery_telemetry": [item("battery_level_percent", value=80), item("battery_voltage", value=4100),
                              item("battery_temperature", value=30.0),
                              item("battery_property_current_now", value=-250000, unit="uA"),
                              item("battery_property_current_average", "UNAVAILABLE", notes="sentinel"),
                              item("battery_property_charge_counter", value=3500000, unit="uAh"),
                              item("battery_property_energy_counter", "UNAVAILABLE", notes="sentinel")],
        "service_capability": [item("service_PowerManager", value="ok"),
                               item("service_HardwarePropertiesManager", "PERMISSION_REQUIRED",
                                    error_message="SecurityException: not device owner"),
                               item("service_CameraManager", value="ok"), item("service_ActivityManager", value="ok"),
                               item("service_BatteryManager", value="ok"), item("power_save_mode", value=False)],
        "cpu_telemetry": [item("app_cpu_time", value=420)],
        "gpu_capability": [item("gpu_renderer", value={"renderer": "Adreno (TM) 610", "vendor": "Qualcomm",
                                                        "version": "OpenGL ES 3.2"}),
                           item("gpu_vulkan_support", value={"vulkan_hardware_version_encoded": 4198400})],
        "profiling_capability": [
            item("system_nano_time", value={"system_nano_time": {"monotonic": True},
                                            "elapsed_realtime_nanos": {"monotonic": True}}),
            item("android_trace_api", value={"section": "x", "is_enabled": False})],
        "camera_telemetry": [item("camera_id_list", value=["0", "1"]), item("camera_count", value=2)]
                            + camera_records("0", "BACK", manual=True) + camera_records("1", "FRONT", manual=False),
    }
    app.update(overrides)
    return app


GETPROP = ("[ro.product.manufacturer]: [OPPO]\n[ro.product.model]: [CPH1931]\n[ro.build.version.sdk]: [29]\n"
           "[ro.build.version.release]: [10]\n[ro.board.platform]: [trinket]\n"
           "[ro.build.version.security_patch]: [2020-09-05]\n[ro.build.fingerprint]: [OPPO/CPH1931/x:10/y/z:user]\n")
BATTERY = ("Current Battery Service state:\n  AC powered: false\n  USB powered: true\n  Charge counter: 3500000\n"
           "  status: 2\n  health: 2\n  present: true\n  level: 80\n  scale: 100\n  voltage: 4100\n"
           "  temperature: 300\n  technology: Li-poly\n")
CAMERA_DUMPSYS = ("== Camera device 0 static information: ==\n  Device static metadata:\n"
                  "      android.lens.facing (80005): byte[1]\n        [1 ]\n"
                  "      android.request.availableCapabilities (c000c): byte[2]\n        [BACKWARD_COMPATIBLE MANUAL_SENSOR ]\n")


def make_transport(app, responses=None, fail=()):
    responses = dict(responses or {})

    def transport(args):
        cmd = " ".join(args)
        for key, resp in responses.items():
            if key in cmd:
                return resp
        if any(f in cmd for f in fail):
            return 1, "", f"synthetic failure: {cmd}"
        if cmd == "shell getprop":
            return 0, GETPROP, ""
        if "/proc/meminfo" in cmd:
            return 0, "MemTotal:        2705408 kB\nMemAvailable:    921600 kB\n", ""
        if "/proc/cpuinfo" in cmd:
            return 0, "processor : 0\nprocessor : 1\nHardware : Qualcomm Technologies, Inc TRINKET\n", ""
        if "/proc/stat" in cmd:
            return 0, "cpu 1 2 3\n", ""
        if "ls /sys/devices/system/cpu/cpufreq" in cmd:
            return 0, "policy0\npolicy4\n", ""
        if "cpuinfo_max_freq" in cmd or "scaling_max_freq" in cmd or "scaling_cur_freq" in cmd:
            return 0, "1804800\n", ""
        if "gpuclk" in cmd:
            return 0, "600000000\n", ""
        if "gpubusy" in cmd:
            return 0, "     1234    56789\n", ""
        if "/proc/pressure/memory" in cmd:
            return 1, "", "cat: /proc/pressure/memory: No such file or directory"
        if "uname -r" in cmd:
            return 0, "4.14.117-perf+\n", ""
        if "dumpsys battery" in cmd:
            return 0, BATTERY, ""
        if "dumpsys SurfaceFlinger" in cmd:
            return 0, "GLES: Qualcomm, Adreno (TM) 610, OpenGL ES 3.2 V@415.0\n", ""
        if "dumpsys media.camera" in cmd:
            return 0, CAMERA_DUMPSYS, ""
        if "thermal_zone0/type" in cmd:
            return 0, "battery\n", ""
        if "thermal_zone0/temp" in cmd:
            return 0, "30000\n", ""
        if "dumpsys thermalservice" in cmd:
            return 0, "Thermal Status: 0\n", ""
        if "atrace" in cmd:
            return 0, "gfx - Graphics\n", ""
        if "airplane_mode_on" in cmd:
            return 0, "1\n", ""
        if "boot_id" in cmd:
            return 0, "synthetic_boot\n", ""
        if "run-as" in cmd:
            return (0, app, "") if isinstance(app, str) else (1, "", "run-as: package not debuggable")
        return 1, "", "No such file or directory"

    return transport


def run_pipeline(tmp_path, app=None, responses=None, fail=(), cfg_overrides=None, run_suffix="170000"):
    """Runs the real pipeline. `app`: dict (serialised), str (raw), or None (no app output)."""
    app_text = json.dumps(app if app is not None else full_app()) if not isinstance(app, str) else app
    if app == "MISSING":
        app_text = None
    cfg_path = CONFIG
    if cfg_overrides:
        cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
        cfg.update(cfg_overrides)
        cfg_path = tmp_path / "cfg.yaml"
        cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    adb = ADBCollector(device_id="SYNTHETIC_CORRECTION")
    run_id = f"run_{datetime.datetime.utcnow().strftime('%Y%m%d')}_{run_suffix}"
    with patch.object(adb, "_adb_cmd", side_effect=make_transport(app_text, responses, fail)):
        with patch("scripts.device_characterization.run_characterization.ADBCollector", return_value=adb):
            with patch.object(adb, "get_connection_status", return_value="CONNECTED"):
                out_dir, _ = run_characterization(cfg_path, run_id=run_id, overwrite=True,
                                                  results_dir=tmp_path / "results")
    data = json.loads((out_dir / "characterization.json").read_text(encoding="utf-8"))
    observed = json.loads((out_dir / "evidence" / "observed_props.json").read_text(encoding="utf-8"))
    return out_dir, data, observed


def records(data):
    """Flat {path: record} over every record in a run."""
    out = {}
    for r in data["device_identity"]["observed"]:
        out[f"identity/{r['metric']}"] = r
    out["identity/variant_check"] = data["device_identity"]["variant_check"]
    for t in data["telemetry"]:
        for r in t["results"]:
            out[f"{t['dimension']}/{r['metric']}"] = r
    th = data["thermal"]
    for k in ("thermal_status_api", "thermal_headroom_api", "frequency_capping_observable", "external_surface_probe"):
        out[f"thermal/{k}"] = th[k]
    for r in th["temperature_sources"]:
        out[f"thermal/{r['metric']}"] = r
    for cam in data["camera"]:
        for r in cam["results"] + [cam["manual_control_honoured"]]:
            out[f"camera/{cam['camera_id']}/{r['metric']}"] = r
    for b in data["backends"]:
        for k in ("availability", "delegation", "probability_output"):
            out[f"backend/{b['backend']}/{k}"] = b[k]
    for r in data["profiling"]:
        out[f"profiling/{r['metric']}"] = r
    for k in ("E1_battery_side_reference", "E2_supply_powered_session", "E3_software_counters"):
        out[f"energy/{k}"] = data["energy"][k]
    return out


@pytest.fixture(scope="module")
def full_run(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("full")
    return run_pipeline(tmp)


# ---------------------------------------------------------------------------
# A1 evidence integrity
# ---------------------------------------------------------------------------

def test_every_evidence_ref_in_a_full_run_names_an_existing_file(full_run):
    out_dir, data, _ = full_run
    refs = [r["evidence_ref"] for r in records(data).values() if r.get("evidence_ref")]
    assert refs, "a full synthetic run must carry evidence references"
    for ref in refs:
        assert (out_dir / ref.split("#")[0]).exists(), ref


def test_no_phantom_evidence_file_names_remain_in_collectors():
    src = Path("src/monitoring/characterization/collectors.py").read_text(encoding="utf-8")
    for phantom in ("memory_props.json", "cpu_props.json", "kgsl_evidence.txt", "battery_evidence.json",
                    "thermal_evidence.json", "profiling_evidence.json", "#lowMemory"):
        assert phantom not in src, phantom
    assert "camera_{cid}_evidence.json" not in src
    assert "backend_{b_name}_evidence.json" not in src


def test_dangling_evidence_ref_on_unverified_record_fails_validation(full_run, tmp_path):
    out_dir, data, _ = full_run
    bad = copy.deepcopy(data)
    rec = next(r for t in bad["telemetry"] for r in t["results"] if r["metric"] == "psi_memory_pressure")
    rec["evidence_ref"] = "evidence/does_not_exist.json"
    errors = validate_characterization_record(bad, output_dir=out_dir)
    assert any("does_not_exist.json" in e for e in errors)


def test_missing_new_evidence_file_is_detected_by_manifest(full_run):
    out_dir, data, _ = full_run
    victim = out_dir / "evidence" / "psi_memory_evidence.json"
    content = victim.read_bytes()
    try:
        victim.unlink()
        errors = validate_characterization_record(data, output_dir=out_dir)
        assert any("psi_memory_evidence.json" in e for e in errors)
    finally:
        victim.write_bytes(content)


def test_new_evidence_files_are_hashed_in_manifest(full_run):
    out_dir, _, _ = full_run
    manifest = json.loads((out_dir / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    paths = {e["relative_path"] for e in manifest}
    for name in ("cpufreq_policy_evidence.json", "gpu_busy_evidence.json", "psi_memory_evidence.json",
                 "gpu_renderer_evidence.txt", "camera_host_evidence.json"):
        assert f"evidence/{name}" in paths, name


# ---------------------------------------------------------------------------
# A2 app -> host bridge
# ---------------------------------------------------------------------------

def test_bridge_routes_every_new_app_metric_with_app_provenance(full_run):
    _, data, observed = full_run
    recs = records(data)
    for path, anchor in (
        ("identity/service_PowerManager", "service_PowerManager"),
        ("memory/low_memory_flag", "low_memory_flag"),
        ("memory/app_heap_allocated_mb", "app_heap_allocated_mb"),
        ("memory/app_pss_kb", "app_pss_kb"),
        ("cpu/app_cpu_time", "app_cpu_time"),
        ("profiling/system_nano_time", "system_nano_time"),
        ("profiling/android_trace_api", "android_trace_api"),
        ("thermal/thermal_status_listener", "thermal_status_listener"),
        ("identity/storage_total", "storage_total_bytes"),
    ):
        assert recs[path]["state"] == "AVAILABLE", path
        assert recs[path]["evidence_ref"] == f"{APP_EV}#{anchor}", path
    assert "app_unrecognised_items" not in observed


def test_bridge_reports_unrecognised_app_items_instead_of_dumping_them(tmp_path):
    app = full_app()
    app["cpu_telemetry"].append(item("made_up_metric", value=1))
    _, _, observed = run_pipeline(tmp_path, app)
    assert observed["app_unrecognised_items"] == ["cpu_telemetry/made_up_metric"]
    assert "made_up_metric" not in observed


def test_host_value_is_never_cited_as_app_evidence(full_run):
    _, data, _ = full_run
    recs = records(data)
    for path in ("cpu/cpu_scaling_cur_freq", "cpu/device_wide_cpu_utilization", "gpu/gpu_clock_hz",
                 "gpu/gpu_utilization", "memory/psi_memory_pressure", "profiling/adb_atrace_profiling",
                 "battery/battery_charging_state", "thermal/thermal_zones_sysfs", "identity/security_patch"):
        ref = recs[path].get("evidence_ref") or ""
        assert not ref.startswith(APP_EV), path


def test_app_output_error_is_error_not_not_tested(tmp_path):
    _, data, _ = run_pipeline(tmp_path, "{not json")
    recs = records(data)
    assert data["app_output_status"] == "APP_OUTPUT_ERROR"
    for path in ("memory/low_memory_flag", "cpu/app_cpu_time", "profiling/system_nano_time"):
        assert recs[path]["state"] == "ERROR", path
        assert recs[path]["value"] is None


def test_older_app_without_a_probe_stays_not_tested_with_explanation(tmp_path):
    app = full_app()
    app["cpu_telemetry"] = []
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["cpu/app_cpu_time"]
    assert rec["state"] == "NOT_TESTED" and rec["value"] is None
    assert "no 'app_cpu_time' record" in rec["notes"]


def test_app_available_without_value_is_error(tmp_path):
    app = full_app()
    app["cpu_telemetry"] = [item("app_cpu_time")]  # AVAILABLE, no value
    _, data, _ = run_pipeline(tmp_path, app)
    assert records(data)["cpu/app_cpu_time"]["state"] == "ERROR"


# ---------------------------------------------------------------------------
# A3/B2 battery
# ---------------------------------------------------------------------------

def test_dumpsys_charge_counter_is_parsed():
    parsed = ADBCollector(device_id="x").parse_dumpsys_battery(BATTERY)
    assert parsed["battery_charge_counter"] == 3500000
    assert parsed["battery_health_code"] == 2
    assert "current now" not in parsed["battery_dumpsys_fields"]


def test_malformed_charge_counter_is_error():
    parsed = ADBCollector(device_id="x").parse_dumpsys_battery("  Charge counter: abc\n  level: 50\n")
    assert "battery_charge_counter" not in parsed
    res = next(r for r in BatteryTelemetryCollector().collect(dict(parsed, is_real_device_observation=True)).results
               if r.metric == "battery_charge_counter")
    assert res.state == "ERROR" and res.value is None


def test_charge_counter_from_dumpsys_when_app_has_no_property(tmp_path):
    app = full_app()
    app["battery_telemetry"] = [r for r in app["battery_telemetry"] if r["metric"] != "battery_property_charge_counter"]
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["battery/battery_charge_counter"]
    assert rec["state"] == "AVAILABLE" and rec["value"] == 3500000
    assert rec["report_status"] == "REQUIRES PILOT VALIDATION" and rec["verified"] is False
    assert rec["evidence_ref"] == "evidence/battery_dumpsys_evidence.txt#Charge counter"


def test_current_now_absent_from_dumpsys_and_app_is_explicit_not_tested(tmp_path):
    app = full_app()
    app["battery_telemetry"] = [r for r in app["battery_telemetry"] if r["metric"] != "battery_property_current_now"]
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["battery/battery_current_now"]
    assert rec["state"] == "NOT_TESTED" and rec["value"] is None
    assert "does not print 'current now'" in rec["notes"]
    assert rec["evidence_ref"] == "evidence/battery_dumpsys_evidence.txt"


def test_app_current_now_is_pilot_validation_not_verified(full_run):
    rec = records(full_run[1])["battery/battery_current_now"]
    assert rec["state"] == "AVAILABLE" and rec["value"] == -250.0 and rec["unit"] == "mA"
    assert rec["report_status"] == "REQUIRES PILOT VALIDATION" and rec["verified"] is False
    assert rec["evidence_ref"] == f"{APP_EV}#battery_property_current_now"


def test_batterymanager_unsupported_sentinel_is_unavailable_without_value(full_run):
    recs = records(full_run[1])
    for path in ("battery/battery_current_average", "battery/battery_energy_counter"):
        assert recs[path]["state"] == "UNAVAILABLE" and recs[path]["value"] is None, path
        assert recs[path]["report_status"] == "UNAVAILABLE"


def test_zero_charge_counter_is_not_verified(tmp_path):
    app = full_app()
    app["battery_telemetry"] = [r if r["metric"] != "battery_property_charge_counter" else
                                item("battery_property_charge_counter", value=0) for r in app["battery_telemetry"]]
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["battery/battery_charge_counter"]
    assert rec["value"] == 0 and rec["verified"] is False and rec["report_status"] == "AVAILABLE"


def test_temperature_battery_is_derived_from_battery_temperature(full_run):
    recs = records(full_run[1])
    assert recs["thermal/temperature_battery"]["state"] == "AVAILABLE"
    assert recs["thermal/temperature_battery"]["evidence_ref"] == recs["battery/battery_temperature"]["evidence_ref"]


def test_battery_status_and_health_are_not_defaulted_when_absent(tmp_path):
    _, data, _ = run_pipeline(tmp_path, full_app(), responses={"dumpsys battery": (0, "  level: 80\n  voltage: 4100\n", "")})
    recs = records(data)
    assert recs["battery/battery_charging_state"]["state"] == "UNAVAILABLE"
    assert recs["battery/battery_health_status"]["state"] == "UNAVAILABLE"
    assert recs["battery/battery_charging_state"]["value"] is None


# ---------------------------------------------------------------------------
# A5 PSI / A6 gpubusy / A7 cpufreq: outcomes are distinguished
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("code, out, err, expected", [
    (0, "some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n", "",
     "READABLE"),
    (1, "", "cat: /proc/pressure/memory: No such file or directory", "ABSENT"),
    (1, "", "cat: /proc/pressure/memory: Permission denied", "PERMISSION_DENIED"),
    (1, "", "error: device offline", "ERROR"),
    (0, "", "", "ERROR"),
])
def test_shell_read_outcome_classification(code, out, err, expected):
    assert host_probes.classify_shell_read(code, out, err) == expected


@pytest.mark.parametrize("resp, state, report", [
    ((0, "some avg10=0.00 avg60=0.00 avg300=0.00 total=0\n", ""), "AVAILABLE", "CONDITIONALLY AVAILABLE"),
    ((1, "", "cat: /proc/pressure/memory: No such file or directory"), "UNAVAILABLE", "UNAVAILABLE"),
    ((1, "", "cat: /proc/pressure/memory: Permission denied"), "PERMISSION_REQUIRED", "UNAVAILABLE"),
    ((1, "", "error: closed"), "ERROR", "NOT YET VERIFIED"),
    ((0, "garbage\n", ""), "ERROR", "NOT YET VERIFIED"),
])
def test_psi_states_e2e(tmp_path, resp, state, report):
    out_dir, data, _ = run_pipeline(tmp_path, full_app(), responses={"/proc/pressure/memory": resp})
    rec = records(data)["memory/psi_memory_pressure"]
    assert rec["state"] == state and rec["report_status"] == report
    assert rec["evidence_ref"] == "evidence/psi_memory_evidence.json"
    ev = json.loads((out_dir / "evidence" / "psi_memory_evidence.json").read_text(encoding="utf-8"))
    assert ev["psi"]["stderr"] == resp[2]  # raw stderr preserved
    assert ev["kernel_release"]["stdout"].strip() == "4.14.117-perf+"
    if state != "AVAILABLE":
        assert rec["value"] is None


@pytest.mark.parametrize("resp, state", [
    ((0, " 1234  56789\n", ""), "AVAILABLE"),
    ((1, "", "No such file or directory"), "UNAVAILABLE"),
    ((1, "", "Permission denied"), "PERMISSION_REQUIRED"),
    ((0, "not two counters\n", ""), "ERROR"),
])
def test_gpubusy_states_e2e(tmp_path, resp, state):
    _, data, _ = run_pipeline(tmp_path, full_app(), responses={"gpubusy": resp})
    rec = records(data)["gpu/gpu_utilization"]
    assert rec["state"] == state
    if state == "AVAILABLE":
        assert rec["report_status"] == "CONDITIONALLY AVAILABLE" and rec["condition"] == "HOST ADB SHELL"
        assert rec["value"] == "kgsl gpubusy counters readable"  # never a utilisation percentage
        assert "REQUIRES PILOT VALIDATION" in rec["notes"]
    else:
        assert rec["value"] is None


def test_cpufreq_policies_give_observability_without_throttling_claim(full_run):
    recs = records(full_run[1])
    cap = recs["thermal/frequency_capping_observable"]
    assert cap["state"] == "AVAILABLE" and cap["report_status"] == "CONDITIONALLY AVAILABLE"
    assert "drop" not in str(cap["value"]).lower() and "throttl" not in str(cap["value"]).lower()
    assert "REQUIRES PILOT VALIDATION" in cap["notes"]
    limits = recs["cpu/cpu_frequency_limits"]
    assert set(limits["value"]) == {"policy0", "policy4"}


@pytest.mark.parametrize("resp, state", [
    ((1, "", "ls: /sys/devices/system/cpu/cpufreq: No such file or directory"), "UNAVAILABLE"),
    ((1, "", "ls: /sys/devices/system/cpu/cpufreq: Permission denied"), "PERMISSION_REQUIRED"),
    ((0, "\n", ""), "ERROR"),
])
def test_cpufreq_policy_listing_outcomes(tmp_path, resp, state):
    _, data, _ = run_pipeline(tmp_path, full_app(), responses={"ls /sys/devices/system/cpu/cpufreq": resp})
    assert records(data)["thermal/frequency_capping_observable"]["state"] == state


def test_cpufreq_files_permission_denied(tmp_path):
    _, data, _ = run_pipeline(tmp_path, full_app(), responses={
        "scaling_max_freq": (1, "", "Permission denied"), "cpuinfo_max_freq": (1, "", "Permission denied")})
    assert records(data)["thermal/frequency_capping_observable"]["state"] == "PERMISSION_REQUIRED"


# ---------------------------------------------------------------------------
# A10 configuration-first
# ---------------------------------------------------------------------------

def test_probe_paths_come_from_config(tmp_path):
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    probes = dict(cfg["probes"], kgsl_gpu_busy_path="/sys/class/kgsl/kgsl-3d0/CONFIGURED_BUSY",
                  psi_memory_path="/proc/pressure/CONFIGURED_PSI")
    seen = []
    adb = ADBCollector(device_id="x", probe_config=probes)
    transport = make_transport(json.dumps(full_app()))

    def recording(args):
        seen.append(" ".join(args))
        return transport(args)

    with patch.object(adb, "_adb_cmd", side_effect=recording):
        adb.collect_raw_evidence_and_observations(tmp_path)
    assert any("CONFIGURED_BUSY" in c for c in seen)
    assert any("CONFIGURED_PSI" in c for c in seen)


def test_probe_config_missing_key_is_rejected():
    probes = load_probe_config()
    probes.pop("kgsl_gpu_busy_path")
    with pytest.raises(ValueError, match="kgsl_gpu_busy_path"):
        ADBCollector(device_id="x", probe_config=probes)


def test_no_hardcoded_probe_paths_in_production_host_code():
    host = Path("scripts/device_characterization/adb_collector.py").read_text(encoding="utf-8")
    for path in ("/sys/class/kgsl/kgsl-3d0/gpuclk", "/sys/class/kgsl/kgsl-3d0/gpubusy", "/proc/pressure/memory",
                 "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "/sys/class/thermal/thermal_zone"):
        assert path not in host, path


# ---------------------------------------------------------------------------
# A8 GPU renderer: one authoritative observation
# ---------------------------------------------------------------------------

def test_gpu_renderer_records_share_one_source(full_run):
    recs = records(full_run[1])
    ident, gpu = recs["identity/gpu_renderer"], recs["gpu/gpu_vendor_renderer"]
    assert ident["evidence_ref"] == gpu["evidence_ref"] == f"{APP_EV}#gpu_renderer"
    assert ident["value"]["renderer"] in gpu["value"]
    assert ident["state"] == gpu["state"] == "AVAILABLE"


def test_gpu_renderer_falls_back_to_surfaceflinger_as_conditional(tmp_path):
    app = full_app()
    app["gpu_capability"] = [item("gpu_renderer", "ERROR", error_message="eglInitialize failed")]
    _, data, _ = run_pipeline(tmp_path, app)
    recs = records(data)
    for path in ("identity/gpu_renderer", "gpu/gpu_vendor_renderer"):
        assert recs[path]["state"] == "AVAILABLE"
        assert recs[path]["report_status"] == "CONDITIONALLY AVAILABLE"
        assert recs[path]["evidence_ref"] == "evidence/gpu_renderer_evidence.txt"
    assert recs["identity/gpu_renderer"]["value"]["renderer"] == "Adreno (TM) 610"


# ---------------------------------------------------------------------------
# B1 services
# ---------------------------------------------------------------------------

def test_service_permission_required_is_preserved(full_run):
    recs = records(full_run[1])
    hpm = recs["identity/service_HardwarePropertiesManager"]
    assert hpm["state"] == "PERMISSION_REQUIRED" and hpm["value"] is None and hpm["verified"] is False
    assert "SecurityException" in hpm["error_message"]
    assert hpm["evidence_ref"] == f"{APP_EV}#service_HardwarePropertiesManager"
    for svc in ("PowerManager", "CameraManager", "ActivityManager", "BatteryManager"):
        assert recs[f"identity/service_{svc}"]["state"] == "AVAILABLE"


# ---------------------------------------------------------------------------
# B6-B8 cameras
# ---------------------------------------------------------------------------

def test_camera_ids_and_facing_are_the_reported_ones(tmp_path):
    app = full_app()
    app["camera_telemetry"] = ([item("camera_id_list", value=["0", "2", "20"])] + camera_records("0", "BACK")
                               + camera_records("2", "FRONT", manual=False) + camera_records("20", "BACK"))
    _, data, _ = run_pipeline(tmp_path, app)
    assert [c["camera_id"] for c in data["camera"]] == ["0", "2", "20"]
    assert [c["lens_facing"] for c in data["camera"]] == ["BACK", "FRONT", "BACK"]


def test_camera_count_alone_never_generates_ids(tmp_path):
    app = full_app()
    app["camera_telemetry"] = [item("camera_count", value=4)]
    _, data, _ = run_pipeline(tmp_path, app)
    assert [c["camera_id"] for c in data["camera"]] == ["UNIDENTIFIED"]
    assert data["camera"][0]["lens_facing"] is None


def test_missing_lens_facing_is_not_defaulted_to_back(tmp_path):
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + [
        r for r in camera_records("0") if r["metric"] != "lens_facing"]
    _, data, _ = run_pipeline(tmp_path, app)
    assert data["camera"][0]["lens_facing"] is None
    assert records(data)["camera/0/lens_facing"]["state"] == "NOT_TESTED"


def test_manual_capability_advertised_and_honoured(full_run):
    recs = records(full_run[1])
    assert recs["camera/0/manual_exposure_advertised"]["state"] == "AVAILABLE"
    assert recs["camera/0/manual_control_honoured"]["state"] == "AVAILABLE"
    assert recs["camera/1/manual_exposure_advertised"]["state"] == "UNAVAILABLE"
    assert recs["camera/1/manual_control_honoured"]["state"] == "UNAVAILABLE"
    assert recs["camera/0/available_capabilities"]["notes"].startswith("Host dumpsys cross-check")


def test_advertised_but_not_honoured_is_unavailable(tmp_path):
    honoured = item("manual_control_honoured", value={
        "requested_exposure_time_ns": 16666666, "reported_exposure_time_ns": 33333333,
        "requested_sensitivity": 850, "reported_sensitivity": 850, "frames_compared": 5})
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", honoured=honoured)
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["camera/0/manual_control_honoured"]
    assert rec["state"] == "UNAVAILABLE" and "NOT HONOURED" in rec["notes"] and rec["value"] is None


def test_honoured_tolerance_comes_from_config():
    cam = CameraCapabilityCollector({"exposure_time_relative_tolerance": 0.01, "sensitivity_relative_tolerance": 0.0})
    props = {"is_real_device_observation": True, "app_output_status": "APP_OUTPUT_COLLECTED",
             "app_records": {"camera_id_list": item("camera_id_list", value=["0"])},
             "app_camera_records": {"0": {r["metric"]: r for r in camera_records("0", honoured=item(
                 "manual_control_honoured", value={"requested_exposure_time_ns": 1000000,
                                                   "reported_exposure_time_ns": 1005000,
                                                   "requested_sensitivity": 400, "reported_sensitivity": 400}))}}}
    assert cam.collect(props)[0].manual_control_honoured.state == "AVAILABLE"
    strict = CameraCapabilityCollector({"exposure_time_relative_tolerance": 0.0, "sensitivity_relative_tolerance": 0.0})
    assert strict.collect(props)[0].manual_control_honoured.state == "UNAVAILABLE"


def test_honoured_claim_without_advertisement_is_error(tmp_path):
    honoured = item("manual_control_honoured", value={
        "requested_exposure_time_ns": 1, "reported_exposure_time_ns": 1,
        "requested_sensitivity": 1, "reported_sensitivity": 1})
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", manual=False, honoured=honoured)
    _, data, _ = run_pipeline(tmp_path, app)
    assert records(data)["camera/0/manual_control_honoured"]["state"] == "ERROR"


def test_camera_permission_required(tmp_path):
    perm = item("manual_control_honoured", "PERMISSION_REQUIRED", notes="CAMERA runtime permission not granted")
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", honoured=perm)
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["camera/0/manual_control_honoured"]
    assert rec["state"] == "PERMISSION_REQUIRED" and rec["value"] is None and rec["verified"] is False


def test_manual_control_never_claimed_without_check(tmp_path):
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + [
        r for r in camera_records("0") if r["metric"] != "manual_control_honoured"]
    _, data, _ = run_pipeline(tmp_path, app)
    rec = records(data)["camera/0/manual_control_honoured"]
    assert rec["state"] == "NOT_TESTED" and rec["value"] is None


def test_camera_tolerance_config_is_validated():
    with pytest.raises(ValueError):
        CameraCapabilityCollector({"exposure_time_relative_tolerance": -1, "sensitivity_relative_tolerance": 0})


# ---------------------------------------------------------------------------
# B9 clocks / B10 trace
# ---------------------------------------------------------------------------

def test_non_monotonic_clock_is_error(tmp_path):
    app = full_app()
    app["profiling_capability"] = [item("system_nano_time", value={
        "system_nano_time": {"monotonic": False}, "elapsed_realtime_nanos": {"monotonic": True}})]
    _, data, _ = run_pipeline(tmp_path, app)
    assert records(data)["profiling/system_nano_time"]["state"] == "ERROR"


def test_trace_api_is_available_but_never_verified(full_run):
    rec = records(full_run[1])["profiling/android_trace_api"]
    assert rec["state"] == "AVAILABLE" and rec["verified"] is False and rec["report_status"] == "AVAILABLE"


# ---------------------------------------------------------------------------
# §9 status mapping corrections
# ---------------------------------------------------------------------------

def test_status_mapping_supports_conditional_and_pilot():
    assert map_runtime_state_to_report_status(RuntimeState.AVAILABLE, pilot_validation=True) == \
        ReportStatus.REQUIRES_PILOT_VALIDATION
    assert map_runtime_state_to_report_status(RuntimeState.AVAILABLE, condition="HOST ADB SHELL",
                                              pilot_validation=True) == ReportStatus.CONDITIONALLY_AVAILABLE
    for state in (RuntimeState.NOT_TESTED, RuntimeState.ERROR, RuntimeState.UNAVAILABLE):
        assert map_runtime_state_to_report_status(state, pilot_validation=True) != \
            ReportStatus.REQUIRES_PILOT_VALIDATION
    assert map_runtime_state_to_report_status(RuntimeState.PERMISSION_REQUIRED) == ReportStatus.UNAVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.UNAVAILABLE) == ReportStatus.UNAVAILABLE
    with pytest.raises(ValueError):
        map_runtime_state_to_report_status(RuntimeState.AVAILABLE, verified=True, condition="HOST ADB SHELL")
    with pytest.raises(ValueError):
        map_runtime_state_to_report_status(RuntimeState.AVAILABLE, verified=True, pilot_validation=True)


def test_record_model_rejects_misclassified_statuses():
    with pytest.raises(ValueError):
        CapabilityResult(metric="m", state="NOT_TESTED", report_status="REQUIRES PILOT VALIDATION")
    with pytest.raises(ValueError):
        CapabilityResult(metric="m", state="AVAILABLE", report_status="CONDITIONALLY AVAILABLE", value=1)
    with pytest.raises(ValueError):
        CapabilityResult(metric="m", state="AVAILABLE", report_status="VERIFIED", value=1, verified=True,
                         evidence_ref="e", observed_at="t", condition="HOST ADB SHELL")


def test_host_only_signals_are_conditionally_available_not_verified(full_run):
    recs = records(full_run[1])
    for path in ("cpu/device_wide_cpu_utilization", "gpu/gpu_clock_hz", "profiling/adb_atrace_profiling",
                 "cpu/cpu_scaling_cur_freq", "thermal/thermal_zones_sysfs"):
        assert recs[path]["report_status"] == "CONDITIONALLY AVAILABLE", path
        assert recs[path]["verified"] is False and recs[path]["condition"] == "HOST ADB SHELL", path


def test_validator_rejects_conditional_verified_and_pilot_on_untested(full_run):
    out_dir, data, _ = full_run
    bad = copy.deepcopy(data)
    rec = next(r for t in bad["telemetry"] for r in t["results"] if r["metric"] == "gpu_clock_hz")
    rec.update(verified=True, report_status="VERIFIED")
    assert any("condition-gated" in e or "condition" in e for e in validate_characterization_record(bad, out_dir))
    bad2 = copy.deepcopy(data)
    rec2 = next(r for t in bad2["telemetry"] for r in t["results"] if r["metric"] == "app_cpu_time")
    rec2.update(state="NOT_TESTED", value=None, verified=False, report_status="REQUIRES PILOT VALIDATION")
    assert any("REQUIRES PILOT VALIDATION" in e for e in validate_characterization_record(bad2, out_dir))


def test_api_unsupported_headroom_cites_api_level_evidence(full_run):
    rec = records(full_run[1])["thermal/thermal_headroom_api"]
    assert rec["state"] == "API_UNSUPPORTED"
    assert rec["evidence_ref"] == "evidence/getprop_evidence.txt#ro.build.version.sdk"


# ---------------------------------------------------------------------------
# D-16 energy hierarchy
# ---------------------------------------------------------------------------

def _level(assessed=True, feasible=False, validated=False, **kw):
    d = {"assessed": assessed, "feasible": feasible, "reference_validated": validated}
    d.update(kw)
    return d


def test_select_energy_level_never_skips_a_preferred_level():
    assert select_energy_level(None, None, True) is None
    assert select_energy_level(_level(assessed=False), None, True) is None             # E-1 unassessed
    assert select_energy_level(_level(feasible=True, validated=False), None, True) is None  # E-1 pending validation
    assert select_energy_level(_level(feasible=True, validated=True), None, True) == "E-1"
    assert select_energy_level(_level(), _level(assessed=False), True) is None          # E-2 unassessed
    assert select_energy_level(_level(), _level(feasible=True, validated=True, non_charging_verified=False), True) is None
    assert select_energy_level(_level(), _level(feasible=True, validated=True, non_charging_verified=True), True) == "E-2"
    assert select_energy_level(_level(), _level(), True) == "E-3"
    assert select_energy_level(_level(), _level(), None) is None
    assert select_energy_level(_level(), _level(), False) is None


def test_software_counters_alone_do_not_select_e3(full_run):
    energy = full_run[1]["energy"]
    assert energy["E3_software_counters"]["state"] == "AVAILABLE"
    assert energy["E3_software_counters"]["report_status"] == "REQUIRES PILOT VALIDATION"
    assert energy["E1_battery_side_reference"]["state"] == "NOT_TESTED"
    assert energy["E2_supply_powered_session"]["state"] == "NOT_TESTED"
    assert energy["selected_level"] is None
    assert energy["absolute_energy_claimed"] is False


def test_e3_unavailable_when_all_counters_unsupported():
    batt = BatteryTelemetryCollector().collect({
        "is_real_device_observation": True, "app_output_status": "APP_OUTPUT_COLLECTED",
        "app_records": {m: item(m, "UNAVAILABLE") for m in ("battery_property_current_now",
                                                           "battery_property_charge_counter",
                                                           "battery_property_energy_counter")}})
    e = EnergyMeasurementCapabilityChecker().collect({"is_real_device_observation": True}, battery_results=batt.results)
    assert e.E3_software_counters.state == "UNAVAILABLE"
    assert e.selected_level is None


def _write_energy(tmp_path, e1, e2):
    (tmp_path / "photo.txt").write_text("inspection note", encoding="utf-8")
    base = {"assessed_by": "researcher", "assessed_on": "2026-10-08", "evidence_files": ["photo.txt"],
            "notes": None, "instrument_model": None, "meter_model": None, "safety_signoff": False,
            "non_charging_verified": False}
    data = {"E1_battery_side_reference": dict(base, **e1), "E2_supply_powered_session": dict(base, **e2)}
    for k in data:
        if k == "E1_battery_side_reference":
            data[k].pop("non_charging_verified")
        else:
            data[k].pop("safety_signoff")
    path = tmp_path / "energy.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def test_researcher_energy_evidence_selects_e3_only_after_e1_e2_ruled_out(tmp_path):
    path = _write_energy(tmp_path, _level(), _level())
    out_dir, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(path)})
    energy = data["energy"]
    assert energy["E1_battery_side_reference"]["state"] == "EXTERNAL_REQUIRED"
    assert energy["E1_battery_side_reference"]["report_status"] == "REQUIRES EXTERNAL INSTRUMENTATION"
    assert energy["E1_battery_side_reference"]["evidence_ref"].startswith("evidence/energy_feasibility_evidence.yaml")
    assert energy["selected_level"] == "E-3"
    assert (out_dir / "evidence" / "energy_feasibility_evidence.yaml").exists()
    assert (out_dir / "evidence" / "energy_feasibility_photo.txt").exists()


def test_invalid_energy_evidence_is_error_and_selects_nothing(tmp_path):
    bad = tmp_path / "energy.yaml"
    bad.write_text(yaml.safe_dump({"E1_battery_side_reference": {"assessed": True}}), encoding="utf-8")
    _, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(bad)})
    assert data["energy"]["E1_battery_side_reference"]["state"] == "ERROR"
    assert data["energy"]["selected_level"] is None


def test_energy_template_is_valid_and_unassessed():
    data = yaml.safe_load(Path("configs/energy_feasibility_evidence_template.yaml").read_text(encoding="utf-8"))
    assert validate_energy_evidence(data) == []
    assert all(data[k]["assessed"] is False for k in data)
    assert yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["energy_feasibility_evidence"] is None


# ---------------------------------------------------------------------------
# §9 coverage and sign-off
# ---------------------------------------------------------------------------

def test_every_matrix_row_is_mapped_and_no_stale_mapping():
    rows = {r["row_id"] for r in parse_matrix()}
    mapping = set(load_coverage_config()["rows"])
    assert rows == mapping


def test_coverage_flags_untested_rows_and_backends(full_run):
    cov = check_matrix_coverage(full_run[1])
    by_id = {r["row_id"]: r for r in cov["rows"]}
    assert cov["passed"] is False
    assert by_id["5/TFLite GPU delegate"]["passed"] is False and "NOT_TESTED" in by_id["5/TFLite GPU delegate"]["problem"]
    assert by_id["3/GPU/Memory"]["problem"] == "NO_COLLECTOR"
    assert by_id["8/E-1 battery-side external reference"]["passed"] is False
    assert by_id["7/D. External surface temperature required"]["passed"] is True
    assert by_id["1/RAM variant"]["passed"] is True
    assert by_id["4/Manual control honoured"]["passed"] is True


def test_coverage_detects_unmapped_and_stale_rows(full_run):
    cfg = load_coverage_config()
    rows = dict(cfg["rows"])
    rows.pop("1/Manufacturer")
    rows["9/Not a matrix row"] = {"records": ["identity:model"]}
    cov = check_matrix_coverage(full_run[1], config={"rows": rows})
    problems = {r["row_id"]: r["problem"] for r in cov["rows"]}
    assert problems["1/Manufacturer"] == "UNMAPPED_ROW"
    assert problems["9/Not a matrix row"] == "STALE_MAPPING"


def test_coverage_passes_when_every_row_has_status_and_evidence(full_run):
    """The checker is not vacuous: with every gap row filled it passes; removing one evidence ref fails it."""
    data = copy.deepcopy(full_run[1])
    filled = {"state": "AVAILABLE", "report_status": "AVAILABLE", "evidence_ref": "evidence/x", "value": 1}
    for b in data["backends"]:
        for k in ("availability", "delegation", "probability_output"):
            b[k].update(filled)
    for k in ("E1_battery_side_reference", "E2_supply_powered_session"):
        data["energy"][k].update(state="EXTERNAL_REQUIRED", report_status="REQUIRES EXTERNAL INSTRUMENTATION",
                                 evidence_ref="evidence/energy_feasibility_evidence.yaml")
    cfg = load_coverage_config()
    rows = {k: v for k, v in cfg["rows"].items() if v.get("records") or v.get("specification_fixed")}
    rows["3/GPU/Memory"] = {"records": ["identity:model"]}
    rows["5/Other approved runtimes (e.g. ExecuTorch)"] = {"records": ["identity:model"]}
    cov = check_matrix_coverage(data, config={"rows": rows})
    assert cov["passed"] is True, [r for r in cov["rows"] if not r["passed"]]
    rec = next(r for t in data["telemetry"] for r in t["results"] if r["metric"] == "app_cpu_time")
    rec["evidence_ref"] = None
    assert check_matrix_coverage(data, config={"rows": rows})["passed"] is False


def test_signoff_requires_every_criterion_and_human_review(full_run):
    out_dir, data, _ = full_run
    s = evaluate_step10d_signoff(data)
    assert s["signoff_allowed"] is False
    assert s["criteria"]["criterion_2_variant_check"]["passed"] is True
    assert s["criteria"]["criterion_3_d10_thermal_source"]["passed"] is True
    assert s["criteria"]["criterion_3_d16_energy_level"]["passed"] is False
    assert s["criteria"]["criterion_4_review_gate"]["status"] == "PENDING_HUMAN_REVIEW"
    # Even with review confirmed, failing automated criteria keep sign-off blocked.
    assert evaluate_step10d_signoff(data, review_confirmed=True)["signoff_allowed"] is False
    written = json.loads((out_dir / "step10d_signoff.json").read_text(encoding="utf-8"))
    assert written["signoff"]["signoff_allowed"] is False
    assert written["signoff"]["criteria"]["criterion_4_review_gate"]["passed"] is False
    readme = (out_dir / "README.md").read_text(encoding="utf-8")
    assert "**Step 10D sign-off**: `NOT ALLOWED`" in readme and "PENDING_HUMAN_REVIEW" in readme


def test_signoff_d16_rejects_e3_with_unassessed_preferred_levels(full_run):
    data = copy.deepcopy(full_run[1])
    data["energy"]["selected_level"] = "E-3"  # forged: E-1/E-2 still NOT_TESTED
    d16 = evaluate_step10d_signoff(data)["criteria"]["criterion_3_d16_energy_level"]
    assert d16["passed"] is False and any("preferred level is unassessed" in p for p in d16["problems"])


def test_signoff_d10_requires_evidence(full_run):
    data = copy.deepcopy(full_run[1])
    data["thermal"]["thermal_status_api"]["evidence_ref"] = None
    assert evaluate_step10d_signoff(data)["criteria"]["criterion_3_d10_thermal_source"]["passed"] is False
    data["thermal"]["selected_thermal_source"] = None
    assert evaluate_step10d_signoff(data)["criteria"]["criterion_3_d10_thermal_source"]["passed"] is False


def test_repeat_comparison_covers_all_phases(full_run):
    a = copy.deepcopy(full_run[1])
    b = copy.deepcopy(full_run[1])
    a["started_at"], b["started_at"] = "2026-10-08T10:00:00Z", "2026-10-09T10:00:00Z"
    a["conditions"]["boot_id"], b["conditions"]["boot_id"] = "b1", "b2"
    gen = CharacterizationReportGenerator()
    assert gen.compare_repeat_runs(a, b)["stable"] is True
    b["camera"][0]["manual_control_honoured"]["state"] = "UNAVAILABLE"
    b["camera"][0]["manual_control_honoured"]["value"] = None
    res = gen.compare_repeat_runs(a, b)
    assert res["stable"] is False
    assert any("camera/0/manual_control_honoured" in d for d in res["discrepancies"])
    assert res["signoff_allowed"] is False


# ---------------------------------------------------------------------------
# Historical runs and backends
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("run_id", ["run_20261005_181140", "run_20261006_052440", "run_20261007_082743"])
def test_protected_historical_runs_are_never_written(tmp_path, run_id):
    target = tmp_path / run_id
    target.mkdir()
    (target / "sentinel.txt").write_text("historical", encoding="utf-8")
    with pytest.raises(PermissionError):
        run_characterization(CONFIG, run_id=run_id, dry_run=True, overwrite=True, results_dir=tmp_path)
    assert [p.name for p in target.iterdir()] == ["sentinel.txt"]


def test_protected_runs_listed_in_config():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert set(cfg["protected_runs"]) == {"run_20261005_181140", "run_20261006_052440", "run_20261007_082743"}


def test_backends_stay_not_tested_and_are_marked_blocked(full_run):
    for b in full_run[1]["backends"]:
        for k in ("availability", "delegation", "probability_output"):
            assert b[k]["state"] == "NOT_TESTED" and b[k]["value"] is None
            assert "BLOCKED PENDING RESEARCHER DECISION" in b[k]["notes"]


def test_no_ml_runtime_dependency_added_to_app():
    gradle = Path("mobile/characterization/build.gradle.kts").read_text(encoding="utf-8").lower()
    for dep in ("tensorflow", "tflite", "litert", "onnxruntime", "executorch"):
        assert dep not in gradle, dep


def test_app_sections_match_host_bridge():
    import re
    fmt = Path("mobile/characterization/src/main/kotlin/org/pocketinspect/characterization/AppJsonLogFormatter.kt"
               ).read_text(encoding="utf-8")
    runner = Path("mobile/characterization/src/main/kotlin/org/pocketinspect/characterization/CharacterizationRunner.kt"
                  ).read_text(encoding="utf-8")
    block = fmt[fmt.index("val SECTIONS"):fmt.index(")", fmt.index("val SECTIONS"))]
    sections = re.findall(r'"([a-z_]+)"', block)
    assert set(sections) == set(ADBCollector.APP_SECTION_METRICS)
    for s in sections:
        assert f'"{s}" to' in runner, s
