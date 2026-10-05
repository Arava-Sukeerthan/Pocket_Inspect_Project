# Step 10D — Device Capability Matrix (Report Skeleton)

_Step 10D specification, 2026-10-05, Claude Code._

**Device: OPPO A5 2020, 3 GB RAM variant (experimental platform).**

Every observation column is **NOT YET VERIFIED**: nothing has been run on the physical device. Antigravity's characterization run fills the `Status` and `Evidence` columns. Claude Code reviews every change.

- "Expected class" comes from platform documentation or earlier steps. It is a prediction, not a finding.
- No value appears in this document.
- Status vocabulary: [`device_characterization_protocol.md`](device_characterization_protocol.md) §3.

## 1. Device Identity

| Item | Known specification | Observation source | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| Manufacturer | OPPO | `Build.MANUFACTURER` | NOT YET VERIFIED | — |
| Model | OPPO A5 2020 | `Build.MODEL`, `Build.DEVICE`, `Build.PRODUCT` (vendor model codes) | NOT YET VERIFIED | — |
| RAM variant | 3 GB LPDDR4X (4 GB / 6 GB variants excluded) | `ActivityManager.MemoryInfo.totalMem` with the nearest-variant check (protocol §2) | NOT YET VERIFIED | — |
| Storage | 64 GB | `StatFs` on the data partition | NOT YET VERIFIED | — |
| SoC | Qualcomm Snapdragon 665 | `Build.HARDWARE`, `Build.BOARD`; `Build.SOC_MODEL` only at API 31 or later (else API_UNSUPPORTED); `/proc/cpuinfo` | NOT YET VERIFIED | — |
| GPU | Adreno 610 | GLES `GL_RENDERER` / `GL_VENDOR` from an EGL context | NOT YET VERIFIED | — |
| Build | — | `Build.FINGERPRINT`, `Build.DISPLAY`, vendor ROM property via ADB `getprop` (conditional) | NOT YET VERIFIED | — |

## 2. Installed Android / API

| Item | Source | Expected class | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| Android version | `Build.VERSION.RELEASE` | AVAILABLE | NOT YET VERIFIED (launch version Android 9; installed version **not assumed**) | — |
| API level | `Build.VERSION.SDK_INT` | AVAILABLE | NOT YET VERIFIED | — |
| Security patch | `Build.VERSION.SECURITY_PATCH` | AVAILABLE | NOT YET VERIFIED | — |
| Thermal-status API (API ≥ 29) | `PowerManager.getCurrentThermalStatus()` | CONDITIONALLY AVAILABLE (depends on installed API) | NOT YET VERIFIED (**not assumed**) | — |
| Thermal headroom (API ≥ 30) | `PowerManager.getThermalHeadroom()` | CONDITIONALLY AVAILABLE | NOT YET VERIFIED | — |

## 3. Telemetry Capability Matrix

