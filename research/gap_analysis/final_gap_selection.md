# Step 9.9 Phase A: Final Research-Gap Selection Framework

**Status.** Pending researcher review. Phase A framework, reconciled in Step 9.9C with the Step 9.9B GC-03 evidence closure. `selection_status: researcher_approval_required`; `selected_candidate: null`.

**What this document does.**
- Builds a transparent selection framework.
- Evaluates GC-01, GC-02 and GC-03 against it.

**What it does not do.**
- It does not rank, score or weight the candidates.
- It does not select a candidate.
- It does not create `research_gap.md`.

**Companion files.**
- [`final_gap_selection_matrix.csv`](final_gap_selection_matrix.csv): candidate × criterion evidence.
- [`../../configs/gap_selection.yaml`](../../configs/gap_selection.yaml): criteria, gate, candidate RQs, datasets and contribution analysis.

**Epistemic labels** (as in [`RESEARCH_RULES.md`](../../RESEARCH_RULES.md)): **Fact**, **Assumption**, **Hypothesis**, **Proposed idea**. Nothing in this document is an experimental result.

**Ordering.** Candidates are listed in ID order throughout. ID order implies no ordering of merit.

---

## GC-03 Evidence Closure Status

_Added in Step 9.9C. It reconciles Step 9.9 Phase A (`d8894d9`) with the Step 9.9B evidence closure (`f9187fd`). Full record: [`gc03_evidence_closure.md`](gc03_evidence_closure.md). Approval document: [`research_gap_approval.md`](research_gap_approval.md)._

Evidence closure is complete for GC-03, but final research-gap selection requires explicit researcher approval.

| Gate question | Phase A status | Step 9.9B result | Status now recorded |
| :-- | :-- | :-- | :-- |
| Q2. Unknown burden | unresolved | **Conditionally acceptable** | partially_satisfied |
| Q8. Contribution distinguishable from integration | unresolved | **Conditionally distinct** | partially_satisfied |
| Q10. Literature overturn risk | unresolved | **Moderate** | partially_satisfied |

- **Q2: Conditionally acceptable.** The remaining Unknown burden is acceptable for a corpus-bounded candidate-gap statement, provided unresolved high-impact papers such as P001 and AIVD are explicitly retained as limitations. The evidence does not justify a universal claim that no counterexample exists.
- **Q8: Conditionally distinct.** The individual mechanisms already exist in the literature, and integration alone is not sufficient novelty. The potentially distinctive contribution is the experimentally testable question of whether confidence-aware verification can recover inspection performance lost when resource-driven adaptation downgrades a smartphone inspection configuration, including whether confidence calibration changes across configurations.
- **Q10: Moderate.** Additional literature could overturn the candidate if a single study demonstrates smartphone-based optical inspection, device-state-driven runtime configuration changes, and confidence-triggered downstream recapture or escalation in one system. P001, AIVD, and Choi 2026 remain particularly important unresolved evidence.
- **Full counterexamples identified: 0.**
  - Partial counterexamples (all fail the smartphone criterion, and most also fail resource awareness): PMC11435656, SAEC, RobustDefect-LLM, ActiveInspect, arXiv 2608.14727, P011, P016, P007, Yan et al. 2025, RAMS, HAPI.
- **Remaining unresolved evidence:**
  - P001 full text (potential);
  - AIVD, arXiv 2601.04734 (potential; snippet only);
  - Choi et al. 2026 (potential; abstract only);
  - Zakaria et al. 2022 and Electronics 15(17):3915 (potential);
  - ActiveInspect `confidence_gating`, an operational-definition issue (Decision B "explicitly informs" vs "explicitly triggers");
  - database access was substituted rather than direct;
  - English-only search; one results page per search;
  - the remaining corpus Unknown burden.
- **These results are not absolute proof.** They are corpus-bounded and depend on the limitations above.
- **Q3 caveat superseded.** The Q3 rationale below ("keyword-scanned") predates Step 9.9B. Both papers have since been read end to end; the Q3 status itself was left as Phase A recorded it.
- **Researcher approval required.**

At this stage, GC-03 is the strongest approval-ready candidate based on the completed evidence closure, but it has NOT been formally selected. Final selection requires explicit researcher approval.

_Scope of that sentence: it describes evidence-closure status. GC-03 is the only candidate whose Q2, Q8 and Q10 have been closed; GC-01 and GC-02 did not undergo an evidence-closure pass and keep their Phase A gate status. It is not a ranking of merit, and GC-01 and GC-02 remain candidate gaps._

---

## 1. Purpose

Step 9.9 is the stage where final research-gap selection becomes permissible. It has two phases:

- **Phase A (this document).** Define selection principles and criteria, then analyse each candidate:
  - candidate research questions;
  - experimental, dataset and contribution feasibility;
  - risks;
  - a selection gate.
- **Phase B (not performed).** Final selection. It happens only after explicit researcher approval.

## 2. Frozen corpus boundary

- **Fact.** `research/literature/papers.csv` is frozen: 54 records, 31 columns, 0 duplicate IDs, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. This step did not read it for recoding and did not modify it.
- **Fact.** Evidence comes from the merged Step 9.7 and 9.8 artefacts:
  - `gap_candidates.md`;
  - `gap_matrix.csv`;
  - `visual_inspection_scope.csv`;
  - `counterexample_candidates.csv` (48 rows);
  - `targeted_search_log.md` (S01–S45);
  - `candidate_gap_matrix.csv`;
  - `candidate_gap_evaluation.md`.

  Operational Decisions A–C and the narrowed wording are taken from `configs/gap_evaluation.yaml`.
- **Fact.** External papers cited here were found and verified in Step 9.8. None is part of the canonical corpus.
- **Rule.** `Unknown` is never treated as `No`. Dataset availability is never asserted without verification.

## 3. Selection principles

A final research gap must satisfy **all** of the following. They are checked qualitatively in §16; no score is computed.

| # | Principle | Meaning in this workflow |
| :-- | :-- | :-- |
| 1 | Evidence-supported | Supported by verified literature evidence, with Unknown values accounted for |
| 2 | Falsification-surviving | No full counterexample in the Step 9.8 targeted searches |
| 3 | Scientifically precise | Specific enough to yield a testable research question |
| 4 | PocketInspect alignment | Corresponds directly to the PocketInspect research problem (`PROJECT_SPEC.md`) |
| 5 | Experimentally testable | Quantitative experiments can directly test it |
| 6 | Reproducible | Measurements and conditions can be reproduced |
| 7 | Dataset-feasible | Suitable datasets exist, or a defensible acquisition strategy does |
| 8 | Hardware-feasible | Executable on realistic resource-constrained smartphone hardware |
| 9 | Baseline-feasible | Meaningful baselines can be implemented |
| 10 | Contribution clarity | The contribution is distinguishable from merely integrating existing components |
| 11 | Evaluation depth | Supports ablations and quantitative evaluation |
| 12 | Publication defensibility | Can support a technically credible paper |

