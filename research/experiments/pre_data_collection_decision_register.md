# Pre-Data-Collection Decision Register (Step 10C-DR)

_Step 10C-DR, 2026-10-05, Claude Code. Canonical register of the decisions that must be settled before data collection._

**Protocol / methodology only.** No experiment, measurement, model benchmark, dataset collection or empirical result exists. No numerical value in this register is a measurement. The only numbers that appear are the two values approved at the Step 10C-DR final freeze (α and target power) and standard constants of a named statistical method.

Frozen decisions: [`configs/pre_data_collection.yaml`](../../configs/pre_data_collection.yaml). Traceability: [`decision_traceability.csv`](decision_traceability.csv). Protocol: [`experimental_protocol.md`](experimental_protocol.md).

The approved gap (GC-03), RQ1, B1–B5, B5-F as an ablation, and the recovery metric (B5 − B3) / (B1 − B3) are **unchanged**. The experimental platform remains the OPPO A5 2020 (3 GB RAM variant), which is not the research contribution.

## 1. Status Legend

| Status | Meaning |
| :-- | :-- |
| RESOLVED | The decision is fixed now. Any value it produces is computed later by the stated deterministic rule. |
| PRE-DATA-COLLECTION FREEZE | A concrete choice is proposed; it becomes binding only after explicit researcher approval, which must happen before data collection. |
| PILOT-DEPENDENT | The procedure is fixed; the outcome needs E0/E1 pilot measurements and is frozen at the stated freeze point. |
| DEVICE-VERIFICATION DEPENDENT | The decision depends on what the OPPO A5 2020 actually exposes; this is verified in Step 10D before any pilot value is derived. |
| DEFERRED | Cannot be decided before a named external input exists; the experiment proceeds without it, with the stated limitation. |
| NOT APPLICABLE | Not needed under the current design. |

**Freeze categories** (Step 10C-DR final freeze). Every decision component is assigned to exactly one category in §3a.
- **FROZEN NOW**
- **PILOT-DEPENDENT**
- **DEVICE-VERIFICATION DEPENDENT**
- **REQUIRES FUTURE APPROVAL**

## 2. ID Mapping to Step 10C

This register uses the Step 10C-DR numbering. The Step 10C list (`experimental_protocol.md` §14) grouped some items differently, and no item was dropped.

| DR ID | Step 10C item(s) |
| :-- | :-- |
| D-01 | D-01 (SESOI) |
| D-02 | D-02 (α part) |
| D-03 | D-02 (power and minimum cell sizes) |
| D-04 | D-03 (primary cost metric) + D-05 (minimum rung count) |
| D-05 | D-04 (minimum inspection requirement) |
| D-06 | D-06 (threshold rule) |
| D-07 | D-07 (priority order, cap, cap outcome, primary action) |
| D-08 | D-07 (A2 fusion rule) |
| D-09 | D-08 (split proportions) |
| D-10 | D-09 (classification rule, hysteresis, quantile rule) |
| D-11 | D-10 (pressure mechanism) |
| D-12 | D-11 (time budget) |
| D-13 | D-12 (model residency) |
| D-14 | D-13 (repeated runs and McNemar) |
| D-15 | D-14 (precision co-requirement) |
| D-16 | D-15 (energy validation, network) + D-16 (additional devices) |

## 3. Register Summary

**Freeze points.**
- **FP-0:** before any pilot data.
- **FP-1:** after the E0 device-characterisation pilot.
- **FP-2:** after ladder selection (E0/E1 pilot on validation data).
- **FP-3:** after on-device calibration on the calibration splits.
- **FP-4:** before the first confirmatory (test-split) run.

All frozen artefacts carry a hash and a git commit.