| Dimension | Metric | Interface | Min API / condition | Expected class | Verification method | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Battery | Percentage | `BATTERY_PROPERTY_CAPACITY`; `ACTION_BATTERY_CHANGED` level/scale | — | AVAILABLE | Compare both sources | NOT YET VERIFIED | — |
| Battery | Charging state / plug type | `ACTION_BATTERY_CHANGED` status, plugged; `isCharging()` | — | AVAILABLE | Plug and unplug check | NOT YET VERIFIED | — |
| Battery | Voltage | `EXTRA_VOLTAGE` | — | AVAILABLE | Unit check (mV) | NOT YET VERIFIED | — |
| Battery | Current | `BATTERY_PROPERTY_CURRENT_NOW`, `CURRENT_AVERAGE` | Unsupported sentinel when the app targets API ≥ 28 | CONDITIONALLY AVAILABLE | Sentinel check; sign convention when charging vs discharging; update interval | NOT YET VERIFIED | — |
| Battery | Charge / energy counter | `CHARGE_COUNTER`, `ENERGY_COUNTER` | Sentinel as above | CONDITIONALLY AVAILABLE | Sentinel check; monotonic change during discharge | NOT YET VERIFIED | — |
| Battery | Temperature | `EXTRA_TEMPERATURE` | — | AVAILABLE | Unit check (tenths of a degree) | NOT YET VERIFIED | — |
| Battery | Health / status | `EXTRA_HEALTH`, `EXTRA_STATUS` | — | AVAILABLE | Read | NOT YET VERIFIED | — |
| Battery | Power information | Derived only (current × voltage), never stored as measured power | Depends on current | CONDITIONALLY AVAILABLE | Requires E-level validation (§8) | NOT YET VERIFIED | — |
| Memory | Total / available RAM, threshold, low-memory flag | `ActivityManager.MemoryInfo` | — | AVAILABLE | Read; compare with ADB `dumpsys meminfo` | NOT YET VERIFIED | — |
| Memory | App / process memory | `Debug.getMemoryInfo()`, `getProcessMemoryInfo()` | — | AVAILABLE | Compare with ADB `dumpsys meminfo <pkg>` | NOT YET VERIFIED | — |
| Memory | Memory-pressure indicators | `onTrimMemory` levels; `/proc/meminfo` (app-readable: verify); PSI files (kernel-dependent) | — | CONDITIONALLY AVAILABLE | Readability check | NOT YET VERIFIED | — |
| CPU | Model / core count | `/proc/cpuinfo`; `Runtime.availableProcessors()`; cpufreq policy directories | — | AVAILABLE / CONDITIONALLY AVAILABLE | Read | NOT YET VERIFIED | — |
| CPU | Current / per-core frequency | `/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq` (app or ADB) | SELinux-dependent | CONDITIONALLY AVAILABLE | App read, then ADB read | NOT YET VERIFIED | — |
| CPU | Frequency limits | `cpuinfo_max_freq`, `scaling_max_freq` | SELinux-dependent | CONDITIONALLY AVAILABLE | Read both | NOT YET VERIFIED | — |
| CPU | Device-wide utilisation | `/proc/stat` (blocked for apps since API 26; ADB shell) | Host ADB | CONDITIONALLY AVAILABLE | App read expected to fail; ADB read | NOT YET VERIFIED | — |
| CPU | Process CPU time | `Process.getElapsedCpuTime()`; `/proc/self/stat` | — | AVAILABLE | Consistency check | NOT YET VERIFIED | — |
| GPU | Identification | GLES renderer/vendor/version; Vulkan physical-device properties | Vulkan support to verify | AVAILABLE / CONDITIONALLY AVAILABLE | Read | NOT YET VERIFIED | — |
| GPU | Utilisation | Adreno kernel-driver sysfs (`/sys/class/kgsl/kgsl-3d0/...`) via app or ADB; trace GPU counters | SELinux / driver dependent | CONDITIONALLY AVAILABLE or UNAVAILABLE | Readability check; if absent: **UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE** | NOT YET VERIFIED | — |
| GPU | Frequency | kgsl / devfreq sysfs via ADB | As above | CONDITIONALLY AVAILABLE or UNAVAILABLE | As above | NOT YET VERIFIED | — |
| GPU | Memory | No public API; driver-specific | — | Expected UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE | Check | NOT YET VERIFIED | — |
| Thermal | Thermal status / listener | `PowerManager` | API ≥ 29 | CONDITIONALLY AVAILABLE | API-level gate, then call | NOT YET VERIFIED | — |
| Thermal | Temperature sources | Battery temperature; `/sys/class/thermal/thermal_zone*/type,temp` (app or ADB); `HardwarePropertiesManager` (device owner / VR only) | — | Battery AVAILABLE; zones CONDITIONALLY AVAILABLE; HardwarePropertiesManager PERMISSION_REQUIRED | Record zone type names; **no zone assumed to be SoC** | NOT YET VERIFIED | — |
| Thermal | Throttling indicator | `scaling_max_freq` vs `cpuinfo_max_freq`; thermal status if available | — | CONDITIONALLY AVAILABLE | Read at idle (no load test in 10D) | NOT YET VERIFIED | — |

## 4. Camera Capability Matrix

| Item | Interface | Status | Evidence |
| :-- | :-- | :-- | :-- |
| Rear camera availability, camera IDs, logical/physical IDs | `CameraManager.getCameraIdList()`, `LENS_FACING`, physical camera IDs (API 28) | NOT YET VERIFIED | — |
| Camera2 hardware level | `INFO_SUPPORTED_HARDWARE_LEVEL` | NOT YET VERIFIED | — |
| Capabilities (MANUAL_SENSOR, MANUAL_POST_PROCESSING, RAW, BURST_CAPTURE) | `REQUEST_AVAILABLE_CAPABILITIES` | NOT YET VERIFIED | — |
| Resolutions and formats | `SCALER_STREAM_CONFIGURATION_MAP` | NOT YET VERIFIED | — |
| FPS ranges | `CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES` | NOT YET VERIFIED | — |
| Autofocus / manual focus | `CONTROL_AF_AVAILABLE_MODES`, `LENS_INFO_MINIMUM_FOCUS_DISTANCE` | NOT YET VERIFIED | — |
| Exposure / ISO ranges | `SENSOR_INFO_EXPOSURE_TIME_RANGE`, `SENSOR_INFO_SENSITIVITY_RANGE` | NOT YET VERIFIED | — |
| White balance | `CONTROL_AWB_AVAILABLE_MODES`, AWB lock | NOT YET VERIFIED | — |
| AE / AWB lock | `CONTROL_AE_LOCK_AVAILABLE`, `CONTROL_AWB_LOCK_AVAILABLE` | NOT YET VERIFIED | — |
| Manual control honoured | Request locked values, then compare with `CaptureResult` | NOT YET VERIFIED (**manual control not assumed**) | — |
| Video capability | `CamcorderProfile` / stream configurations | NOT YET VERIFIED | — |

## 5. Runtime / Backend Capability Matrix

