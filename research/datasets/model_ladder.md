# Model Configuration Ladder and Confidence Signal — GC-03

_Step 10B, 2026-10-05, Claude Code. Research design only: no model was trained, exported, converted or benchmarked._

Conceptual ladder: [`experimental_framework.md`](../research_questions/experimental_framework.md) §2. Device constraints: [`device_requirements.md`](device_requirements.md). Verification steps: [`verification_checklist.md`](verification_checklist.md).

**No performance value appears in this document.** Accuracy, latency, memory, energy and parameter counts of the exported models are **REQUIRES EMPIRICAL BENCHMARKING** on the chosen device and data. Model families are named as *candidates* only (PROVISIONAL). None is selected because it is popular; §2 gives the selection criteria.

## 1. Task Assumed by the Ladder (PROVISIONAL)

- **Task.** Per-view binary defect classification (defective vs normal) with a class-probability output, plus a pre-registered item-level aggregation across views ([`dataset_selection.md`](dataset_selection.md) §5).
- **Why classification, not unsupervised anomaly detection.**
  - A classifier gives a probability whose calibration can be measured and adjusted per configuration (H4).
  - Memory-bank anomaly detectors (PatchCore-type) carry a feature bank whose size depends on the training set. That makes the memory side of the ladder dataset-dependent and on-device deployment harder to control.
  - This alternative stays open if the supervised split proves infeasible (REQUIRES_VERIFICATION after data inspection).

## 2. Selection Criteria

Every configuration in the final ladder must satisfy all of the following. Each criterion is checked by a named procedure, not by reputation.

| # | Criterion | How it is checked | Status |
| :-- | :-- | :-- | :-- |
| S1 | Same inspection task | Same training data, label space and output head across C1–C4. | PROVISIONAL (design rule) |
| S2 | Comparable outputs | Every configuration outputs a probability for the same classes; the same metrics apply. | PROVISIONAL (design rule) |
| S3 | Different resource requirements | On-device E1 measurement shows strictly ordered cost (latency, energy, memory) from C1 to C4 at R0, beyond measurement resolution. | REQUIRES EMPIRICAL BENCHMARKING |
| S4 | Deployable on the selected smartphone | Converts to the chosen runtime, runs offline, and the intended backend executes the graph (delegation coverage logged). | REQUIRES_VERIFICATION |
| S5 | Confidence available or calibratable | Probability output exists, and temperature scaling (§4) can be fitted on a held-out calibration split. | PROVISIONAL |
| S6 | Distinct accuracy–efficiency trade-offs | Validation accuracy is ordered C1 ≥ C2 ≥ C3 ≥ C4, and adjacent configurations differ by more than the pre-registered SESOI in accuracy or cost. | REQUIRES EMPIRICAL BENCHMARKING |
| S7 | Not chosen for popularity | Each candidate must pass S1–S6. A candidate that fails is replaced, however widely used. | Design rule |

### Formal C1–C4 selection rule

C1–C4 may be selected only after **all** of the following hold, in this order:

1. the smartphone is confirmed (gate G1);
2. the candidate models support the same inspection task (S1, S2);
3. offline deployment is verified on that smartphone (S4);
4. a confidence/probability output is available (S5);
5. the models can be ordered by **measured** resource cost (S3);
6. every configuration satisfies the minimum functional inspection requirements (pre-registered; TO BE PRE-REGISTERED);
7. empirical benchmarking confirms a meaningful resource ladder (S3, S6).

**Final C1–C4 model assignment is deferred to the implementation benchmark stage.**

Until then, the families in §3 are candidates only, every configuration remains PROVISIONAL, and no accuracy, latency, memory or energy value is stated (gate G4).

**Ladder-construction rule (PROVISIONAL).** Build the ladder along a small number of documented axes:
- backbone size;
- input resolution;
- numeric precision (FP32 / FP16 / INT8);
- execution backend (accelerator vs CPU).

Each step should change as few axes as possible, so that the cause of a difference is attributable.

If S3 or S6 fails on the device (e.g. a "lighter" configuration is not cheaper after delegate fallback), the ladder is rebuilt. It is never relabelled to keep the intended order.

## 3. Candidate Ladder (PROVISIONAL)

