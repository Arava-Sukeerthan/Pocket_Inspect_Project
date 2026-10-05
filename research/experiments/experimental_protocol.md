# Experimental Protocol — Resource-Aware Adaptive Inspection with Confidence-Aware Verification

_Step 10C, 2026-10-05, Claude Code._

**Protocol design only.** No experiment has been run. No measurement, model benchmark, dataset collection or empirical result exists. Every value this protocol needs is either derived later by a frozen rule or marked **TO BE MEASURED**, **REQUIRES DEVICE VERIFICATION** or **DECISION REQUIRED BEFORE DATA COLLECTION**.

Approved gap (unchanged): [`research_gap.md`](../gap_analysis/research_gap.md). Research questions, hypotheses and variables (unchanged): [`research/research_questions/`](../research_questions/). Declarative configuration: [`configs/experiment_protocol.yaml`](../../configs/experiment_protocol.yaml).

Companion documents:
- [`generalization_framework.md`](generalization_framework.md)
- [`resource_states.md`](resource_states.md)
- [`model_selection_protocol.md`](model_selection_protocol.md)
- [`confidence_verification_protocol.md`](confidence_verification_protocol.md)
- [`measurement_protocol.md`](measurement_protocol.md)
- [`experimental_matrix.csv`](experimental_matrix.csv)
- [`log_schema.json`](log_schema.json)

## 1. Research Positioning

**Primary RQ (unchanged).** "Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained smartphone dynamically downgrades its inference configuration under changing device conditions?"

**What is investigated.** An adaptive, resource-aware Edge-AI visual-inspection **methodology** for resource-constrained and legacy smartphones, experimentally demonstrated on an OPPO A5 2020 with 3 GB RAM. The methodology couples device-state-driven runtime adaptation with confidence-aware downstream verification.

**Device-generalization principle.**

> The OPPO A5 2020 serves as the primary experimental platform rather than defining the scope of the proposed methodology. The methodology is intended for resource-constrained and legacy smartphones more generally. Device-specific results are reported as evidence obtained on the selected platform, while claims of generalization beyond the evaluated device are limited to what the experimental design supports.

**Three levels are kept separate.** They are general methodology, the experimental device, and device-specific measurements ([`generalization_framework.md`](generalization_framework.md) §1). Results are classified as device-specific, methodological, generalization evidence, or unvalidated generalization (§2 there).

## 2. General Architecture (device-independent)

```
                    Visual Input
                         |
                         v
                 Resource Monitor          (device-state signals only)
                         |
                         v
              Resource-State Estimator     (R0-R3, frozen rule-based classifier)
                         |
                         v
             Adaptive Model Selection      (frozen R -> C mapping, hysteresis, dwell)
                         |
                    C1 / C2 / C3 / C4
                         |
                         v
                 Inspection Result
                         |
                         v
               Calibrated Confidence       (per-configuration temperature scaling)
                         |
              +----------+----------+
              |                     |
        High confidence       Low confidence
              |                     |
              v                     v
            Accept (A0)        Verification (permitted by stage and resource state)
                                  |
                    +-------------+-------------+-------------+
                    |             |             |             |
              Recapture (A1)  New view (A2)  Stronger      Human
              [Stage 2 only]  [Stage 1:      model (A3)    review (A4)
                              simulated]
                                  |
                                  v
                            Final Decision
```

**Device independence.**
- No component depends on OPPO-specific APIs.
- Device-specific choices (which telemetry signals exist, thresholds, the ladder) are made by the instantiation procedures for the device at hand.
- Those choices are documented in the "OPPO A5 2020 instantiation" sections of the companion documents.

## 3. Experimental Platform

**Confirmed device (gate G1 closed, 2026-10-05):** OPPO A5 2020, **3 GB RAM variant** (Snapdragon 665, Adreno 610).
- The 4 GB and 6 GB variants are not the experimental platform, and their specifications are not used.
- Specifications (A), capabilities requiring verification (B) and measurements still to be obtained (C) are separated in [`measurement_protocol.md`](measurement_protocol.md) §1.
- The device is a representative member of the resource-constrained class, not the research contribution.