**Principle on contributions.** Integration of known components is not automatically a novel contribution.

## 4. Evaluation criteria

Each candidate is assessed on criteria A–Q. For each criterion, the matrix records:
- supporting evidence;
- weakening evidence;
- Unknowns;
- counterexamples;
- a qualitative assessment;
- a confidence label;
- the verification still needed.

The practical implication for each candidate is given in §5–§7.

- **Assessment labels:** `supports`, `weakens`, `mixed`, `unresolved`, `feasible`, `feasible_with_conditions`, `difficult`.
- **Confidence labels:** `low`, `moderate`, `high`.

Labels are not converted to numbers and are not aggregated.

| Criterion | What is examined |
| :-- | :-- |
| A. Literature evidence strength | Corpus Yes/No/Unknown counts in the visual-inspection scope and the evidence level behind them |
| B. Unknown/evidence burden | Share of Unknown values and whether full text could resolve them |
| C. Counterexample risk | Full, partial and potential counterexamples from Step 9.8 |
| D. Specificity of the gap | Whether platform, task and mechanism are pinned down |
| E. PocketInspect alignment | Mapping to `PROJECT_SPEC.md` modules and phases |
| F. Research-question clarity | Whether candidate RQs have measurable outcomes and falsification conditions |
| G. Dataset feasibility | Repository-recorded datasets, smartphone capture and multi-view needs |
| H. Smartphone hardware feasibility | Device availability and on-device feasibility |
| I. Measurement feasibility | Whether the outcome variables can be measured validly |
| J. Baseline availability | Implementable baselines and comparators |
| K. Experimental depth | Number and meaning of experimental factors |
| L. Ablation potential | Whether components can be isolated |
| M. Contribution distinctiveness | Existing components versus what would have to be new or experimentally meaningful |
| N. Reproducibility | Controllability of conditions and data |
| O. Implementation complexity | Subsystems to build relative to the plan |
| P. Publication potential | Fit with venues of verified related work |
| Q. Risk of the gap collapsing after additional literature search | Likelihood that more searching yields a full counterexample |

## 5. GC-01 analysis

**Candidate (Step 9.8 wording).** Limited evidence of resource-driven runtime adaptation for visual inspection specifically on resource-constrained smartphones within the reviewed corpus.

- **Adaptive-inference counterexamples (Fact).** Adaptive inference already exists in edge visual inspection:
  - arXiv 2608.14727: content-driven cascade on a Jetson Nano;
  - PMC11435656: confidence-triggered edge-to-cloud escalation on a Raspberry Pi 4;
  - SAEC, arXiv 2509.17136: scene-complexity/confidence-driven edge-cloud routing on a Xeon CPU and an A100.

  Adaptive inference as such is not a gap.
- **Content-driven versus resource-driven (Fact, Decision A).** All three edge examples adapt to input content or prediction confidence. None adapts to device/resource state (`resource_awareness` No or Unknown). Resource-driven runtime adaptation exists on smartphones only for non-inspection workloads (P029, P033, P034; P031 is system-level DVFS).
- **Smartphone evidence (Fact).** P011 is the only full-text-verified smartphone visual-inspection paper in scope, and it uses a static model. P001 is a smartphone record with Unknown visual scope and runtime fields.
- **Resource-awareness evidence (Fact).** In scope, `resource_awareness` is Yes 0 / No 4 / Unknown 23.
- **Remaining Unknowns.**
  - 22/27 in-scope records are unresolved.
  - ApproxDet and Mobiprox (resource/contention-aware mobile inference) were seen at title level only.
  - Electronics 14(11):2188 and DMS are title-only.
- **Possible datasets.** See §12: MVTec AD, DeepPCB, CAXTON and the P016/P020 3D-print sets. A phone-captured evaluation set would be custom (Proposed idea).
- **Possible models (Proposed idea).** Lightweight backbones already used in verified work:
  - MobileNetV2/V3 (arXiv 2603.20288, 2410.11591, 2512.13497);
  - YOLO nano variants (arXiv 2608.14727, 2606.07659).

  These would come as several capacity variants or input resolutions to switch between.
- **Possible resource signals (Assumption: readable on Android).** Thermal status, battery level and charging state, CPU/memory load, frame-latency budget.
- **Experiments, baselines and ablations.** See §11. Baselines: best and smallest static configuration, plus a content-driven cascade. Ablations: trigger signal, action set and policy.
- **Expected contribution (Hypothesis).** A measured effect of device-state-driven adaptation on inspection accuracy and sustained latency, compared with content-driven and static policies. The adaptation mechanism itself is not a contribution (§13).
- **Implementation complexity.** Moderate: an on-device runtime with model variants, telemetry and a policy.
- **Risk of additional counterexamples.** Plausible. Generic mobile adaptive-inference literature is large, and indexed databases were not searched.

| Criterion | Assessment | Confidence | Practical implication |
| :-- | :-- | :-- | :-- |
| A. Literature evidence strength | mixed | low | Supports pursuing the question only with an explicit corpus-bounded framing. |
| B. Unknown/evidence burden | weakens | moderate | A selection would rest mainly on search results rather than corpus coding. |
| C. Counterexample risk | mixed | moderate | The candidate is defensible only in its smartphone-specific, resource-driven form. |
| D. Specificity of the gap | supports | high | Precise enough to derive RQs once device classes are defined. |
| E. PocketInspect alignment | supports | high | Directly maps to planned modules. |
| F. Research-question clarity | supports | moderate | RQs are testable once tolerances are fixed. |
| G. Dataset feasibility | feasible_with_conditions | moderate | Public data can train/evaluate models; phone-domain evaluation needs custom capture. |
| H. Smartphone hardware feasibility | feasible_with_conditions | moderate | Feasible if one or more devices are available. |
| I. Measurement feasibility | feasible_with_conditions | moderate | Requires a controlled measurement protocol. |
| J. Baseline availability | feasible | moderate | Baselines are definable without external code. |
| K. Experimental depth | feasible | moderate | Supports a multi-factor study. |
| L. Ablation potential | feasible | moderate | Component ablations are straightforward. |
| M. Contribution distinctiveness | unresolved | low | Contribution must come from inspection-specific findings, not from the mechanism. |
| N. Reproducibility | feasible_with_conditions | moderate | Reproducible with documented device conditions. |
| O. Implementation complexity | feasible_with_conditions | moderate | Moderate engineering; fewer subsystems than GC-03. |
| P. Publication potential | mixed | low | Publication defensibility depends on inspection-specific evidence. |
| Q. Risk of the gap collapsing after additional literature search | unresolved | low | Additional search could plausibly narrow or overturn the candidate. |

