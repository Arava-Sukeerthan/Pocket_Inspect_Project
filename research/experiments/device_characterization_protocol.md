# Step 10D — Device Characterization Protocol

_Step 10D specification, 2026-10-05, Claude Code (research/repository review and specification agent)._

**Specification only.** No code has been run on the device, and no device observation exists. Every device fact below is either a **known specification** (researcher-provided, not measured) or **NOT YET VERIFIED**. Implementation is assigned to **Antigravity** ([`step10d_device_characterization_handoff.md`](../../docs/architecture/step10d_device_characterization_handoff.md)).

Related:
- [`device_capability_matrix.md`](device_capability_matrix.md) is the report skeleton.
- [`device_characterization_schema.json`](device_characterization_schema.json) is the record schema.
- [`measurement_protocol.md`](measurement_protocol.md) §2 holds the E0 variable list.
- [`pre_data_collection_decision_register.md`](pre_data_collection_decision_register.md) holds the frozen decisions.

## 1. Purpose and Scope

Step 10D is the first stage that touches the physical experimental platform. Its only purpose is **device characterization**: to establish what the OPPO A5 2020 (3 GB RAM variant) can actually provide for the protocol.

It answers:
1. installed Android version and API level;
2. telemetry interfaces;
3. thermal interfaces;
4. battery interfaces;
5. CPU information;
6. GPU information;
7. memory information;
8. runtime and model-execution backends;
9. camera controls;
10. on-device tracing and profiling;
11. physically feasible energy-measurement options;
12. what must be obtained externally;
13. what is unavailable.

**Out of scope:**
- selecting C1–C4 (they remain **TO BE EMPIRICALLY DETERMINED**);
- deriving R0–R3 thresholds (they remain **PILOT-DEPENDENT**);
- calibration;
- the E0 threshold pilot;
- any E1/E2/E3 run;
- any performance, accuracy, energy or thermal *result*.

**Positioning.** The OPPO A5 2020 is the experimental platform, not the research contribution. The characterization procedure is written device-independently (§4–§5), so it can be repeated on any other resource-constrained smartphone. Its outcome on this device is a set of **device-specific observations** (result class A, [`generalization_framework.md`](generalization_framework.md)).

## 2. Known Specification vs Actual Observation

| Kind | Source | Status label | Example |
| :-- | :-- | :-- | :-- |
| Known specification | Researcher-provided manufacturer specification (Step 10C, `configs/experiment_protocol.yaml` `platform.specification`) | KNOWN SPECIFICATION (never a measurement) | "Snapdragon 665", "3 GB RAM variant", "Android 9 at launch" |
| Actual device observation | A collector run on the physical device, with stored evidence (raw API output, adb output, capability dump) | Report statuses (§3) | Installed `Build.VERSION.SDK_INT`; observed `MemoryInfo.totalMem` |

**Rules:**
- An observation never overwrites a specification. Both are stored side by side.
- A disagreement is reported as a finding. Example: the reported total RAM is not consistent with the 3 GB variant, which would mean the wrong unit is in use. That case blocks Step 10D sign-off.
- **The experimental device is the 3 GB RAM variant only.** The 4 GB and 6 GB variants are never substituted, and their specifications are never used.
- **Variant check.** The observed `totalMem` is compared with the nominal capacities of the three variants. It must be nearest to the 3 GB nominal, allowing for memory reserved by the kernel and firmware (observed values are always below nominal).

## 3. Status Vocabularies

**Report statuses** (device capability matrix):

| Status | Meaning |
| :-- | :-- |
| VERIFIED | Observed on the physical OPPO A5 2020 with stored evidence, and its semantics (unit, sign, update behaviour) checked |
| AVAILABLE | The interface responded on the physical device, but the value semantics are not yet validated |
| CONDITIONALLY AVAILABLE | Obtainable only through a condition: host ADB, a shell-only path, a developer setting, a system property or a permission |
| UNAVAILABLE | The interface is absent, unsupported (API level or unsupported sentinel), or blocked on this device |
| REQUIRES EXTERNAL INSTRUMENTATION | Can only be measured with external equipment |
| REQUIRES PILOT VALIDATION | Interface works, but accuracy, reliability or update rate must be established in the E0 pilot |
| NOT YET VERIFIED | Not yet checked on the physical device (**the state of every device observation at the time of this specification**) |

**Runtime capability states** returned by each collector:

