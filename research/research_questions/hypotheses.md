# Hypotheses — GC-03

_Step 10A, 2026-10-05, Claude Code._

Every hypothesis below is a **Hypothesis** in the sense of `RESEARCH_RULES.md`: a testable proposition that has not been tested. No experiment has been run, no measurement exists and no result is reported. No numerical threshold, significance level or effect size is fixed in this document; each is marked `to_be_preregistered` and must be fixed, with a written justification, in `configs/` before data collection (see [`configs/research_protocol.yaml`](../../configs/research_protocol.yaml)).

Baselines (B1–B5, B5-F), experiments (E1–E3), resource states (R0–R3), configurations (C1–C4) and actions (A0–A4) are defined in [`experimental_framework.md`](experimental_framework.md). Variables are defined in [`variables_and_factors.md`](variables_and_factors.md).

## 1. Shared Definitions and Analysis Rules

- **Primary accuracy metric (M).** Defect recall on the test items. Secondary: precision, F1, and mAP where the task is detection. Metrics are reported both for the automated decision and with human-review referrals (A4) counted separately, never silently as correct.
- **Coverage.** The proportion of items decided without A4. Any accuracy comparison involving A4 is reported at matched coverage or as a risk–coverage curve, so that recovery cannot be produced by referring everything to a human.
- **Degradation.** Δ_deg = M(B1) − M(B3), on the same items under the same resource-pressure schedule.
- **Recovery proportion.** Recovery = (B5 − B3) / (B1 − B3), i.e. ρ = [M(B5) − M(B3)] / [M(B1) − M(B3)].
  - **Edge case (denominator).** If the B1 − B3 denominator is zero or practically negligible, the recovery ratio is undefined or uninformative and **must not be interpreted as evidence of recovery**. A tiny denominator inflates ρ arbitrarily and makes its sign unstable.
  - "Practically negligible" means the confidence interval for Δ_deg = M(B1) − M(B3) does not lie entirely above the pre-registered SESOI. The SESOI is `to_be_preregistered`; no numerical threshold is set here.
  - In that case, ρ is not reported as a recovery estimate. H2 is reported as **not testable** (neither supported nor refuted), and only the absolute difference M(B5) − M(B3), with its CI, is reported descriptively.
  - ρ is computed only when the confidence interval for Δ_deg lies above zero and beyond the SESOI (H1 statistically and practically supported).
- **Pairing.** All baselines run on the same item sequence and the same scripted resource-pressure schedule, so item-level comparisons are paired.
- **Repeated runs.** Each condition is repeated; the number of runs is `to_be_preregistered`. Run is a random effect in device-level cost models.
- **Multiplicity.** Holm correction across the confirmatory tests H1–H5.
- **Statistical vs practical significance.** A difference is *statistically significant* if the pre-registered test rejects the null at the pre-registered level after correction. It is *practically significant* only if its confidence interval also lies beyond the pre-registered smallest effect size of interest (SESOI). A result can be statistically but not practically significant; both are reported. Claims of "no meaningful difference" require an equivalence test (TOST) against the SESOI, not a non-significant result.

## 2. H1 — Degradation from resource-driven downgrading

**Statement.** Resource-driven runtime downgrading decreases inspection performance relative to the best static configuration under equivalent task conditions.

| Element | Specification |
| :-- | :-- |
| Null hypothesis (H1₀) | M(B3) ≥ M(B1) under the same items and resource-pressure schedule. |
| Alternative (H1₁) | M(B3) < M(B1). |
| Independent variable(s) | Policy condition (B1 vs B3); resource-pressure schedule (R-state sequence); in E1, forced configuration C1–C4. |
| Dependent variable(s) | Recall (primary); precision, F1, mAP; per-configuration share of items processed. Context: latency, energy, temperature, memory (needed to show the downgrade buys a resource saving, F1). |
| Expected direction | M(B3) < M(B1); resource cost of B3 < B1. |
| Falsification condition | No degradation: the CI for Δ_deg includes zero or lies within ±SESOI (equivalence), or the policy never leaves C1 under the schedule. |
| Statistical comparison | Paired item-level McNemar test on correct/incorrect decisions; paired bootstrap CI for Δ_deg in recall, F1 and mAP. E1 supplies the per-configuration accuracy that bounds Δ_deg. |
| Practical significance | Lower bound of the Δ_deg CI exceeds the accuracy SESOI (`to_be_preregistered`, justified from inspection requirements). |

**Note.** H1 is expected on prior grounds: lighter configurations are usually less accurate. Its role is to establish that the loss RQ3 tries to recover exists and has a measurable size under realistic schedules. If H1 is not supported, H2 cannot be tested.

## 3. H2 — Recovery by confidence-aware verification

**Statement.** Confidence-aware downstream verification recovers a measurable portion of the performance degradation introduced by resource-driven downgrading.

| Element | Specification |
| :-- | :-- |
| Null hypothesis (H2₀) | M(B5) ≤ M(B3), i.e. ρ ≤ 0. |
| Alternative (H2₁) | M(B5) > M(B3), i.e. ρ > 0. |
| Independent variable(s) | Verification enabled vs disabled (B5 vs B3); verification action (A1–A4); resource state; confidence threshold (per configuration). |
| Dependent variable(s) | Recall (primary), precision, F1, mAP; ρ; coverage; recapture, additional-view, escalation and referral rates. |
| Expected direction | M(B5) > M(B3); 0 < ρ ≤ 1 expected, ρ > 1 possible and reported if observed. |
| Falsification condition | CI for M(B5) − M(B3) includes zero or lies within ±SESOI; or recovery appears only at matched coverage below the pre-registered minimum coverage. |
| Statistical comparison | Paired McNemar test (B5 vs B3); paired bootstrap CI for ρ; stratified by resource state and by action. |
| Practical significance | Lower bound of the recovery CI exceeds the accuracy SESOI at the pre-registered minimum coverage. |