**Candidate research questions and hypotheses.**

- **GC-01-RQ1 (primary; Candidate research question (not final)).** On a resource-constrained Android smartphone running a fixed optical inspection task, does a runtime policy that switches model variant and/or input resolution based on measured device state (thermal status, battery level, CPU load) keep defect-detection performance within a pre-registered tolerance of the best static configuration while reducing latency degradation over sustained inspection sessions?
  - *Measurable outcomes:* defect recall at fixed false-positive rate; image-level AUROC or F1; p50/p95 latency over time; throughput degradation under throttling.
  - *Falsified if:* The resource-driven policy shows no reduction in sustained-session latency degradation relative to the best static configuration, or its accuracy loss exceeds the pre-registered tolerance.
- **GC-01-RQ2 (secondary; Candidate research question (not final)).** Which device-resource signals (thermal status, battery level, CPU/memory load), used alone or combined, produce measurably different accuracy-latency trade-offs when driving runtime adaptation for smartphone inspection?
  - *Measurable outcomes:* accuracy-latency trade-off per signal configuration; number of adaptation switches; time spent in throttled states.
  - *Falsified if:* All signal configurations produce trade-offs indistinguishable within run-to-run variance.
- **GC-01-RQ3 (evaluation; Candidate research question (not final)).** How do resource-driven, content-driven and static configurations compare on accuracy, latency and throttling behaviour under controlled thermal and battery conditions?
  - *Measurable outcomes:* accuracy; latency distribution; throttling onset time; battery drain per inspected item.
  - *Falsified if:* Resource-driven and content-driven policies yield the same outcomes within variance across all tested conditions.
- **Candidate hypotheses.**
  - H-GC01-1 (Hypothesis): A device-state-driven policy reduces sustained-session latency degradation relative to the best static configuration with accuracy loss within a pre-registered tolerance.
  - H-GC01-2 (Hypothesis): Thermal-status signals contribute more to sustained performance than battery level on the tested devices.

## 6. GC-02 analysis

**Candidate (Step 9.8 wording).** Limited direct joint evaluation of energy and thermal behavior for resource-adaptive visual inspection on resource-constrained smartphones within the reviewed corpus.

- **Energy counterexamples (Fact).**
  - TinyGLASS (arXiv 2603.16451) reports energy per inference for in-sensor edge visual inspection. It has no thermal results and does not use a smartphone.
  - SAEC reports energy per correct prediction (GPU power), with no thermal results.

  Energy evaluation of visual inspection therefore exists. The candidate does not claim otherwise.
- **Smartphone energy studies outside inspection (Fact).**
  - arXiv 2603.26603 measures energy (Android BatteryManager) and device temperature on a Samsung Galaxy S25 Ultra for LLM inference, without adaptation.
  - P029 and P034 report energy for adaptive inference on mobile devices (non-inspection).
- **Thermal evidence (Fact).**
  - P031 measures thermal behaviour on a smartphone (generic object detection).
  - arXiv 2010.06291 measures thermal throttling on a Raspberry Pi 4B (ImageNet classification).
  - No verified inspection paper reports device thermal behaviour.
