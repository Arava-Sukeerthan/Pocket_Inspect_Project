# Experimental Framework — GC-03

_Step 10A, 2026-10-05, Claude Code._

**Proposed idea / planning artefact only.** Nothing here is implemented, no experiment has been run and no device has been measured. Every numerical threshold is **TO BE CALIBRATED DURING EXPERIMENT DESIGN**; no model architecture is chosen (Step 10B). Declarative identifiers are in [`configs/research_protocol.yaml`](../../configs/research_protocol.yaml).

## 1. Resource-State Framework (R0–R3)

The resource state is a qualitative, ordered decision variable derived from measured telemetry. Candidate telemetry sources on Android (Assumption; availability must be verified on the chosen device): the platform thermal-status API (`PowerManager`), battery level, current and charge counters (`BatteryManager`), power-saver mode, CPU/GPU utilisation and frequency where readable, and available memory and low-memory signals (`ActivityManager`).

**Common rules for all states.**
- **Measured in every state:** battery level and charging state; thermal status and battery/skin temperature; CPU/GPU utilisation (and frequency where readable); available memory; power-saver mode; ambient temperature where controlled.
- **Transitions** use thresholds on the measured signals with hysteresis and a minimum dwell time, so the state does not oscillate. All thresholds, hysteresis bands, dwell times and sampling periods: **TO BE CALIBRATED DURING EXPERIMENT DESIGN**.
- **Recorded for every inference:** the state, the raw telemetry behind it, and every transition with its cause.

| State | Meaning | Transition trigger (thresholds TO BE CALIBRATED DURING EXPERIMENT DESIGN) | Permitted adaptation | Possible configuration changes | Must be recorded |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **R0 — nominal** | No resource constraint is active. | Enter: all signals inside the nominal band for the dwell time. Leave: any signal crosses the R1 entry threshold. | None required; recovery upward to C1 permitted. | C1 (default). | State, telemetry, configuration, time in state. |
| **R1 — moderate resource pressure** | Sustained load, rising temperature or declining battery that does not yet threaten operation. | Enter: any signal crosses the R1 threshold for the dwell time. Leave: return to the nominal band (with hysteresis) or escalation to R2. | One-step downgrade; verification actions all permitted. | C1 → C2. | As R0, plus downgrade events and the triggering signal. |
| **R2 — high resource pressure** | Thermal throttling likely or active, low battery, or memory pressure. | Enter: any signal crosses the R2 threshold, or thermal status reports throttling. Leave: as R1. | Further downgrade; costly verification actions restricted (A3 escalation limited or disabled per policy). | C2 → C3. | As R1, plus restricted-action events. |
| **R3 — critical resource pressure** | Continued operation at risk (e.g. severe thermal status, critical battery, low-memory signal). | Enter: any signal crosses the R3 threshold or the OS reports a critical condition. Leave: as R1. | Emergency configuration only; only low-cost verification actions (A0, A4; A1 only if acquisition cost is permitted). | C3 → C4. | As R2, plus any skipped or deferred items. |

The coupling between the two mechanisms is visible here: the resource state limits which verification actions are permitted, so verification is resource-aware, not independent of the adaptation policy.

## 2. Inference Configuration Ladder (C1–C4)

A configuration is the full inference setting: model variant, input resolution, numeric precision and execution backend. Configurations are defined conceptually; actual choices belong to Step 10B.

**Requirements on the ladder as a whole.**
- All configurations share the same label space and output schema, so accuracy metrics are comparable.
- Expected accuracy is non-increasing and expected resource cost is non-increasing from C1 to C4. This ordering is an **Assumption to be verified on the device** (E1): a nominally lighter configuration may not be cheaper on a given device, for example after a delegate fallback.
- Each configuration exposes a confidence score for every prediction, so verification can act on it.
- Each configuration must be exportable to an on-device runtime (TFLite or ONNX Runtime) per `RESEARCH_RULES.md` §8.

