# Smartphone Requirements — GC-03

_Step 10B, 2026-10-05, Claude Code. Research design only._

> **Step 10C update (2026-10-05): gate G1 CLOSED.** The researcher confirmed the actual experimental device: **OPPO A5 2020, 3 GB RAM variant** (Snapdragon 665, Adreno 610; Android 9 / ColorOS at launch). The 4 GB and 6 GB variants are not the experimental device. Its capabilities against the requirements below are still **REQUIRES DEVICE VERIFICATION**, and the installed Android version is unknown. See [`measurement_protocol.md`](../experiments/measurement_protocol.md) §1. The rest of this document records the Step 10B requirement analysis. Its pre-confirmation status lines are kept as an audit trail.

**No smartphone is selected and none is claimed to be available.** _(Step 10B status, superseded by the update above.)_

**ACTUAL DEVICE — REQUIRES RESEARCHER CONFIRMATION.** A repository search (2026-10-05) of all non-literature files (configs, docs, `PROJECT_SPEC.md`, `mobile/`, `research/` outside the literature and gap-analysis records) found no documented device owned by or available to the project. Until the researcher records an actual device (exact model and source), no phone is selected (gate G1 in [`verification_checklist.md`](verification_checklist.md)).
- The repository does not specify an available device. The phones named in `docs/agent_sync/CHANGELOG.md` and `research/gap_analysis/` belong to papers in the literature corpus, not to this project.
- This document therefore gives **DEVICE REQUIREMENTS** and a shortlist of candidate device *classes*.
- Choosing a specific device needs the researcher to confirm which hardware is available ([`verification_checklist.md`](verification_checklist.md) §3).

**Evidence for Android facts.**
- **SUPPORTED (reference read 2026-10-05):** statements about `PowerManager`, `BatteryManager` and `HardwarePropertiesManager`, checked against their developer.android.com reference pages.
  - `getCurrentThermalStatus()` was added at API 29 and `getThermalHeadroom()` at API 30.
  - `BATTERY_PROPERTY_CURRENT_NOW` is in microamperes; `BATTERY_PROPERTY_ENERGY_COUNTER` is remaining energy in nanowatt-hours.
  - `getDeviceTemperatures()` throws `SecurityException` for callers other than the device owner or the current VR service.
- **PROVISIONAL (agent knowledge, not re-read in this step):** all other platform statements, including Perfetto power rails, `/proc/stat` restrictions, sysfs access, NNAPI deprecation and Camera2 capability levels.
- None of these has been verified on a device. Availability, units and sampling behaviour vary by manufacturer and must be checked on the chosen device.

## 1. Device Requirements

