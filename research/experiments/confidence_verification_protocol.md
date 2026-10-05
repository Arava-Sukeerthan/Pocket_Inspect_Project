# Confidence Estimation and Confidence-Aware Verification Protocol

_Step 10C, 2026-10-05, Claude Code. Protocol design only. No threshold, temperature or calibration value exists._

Master protocol: [`experimental_protocol.md`](experimental_protocol.md). Signal evaluation: [`model_ladder.md`](../datasets/model_ladder.md) §4.

## 1. Data Splits (item-level)

All splits are made **by physical item (Real-IAD sample)**, never by image. All views of an item, and in Stage 2 all recaptures, fall in one split.

| Split | Use | Never used for |
| :-- | :-- | :-- |
| Train | Model training | Anything else |
| Validation | Model selection, early stopping, ladder steps 6–7 | Calibration, thresholds, final evaluation |
| Calibration-T | Fitting the temperature per configuration | Thresholds, final evaluation |
| Calibration-τ | Selecting the confidence thresholds per configuration (and the single B5-F threshold) | Final evaluation |
| Test | Confirmatory evaluation, used once after everything is frozen | Any fitting or tuning |

**Split proportions:** DECISION REQUIRED BEFORE DATA COLLECTION. They are set by a pre-registered rule that guarantees enough defective items in Calibration-τ and Test for the planned analyses (§7 of the master protocol).

**Seeds.** Splits are generated once from a recorded seed, and the item-ID manifests are committed (IDs only, no images).

## 2. Confidence Estimation

**Primary method: configuration-specific probability calibration using temperature scaling.**
1. Each configuration Cᵢ is run **on the device** over Calibration-T, because quantisation and backend numerics differ from desktop execution.
2. One temperature Tᵢ is fitted per configuration by minimising negative log-likelihood.
3. The confidence score is the calibrated probability of the predicted class.

**Raw softmax is never treated as calibrated confidence.** It is logged as `confidence`; the calibrated value is logged separately as `calibrated_confidence`.

**Secondary method: split conformal prediction**, only if feasibility is established (on-device cost and per-configuration calibration). Exchangeability across configurations and resource states is not assumed and must be checked (H4).

**Not primary:** MC dropout and ensembles. Both multiply inference cost under resource pressure, so they are not used unless later justified.

**Calibration metrics** (reported per configuration, before and after scaling, and per resource state at a fixed configuration for H4.b):
- expected calibration error with a pre-registered binning scheme;
- Brier score;
- negative log-likelihood;
- reliability diagrams;
- AUROC of confidence for error detection.

## 3. Threshold Selection

| Element | Rule |
| :-- | :-- |
| Configuration-specific thresholds τᵢ (B4, B5) | Chosen on Calibration-τ by one pre-registered rule applied identically to every configuration. Candidate rules: a target verification-trigger rate, or a target selective risk at a minimum coverage. Rule choice: DECISION REQUIRED BEFORE DATA COLLECTION. |
| Single global threshold τ_F (B5-F) | Same rule, applied once to Calibration-τ outputs pooled across configurations |
| Numerical values | None chosen now. They are computed only by the frozen rule. |
| Freezing | Temperatures, thresholds and rule are written to the configuration with hash and commit before any test-split run |
| Test-set protection | The test manifest is not loaded by the calibration or threshold code. Runs are tagged `split`. Any test-split run before freezing is invalid for confirmatory analysis. |

## 4. Verification Actions

| Action | Meaning | Stage 1 (Real-IAD replay) | Stage 2 (custom capture) | Resource-state condition |
| :-- | :-- | :-- | :-- | :-- |
| A0 | Accept | Allowed | Allowed | Always |
| A1 | Same-view recapture | **NOT AVAILABLE.** Real-IAD stored views are not physical smartphone recapture. | Allowed (physical recapture on the phone) | Allowed if acquisition is permitted in the state (frozen permission table) |
| A2 | Additional view | Allowed as **controlled additional-view simulation**: the next stored view of the same item, in pre-registered order | Allowed (actual capture of a new view) | Same as A1 |
| A3 | Stronger model | Allowed: re-run on a higher ladder rung | Allowed | Allowed only if the state permits that rung (memory, thermal), per the frozen permission table |
| A4 | Human review (referral) | Allowed; the referral is recorded and the item's decision is resolved by ground truth for "system" metrics, which are reported separately from automated metrics, with coverage | Allowed | Always |

A1 has not been validated experimentally. It can be tested only in Stage 2, which needs the custom dataset that does not yet exist (gate G3).

## 5. Verification Policy (general, device-independent)

**Inputs:**
- calibrated confidence;
- the configuration that produced it;
- the resource state;
- the set of actions available in the stage;
- per-action verification cost, measured in E1 per state;
- the item's verification history.

**Rule:**
1. If calibrated confidence ≥ τᵢ for the producing configuration, take **A0**.
2. Otherwise choose, from the actions permitted by the stage and the resource state, the action that is first in a **pre-registered priority order**. The order is set from the E1-measured costs, cheapest effective action first (DECISION REQUIRED BEFORE DATA COLLECTION, after E1).
3. Re-infer and re-evaluate confidence after the action. View fusion for A2 follows a pre-registered rule (e.g. maximum defect probability or mean of calibrated probabilities; DECISION REQUIRED).
4. A per-item cap limits verification actions. When the cap is reached, the item is either referred (A4) or decided at its current prediction, by a pre-registered rule (DECISION REQUIRED).
5. One action type is pre-registered as **primary** for the confirmatory H2 test in each stage. Others are secondary analyses.

**Freezing.** Priority order, cap, fusion rule, permission table and primary action are frozen together with the thresholds.

**Separation from adaptation.** The verification policy never changes the resource state or the adaptation mapping. A3 escalation is a per-item verification action and does not change the configuration used for subsequent items.

## 6. OPPO A5 2020 (3 GB) Instantiation

| Item | Status |
| :-- | :-- |
| On-device calibration runs per configuration | TO BE PERFORMED |
| A3 feasibility (escalation model resident in 3 GB RAM alongside the current one) | TO BE MEASURED (E0/E1) |
| A1/A2 camera capture (Stage 2): Camera2 manual-control level of the rear camera | REQUIRES DEVICE VERIFICATION |
| Verification cost per action and state | TO BE MEASURED (E1) |
