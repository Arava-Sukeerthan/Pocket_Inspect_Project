# Variables and Factors — GC-03

_Step 10A, 2026-10-05, Claude Code. Variable definitions only; nothing has been measured._

Hypotheses: [`hypotheses.md`](hypotheses.md). Resource states, configuration ladder and verification actions: [`experimental_framework.md`](experimental_framework.md).

## 1. Measurement Variables vs Decision Variables

The same quantity can play different roles, so every variable is tagged with one of two kinds.

- **Measurement variable.** Observed and logged; it is never chosen by the system. Examples: battery level, temperature, latency, recall.
- **Decision variable.** Chosen by a policy (or forced by the experimenter). Examples: resource state R (derived from telemetry by the state classifier), configuration C, verification action A, confidence threshold.

### 1.1 Three layers of resource variables

Measured telemetry, experimental resource condition and adaptation decision are different things and are never conflated.

| Layer | What it is | Examples | Role in the design |
| :-- | :-- | :-- | :-- |
| 1. Measured resource telemetry | Raw signals read from the device | Battery level and charging state, temperature / thermal status, CPU/GPU utilisation and frequency, available RAM, power-saver mode | **Measurement variables.** Logged continuously as covariates and as manipulation checks. Not independently manipulated factors unless a later experimental protocol specifies it. |
| 2. Experimental resource condition | The qualitative state R0–R3 | R0 nominal … R3 critical | **The manipulated resource factor.** The experimenter induces a target condition through a pressure protocol (load, thermal soak, battery/power-saver state). Telemetry verifies that the intended condition was reached; at runtime the policy classifies telemetry into R. |
| 3. Adaptation decision | The configuration C1–C4 chosen for an item | C1 → C2 under R1 | **Decision variable.** Forced by the experimenter in E1 (an independent variable); chosen by the policy from R in E2 (B3, B5), where it is a logged mediator, not a manipulated factor. |

The individual telemetry signals are correlated (load raises temperature; temperature triggers throttling), and the pressure protocol does not set them independently. Treating them as separate experimental factors would claim a factorial control that the design does not have. Analyses may use them as covariates only.

Consequences for the design:
- In **E1** (forced sweep) configuration and induced resource state are **manipulated** by the experimenter, so they are true independent variables.
- In **E2** (policy-driven) configuration and action are **endogenous**: they are outputs of the policies, driven by the resource-pressure schedule. The manipulated independent variables are the baseline (which mechanisms are enabled) and the pressure schedule; configuration and action are logged as mediators.
- The resource state R is a decision variable derived from measurement variables. Its thresholds are `TO BE CALIBRATED DURING EXPERIMENT DESIGN`.

## 2. Independent Variables

| Variable | Kind | Levels / form | Manipulated in |
| :-- | :-- | :-- | :-- |
| Resource-pressure condition | Layer 2: experimental condition (manipulated) | R0–R3 (E1); scripted R-state schedule (E2), induced by the pressure protocol | E1, E2 |
| Battery state (level, charging state, power-saver mode) | Layer 1: measured telemetry (input to R; manipulation check) | Logged; moved by the discharge / power-saver part of the protocol, not set independently | Not independently manipulated |
| Temperature (device thermal status, battery/skin temperature) | Layer 1: measured telemetry (input to R; manipulation check) | Logged; moved by thermal soak / sustained load | Not independently manipulated |
| CPU/GPU utilisation (and frequency where readable) | Layer 1: measured telemetry (input to R; manipulation check) | Logged; moved by scripted background load | Not independently manipulated |
| Available memory | Layer 1: measured telemetry (input to R; manipulation check) | Logged; moved by scripted memory pressure | Not independently manipulated |
| Inference configuration | Layer 3: adaptation decision | C1–C4 | Forced in E1; policy-chosen in E2 (B3, B5), logged as mediator |
| Adaptation state | Decision | Adaptation enabled/disabled; current state and transition history | E2 |
| Confidence threshold | Decision | Per configuration (B5) or fixed global (B5-F); values `to_be_calibrated` | E2, E3 |
| Baseline condition | Decision (experimenter) | B1–B5, B5-F | E2, E3 |