| Decision ID | Decision | Current status | Resolution | Rationale | Evidence/source | Depends on measurement? | Freeze point | Impact on experiment |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| D-01 | Smallest meaningful effect (SESOI) | PILOT-DEPENDENT | max(requirement-based value, pilot smallest detectable difference); no requirement-based value exists yet | Prevents both trivially small and undetectable effects from being called meaningful | Step 10A hypotheses §1; Step 10C §6 | Yes (pilot variability) | FP-1 (procedure FP-0) | Practical significance for H1–H5, the recovery denominator rule, precision margin, energy acceptance |
| D-02 | Significance level | RESOLVED | FROZEN NOW: α = 0.05, two-sided tests, Holm correction over H1–H5 | Approved by the researcher at the Step 10C-DR final freeze; a new pre-data-collection decision, not an earlier project decision | Researcher approval (Step 10C-DR final freeze); Holm from Step 10A | No | Frozen (FP-0 satisfied for α) | All confirmatory tests; power (D-03) |
| D-03 | Statistical power and sample size | PILOT-DEPENDENT (target power frozen) | FROZEN NOW: target power = 0.80. PILOT-DEPENDENT: required item count and run count, from pilot effect and variability estimates with item-level clustering | Power is approved; sample size cannot be computed before variability is known | Researcher approval; Step 10C §7 | Yes (sample size) | Power frozen; sample size FP-1 | Test-split size (D-09), run count |
| D-04 | Resource-cost metric for ladder ordering | RESOLVED | Primary: median steady-state per-item latency at R0 on the device. Gates and checks: peak memory, energy, thermal rise. No composite score. | Directly measurable at high resolution; energy may lack a validated reference | Step 10B `model_ladder.md` S3; Step 10C ladder step 5 | Ordering values yes; rule no | FP-2 | Defines C1–C4 order; identities stay TO BE EMPIRICALLY DETERMINED |
| D-05 | Minimum inspection requirement | RESOLVED (requirement-based floor DEFERRED) | Better-than-no-skill on validation for recall, precision and AUROC (data-derived). A task-specified floor is added only when a documented requirement exists. | Blocks efficient-but-useless models without inventing a number | Step 10C ladder step 6 | Yes (validation data) | FP-2 | Ladder admissibility |
| D-06 | Confidence threshold rule | PRE-DATA-COLLECTION FREEZE (procedure frozen; risk target requires approval) | FROZEN NOW: risk-controlled selective-acceptance procedure on Calibration-τ with configuration-specific temperature scaling; one common acceptance-risk target for all configurations. REQUIRES FUTURE APPROVAL: the numerical risk target. | Thresholds follow a pre-specified acceptance risk, not equivalence to C1; deterministic; test set unused | Step 10C confidence protocol §3; review correction | Calibration data (not test) | Target at FP-0; τ values at FP-3 | B4, B5, B5-F thresholds |
| D-07 | Verification action order | PILOT-DEPENDENT | Eligibility by stage and resource-state permission; automated actions before A4; order among eligible automated actions by measured cost; each automated action at most once per item; then A4. Verification is not constrained by the C1 inference latency. | Bounded actions, no retry-until-success; verification overhead reported separately | Step 10C confidence protocol §4–5 | Yes (action costs) | FP-2 | B4, B5, B5-F behaviour |
| D-08 | Additional-view combination | RESOLVED (conditional on V-05) | Any-view late fusion: maximum calibrated defect probability across considered views; mean fusion as a pre-registered sensitivity analysis | Matches item-level label semantics (an item is defective if any view shows the defect) | Step 10B dataset §2, §5 | No (label semantics to verify) | FP-0 | A2 decisions |
| D-09 | Data split proportions | PILOT-DEPENDENT | Item-level, stratified, seeded; test size from D-03, calibration sizes from D-06 feasibility, remainder to train and validation | Sizes follow analysis needs, not convention | Step 10C confidence protocol §1 | Yes (D-03 pilot) | FP-1 | All splits |
| D-10 | Resource-state classification rule | DEVICE-VERIFICATION DEPENDENT (aggregation rule frozen; thresholds pilot-dependent) | FROZEN NOW: per-dimension ordinal levels, state = maximum, missing-telemetry handling, hysteresis, dwell, transitions, cooldown. DEVICE-VERIFICATION DEPENDENT: the thermal-dimension source (platform thermal status, or the temperature and frequency-capping fallback). No thermal mapping is inserted. | Platform thermal-status availability on the installed Android version is unknown | Step 10C `resource_states.md`; Step 10C measurement protocol §1 | Thresholds yes; thermal source needs device verification | Rule now; source in Step 10D; thresholds FP-1 | R0–R3 for all E1/E2 runs |
| D-11 | Controlled pressure mechanism | PILOT-DEPENDENT | Provisional primary: scripted background compute load (sustained). Secondary sensitivity: thermal pre-soak; power-save mode. Memory pressure: pilot-only unless stable. | Most reproducible and controllable; least change to the inspection code path | Step 10C `resource_states.md` §7 | Yes (pilot reproducibility) | FP-1 | Manipulated factor in E1/E2 |
| D-12 | Inference, verification and decision time | PILOT-DEPENDENT (latency separation frozen) | FROZEN NOW: inference latency, verification latency and total per-item decision time are measured and reported separately; verification is never forced inside the C1 inference latency. PILOT-DEPENDENT: the inference-latency admissibility reference. REQUIRES FUTURE APPROVAL: a total decision-time budget, only if one is needed. | Keeps verification overhead visible instead of hiding it inside a budget | Step 10C admissibility; review correction | Yes | FP-2 (inference reference) | Configuration admissibility; H3, H5 cost reporting |
| D-13 | Model memory residency | PILOT-DEPENDENT | Largest resident set that shows no low-memory flag and no process kill in the pilot (all four, else current + escalation target, else current only); identical across adaptive baselines | 3 GB RAM; loading cost measured separately | Step 10C `resource_states.md` §8 | Yes | FP-1 | Switch latency, A3 feasibility |
| D-14 | Repeated runs and McNemar | RESOLVED | Item-level aggregation across runs; paired item-level sign-flip permutation test with item-cluster bootstrap CI; McNemar retained only where each item gives exactly one paired observation | Runs are not independent observations | Step 10A H1/H2 tests; Step 10C refinement issue 1 | No | FP-0 | H1, H2, H2.b, H5 analyses |
| D-15 | Recovery and precision | RESOLVED (margin via D-01) | Recall-based recovery retained as primary; a claim of recovery also requires precision non-inferiority of B5 vs B3; F1-based recovery and false-reject rate are secondary | Prevents recall gain by over-calling defects | Step 10C §6, refinement issue 3 | Margin yes | FP-0 (rule); FP-1 (margin) | H2 decision |
| D-16 | Energy validation, network, devices | PRE-DATA-COLLECTION FREEZE (method, fallback, network and scope frozen; agreement threshold requires decision) | FROZEN NOW: an external battery-side reference is preferred; an explicit fallback hierarchy; no forced absolute energy; fully offline runs; USB disconnected for battery runs; OPPO A5 2020 the only platform. PRE-DATA-COLLECTION DECISION REQUIRED: the agreement threshold. DEVICE-VERIFICATION DEPENDENT: battery-bypass feasibility. | Defensible energy claims only; no charging confound; bounded scope | Step 10B/10C measurement docs; review correction | Agreement yes; feasibility needs device verification | Fallback level at FP-1 | Energy outcomes, telemetry, scope |