| Field | C1 — highest accuracy | C2 — medium | C3 — lightweight | C4 — lowest resource |
| :-- | :-- | :-- | :-- | :-- |
| Model family candidate | Largest mobile-deployable CNN backbone that passes S4 (candidates: EfficientNet-family or ConvNeXt-Tiny-class) | Mid-size mobile backbone (candidates: EfficientNet-Lite / MobileNetV3-Large-class) | Small mobile backbone (candidate: MobileNetV3-Small-class) | Same backbone as C3 |
| Parameter count | Read from the exported model (REQUIRES_VERIFICATION) | Same | Same | Same as C3 |
| Input size | Highest on the ladder | ≤ C1 | ≤ C2 | Lowest on the ladder |
| Expected accuracy | Highest (hypothesised ordering only) | Below C1 | Below C2 | Lowest acceptable |
| Expected latency | Highest | Below C1 | Below C2 | Lowest |
| Memory requirement | Highest; must fit at R0 with the camera pipeline and logger | Below C1 | Below C2 | Lowest; must run under memory pressure |
| Accelerator compatibility | GPU delegate / NPU backend (REQUIRES_VERIFICATION) | GPU delegate (REQUIRES_VERIFICATION) | GPU or CPU | CPU (so that it runs when accelerators are throttled or busy) |
| Quantization options | FP16 (FP32 reference off-device) | FP16 or INT8 | INT8 | INT8 (full-integer) |
| Confidence output | Softmax probability → per-configuration temperature scaling (§4) | Same | Same | Same |
| Deployment format | One runtime for all levels: TFLite/LiteRT, ONNX Runtime Mobile or ExecuTorch (choice REQUIRES_VERIFICATION, §5) | Same | Same | Same |
| Limitations | May be unsustainable under thermal load, which is the motivation. Accelerator coverage must be complete or fallback logged. | Must differ enough from C1 and C3 (S6). | INT8 calibration may shift confidence (H4). | Lowest-resolution input may hide small defects; accuracy may fall below usefulness (a finding, not a failure). |
| Metrics | REQUIRES EMPIRICAL BENCHMARKING | REQUIRES EMPIRICAL BENCHMARKING | REQUIRES EMPIRICAL BENCHMARKING | REQUIRES EMPIRICAL BENCHMARKING |

**Escalation (A3)** moves an item to a higher rung, subject to the actions the resource state allows. Keeping C1 resident for escalation at R2–R3 has a memory cost, which is measured.

**B2 (static lightweight)** uses C3 unless C4 is pre-registered.

## 4. Confidence Signal

**Definitions** (Step 9.8 Decision B and Step 10A):
- **Confidence reporting** means a model outputs a score that is logged.
- **Confidence gating** means that confidence, probability or uncertainty **triggers a downstream action** (A1–A4).

Only gating is the mechanism under test. A logged softmax value that triggers nothing is reporting, not gating.

**Raw softmax confidence is not formal uncertainty.** A softmax probability can be miscalibrated and is not an epistemic uncertainty estimate. It is used only after calibration, and calibration is measured (H4).

| Signal | What it is | Overhead | Smartphone feasibility | Assessment |
| :-- | :-- | :-- | :-- | :-- |
| Raw softmax probability | Max class probability | None (part of inference) | Yes | Reported but not used for gating without calibration. |
| **Calibrated probability (temperature scaling)** | Softmax with one scalar temperature per configuration, fitted on a held-out calibration split | Negligible (one division) | Yes | **Simplest defensible signal**: PROVISIONAL primary. |
| Entropy | Entropy of the predictive distribution | Negligible | Yes | For binary classification, a monotone function of the max probability, so it adds nothing. Kept for multi-class extensions. |
| Margin | Difference between the top two probabilities | Negligible | Yes | Equivalent ordering to max probability for binary; same note as entropy. |
| Ensemble uncertainty | Disagreement across several models | Multiplies inference cost | Poor under resource pressure | Not primary. Conflicts with the resource constraint; possible offline analysis only. |
| MC dropout | Several stochastic forward passes | Multiplies inference cost; needs dropout at inference in the exported graph | Poor; runtime support REQUIRES_VERIFICATION | Not primary. |
| Conformal / selective prediction | Threshold set on a calibration split to target a coverage or risk level | Negligible at inference | Yes | **Secondary option** for setting thresholds. Its guarantee assumes exchangeability between calibration and test data, which a resource-driven configuration change may violate. It must be calibrated per configuration and checked (H4). |

**Primary design (PROVISIONAL).**
1. Per-configuration temperature scaling is fitted on a calibration split disjoint from the test split (split by item).
2. The gating signal is the calibrated probability of the predicted class.
3. Thresholds are configuration-specific, set on the calibration split by a pre-registered rule (e.g. a target referral rate or risk level).
4. **Threshold values are not chosen here.**

**Measured, not assumed:**
- calibration error before and after scaling, per configuration and per resource state (E1);
- the added latency and energy of scaling and of each triggered action (H3).

## 5. Runtime Choice (REQUIRES_VERIFICATION)

| Runtime | Consideration | Status |
| :-- | :-- | :-- |
| TFLite / LiteRT | Mature GPU delegate; INT8/FP16 tooling | REQUIRES_VERIFICATION on the device |
| ONNX Runtime Mobile | Several execution providers; vendor NPU coverage varies | REQUIRES_VERIFICATION |
| ExecuTorch | Vendor backends; newer toolchain | REQUIRES_VERIFICATION |

One runtime is used for all of C1–C4, so that runtime differences do not confound the ladder. It is chosen after S4 checks on the selected device.

## 6. Status

| Item | Status |
| :-- | :-- |
| Ladder structure (axes, rules) | PROVISIONAL |
| Model families | PROVISIONAL candidates; not selected |
| Final C1–C4 assignment | Deferred to the implementation benchmark stage (gate G4) |
| Any performance value | None given; REQUIRES EMPIRICAL BENCHMARKING |
| Confidence signal | PROVISIONAL: temperature-scaled probability, configuration-specific thresholds |
| Runtime | REQUIRES_VERIFICATION |
