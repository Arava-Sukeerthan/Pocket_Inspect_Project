# Device Characterisation and Measurement Protocol

_Step 10C, 2026-10-05, Claude Code. Protocol design only. **No measurement has been taken.** Availability classes are expectations from platform documentation (see [`device_requirements.md`](../datasets/device_requirements.md) for evidence levels). None is verified on the device._

## 1. Confirmed Experimental Platform

**A. Known device specifications.** As confirmed by the researcher on 2026-10-05; manufacturer specification, not measured.

| Field | Value |
| :-- | :-- |
| Manufacturer / model | OPPO A5 2020 |
| Experimental RAM variant | **3 GB** LPDDR4X (only this variant; the 4 GB and 6 GB variants are **not** the experimental platform) |
| Storage | 64 GB |
| SoC | Qualcomm Snapdragon 665, 11 nm |
| CPU | Octa-core, up to 2.0 GHz |
| GPU | Adreno 610 |
| Battery | 5000 mAh |
| Rear cameras | 12 MP primary; 8 MP ultra-wide |
| Android launch version | Android 9 / ColorOS |

**B. Capabilities requiring verification (REQUIRES DEVICE VERIFICATION):**
- installed Android version and API level;
- thermal-status and thermal-headroom API availability (API ≥ 29 and ≥ 30 respectively);
- battery current and energy counters;
- thermal-zone readability;
- GPU counters;
- runtime GPU, DSP and NPU backends;
- Camera2 manual-control level;
- ColorOS background-process behaviour;
- battery-bypass feasibility for an external energy reference.

**C. Measurements to be obtained experimentally.** Everything in §2 and §3. None exists.

## 2. E0 — Device Characterisation (pilot only)

**Purpose:**
- establish which signals are readable, at what update interval and with what noise;
- derive R-state thresholds ([`resource_states.md`](resource_states.md) §4);
- measure model load and switch costs;
- validate software energy counters against the external reference.

E0 data are **pilot only** and are excluded from confirmatory analysis.

**Roles:**
- **T** = device telemetry;
- **M** = experimental manipulation;
- **O** = outcome variable;
- **Cov** = covariate;
- **MC** = manipulation check.

| Variable | Source / API | Expected availability | Unit | Sampling interval | Validation | Role |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Android version / API level | `Build.VERSION` | REQUIRED / DIRECTLY AVAILABLE | API level | Once per run | Recorded | Cov (reproducibility) |
| Total RAM | `ActivityManager.MemoryInfo.totalMem` | REQUIRED / DIRECTLY AVAILABLE | bytes | Once per run | Must be consistent with the 3 GB variant | Cov |
| Available RAM, low-memory flag | `ActivityManager.MemoryInfo` | REQUIRED / DIRECTLY AVAILABLE | bytes; boolean | TO BE DETERMINED (E0) | Compare with `dumpsys meminfo` | T, MC (memory pressure), state input |
| App memory usage | `Debug.getMemoryInfo()` / PSS | REQUIRED / DIRECTLY AVAILABLE | kB | Per item | Compare with `dumpsys meminfo` | O (memory) |
| CPU information | `/proc/cpuinfo`, cpufreq policy files via ADB | CONDITIONALLY AVAILABLE | — | Once | Recorded | Cov |
| App CPU time | `Process.getElapsedCpuTime()`, `/proc/self/stat` | REQUIRED / DIRECTLY AVAILABLE | ms of CPU time | Per item | Consistency check | O (resource utilisation) |
| Device-wide CPU utilisation | `/proc/stat` via ADB, `top`, Perfetto | CONDITIONALLY AVAILABLE (host-side) | fraction | TO BE DETERMINED (E0) | Cross-check two sources | T, MC (load), state input |
| CPU frequency | cpufreq via ADB / Perfetto | CONDITIONALLY AVAILABLE | kHz | TO BE DETERMINED (E0) | SELinux readability check | T, MC (throttling), state input |
| GPU utilisation / frequency | Adreno kernel-driver sysfs via ADB, or profiler | CONDITIONALLY AVAILABLE (may be UNAVAILABLE) | fraction; Hz | TO BE DETERMINED (E0) | Readability check | T, O (resource utilisation) |
| Battery level | `BatteryManager.BATTERY_PROPERTY_CAPACITY` | REQUIRED / DIRECTLY AVAILABLE | percent (integer) | Broadcast-driven | — | T, Cov, state input |
| Battery voltage | `ACTION_BATTERY_CHANGED` `EXTRA_VOLTAGE` | REQUIRED / DIRECTLY AVAILABLE | mV | Broadcast-driven | Compare with external meter | T |
| Battery current | `BATTERY_PROPERTY_CURRENT_NOW` | CONDITIONALLY AVAILABLE | µA (sign convention to verify) | TO BE DETERMINED (E0) | Against external reference | T (energy proxy) |
| Charge / energy counter | `CHARGE_COUNTER`, `ENERGY_COUNTER` | CONDITIONALLY AVAILABLE (energy counter often unsupported) | µAh; nWh | TO BE DETERMINED (E0) | Against external reference | T (energy proxy) |
| Battery temperature | `ACTION_BATTERY_CHANGED` `EXTRA_TEMPERATURE` | REQUIRED / DIRECTLY AVAILABLE | tenths of a degree Celsius | Broadcast-driven | Against external probe | T, O (thermal), state input |
| SoC / skin temperature | Thermal zones via ADB; `HardwarePropertiesManager` is restricted to device owner / VR service | CONDITIONALLY AVAILABLE | degrees Celsius (per zone) | TO BE DETERMINED (E0) | Zone mapping per device | T, O (thermal) |
| Device surface temperature | External surface probe | EXTERNAL INSTRUMENTATION REQUIRED | degrees Celsius | TO BE DETERMINED | Probe calibration | O (thermal) |
| Ambient temperature | External thermometer | EXTERNAL INSTRUMENTATION REQUIRED | degrees Celsius | Per run, continuous | Calibration | Cov |
| Thermal status | `PowerManager.getCurrentThermalStatus()` | CONDITIONALLY AVAILABLE (API ≥ 29; launch version is API 28) | categorical | On change (listener) | Installed API level | T, state input; **a state, not a temperature** |
| Thermal headroom | `PowerManager.getThermalHeadroom()` | CONDITIONALLY AVAILABLE (API ≥ 30) | dimensionless | TO BE DETERMINED | Installed API level | T |
| Power-save mode | `PowerManager.isPowerSaveMode()` | REQUIRED / DIRECTLY AVAILABLE | boolean | On change | — | M (P-battery) / MC |
| Controlled pressure condition | Pressure protocol scripts | Design element | categorical (R-level target / schedule ID) | Per run | Manipulation check via telemetry | M |
| Model load time | In-app monotonic timer | REQUIRED / DIRECTLY AVAILABLE | ms | Per load | Repeated loads | O |
| Inference latency | In-app monotonic timer per stage | REQUIRED / DIRECTLY AVAILABLE | ms | Per item | Timer overhead check | O (primary) |
| FPS / throughput | Derived from timestamps | REQUIRED / DIRECTLY AVAILABLE | items per second | Per window | — | O |
| Whole-device power / energy | External reference instrument | EXTERNAL INSTRUMENTATION REQUIRED | W; J | Instrument-defined (TO BE DETERMINED) | Instrument calibration; sync | O (energy) |
| Camera characteristics | `CameraCharacteristics` (hardware level, capabilities, AE/AF/AWB lock support) | CONDITIONALLY AVAILABLE | — | Once | Capability dump | Cov (Stage 2) |
| Per-frame camera metadata | `CaptureResult` | CONDITIONALLY AVAILABLE | per field | Per frame | — | Cov (Stage 2) |

