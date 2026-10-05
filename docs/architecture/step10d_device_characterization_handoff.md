# Step 10D — Device Characterization: Implementation Handoff to Antigravity

_Step 10D specification, 2026-10-05, written by Claude Code (research/repository review and specification agent)._

| Role | Agent | Responsibility in Step 10D |
| :-- | :-- | :-- |
| **Implementation agent** | **Antigravity** | Implements the characterization architecture and code; runs the device-side checks on the physical OPPO A5 2020 (3 GB); runs the tests; appends its own CHANGELOG entry |
| **Review/specification agent** | **Claude Code** | Wrote this specification; reviews Antigravity's implementation for research consistency, protocol compliance, bugs and methodological problems; suggests corrections; records review entries. **Claude Code does not silently replace Antigravity's implementation.** |

Protocol: [`device_characterization_protocol.md`](../../research/experiments/device_characterization_protocol.md). Report skeleton: [`device_capability_matrix.md`](../../research/experiments/device_capability_matrix.md). Schema: [`device_characterization_schema.json`](../../research/experiments/device_characterization_schema.json).

**Nothing in this handoff is a device observation.** All device capabilities are NOT YET VERIFIED until Antigravity's run produces evidence.

## 1. Scope Boundaries

**In scope:**
- device characterization only (protocol §1, questions 1–13);
- the 12 components below;
- the characterization report.

**Out of scope:**
- C1–C4 selection (**TO BE EMPIRICALLY DETERMINED**);
- R0–R3 thresholds (**PILOT-DEPENDENT**);
- pressure protocols;
- calibration;
- any E0/E1/E2/E3 run;
- any accuracy, latency, energy or thermal *result*.

**Methodology stays device-independent.**
- Collectors use platform interfaces gated by API level and capability. They are not OPPO-specific code paths.
- Vendor-specific probes (ColorOS properties, Adreno kgsl paths) are isolated in clearly named optional probes. Each returns an explicit state when absent.

## 2. Proposed Code Placement (follows `AGENTS.md` §2)

| Path | Content |
| :-- | :-- |
| `mobile/characterization/` | Android app module (Kotlin): on-device collectors 1–10 and 11 (the software parts); writes schema-conformant JSON |
| `scripts/device_characterization/` | Host-side CLI (`argparse`): ADB collection of shell-only paths (`/proc/stat`, cpufreq, kgsl, thermal zones, `dumpsys`, `getprop`, trace start/pull); log retrieval |
| `src/monitoring/characterization/` | Python package (with `__init__.py` and docstrings): record models, schema validation, state → report-status mapping, `CharacterizationReportGenerator` |
| `configs/device_characterization.yaml` | Procedural parameters (poll interval, observation window, repeat count, enabled probes). These are procedure settings, not thresholds or results. Each value needs a written justification and is reviewed by Claude Code. |
| `tests/` | Unit tests for collectors' state handling (mocked inputs), schema conformance, report generation |
| `research/results/device_characterization/<run_id>/` | Run outputs: schema-valid JSON records and raw evidence text. No images, no binaries. |

**Android build constraints:**
- **minSdk must not exceed 28.** The device launched on API 28, and the installed level is unknown.
- **targetSdk at least 28**, so that `BatteryManager` property calls return the documented unsupported sentinel and not 0. Even so, a returned 0 for current or counters must be checked against the sentinel semantics before it is accepted.
- **Every API ≥ 29 call** is guarded by `Build.VERSION.SDK_INT`. Below the gate, the result is `API_UNSUPPORTED`.

**Existing guard tests.** Steps 10A–10C contain "no implementation yet" guards:
- `tests/test_research_protocol.py`, `tests/test_dataset_device_model.py` and `tests/test_gap_selection_reconciliation.py` assert that `mobile/`, `experiments/`, `src/<module>/` and `research/results/` contain only their README or init files.

Antigravity's code will intentionally break these guards. Antigravity must **narrow each guard to an explicit Step 10D allow-list** (the exact paths above, the allowed file types, and no model binaries or images) instead of deleting it. Each guard change is recorded in the CHANGELOG, and Claude Code reviews it as a lifecycle transition.

