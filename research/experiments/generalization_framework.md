# Generalization Framework — Methodology vs Experimental Platform

_Step 10C, 2026-10-05, Claude Code. Protocol design only: no experiment, measurement or result exists._

Master protocol: [`experimental_protocol.md`](experimental_protocol.md).

## 1. Device-Generalization Principle

> The OPPO A5 2020 serves as the primary experimental platform rather than defining the scope of the proposed methodology. The methodology is intended for resource-constrained and legacy smartphones more generally. Device-specific results are reported as evidence obtained on the selected platform, while claims of generalization beyond the evaluated device are limited to what the experimental design supports.

The research contribution is the **methodology**: resource-aware runtime adaptation coupled with confidence-aware downstream verification, and the empirical answer to RQ1. The **OPPO A5 2020 (3 GB RAM variant)** is the platform on which that methodology is evaluated. It is not the contribution, and PocketInspect is not an inspection system designed specifically for that phone.

Three levels are kept separate throughout the repository:

| Level | What it is | Where it lives |
| :-- | :-- | :-- |
| 1. General methodology | Device-independent architecture, resource-state framework, ladder-selection procedure, adaptation policy, verification policy, baselines and analysis | `research/experiments/*.md` (general sections); `configs/experiment_protocol.yaml` `methodology` |
| 2. Experimental device | The OPPO A5 2020, 3 GB, as the platform that instantiates the methodology | "OPPO A5 2020 instantiation" sections; `configs/experiment_protocol.yaml` `platform` |
| 3. Device-specific measurements | Values obtained on that device (thresholds, ladder costs, latencies, energy) | Not yet existing. Future run logs under `research/results/` only. |

## 2. Result Classification

Every future result is labelled with exactly one class before it is reported.

| Class | Definition | Example (illustrative wording; no value exists) | Allowed claim |
| :-- | :-- | :-- | :-- |
| **A. DEVICE-SPECIFIC RESULT** | A numerical or behavioural observation obtained on the OPPO A5 2020 under the protocol | "An inference latency of X ms for C3 at R0 on the OPPO A5 2020" | Holds for this device, software stack and conditions only. |
| **B. METHODOLOGICAL RESULT** | A comparison between policies (B1–B5, B5-F) that answers an RQ or hypothesis on the evaluated device | "Resource-aware model switching reduced computational demand under experimentally induced resource pressure" | Evidence that the mechanism works or fails as designed, on the evaluated platform. |
| **C. GENERALIZATION EVIDENCE** | A result replicated on additional devices or conditions that the design explicitly includes | None planned: the current experiment has one device. | Only if additional devices are approved and evaluated. |
| **D. UNVALIDATED GENERALIZATION** | Any statement about devices, tasks or conditions not evaluated | "The approach should also help other phones with limited RAM" | Must be written as a hypothesis or discussion point, never as a finding. |

**Rules.**
- Numerical performance from the OPPO A5 2020 is never extrapolated to other legacy smartphones.
- A class B result does not become class C without additional evaluated devices.
- With a single device, the strongest available claim is B. Claims of generalization remain D unless the design is extended (DECISION REQUIRED, §4).

## 3. Legacy / Resource-Constrained Smartphone Class

"Legacy" is not defined by chronological age. The methodology targets phones characterised by **measurable resource constraints**:

| Characteristic | How it is measured (E0 device characterisation) |
| :-- | :-- |
| Limited RAM | Total and available RAM; low-memory signals under the ladder's memory load |
| Older CPU/GPU | Sustained throughput of the lightest and heaviest feasible configurations |
| Limited thermal headroom | Time-to-throttle and sustained-performance degradation under a fixed workload |
| Battery constraints | Battery capacity and state, discharge behaviour under sustained inference |
| Limited sustained inference capacity | Drift of latency over a sustained run at a fixed configuration |

The OPPO A5 2020 (3 GB) is treated as a **representative example** of this class, on the basis of its specification. Its actual constraint profile is a device-specific result of E0.

**Eligibility requirements for applying the methodology to another device.** A device is eligible only if all of these hold. Not every old smartphone will meet them.
1. At least two configurations of the ladder run offline with a probability output.
2. Measured resource cost differs between configurations (a ladder exists).
3. At least one device-state signal can be read at runtime and maps to resource pressure, or external instrumentation is available.
4. For the camera-based Stage 2: rear-camera capture with logged capture metadata. Manual locking of exposure and focus is preferred and its absence is recorded.
5. External energy instrumentation is feasible if energy claims are to be made.

## 4. Extending to More Devices

- Future devices are **not** part of the current experiment unless the researcher explicitly approves them.
- If they are added, they repeat E0 and the full ladder-selection procedure. Their thresholds and ladder are derived, never copied from the OPPO A5 2020.
- Whether to include additional devices (to obtain class C evidence) is a **DECISION REQUIRED** by the researcher.
- No multi-device result exists or is implied.