No variable is **UNAVAILABLE** by assumption. Any signal that E0 finds unreadable is reclassified as UNAVAILABLE and the protocol falls back as documented ([`resource_states.md`](resource_states.md) Part II).

## 3. Outcome Measurements

| Tier | Measure | Definition |
| :-- | :-- | :-- |
| Primary | Inspection performance | Item-level defect recall (primary metric M, Step 10A) with precision, F1 and false-reject rate. Automated and system (with A4) metrics are reported separately, with coverage. |
| Primary | Recovery | ρ = [M(B5) − M(B3)] / [M(B1) − M(B3)] ([`experimental_protocol.md`](experimental_protocol.md) §6) |
| Primary | Latency | Per item, including verification; per stage breakdown; tail percentiles |
| Secondary | Calibration | ECE, Brier, NLL, reliability, per configuration and state |
| Secondary | Energy | Per item, per verified item, per inference; average power; peak power only with an adequate-resolution reference |
| Secondary | Thermal behaviour | Temperature trajectories (measurement) and thermal-status trajectory (state), reported separately |
| Secondary | Memory | Peak and resident app memory; low-memory events |
| Secondary | Resource utilisation | App CPU time; device CPU/GPU utilisation where available |
| Secondary | Verification frequency and overhead | Trigger rate per action; added latency and energy per verified item |
| Secondary | Model-switch frequency | Switches per unit time; switch latency; cap events |
| Secondary | False accepts / false rejects | Defective items accepted (missed) / normal items rejected or referred |

## 4. Energy

**EXTERNAL-METER VALIDATION REQUIRED.** Software battery counters are **not** ground truth.

1. **Reference instrument.** A battery-bypass power analyzer, or a validated pass-through.
   - On the OPPO A5 2020, bypass feasibility REQUIRES DEVICE VERIFICATION.
   - If no reference is feasible, absolute energy is not reported. Only relative comparisons from software counters, validated against whatever reference exists, are reported as a limitation.
2. **Validation.**
   - Identical scripted workloads are measured simultaneously by the reference and the software counters.
   - Agreement is assessed by bias and limits of agreement; acceptance criteria are DECISION REQUIRED BEFORE DATA COLLECTION.
3. **Unit of analysis.** Energy is integrated over intervals at least as long as the validated resolution (e.g. a batch of items) and then divided by the item count.
4. **Pressure-workload energy.** It is part of whole-device energy. Comparisons are therefore made between baselines under the identical pressure schedule.
5. **Battery-factor conflict.** Battery-state conditions need battery power, so reference sessions are run separately to calibrate the counters (Step 10B).

## 5. Thermal

- **Temperature measurement** (battery, SoC zones, surface, ambient) and **thermal state / throttling** (platform thermal status if available; observed CPU-frequency capping) are logged in separate fields and analysed separately. Neither is inferred from the other.
- Where platform access is restricted (likely for SoC and skin temperatures on an unrooted device), the external surface probe is the reference.
- If the thermal-status API is unavailable on the installed Android version, throttling is characterised by frequency capping only and is labelled as such.

## 6. Software Telemetry vs External Instrumentation

| Software telemetry (on device / host via ADB) | External instrumentation |
| :-- | :-- |
| Battery level, voltage, current, counters, temperature; RAM; CPU time; CPU/GPU utilisation and frequency; thermal status; latency; load time; camera metadata | Whole-device power and energy reference; device surface probe; ambient thermometer |