| Configuration | Accuracy | Latency | Memory | Energy | Thermal behaviour | Input requirements |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **C1 — highest-accuracy** | Highest on the ladder; used as the B1 reference. | Highest; must still complete an item within the task's time budget at R0. | Highest; must fit the device without triggering low-memory kills at R0. | Highest per item. | May not be sustainable under continuous load; this is the motivation for adaptation. | Highest input resolution on the ladder; standard capture. |
| **C2 — medium** | Below C1. | Below C1. | Below C1. | Below C1. | Sustainable for longer than C1 (to verify). | Same capture; input resolution ≤ C1. |
| **C3 — lightweight** | Below C2; used as the B2 reference (or C4 if pre-registered). | Below C2. | Below C2. | Below C2. | Sustainable under moderate pressure (to verify). | Same capture; input resolution ≤ C2. |
| **C4 — emergency / lowest-resource** | Lowest acceptable; must still produce a valid prediction and confidence. | Lowest. | Lowest; must run under low-memory conditions. | Lowest. | Must not worsen a critical thermal state. | Same capture; lowest input resolution on the ladder. |

The ladder also defines the stronger model used by escalation (A3): escalation moves an item to a configuration higher on the ladder, subject to the actions permitted by the current resource state.

## 3. Confidence-Aware Verification

**Pipeline.** confidence → verification policy → downstream action.

1. **Confidence.** The configuration that produced the prediction outputs a confidence score (and optionally an uncertainty estimate).
2. **Verification policy.** Inputs: confidence, the configuration that produced it, the current resource state, and the item's verification history (to cap repeated actions). It compares confidence with a **configuration-specific** threshold (calibrated per configuration because calibration may differ, H4) and selects one action from those the resource state permits. Thresholds, caps and action priorities: **TO BE CALIBRATED DURING EXPERIMENT DESIGN**. One action is pre-registered as primary.
3. **Downstream action.**

| Action | Meaning | Cost (qualitative) | Notes |
| :-- | :-- | :-- | :-- |
| A0 — accept prediction | Confidence is sufficient; output is final. | None | Default. |
| A1 — recapture same view | Capture the same view again and re-infer. | Acquisition + one inference | Needs physical capture; on replayed datasets it can only be approximated, which is a stated limitation. |
| A2 — acquire additional view | Capture or load a different view and re-infer; fuse decisions by a pre-registered rule. | Acquisition + one inference + fusion | On multi-view datasets, stored views stand in for new captures (Stage 1 proxy). |
| A3 — escalate to stronger model | Re-run the item on a configuration higher on the ladder. | One higher-cost inference | Permission depends on resource state. |
| A4 — request human review | Refer the item to an operator. | Human time; reduces coverage | Reported as referral rate and coverage; never counted silently as correct. |

**How the mechanism differs from a fixed confidence threshold.** A fixed-threshold policy uses one global threshold and one action regardless of configuration and resource state. The proposed mechanism differs in three testable ways: thresholds are configuration-specific; the permitted action set depends on resource state; and escalation targets depend on the ladder position. The ablation **B5-F** (B5 with one fixed global threshold and the same primary action) isolates these differences in E3 (H2.b). If B5 is not better than B5-F, the mechanism reduces to fixed-threshold gating and this is reported.

## 4. Baselines

| Baseline | Enabled | Disabled | Purpose | Comparison it enables |
| :-- | :-- | :-- | :-- | :-- |
| **B1 — Static best model** | C1 for every item. | Resource adaptation; verification. | Accuracy reference and cost ceiling; shows the throttling cost of not adapting. | B3 vs B1 (H1); B5 vs B1 (F3); reference point for H5. |
| **B2 — Static lightweight model** | The lightweight configuration (C3, or C4 if pre-registered) for every item. | Resource adaptation; verification. | Cost floor and accuracy floor. | Lower reference for H5; bounds how far B3 can degrade. |
| **B3 — Resource adaptation only** | State-driven configuration switching (R → C). | Verification (always A0). | Isolates degradation caused by downgrading. | B3 vs B1 (H1); B5 vs B3 (H2, H3); H5. |
| **B4 — Confidence verification only** | Verification on a fixed, pre-registered configuration. | Resource adaptation. | Isolates the verification effect without downgrading. | B5 vs B4 (H5); verification overhead without adaptation (H3). |
| **B5 — Resource adaptation + confidence verification** | Both mechanisms, coupled as in §1 and §3. | Nothing. | The system under test. | All hypotheses. |
| B5-F (ablation of B5, not a sixth baseline) | As B5, with one fixed global threshold. | Configuration-specific thresholds and state-dependent action sets. | Distinguishes the mechanism from fixed-threshold gating. | B5 vs B5-F (H2.b). |