## 3a. Freeze Classification

| Category | Components |
| :-- | :-- |
| **FROZEN NOW** | D-02 α = 0.05, two-sided, Holm · D-03 target power 0.80 · D-04 cost-metric rule · D-05 no-skill floors · D-06 threshold-selection procedure · D-07 eligibility, stopping and at-most-once rules · D-08 fusion rule (conditional on V-05) · D-09 split procedure · D-10 aggregation and transition rules · D-12 separation of inference, verification and total decision time · D-14 clustered analysis · D-15 recovery metric and precision safeguard · D-16 energy method and fallback hierarchy, network policy, single-device scope |
| **PILOT-DEPENDENT** | D-01 SESOI values · D-03 item and run counts · D-07 order among automated actions · D-09 split sizes · D-10 continuous thresholds · D-11 pressure mechanism confirmation · D-12 inference-latency admissibility reference · D-13 resident set · D-15 precision margin · D-16 measured agreement and fallback level |
| **DEVICE-VERIFICATION DEPENDENT** (Step 10D) | D-10 thermal-dimension source (installed API level; thermal-status API or fallback) · D-16 battery-bypass feasibility · D-13 low-memory behaviour under ColorOS · D-11 process stability · on-device trace availability (D-16 B) |
| **REQUIRES FUTURE APPROVAL** | D-06 numerical acceptance-risk target · D-16 energy agreement threshold · D-12 total decision-time budget (only if needed) · D-05 requirement-based floor (DEFERRED until a documented requirement exists) · D-10 mapping of platform thermal-status levels, if the API exists · ECE binning rule |

## 4. Decisions in Detail

### D-01 — Smallest meaningful effect (SESOI) · PILOT-DEPENDENT

**NO NUMERICAL VALUE IS JUSTIFIED BEFORE PILOT CHARACTERIZATION.** The repository contains no task requirement (no stakeholder-specified miss rate, part specification or inspector baseline) from which a requirement-based value could be derived.

**Requirement-based component.** Admissible evidence:
- a documented acceptance criterion for the inspected parts (customer specification, standard, or internal QA rule) stating a tolerable miss rate or false-reject rate;
- or a measured human-inspector baseline on the same items.

Any such source must be cited in the SESOI memo. Without one, this component is **absent** (not zero), and the SESOI is detectability-based. This is stated as a limitation.

**Detectability component** (smallest detectable difference, SDD):
1. Run the E2 pilot (B1, B3, B5) on the **validation** split under the pilot pressure schedule, with repeated runs.
2. Compute per-item aggregated correctness (D-14) and the paired per-item differences.
3. Estimate the standard error of the paired recall difference by **item-cluster bootstrap**, resampling items with all their runs, scaled to the planned test-split item count.
4. SDD = the half-width of the two-sided (1 − α_Holm,first) confidence interval implied by that standard error, where α_Holm,first is the most stringent Holm level from D-02.
5. Repeat for the precision difference (D-15) and for each cost outcome: latency and energy per item (run-level, from repeated-run variability), and thermal rise.

**Final value.** SESOI = the larger of the two components, per outcome. It is recorded in a SESOI memo with the pilot data hash and frozen at **FP-1**, before any test-split run. Pilot data are excluded from confirmatory analysis.

### D-02 — Significance level · RESOLVED

**FROZEN NOW** (approved by the researcher at the Step 10C-DR final freeze):
- α = 0.05;
- two-sided tests;
- Holm correction across the confirmatory family H1–H5.

This is a **newly approved pre-data-collection decision**. It is not an earlier project decision: before this freeze, `configs/research_protocol.yaml` recorded `significance_level: to_be_preregistered`.

Holm was approved in Step 10A and is preserved. H2.b and the per-action and per-state analyses are secondary and reported with unadjusted CIs labelled secondary.

Direction is checked from the estimate. The approved hypotheses are not rewritten.

### D-03 — Statistical power and sample size · PILOT-DEPENDENT (target power frozen)