**Secondary comparison H2.b (distinction from a fixed threshold).** H2.b₀: M(B5) ≤ M(B5-F) at matched verification rate or matched cost. H2.b₁: M(B5) > M(B5-F). This tests whether configuration- and state-aware verification adds anything beyond a single fixed global confidence threshold (E3). It is secondary: if it fails, H2 can still hold, but the mechanism reduces to fixed-threshold gating and the contribution narrows accordingly.

## 4. H3 — Overhead of verification

**Statement.** Confidence-aware verification introduces measurable latency, energy, memory, or thermal overhead.

| Element | Specification |
| :-- | :-- |
| Null hypothesis (H3₀) | For each cost metric, cost(B5) − cost(B3) and cost(B4) − cost(fixed configuration without verification) are zero within measurement resolution. |
| Alternative (H3₁) | At least one cost metric is higher with verification. |
| Independent variable(s) | Verification enabled vs disabled; verification action; trigger rate (via threshold); resource state. |
| Dependent variable(s) | Latency per item and per verified item (mean and tail percentiles); energy per item; temperature trajectory; peak and resident memory; verification-action counts; human-review load. |
| Expected direction | Higher cost with verification, scaling with trigger rate and action type (A3 and A1/A2 costlier than A0). |
| Falsification condition | No cost metric differs beyond measurement resolution (established by idle and repeated-run calibration of the instruments). |
| Statistical comparison | Mixed-effects model (condition as fixed effect, run as random effect) or paired Wilcoxon signed-rank across runs; bootstrap CIs on per-item cost differences. |
| Practical significance | Overhead compared against the resource saving of adaptation (B1 − B3 cost). Overhead is practically decisive if it removes the saving (falsification F4). |

**Note.** H3 is a characterisation hypothesis: some overhead is expected. Its value lies in the magnitude, the per-verified-item unit and the comparison with the adaptation saving.

## 5. H4 — Calibration differs across configurations and resource conditions

**Statement.** Confidence distributions and calibration characteristics differ between inference configurations operating under different resource conditions.

| Element | Specification |
| :-- | :-- |
| Null hypothesis (H4₀) | Calibration error and confidence distributions are the same across configurations C1–C4, and, for a fixed configuration, the same across resource states R0–R3. |
| Alternative (H4₁) | They differ across configurations (H4.a) and/or across resource states at a fixed configuration (H4.b). |
| Independent variable(s) | Configuration (forced in E1); resource state (induced in E1). |
| Dependent variable(s) | Expected calibration error, Brier score, reliability diagrams, confidence histograms for correct and incorrect predictions, AUROC of confidence for error detection. |
| Expected direction | H4.a: differences expected (lighter configurations differently calibrated). H4.b: no direct effect expected for deterministic execution on identical input; a difference would indicate backend fallback, precision change or acquisition effects, and is logged as such. |
| Falsification condition | H4.a: CIs of per-configuration calibration error overlap within ±SESOI and confidence distributions are equivalent. H4.b is reported separately and its null is the expected outcome. |
| Statistical comparison | Bootstrap CIs on ECE and Brier differences; two-sample tests (e.g. Kolmogorov–Smirnov) on confidence distributions with Holm correction; binning scheme pre-registered. |
| Practical significance | A calibration difference is practically significant if applying one configuration's threshold to another changes the trigger rate or the recovery (H2) beyond SESOI. |

## 6. H5 — Joint trade-off

**Statement.** A joint resource-adaptation + confidence-verification policy provides a more favorable accuracy–efficiency trade-off than either mechanism alone.

| Element | Specification |
| :-- | :-- |
| Null hypothesis (H5₀) | B5 is not more favourable than B3 or B4: it is Pareto-dominated by, or equivalent to, at least one of them on (accuracy, cost), and at matched cost its accuracy is not higher. |
| Alternative (H5₁) | B5 is not dominated by B3 or B4 and, at matched cost (energy per item or latency per item), achieves higher accuracy than each; B1 and B2 are reported as reference points. |
| Independent variable(s) | Baseline B1–B5; resource-pressure schedule. |
| Dependent variable(s) | Accuracy (recall, F1, mAP), coverage, energy per item, latency per item, temperature trajectory, memory, sustained operation time under the schedule. |
| Expected direction | B5 lies on or beyond the B3/B4 Pareto front; B5 is cheaper than B1 at an accuracy closer to B1 than B3 is. |
| Falsification condition | B5 is dominated by or equivalent to B3 or B4 (F6); or B5 needs at least the cost of B1 for its accuracy (F3); or the verification overhead removes the adaptation saving (F4). |
| Statistical comparison | Bootstrap CIs of paired accuracy and cost differences; Pareto-dominance assessed with bootstrap uncertainty; matched-budget accuracy comparison. |
| Practical significance | Improvement beyond SESOI in accuracy at matched cost, or in cost at matched accuracy. |

## 7. Decision Rule for RQ1

- **Yes, conditionally:** H1 supported, H2 supported (statistically and practically) and H5 not refuted.
- **No:** H1 supported and H2 not supported, or H2 supported only at a cost equal to or above B1 (Step 9.9C falsification condition).
- **Not testable:** H1 not supported (no loss to recover). Reported as a finding about the adaptation policy, not as support for RQ1.

## 8. Status

| ID | Status |
| :-- | :-- |
| H1 | STATUS: TO BE TESTED |
| H2 | STATUS: TO BE TESTED |
| H3 | STATUS: TO BE TESTED |
| H4 | STATUS: TO BE TESTED |
| H5 | STATUS: TO BE TESTED |

None of the hypotheses is proven, supported or refuted. No data exist.