## 4. Experiment Families and Stages

| ID | Name | Purpose | Status in analysis |
| :-- | :-- | :-- | :-- |
| E0 | Device characterisation and pilot | Telemetry availability, signal noise, threshold derivation, load and switch costs, energy-counter validation, ladder steps 3–7, sample-size pilot | Pilot only; excluded from confirmatory tests |
| E1 | Forced-configuration sweep | C1–C4 × R0–R3 under controlled pressure, verification disabled; per-cell accuracy, calibration and cost; derives the R → C mapping and the verification costs | Characterisation; confirmatory for H4 |
| E2 | Policy-driven baseline episodes | B1–B5 on identical item sequences under identical controlled pressure schedules | Confirmatory for H1, H2, H3, H5 |
| E3 | Verification-policy ablation | B5 vs B5-F under the E2 schedules | Confirmatory for H2.b |

| Stage | Data | Verification actions | What it can and cannot show |
| :-- | :-- | :-- | :-- |
| **Stage 1** | Real-IAD (PROVISIONAL primary), replayed on the device | A0, A2 (**controlled additional-view simulation** from stored views), A3, A4 | Adaptation, recovery via simulated additional views and escalation, calibration, cost. **Cannot** test physical smartphone same-view recapture: Real-IAD stored views are **not** smartphone recapture. |
| **Stage 2** | Custom smartphone-captured dataset: **PROTOCOL ONLY — NOT YET COLLECTED** (§11) | A0–A4, with actual A1 and A2 capture | Physical recapture and real smartphone capture. Conditional on gate G3 and data collection. |

## 5. Baselines

Unchanged from Step 10A. Their definitions do not depend on the device.

| Baseline | Model policy | Resource adaptation | Confidence verification | Purpose |
| :-- | :-- | :-- | :-- | :-- |
| B1 — Static best model | C1 for every item | Disabled | Disabled (A0 always) | Accuracy reference and cost ceiling; exposes the cost of not adapting |
| B2 — Static lightweight model | C3 for every item (C4 if pre-registered) | Disabled | Disabled | Cost floor and accuracy floor |
| B3 — Resource adaptation only | R → C mapping (frozen) | Enabled | Disabled | Isolates degradation caused by downgrading (H1) |
| B4 — Confidence verification only | One fixed pre-registered configuration | Disabled | Enabled (configuration-specific τ) | Isolates the verification effect without downgrading |
| B5 — Resource adaptation + confidence verification | R → C mapping (frozen) | Enabled | Enabled (configuration-specific τ, state-dependent actions) | The methodology under test |
| B5-F — **ablation of B5**, not a sixth primary baseline | As B5 | Enabled | Enabled with one fixed global threshold τ_F | Isolates the contribution of configuration-specific thresholds (H2.b) |

## 6. Recovery Metric

**Recovery** = (B5 − B3) / (B1 − B3), that is ρ = [M(B5) − M(B3)] / [M(B1) − M(B3)].

- **Performance measure M.**
  - Item-level **defect recall** on the test split (Step 10A primary metric), computed on the automated decision at matched coverage.
  - A4 referrals are reported separately, never counted silently as correct.
  - ρ is also reported, as a secondary analysis, with F1 in place of recall.
- **Guard against gaming.**
  - Recall can be raised by shifting decisions toward "defective", so precision and false-reject rate are always reported with ρ.
  - Whether a precision non-inferiority condition becomes a formal co-requirement is a **DECISION REQUIRED BEFORE DATA COLLECTION**. It is recorded here as an open issue, not silently added to H2.
- **Denominator edge case.**
  - If B1 − B3 is zero or practically negligible, ρ is **undefined or uninformative** and is **not** interpreted as evidence of recovery.
  - "Practically negligible" means the confidence interval for M(B1) − M(B3) does not lie entirely above the SESOI.
  - In that case H2 is reported as **not testable**, and only M(B5) − M(B3) with its CI is reported descriptively.