## 3. Global Implementation Rules

1. **No fake zeros.** An unavailable metric is `{"state": "UNAVAILABLE" | "PERMISSION_REQUIRED" | "API_UNSUPPORTED" | ..., "value": null}`. GPU utilisation unavailable must **not** become 0. The schema enforces this (`allOf` rule in `capability_result`).
2. **Status/value separation.** Every result carries `state`, `report_status`, `value`, `unit`, `source`, `verified` and `verification_method`.
3. **`verified: true` only with evidence.** This means an observation on the physical device, a stored raw-evidence reference, and a semantics check (unit, sign, update behaviour).
4. **Known specification ≠ observation.** `known_specification` is copied from `configs/experiment_protocol.yaml` and never overwritten. The 3 GB variant is fixed, and the 4 GB / 6 GB variants are never used.
5. **Nothing assumed.** In particular:
   - the Android version or API level;
   - the thermal-status API (API ≥ 29);
   - thermal headroom (API ≥ 30);
   - manual camera control;
   - GPU counters;
   - NNAPI acceleration;
   - which thermal zone is the SoC;
   - energy accuracy.
6. **No performance results.** Backend checks record availability, delegation and output validity only. No latency, throughput, accuracy, energy or temperature value is reported as a result. Timer checks verify clock behaviour, not model speed.
7. **No sensitive identifiers.**
   - Do not read IMEI, phone number or account data, and request no telephony permissions.
   - The device unit ID is a researcher-assigned label.
   - The build fingerprint is recorded; hardware serials are not.
8. **No model binaries in git** (`AGENTS.md`). Reference graphs are generated by a script at build or test time; only their generator and hash are committed.
9. **Fail explicit.** A collector exception becomes `state: ERROR` with `error_message`. It never becomes a default value.
10. **Configuration-first.** Procedural parameters live in `configs/`; nothing is hard-coded.

## 4. Components

Each component returns `capability_result` records (schema `$defs/capability_result`), plus a component-level summary state. **No component is assumed to have a working data source.**