| Element | Specification |
| :-- | :-- |
| Target power | **FROZEN NOW: 0.80** (researcher approval, Step 10C-DR final freeze) |
| α | 0.05 two-sided with Holm (D-02). The a-priori calculation uses the most stringent Holm level, so it is conservative. |
| Primary comparison | H2: B5 vs B3, the recovery comparison central to RQ1 (H1 is its precondition) |
| Primary endpoint | Item-level defect recall on defective test items, with each item's correctness aggregated across runs (D-14) |
| Effect-size input | The recall SESOI from D-01, estimated in the pilot |
| Variance input | Pilot (validation split): item-level variance of aggregated paired differences and B5/B3 discordance |
| Paired / repeated structure | Paired by item. Repeated runs are aggregated **within** each item, so each item contributes one paired observation. Runs are never treated as independent observations. |
| Sample-size calculation | Paired-proportion (McNemar-type, Connor 1987) formula on the aggregated item-level discordance, cross-checked by simulation from item-cluster bootstrap resamples of the pilot. The larger requirement is adopted. |
| Required item count | **PILOT-DEPENDENT.** n_defective from the calculation; total test items = n_defective / (defect prevalence in the stratified test split). No count is stated before the pilot. |
| Runs per condition | **PILOT-DEPENDENT.** From pilot run-block variability of the cost outcomes, at the same α and power. |
| Pilot requirement | The E0/E2 pilot on validation data estimates the effect and variability inputs. Frozen at FP-1. |

**Minimum cell size for E1.** Every configuration × state cell processes the full test split, so the cell size equals the test-split size.

**If the dataset cannot supply the required n_defective,** no powered claim is made. The minimum detectable effect at α = 0.05 and power 0.80 for the available n is reported instead.

### D-04 — Resource-cost metric for C1–C4 ordering · RESOLVED

**Primary metric:** median steady-state per-item inference latency at R0, on the device, after the warm-up policy, on validation items.

**Justification:**
- It is measured directly in-app with high time resolution.
- It does not depend on an external energy reference, which may be infeasible on this sealed device (V-11).
- It is the quantity the inference-latency admissibility reference (D-12 A) constrains.

**Secondary metrics and their roles:**

| Metric | Role |
| :-- | :-- |
| Peak resident memory | Admissibility gate (D-13): must fit; not an ordering metric |
| Energy per item | Confirmation: if validated (D-16A) and the ladder mixes backends, latency order and energy order must agree. If they disagree, the disagreement is reported and the candidate pair is flagged; the order is not silently changed. |
| Thermal rise | Temperature slope over a fixed sustained run; reported per rung |
| CPU/GPU utilisation | Reported where available |

**No composite score.** There is no principled basis for weights before data exist.

**Tie-breaking.** Two candidates are tied if the item × run cluster-bootstrap CI of their latency difference includes zero. Among tied candidates, keep the one with lower peak memory; if still tied, keep the one with higher validation recall.

**Minimum rung count** (Step 10C D-05):
- If fewer than four admissible, strictly ordered candidates exist, use the available k = 3 or k = 2 rungs, with R → C mapping per Step 10C.
- If fewer than two exist, adaptation is untestable on this device. Stop and report.

**Freeze.** Order and identities are written to a ladder report with hashes at FP-2. **C1–C4 identities: TO BE EMPIRICALLY DETERMINED.**

### D-05 — Minimum inspection requirement · RESOLVED (requirement-based floor DEFERRED)

A candidate is admissible only if, on the **validation** split at its argmax decision:
1. the lower CI bound of AUROC exceeds the no-skill value;
2. the lower CI bound of precision exceeds the validation defect prevalence (the precision of a no-skill classifier);
3. the lower CI bound of recall exceeds the classifier's own positive-prediction rate on normal items (no-skill recall at the same positive rate).

These floors are **data-derived**, so no number is invented. They block a model that is efficient but uninformative.

The **requirement-based floor is DEFERRED** until a documented inspection requirement (D-01) exists. Until then, lighter rungs may be weak; this is a finding about degradation (H1), and practicality claims are bounded accordingly.

### D-06 — Confidence threshold rule · PRE-DATA-COLLECTION FREEZE (procedure frozen; risk target requires approval)

**Revision.** The earlier rule (the smallest threshold whose accepted predictions are statistically as accurate as C1) is **withdrawn**. Thresholds are no longer tied to equivalence with C1.

**FROZEN NOW: risk-controlled selective-acceptance procedure.**
1. **Confidence.** Configuration-specific temperature scaling is preserved. Each configuration Cᵢ is calibrated on its own on-device outputs over Calibration-T.
2. **Acceptance-risk target.** One pre-specified acceptance-risk target r* (the maximum tolerated misclassification rate among accepted predictions) applies to every configuration.
   - **The numerical value of r* is UNSET (REQUIRES FUTURE APPROVAL).** It must be approved before FP-0 closes, and before any calibration output is inspected.
3. **Candidate thresholds.** The sorted distinct calibrated confidences of Cᵢ on Calibration-τ. These are data-defined; no grid is invented.
4. **Selection.** τᵢ is the smallest candidate threshold for which the one-sided upper Clopper–Pearson bound (α = 0.05, D-02) on the misclassification rate of accepted Calibration-τ items is ≤ r*.
   - The selection depends only on r*, the calibrated outputs and the frozen α.
   - Ties resolve to the higher threshold.