| State | Meaning | Maps to report status |
| :-- | :-- | :-- |
| AVAILABLE | Call succeeded and returned a supported value | VERIFIED after the semantics check, otherwise AVAILABLE or REQUIRES PILOT VALIDATION |
| UNAVAILABLE | Supported API, but the device reports the value as unsupported (e.g. an unsupported-property sentinel) or the path does not exist | UNAVAILABLE |
| PERMISSION_REQUIRED | Blocked by permissions, SELinux or the device-owner restriction | CONDITIONALLY AVAILABLE if a documented condition unlocks it; otherwise UNAVAILABLE |
| API_UNSUPPORTED | The installed API level is below the interface's minimum | UNAVAILABLE |
| EXTERNAL_REQUIRED | Needs external equipment | REQUIRES EXTERNAL INSTRUMENTATION |
| NOT_TESTED | The collector did not run this check | NOT YET VERIFIED |
| ERROR | The check threw or returned inconsistent output; the message is recorded | NOT YET VERIFIED (re-run required) |

**The no-fake-zero rule.**
- An unavailable metric is recorded as `status: unavailable` (or another non-available state) **with `value: null`**.
- It is never 0, −1 or a default. GPU utilisation unavailable is **not** "GPU utilisation = 0".
- Platform sentinels for "unsupported" (for example the minimum-integer return of `BatteryManager.getIntProperty` on apps targeting API 28 or later) are mapped to UNAVAILABLE, never stored as values.

## 4. Characterization Procedure (device-independent)

| Phase | Content | Device state |
| :-- | :-- | :-- |
| P0 Preparation | Record the device unit ID; factory-state notes; installed apps; ColorOS settings (battery optimisation, background restrictions); developer options and USB debugging enabled (recorded); app installed with minimum SDK not above the installed API level | Charging allowed |
| P1 Identity and platform | Device identity; Android version; API level; security patch; build fingerprint; vendor ROM version (system property, conditional) | Any |
| P2 Telemetry capability | Battery, memory, CPU, GPU and thermal collectors: availability, unit, sign convention, observed update interval (sampled at a fixed poll interval for a fixed short window; **interval values are not results**, only capability evidence) | Battery-powered, offline, USB disconnected for battery checks |
| P3 Camera capability | Camera ID list, characteristics dump, then an **advertised-vs-honoured** check: request locked settings and read `CaptureResult` to confirm they were applied | Rig not required |
| P4 Backend capability | For each runtime/backend: create the interpreter or session with a **tiny in-repo reference graph** (no trained weights; e.g. one convolution + softmax); record delegation coverage (delegated vs CPU partitions), output shape, finite outputs and probability sum. **No latency is recorded or reported.** | Any |
| P5 Profiling capability | Clock sources and resolution; timer overhead check; trace availability (on-device trace binary, system tracing toggles); process CPU time | Any |
| P6 Thermal capability | Thermal status API (if API ≥ 29), headroom (if API ≥ 30), listener; temperature sources (battery; thermal zones via app or ADB, with zone type names recorded, **no zone assumed to be SoC temperature**); CPU-frequency capping observability | Any |
| P7 Energy feasibility | Physical and procedural checks of E-1/E-2/E-3 (§6); **no energy experiment** | Any |
| P8 Report | Aggregate all capability records into the characterization report (`device_capability_matrix.md` filled with evidence references) | Host |

Each phase is repeated on a second day (a reboot in between) to confirm that capability states are stable. A state that differs between repeats is reported as unstable.

## 5. Capability Items

### 5.1 Android / API
- **Installed version.** The OPPO A5 2020 launched with Android 9 (API 28) according to the specification. **The installed version is NOT assumed.** It is read from `Build.VERSION.RELEASE` and `Build.VERSION.SDK_INT`.
- **Thermal-status API.** Not assumed.
  - If SDK_INT ≥ 29: test `PowerManager.getCurrentThermalStatus()` and the listener.
  - If SDK_INT ≥ 30: test `getThermalHeadroom()`.
  - If SDK_INT is 28: record **API_UNSUPPORTED** and apply the approved fallback (D-10): temperature signals plus CPU-frequency-capping evidence.

### 5.2 Telemetry
The battery, memory, CPU, GPU and thermal items are listed in [`device_capability_matrix.md`](device_capability_matrix.md) §3, each with its interface, expected class and verification method.

### 5.3 Camera
Rear camera IDs and logical/physical cameras (the ultra-wide may not be exposed to third-party apps; verify). Also recorded:
- hardware level and capabilities (MANUAL_SENSOR, MANUAL_POST_PROCESSING, RAW, BURST_CAPTURE);
- output sizes per format;
- AE target FPS ranges;
- AF modes and minimum focus distance (zero means fixed focus);
- exposure-time and sensitivity ranges;
- AWB modes;
- AE and AWB lock availability;
- video profiles.

**Manual control is not claimed unless the advertised-vs-honoured check passes.**