| Field | Requirement | Why | Status |
| :-- | :-- | :-- | :-- |
| Device | One physical Android smartphone, a single unit for all runs; the unit ID is logged. | Device model is a control variable (`variables_and_factors.md` §4). | REQUIRES_VERIFICATION (no device known) |
| Manufacturer | Any. Prefer one whose telemetry interfaces are documented (§3). | Telemetry access differs by vendor. | PROVISIONAL |
| Model | Not selected. | No evidence of an available device. | REQUIRES_VERIFICATION |
| SoC | Must offer a CPU path and at least one accelerator path (GPU, and NPU/DSP if available) usable by the chosen runtime. | C1–C4 may differ in backend. | REQUIRES_VERIFICATION |
| CPU | Multi-core ARM64 (arm64-v8a). | Runtime builds target arm64. | PROVISIONAL |
| GPU | Supported by the TFLite (LiteRT) GPU delegate or ONNX Runtime / ExecuTorch GPU backends. | Accelerated configurations. | REQUIRES_VERIFICATION |
| NPU | Optional. If present, a runtime backend must expose it (e.g. vendor delegate or execution provider). | Possible C1/C2 backend; not required. | REQUIRES_VERIFICATION |
| RAM | Enough to hold the largest configuration (C1), the camera pipeline and a resident escalation model (A3). Exact need: REQUIRES EMPIRICAL BENCHMARKING. | Memory pressure is a resource condition; C1 must fit at R0. | REQUIRES_VERIFICATION |
| Storage | Room for models, logs and (Stage 2) captured images. Not a constraint at research scale. | Logging. | PROVISIONAL |
| Android version | API level 30 (Android 11) or later preferred: `PowerManager.getThermalHeadroom()` was added at API 30, and `getCurrentThermalStatus()` at API 29. | Thermal state (R-state input). | SUPPORTED (reference read 2026-10-05) |
| Camera | Rear camera whose Camera2 characteristics report the `MANUAL_SENSOR` capability (and manual post-processing / AF control as needed), so exposure, focus and white balance can be locked; `FULL` or `LEVEL_3` hardware level is the usual indicator. | Camera parameters are control variables. | REQUIRES_VERIFICATION |
| Battery capacity | Recorded; no minimum. Battery health is recorded at the start of each experiment. | Battery state is part of R0–R3. | PROVISIONAL |
| Thermal sensors | Thermal-status API required; per-sensor temperatures desirable (§3). | R-state; thermal outcome. | REQUIRES_VERIFICATION |
| CPU utilisation access | Per-process CPU time from the app; device-wide via ADB / Perfetto (§3). | Resource-condition manipulation check. | CONDITIONALLY_AVAILABLE |
| GPU utilisation access | No public Android API; vendor-specific or profiler-based (§3). | Manipulation check for GPU load. | CONDITIONALLY_AVAILABLE |
| RAM telemetry | `ActivityManager.MemoryInfo` (available, total, low-memory flag); per-process memory via `Debug`. | Memory condition and DV. | AVAILABLE (platform API; verify values) |
| Battery telemetry | `BatteryManager` properties and `ACTION_BATTERY_CHANGED` extras (§3). | Battery condition; energy proxy. | AVAILABLE (platform API; vendor support varies) |
| Temperature telemetry | Battery temperature via `ACTION_BATTERY_CHANGED`; other sensors conditional (§3). | Thermal DV. | CONDITIONALLY_AVAILABLE |
| Power/energy options | Software counters plus external instrumentation ([`measurement_hardware.md`](measurement_hardware.md) §2). | Energy DV. | EXTERNAL-METER VALIDATION REQUIRED |
| Runtime support | At least one of TFLite/LiteRT, ONNX Runtime Mobile or ExecuTorch, running all of C1–C4 offline. | Deployment of the ladder. | REQUIRES_VERIFICATION |
| Hardware acceleration | The accelerator backend must actually execute the model graph. Partial delegation and silent CPU fallback must be detectable and logged. | Configuration identity. | REQUIRES_VERIFICATION |
| Offline inference | Required. No network during runs; flight mode logged. | Cloud inference is out of scope; network adds energy noise. | PROVISIONAL |
| Camera API | Camera2 (or CameraX on Camera2) with per-frame metadata (`CaptureResult`). | Logging camera parameters. | PROVISIONAL (agent knowledge) |
| Multi-view capture | Single rear camera with a jig or turntable providing views. Multi-camera hardware is not required. | A2 and A1 in Stage 2. | PROVISIONAL |

**Runtime notes** (PROVISIONAL, agent knowledge; unverified on device):
- NNAPI is deprecated from Android 15. A design that depends on NNAPI should prefer a GPU delegate or a vendor-specific backend.
- Each runtime's delegate coverage depends on the operators in the model. Coverage must be checked per configuration.

## 2. Candidate Device Classes (shortlist)

**These are requirement classes only, not device selections.** No specific model is named as available. Per the project vision (`PROJECT_SPEC.md` §1), the classes cover a "resource-constrained" and possibly legacy phone.

| Class | Rationale | Expected telemetry advantage | Risk | Status |
| :-- | :-- | :-- | :-- | :-- |
| **D1. Google Pixel class (recent, stock Android)** | Stock Android, current API levels, Perfetto support. | Some Pixel models expose on-device power-rail monitors through Perfetto (vendor support REQUIRES_VERIFICATION per model). | Higher-end than "resource-constrained"; may throttle less. | PROVISIONAL |
| **D2. Mid-range Qualcomm Snapdragon class** | Widely available; Adreno GPU; vendor NPU (Hexagon) via vendor backends. | Vendor GPU counters through profiling tools (REQUIRES_VERIFICATION). | Vendor Android variants may restrict sysfs access. | PROVISIONAL |
| **D3. Low-cost / legacy class (repurposed phone)** | Matches the "repurpose legacy smartphones" vision and makes resource pressure easy to reach. | Possibly older API level (no `getThermalHeadroom` below API 30). | Weaker telemetry; may lack an accelerator path. | PROVISIONAL |

**Selection rule (PROVISIONAL).** Choose the most resource-constrained device that still meets the mandatory requirements:
- API ≥ 29 thermal status;
- Camera2 manual controls;
- every C1–C4 deployable offline;
- battery telemetry;
- compatibility with an external energy reference.

GC-03 concerns *resource-constrained* phones, so D3 or D2 are preferred over D1 if they pass. **If no available device meets the mandatory requirements, the gap cannot be tested as specified, and the researcher must decide on a relaxation.**