5. **Coverage.** The coverage at τᵢ (the share of items accepted without verification) is reported per configuration. If no candidate meets r*, τᵢ is set to its maximum, so every item is verified, subject to the D-07 action limit. This is reported as **infeasible at r***.
6. **B5-F.** The same procedure and the same r*, applied to the union of all configurations' Calibration-τ outputs with equal weight per configuration, gives one global threshold.
7. **B4 configuration.** The B2 configuration, as before.

**Test isolation.**
- **The final test set is never used for threshold selection.**
- The test manifest is never loaded by fitting code.
- τ values are frozen with their hashes at FP-3.

**No numerical confidence threshold is stated in this register.**

### D-07 — Verification action order · PILOT-DEPENDENT

**Eligibility.**

| Action | Stage 1 (Real-IAD) | Stage 2 (custom capture) | Resource condition |
| :-- | :-- | :-- | :-- |
| A0 accept | Yes | Yes | Always |
| A1 same-view recapture | **No: Real-IAD has no physical recapture** | Yes | Permitted in the current resource state per the frozen permission table (E1 admissibility: memory, thermal) |
| A2 additional view | Yes, as simulation (next stored view in the pre-registered order) | Yes, actual capture | As A1 |
| A3 stronger model | Yes | Yes | Only if the next higher rung is admissible in the current state (memory, D-13; inference latency, D-12) |
| A4 human review | Yes | Yes | Always (last resort) |

**Order.**
1. Automated actions come before A4.
2. Among eligible automated actions, the order is by **E1-measured mean added verification latency in the current state**, cheapest first. This is frozen at FP-2 as a per-state priority table.

**Stopping rule.**
- After each action, the calibrated confidence of the updated decision is compared with the threshold of the configuration that produced it. For A2 this is the fused score (D-08) against the current configuration's τ; for A3 it is the escalated configuration's τ.
- Stop at the first action that reaches the threshold.

**Maximum actions.**
- Each eligible automated action type is used **at most once per item**. The maximum is therefore the number of eligible automated types: up to two in Stage 1, up to three in Stage 2.
- Verification is **not** required to fit inside the C1 inference latency. Its latency is measured and reported separately (D-12).

**If confidence remains low,** the item is referred (A4). For automated metrics at full coverage, its last automated prediction is scored. For system metrics, the referral is reported separately, with coverage.

**Primary action for H2.** The complete B5 policy is the confirmatory mechanism. Per-action effects are secondary.

### D-08 — Additional-view combination · RESOLVED (conditional on V-05)

**Primary: any-view late fusion.** The fused defect probability is the maximum of the calibrated defect probabilities over the views considered (initial plus additional). The decision is defective if the fused probability ≥ 0.5; this is the argmax of the fused binary probability, not a tuned value.

**Justification:**
- An item is defective if any view shows a defect; defects are view-dependent. Averaging dilutes a defect visible in one view.
- Majority voting is undefined for two views.
- Strongest-view selection ignores the defect-specific semantics.

**Precision.** Any-view fusion can raise false positives. This is monitored by the D-15 precision safeguard, not tuned away.

**Sensitivity analysis.** Mean of calibrated probabilities, pre-registered.

**Condition.** Valid if Real-IAD item labels are defined as "any view anomalous" (V-05 / G2). If V-05 shows otherwise, this decision returns to PRE-DATA-COLLECTION FREEZE before FP-0 closes.

**Test isolation.** No fusion rule is chosen on test data.

### D-09 — Data split proportions · PILOT-DEPENDENT

**Procedure (RESOLVED):**
1. Split by **physical item** (Real-IAD sample), stratified by object category × defect status, with a recorded seed.
2. All views of an item stay in one split. In Stage 2 this also covers all recaptures.
3. Do not reuse the official Real-IAD split: it is an unsupervised-AD split with normal-only training, so it does not support this supervised protocol.

**Allocation order:**
1. Test: n_test from D-03.
2. Calibration-τ: large enough that the D-06 bound can certify a non-trivial accepted set for the lightest rung. Estimated on validation outputs in the pilot.
3. Calibration-T: the same item count as Calibration-τ.
4. Validation: what remains for ladder steps 6–7 and the pilots.
5. Train: the remainder.

If the items are insufficient, the shortfall is reported, and the test size is never reduced below the D-03 requirement without stating the reduced minimum detectable effect.

**Leakage checks (automated before FP-4):**
- no item ID in two splits;
- every view of an item in the same split;
- manifests committed with hashes.

### D-10 — Resource-state classification rule · DEVICE-VERIFICATION DEPENDENT (aggregation rule frozen; thresholds pilot-dependent)

**FROZEN NOW.**
- **Dimension levels.**
  - Each dimension d ∈ {thermal, battery, memory, compute} has an ordinal level L_d ∈ {0, 1, 2, 3}.
  - Latency, accuracy and confidence are excluded from every dimension.