| # | Component | Responsibility | Primary sources (gate) | Required explicit states |
| :-- | :-- | :-- | :-- | :-- |
| 1 | **DeviceIdentityCollector** | Device identity; known specification vs observation; 3 GB variant check | `Build.*`; `MemoryInfo.totalMem`; `StatFs`; `Build.SOC_MODEL` (API ≥ 31); GLES renderer; ADB `getprop` (vendor ROM) | AVAILABLE, API_UNSUPPORTED (SOC_MODEL), NOT_TESTED, ERROR |
| 2 | **AndroidCapabilityCollector** | Installed Android version, API level, security patch, platform services present (`PowerManager`, `HardwarePropertiesManager`, `CameraManager`) | `Build.VERSION.*`; `getSystemService` | AVAILABLE, UNAVAILABLE, ERROR |
| 3 | **BatteryTelemetryCollector** | Percentage, charging/plug state, voltage, current, charge/energy counters, temperature, health/status; sentinel handling; sign convention and observed update interval | `BatteryManager` properties; `ACTION_BATTERY_CHANGED` | AVAILABLE, UNAVAILABLE (sentinel), ERROR |
| 4 | **MemoryTelemetryCollector** | Total/available RAM, threshold, low-memory flag, app and process memory, trim levels, `/proc/meminfo` and PSI readability | `MemoryInfo`; `Debug`; `onTrimMemory`; file reads; ADB `dumpsys meminfo` | AVAILABLE, PERMISSION_REQUIRED, UNAVAILABLE |
| 5 | **CPUTelemetryCollector** | Model, core count, policy layout, current/min/max scaling frequency, hardware max, process CPU time, device-wide utilisation (expected via ADB only) | `/proc/cpuinfo`; cpufreq sysfs (app, then ADB); `/proc/self/stat`; `Process.getElapsedCpuTime()`; ADB `/proc/stat` | AVAILABLE, PERMISSION_REQUIRED (app read of `/proc/stat`), UNAVAILABLE |
| 6 | **GPUTelemetryCollector** | Identification; utilisation, frequency and memory where readable | GLES/EGL strings; Vulkan properties (if supported); kgsl/devfreq sysfs via app or ADB; trace GPU counters | AVAILABLE, PERMISSION_REQUIRED, UNAVAILABLE (report "UNAVAILABLE THROUGH AVAILABLE PLATFORM INTERFACE") |
| 7 | **ThermalTelemetryCollector** | Thermal status API, listener, headroom; temperature sources (battery; thermal zones with type names; no zone assumed to be the SoC); frequency-capping observability; selection of the D-10 thermal source from evidence | `PowerManager` (API ≥ 29 / ≥ 30); `/sys/class/thermal` (app, then ADB); `HardwarePropertiesManager` (expected PERMISSION_REQUIRED); cpufreq | AVAILABLE, API_UNSUPPORTED, PERMISSION_REQUIRED, UNAVAILABLE |
| 8 | **CameraCapabilityCollector** | Camera IDs (logical/physical), hardware level, capabilities, sizes/formats, FPS ranges, AF/focus, exposure/ISO, AWB, locks, video; **advertised-vs-honoured** manual-control check through `CaptureResult` | `CameraManager`, `CameraCharacteristics`, a capture session | AVAILABLE, UNAVAILABLE, PERMISSION_REQUIRED (camera permission), ERROR |
| 9 | **InferenceBackendCapabilityCollector** | For each backend (TFLite CPU/XNNPACK, GPU delegate, NNAPI delegate, ONNX Runtime CPU and NNAPI EP, other approved): load the reference graph, record delegation coverage, probability-output validity (finite, correct shape, softmax normalised), INT8/FP16 support, load/release; **no timing results** | Runtime APIs; NNAPI device query (API ≥ 29) | AVAILABLE, UNAVAILABLE, API_UNSUPPORTED, ERROR |
| 10 | **ProfilingCapabilityCollector** | Clock sources and resolution, timer-overhead sanity, `Trace` sections, on-device trace binary availability and enablement on the installed version, simpleperf; primary, secondary and validation source per variable | `SystemClock`, `System.nanoTime`, `android.os.Trace`; ADB trace commands | AVAILABLE, CONDITIONALLY via ADB (record the condition), UNAVAILABLE |
| 11 | **EnergyMeasurementCapabilityChecker** | Feasibility of E-1, E-2 and E-3 (D-16). Software part: counter support (from 3). Procedural part: a structured researcher checklist (battery accessibility, connector, charging behaviour, meter model, safety sign-off). Outputs `selected_level` only with evidence; `absolute_energy_claimed` is always false. | Component 3 records; researcher-entered checklist | EXTERNAL_REQUIRED, AVAILABLE (counters), UNAVAILABLE, NOT_TESTED |
| 12 | **CharacterizationReportGenerator** | Validates all records against the schema; maps runtime states to report statuses (protocol §3); fills `device_capability_matrix.md` with evidence references; flags instability between repeats and specification/observation disagreements; refuses to emit any record that breaks the null-value rule | `src/monitoring/characterization/` | n/a (generator); fails the build on schema violations |

**Thermal source decision (D-10).** Component 7 outputs `selected_thermal_source`:
- `platform_thermal_status` only if the API exists and works on the installed version;
- otherwise `fallback_temperature_and_frequency_capping`.

Any mapping of platform levels to R-levels stays REQUIRES FUTURE APPROVAL.

**Energy level decision (D-16).** Component 11 outputs `selected_level` (E-1, E-2 or E-3) from evidence. The agreement threshold stays PRE-DATA-COLLECTION DECISION REQUIRED.

## 5. Data Schemas

Defined in [`device_characterization_schema.json`](../../research/experiments/device_characterization_schema.json):

| Schema | Purpose |
| :-- | :-- |
| `device_identity` | Known specification vs observed records, plus the variant check |
| `capability_result` | Shared record with explicit status/value separation and the null-value rule |
| `telemetry_capability` | Per dimension (battery, memory, CPU, GPU, thermal), with the resource-state-input flag |
| `camera_capability` | Per camera ID, including manual-control honoured |
| `backend_capability` | Availability, delegation, quantization, probability output; **no latency or accuracy fields by design** |
| `thermal_capability` | Temperature sources separate from the throttling/status APIs |
| `energy_capability` | E-1/E-2/E-3 feasibility; `absolute_energy_claimed` fixed false |
| `characterization_run` | Run metadata, conditions, all of the above; `performance_results` fixed null |

