# Resource States R0–R3, Resource Pressure and Runtime Adaptation

_Step 10C, 2026-10-05, Claude Code. Protocol design only. No threshold, signal value or transition has been measured. Every numerical threshold is **TO BE DERIVED FROM DEVICE CHARACTERISATION (E0) AND FROZEN BEFORE CONFIRMATORY RUNS**._

Master protocol: [`experimental_protocol.md`](experimental_protocol.md). Variable layers: [`variables_and_factors.md`](../research_questions/variables_and_factors.md) §1.1.

## Part I — General Resource-State Framework (device-independent)

### 1. States

| State | Meaning |
| :-- | :-- |
| R0 | Nominal: no constraint active |
| R1 | Moderate resource pressure |
| R2 | High resource pressure |
| R3 | Critical resource pressure |

### 2. Monitored variables (state-estimator inputs)

Only **device-state signals** feed the estimator. Outcome variables (inference latency, accuracy, confidence) are excluded, so the state does not depend on the quantities it is used to explain.

| Dimension | Candidate signals (availability per device: [`measurement_protocol.md`](measurement_protocol.md) §2) |
| :-- | :-- |
| Thermal | Platform thermal status (categorical, where the API exists); battery temperature; SoC/skin temperature where readable; observed CPU-frequency capping |
| Battery | Battery level; power-save mode; charging state |
| Memory | Available RAM; platform low-memory flag |
| Compute load | Device-wide CPU utilisation and frequency (host-side) |

### 3. Classification logic (PROVISIONAL)

**Rule-based, maximum-severity classification.**
1. Each dimension is mapped to an ordinal level 0–3 by its own thresholds.
2. The resource state is the maximum level across dimensions.

**Why not a weighted composite score.**
- A composite needs weights for incommensurable signals, and there is no principled basis for them before data exist.
- Maximum severity is interpretable, reproducible from the logged signals, and conservative: any critical dimension makes the state critical.

A composite score remains an alternative. Choosing it would be a **DECISION REQUIRED BEFORE DATA COLLECTION**, with weights justified from E0.

### 4. Threshold-selection methodology

1. **Platform-defined levels first.** Where the platform exposes a categorical signal (thermal status levels, power-save mode, low-memory flag), its own levels are mapped to R-levels by a written correspondence. No new number is invented.
2. **Continuous signals from E0.**
   - For each continuous signal, E0 records its trajectory under idle and under each controlled pressure protocol (§7).
   - Thresholds are placed at **change points** where a fixed reference configuration's sustained behaviour departs from its nominal behaviour beyond measurement noise. Examples are the onset of frequency capping, or sustained latency drift at a fixed configuration, measured for threshold derivation only.
   - Where no change point exists, thresholds are placed at pre-registered quantiles of the signal distribution under the corresponding pressure protocol (quantile choice: DECISION REQUIRED BEFORE DATA COLLECTION).
3. **Separation of data.**
   - Threshold derivation uses E0 pilot data only.
   - Pilot data are excluded from confirmatory analysis.
4. **Freezing.**
   - All thresholds, hysteresis bands, dwell times and the classification rule are written to the experiment configuration.
   - The configuration's hash and git commit are recorded before E1/E2 confirmatory runs.
   - Any later change voids the confirmatory status of runs made before it, and is logged as a protocol deviation.

### 5. Hysteresis, dwell time, cooldown, transitions

| Mechanism | Rule | Value |
| :-- | :-- | :-- |
| Hysteresis | Each threshold has an entry value and a lower exit value. The band width is derived from the E0 noise of the signal: a pre-registered multiple of its observed short-term variability. | Multiple: DECISION REQUIRED BEFORE DATA COLLECTION |
| Minimum dwell time | A new state is adopted only after the classified level persists for the dwell time. The dwell time must exceed the measured configuration-switch cost (model load or swap time, from E0) by a pre-registered factor. | TO BE DERIVED FROM E0 |
| Transition rule | Escalation to a higher-pressure state may skip levels (R0 → R2) after dwell. De-escalation moves one level at a time, after the exit threshold and dwell time. | Rule fixed here; timings from E0 |
| Cooldown (within run) | After de-escalation, no further de-escalation until another dwell period has elapsed. | From E0 |
| Cooldown (between runs) | A run starts only when the device has returned to a defined start window (battery temperature and thermal status within the band recorded at idle in E0) after a minimum rest. | Window from E0 |
| Logging | Every classification sample and every transition: timestamp, raw signals, per-dimension level, resulting state, triggering dimension, dwell timer. | Required (log schema) |

Given the same logged signal stream and the frozen configuration, the classifier is deterministic, so another researcher can reproduce every state transition.

### 6. Natural device state vs controlled resource-pressure condition