- **Aggregation.** R = max_d L_d, with no weighting.
- **Missing telemetry.**
  - A dimension found **UNAVAILABLE** in E0 is removed from the estimator for the whole study. This is fixed at FP-1 and reported.
  - A transient gap holds the last valid level for at most one dwell period, then keeps holding it and flags `telemetry_gap`.
  - Flagged runs are included in the primary analysis and excluded in a sensitivity analysis.
- **Hysteresis, dwell, transitions and cooldown.** As in Step 10C `resource_states.md` §5. Escalation may skip levels; de-escalation is one level at a time.

**DEVICE-VERIFICATION DEPENDENT (Step 10D): the thermal dimension.**
- **Platform thermal-status API availability is NOT assumed.**
  - The OPPO A5 2020 launched on Android 9 (API 28). The thermal-status API needs API 29 or later.
  - The installed Android version and API level, and the thermal interfaces the device actually exposes, are verified in Step 10D.
- **If the API is available,** the thermal levels the device actually reports are recorded. Mapping them to L_thermal is **REQUIRES FUTURE APPROVAL**, based on that observation.
- **If the API is unavailable,** the documented fallback is used:
  - L_thermal is derived from the available temperature signals (battery temperature; readable thermal zones) and frequency-capping / throttling evidence (CPU frequency below its unthrottled level under a fixed load);
  - thresholds come from E0 change points (PILOT-DEPENDENT);
  - the thermal state is then labelled as inferred, not platform-reported.
- **No thermal mapping is inserted in this register.**

**PILOT-DEPENDENT.** All continuous thresholds come from E0 and are frozen at FP-1.

### D-11 — Controlled pressure mechanism · PILOT-DEPENDENT

**Resource state vs pressure mechanism.**
- The resource state is what the estimator classifies from telemetry.
- The pressure mechanism is how the experimenter induces conditions.
- Mechanisms are not combined in the primary design.

**Assessment.**

| Mechanism | Reproducibility | Safety | Isolation | Interference with pipeline | Role |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Scripted background compute load (fixed thread count and duty cycle, separate process, sustained) | High: fully parameterised | Bounded by abort rules | Compute, plus thermal through sustained heating (realistic contention) | Does not touch the inspection code path; competes for CPU | **Provisional primary** |
| Thermal pre-soak (workload until a target thermal level, then stop) | Medium: decays during the run | Abort rules | Thermal, without concurrent contention | None during the run | Secondary sensitivity |
| Power-save mode toggle | High (binary) | Safe | Battery and governor policy (system-wide) | Changes system scheduling | Secondary sensitivity |
| Memory pressure (separate process holding memory) | Questionable: ColorOS low-memory killer | Risk of killing the app or logger | Memory | May terminate measurement | Pilot-only, unless the pilot shows stability |
| Battery level (discharge to window) | Slow | Safe | Battery | None | Start-window control (Step 10C §7), not a manipulation |

**Pilot (E0):**
1. Run each mechanism at an intensity grid derived from device parameters, e.g. thread counts up to the eight available cores.
2. Repeat runs per intensity.
3. Primary confirmation criteria:
   - telemetry trajectories reproducible across repeats (item-free manipulation check);
   - target R-levels reached and held;
   - no process kills.
4. If the compute load fails these criteria, the next mechanism in the table that passes becomes primary. This is recorded at FP-1.

**Safety abort rules (no invented limits).** Abort a run immediately if any of the following occurs:
- platform thermal status reaches CRITICAL or higher (where available);
- the OS shows an overheating warning;
- the battery temperature leaves the manufacturer-stated operating range (the range itself REQUIRES VERIFICATION).

**No external heat sources are used.**

### D-12 — Inference, verification and decision time · PILOT-DEPENDENT (latency separation frozen)

**FROZEN NOW: three separate quantities**, each logged per item and reported separately:

| Quantity | Definition | Log field |
| :-- | :-- | :-- |
| A. Inference latency | Preprocessing plus initial inference of the configuration chosen for the item, plus model-switch time if a switch preceded the item (switch time also reported separately) | `inference_latency`, `model_load_time` |
| B. Verification latency | Added time of all verification actions taken for the item (A1/A2 acquisition and inference, fusion, A3 escalation inference) | `verification_latency` |
| C. Total per-item decision time | A + B, from item start to the final automated decision; human review (A4) is excluded from device time and reported as referral rate | derived |

- **Verification is never forced to fit inside the C1 inference latency.** Verification overhead (B, and its share of C) is reported separately for H3 and H5.

**PILOT-DEPENDENT: the inference-latency admissibility reference.**
- The reference is the median inference latency (A) of C1 at R0 on the device, on validation items, after warm-up. It is frozen at FP-2.
- It is used only to decide which configurations are admissible in each resource state (Step 10C §8), and applies to A only.

**REQUIRES FUTURE APPROVAL: a total decision-time budget (C), only if one is needed.** The primary design imposes none.
- **Freeze procedure, if adopted:**
  1. The E1/E2 pilot on validation data records the distribution of C for B5 at each pressure level.
  2. The researcher approves a budget, stated as a statistic of that pilot distribution or as a documented production cycle-time requirement.
  3. The budget is frozen at FP-2, before any test-split run.