- **Pre-data-collection procedure for the SESOI.**
  1. Derive a requirement-based value from the inspection use case (the smallest recall change that would alter an inspection decision).
  2. Derive the smallest detectable difference from the E0 pilot (the measurement and replay variability of M).
  3. Adopt the larger of the two, and document and freeze it before confirmatory data.
  4. **Value: PRE-DATA-COLLECTION DECISION REQUIRED.**

## 7. Repetition and Control

| Element | Rule |
| :-- | :-- |
| Warm-up | A pre-registered number of unscored warm-up items per configuration after each model load (number from E0, where latency stabilises) |
| Cold start | Model load time is measured separately from steady-state latency; cold-start runs are a separate, labelled condition |
| Model loading | Load and swap policy per [`resource_states.md`](resource_states.md) §8; every load is timed and logged |
| Image order | Randomised per run from a recorded seed; within a run, all baselines use the **same** order |
| Condition order | Baselines and pressure schedules counterbalanced across runs (Latin-square or randomised blocks, seed recorded) to spread drift (battery wear, ambient) across conditions |
| Battery starting range | Each run starts within a pre-registered battery-level window (from E0) |
| Charging policy | Charging disabled during runs; charging between runs only to return to the start window, followed by the cooldown rule |
| Ambient temperature | Recorded continuously; runs start only within a pre-registered ambient window (controlled room or logged) |
| Background processes | Fixed app set; non-essential apps stopped; the ColorOS background policy is characterised in E0; the pressure process is the only intentional load |
| Screen state | Fixed (on, fixed brightness, or off with a wake lock), the same for all runs; recorded |
| Network | Flight mode with Wi-Fi off during runs (offline inference); host connection over USB only if the energy reference allows, otherwise wireless ADB is excluded and logs are pulled after the run (DECISION REQUIRED after E0) |
| Camera (Stage 2) | Fixed resolution; AE/AF/AWB locks where supported; metadata logged |
| Random seeds | Recorded for splits, image order, condition order and any training |
| Log synchronisation | A shared sync event at the start and end of each run across phone, host and external instruments; offset and drift estimated and reported |
| Repeated runs | Number of runs per condition: **TO BE DETERMINED BY THE E0 PILOT** (below) |

**Sample-size and pilot procedure.**
1. E0 runs a pilot of each E2 condition on the validation split.
2. Run-to-run variability is estimated for the cost outcomes, together with the variability of the policy trajectory.
3. Item-level paired discordance rates are estimated for the McNemar comparisons.
4. The number of test items and the number of runs are computed to give the pre-registered power for the SESOI at the Holm-adjusted level. The power target and α are a **DECISION REQUIRED BEFORE DATA COLLECTION**.
5. If the test split cannot supply enough defective items, this is reported, and the minimum detectable effect is stated instead of a power claim.

Stage 1 replay is deterministic for a fixed item and configuration. Repeated runs therefore vary through the resource trajectory and the configuration choices, not through model noise. Repeated runs matter for policy-driven baselines and cost outcomes.

## 8. Statistical Analysis

The Step 10A tests are preserved ([`hypotheses.md`](../research_questions/hypotheses.md)). Issues found while operationalising them are recorded under **Refinement issues**. They are not silently applied.

