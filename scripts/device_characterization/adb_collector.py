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


def _get_adb_binary() -> str:
    sdk_adb = os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe")
    if os.path.exists(sdk_adb):
        return sdk_adb
    return "adb"


class ADBCollector:
    """Host-side ADB collector for querying connected Android device shell paths."""

    def __init__(self, device_id: Optional[str] = None, timeout_seconds: int = 15):
        self.device_id = device_id
        self.timeout = timeout_seconds
        self.command_logs: List[Dict[str, Any]] = []

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
        for i in range(10):
            t_path = f"/sys/class/thermal/thermal_zone{i}/type"
            v_path = f"/sys/class/thermal/thermal_zone{i}/temp"
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
        for line in text.splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if k == "level":
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
                        pass
        if "charging_state" not in res:
            res["charging_state"] = False
        return res

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

    def _normalize_app_output(self, app_parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes the nested JSON schema produced by CharacterizationRunner.kt."""
        norm: Dict[str, Any] = {}
        if not isinstance(app_parsed, dict):
            return norm

        for section_name in ["device_identity", "memory_telemetry", "battery_telemetry", "camera_telemetry"]:
            section = app_parsed.get(section_name)
            if isinstance(section, list):
                for item in section:
                    if isinstance(item, dict) and "metric" in item:
                        m = item["metric"]
                        v = item.get("value")
                        unit = item.get("unit")
                        norm[m] = v
                        if unit:
                            norm[f"{m}_unit"] = unit
                        norm[f"{m}_app_item"] = item
            elif isinstance(section, dict):
                for m, v in section.items():
                    norm[m] = v

        thermal = app_parsed.get("thermal_capability")
        if isinstance(thermal, dict):
            if "metric" in thermal:
                norm[thermal["metric"]] = thermal.get("value")
            for k, v in thermal.items():
                if k not in norm:
                    norm[k] = v
        elif isinstance(thermal, list):
            for item in thermal:
                if isinstance(item, dict) and "metric" in item:
                    norm[item["metric"]] = item.get("value")

        for k, v in app_parsed.items():
            if k not in norm and k not in ["run_id", "observed_at"]:
                norm[k] = v

        return norm

    def collect_raw_evidence_and_observations(self, output_dir: Path) -> Tuple[List[Path], Dict[str, Any]]:
        """Collects raw evidence text files, writes observed_props.json & manifest.json."""
        ev_dir = output_dir / "evidence"
        ev_dir.mkdir(parents=True, exist_ok=True)
        files_saved = []
        observed_props: Dict[str, Any] = {"is_real_device_observation": True}
        manifest_entries: List[Dict[str, Any]] = []

        def _save_evidence(filename: str, content: str) -> Path:
            p = ev_dir / filename
            data_bytes = content.encode("utf-8")
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
        ok_freq, out_freq = self.read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
        if ok_freq:
            _save_evidence("cpufreq_evidence.txt", out_freq)
            try:
                observed_props["cpu_scaling_cur_freq"] = int(out_freq.strip())
            except ValueError:
                pass
        else:
            observed_props["probe_error_cpufreq"] = f"Failed to read cpufreq node: {out_freq}"

        # 8. GPU sysfs / dumpsys
        ok_gpu, out_gpu = self.read_file("/sys/class/kgsl/kgsl-3d0/gpuclk")
        if ok_gpu:
            _save_evidence("gpu_evidence.txt", out_gpu)
            try:
                observed_props["gpu_clock_hz"] = int(out_gpu.strip())
            except ValueError:
                pass
        else:
            observed_props["probe_error_gpu"] = f"Failed to read kgsl gpuclk node: {out_gpu}"

        # 9. Camera dumpsys
        code_cam, out_cam, err_cam = self._adb_cmd(["shell", "dumpsys", "media.camera"])
        if code_cam == 0:
            _save_evidence("camera_dumpsys_evidence.txt", out_cam)
        else:
            observed_props["probe_error_camera"] = f"Exit code {code_cam}: {err_cam or out_cam}"

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
            norm_app = self._normalize_app_output(app_parsed)
            observed_props["app_telemetry"] = app_parsed
            for k, v in norm_app.items():
                if k not in observed_props or observed_props[k] is None:
                    observed_props[k] = v

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