- If adopted, actions whose E1-measured cost would exceed the remaining budget are skipped and logged.

### D-13 — Model memory residency · PILOT-DEPENDENT

**Procedure:**
1. In E0, measure each configuration's resident memory after load and its peak during inference, with the camera pipeline (Stage 2), the logger and the pressure process active.
2. Choose the largest resident set that shows no low-memory flag and no process kill during sustained pilot runs at each pressure level. Preference order:
   1. all four configurations;
   2. otherwise, current plus the escalation target;
   3. otherwise, current only.

**Equality.**
- The same residency policy applies to B3, B4, B5 and B5-F.
- B1 and B2 hold their single configuration; their memory footprint is reported.

**Loading cost.**
- Load and swap times are measured separately (`model_load_time`).
- They are included in per-item time when a switch occurs.

**Freeze.** Frozen at FP-1 and verified again in the E1 pilot.

### D-14 — Repeated runs and McNemar · RESOLVED (methodological refinement of Step 10A)

**Problem.**
- Each item appears in every run. McNemar on pooled runs violates independence, and McNemar on one run discards data.
- Stage 1 replay is deterministic for a fixed (item, configuration), so run-to-run differences arise only from the configuration trajectory.

**Primary analysis (H1, H2, H2.b, accuracy part of H5).**
1. For each item i and policy b, compute p_i(b): the proportion of runs in which the final automated decision is correct. Recall uses defective items.
2. Per-item paired differences d_i = p_i(B5) − p_i(B3), and analogously for the other comparisons.
3. p-value: an **item-level paired sign-flip permutation test** on d_i. It is valid under exchangeability of paired item differences, and it feeds Holm.
4. CI: an **item-cluster bootstrap**, resampling items together with all their runs.
5. Sensitivity: a logistic mixed model with item and run random intercepts and policy as a fixed effect.

**McNemar is retained exactly where valid:**
- (a) comparisons in which each item contributes one paired binary observation, e.g. E1 forced configurations Cᵢ vs Cⱼ on identical inputs, after confirming that outputs are deterministic across runs;
- (b) a pre-designated single-run sensitivity analysis (the first run of each counterbalanced block).

**Cost outcomes (H3, cost part of H5).** The unit is the counterbalanced run block. Paired Wilcoxon signed-rank tests on block-level differences are used; this is one of the two Step 10A options, now fixed.

**Recorded as:** "Step 10A method refined because of repeated/clustered design." The Step 10A hypotheses text is not edited.

### D-15 — Recovery and precision · RESOLVED (margin via D-01)

- **Preserved.** Recovery = (B5 − B3) / (B1 − B3) on item-level defect recall (primary), with the Step 10C denominator rule.
- **Precision safeguard (pre-specified).**
  - H2 is declared supported only if recall recovery holds **and** B5's precision is non-inferior to B3's: the lower bound of the item-cluster bootstrap CI of precision(B5) − precision(B3) must exceed −SESOI_precision (D-01).
  - If recall recovers but precision fails this test, the outcome is classified as a **trade-off**, not recovery.
- **Secondary measures (always reported):**
  - F1-based recovery;
  - false-reject rate;
  - false-accept rate;
  - referral rate and coverage.
- **Recorded as** a methodological refinement. The approved metric is unchanged; the guard adds a condition and replaces nothing.

### D-16 — Energy validation, network, additional devices · PRE-DATA-COLLECTION FREEZE (method, fallback, network and scope frozen; agreement threshold requires decision)

**A. Energy.**

**FROZEN NOW: method.**
- Simultaneous software-counter and reference measurements over matched intervals of scripted workloads.
- Bland–Altman bias and limits of agreement (bias ± 1.96 SD of differences), plus a regression of difference on mean to check for proportional bias.
- Software battery counters are never treated as ground truth.

**PRE-DATA-COLLECTION DECISION REQUIRED: the agreement threshold.**
- The tolerance within which the limits of agreement must lie is **not set**. No numeric tolerance is invented.
- A candidate basis is the energy SESOI (D-01). Adopting it, or any other tolerance, requires a decision before data collection.

**FROZEN NOW: reference preference and fallback hierarchy.** The level actually achieved is DEVICE-VERIFICATION DEPENDENT (Step 10D) and recorded at FP-1.

| Level | Setup | What may be reported |
| :-- | :-- | :-- |
| E-1 (preferred) | Validated **battery-side external reference**: a power analyzer replacing the battery through a bypass | Absolute energy and power per item, per verified item, per inference; software counters validated against it |
| E-2 | Battery bypass not achievable on the OPPO A5 2020, but an external meter can measure a **supply-powered session** in which charging is excluded (verified non-charging state) | Absolute energy only for that setup, labelled as supply-powered. Battery-powered runs use software counters as **relative** comparisons, calibrated against E-2 sessions where agreement meets the approved threshold. |
| E-3 (fallback) | No defensible external reference | **No absolute energy is reported.** Software-counter energy is reported only as **relative, within-device differences between conditions** under identical schedules, labelled "software-estimated, not externally validated". The energy parts of H3 and H5 become secondary and descriptive; H5 uses latency as its cost axis. |