| RQ / H | IVs | DVs | Unit of analysis | Test (Step 10A) | Effect size | CI | Practical significance | Multiplicity |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| RQ2 / H1 | Baseline B1 vs B3; pressure schedule | Recall (primary), precision, F1 | Item (paired across baselines) | Paired McNemar; paired bootstrap CI of M(B1) − M(B3) | Recall difference; discordant-pair odds ratio | Bootstrap (resampling items) | CI beyond SESOI | Holm across H1–H5 |
| RQ3 / H2 | B5 vs B3; action; threshold; state | Recall, ρ, coverage, action rates | Item | Paired McNemar; bootstrap CI of ρ, stratified by state and action | ρ; recall difference | Bootstrap | Recovery CI beyond SESOI at minimum coverage | Holm |
| RQ3 / H2.b | B5 vs B5-F | Recall at matched verification rate or cost | Item | Paired McNemar at matched rate; bootstrap | Recall difference | Bootstrap | Beyond SESOI | Secondary (reported, outside the Holm family) |
| RQ4 / H4 | Configuration (E1); state at fixed configuration (E1) | ECE, Brier, NLL, confidence distributions, AUROC | Configuration × state cell (items within the cell) | Bootstrap CIs of ECE/Brier differences; Kolmogorov–Smirnov tests on confidence distributions | ECE/Brier difference; KS statistic | Bootstrap | Calibration difference changes trigger rate or recovery beyond SESOI | Holm within H4 tests |
| RQ5 / H3 | Verification on vs off; action; state | Latency, energy, temperature, memory, overhead | Run (cost aggregates); item for latency | Mixed-effects model (condition fixed, run random) or paired Wilcoxon signed-rank across runs; bootstrap CIs | Cost difference per item and per verified item | Bootstrap / model-based | Compared with the adaptation saving (F4) | Holm |
| RQ6 / H5 | Baseline B1–B5; schedule | Accuracy, coverage, energy, latency, temperature, memory | Run (aggregates); item for accuracy | Pareto dominance with bootstrap uncertainty; matched-budget accuracy comparison | Matched-cost recall difference | Bootstrap | Beyond SESOI in accuracy at matched cost, or in cost at matched accuracy | Holm |
| RQ1 | — | — | — | Decision rule over H1, H2, H5 (Step 10A §7) | — | — | — | — |

**Statistical vs practical significance.**
- Statistical significance means the test rejects the null at the Holm-adjusted level.
- Practical significance means the CI lies beyond the SESOI.
- "No meaningful difference" requires equivalence testing (TOST) against the SESOI.
- α, power, the SESOIs (accuracy, cost) and binning schemes: **PRE-DATA-COLLECTION DECISION REQUIRED**.

**Refinement issues** (recorded; not applied without researcher decision):
1. **Repeated runs and McNemar.**
   - Each item appears once per run, and there are several runs, so McNemar on a single run discards data, while pooling runs violates independence.
   - Options: a designated primary run per item, per-item majority across runs, or a GLMM with item and run random effects.
   - DECISION REQUIRED BEFORE DATA COLLECTION.
2. **Item vs view.**
   - Stage 1 evaluates per-view predictions aggregated to item-level decisions.
   - The unit is the item; views are clustered within items.
3. **Recall-only recovery** can be gamed (§6). A precision co-requirement is DECISION REQUIRED.
4. **KS tests across many cells** may be underpowered for small cells. Minimum cell size: DECISION REQUIRED after the pilot.

## 9. Hypotheses, Falsification and Outcome Categories

Hypotheses (unchanged):
- **H1.** Resource-driven runtime downgrading decreases inspection performance relative to the best static configuration under equivalent task conditions.
- **H2.** Confidence-aware downstream verification recovers a measurable portion of the performance degradation introduced by resource-driven downgrading.
- **H3.** Confidence-aware verification introduces measurable latency, energy, memory, or thermal overhead.
- **H4.** Confidence distributions and calibration characteristics differ between inference configurations operating under different resource conditions.
- **H5.** A joint resource-adaptation + confidence-verification policy provides a more favorable accuracy–efficiency trade-off than either mechanism alone.

