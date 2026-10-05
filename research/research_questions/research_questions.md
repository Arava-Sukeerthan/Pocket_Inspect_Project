# Research Questions — GC-03

_Step 10A, 2026-10-05, Claude Code. Research specification only; no question has been answered._

Approved gap: [`research_gap.md`](../gap_analysis/research_gap.md). Objectives: [`objectives.md`](objectives.md). Hypotheses: [`hypotheses.md`](hypotheses.md). Variables: [`variables_and_factors.md`](variables_and_factors.md). Resource states, configuration ladder, verification actions, baselines, falsification and contribution boundary: [`experimental_framework.md`](experimental_framework.md). Traceability: [`traceability_matrix.csv`](traceability_matrix.csv).

Baseline labels used below: B1 static best model, B2 static lightweight model, B3 resource adaptation only, B4 confidence verification only, B5 resource adaptation + confidence verification, B5-F (ablation of B5 with one fixed global confidence threshold). Experiment families: E1 forced-configuration sweep, E2 policy-driven baseline episodes, E3 verification-policy ablation.

## 1. Primary Research Question

> **RQ1.** Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained smartphone dynamically downgrades its inference configuration under changing device conditions?

RQ1 is not answered by a single comparison. It is answered by the conjunction of RQ2 (a loss exists), RQ3 (part of it is recovered), RQ5 (at what cost) and RQ6 (whether the result is worth having), with RQ4 explaining why recovery succeeds or fails. RQ1 is answered **yes** only if H1 and H2 are both supported and H5 is not refuted; see [`hypotheses.md`](hypotheses.md) §7.

## 2. Secondary Research Questions

| ID | Question | Hypothesis | Experiment |
| :-- | :-- | :-- | :-- |
| RQ2 | How does resource-driven runtime adaptation change defect-detection performance and resource consumption on a resource-constrained smartphone, relative to the static configurations it switches between? | H1 | E1, E2 |
| RQ3 | What proportion of the inspection-performance loss caused by resource-driven configuration downgrading does confidence-aware verification recover, and how does that proportion vary with resource state and verification action? | H2 | E2, E3 |
| RQ4 | How do confidence distributions and calibration differ across inference configurations, and do they differ across resource states when the configuration is held fixed? | H4 | E1 |
| RQ5 | What latency, energy, thermal, memory and verification-action overhead does confidence-aware verification add, per inspected item and per verified item? | H3 | E1, E2 |
| RQ6 | Does combining resource adaptation with confidence verification give a more favourable accuracy–efficiency trade-off than either mechanism alone, and how does it compare with the static best and static lightweight configurations? | H5 | E2 |

## 3. Review of the Candidate Questions

Each candidate from the task was checked against five properties: measurable, falsifiable, non-overlapping, connected to GC-03 and experimentally actionable. Four were revised.

| Candidate | Problem found | Revision |
| :-- | :-- | :-- |
| RQ2 "How does resource-driven runtime adaptation affect defect-detection performance…?" | Measured only accuracy. Falsification criterion F1 (adaptation gives no resource benefit) then had no question behind it, and a loss in accuracy with no resource saving would not motivate recovery. | Added resource consumption and an explicit reference (the static configurations the policy switches between). |
| RQ3 "How much inspection-performance degradation can confidence-aware verification recover…?" | Overlapped with RQ1: both asked whether recovery happens. | Restated as a proportion with a defined denominator (the B1–B3 loss) and with variation by resource state and action, which RQ1 does not ask. RQ1 is kept as the umbrella question. |
| RQ4 "How does confidence calibration change across inference configurations and resource conditions?" | Ambiguous mechanism. For a deterministic model on fixed input, resource state cannot change outputs directly; it acts through the configuration chosen, through execution-backend changes (e.g. delegate fallback, precision) or through acquisition (frame timing, camera behaviour under power saving). Without separating these, the question cannot be falsified cleanly. | Split into a between-configuration comparison and a within-configuration, across-state comparison. |
| RQ5 "What latency, energy, thermal, memory, and verification overhead is introduced…?" | Measurable, but the unit was undefined: overhead per item and per verified item lead to different conclusions when the trigger rate changes. | Units stated. |
| RQ6 "Does the combined … strategy provide a better accuracy–efficiency trade-off than either mechanism alone?" | "Better" undefined; and falsification criterion F3 (recovery no better than the static best model) was not covered. | Comparison references made explicit (B3, B4, and B1/B2); "more favourable" is operationalised in H5 as Pareto dominance or a better metric at a matched budget. |

### Properties after revision

| ID | Measurable | Falsifiable | Non-overlapping | Linked to GC-03 | Actionable |
| :-- | :-- | :-- | :-- | :-- | :-- |
| RQ1 | Via RQ2–RQ6 | Yes (H1 ∧ H2 ∧ ¬refuted H5) | Umbrella; decomposed | Is the approved primary question | Via E1–E3 |
| RQ2 | Recall, precision, F1, mAP; latency, energy, temperature, memory | Yes (H1, F1) | Adaptation effect only; no verification | Device-state-driven adaptation | E1, E2 |
| RQ3 | Recovery proportion with CI | Yes (H2, F2) | Verification effect conditional on downgrading | Coupling of the two mechanisms | E2, E3 |
| RQ4 | ECE, Brier, reliability diagrams, confidence distributions | Yes (H4, F5) | Calibration only | Confidence as the verification signal | E1 |
| RQ5 | Latency, energy, temperature, memory, action counts | Yes (H3) | Cost of verification only | Overhead of the coupling | E1, E2 |
| RQ6 | Pareto front over accuracy and cost | Yes (H5, F3, F4, F6) | Joint system vs ablations | Integrated system | E2 |

## 4. What the Questions Do Not Ask

- Which architecture is best for 3D-print defect inspection (Step 10B selects candidates as an enabling step).
- Whether the system is superior to existing systems in general.
- Whether results transfer to other devices, tasks or domains not tested.

## 5. Status

All questions: **OPEN — TO BE ANSWERED EXPERIMENTALLY.** No data have been collected.