All baselines use the same device, dataset, item order, ladder and resource-pressure schedule.

## 5. Experiment Families (planned, not run)

| ID | Design | Hypotheses |
| :-- | :-- | :-- |
| E1 | Forced-configuration sweep: every configuration C1–C4 under every induced resource state R0–R3, verification disabled. Characterises accuracy, calibration and cost per cell and verifies the ladder ordering. | H1 (bounds), H3 (instrument resolution), H4 |
| E2 | Policy-driven episodes: B1–B5 under identical scripted resource-pressure schedules on identical item sequences, repeated runs. | H1, H2, H3, H5 |
| E3 | Verification-policy ablation: B5 vs B5-F under the E2 schedules. | H2.b |

## 6. Falsification Criteria

GC-03 is experimentally weakened if any of the following holds. Each criterion is judged on both **statistical significance** (the pre-registered test rejects the null at the pre-registered level after Holm correction) and **practical significance** (the confidence interval lies beyond the pre-registered smallest effect size of interest). No effect size is fixed here. A "no meaningful difference" conclusion requires an equivalence test against the SESOI.

| ID | GC-03 is weakened if… | Test | Hypothesis |
| :-- | :-- | :-- | :-- |
| F1 | Resource adaptation produces no meaningful resource benefit: B3 cost is equivalent to B1 cost, or B3 does not prolong sustained operation under the schedule. | Cost difference CI within ±SESOI (TOST). | H1 (context), H5 |
| F2 | Confidence verification does not recover measurable performance: M(B5) − M(B3) is not significantly greater than zero or is within ±SESOI. | Paired McNemar and bootstrap CI on ρ. | H2 |
| F3 | Recovery is no better than simply using the static best model: B5 needs at least B1's cost to reach its accuracy, or B1 dominates B5. | Matched-cost accuracy comparison; Pareto dominance with bootstrap uncertainty. | H5 |
| F4 | Verification overhead eliminates the efficiency benefit: B5 cost − B3 cost ≥ B1 cost − B3 cost. | Bootstrap CI on the cost differences. | H3, H5 |
| F5 | Confidence calibration does not meaningfully change across configurations/resource states: per-configuration calibration differences are within ±SESOI. | Bootstrap CIs on ECE/Brier; equivalence test. | H4 |
| F6 | The combined method does not outperform appropriate ablations: B5 is dominated by or equivalent to B3 or B4. | Pareto and matched-budget comparisons. | H5 |

**Interpretation.**
- F2, F3, F4 or F6 holding answers RQ1 negatively for the tested device, dataset and ladder. That is a reportable result, not a failure to report.
- F5 holding does not refute RQ1 on its own; it means configuration-specific thresholds are unnecessary, which weakens H2.b.
- F1 holding means the adaptation policy is not useful on the tested device, so the downgrade-recovery question does not arise in practice.

## 7. Contribution Boundary

**CANDIDATE CONTRIBUTION — TO BE VALIDATED EXPERIMENTALLY**

> An empirical investigation of whether confidence-aware downstream verification can recover inspection performance degraded by resource-driven runtime configuration changes on a resource-constrained smartphone, including analysis of accuracy, calibration, latency, energy, thermal behavior, and verification overhead.

**The project will not claim:**
- to be the first smartphone inspection system;
- to be the first resource-aware inference system;
- to be the first confidence-aware inspection system;
- to be the first adaptive inspection system;
- universal novelty, or novelty beyond the reviewed corpus and logged searches;
- superiority over all existing systems;
- generalisation to devices, datasets, defect types or tasks that were not tested;
- that any hypothesis is supported before the pre-registered analysis is run.

**What may be claimed, if the experiments support it:** an empirical answer to RQ1–RQ6 for the tested device, ladder and dataset, with the stated limitations of the literature boundary ([`research_gap.md`](../gap_analysis/research_gap.md) §2, §7).

## 8. Status

Planning artefact only. No implementation, no dataset download, no experiment, no measurement, no results.