| H | Null | Alternative | Required comparison | Falsification | Practical criterion |
| :-- | :-- | :-- | :-- | :-- | :-- |
| H1 | M(B3) ≥ M(B1) | M(B3) < M(B1) | E2: B1 vs B3, same items and schedule | CI of M(B1) − M(B3) includes zero or lies within ±SESOI | Lower CI bound > SESOI |
| H2 | M(B5) ≤ M(B3) | M(B5) > M(B3) | E2: B5 vs B3; E3: B5 vs B5-F (H2.b) | CI includes zero or lies within ±SESOI at minimum coverage; not testable if H1 fails | Recovery CI beyond SESOI |
| H3 | Cost with verification = cost without, within measurement resolution | Higher for at least one cost metric | E1/E2: verification on vs off | No cost metric differs beyond resolution | Overhead compared with the adaptation saving |
| H4 | Calibration and confidence distributions equal across configurations (H4.a) and across states at a fixed configuration (H4.b) | They differ | E1 cells | Differences within ±SESOI (equivalence) | Changes trigger rate or recovery beyond SESOI |
| H5 | B5 dominated by or equivalent to B3 or B4; not better at matched cost | B5 non-dominated and better at matched cost | E2: B1–B5 | B5 dominated or equivalent (F6); needs at least B1 cost (F3); overhead removes saving (F4) | Beyond SESOI at matched cost |

**Falsification criteria F1–F6** (preserved from Step 10A, [`experimental_framework.md`](../research_questions/experimental_framework.md) §6):

| ID | GC-03 is weakened if… |
| :-- | :-- |
| F1 | Resource adaptation produces no meaningful resource benefit |
| F2 | Confidence verification does not recover measurable performance |
| F3 | Recovery is no better than simply using the static best model |
| F4 | Verification overhead eliminates the efficiency benefit |
| F5 | Confidence calibration does not meaningfully change across configurations/resource states |
| F6 | The combined method does not outperform appropriate ablations |

**Every outcome category is reportable.** The design does not depend on confirmation.

| Outcome | Pattern | Report |
| :-- | :-- | :-- |
| No benefit | H1 supported; H2 not supported (F2) | Negative result: verification does not recover the loss on this platform |
| Partial benefit | H2 supported statistically but not practically, or only for some actions or states | Recovery bounded; conditions reported |
| Trade-off | H2 supported, but F3 or F4 holds | Recovery exists but costs as much as not adapting |
| Negative result | B5 worse than B3, or adaptation gives no resource benefit (F1) | Reported as a finding about the methodology on this platform |
| Not testable | H1 not supported | No loss to recover; reported as a finding about adaptation |

## 10. Experimental Matrix

[`experimental_matrix.csv`](experimental_matrix.csv) lists every combination with its status: REQUIRED, OPTIONAL, PILOT_ONLY or NOT_APPLICABLE.

**Reduction rationale.** A full factorial of dataset × device × configuration × state × baseline × confidence policy × action would mostly contain incoherent cells:
- In E2, the configuration is chosen by each baseline's policy, so it is not a free factor.
- Verification actions apply only to baselines with verification enabled.
- A1 does not exist in Stage 1.

The matrix is therefore factorised:
- **E1** crosses configuration × state (the only full factorial).
- **E2** crosses baseline × pressure schedule, with confidence policy and action nested within the baselines that use them.
- **E3** is a single paired comparison.

There is one device. Future devices are not part of the current experiment.

## 11. Dataset Protocol

**Stage 1 — Real-IAD (PROVISIONAL; access and licence REQUIRE_VERIFICATION, Step 10B).**
- Item-level splits per [`confidence_verification_protocol.md`](confidence_verification_protocol.md) §1.
- Stored views are used for **controlled additional-view simulation** (A2) only.
- They are not smartphone recapture, and Stage 1 does not test physical recapture.

**Stage 2 — custom smartphone-captured dataset: PROTOCOL ONLY — NOT YET COLLECTED.** The capture protocol is general, so it can be repeated on other smartphones. The device is recorded per image (currently the OPPO A5 2020, 3 GB).