| Backend | API requirement | Acceleration evidence | Known limitations to check | Verification method | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| TFLite (LiteRT) CPU / XNNPACK | Library-defined | — | Operator coverage | Reference graph runs; output checks | NOT YET VERIFIED |
| TFLite GPU delegate | OpenGL ES / OpenCL support on Adreno 610 (verify) | Delegated partition count | Partial delegation; CPU fallback | Reference graph; delegation report | NOT YET VERIFIED |
| TFLite NNAPI delegate | API ≥ 27 | NNAPI device list (API ≥ 29) | Vendor driver coverage; NNAPI deprecated from Android 15 | Reference graph; delegation report | NOT YET VERIFIED |
| ONNX Runtime Mobile CPU | Library-defined | — | Operator set / opset | Reference graph | NOT YET VERIFIED |
| ONNX Runtime NNAPI EP | API ≥ 27 | Assigned-node count | Partial assignment | Reference graph | NOT YET VERIFIED |
| Other approved runtimes (e.g. ExecuTorch) | Library-defined | Backend partitioning | — | Reference graph | NOT YET VERIFIED |

Model deployment feasibility (formats, operators, INT8/FP16, input constraints, probability output, load/release) is checked with reference graphs only. Multi-model residency is REQUIRES PILOT VALIDATION. **C1–C4: TO BE EMPIRICALLY DETERMINED.** No latency is recorded in this matrix.

## 6. Profiling / Tracing Capability

| Variable | Primary source | Secondary source | Validation source | Status |
| :-- | :-- | :-- | :-- | :-- |
| Timestamps (monotonic) | `SystemClock.elapsedRealtimeNanos()` | `System.nanoTime()` | Host-side sync events | NOT YET VERIFIED |
| Model load / inference timing | In-app monotonic timers | `Trace` sections in a system trace | Trace timeline | NOT YET VERIFIED |
| App CPU time | `Process.getElapsedCpuTime()` | `/proc/self/stat` | ADB `top` / `dumpsys cpuinfo` | NOT YET VERIFIED |
| Process memory | `Debug.getMemoryInfo()` | `getProcessMemoryInfo()` | ADB `dumpsys meminfo` | NOT YET VERIFIED |
| Frame timing (Stage 2 camera) | `CaptureResult` sensor timestamp | `Choreographer` frame callbacks | Trace | NOT YET VERIFIED |
| Thermal monitoring | Thermal status (if API ≥ 29) | Battery temperature, readable zones | External probe | NOT YET VERIFIED |
| System tracing | On-device trace binary started via ADB (enablement on the installed version to verify) | simpleperf | — | NOT YET VERIFIED |
| GPU counters | Trace GPU counters (driver-dependent) | kgsl sysfs | — | NOT YET VERIFIED (possibly UNAVAILABLE) |

## 7. Thermal Capability

| Aspect | Status |
| :-- | :-- |
| A. Thermal status API exists | NOT YET VERIFIED (not assumed) |
| B. Temperature sensors accessible (battery; zones by type name) | NOT YET VERIFIED |
| C. CPU-frequency capping observable | NOT YET VERIFIED |
| D. External surface temperature required | REQUIRES EXTERNAL INSTRUMENTATION |
| Temperature measurement vs throttling state | Recorded in separate fields |

## 8. Energy Measurement Feasibility

| Level | Status |
| :-- | :-- |
| E-1 battery-side external reference | NOT YET VERIFIED |
| E-2 supply-powered external session, charging excluded | NOT YET VERIFIED |
| E-3 software counters only | NOT YET VERIFIED |
| Absolute energy | **Not claimed**; requires a validated level |

## 9. Resource-State Input Availability

| Dimension | Candidate signals | Source | Sampling behaviour | Unit | Reliability | Limitations | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Thermal | Thermal status (if API ≥ 29); battery temperature; readable zones; frequency capping | App / ADB | To be observed (P2) | categorical; tenths of a degree; kHz | REQUIRES PILOT VALIDATION | API may be absent on the installed version; zone semantics are vendor-specific | NOT YET VERIFIED |
| Battery | Level; power-save mode; charging state | App | Broadcast-driven | percent; boolean | REQUIRES PILOT VALIDATION | Integer resolution | NOT YET VERIFIED |
| Memory | Available RAM; low-memory flag; trim level | App | To be observed | bytes; boolean; level | REQUIRES PILOT VALIDATION | ColorOS memory management | NOT YET VERIFIED |
| Compute | Device-wide CPU utilisation; frequency | ADB / on-device trace | To be observed | fraction; kHz | REQUIRES PILOT VALIDATION | Host-side only for battery runs (D-16 network policy) | NOT YET VERIFIED |

**R0–R3 thresholds: PILOT-DEPENDENT.**

## 10–12. Limitations, External Instrumentation, Pilot Items

- **Known limitations.** To be filled from evidence. Expected candidates: the installed API level may lack thermal APIs; `/proc/stat` is blocked for apps; GPU counters may be unavailable; vendor background restrictions apply.
- **Required external instrumentation.** Energy reference (E-1/E-2), surface probe, ambient thermometer; see protocol §7.
- **Items requiring pilot validation.**
  - all resource-state input reliability;
  - software-counter energy agreement;
  - multi-model residency;
  - sampling-interval adequacy.
