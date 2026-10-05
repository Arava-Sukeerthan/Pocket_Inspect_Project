"""
ADB collector for host-side shell paths and telemetry evidence.

Executes ADB commands (`getprop`, `/proc/stat`, `/proc/meminfo`, cpufreq, thermal zones,
dumpsys meminfo, atrace) to collect evidence from the connected physical device (OPPO A5 2020).
"""

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ADBCollector:
    """Host-side ADB collector for querying connected Android device shell paths."""

    def __init__(self, device_id: Optional[str] = None, timeout_seconds: int = 15):
        self.device_id = device_id
        self.timeout = timeout_seconds

    def _adb_cmd(self, args: List[str]) -> Tuple[int, str, str]:
        cmd = ["adb"]
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

    def collect_raw_evidence(self, output_dir: Path) -> List[Path]:
        """Collects raw evidence text files for device characterization run."""
        output_dir.mkdir(parents=True, exist_ok=True)
        files_saved = []

        # 1. getprop
        code, out, _ = self._adb_cmd(["shell", "getprop"])
        if code == 0:
            p = output_dir / "getprop_evidence.txt"
            p.write_text(out, encoding="utf-8")
            files_saved.append(p)

        # 2. dumpsys meminfo
        code, out, _ = self._adb_cmd(["shell", "dumpsys", "meminfo"])
        if code == 0:
            p = output_dir / "dumpsys_meminfo_evidence.txt"
            p.write_text(out, encoding="utf-8")
            files_saved.append(p)

        # 3. proc meminfo
        ok, out = self.read_file("/proc/meminfo")
        if ok:
            p = output_dir / "proc_meminfo_evidence.txt"
            p.write_text(out, encoding="utf-8")
            files_saved.append(p)

        # 4. proc cpuinfo
        ok, out = self.read_file("/proc/cpuinfo")
        if ok:
            p = output_dir / "proc_cpuinfo_evidence.txt"
            p.write_text(out, encoding="utf-8")
            files_saved.append(p)

        return files_saved
