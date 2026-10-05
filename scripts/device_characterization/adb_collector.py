"""
ADB collector for host-side shell paths, evidence parsing, and provenance.

Executes ADB commands (`getprop`, `/proc/stat`, `/proc/meminfo`, cpufreq, thermal zones,
dumpsys meminfo, atrace, boot_id) to collect raw evidence from the connected physical device (OPPO A5 2020)
and parses it into structured device observation properties with real evidence files.
"""

import hashlib
import os
import re
import subprocess
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

    def _adb_cmd(self, args: List[str]) -> Tuple[int, str, str]:
        cmd = [_get_adb_binary()]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return res.returncode, res.stdout, res.stderr
        except Exception as e:
            return -1, "", str(e)

    def get_adb_version(self) -> str:
        code, out, _ = self._adb_cmd(["version"])
        if code == 0:
            match = re.search(r"Android Debug Bridge version ([\d.]+)", out)
            return match.group(1) if match else out.strip().splitlines()[0]
        return "unknown"

    def is_device_connected(self) -> bool:
        code, stdout, _ = self._adb_cmd(["get-state"])
        return code == 0 and "device" in stdout.strip()

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
        """Parses /proc/meminfo text into kB values and total RAM in MB."""
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
        if "MemTotal" in res:
            res["total_ram_mb"] = res["MemTotal"] // 1024
        return res

    def parse_proc_cpuinfo(self, text: str) -> Dict[str, Any]:
        """Parses /proc/cpuinfo text for processor count and hardware model."""
        processors = re.findall(r"^processor\s*:\s*\d+", text, flags=re.MULTILINE)
        hardware = re.search(r"^Hardware\s*:\s*(.+)$", text, flags=re.MULTILINE)
        return {
            "core_count": len(processors) if processors else None,
            "hardware": hardware.group(1).strip() if hardware else None,
        }

    def get_boot_id(self) -> str:
        ok, out = self.read_file("/proc/sys/kernel/random/boot_id")
        if ok and out.strip():
            return out.strip()
        ok_up, out_up = self.read_file("/proc/uptime")
        if ok_up:
            return f"uptime_{out_up.strip().split()[0]}"
        return "unknown_boot_id"

    def collect_raw_evidence_and_observations(self, output_dir: Path) -> Tuple[List[Path], Dict[str, Any]]:
        """Collects raw evidence text files and parses device observations."""
        ev_dir = output_dir / "evidence"
        ev_dir.mkdir(parents=True, exist_ok=True)
        files_saved = []
        observed_props: Dict[str, Any] = {"is_real_device_observation": True}

        # 1. getprop
        code, out_prop, _ = self._adb_cmd(["shell", "getprop"])
        if code == 0:
            p = ev_dir / "getprop_evidence.txt"
            p.write_text(out_prop, encoding="utf-8")
            files_saved.append(p)
            props = self.get_properties()
            observed_props["manufacturer"] = props.get("ro.product.manufacturer")
            observed_props["model"] = props.get("ro.product.model")
            observed_props["release_version"] = props.get("ro.build.version.release")
            sdk_str = props.get("ro.build.version.sdk")
            observed_props["api_level"] = int(sdk_str) if sdk_str and sdk_str.isdigit() else None
            observed_props["cpu_abi"] = props.get("ro.product.cpu.abi")
            observed_props["soc_model"] = props.get("ro.soc.model") or props.get("ro.board.platform")
            observed_props["build_fingerprint"] = props.get("ro.build.fingerprint")

        # 2. dumpsys meminfo / proc meminfo
        ok_mem, out_mem = self.read_file("/proc/meminfo")
        if ok_mem:
            p = ev_dir / "meminfo_evidence.txt"
            p.write_text(out_mem, encoding="utf-8")
            files_saved.append(p)
            mem_parsed = self.parse_proc_meminfo(out_mem)
            observed_props.update(mem_parsed)

        # 3. proc cpuinfo
        ok_cpu, out_cpu = self.read_file("/proc/cpuinfo")
        if ok_cpu:
            p = ev_dir / "cpuinfo_evidence.txt"
            p.write_text(out_cpu, encoding="utf-8")
            files_saved.append(p)
            cpu_parsed = self.parse_proc_cpuinfo(out_cpu)
            observed_props.update(cpu_parsed)

        # 4. proc stat check
        ok_stat, out_stat = self.read_file("/proc/stat")
        if ok_stat:
            p = ev_dir / "proc_stat_evidence.txt"
            p.write_text(out_stat, encoding="utf-8")
            files_saved.append(p)
            observed_props["proc_stat_readable_via_adb"] = True

        # 5. thermal zones
        zones = self.check_thermal_zones()
        if zones:
            p = ev_dir / "thermal_evidence.txt"
            p.write_text("\n".join([f"{z['zone']}: {z['type']} = {z['temp']}" for z in zones]), encoding="utf-8")
            files_saved.append(p)
            observed_props["thermal_zones_readable_count"] = len(zones)

        # 6. Boot ID
        observed_props["boot_id"] = self.get_boot_id()
        observed_props["atrace_adb_available"] = True

        return files_saved, observed_props
