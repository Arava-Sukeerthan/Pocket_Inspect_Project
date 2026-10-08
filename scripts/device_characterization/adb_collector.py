"""
ADB collector for host-side shell paths, evidence parsing, and provenance.

Executes ADB commands (`getprop`, `/proc/stat`, `/proc/meminfo`, cpufreq, thermal zones,
dumpsys battery, dumpsys thermalservice, dumpsys media.camera, atrace, boot_id) to collect raw
evidence from the connected physical device (OPPO A5 2020) and parses it into structured device
observation properties with real evidence files, SHA-256 manifests, and observed_props.json.
"""

import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from src.monitoring.characterization import host_probes

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = ROOT / "configs" / "device_characterization.yaml"

REQUIRED_PROBE_KEYS = (
    "cpufreq_sysfs_pattern", "cpufreq_policy_dir", "cpufreq_policy_files", "thermal_sysfs_pattern",
    "thermal_zone_scan_count", "kgsl_gpu_clock_path", "kgsl_gpu_busy_path", "kgsl_gpu_memory_paths",
    "psi_memory_path", "kernel_release_command",
)


def load_probe_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Loads and validates the `probes` block of configs/device_characterization.yaml (A10: no hidden paths)."""
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    return validate_probe_config(cfg.get("probes") or {})


def validate_probe_config(probes: Dict[str, Any]) -> Dict[str, Any]:
    missing = [k for k in REQUIRED_PROBE_KEYS if k not in probes]
    if missing:
        raise ValueError(f"configs/device_characterization.yaml probes block is missing keys: {missing}")
    mem_paths = probes["kgsl_gpu_memory_paths"]
    if not isinstance(mem_paths, list) or not mem_paths or not all(isinstance(p, str) and p for p in mem_paths):
        raise ValueError("configs/device_characterization.yaml probes.kgsl_gpu_memory_paths must be a non-empty "
                         "list of paths")
    return dict(probes)


def _get_adb_binary() -> str:
    sdk_adb = os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe")
    if os.path.exists(sdk_adb):
        return sdk_adb
    return "adb"


class ADBCollector:
    """Host-side ADB collector for querying connected Android device shell paths."""

    def __init__(self, device_id: Optional[str] = None, timeout_seconds: int = 15,
                 probe_config: Optional[Dict[str, Any]] = None):
        self.device_id = device_id
        self.timeout = timeout_seconds
        self.command_logs: List[Dict[str, Any]] = []
        self.probes = validate_probe_config(probe_config) if probe_config else load_probe_config()

    def _adb_cmd(self, args: List[str]) -> Tuple[int, str, str]:
        adb_bin = _get_adb_binary()
        cmd = [adb_bin]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            self.command_logs.append({
                "timestamp": ts,
                "cmd": cmd,
                "exit_code": res.returncode,
                "stdout_snippet": res.stdout[:500] if res.stdout else "",
                "stderr_snippet": res.stderr[:500] if res.stderr else ""
            })
            return res.returncode, res.stdout, res.stderr
        except Exception as e:
            self.command_logs.append({
                "timestamp": ts,
                "cmd": cmd,
                "exit_code": -1,
                "stdout_snippet": "",
                "stderr_snippet": str(e)
            })
            return -1, "", str(e)

    def get_adb_version(self) -> str:
        code, out, _ = self._adb_cmd(["version"])
        if code == 0:
            match = re.search(r"Android Debug Bridge version ([\d.]+)", out)
            return match.group(1) if match else out.strip().splitlines()[0]
        return "unknown"

    def get_connection_status(self) -> str:
        """Classifies the connection state explicitly.

        Returns one of:
          - ADB_MISSING
          - NO_DEVICE
          - UNAUTHORIZED
          - OFFLINE
          - MULTIPLE_DEVICES
          - CONNECTED
        """
        adb_bin = _get_adb_binary()
        if not os.path.exists(adb_bin) and adb_bin != "adb":
            return "ADB_MISSING"

        code, stdout, stderr = self._adb_cmd(["devices"])
        if code != 0:
            return "ADB_MISSING"

        lines = [line.strip() for line in stdout.splitlines() if line.strip() and not line.startswith("List of devices")]
        if not lines:
            return "NO_DEVICE"

        if self.device_id:
            matching = []
            for line in lines:
                parts = line.split()
                if parts and parts[0] == self.device_id:
                    matching.append(line)
            if not matching:
                return "NO_DEVICE"
            target_line = matching[0]
        else:
            if len(lines) > 1:
                return "MULTIPLE_DEVICES"
            target_line = lines[0]

        parts = target_line.split()
        if len(parts) >= 2:
            state = parts[1]
            if state == "device":
                self.detected_serial = parts[0]
                return "CONNECTED"
            elif state == "unauthorized":
                return "UNAUTHORIZED"
            elif state == "offline":
                return "OFFLINE"

        return "NO_DEVICE"

    def is_device_connected(self) -> bool:
        return self.get_connection_status() == "CONNECTED"

    def get_properties(self) -> Dict[str, str]:
        code, stdout, _ = self._adb_cmd(["shell", "getprop"])
        if code != 0:
            return {}
        props: Dict[str, str] = {}
        for line in stdout.splitlines():
            line = line.strip()
            if line.startswith("[") and "]: [" in line:
                key, val = line[1:].split("]: [", 1)
                val = val.rstrip("]")
                props[key] = val
        return props

    def read_file(self, path: str) -> Tuple[bool, str]:
        code, stdout, stderr = self._adb_cmd(["shell", "cat", path])
        if code == 0 and "No such file" not in stdout and "Permission denied" not in stdout:
            return True, stdout
        return False, stderr or stdout

    def check_thermal_zones(self) -> List[Dict[str, str]]:
        zones = []
        pattern = self.probes["thermal_sysfs_pattern"]
        for i in range(int(self.probes["thermal_zone_scan_count"])):
            t_path = f"{pattern % i}/type"
            v_path = f"{pattern % i}/temp"
            ok_t, name = self.read_file(t_path)
            ok_v, temp = self.read_file(v_path)
            if ok_t and ok_v:
                zones.append({"zone": f"thermal_zone{i}", "type": name.strip(), "temp": temp.strip()})
        return zones

    def parse_proc_meminfo(self, text: str) -> Dict[str, int]:
        """Parses /proc/meminfo text into kB values and total/avail RAM in MB."""
        res = {}
        for line in text.splitlines():
            if ":" in line:
                parts = line.split(":", 1)
                k = parts[0].strip()
                v_str = parts[1].strip().split()[0]
                try:
                    res[k] = int(v_str)
                except ValueError:
                    pass
        out = {}
        if "MemTotal" in res:
            out["total_ram_mb"] = res["MemTotal"] // 1024
        if "MemAvailable" in res:
            out["available_memory_mb"] = res["MemAvailable"] // 1024
        return out

    def parse_proc_cpuinfo(self, text: str) -> Dict[str, Any]:
        """Parses /proc/cpuinfo text for processor count and hardware model."""
        processors = re.findall(r"^processor\s*:\s*\d+", text, flags=re.MULTILINE)
        hardware = re.search(r"^Hardware\s*:\s*(.+)$", text, flags=re.MULTILINE)
        return {
            "core_count": len(processors) if processors else None,
            "hardware": hardware.group(1).strip() if hardware else None,
        }

    def parse_dumpsys_battery(self, text: str) -> Dict[str, Any]:
        """Parses dumpsys battery output."""
        res: Dict[str, Any] = {}
        fields: List[str] = []
        for line in text.splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                fields.append(k)
                if k == "Charge counter":
                    try:
                        res["battery_charge_counter"] = int(v)
                    except ValueError:
                        res["probe_error_battery_charge_counter"] = f"Failed to parse charge counter value: '{v}'"
                elif k == "health":
                    try:
                        res["battery_health_code"] = int(v)
                    except ValueError:
                        pass
                elif k == "present":
                    res["battery_present"] = (v == "true")
                elif k == "level":
                    try:
                        res["battery_level_percent"] = int(v)
                    except ValueError:
                        pass
                elif k == "voltage":
                    try:
                        res["battery_voltage"] = int(v)
                    except ValueError:
                        pass
                elif k == "temperature":
                    try:
                        res["battery_temperature"] = int(v) / 10.0
                    except ValueError:
                        pass
                elif k == "AC powered" and v == "true":
                    res["charging_state"] = True
                    res["plugged_source"] = "AC"
                elif k == "USB powered" and v == "true":
                    res["charging_state"] = True
                    res["plugged_source"] = "USB"
                elif k == "Wireless powered" and v == "true":
                    res["charging_state"] = True
                    res["plugged_source"] = "Wireless"
                elif k == "status":
                    try:
                        st = int(v)
                        # BatteryManager.BATTERY_STATUS_CHARGING = 2, FULL = 5
                        res["battery_status_code"] = st
                        if "charging_state" not in res:
                            res["charging_state"] = st in (2, 5)
                    except ValueError:
                        pass
                elif k == "current now":
                    try:
                        res["battery_current_now"] = int(v)
                    except ValueError:
                        res["battery_current_now"] = v
                        res["probe_error_battery_current"] = f"Failed to parse battery current value: '{v}'"
        if "charging_state" not in res:
            res["charging_state"] = False
        # Which fields this build's dumpsys prints: lets collectors say "field not printed" instead of NOT_TESTED silently.
        res["battery_dumpsys_fields"] = fields
        return res

    def probe_path(self, path: str) -> Dict[str, Any]:
        """Reads one path with `adb shell cat` and returns the structured probe record (outcome + raw streams)."""
        code, out, err = self._adb_cmd(["shell", "cat", path])
        return host_probes.probe_record(path, code, out, err)

    def probe_command(self, args: List[str]) -> Dict[str, Any]:
        code, out, err = self._adb_cmd(["shell"] + list(args))
        return host_probes.probe_record(" ".join(args), code, out, err)

    def get_boot_id(self) -> str:
        ok, out = self.read_file("/proc/sys/kernel/random/boot_id")
        if ok and out.strip():
            return out.strip()
        ok_up, out_up = self.read_file("/proc/uptime")
        if ok_up and out_up.strip():
            return f"uptime_{out_up.strip().split()[0]}"
        return "unknown_boot_id"

    def probe_profiling_capability(self, ev_dir: Path) -> Tuple[bool, Path]:
        """Executes actual atrace profiling probe and records evidence."""
        ev_dir.mkdir(parents=True, exist_ok=True)
        code, out, err = self._adb_cmd(["shell", "atrace", "--list_categories"])
        ev_file = ev_dir / "atrace_evidence.txt"
        ev_file.write_text(f"Exit Code: {code}\nSTDOUT:\n{out}\nSTDERR:\n{err}", encoding="utf-8")
        success = (code == 0 and len(out.strip()) > 0 and "No such file" not in err)
        return success, ev_file

    def probe_network_state(self, ev_dir: Path) -> Tuple[Optional[str], Path]:
        """Probes airplane mode / network state via settings get global."""
        ev_dir.mkdir(parents=True, exist_ok=True)
        code, out, err = self._adb_cmd(["shell", "settings", "get", "global", "airplane_mode_on"])
        ev_file = ev_dir / "network_evidence.txt"
        ev_file.write_text(f"Exit Code: {code}\nSTDOUT:\n{out}\nSTDERR:\n{err}", encoding="utf-8")
        if code == 0:
            val = out.strip()
            if val == "1":
                return "OFFLINE", ev_file
            elif val == "0":
                return "ONLINE", ev_file
        return None, ev_file

    def retrieve_android_app_output(
        self, ev_dir: Path, manifest_entries: List[Dict[str, Any]]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Host retrieves on-device Android app output via ADB, saves evidence, and computes SHA-256 hash.

        Status flow:
          - APP_OUTPUT_COLLECTED: Output file retrieved and valid JSON
          - APP_OUTPUT_MISSING: Retrieval command executed successfully but output file missing
          - APP_OUTPUT_ERROR: Retrieval command failed (run-as or shell error, permission denied, invalid JSON)
        """
        code_runas, out_runas, err_runas = self._adb_cmd(
            ["shell", "run-as", "org.pocketinspect.characterization", "cat", "files/characterization_output.json"]
        )
        out = out_runas
        err = err_runas
        code = code_runas

        if code_runas != 0 or "Permission denied" in err_runas or "not debuggable" in err_runas or "not debuggable" in out_runas:
            code_sd, out_sd, err_sd = self._adb_cmd(
                ["shell", "cat", "/sdcard/Android/data/org.pocketinspect.characterization/files/characterization_output.json"]
            )
            code = code_sd
            out = out_sd
            err = err_sd

        if "No such file" in out or "No such file" in err:
            return "APP_OUTPUT_MISSING", None

        if code != 0 or "Permission denied" in out or "Permission denied" in err or not out.strip():
            return "APP_OUTPUT_ERROR", None

        try:
            parsed = json.loads(out)
            p = ev_dir / "android_app_evidence.json"
            data_bytes = out.encode("utf-8")
            p.write_bytes(data_bytes)
            manifest_entries.append({
                "relative_path": "evidence/android_app_evidence.json",
                "size_bytes": len(data_bytes),
                "sha256": hashlib.sha256(data_bytes).hexdigest(),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            return "APP_OUTPUT_COLLECTED", parsed
        except Exception:
            p_err = ev_dir / "android_app_evidence_raw.txt"
            data_bytes = out.encode("utf-8")
            p_err.write_bytes(data_bytes)
            manifest_entries.append({
                "relative_path": "evidence/android_app_evidence_raw.txt",
                "size_bytes": len(data_bytes),
                "sha256": hashlib.sha256(data_bytes).hexdigest(),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            return "APP_OUTPUT_ERROR", None

    # ------------------------------------------------------------------
    # Android app -> host bridge (A2)
    # ------------------------------------------------------------------
    # Explicit registry of the app report (CharacterizationRunner.kt): section -> metrics the host consumes.
    # Anything outside the registry is not used as an observation; it is listed in
    # `app_unrecognised_items` and stays only in the raw evidence file (android_app_evidence.json).
    APP_SECTION_METRICS: Dict[str, Tuple[str, ...]] = {
        "device_identity": ("manufacturer", "model", "soc_model", "storage_total_bytes"),
        "memory_telemetry": ("total_ram_mb", "available_memory_mb", "low_memory_flag", "memory_threshold_mb",
                             "app_heap_allocated_mb", "app_pss_kb"),
        "thermal_capability": ("thermal_status_api", "thermal_status_listener"),
        "battery_telemetry": ("battery_level_percent", "battery_voltage", "battery_temperature", "is_charging",
                              "battery_property_current_now", "battery_property_current_average",
                              "battery_property_charge_counter", "battery_property_energy_counter"),
        "service_capability": ("service_PowerManager", "service_HardwarePropertiesManager",
                               "service_CameraManager", "service_ActivityManager", "service_BatteryManager",
                               "power_save_mode"),
        "cpu_telemetry": ("app_cpu_time",),
        "gpu_capability": ("gpu_renderer", "gpu_vulkan_support"),
        "profiling_capability": ("system_nano_time", "android_trace_api"),
        "camera_telemetry": ("camera_id_list", "camera_probe", "camera_count", "camera_0_hardware_level"),
        "backend_capability": (),  # every record is per backend (see APP_BACKEND_METRICS)
    }
    # Per-backend metrics: app records in backend_capability that carry a "backend" field (BackendProbes.kt).
    # `reference_graph_check` records also carry "graph_variant" and are keyed "reference_graph_check/<variant>".
    APP_BACKEND_METRICS: Tuple[str, ...] = ("backend_runtime", "reference_graph_check")
    # Per-camera metrics: app records in camera_telemetry that carry a "camera_id" field.
    APP_CAMERA_METRICS: Tuple[str, ...] = (
        "lens_facing", "hardware_level", "available_capabilities", "manual_exposure_advertised",
        "manual_control_honoured", "capture_sensor_timestamp", "ae_target_fps_ranges", "af_available_modes",
        "lens_min_focus_distance", "exposure_time_range_ns", "sensitivity_range", "awb_available_modes",
        "ae_lock_available", "awb_lock_available", "physical_camera_ids", "stream_configurations",
        "video_profiles",
    )
    # Legacy flat metrics merged into observed_props with host-wins provenance (P5-01). All other app
    # metrics are consumed only through `app_records` / `app_camera_records`, always citing the app file.
    APP_METRICS = (
        "manufacturer",
        "model",
        "soc_model",
        "total_ram_mb",
        "available_memory_mb",
        "battery_level_percent",
        "battery_voltage",
        "battery_temperature",
        "thermal_status_api",
        "camera_probe",
    )
    _RECORD_FIELDS = ("state", "value", "unit", "error_message", "notes", "details", "source", "min_api")

    @classmethod
    def _app_record(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        return {k: item.get(k) for k in cls._RECORD_FIELDS}

    @staticmethod
    def _prefer(existing: Optional[Dict[str, Any]], new: Dict[str, Any]) -> bool:
        """An AVAILABLE record takes precedence over a non-AVAILABLE one for the same metric."""
        return not (existing and existing.get("state") == "AVAILABLE" and new.get("state") != "AVAILABLE")

    def _normalize_app_output_full(self, app_parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes the app report into {"records", "camera_records", "backend_records", "unrecognised"}
        (structured, no raw dump)."""
        records: Dict[str, Dict[str, Any]] = {}
        camera_records: Dict[str, Dict[str, Dict[str, Any]]] = {}
        backend_records: Dict[str, Dict[str, Dict[str, Any]]] = {}
        unrecognised: List[str] = []
        if not isinstance(app_parsed, dict):
            return {"records": records, "camera_records": camera_records, "backend_records": backend_records,
                    "unrecognised": unrecognised}

        for section_name, allowed in self.APP_SECTION_METRICS.items():
            section = app_parsed.get(section_name)
            items = section if isinstance(section, list) else ([section] if isinstance(section, dict) else [])
            for item in items:
                if not isinstance(item, dict):
                    continue
                metric = item.get("metric")
                cam_id = item.get("camera_id")
                backend = item.get("backend")
                if section_name == "backend_capability":
                    variant = item.get("graph_variant")
                    if backend is None or metric not in self.APP_BACKEND_METRICS or \
                            (metric == "reference_graph_check") != (variant is not None):
                        unrecognised.append(f"{section_name}/{backend}/{metric}/{variant}")
                        continue
                    key = metric if variant is None else f"{metric}/{variant}"
                    backend_records.setdefault(str(backend), {})[key] = self._app_record(item)
                    continue
                if section_name == "camera_telemetry" and cam_id is not None:
                    if metric not in self.APP_CAMERA_METRICS:
                        unrecognised.append(f"{section_name}/{cam_id}/{metric}")
                        continue
                    rec = self._app_record(item)
                    per_cam = camera_records.setdefault(str(cam_id), {})
                    if self._prefer(per_cam.get(metric), rec):
                        per_cam[metric] = rec
                    continue
                if metric not in allowed:
                    unrecognised.append(f"{section_name}/{metric}")
                    continue
                rec = self._app_record(item)
                if self._prefer(records.get(metric), rec):
                    records[metric] = rec
        return {"records": records, "camera_records": camera_records, "backend_records": backend_records,
                "unrecognised": unrecognised}

    def _normalize_app_output(self, app_parsed: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Legacy view: one record per APP_METRICS metric ({"state", "value", "unit", "error_message"})."""
        full = self._normalize_app_output_full(app_parsed)
        return {
            m: {k: r.get(k) for k in ("state", "value", "unit", "error_message")}
            for m, r in full["records"].items() if m in self.APP_METRICS
        }

    @staticmethod
    def _merge_app_observations(observed_props: Dict[str, Any], app_records: Dict[str, Dict[str, Any]]) -> None:
        """Merges app records into observed_props with source-correct provenance.

        - Host value present: the host value wins and no app flag is set.
        - Host value absent and the app reports AVAILABLE with a value: the app value is
          used and `<metric>_is_app_derived` is set, so collectors cite android_app_evidence.json.
        - Any non-AVAILABLE app state is recorded in `app_metric_states` and never becomes a value.
        """
        app_states: Dict[str, Dict[str, Any]] = {}
        for metric, rec in app_records.items():
            state = rec.get("state")
            if state != "AVAILABLE":
                app_states[metric] = {"state": state, "error_message": rec.get("error_message")}
                continue

            if metric == "thermal_status_api":
                # The app's AVAILABLE result is the only observation of this API.
                if observed_props.get("thermal_status_api_available") is None:
                    observed_props["thermal_status_api_available"] = True
                    observed_props["thermal_status_api_is_app_derived"] = True
                continue

            value = rec.get("value")
            if value is None or observed_props.get(metric) is not None:
                continue
            observed_props[metric] = value
            observed_props[f"{metric}_is_app_derived"] = True
            if rec.get("unit"):
                observed_props[f"{metric}_unit"] = rec["unit"]
            if metric == "soc_model":
                observed_props["source_soc_prop"] = "Build.SOC_MODEL (android app)"

        if app_states:
            observed_props["app_metric_states"] = app_states

    def collect_raw_evidence_and_observations(
        self, output_dir: Path, extra_evidence: Optional[Dict[str, bytes]] = None
    ) -> Tuple[List[Path], Dict[str, Any]]:
        """Collects raw evidence text files, writes observed_props.json & manifest.json."""
        ev_dir = output_dir / "evidence"
        ev_dir.mkdir(parents=True, exist_ok=True)
        files_saved = []
        observed_props: Dict[str, Any] = {"is_real_device_observation": True}
        manifest_entries: List[Dict[str, Any]] = []

        def _save_evidence(filename: str, content: Any) -> Path:
            p = ev_dir / filename
            data_bytes = content if isinstance(content, bytes) else content.encode("utf-8")
            p.write_bytes(data_bytes)
            files_saved.append(p)
            sha256 = hashlib.sha256(data_bytes).hexdigest()
            manifest_entries.append({
                "relative_path": f"evidence/{filename}",
                "size_bytes": len(data_bytes),
                "sha256": sha256,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            return p

        def _save_json_evidence(filename: str, obj: Any) -> Path:
            return _save_evidence(filename, json.dumps(obj, indent=2, sort_keys=True))

        # 1. proc cpuinfo (parsed early for SoC fallback)
        ok_cpu, out_cpu = self.read_file("/proc/cpuinfo")
        cpu_parsed = {}
        if ok_cpu:
            _save_evidence("cpuinfo_evidence.txt", out_cpu)
            cpu_parsed = self.parse_proc_cpuinfo(out_cpu)
            observed_props.update(cpu_parsed)
        else:
            observed_props["probe_error_cpuinfo"] = f"Failed to read /proc/cpuinfo: {out_cpu}"

        # 2. getprop with P-04 SoC property fallback provenance
        code, out_prop, err_prop = self._adb_cmd(["shell", "getprop"])
        if code == 0:
            _save_evidence("getprop_evidence.txt", out_prop)
            props = self.get_properties()
            observed_props["manufacturer"] = props.get("ro.product.manufacturer")
            observed_props["model"] = props.get("ro.product.model")
            observed_props["release_version"] = props.get("ro.build.version.release")
            sdk_str = props.get("ro.build.version.sdk")
            observed_props["api_level"] = int(sdk_str) if sdk_str and sdk_str.isdigit() else None
            observed_props["cpu_abi"] = props.get("ro.product.cpu.abi")
            observed_props["build_fingerprint"] = props.get("ro.build.fingerprint")
            observed_props["security_patch"] = props.get("ro.build.version.security_patch")

            # P-04 SoC property fallback with explicit source property recording
            if props.get("ro.soc.model"):
                observed_props["soc_model"] = props.get("ro.soc.model")
                observed_props["source_soc_prop"] = "ro.soc.model"
            elif props.get("ro.board.platform"):
                observed_props["soc_model"] = props.get("ro.board.platform")
                observed_props["source_soc_prop"] = "ro.board.platform"
            elif cpu_parsed.get("hardware"):
                observed_props["soc_model"] = cpu_parsed.get("hardware")
                observed_props["source_soc_prop"] = "Hardware (/proc/cpuinfo)"
            else:
                observed_props["soc_model"] = None
                observed_props["source_soc_prop"] = "UNAVAILABLE"
        else:
            observed_props["probe_error_getprop"] = f"Exit code {code}: {err_prop or out_prop}"

        # 3. dumpsys meminfo / proc meminfo
        ok_mem, out_mem = self.read_file("/proc/meminfo")
        if ok_mem:
            _save_evidence("meminfo_evidence.txt", out_mem)
            mem_parsed = self.parse_proc_meminfo(out_mem)
            observed_props.update(mem_parsed)
        else:
            observed_props["probe_error_meminfo"] = f"Failed to read /proc/meminfo: {out_mem}"

        # 4. proc stat check
        ok_stat, out_stat = self.read_file("/proc/stat")
        if ok_stat:
            _save_evidence("proc_stat_evidence.txt", out_stat)
            observed_props["proc_stat_readable_via_adb"] = True
        else:
            observed_props["probe_error_proc_stat"] = f"Failed to read /proc/stat: {out_stat}"

        # 5. thermal zones & dumpsys thermalservice
        zones = self.check_thermal_zones()
        code_th, out_th, err_th = self._adb_cmd(["shell", "dumpsys", "thermalservice"])
        th_content = f"THERMAL ZONES:\n" + "\n".join([f"{z['zone']}: {z['type']} = {z['temp']}" for z in zones])
        if code_th == 0:
            th_content += f"\n\nDUMPSYS THERMALSERVICE:\n{out_th}"
            _save_evidence("thermal_evidence.txt", th_content)
        else:
            if zones:
                _save_evidence("thermal_evidence.txt", th_content)
            else:
                observed_props["probe_error_thermal"] = f"Exit code {code_th}: {err_th or out_th}"

        if zones:
            observed_props["thermal_zones_readable_count"] = len(zones)

        # 6. dumpsys battery
        code_bat, out_bat, err_bat = self._adb_cmd(["shell", "dumpsys", "battery"])
        if code_bat == 0:
            _save_evidence("battery_dumpsys_evidence.txt", out_bat)
            bat_parsed = self.parse_dumpsys_battery(out_bat)
            observed_props.update(bat_parsed)
        else:
            observed_props["probe_error_battery"] = f"Exit code {code_bat}: {err_bat or out_bat}"

        # 7. cpufreq
        ok_freq, out_freq = self.read_file(self.probes["cpufreq_sysfs_pattern"] % 0)
        if ok_freq and out_freq.strip():
            _save_evidence("cpufreq_evidence.txt", out_freq)
            try:
                observed_props["cpu_scaling_cur_freq"] = int(out_freq.strip())
            except ValueError:
                observed_props["probe_error_cpufreq"] = f"Failed to parse cpufreq node value: '{out_freq.strip()}'"
        else:
            observed_props["probe_error_cpufreq"] = f"Failed to read cpufreq node: {out_freq}"

        # 8. GPU sysfs / dumpsys
        ok_gpu, out_gpu = self.read_file(self.probes["kgsl_gpu_clock_path"])
        if ok_gpu and out_gpu.strip():
            _save_evidence("gpu_evidence.txt", out_gpu)
            try:
                observed_props["gpu_clock_hz"] = int(out_gpu.strip())
            except ValueError:
                observed_props["probe_error_gpu"] = f"Failed to parse kgsl gpuclk node value: '{out_gpu.strip()}'"
        else:
            observed_props["probe_error_gpu"] = f"Failed to read kgsl gpuclk node: {out_gpu}"

        # 9. Camera dumpsys
        code_cam, out_cam, err_cam = self._adb_cmd(["shell", "dumpsys", "media.camera"])
        if code_cam == 0:
            _save_evidence("camera_dumpsys_evidence.txt", out_cam)
            # A9: host cross-check only. Camera statuses come from the app's CameraCharacteristics probe.
            parsed_cam = host_probes.parse_camera_dumpsys(out_cam)
            _save_json_evidence("camera_host_evidence.json", {
                "source": "adb shell dumpsys media.camera (parsed from camera_dumpsys_evidence.txt)",
                "role": "host cross-check; not a substitute for the app CameraCharacteristics probe",
                "devices": parsed_cam,
            })
            observed_props["host_camera_dumpsys"] = parsed_cam
        else:
            observed_props["probe_error_camera"] = f"Exit code {code_cam}: {err_cam or out_cam}"

        # 9a. CPU frequency observability per CPU group (A7): scaling_cur/scaling_max/cpuinfo_max per policy.
        policy_dir = self.probes["cpufreq_policy_dir"]
        listing = self.probe_command(["ls", policy_dir])
        policies = host_probes.parse_policy_listing(listing["stdout"]) if listing["outcome"] == host_probes.READABLE else []
        policy_reads: Dict[str, Dict[str, Any]] = {}
        for pol in policies:
            for fname in self.probes["cpufreq_policy_files"]:
                rec = self.probe_path(f"{policy_dir}/{pol}/{fname}")
                rec["value"] = host_probes.parse_int_node(rec["stdout"]) if rec["outcome"] == host_probes.READABLE else None
                if rec["outcome"] == host_probes.READABLE and rec["value"] is None:
                    rec["outcome"] = host_probes.ERROR
                    rec["parse_error"] = "content is not a single integer"
                policy_reads.setdefault(pol, {})[fname] = rec
        _save_json_evidence("cpufreq_policy_evidence.json", {"policy_listing": listing, "policies": policy_reads})
        observed_props["cpufreq_policy_probe"] = {
            "listing_outcome": listing["outcome"],
            "policies": {pol: {f: {"outcome": r["outcome"], "value": r.get("value")} for f, r in files.items()}
                         for pol, files in policy_reads.items()},
        }

        # 9b. GPU busy counters (A6): readability of the configured kgsl gpubusy node; no utilisation claim.
        busy = self.probe_path(self.probes["kgsl_gpu_busy_path"])
        busy["parsed"] = host_probes.parse_gpubusy(busy["stdout"]) if busy["outcome"] == host_probes.READABLE else None
        if busy["outcome"] == host_probes.READABLE and busy["parsed"] is None:
            busy["outcome"] = host_probes.ERROR
            busy["parse_error"] = "content is not two integer counters"
        _save_json_evidence("gpu_busy_evidence.json", busy)
        observed_props["gpu_busy_probe"] = {"outcome": busy["outcome"], "target": busy["target"]}

        # 9b'. GPU memory: readability of the configured candidate KGSL allocation nodes. A readable node's raw
        # integer is kept as reported; unit and meaning are not interpreted. Nothing is defaulted.
        mem_reads = []
        for path in self.probes["kgsl_gpu_memory_paths"]:
            rec = self.probe_path(path)
            rec["value"] = host_probes.parse_int_node(rec["stdout"]) if rec["outcome"] == host_probes.READABLE else None
            if rec["outcome"] == host_probes.READABLE and rec["value"] is None:
                rec["outcome"] = host_probes.ERROR
                rec["parse_error"] = "content is not a single integer"
            mem_reads.append(rec)
        mem_outcome = host_probes.aggregate_outcomes([r["outcome"] for r in mem_reads])
        _save_json_evidence("gpu_memory_evidence.json", {"aggregate_outcome": mem_outcome, "paths": mem_reads})
        observed_props["gpu_memory_probe"] = {
            "outcome": mem_outcome,
            "target": ", ".join(r["target"] for r in mem_reads),
            "paths": [{"target": r["target"], "outcome": r["outcome"], "value": r["value"]} for r in mem_reads],
        }

        # 9c. PSI memory pressure (A5) and kernel release.
        psi = self.probe_path(self.probes["psi_memory_path"])
        psi["parsed"] = host_probes.parse_psi(psi["stdout"]) if psi["outcome"] == host_probes.READABLE else None
        if psi["outcome"] == host_probes.READABLE and psi["parsed"] is None:
            psi["outcome"] = host_probes.ERROR
            psi["parse_error"] = "content is not in PSI format"
        kernel = self.probe_command(self.probes["kernel_release_command"])
        _save_json_evidence("psi_memory_evidence.json", {"psi": psi, "kernel_release": kernel})
        observed_props["psi_memory_probe"] = {"outcome": psi["outcome"], "target": psi["target"]}
        observed_props["kernel_release"] = kernel["stdout"].strip() if kernel["outcome"] == host_probes.READABLE else None

        # 9d. GPU renderer identity from SurfaceFlinger (A8 host source; the app EGL probe is preferred).
        code_sf, out_sf, err_sf = self._adb_cmd(["shell", "dumpsys", "SurfaceFlinger"])
        gles = host_probes.parse_surfaceflinger_gles(out_sf) if code_sf == 0 else None
        gles_lines = [ln for ln in (out_sf or "").splitlines() if "GLES" in ln]
        _save_evidence("gpu_renderer_evidence.txt",
                       "COMMAND: adb shell dumpsys SurfaceFlinger (lines containing 'GLES' only)\n"
                       f"Exit Code: {code_sf}\nSTDERR:\n{err_sf}\nGLES LINES:\n" + "\n".join(gles_lines) + "\n")
        if code_sf != 0:
            observed_props["probe_error_surfaceflinger"] = f"Exit code {code_sf}: {err_sf or out_sf}"
        observed_props["host_gles"] = gles

        # 10. Profiling probe (R-02)
        atrace_avail, _ = self.probe_profiling_capability(ev_dir)
        files_saved.append(ev_dir / "atrace_evidence.txt")
        data_bytes = (ev_dir / "atrace_evidence.txt").read_bytes()
        manifest_entries.append({
            "relative_path": "evidence/atrace_evidence.txt",
            "size_bytes": len(data_bytes),
            "sha256": hashlib.sha256(data_bytes).hexdigest(),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })
        observed_props["atrace_adb_available"] = atrace_avail

        # 11. Network state probe (R-07)
        net_state, _ = self.probe_network_state(ev_dir)
        files_saved.append(ev_dir / "network_evidence.txt")
        data_bytes = (ev_dir / "network_evidence.txt").read_bytes()
        manifest_entries.append({
            "relative_path": "evidence/network_evidence.txt",
            "size_bytes": len(data_bytes),
            "sha256": hashlib.sha256(data_bytes).hexdigest(),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })
        observed_props["network_state"] = net_state

        # 12. On-device Android app output retrieval (P-03 integration)
        app_status, app_parsed = self.retrieve_android_app_output(ev_dir, manifest_entries)
        observed_props["app_output_status"] = app_status
        if app_status == "APP_OUTPUT_COLLECTED" and app_parsed:
            files_saved.append(ev_dir / "android_app_evidence.json")
            # Normalize nested Android app JSON schema produced by CharacterizationRunner.kt
            observed_props["app_telemetry"] = app_parsed
            full = self._normalize_app_output_full(app_parsed)
            observed_props["app_records"] = full["records"]
            observed_props["app_camera_records"] = full["camera_records"]
            observed_props["app_backend_records"] = full["backend_records"]
            if full["unrecognised"]:
                observed_props["app_unrecognised_items"] = full["unrecognised"]
            self._merge_app_observations(observed_props, self._normalize_app_output(app_parsed))

        # 12b. Researcher-provided evidence handed in by the orchestrator (e.g. energy feasibility, D-16).
        for name, data in (extra_evidence or {}).items():
            _save_evidence(name, data)

        # 13. Boot ID
        observed_props["boot_id"] = self.get_boot_id()

        # 14. Save command log (R-03)
        cmd_log_json = json.dumps(self.command_logs, indent=2)
        _save_evidence("commands.log", cmd_log_json)

        # 15. Write observed_props.json (R-01)
        observed_props["source_evidence_manifest"] = manifest_entries
        observed_props_json = json.dumps(observed_props, indent=2)
        _save_evidence("observed_props.json", observed_props_json)

        # 16. Write manifest.json (R-01, R-07)
        manifest_file = ev_dir / "manifest.json"
        manifest_bytes = json.dumps(manifest_entries, indent=2).encode("utf-8")
        manifest_file.write_bytes(manifest_bytes)
        files_saved.append(manifest_file)
        observed_props["manifest_sha256"] = hashlib.sha256(manifest_bytes).hexdigest()

        return files_saved, observed_props
