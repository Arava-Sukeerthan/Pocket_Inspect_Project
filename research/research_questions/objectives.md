# Research Objectives — GC-03

_Step 10A, 2026-10-05, Claude Code. Objectives describe planned work; none has been carried out._

Research questions: [`research_questions.md`](research_questions.md). Hypotheses: [`hypotheses.md`](hypotheses.md). Traceability: [`traceability_matrix.csv`](traceability_matrix.csv).

## 1. Objectives

| ID | Objective | Research question(s) | Hypothesis / measurement | Deliverable (planned) |
| :-- | :-- | :-- | :-- | :-- |
| O1 | Design a resource-aware runtime inference policy for smartphone visual inspection that maps measured device state (R0–R3) to a configuration on the ladder (C1–C4). | RQ2 | Enables H1, H5; measured by state-transition and configuration logs | Policy specification in `configs/`; policy description in `docs/` |
| O2 | Quantify inspection-performance degradation under controlled resource pressure and configuration downgrading. | RQ2 | H1 | E1 and E2 accuracy and resource tables |
| O3 | Design a confidence-aware downstream verification mechanism that maps confidence, configuration and resource state to an action (A0–A4). | RQ3 | Enables H2, H3, H5; distinguished from a fixed threshold by E3 | Verification-policy specification in `configs/` |
| O4 | Measure how much of the performance degradation the verification mechanism recovers. | RQ3, RQ1 | H2 | Recovery proportion with confidence intervals, per resource state and action |
| O5 | Characterise confidence and calibration changes across configurations and resource states. | RQ4 | H4 | Per-configuration and per-state calibration analysis |
| O6 | Quantify latency, energy, thermal, memory and verification overhead. | RQ5 | H3 | Overhead per item and per verified item |
| O7 | Compare the combined strategy against the ablation baselines B1–B4 (and B5-F). | RQ6 | H5 | Accuracy–cost Pareto analysis |
| O8 | Determine whether the combined approach gives a statistically and practically meaningful accuracy–efficiency improvement. | RQ6, RQ1 | H5, H2 (statistical and practical criteria) | Pre-registered analysis; decision on RQ1 |

## 2. Coverage Checks

**Every research question maps to at least one objective.**

| RQ | Objectives |
| :-- | :-- |
| RQ1 | O4, O8 |
| RQ2 | O1, O2 |
| RQ3 | O3, O4 |
| RQ4 | O5 |
| RQ5 | O6 |
| RQ6 | O7, O8 |

**Every objective maps to at least one research question** (table in §1).

**Every objective maps to a hypothesis or a measurement.** O1 and O3 are design objectives; they do not test a hypothesis on their own but produce the policies whose effects H1, H2, H3 and H5 test, and their behaviour is logged (state transitions, configuration choices, triggered actions).

## 3. Assumptions

- **Assumption.** One Android smartphone with access to battery, thermal-status, CPU/GPU and memory telemetry is available; model and API access are to be verified.
- **Assumption.** Resource pressure can be induced reproducibly (background load, thermal soak, battery/power-saver state).
- **Assumption.** A configuration ladder whose accuracy and cost are ordered can be constructed; the ordering must be verified on the device (Step 10B).
- **Assumption.** At least one dataset with suitable access and licence, and with multiple views for A2, can be used; nothing is downloaded in Step 10A.

## 4. Status

All objectives: **PLANNED — NOT STARTED.**