## 3. Telemetry Access Classification

Classes: **AVAILABLE**, **CONDITIONALLY_AVAILABLE**, **UNAVAILABLE**, **REQUIRES_EXTERNAL_INSTRUMENTATION**. Classification rests on platform documentation or agent knowledge (see the evidence note above), never on a device test, and must be verified on the chosen device. **AVAILABLE** means a public API exists, not that the values are accurate.

| Signal | Source | Class | Notes |
| :-- | :-- | :-- | :-- |
| Battery percentage | `BatteryManager.BATTERY_PROPERTY_CAPACITY`; `ACTION_BATTERY_CHANGED` level/scale | AVAILABLE | Coarse (integer percent); a fuel-gauge estimate. |
| Battery voltage | `ACTION_BATTERY_CHANGED` `EXTRA_VOLTAGE` | AVAILABLE | Update rate set by the system broadcast. |
| Battery current | `BATTERY_PROPERTY_CURRENT_NOW`, `CURRENT_AVERAGE` | CONDITIONALLY_AVAILABLE | Sign convention, units and refresh rate vary by vendor; may be unsupported. |
| Charge / energy counters | `BATTERY_PROPERTY_CHARGE_COUNTER`; `ENERGY_COUNTER` | CONDITIONALLY_AVAILABLE | `ENERGY_COUNTER` is often unsupported; charge-counter resolution is device-specific. |
| CPU utilisation (own process) | Process CPU time (`/proc/self/stat`, `Process.getElapsedCpuTime()`) | AVAILABLE | Own process only. |
| CPU utilisation (device-wide) | `/proc/stat` (restricted to apps since Android 8); ADB `dumpsys cpuinfo`, `top`, Perfetto | CONDITIONALLY_AVAILABLE | Needs a host-side ADB/Perfetto session, not the app alone. |
| CPU frequency | `/sys/devices/system/cpu/*/cpufreq/*`; Perfetto | CONDITIONALLY_AVAILABLE | Readability depends on SELinux policy. |
| GPU utilisation | No public API; vendor sysfs via ADB; Perfetto GPU counters / Android GPU Inspector on supported devices | CONDITIONALLY_AVAILABLE | May be UNAVAILABLE on the chosen device. |
| RAM | `ActivityManager.MemoryInfo`; `Debug.getMemoryInfo()` | AVAILABLE | |
| CPU / SoC temperature | Thermal zones (`/sys/class/thermal`) via ADB; `HardwarePropertiesManager.getDeviceTemperatures()` | CONDITIONALLY_AVAILABLE | `HardwarePropertiesManager.getDeviceTemperatures()` throws `SecurityException` unless the caller is the device owner or the current VR service (reference read); app access to thermal zones is often blocked. |
| Device / skin temperature | `HardwarePropertiesManager` (`DEVICE_TEMPERATURE_SKIN`), vendor thermal zones | CONDITIONALLY_AVAILABLE | External surface probe as the reference ([`measurement_hardware.md`](measurement_hardware.md) §3). |
| Battery temperature | `ACTION_BATTERY_CHANGED` `EXTRA_TEMPERATURE` (tenths of °C) | AVAILABLE | Lags SoC temperature. |
| Thermal status / headroom | `PowerManager.getCurrentThermalStatus()` (API 29), `getThermalHeadroom()` (API 30), status listener | AVAILABLE (API-level dependent) | A *state*, not a temperature. |
| Power-save mode | `PowerManager.isPowerSaveMode()` | AVAILABLE | |
| Inference latency | Monotonic in-app timing around each stage | AVAILABLE | Measured, never estimated. |
| FPS / throughput | Derived from timestamps | AVAILABLE | |
| Model load time | In-app timing of model initialisation and delegate creation | AVAILABLE | Logged separately from steady-state latency. |
| Absolute energy | External power reference | REQUIRES_EXTERNAL_INSTRUMENTATION | See [`measurement_hardware.md`](measurement_hardware.md) §2. |
| Ambient temperature | External thermometer | REQUIRES_EXTERNAL_INSTRUMENTATION | |

## 4. Status

| Item | Status |
| :-- | :-- |
| Specific device | ACTUAL DEVICE — REQUIRES RESEARCHER CONFIRMATION (gate G1) |
| Device availability | Not claimed; no repository evidence of an available device |
| D1–D3 | Requirement classes only |
| Requirements table | PROVISIONAL |
| Telemetry classification | SUPPORTED (three reference pages) / PROVISIONAL (other sources); device verification required |
