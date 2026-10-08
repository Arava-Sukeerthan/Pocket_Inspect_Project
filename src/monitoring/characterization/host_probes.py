"""
Pure host-probe helpers for Step 10D (no ADB, no I/O): outcome classification and text parsers.

The ADB collector (scripts/device_characterization/adb_collector.py) runs the shell commands and stores the
raw output as evidence; this module turns that raw output into structured observations. Keeping the logic
here makes it unit-testable without a device.

Probe outcomes (one per attempted file read or command), never collapsed into a single boolean:
- READABLE: the command succeeded and returned content.
- ABSENT: the path does not exist ("No such file or directory").
- PERMISSION_DENIED: the path exists but SELinux/DAC refused the read.
- ERROR: anything else (non-zero exit without a recognised reason, empty output, transport failure).
"""

import re
from typing import Any, Dict, List, Optional

READABLE = "READABLE"
ABSENT = "ABSENT"
PERMISSION_DENIED = "PERMISSION_DENIED"
ERROR = "ERROR"
PROBE_OUTCOMES = (READABLE, ABSENT, PERMISSION_DENIED, ERROR)

# Runtime state each outcome maps to (protocol §3): absent path -> UNAVAILABLE, permission -> PERMISSION_REQUIRED.
OUTCOME_TO_STATE = {
    READABLE: "AVAILABLE",
    ABSENT: "UNAVAILABLE",
    PERMISSION_DENIED: "PERMISSION_REQUIRED",
    ERROR: "ERROR",
}


def classify_shell_read(exit_code: int, stdout: str, stderr: str) -> str:
    """Classifies one `adb shell cat <path>` (or similar) result into a probe outcome.

    Error text is matched in both streams because adb without the shell-v2 protocol folds stderr into stdout.
    """
    text = f"{stdout or ''}\n{stderr or ''}"
    if "No such file or directory" in text:
        return ABSENT
    if "Permission denied" in text or "Operation not permitted" in text:
        return PERMISSION_DENIED
    if exit_code == 0 and (stdout or "").strip():
        return READABLE
    return ERROR


def probe_record(path_or_cmd: str, exit_code: int, stdout: str, stderr: str) -> Dict[str, Any]:
    """Structured evidence for one probe: command/path, exit code, raw streams and outcome."""
    outcome = classify_shell_read(exit_code, stdout, stderr)
    return {
        "target": path_or_cmd,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "outcome": outcome,
    }


def aggregate_outcomes(outcomes: List[str]) -> str:
    """One outcome for a set of candidate paths answering the same item.

    READABLE if any path was readable; otherwise ERROR if any read failed unexpectedly (re-run required);
    otherwise PERMISSION_DENIED if any existing path was refused; ABSENT only when every path is absent.
    An empty list is ERROR (nothing was probed).
    """
    for outcome in (READABLE, ERROR, PERMISSION_DENIED, ABSENT):
        if outcome in outcomes:
            return outcome
    return ERROR


def parse_int_node(text: str) -> Optional[int]:
    """Parses a single-integer sysfs node; None if the content is not one integer."""
    stripped = (text or "").strip()
    return int(stripped) if re.fullmatch(r"-?\d+", stripped) else None


def parse_gpubusy(text: str) -> Optional[Dict[str, int]]:
    """Parses kgsl `gpubusy` ("<busy> <total>"). Returns the two raw counters, never a utilisation figure."""
    parts = (text or "").split()
    if len(parts) == 2 and all(re.fullmatch(r"-?\d+", p) for p in parts):
        return {"busy": int(parts[0]), "total": int(parts[1])}
    return None


def parse_psi(text: str) -> Optional[Dict[str, Dict[str, float]]]:
    """Parses /proc/pressure/memory ("some avg10=.. avg60=.. avg300=.. total=.."; "full ...")."""
    out: Dict[str, Dict[str, float]] = {}
    for line in (text or "").splitlines():
        fields = line.split()
        if not fields or fields[0] not in ("some", "full"):
            continue
        vals: Dict[str, float] = {}
        for f in fields[1:]:
            if "=" in f:
                k, v = f.split("=", 1)
                try:
                    vals[k] = float(v)
                except ValueError:
                    return None
        out[fields[0]] = vals
    return out or None


def parse_policy_listing(text: str) -> List[str]:
    """Policy directory names (policyN) from `ls <cpufreq_policy_dir>`, sorted by N."""
    names = re.findall(r"\bpolicy\d+\b", text or "")
    return sorted(set(names), key=lambda n: int(n[len("policy"):]))


def parse_surfaceflinger_gles(text: str) -> Optional[Dict[str, str]]:
    """Parses the `GLES: <vendor>, <renderer>, <version>` line of `dumpsys SurfaceFlinger`."""
    for line in (text or "").splitlines():
        m = re.match(r"\s*GLES:\s*(.+)$", line)
        if not m:
            continue
        parts = [p.strip() for p in m.group(1).split(",")]
        if len(parts) >= 2 and parts[0] and parts[1]:
            return {"vendor": parts[0], "renderer": parts[1], "version": ", ".join(parts[2:]) or None,
                    "raw_line": line.strip()}
    return None


_FACING = {"0": "FRONT", "1": "BACK", "2": "EXTERNAL", "FRONT": "FRONT", "BACK": "BACK", "EXTERNAL": "EXTERNAL"}


def parse_camera_dumpsys(text: str) -> Dict[str, Dict[str, Any]]:
    """Best-effort parse of `dumpsys media.camera` static metadata, per camera device.

    Host cross-check only: the protocol's camera checks use CameraManager/CameraCharacteristics in the app.
    Extracts, where printed: lens facing and available capabilities. Unknown formats yield an empty dict.
    """
    devices: Dict[str, Dict[str, Any]] = {}
    current: Optional[str] = None
    pending_key: Optional[str] = None
    for raw in (text or "").splitlines():
        line = raw.strip()
        m = re.match(r"==\s*Camera device (\S+) static information", line)
        if m:
            current = m.group(1)
            devices.setdefault(current, {})
            pending_key = None
            continue
        if line.startswith("== ") and "static information" not in line:
            current = None if "Camera device" not in line else current
            pending_key = None
            continue
        if current is None:
            continue
        if line.startswith("android.lens.facing"):
            pending_key = "lens_facing"
            continue
        if line.startswith("android.request.availableCapabilities"):
            pending_key = "available_capabilities"
            continue
        if pending_key and line.startswith("["):
            tokens = line.strip("[]").split()
            if pending_key == "lens_facing" and tokens:
                devices[current]["lens_facing"] = _FACING.get(tokens[0].upper(), tokens[0])
            elif pending_key == "available_capabilities":
                devices[current].setdefault("available_capabilities", []).extend(tokens)
            pending_key = None
    return devices