- **Is joint measurement meaningful? (Hypothesis H-GC02-1).** It is meaningful only if energy-optimal and thermally sustainable configurations can differ for inspection workloads. If they always coincide, joint measurement adds little. GC-02-RQ1 is designed to falsify this.
- **Hardware measurement feasibility and instrumentation.**
  - *Fact (arXiv 2603.26603):* on-device BatteryManager logging works without root.
  - *Fact (same paper's discussion):* external monitors need battery bypass, which changes thermal behaviour.
  - *Assumption:* a USB power monitor or a bypass setup is available for validation.
- **Datasets.** Energy and thermal behaviour are workload-driven, so repository-recorded datasets can drive the workload (§12).
- **Baselines, experiments, ablations and reproducibility.** See §11. Baselines are static and adaptive configurations. Reproducibility needs fixed ambient temperature, battery range and cool-down protocols (as in arXiv 2603.26603).
- **Publication potential.** Mixed: defensible if H-GC02-1 holds, weaker if the study reduces to measurements.
- **Engineering complexity.** Moderate. It needs a GC-01-type adaptive mechanism plus a measurement harness.
- **Benchmarking risk.** The main contribution risk is that the work becomes primarily benchmarking (§13, §14).

| Criterion | Assessment | Confidence | Practical implication |
| :-- | :-- | :-- | :-- |
| A. Literature evidence strength | mixed | low | Defensible only in its joint, resource-adaptive, smartphone form. |
| B. Unknown/evidence burden | weakens | moderate | Selection would rest mainly on search results. |
| C. Counterexample risk | mixed | moderate | Measurement methodology exists; the inspection-specific joint evaluation is what remains. |
| D. Specificity of the gap | supports | moderate | Precise, but coupled to GC-01. |
| E. PocketInspect alignment | supports | high | Directly maps to monitoring/ and adaptation/. |
| F. Research-question clarity | supports | moderate | Clear primary RQ; validity study is a prerequisite. |
| G. Dataset feasibility | feasible_with_conditions | moderate | Least data-dependent of the three for the measurement part. |
| H. Smartphone hardware feasibility | feasible_with_conditions | moderate | Feasible with BatteryManager logging; external validation needs hardware. |
| I. Measurement feasibility | feasible_with_conditions | moderate | Measurement validity is the main technical risk. |
| J. Baseline availability | feasible | moderate | Baselines are easy to define. |
| K. Experimental depth | feasible_with_conditions | moderate | Depth depends on H-GC02-1 holding. |
| L. Ablation potential | feasible | moderate | Feasible as a factorial measurement design. |
| M. Contribution distinctiveness | unresolved | low | Contribution risk is that it becomes primarily benchmarking. |
| N. Reproducibility | feasible_with_conditions | moderate | Reproducible with strict protocol. |
| O. Implementation complexity | feasible_with_conditions | moderate | Moderate; depends on GC-01 components. |
| P. Publication potential | mixed | low | Defensible if H-GC02-1 holds; weaker otherwise. |
| Q. Risk of the gap collapsing after additional literature search | unresolved | low | Additional search could narrow the candidate. |

**Candidate research questions and hypotheses.**

- **GC-02-RQ1 (primary; Candidate research question (not final)).** For resource-adaptive optical inspection on a resource-constrained smartphone, do energy-only and joint energy-plus-thermal evaluations lead to different conclusions about which configuration sustains the target inspection throughput over a fixed session length?
  - *Measurable outcomes:* energy per inspected item; device/battery temperature trajectory; time to thermal throttling; sustained throughput.
  - *Falsified if:* Energy-only and joint energy-thermal evaluations select the same configurations under all tested sustained workloads.
- **GC-02-RQ2 (secondary; Candidate research question (not final)).** How do energy per inspected item and thermal trajectory change between static and resource-adaptive inspection configurations under sustained workloads at controlled ambient temperature?
  - *Measurable outcomes:* energy per inspected item; peak and mean temperature; time to throttling; accuracy.
  - *Falsified if:* No measurable difference in energy or thermal trajectory between static and adaptive configurations beyond run-to-run variance.
- **GC-02-RQ3 (evaluation; Candidate research question (not final)).** How closely does on-device software energy logging (Android BatteryManager) agree with an external power measurement for inspection workloads on the target smartphone?
  - *Measurable outcomes:* agreement between software and external energy estimates; bias and variance across runs.
  - *Falsified if:* Not a hypothesis test in itself; it establishes the measurement validity required by RQ1 and RQ2.
- **Candidate hypotheses.**
  - H-GC02-1 (Hypothesis): Energy-optimal and thermally sustainable configurations differ for at least one tested inspection workload.

## 7. GC-03 analysis

**Candidate (Step 9.8 wording).** Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus.

- **PMC11435656 (partial; Fact).** Raspberry Pi 4 PCB inspection in which low-confidence samples escalate to a cloud model. This is runtime adaptation plus confidence-triggered verification. It does not use a smartphone, and `resource_awareness` is **No** (Step 9.9B end-to-end read: confidence-only routing; the three-device split is design-time).
- **ActiveInspect (partial; Fact).** Learned selection of additional views/modalities on A100 GPUs. `resource_awareness` is **No** (Step 9.9B end-to-end read: fixed observation budget). Under Decision B, learned view selection alone is not confidence gating; `confidence_gating` stays Unknown as an operational-definition issue.
- **SAEC (partial; Fact).** Edge predictions are accepted only if probability, margin and entropy thresholds hold; otherwise they escalate. The routing is content/confidence-driven, not resource-driven, and does not run on a smartphone.
- **arXiv 2608.14727 (partial; Fact).** Content-driven cascade at the edge, positioned as triage. Its trigger score is not described as confidence.
- **RobustDefect-LLM (partial; Fact).** Confidence/margin-triggered human review with a mobile client. Inference runs in a backend, and there is no adaptation.
- **Edge versus smartphone.** Every partial counterexample runs on edge boards, CPUs or GPUs, or uses the phone only as a client.
- **Content-driven versus resource-driven.** No partial counterexample adapts to device state.
- **View selection versus confidence gating.** Only a confidence-, uncertainty- or prediction-quality-triggered action qualifies (Decision B).
- **Recapture and additional-view options (Proposed idea).**
  - User-prompted recapture through the app;
  - scripted recapture on a rig;
  - additional view from a second pose;
  - escalation to a larger on-device model.
- **Datasets.** Multi-view datasets are recorded in the corpus (Real-IAD, MANTA, MVTec3D-AD/Eyecandies). No smartphone recapture dataset was identified (§12).
- **Measurable outcomes.** Recall at a fixed review rate, trigger rate, expected calibration error, risk–coverage, latency, energy.
- **Implementation complexity.** The highest of the three (§14).
- **Integration risk.** Combining known components is not automatically a contribution. A contribution needs a question beyond integration, e.g. calibration shift under resource-driven downgrades (Hypothesis H-GC03-1).

| Criterion | Assessment | Confidence | Practical implication |
| :-- | :-- | :-- | :-- |
| A. Literature evidence strength | mixed | low | Defensible only as the integrated, resource-aware smartphone realisation. |
| B. Unknown/evidence burden | weakens | moderate | Selection would rest mainly on search results. |
| C. Counterexample risk | mixed | moderate | Closest neighbours are near; distinction rests on smartphone + resource-driven trigger. |
| D. Specificity of the gap | supports | moderate | Precise but conjunctive. |
| E. PocketInspect alignment | supports | high | Maps to the most modules. |
| F. Research-question clarity | supports | moderate | Testable with a rig or scripted recapture. |
| G. Dataset feasibility | difficult | moderate | Most data-demanding; custom acquisition likely required. |
| H. Smartphone hardware feasibility | feasible_with_conditions | moderate | Feasible with app development. |
| I. Measurement feasibility | feasible_with_conditions | moderate | Measurement feasible with controlled acquisition. |
| J. Baseline availability | feasible | moderate | Natural factorial baselines. |
| K. Experimental depth | feasible | moderate | Richest experimental space. |
| L. Ablation potential | feasible | moderate | Strong ablation structure. |
| M. Contribution distinctiveness | unresolved | low | Contribution must come from a question beyond integration. |
| N. Reproducibility | feasible_with_conditions | moderate | Reproducible only with scripted acquisition. |
| O. Implementation complexity | difficult | moderate | Highest engineering complexity. |
| P. Publication potential | mixed | low | Defensible if a question beyond integration is answered. |
| Q. Risk of the gap collapsing after additional literature search | unresolved | low | Additional search could plausibly narrow the candidate. |

**Candidate research questions and hypotheses.**

- **GC-03-RQ1 (primary; Candidate research question (not final)).** Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained smartphone dynamically downgrades its inference configuration under changing device conditions? _(Step 9.9C approval-ready wording. The Phase A wording is kept in `configs/gap_selection.yaml` as `phase_a_text`.)_
  - *Independent variables:* resource/device state; selected inference configuration; adaptation state.
  - *Dependent variables:* recall; precision; F1; mAP where appropriate; calibration/error; latency; energy/power; temperature; memory; recapture rate; escalation rate.
  - *Potential mediating variable:* confidence threshold / uncertainty.
  - *Measurable outcomes:* recall; precision; F1; mAP where appropriate; calibration error; latency; energy/power; temperature; memory; recapture rate; escalation rate.
  - *Falsified if:* Confidence-triggered verification does not recover recall beyond the downgraded baseline, or recovers it only at a cost equal to running the full-capacity configuration.
- **GC-03-RQ2 (secondary; Candidate research question (not final)).** Does the confidence calibration of the inspection model change across resource-adaptive configurations, and does per-configuration threshold recalibration change verification trigger rates and residual error?
  - *Measurable outcomes:* expected calibration error per configuration; risk-coverage curves; trigger rate; residual error rate.
  - *Falsified if:* Calibration error and trigger behaviour are unchanged across configurations within variance.
- **GC-03-RQ3 (evaluation; Candidate research question (not final)).** What are the risk-coverage and operator-workload trade-offs of combining resource-driven adaptation with confidence-aware verification, compared with each component alone?
  - *Measurable outcomes:* risk-coverage curve; referral rate; recall at fixed referral rate; latency; energy.
  - *Falsified if:* The combination is not distinguishable from the better single component on any measured trade-off.
- **Candidate hypotheses** (Step 9.9C; they replace H-GC03-1, now H4, and H-GC03-2, now H2 and H5). All are **CANDIDATE — NOT YET TESTED**:
  - H1: Resource-driven runtime downgrading decreases inspection performance relative to the best static configuration under equivalent task conditions.
  - H2: Confidence-aware downstream verification recovers a measurable portion of the performance degradation introduced by resource-driven downgrading.
  - H3: Confidence-aware verification introduces measurable computational and/or energy/latency overhead.
  - H4: Confidence distributions and calibration characteristics differ between inference configurations operating under different resource conditions.
  - H5: A joint resource-adaptation + confidence-verification policy provides a more favorable accuracy–efficiency trade-off than either mechanism alone.

## 8. Comparative strengths

Listed in ID order; no ordering of merit is implied.

- **GC-01.**
  - Precise trigger distinction (resource-driven versus content-driven) backed by verified partial counterexamples.
  - Simple baselines and ablations.
  - Moderate engineering effort.
  - Reusable as a foundation for the other two candidates.
- **GC-02.**
  - Least data-dependent for its measurement part.
  - The primary RQ is cleanly falsifiable (energy-only versus joint conclusions).
  - Measurement protocols exist in verified non-inspection work.
- **GC-03.**
  - Richest experimental and ablation space.
  - Maps to the most `PROJECT_SPEC.md` modules.
  - Admits a question beyond integration (calibration shift under downgrades).

## 9. Comparative weaknesses

Listed in ID order; no ordering of merit is implied.

- **GC-01.**
  - The mechanism is demonstrated on smartphones outside inspection, so contribution distinctiveness is unresolved.
  - High Unknown burden.
- **GC-02.**
  - Risk of becoming primarily benchmarking.
  - Depends on a GC-01-type mechanism.
  - Measurement validity (software versus external) is unverified on the target device.
- **GC-03.**
  - The most Unknown-dependent candidate.
  - The closest partial counterexamples meet three of five components.
  - The most demanding data needs (recapture/multi-view on a phone).
  - The highest engineering complexity.

**Shared weaknesses.**
- Corpus-bounded evidence.
- Indexed databases not searched.
- Device availability and Android API access are Assumptions.

## 10. Research-question feasibility

All RQs below are **candidate research questions (not final)**. Final PocketInspect RQs are not set in Phase A.

| RQ | Candidate | Type | Measurable outcomes | Falsification condition |
| :-- | :-- | :-- | :-- | :-- |
| GC-01-RQ1 | GC-01 | primary | defect recall at fixed false-positive rate; image-level AUROC or F1; p50/p95 latency over time; throughput degradation under throttling | The resource-driven policy shows no reduction in sustained-session latency degradation relative to the best static configuration, or its accuracy loss exceeds the pre-registered tolerance. |
| GC-01-RQ2 | GC-01 | secondary | accuracy-latency trade-off per signal configuration; number of adaptation switches; time spent in throttled states | All signal configurations produce trade-offs indistinguishable within run-to-run variance. |
| GC-01-RQ3 | GC-01 | evaluation | accuracy; latency distribution; throttling onset time; battery drain per inspected item | Resource-driven and content-driven policies yield the same outcomes within variance across all tested conditions. |
| GC-02-RQ1 | GC-02 | primary | energy per inspected item; device/battery temperature trajectory; time to thermal throttling; sustained throughput | Energy-only and joint energy-thermal evaluations select the same configurations under all tested sustained workloads. |
| GC-02-RQ2 | GC-02 | secondary | energy per inspected item; peak and mean temperature; time to throttling; accuracy | No measurable difference in energy or thermal trajectory between static and adaptive configurations beyond run-to-run variance. |
| GC-02-RQ3 | GC-02 | evaluation | agreement between software and external energy estimates; bias and variance across runs | Not a hypothesis test in itself; it establishes the measurement validity required by RQ1 and RQ2. |
| GC-03-RQ1 | GC-03 | primary | recall; precision; F1; mAP where appropriate; calibration error; latency; energy/power; temperature; memory; recapture rate; escalation rate | Confidence-triggered verification does not recover recall beyond the downgraded baseline, or recovers it only at a cost equal to running the full-capacity configuration. |
| GC-03-RQ2 | GC-03 | secondary | expected calibration error per configuration; risk-coverage curves; trigger rate; residual error rate | Calibration error and trigger behaviour are unchanged across configurations within variance. |
| GC-03-RQ3 | GC-03 | evaluation | risk-coverage curve; referral rate; recall at fixed referral rate; latency; energy | The combination is not distinguishable from the better single component on any measured trade-off. |

**Feasibility notes.**
- Every RQ needs pre-registered tolerances, session lengths and operating points, stored in `configs/` before any run.
- GC-02-RQ3 is a measurement-validity study, not a hypothesis test, and is a prerequisite for GC-02-RQ1.
- GC-03 RQs need a controlled acquisition protocol.

## 11. Experimental feasibility

Hypothetical minimum viable experiments (**Proposed idea**). Nothing here has been implemented, and no results are claimed.

| Item | GC-01 | GC-02 | GC-03 |
| :-- | :-- | :-- | :-- |
| 1. Input/data | Public optical dataset (e.g. MVTec AD or a 3D-print set) replayed as a stream, plus a small phone-captured evaluation set | Same workload as GC-01 (data mainly drives compute) | Multi-view dataset (Real-IAD/MANTA) to emulate additional views, plus phone-captured recapture sequences of 3D-printed parts |
| 2. Smartphone hardware | One or more Android phones of a resource-constrained class (models to be fixed; Assumption: available) | Same, plus an external power monitor or bypass setup for validation (Assumption) | Same as GC-01, with app-level camera control or a fixed rig |
| 3. Baseline model | Static lightweight backbone (e.g. MobileNet-class or YOLO-nano-class) at fixed resolution | Static configurations of the same models | Static model without verification |
| 4. Proposed mechanism | Policy switching model variant/resolution/frame rate on device-state thresholds | GC-01 mechanism under joint energy-thermal measurement | GC-01 mechanism plus confidence-triggered verification (recapture/additional view/escalation) |
| 5. Independent variables | Policy (static/content/resource), signal set, ambient temperature, session length | Configuration (static/adaptive), session length, ambient temperature, battery start range | Adaptation on/off, verification on/off, action type, confidence threshold |
| 6. Dependent variables | Accuracy, latency over time, throttling state, switch count | Energy per item, temperature trajectory, time to throttling, sustained throughput, accuracy | Recall, trigger rate, calibration error, latency, energy |
| 7. Accuracy metrics | Image-level AUROC/F1; recall at fixed false-positive rate | Same as GC-01 (secondary) | Recall at fixed review rate; risk-coverage |
| 8. Latency metrics | p50/p95 per-item latency; throughput over time | Sustained throughput | Added latency per verified item |
| 9. Energy metrics | Battery drain per item (secondary) | Energy per inspected item (software and external) | Added energy per verified item |
| 10. Thermal metrics | Thermal status timeline; throttling onset | Battery/device temperature trajectory; time to throttling | Thermal status timeline (secondary) |
| 11. Confidence metrics | Not primary | Not primary | Expected calibration error per configuration; threshold trigger statistics |
| 12. Resource metrics | CPU/memory load, battery level, thermal status | Same plus current/voltage logs | Same as GC-01 |
| 13. Ablations | Remove each signal; fix the policy; restrict the action set | Vary one factor at a time | Adaptation × verification × action type; recalibrated versus fixed thresholds |
| 14. Runs | Repeated sustained sessions per condition; count set from pilot variance (Assumption) | Repeated sessions with cool-down between runs; count set from pilot variance | Repeated runs per factorial cell; count set from pilot variance |
| 15. Reproducibility | Fixed device/OS, configs, seeds, ambient protocol, telemetry logs (RESEARCH_RULES §7) | As GC-01, plus battery range, cool-down and validation against external measurement | As GC-01, plus scripted acquisition and released capture protocol |

## 12. Dataset feasibility

Repository-derived entries come from `papers.csv` records (read-only) or from Step 9.8 verified external papers, as marked. No external dataset search was performed in Step 9.9.

Availability is `verification_required` or `unknown` for every entry. Access, licence and download were **not** verified in this step.

**Step 9.9C qualification.** The reviewed dataset candidates appear technically suitable for visual-defect inspection experiments, but access, licensing, smartphone suitability, and multi-view/recapture suitability require dataset-specific verification. None of the 13 entries is claimed to be available, licensed or smartphone-captured.

| Dataset | Source | Modality | Task | Defects / size (as recorded) | Smartphone-captured | Multi-view | Availability | Relevant to |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| MVTec AD | P009 (corpus) | RGB images | unsupervised anomaly detection / defect localisation | >70 defect types, 15 categories (corpus record) | Unknown | Unknown | verification_required | GC-01, GC-02, GC-03 |
| Real-IAD | P037 (corpus) | RGB images, multi-view | multi-view industrial anomaly detection | 30 objects, 150K images (corpus record) | Unknown | Yes | verification_required | GC-03 |
| MANTA | P038 (corpus) | RGB images, 5 viewpoints per object | multi-view visual-text anomaly detection for tiny objects | 38 categories, 137.3K images, 8.6K anomalous (corpus record) | Unknown | Yes | verification_required | GC-03 |
| MVTec3D-AD and Eyecandies | P043 (corpus) | RGB + point cloud | 3D anomaly detection | not recorded in corpus | Unknown | Yes (multi-view RGB per P043) | verification_required | GC-03 |
| DeepPCB / public PCB defect dataset | P047 (corpus) | RGB images | PCB defect detection | not recorded in corpus | Unknown | Unknown | verification_required | GC-01, GC-02 |
| CAXTON | P015 (corpus) | RGB images from printer-mounted cameras | 3D-print extrusion error detection | 1,272,273 images from 192 prints (corpus record) | No (printer-mounted cameras per corpus) | No | verification_required | GC-01, GC-02 |
| P016 stringing dataset | P016 (corpus) | RGB camera frames | 3D-print stringing detection | 500 images augmented to 2,500 (corpus record) | No | No | unknown | GC-01, GC-02, GC-03 |
| P020 layer images | P020 (corpus) | RGB layer images | FDM layer-wise fault detection | 1,700 good/bad images (corpus record) | No (Raspberry Pi camera) | No | unknown | GC-01, GC-02 |
| VisA | arXiv 2603.20288 (Step 9.8 external, not in papers.csv) | RGB images | visual anomaly detection | not recorded in repository | Unknown | Unknown | verification_required | GC-01, GC-02 |
| KolektorSDD2 | SAEC arXiv 2509.17136 (Step 9.8 external) | RGB images | surface defect detection | not recorded in repository | Unknown | Unknown | verification_required | GC-01, GC-03 |
| NEU-DET | arXiv 2608.08589 and 2606.07659 (Step 9.8 external) | steel-surface images | 6-class surface defect classification/detection | about 1,800 images (1,799-1,800 as reported), 6 classes | Unknown | Unknown | verification_required | GC-03 |
| MMS dataset | TinyGLASS arXiv 2603.16451 (Step 9.8 external) | microscope and IMX500 sensor images (cross-device) | micro-component anomaly detection | crack-hole, scratch, half (as reported) | No | No (cross-device, same objects) | verification_required | GC-02 |
| Phone-captured 3D-printed-part set | Proposed idea (no existing dataset identified) | smartphone RGB images/video, optional recapture and multiple views | 3D-printed part inspection | to be designed (seeded defects as in P016/P020/P022) | Yes (by design) | Optional (by design) | unknown | GC-01, GC-02, GC-03 |

**Class balance (Fact/Assumption).**
- MVTec AD and Real-IAD are recorded in the corpus as anomaly-detection benchmarks; their class balance is not recorded in the repository (to verify).
- The P016 and P020 custom sets report image counts only.

**Per candidate.**
- **GC-01.** Feasible with conditions. Public data covers model training/evaluation; a phone-captured set is needed for in-domain evaluation (custom; Proposed idea).
- **GC-02.** Feasible with conditions. The measurement part is workload-driven; accuracy reporting has the same needs as GC-01.
- **GC-03.** Difficult. Multi-view datasets can emulate additional views, but no smartphone recapture or multi-view inspection dataset was identified. A custom acquisition is likely required.

**Verification required.** For each dataset: licence, download access, defect taxonomy and class balance. For the custom set: acquisition protocol and annotation plan.

## 13. Contribution analysis

**Integration of known components is not automatically a novel contribution.** Existing components are listed as demonstrated in the literature. Potential contributions are listed as requiring empirical validation, and none is claimed.

**GC-01**
- *Existing components (demonstrated in literature; not claimed as contributions):*
  - Runtime resource-aware model/sub-network adaptation on smartphones (non-inspection workloads) (P029, P033, P034).
  - Thermal-driven DVFS on smartphones (system-level) (P031).
  - Content-driven cascades in edge visual inspection (arXiv 2608.14727, SAEC arXiv 2509.17136).
  - Smartphone on-device visual inspection with a static model (P011).
- *Potential research contribution (requires empirical validation; not a finding):*
  - Quantified effect of device-state-driven adaptation on inspection accuracy and sustained latency, compared with content-driven and static policies, on smartphones.
  - Inspection-specific accuracy-tolerance constraints for adaptation policies (e.g. defect recall floor), if they change policy behaviour relative to generic workloads.
- *What would have to be technically new or experimentally meaningful:* evidence that inspection-specific constraints (e.g. defect-recall floors under resource pressure) change adaptation behaviour or outcomes, relative to content-driven and static policies, on smartphones.

**GC-02**
- *Existing components (demonstrated in literature; not claimed as contributions):*
  - Energy reporting for edge visual inspection (TinyGLASS arXiv 2603.16451, SAEC arXiv 2509.17136).
  - Smartphone energy and temperature logging without root (LLM workload) (arXiv 2603.26603).
  - Smartphone energy evaluation of adaptive inference (non-inspection) (P029, P034).
  - Thermal measurement of CNN inference on edge boards (arXiv 2010.06291; P031 (smartphone, non-inspection)).
- *Potential research contribution (requires empirical validation; not a finding):*
  - Evidence on whether joint energy-thermal evaluation changes configuration conclusions for resource-adaptive smartphone inspection.
  - A reproducible on-device measurement protocol for inspection workloads, validated against external measurement.
- *What would have to be technically new or experimentally meaningful:* evidence that joint energy-thermal evaluation changes configuration conclusions for resource-adaptive inspection (H-GC02-1), together with a validated protocol. Without this, the work is a benchmark.

**GC-03**
- *Existing components (demonstrated in literature; not claimed as contributions):*
  - Confidence-triggered escalation combined with per-sample adaptation at the edge (PMC11435656, SAEC arXiv 2509.17136).
  - Confidence/margin-triggered human review with a mobile client (backend inference) (RobustDefect-LLM arXiv 2608.08589).
  - Learned additional-view selection (GPU) (ActiveInspect doi 10.3390/s26154932).
  - Confidence-gated action on an edge 3D-print monitor (P016).
  - Confidence-based early exit in visual defect inspection, not on a smartphone (Yan et al. 2025; abstract level, Step 9.9B).
  - Resource-adaptive and confidence-conditioned switching outside inspection (RAMS, HAPI at snippet level; Choi et al. 2026 at abstract level; Step 9.9B).
  - Resource-aware inference and energy/thermal monitoring on smartphones, non-inspection (P029, P031, P033, P034; arXiv 2603.26603).
- *Potential research contribution (requires empirical validation; not a finding):*
  - **CANDIDATE CONTRIBUTION — REQUIRES EXPERIMENTAL VALIDATION:** An empirical investigation of whether confidence-aware downstream verification can recover inspection performance degraded by resource-driven runtime configuration changes on a resource-constrained smartphone, including analysis of accuracy, calibration, latency, energy, thermal behavior, and verification overhead.
  - Evidence on whether confidence calibration shifts under resource-driven downgrades and whether per-configuration recalibration is needed.
- *What would have to be technically new or experimentally meaningful:* evidence about the interaction between resource-driven downgrades and confidence-aware verification (e.g. calibration shift and the cost–recall trade-off). The combination alone is not enough.

## 14. Risk analysis

Qualitative levels (low/moderate/high) with reasons. The levels are not combined into a single value.

| Risk | GC-01 | GC-02 | GC-03 |
| :-- | :-- | :-- | :-- |
| Literature | Moderate: generic mobile adaptive inference is large; title-level resource-aware mobile hits unresolved | Moderate: mobile energy/thermal measurement literature is large; thermography noise in search | Moderate: close partial counterexamples exist (PMC11435656, SAEC) |
| Evidence/Unknown | High: 23/27 in-scope Unknown per runtime field | High: 23/27 Unknown for energy and thermal | High: 24/27 Unknown for confidence_gating |
| Implementation | Moderate: runtime with model variants and telemetry | Moderate: adaptive mechanism plus measurement harness | High: adaptation, verification and acquisition loop |
| Dataset | Moderate: no phone-captured inspection dataset identified | Low to moderate: workload-driven; accuracy needs phone data | High: recapture/multi-view phone data needed |
| Hardware | Moderate: device availability and API access are Assumptions | Moderate to high: external validation instrumentation is an Assumption | Moderate: as GC-01 plus camera control |
| Evaluation | Moderate: effect sizes unknown; ambient confounds | Moderate: software energy validity unverified | Moderate to high: factorial size; user variability |
| Contribution | High: mechanism demonstrated outside inspection | High: benchmarking risk | High: integration risk |
| Publication | Moderate: depends on inspection-specific findings | Moderate: depends on H-GC02-1 | Moderate: depends on a question beyond integration |

## 15. Evidence still required

1. Full texts of P001 and P007, the main unresolved corpus records that could flip a candidate. _(Step 9.9B: attempted; both publisher hosts blocked; still unresolved.)_
2. End-to-end reads of PMC11435656 (`resource_awareness`) and ActiveInspect (`confidence_gating`). _(Step 9.9B: done. PMC11435656 `resource_awareness` is No. ActiveInspect `confidence_gating` remains an operational-definition issue.)_
3. Resolution of title-only hits:
   - Electronics 14(11):2188;
   - DMS;
   - ApproxDet;
   - Mobiprox;
   - arXiv 1904.09814;
   - PMC10280690;
   - Electronics 15(17):3915;
   - the FOMO/Edge Impulse paper.
4. An indexed-database search (IEEE Xplore, ACM DL, Scopus) for each narrowed wording. _(Step 9.9B, GC-03 only: 12 searches, S46–S57, through labelled substitutes because the databases were blocked. GC-01 and GC-02 not searched.)_
5. Dataset licence, access and class-balance verification (§12).
6. Confirmation of the available Android devices and of read access to thermal/battery state.
7. For GC-02: validation of on-device energy logging against an external measurement.
8. For GC-03: a pilot on calibration shift under configuration changes (H-GC03-1).

## 16. Researcher decision

**Selection gate (Part XI).** Each candidate is checked against the ten gate questions. Statuses are qualitative and are not aggregated.

| Gate question | GC-01 | GC-02 | GC-03 |
| :-- | :-- | :-- | :-- |
| Q1. Is the evidence strong enough? | **partially_satisfied**: Corpus observation holds (resource_awareness/adaptive_inference Yes 0 in scope) and survived 15 targeted searches, but rests on 4 verified No records and 1 verified smartphone visual-inspection paper (P011). | **partially_satisfied**: No in-scope or core paper is coded Yes for both energy and thermal; survived 15 targeted searches; evidence rests on 4 verified No records. | **partially_satisfied**: No in-corpus paper meets three of the Step 9.7 components; survived 16 targeted searches; confidence_gating evidence in scope is Yes 1 (P016). |
| Q2. Is the Unknown burden acceptable? | **unresolved**: 23/27 in-scope records Unknown per runtime field; acceptable only under the corpus-bounded framing; P001 unresolved. | **unresolved**: 23/27 in-scope records Unknown for energy and for thermal; P007 unresolved. | **partially_satisfied** (Step 9.9B: conditionally acceptable): acceptable for a corpus-bounded statement provided P001 and AIVD are retained as limitations; no universal claim that no counterexample exists. |
| Q3. Are counterexamples sufficiently understood? | **satisfied**: Partial counterexamples (arXiv 2608.14727, PMC11435656, SAEC) are characterised: content- or confidence-driven, not smartphone. | **satisfied**: TinyGLASS (edge energy only), SAEC (energy, no thermal, not smartphone) and arXiv 2603.26603 (smartphone energy + temperature, LLM workload) are characterised. | **partially_satisfied**: Five partial counterexamples characterised; PMC11435656 and ActiveInspect were keyword-scanned, so some fields remain Unknown. |
| Q4. Is the gap precise? | **satisfied**: Narrowed wording fixes platform (smartphone), task (visual inspection) and trigger (device/resource state). | **satisfied**: Narrowed wording requires joint energy and thermal measurement of resource-adaptive smartphone inspection. | **satisfied**: Narrowed wording names five components. |
| Q5. Is the research question testable? | **satisfied**: Candidate RQs compare resource-driven, content-driven and static policies on measurable outcomes. | **satisfied**: Candidate RQs test whether energy-only and thermal-aware evaluation lead to different conclusions; falsifiable. | **partially_satisfied**: Testable with a rig or scripted recapture; user-in-the-loop recapture adds variability. |
| Q6. Is the dataset feasible? | **partially_satisfied**: Public optical datasets exist in the repository record; no smartphone-captured inspection dataset is identified; licences/access not verified. | **partially_satisfied**: Energy/thermal behaviour is workload-driven, so public datasets can drive the workload; inspection accuracy on phone-captured data needs custom capture. | **partially_satisfied**: Multi-view datasets exist (Real-IAD, MANTA, P037/P038); smartphone recapture or multi-view data are not identified and would need custom acquisition. |
| Q7. Is smartphone experimentation feasible? | **partially_satisfied**: Android exposes thermal/battery state (Assumption to verify on the target device); device availability is an Assumption. | **partially_satisfied**: BatteryManager-based logging is shown on an unrooted phone (arXiv 2603.26603, LLM workload); accuracy versus an external meter is unverified for the target device. | **partially_satisfied**: Same device Assumptions as GC-01, plus an acquisition-feedback loop (app UI or rig). |
| Q8. Can the contribution be distinguished from prior integration? | **unresolved**: Resource-driven adaptation mechanisms exist on smartphones outside inspection (P029, P033, P034); whether inspection changes the problem is a Hypothesis. | **unresolved**: Risk that the contribution is primarily benchmarking unless the joint measurement changes a design conclusion (Hypothesis). | **partially_satisfied** (Step 9.9B: conditionally distinct): mechanisms exist and integration alone is insufficient; the distinctive element is the testable recovery-under-downgrade and calibration-shift question. |
| Q9. Can the study produce quantitative evidence? | **satisfied**: Accuracy, latency, throttling and resource traces are quantitative. | **satisfied**: Energy per inspected item, temperature trajectories and time-to-throttling are quantitative. | **satisfied**: Recall at fixed review rate, referral/recapture rates, calibration error, latency and resource use are quantitative. |
| Q10. Could additional literature reasonably overturn the candidate? | **unresolved**: Plausible: generic mobile adaptive-inference literature is large and indexed databases were not searched. | **unresolved**: Plausible: mobile energy/thermal measurement studies are numerous; an inspection-specific study could exist in unsearched venues. | **partially_satisfied** (Step 9.9B: moderate): a single study combining smartphone optical inspection, device-state-driven configuration changes and confidence-triggered recapture/escalation would overturn it; P001, AIVD and Choi 2026 unresolved. |

**Gate outcome (Fact about this assessment).**
- No candidate satisfies all ten gate questions without qualification.
- In Phase A, Q2 (Unknown burden), Q8 (contribution distinguishable from prior integration) and Q10 (risk of being overturned by more literature) were `unresolved` for all three. Step 9.9B closed them for GC-03 only (now `partially_satisfied`, with the limitations stated in the GC-03 Evidence Closure Status section). They remain `unresolved` for GC-01 and GC-02.
- These are documented reasons for not making a selection in Phase A. They are **not** grounds for eliminating any candidate. No candidate is eliminated because it is harder, and none is preferred because it aligns with the current PocketInspect architecture.

**Decisions for the researcher.**
1. Whether the corpus-bounded evidence and the `unresolved` gate items are acceptable, or whether the evidence in §15 must be obtained first.
2. Which candidate, if any, to select. A combination or re-scoping is also possible (e.g. GC-01 as a foundation with GC-02 or GC-03 elements); any such combination would need its own gate check.
3. What would make the contribution distinguishable (§13) for the chosen candidate.

**Selection state.** `selection_status: researcher_approval_required`; `selected_candidate: null` (see `configs/gap_selection.yaml`). The approval document is [`research_gap_approval.md`](research_gap_approval.md); its decision field reads "DECISION: PENDING EXPLICIT RESEARCHER APPROVAL". No candidate was ranked or selected. No final gap was created, and `research_gap.md` does not exist.

Step 9.9 Phase A is complete. Final research-gap selection requires explicit researcher approval and is not automatically performed by this workflow.
