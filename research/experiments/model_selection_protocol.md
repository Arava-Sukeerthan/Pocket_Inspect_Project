# C1–C4 Model-Ladder Selection Protocol

_Step 10C, 2026-10-05, Claude Code. Protocol design only._

**Final C1–C4 identities: TO BE EMPIRICALLY DETERMINED.** No model has been trained, converted, deployed or benchmarked, and no ranking exists. This protocol implements the Step 10B selection rule ([`model_ladder.md`](../datasets/model_ladder.md) §2) as an executable procedure.

## 1. General Definitions (device-independent)

| Configuration | Definition |
| :-- | :-- |
| C1 | Highest-resource / highest-performance candidate that is admissible on the device |
| C2 | Intermediate-high resource candidate |
| C3 | Lightweight candidate |
| C4 | Lowest-resource candidate that still meets the minimum inspection requirement |

A configuration is the tuple (model weights, input resolution, numeric precision, runtime backend). All four use one runtime and one preprocessing pipeline per resolution.

## 2. Seven-Step Empirical Selection Procedure

A candidate enters the ladder only by passing steps 1–6 in order. Step 7 confirms the ladder as a whole. Each step's outcome is logged per candidate as PASS, FAIL or NOT_EVALUATED, with evidence.

| Step | Gate | Procedure | Evidence |
| :-- | :-- | :-- | :-- |
| 1 | Candidate availability | Candidate families and variants are listed from public, licence-compatible sources (Step 10B candidates: EfficientNet-family, ConvNeXt-Tiny-class, EfficientNet-Lite, MobileNetV3-Large/Small-class). Others may be added. Reputation is not a criterion. | Source and licence record |
| 2 | Same inspection task | Trained or fine-tuned on the same training split, label space and output head (per-view binary defect classification) | Training config and hash |
| 3 | Offline deployment on the device | Converts to the chosen runtime; loads and runs offline on the device; backend delegation coverage reported; silent CPU fallback detected | Conversion log, on-device smoke test, delegation report |
| 4 | Probability output | Exposes class probabilities; temperature scaling applicable to on-device outputs | Output signature check |
| 5 | Resource-cost ordering | Measured at R0 in E1 pilot: steady-state latency per item, peak memory, energy over a fixed batch (validated reference). Candidates are ordered by a **pre-registered primary cost metric** (DECISION REQUIRED BEFORE DATA COLLECTION: latency or energy). Two candidates whose cost difference lies within measurement noise are treated as tied, and only one is kept. | E1 pilot cost table |
| 6 | Minimum inspection requirement | Validation-split recall and precision meet the pre-registered minimum functional requirement (value: PRE-DATA-COLLECTION DECISION REQUIRED, set from the inspection use case, not from observed results) | Validation report |
| 7 | Empirical ladder confirmation | Four admissible candidates are chosen so that cost is strictly ordered (C1 > C2 > C3 > C4 beyond noise) and validation accuracy is non-increasing, with adjacent rungs differing by more than the SESOI in accuracy or cost (S6) | Ladder report; frozen before confirmatory runs |

**Data discipline.**
- Selection uses only training and validation data, never calibration or test data.
- The test split is untouched until the confirmatory runs.

## 3. Failure Handling

| Situation | Action |
| :-- | :-- |
| Fewer than four admissible candidates | Use a three- or two-rung ladder and report it. Configurations are not invented to fill four rungs. The hypotheses remain testable with at least two rungs (DECISION REQUIRED on minimum rung count). |
| A nominally lighter candidate is not cheaper on the device | It is placed by its measured cost or dropped. Labels follow the measurements. |
| No candidate fits C1 memory needs on the 3 GB device | C1 is the largest admissible candidate. The limit is reported as a device-specific result. |
| Accelerator unavailable or partial | CPU-only ladder; documented. |

## 4. OPPO A5 2020 (3 GB) Instantiation

| Item | Status |
| :-- | :-- |
| Platform for steps 3–7 | OPPO A5 2020, 3 GB (confirmed, G1) |
| Runtime and backend (CPU; Adreno 610 GPU via the runtime's GPU path; DSP/NPU paths) | REQUIRES DEVICE VERIFICATION |
| Memory headroom for C1 plus camera plus logging | TO BE MEASURED |
| C1–C4 identities | TO BE EMPIRICALLY DETERMINED |

**Transferability.** The same seven steps are repeated on any other device. That device's ladder may differ, and the OPPO A5 2020 ladder is not reused elsewhere.