| | Natural device state | Controlled resource-pressure condition |
| :-- | :-- | :-- |
| Source | Whatever the device experiences during a run, including heat and load from the inspection workload itself | A scripted pressure protocol applied by the experimenter |
| Role | Logged covariate and runtime input to the estimator | The manipulated factor (E1: held at a target level; E2: scripted schedule) |
| Analysis | Exploratory only | Confirmatory |

**Feedback is expected.** A heavier configuration heats the device more. In E2 the baselines therefore share the same **controlled pressure schedule**, but not necessarily the same realised R-state trajectory. The realised trajectory is a mediator and is reported per baseline. This is by design: B1's inability to sustain C1 under pressure is part of what is measured.

### 7. Controlled pressure mechanisms (candidates; none selected or implemented)

| Candidate | Targets | Reproducibility requirement | Concern |
| :-- | :-- | :-- | :-- |
| P-load: scripted background compute workload in a separate process (fixed thread count and duty cycle) | Compute, thermal | Same workload binary, parameters and start offset per run | Its own energy is included in whole-device energy, so energy is compared between baselines under the identical workload, not as an absolute per-item value |
| P-thermal: pre-heating soak with a fixed workload until a target thermal level, then the run | Thermal | Same soak workload and target, reached and logged | Ambient temperature must be controlled or logged |
| P-memory: separate process holding a scripted amount of memory | Memory | Same allocation schedule; the platform low-memory response is logged | The OS may kill processes, so stability must be checked in E0 |
| P-battery: start the run within a pre-registered battery-level window, and/or enable power-save mode | Battery | Window and mode recorded | Battery level cannot be set instantly; discharge protocol needed |

**Selection criteria** (DECISION REQUIRED after E0):
- reproducible to within E0-measured variability;
- has a manipulation check in telemetry;
- does not change the inspection app's code path;
- effect on the measured energy can be held constant across compared conditions.

No threshold is chosen for convenience, such as a fixed round CPU or RAM percentage.

### 8. Runtime adaptation policy (general)

**Pipeline:** device state → resource state → configuration → inspection inference → calibrated confidence → verification if needed.

Resource adaptation (choosing C from R) and confidence verification (choosing A from confidence) are separate modules. B3 enables only the first, B4 only the second, and B5 both.

| Element | Rule |
| :-- | :-- |
| R → allowed configurations | For each state, the highest ladder configuration that satisfies the state's admissibility criteria measured in E1: fits in memory without low-memory signals; meets the pre-registered per-item time budget; does not, by itself, raise the thermal level within a pre-registered window. Criteria are fixed here; values come from E1 (DECISION REQUIRED BEFORE DATA COLLECTION for the time budget). |
| Candidate default mapping | R0→C1, R1→C2, R2→C3, R3→C4. **Candidate only.** The final mapping is derived from E1 and frozen; it may assign the same configuration to two states. |
| Downgrade | Immediate (after state dwell) to the configuration allowed by the new state; rungs may be skipped. |
| Upgrade | One rung at a time, only after the state has de-escalated and dwelled. |
| Switch timing | Only between items, never within an item or its verification actions. |
| Anti-thrashing | (a) The dwell time and hysteresis above; (b) a cap on configuration switches per time window, value from E0 switch cost (DECISION REQUIRED BEFORE DATA COLLECTION). Cap hits are logged. |
| Model residency | Which configurations stay loaded at once is constrained by RAM and decided after E0 measures each configuration's memory. Options: current only; current plus the escalation target; all. (DECISION REQUIRED.) |
| Logging | Every configuration decision: state, allowed set, chosen configuration, switch time, load or swap latency, cap events. |

## Part II — OPPO A5 2020 (3 GB) Instantiation

The general framework is instantiated on the confirmed platform as follows. **All values are to be measured.**

| Item | Instantiation | Status |
| :-- | :-- | :-- |
| Thermal dimension | Platform thermal status **only if the installed Android API level is at least 29**. The launch version is Android 9 (API 28, which has no thermal-status API); the installed version is unknown. Otherwise: battery temperature, readable thermal zones via ADB, and CPU-frequency capping. | REQUIRES DEVICE VERIFICATION |
| Thermal headroom | Usable only at API level 30 or later. | REQUIRES DEVICE VERIFICATION |
| Memory dimension | Available RAM and low-memory flag. The 3 GB variant makes memory a binding dimension: whether C1 plus the camera pipeline fits is measured in E0. | TO BE MEASURED |
| Battery dimension | Level, power-save mode (ColorOS power-saving behaviour to be characterised), charging disabled during runs. | REQUIRES DEVICE VERIFICATION |
| Compute dimension | Host-side CPU utilisation and frequency over ADB/Perfetto (Perfetto availability depends on the installed Android version). | REQUIRES DEVICE VERIFICATION |
| Vendor background management | ColorOS may restrict or kill background processes, which affects the pressure processes and logging. | REQUIRES DEVICE VERIFICATION |
| Thresholds, bands, dwell, cooldown | Derived from E0 on this device. | TO BE MEASURED |