**Absolute energy is never forced** when the setup cannot support a defensible absolute value.

**B. Network policy (FROZEN NOW).**
- All confirmatory runs are **fully offline**: airplane mode, with Wi-Fi, Bluetooth and mobile data off. Inference is on-device only.
- **USB is disconnected during battery-powered runs.**
- Host-side telemetry comes from an on-device trace started before disconnection, where supported. This is DEVICE-VERIFICATION DEPENDENT; otherwise those signals are UNAVAILABLE for those runs.
- Logs are pulled after the run.

**C. Devices (FROZEN NOW).**
- The OPPO A5 2020 (3 GB) is the **only current experimental device**.
- Multi-device validation is future work and not part of the current scope.
- Claims stay within the class B limit of [`generalization_framework.md`](generalization_framework.md).

## 5. Statistical Plan Reconciliation

| RQ / Hypothesis | Original test (Step 10A) | Issue identified | Resolution | Final analysis method | Reason | Pre-data requirement |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| RQ2 / H1 | Paired McNemar; paired bootstrap CI of M(B1) − M(B3) | Repeated runs per item | **Step 10A method refined because of repeated/clustered design** | Item-aggregated correctness; paired sign-flip permutation test; item-cluster bootstrap CI; McNemar only for single-run sensitivity | Runs are not independent | D-01, D-02, D-03 frozen |
| RQ3 / H2 | Paired McNemar; bootstrap CI of ρ | Repeated runs; recall-only gaming | **Step 10A method refined because of repeated/clustered design**, plus the precision safeguard | As H1, plus the ρ bootstrap and the precision non-inferiority condition; ρ undefined if the denominator CI does not lie above the SESOI | Validity; pathological recall gains | D-01, D-02, D-03, D-15 |
| RQ3 / H2.b | Paired McNemar at matched rate | Repeated runs | **Step 10A method refined because of repeated/clustered design** | As H2 at matched verification rate or cost; secondary | Same | D-06 frozen |
| RQ5 / H3 | Mixed-effects model **or** paired Wilcoxon across runs | The choice was open | **Step 10A method retained** (the Wilcoxon option fixed) | Paired Wilcoxon on run-block differences; bootstrap CIs; mixed model as sensitivity | Few runs; non-parametric | D-01 (cost SESOI), run count |
| RQ4 / H4 | Bootstrap CIs of ECE/Brier differences; KS with Holm | Small-cell concern | **Step 10A method retained** | Unchanged; every E1 cell holds the full test split; outputs checked for run determinism (if not deterministic, cluster by item) | Cell size resolved by design | Binning scheme (FP-0), D-02 |
| RQ6 / H5 | Pareto dominance with bootstrap; matched-budget comparison | Accuracy clustered by item; cost by run | **Step 10A method refined because of repeated/clustered design** | Joint bootstrap resampling items (accuracy) and run blocks (cost) | Respects both clustering levels | D-01, D-03 |
| RQ1 | Decision rule over H1, H2, H5 | — | **Step 10A method retained** | Unchanged; H2 support includes D-15 | — | All above |
| Multiplicity | Holm over H1–H5 | — | **Step 10A method retained** | Holm over H1–H5; H2.b and per-action analyses secondary | — | D-02 |

**Statistical parameters applied throughout** (Step 10C-DR final freeze):
- α = 0.05;
- two-sided tests;
- Holm correction over H1–H5;
- target power 0.80;
- sample size PILOT-DEPENDENT (D-03);
- repeated observations clustered at item level (D-14);
- cost outcomes clustered by run block.

**Binning scheme for ECE (FP-0).** Equal-mass bins, with the bin count set as a function of calibration-split size by a stated rule. The rule itself is REQUIRES FUTURE APPROVAL before FP-0 closes.

## 6. Remaining Blockers Before Step 10D

1. **Future approvals:**
   - D-06 acceptance-risk target r*;
   - D-16 energy agreement threshold;
   - ECE binning rule;
   - D-12 total decision-time budget (only if needed).
2. **G2 / V-01, V-03, V-05:** Real-IAD access, data licence, and per-view label semantics. D-08 depends on V-05.
3. **Device verification in Step 10D (V-07 to V-10, V-13):**
   - installed Android version and API level;
   - thermal-status API or fallback (D-10);
   - telemetry access and on-device trace;
   - runtime backends.
4. **Energy reference (V-11):** battery-bypass feasibility, which decides between levels E-1, E-2 and E-3.
5. **G3:** Stage 2 custom-capture protocol approval.
6. **G4:** empirical ladder selection, which needs the E0/E1 pilot.

The pilot-dependent decisions (D-01, the D-03 counts, D-07, the D-09 sizes, the D-10 thresholds, D-11, the D-12 inference reference, D-13, the D-15 margin, and the D-16 measured agreement) close at FP-1 and FP-2.

## 7. Status

Methodology only. **No experiments, measurements, model benchmarking, dataset collection, or empirical results were produced.**