## 3. Dependent Variables

| Variable | Kind | Unit / form | Hypotheses |
| :-- | :-- | :-- | :-- |
| Precision | Measurement | Proportion | H1, H2, H5 |
| Recall (primary accuracy metric) | Measurement | Proportion | H1, H2, H5 |
| F1 | Measurement | Proportion | H1, H2, H5 |
| mAP (where the task is detection) | Measurement | Proportion | H1, H2, H5 |
| Calibration error (ECE, Brier; reliability diagrams) | Measurement | Proportion / score | H4 |
| Latency (per item, per verified item; tail percentiles) | Measurement | Time | H3, H5 |
| FPS / throughput | Measurement | Items per unit time | H3, H5 |
| Energy / power | Measurement | Energy per item; mean power | H3, H5 |
| Temperature (trajectory) | Measurement | Temperature over time | H3, H5 |
| Memory (peak, resident) | Measurement | Bytes | H3, H5 |
| Recapture rate (A1) | Measurement | Proportion of items | H2, H3 |
| Escalation rate (A3) | Measurement | Proportion of items | H2, H3 |
| Additional-view and human-review rates (A2, A4); coverage | Measurement | Proportion of items | H2, H3, H5 |
| Verification overhead | Measurement (derived) | Cost difference with vs without verification | H3, H5 |

Temperature appears as both an independent variable (as an input to resource state) and a dependent variable (as a consequence of the workload). In E2 it is a time-varying covariate, and analyses that use it as an outcome control for the induced pressure schedule.

## 4. Control Variables

| Variable | How it is held constant |
| :-- | :-- |
| Dataset | One pre-registered dataset per experiment; access and licence verified first. |
| Test split | Fixed, versioned split; identical item order across baselines. |
| Image resolution (capture) | Fixed capture resolution per experiment. |
| Preprocessing | One versioned preprocessing pipeline per configuration, recorded in `configs/`. |
| Camera parameters | Fixed exposure, focus, white balance, ISO where the API allows; logged otherwise. |
| Model input size | Fixed per configuration (part of the configuration definition, not varied within it). |
| Lighting (where controlled) | Fixed rig lighting for phone-captured data; recorded otherwise. |
| Object/view protocol | Pre-registered object placement and view set. |
| Software version | App, runtime, delegate and OS versions recorded and frozen per experiment. |
| Device model | One device model (and unit) per experiment; unit ID logged. |
| Battery charging state (where applicable) | Charging disabled or fixed per condition; logged. |
| Ambient temperature (where controlled) | Controlled room or logged ambient temperature; runs started from a defined cool-down state. |

## 5. Potential Mediators

| Mediator | Path |
| :-- | :-- |
| Confidence | Configuration → confidence → triggered action → accuracy. |
| Uncertainty (if estimated separately from confidence) | Same path as confidence. |
| Selected model/configuration | Resource state → configuration → accuracy and cost. |

Mediation is analysed descriptively (logged paths); no causal-mediation claim is made without a design that supports it.

## 6. Potential Moderators

| Moderator | Expected role (Hypothesis) |
| :-- | :-- |
| Defect type | Some defect classes may degrade more under lighter configurations and recover differently. |
| Scene complexity | May change confidence and the benefit of extra views. |
| Image quality (blur, exposure) | May change confidence and recapture benefit (A1). |
| Resource-pressure severity | Recovery may shrink as the permitted action set narrows in R2–R3. |
| Object/view condition | The benefit of A2 depends on whether additional views are informative. |

## 7. Logging Requirements (per inference)

Timestamp; item ID; view ID; baseline; R-state and the raw telemetry behind it; configuration; execution backend actually used; model output and confidence; action taken; latency breakdown (acquisition, preprocessing, inference, verification); energy counter; temperatures; memory; app/runtime/OS versions; git commit; config snapshot hash (`RESEARCH_RULES.md` §7).