Example (conceptual):

```json
{
  "metric": "gpu_utilization",
  "state": "UNAVAILABLE",
  "report_status": "UNAVAILABLE",
  "value": null,
  "unit": "percent",
  "source": "kgsl sysfs via app and ADB",
  "verified": false,
  "verification_method": "readability check"
}
```

## 6. Acceptance Criteria (Definition of Done for Antigravity)

1. All 12 components implemented. Each returns explicit states for every item in `device_capability_matrix.md`.
2. The repository tests pass, including new unit tests:
   - mocked sentinel → UNAVAILABLE with null;
   - SDK below a gate → API_UNSUPPORTED;
   - exception → ERROR;
   - no record with a non-null value under a non-available state;
   - `verified: true` only with evidence.
3. Two characterization runs on the physical device, on separate days with a reboot between them, stored under `research/results/device_characterization/` with raw evidence.
4. `device_capability_matrix.md` filled from the runs. Statuses use only the protocol §3 vocabulary.
5. The variant check confirms the 3 GB unit, or the disagreement is reported as blocking.
6. The D-10 thermal source and the D-16 energy level are selected from evidence.
7. No performance, accuracy, energy or thermal result is reported anywhere.
8. Guard tests narrowed (not deleted) as in §2.
9. Antigravity's CHANGELOG entry appended (§8).

## 7. Claude Code Review Checklist (applied after Antigravity's entry)

- **Research consistency.** GC-03, RQ1, B1–B5, the recovery metric and the D-01 to D-16 freeze are unchanged. The OPPO A5 2020 (3 GB) is the platform, not the contribution.
- **Protocol compliance.** Status vocabulary, the null-value rule, known specification vs observation, no assumed capabilities, no performance results.
- **Correctness.**
  - API gates;
  - sentinel handling;
  - unit and sign conventions (current in microamperes, battery temperature in tenths of a degree, voltage in millivolts);
  - thermal-zone semantics not over-claimed;
  - camera honoured-vs-advertised logic;
  - delegation reporting.
- **Evidence.** Every VERIFIED item has raw evidence, and repeat-run stability is reported.
- **Repository hygiene.** No binaries, images or sensitive identifiers. Guard-test changes are narrow and recorded. Configuration values are justified.
- **Findings** are recorded in a Claude Code CHANGELOG entry and handed back to Antigravity as a correction list. Claude Code does not rewrite the implementation.

## 8. CHANGELOG Synchronization Policy

Cycle: **IMPLEMENT → CHANGELOG → CLAUDE REVIEW → CHANGELOG → ANTIGRAVITY CORRECTION → CHANGELOG → TEST → NEXT STAGE.**

**Antigravity's Step 10D entry must contain:**
- implementation changes;
- files changed;
- tests run and results;
- measurements and capabilities verified on the physical device (with evidence paths);
- limitations;
- unresolved issues;
- commit hash.

**Claude Code** then inspects the current code, the latest CHANGELOG and this protocol, and appends a review entry. Required corrections are handed back to Antigravity, which appends a correction entry, and so on. Earlier entries are never edited (CHANGELOG rule 2).

## 9. Open Questions for the Researcher

1. **Reference-graph tooling.** Building `.tflite` reference graphs normally needs TensorFlow, a heavy package that `AGENTS.md` forbids without explicit instruction. `.onnx` graphs can be built with the lightweight `onnx` package. **DECISION REQUIRED:** authorise a converter, or use reference models shipped with the runtimes, with licence and hash recorded.
2. **External instruments.** Which power meter, surface probe and thermometer are actually available (E-1/E-2 feasibility)?
3. **Battery access.** Is battery-terminal access acceptable on safety grounds (E-1)? This is a researcher decision before any attempt.
4. **Developer settings.** Is enabling developer options, USB debugging and any trace-enabling system property acceptable on the experimental unit?