| Element | Protocol |
| :-- | :-- |
| Physical item IDs | A unique fiducial or label outside the inspected region; an item registry |
| Defect / non-defect labels | Fixed before capture (seeded defects from the project taxonomy, or verified non-defective); per-view visibility label |
| Repeated captures | Several captures per (item, view), with the item removed and re-placed between captures |
| Same-view recapture | Captures of the same indexed view position, providing A1 |
| Additional views | A pre-registered set of indexed views (jig or turntable), providing A2 |
| Camera settings | Fixed resolution; AE/AF/AWB locked where supported; per-frame metadata logged |
| Lighting | Fixed rig light; ambient light recorded |
| Environment | Room, ambient temperature, background |
| Distance and orientation | Fixed by jig; recorded per view index |
| Timestamp | Monotonic and wall-clock time per frame |
| Device state | R-state, raw telemetry and configuration at capture time |
| Resource telemetry | Logged per log schema where captures run under pressure |
| Splitting | By physical item, never by image |

All counts (items, views, recaptures) are **TO BE DETERMINED BY POWER ANALYSIS / PILOT**. Nothing is collected in Step 10C.

## 12. Logging and Reproducibility

**Logging.** One record per item decision per [`log_schema.json`](log_schema.json). Fields are marked REQUIRED, OPTIONAL or CONDITIONALLY_AVAILABLE. Unavailable fields are recorded as null with a reason, never filled with estimates.

**Reproducibility record** (per run; stored with the run log):
- device model and RAM variant, plus a unit identifier;
- Android version and build; app, runtime and delegate versions;
- model versions and file hashes; preprocessing version;
- dataset version and manifest hashes;
- random seeds;
- configuration files and their hashes (thresholds, mapping, policy);
- calibration artefacts (temperatures, threshold values) and their hashes;
- measurement hardware identity and calibration;
- ambient conditions;
- git commit;
- wall-clock and monotonic timestamps.

Another compatible resource-constrained smartphone can repeat the experiment by rerunning E0 and the ladder procedure on that device, with the general framework unchanged.

## 13. Verification Gates

| Gate | Status |
| :-- | :-- |
| G1 — actual smartphone confirmed | **CLOSED / VERIFIED**: OPPO A5 2020, 3 GB, confirmed by the researcher (2026-10-05). Device capabilities remain REQUIRES DEVICE VERIFICATION. |
| G2 — Real-IAD multi-view interpretation confirmed | OPEN / REQUIRES VERIFICATION (unchanged) |
| G3 — custom smartphone capture protocol confirmed | OPEN. Protocol specified in §11; physical dataset **NOT COLLECTED**. |
| G4 — C1–C4 empirical selection criteria confirmed | OPEN. Selection methodology defined ([`model_selection_protocol.md`](model_selection_protocol.md)); empirical selection not performed. |

## 14. Decisions Required Before Data Collection

> **Step 10C-DR update.** These items are resolved, frozen as procedures, or explicitly deferred in the canonical [`pre_data_collection_decision_register.md`](pre_data_collection_decision_register.md). That register uses a renumbered D-01 to D-16, and its §2 maps every item below to the new IDs.

| ID | Decision |
| :-- | :-- |
| D-01 | SESOI values (accuracy; cost) via the §6 procedure |
| D-02 | α, power target, and minimum cell sizes |
| D-03 | Primary cost metric for ladder ordering (latency or energy) |
| D-04 | Minimum functional inspection requirement (ladder step 6) |
| D-05 | Minimum rung count if four admissible configurations do not exist |
| D-06 | Threshold-selection rule (target trigger rate vs selective risk) |
| D-07 | Verification priority order, per-item cap, cap outcome, A2 fusion rule, primary action per stage |
| D-08 | Split proportions |
| D-09 | Classification logic confirmation (maximum severity vs composite), hysteresis multiple, quantile rule for continuous signals |
| D-10 | Controlled pressure mechanisms (after E0) |
| D-11 | Per-item time budget for admissibility |
| D-12 | Model residency policy under 3 GB RAM |
| D-13 | Repeated-run handling for McNemar (refinement issue 1) |
| D-14 | Precision co-requirement for recovery (refinement issue 3) |
| D-15 | Energy-validation acceptance criteria; network/ADB policy during runs |
| D-16 | Whether to add further devices for generalization evidence |

## 15. Status

Protocol only. **No experiments, measurements, model benchmarking, dataset collection, or empirical results were produced in Step 10C.**