### 5.4 Runtime backends
TensorFlow Lite (LiteRT) CPU and XNNPACK, the GPU delegate, the NNAPI delegate (accelerator device list where the API allows), ONNX Runtime Mobile CPU and its NNAPI execution provider, and other repository-approved runtimes.

Recorded per backend:
- availability;
- API requirement;
- hardware acceleration (delegated partitions);
- known limitations;
- verification method.

**No performance is claimed.**

### 5.5 Model deployment feasibility
- Recorded: supported formats; operator coverage per runtime version (reference graphs exercising convolution, depthwise convolution, pooling, fully connected and softmax); INT8 full-integer and FP16 support; fixed input-size constraints; probability-output availability.
- Load-and-release feasibility uses reference graphs only.
- **Whether several real candidate models fit in memory together is REQUIRES PILOT VALIDATION** (D-13), because no candidate model exists yet.
- C1–C4 identities remain **TO BE EMPIRICALLY DETERMINED**.

### 5.6 Profiling
For each variable, the protocol designates a **primary**, a **secondary** and a **validation** source, or records it as **unavailable** ([`device_capability_matrix.md`](device_capability_matrix.md) §6).

### 5.7 Thermal
**Temperature measurement** and **thermal throttling state** are characterised separately:
- **A.** Thermal status API existence.
- **B.** Accessible temperature sensors (battery temperature; thermal-zone types and readability).
- **C.** CPU-frequency capping observability: per-policy current and maximum scaling frequency against hardware maximum.
- **D.** External surface temperature, which is **REQUIRES EXTERNAL INSTRUMENTATION**.

Surface temperature is never converted into SoC temperature without validation.

### 5.8 Resource-state inputs
For each dimension (thermal, battery, memory, compute), the matrix records:
- available signal;
- source;
- observed sampling behaviour;
- unit;
- reliability, which is REQUIRES PILOT VALIDATION;
- limitations.

**R0–R3 thresholds remain PILOT-DEPENDENT.** Latency, accuracy and confidence are never state inputs.

## 6. Energy-Measurement Feasibility (D-16 hierarchy unchanged)

No energy experiment is performed. The checker establishes which level of the approved hierarchy is physically feasible.

| Level | Feasibility questions | Evidence | Default status |
| :-- | :-- | :-- | :-- |
| E-1 battery-side external reference | Is the battery user-removable or accessible without unsafe disassembly? Can a supply be connected at the battery terminals, and with what the device's battery-presence and temperature checks require? Is a suitable power analyser available? | Physical inspection notes, photos, instrument model; researcher sign-off on safety | NOT YET VERIFIED |
| E-2 supply-powered external session, charging excluded | USB connector type; whether the device keeps charging when full; whether charging can be stopped without root; whether the measured USB power reflects device consumption only (battery current near zero and status not charging during the session) | Battery status and current logs during a supply-powered idle check; meter model | NOT YET VERIFIED |
| E-3 software counters only | Which of current, charge counter and energy counter are supported (§5.2) | Collector records | NOT YET VERIFIED |

**Rules:**
- Absolute energy is **not claimed** until a level is validated.
- No energy accuracy value is invented.
- The agreement threshold remains PRE-DATA-COLLECTION DECISION REQUIRED (D-16).

## 7. Required External Instrumentation (expected)

| Instrument | Purpose | Status |
| :-- | :-- | :-- |
| Power analyser (battery-side) or USB power meter | E-1 / E-2 energy reference | REQUIRES EXTERNAL INSTRUMENTATION; availability NOT YET VERIFIED |
| Surface temperature probe | Device surface temperature | REQUIRES EXTERNAL INSTRUMENTATION |
| Ambient thermometer | Ambient covariate | REQUIRES EXTERNAL INSTRUMENTATION |
| Host computer with ADB | Shell-only telemetry paths, trace collection, log retrieval | Required |

## 8. Safety

- **Battery-terminal work.** Any battery-terminal access (E-1) requires a researcher decision on safety before it is attempted.
- **No heat sources and no deliberate overheating.** Step 10D runs no pressure protocol.
- **Charging during capability checks** is recorded, because it changes the battery readings.

## 9. Sign-off Criteria for Step 10D

Step 10D is complete when all of the following hold:
1. every item in [`device_capability_matrix.md`](device_capability_matrix.md) has a non-default status with evidence;
2. the variant check confirms the 3 GB unit;
3. the D-10 thermal source and the D-16 energy level are decided from evidence;
4. Claude Code has recorded a review entry with no open blocking findings.

Items left as REQUIRES PILOT VALIDATION move on to the E0 pilot.

## 10. Status

Specification only. **No device observation, measurement or experiment exists.**
