# Step 9.8 Candidate-Gap Evaluation

**Status.** Pending researcher review. Revised by the Step 9.8 controlled methodology correction (§3.4): four partial counterexamples confirmed, three operational definitions formalised, and the candidate wording narrowed.

**Scope.** This document evaluates the three candidate gaps against an explicit framework and against targeted searches designed to disprove them. The candidates remain unordered, unranked, unselected, corpus-bounded and provisional.

**What it does not do.**
- It does not select the final research gap.
- It does not rank, score or weight the candidates.
- It makes no novelty claim.

**Companion files.**
- [`counterexample_candidates.csv`](counterexample_candidates.csv): every paper assessed as a possible counterexample.
- [`targeted_search_log.md`](targeted_search_log.md): every search, with counts and limitations.
- [`candidate_gap_matrix.csv`](candidate_gap_matrix.csv): one row per candidate × criterion.
- [`../../configs/gap_evaluation.yaml`](../../configs/gap_evaluation.yaml): the framework definitions and guard-rails.

**Epistemic labels** (as in [`RESEARCH_RULES.md`](../../RESEARCH_RULES.md)): **Fact** (verified from a source read in this step or the frozen corpus), **Assumption**, **Hypothesis**, **Proposed idea**.

---

## 1. Purpose

Step 9.7 produced three evidence-supported candidate gaps. Each is a corpus-bounded observation, not a claim about the wider literature. After the counterexample search, the researcher-approved correction narrowed each wording so that no candidate is broader than the evidence supports.

| ID | Current (narrowed) wording | Step 9.7 wording (superseded; kept for traceability) |
| :-- | :-- | :-- |
| GC-01 | Limited evidence of resource-driven runtime adaptation for visual inspection specifically on resource-constrained smartphones within the reviewed corpus. | Limited representation of runtime resource-aware/adaptive inference in smartphone visual inspection within the reviewed corpus |
| GC-02 | Limited direct joint evaluation of energy and thermal behavior for resource-adaptive visual inspection on resource-constrained smartphones within the reviewed corpus. | Limited direct evaluation of energy/thermal behaviour in smartphone or edge visual inspection within the reviewed corpus |
| GC-03 | Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus. | Limited evidence of integrated smartphone visual inspection combining runtime adaptation with confidence-aware downstream decisions within the reviewed corpus |

The Step 9.7 artefacts (`configs/gap_analysis.yaml`, `gap_candidates.md`, `gap_matrix.csv`) keep the original wording as the historical record. They are not rewritten by this correction.

Step 9.8 asks, for each candidate:
1. How strong is the corpus evidence behind it?
2. What would overturn it, and did a deliberate search for counterexamples find any?
3. What would studying it involve (data, measurement, baselines, engineering)?

The answers are recorded per candidate. They are not combined into a ranking.

## 2. Frozen corpus boundary

- **Fact.** [`research/literature/papers.csv`](../literature/papers.csv) is frozen: 54 records, 31 columns, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. This step did not modify it.
- **Fact.** The analysis population is the Step 9.7 core subset of 46 records. It excludes:
  - P002 and P013 (peripheral, by researcher approval);
  - the six survey or review records P010, P024, P026, P035, P036 and P052.

  The visual-inspection scope is the researcher-approved `visual_inspection_scope` (Yes 20, No 19, Unknown 7). In-scope means Yes or Unknown, which gives 27 papers.
- **Fact.** Papers found by the targeted searches were **not** added to `papers.csv`. Their codings are kept in `counterexample_candidates.csv` only. Corpus records listed there (P001, P007, P011, P016, P029, P031, P033, P034) reproduce their existing coded values unchanged.
- **Rule.** `Unknown` is never converted to `No`. External papers were coded with the field definitions in [`research/literature/README.md`](../literature/README.md). Where a source was only scanned, a field is left `Unknown` unless the scan gives explicit evidence.

## 3. Evaluation methodology

### 3.1 Process

1. **Corpus evidence.** Re-read the Step 9.7 per-field counts for each candidate inside the 27-paper in-scope set.
2. **Targeted disproof searches.** These were run on 2026-10-05:
   - 8 queries per candidate, as specified for Step 9.8 (24 web searches);
   - 2 supplementary alphaXiv discovery searches;
   - 1 bibliographic lookup.

   Every plausible hit was followed to the best available evidence level: full text via the alphaXiv reader or PubMed Central, then abstract, then search snippet. Counts and limitations are in `targeted_search_log.md`.
3. **Counterexample classification.** Each hit relevant to a candidate is labelled:
   - `full`: meets every component;
   - `partial`: meets some components with verified evidence;
   - `potential`: key components Unknown;
   - `not_counterexample`.
4. **Framework evaluation.** Each candidate is assessed on 14 dimensions (§3.2). Assessments are qualitative labels (`supports_candidate`, `weakens_candidate`, `mixed`, `unresolved`, `feasible`, `feasible_with_conditions`, `difficult`, `not_applicable`) with a confidence label (`low`, `moderate`, `high`). No numerical score, weight or aggregate is used.

### 3.2 Evaluation framework

The same definitions are stored in `configs/gap_evaluation.yaml`.

| Dimension | Evidence required | Strong evidence | Weak evidence | Disqualifies or weakens a candidate |
| :-- | :-- | :-- | :-- | :-- |
| 1. Literature evidence strength | Corpus Yes/No/Unknown counts for the candidate's fields within the visual-inspection scope, with the evidence level behind each value | Most in-scope values are full-text-verified No for the missing component, and each component is present in verified Yes records | Values are mostly Unknown or abstract-level; the observation rests on a few verified records | Verified in-scope Yes for every component (a full counterexample), or Unknown so dominant that the observation is a coding artefact |
| 2. Unknown burden | Share of in-scope records Unknown for the candidate's fields, and whether full text could resolve them | Few Unknowns, or Unknowns confined to records whose full text was checked | Unknowns dominate and are abstract-level | Any Unknown record that, if resolved to Yes, would make a full counterexample |
| 3. Counterexample risk | Results of targeted disproof searches, with evidence levels | No full counterexample; partial ones are verified and differ in a named component | Searches narrow or access-limited; potential counterexamples unresolved | A verified full counterexample, or partial ones that differ only in a minor component |
| 4. Direct PocketInspect alignment | Mapping of components to modules and phases in `PROJECT_SPEC.md` | Every component maps to a specified module and phase | Only some components map, or they map to optional phases | Requires capabilities outside the project scope |
| 5. Research feasibility | Whether the question can be answered within project resources (no heavy training without approval; smartphone hardware) | Can be studied with available devices, public data and lightweight models | Depends on unconfirmed hardware, data or instrumentation | Requires resources the project cannot obtain |
| 6. Smartphone measurability | Whether the outcome variables can be measured on an Android phone with documented instruments or APIs | Outcomes measurable with standard Android facilities or instruments used in the literature | Depends on vendor counters of uncertain accuracy | Key outcomes not measurable on the device |
| 7. Dataset feasibility | Public optical inspection datasets, and the need for project-captured data | Public datasets cover the components; gaps can be captured with a phone | The required data (multi-view, recapture sequences) must be collected from scratch | No feasible data source for an essential component |
| 8. Experimental feasibility | Whether controlled experiments can be designed and repeated | Controlled conditions and repetitions are practical | Sensitive to uncontrolled factors (ambient temperature, background load, handling) | No reproducible protocol possible |
| 9. Baseline availability | Static, non-adaptive or non-gated baselines, and published comparators | Trivial static baselines, and published comparators exist | Only self-defined baselines | No meaningful baseline |
| 10. Ablation potential | Whether components can be removed or varied to attribute effects | Each component can be switched off independently | Components entangled | No component can be isolated |
| 11. Quantitative evaluation potential | Availability of quantitative outcomes (accuracy, latency, energy, temperature, referral rate) | Several standard, reproducible measures apply | Ad hoc or noisy measures | Only qualitative outcomes |
| 12. Expected engineering complexity | Components to build, relative to the project plan | Builds on planned components | Several new subsystems | Beyond the project timeline |
| 13. Potential contribution depth | Kind of contribution supported (measurement study, method, integration), stated without novelty claims | A clearly defined, testable question with measurable outcomes | Mainly an engineering integration or a single measurement | The question is already answered by verified literature |
| 14. Publication relevance | Venues where the verified related work appears | Established venues whose scope fits | Relies on preprints or grey literature | No identifiable venue |

### 3.3 Coding conventions used for external papers

These follow [`research/literature/README.md`](../literature/README.md), as refined by the operational definitions in §3.4:
- **`adaptive_inference`.** Cascades and per-sample dynamic offloading count as `adaptive_inference = Yes` (Decision A).
- **`resource_awareness`.** Yes only when device/resource state drives the adaptation (Decision A). Deployment-time choices made to fit a device budget are recorded in the notes but are not coded Yes.
- **`confidence_gating = Yes`** requires that confidence, uncertainty or prediction quality explicitly triggers an action (Decision B). Anomaly or reconstruction scores not described as confidence, and learned selection policies whose use of such a signal is not established, are left `Unknown`.
- **Platform.** "Smartphone" means the platform running inference. In-sensor processors count as edge devices, not smartphones (Decision C). Papers where the phone is the inspected product are false positives. Their `smartphone` value is left `Unknown`, not `No`, when the inference platform is not stated.

### 3.4 Controlled methodology correction (researcher-approved)

**Operational definitions.** These are stored in `configs/gap_evaluation.yaml` (`operational_definitions`) and implemented as rule functions in `src/literature/gap_evaluation.py`. They govern the coding of external papers in `counterexample_candidates.csv` only; `papers.csv` is not recoded.

- **Decision A: content-driven cascades.**
  - Content-driven cascades **count as adaptive inference**. If the executed computational path, model, cascade stage, depth, width or inference configuration changes at runtime based on input content or scene complexity, then `adaptive_inference = Yes`.
  - `resource_awareness = Yes` **only** when device/resource state (battery, temperature, CPU/RAM, memory, compute availability or another device-resource condition) actually drives the adaptation.
  - Content-driven adaptation alone is therefore `adaptive_inference = Yes`, and `resource_awareness = No` unless resource-driven adaptation is separately demonstrated (`Unknown` where the source does not establish it).
  - Example: image → complexity analysis → easy image to a lightweight model, hard image to a heavyweight model. This is adaptive inference, but not resource-aware inference.
- **Decision B: learned view-selection policies.**
  - A learned view-selection policy does **not** automatically count as confidence gating.
  - It counts as a confidence-aware downstream decision only when confidence, uncertainty, prediction quality or an equivalent inspection-quality signal explicitly informs or triggers the action.
  - Qualifies: prediction → confidence/uncertainty → low confidence → select additional view → re-inference.
  - Does not qualify on its own: image → learned policy → choose the next camera position.
- **Decision C: in-sensor processors.**
  - For GC-02, in-sensor processors count as **edge computing** when meaningful computation occurs locally at or immediately adjacent to the sensing source (`edge_device = Yes`).
  - In-sensor processing is **not** smartphone evidence (`smartphone = No`) unless the actual computing platform is a smartphone.

**Confirmed partial counterexamples.** All four stay `partial`; none is upgraded to `full`, and their evidence levels are unchanged.

| Paper | Candidate(s) | Established | Not established |
| :-- | :-- | :-- | :-- |
| arXiv 2603.16451 (TinyGLASS) | GC-02 | Edge visual inspection (in-sensor; Decision C); energy result reported | Thermal evaluation (No); smartphone (No); joint smartphone energy + thermal evaluation; resource-adaptive smartphone inspection |
| PMC11435656 | GC-01, GC-03 | Edge visual inspection; runtime per-sample adaptation; confidence-triggered downstream handling | Smartphone (No); resource-driven adaptation (`resource_awareness` Unknown) |
| ActiveInspect (doi 10.3390/s26154932) | GC-03 | Learned view selection / additional-view decisions; runs on A100 GPUs | Smartphone or resource-constrained platform (No); confidence gating (Unknown under Decision B); resource awareness (Unknown) |
| arXiv 2608.14727 | GC-01, GC-03 | Visual inspection; content-driven cascade (`adaptive_inference` Yes); edge deployment (Jetson Nano) | Resource-driven adaptation (`resource_awareness` No under Decision A); smartphone (No); confidence gating (Unknown) |

**Recoding of external rows (documented, not silent).** Applying Decision A changed `resource_awareness` from Yes to No in `counterexample_candidates.csv` for four external papers, each read in full text:
- arXiv 2608.14727 (all three rows): the cascade is content-driven; the FP16 choice was a deployment-time memory fit.
- arXiv 2603.16451 (TinyGLASS): static model; fitting the 8 MB sensor memory is a deployment-time choice.
- arXiv 2309.00022 (both rows): operation modes switch on the number of pedestrians detected (content/workload-driven).
- arXiv 2505.07119: pipeline chosen under budgets at design time; runtime adaptation is future work.

No `Unknown` value was converted to `No`, no corpus record was changed, and no evidence level was changed.

**Matrix assessments revised with the narrowing.** The *counterexample risk* rows for GC-02 and GC-03 changed from `weakens_candidate` to `mixed`. The confirmed partial counterexamples still weaken the Step 9.7 (broad) wording, and that is why the wording was narrowed. Against the narrowed wording, they are close neighbours that do not meet it. This revision applies the same rule to all three candidates (GC-01 was already `mixed`).

## 4. GC-01 evaluation

**Candidate.** Limited evidence of resource-driven runtime adaptation for visual inspection specifically on resource-constrained smartphones within the reviewed corpus.

**Not claimed.** That adaptive inference is generally missing; that adaptive inference in edge visual inspection is missing; that content-driven cascades are missing. The candidate concerns visual inspection, on a smartphone platform, in a resource-constrained setting, with resource-driven runtime adaptation. It remains corpus-bounded.

- **Corpus evidence (Fact).**
  - 27 in-scope papers. `resource_awareness` and `adaptive_inference` are each Yes 0 / No 4 / Unknown 23; 22 of 27 are unresolved for the combination.
  - P011, the only full-text-verified smartphone visual-inspection paper, is No on both runtime fields.
  - Smartphone runtime adaptation appears in the corpus only outside the visual-inspection scope (P029, P031, P033, P034).
- **Targeted searches (Fact).** S01–S08 and S17. No full counterexample. Two researcher-confirmed partial counterexamples show adaptive inference in **edge** visual inspection:
  - **arXiv 2608.14727.** Two-stage fabric-defect cascade on a Jetson Nano. Stage 2 runs only on frames flagged by Stage 1, which is a content-driven cascade: `adaptive_inference` Yes and `resource_awareness` No (Decision A). The FP16 choice forced by memory is a deployment-time decision.
  - **PMC11435656** (Sensors 24(18):5921). PCB inspection on Raspberry Pi 4 edge devices. Low-confidence samples are escalated to a high-precision cloud model, which is dynamic offloading per sample. The trigger is confidence; resource-driven adaptation is not established (`resource_awareness` Unknown).
  - **Potential:** Electronics 15(17):3915 (snippet only).
- **Assessment by dimension** (full rows in `candidate_gap_matrix.csv`).

  | Dimension | Assessment | Confidence |
  | :-- | :-- | :-- |
  | Literature evidence strength | supports_candidate | low |
  | Unknown burden | weakens_candidate | moderate |
  | Counterexample risk | mixed | low |
  | PocketInspect alignment | supports_candidate | high |
  | Research feasibility | feasible_with_conditions | moderate |
  | Smartphone measurability | feasible | moderate |
  | Dataset feasibility | feasible_with_conditions | moderate |
  | Experimental feasibility | feasible_with_conditions | moderate |
  | Baseline availability | feasible | moderate |
  | Ablation potential | feasible | moderate |
  | Quantitative evaluation potential | feasible | moderate |
  | Engineering complexity | feasible_with_conditions | moderate |
  | Contribution depth | mixed | low |
  | Publication relevance | feasible | moderate |

- **Counterexample interpretation (observation, not a gap claim).** Adaptive inference exists in edge visual inspection, including content-driven cascades. What remains as the candidate is specifically resource-driven runtime adaptation on resource-constrained smartphones. The searches did not overturn this narrowed form.

## 5. GC-02 evaluation

**Candidate.** Limited direct joint evaluation of energy and thermal behavior for resource-adaptive visual inspection on resource-constrained smartphones within the reviewed corpus.

**Not claimed.** That edge energy evaluation is absent; that visual-inspection energy evaluation is absent; that energy evaluation is generally absent. TinyGLASS is an explicit partial counterexample. The candidate concerns direct measurement, of both energy **and** thermal behaviour, for resource-adaptive visual inspection, on resource-constrained smartphones.

- **Corpus evidence (Fact).**
  - 27 in-scope papers. `energy_evaluation` and `thermal_evaluation` are each Yes 0 / No 4 / Unknown 23. The four No values (P011, P015, P016, P020) are full-text-verified.
  - Every core paper coded Yes for energy or thermal evaluation is outside the visual-inspection scope, and none of them (P006, P028, P029, P030, P031, P032, P034) is coded Yes for both.
  - `adaptive_inference` and `resource_awareness` are each Yes 0 / No 4 / Unknown 23 in scope, so the resource-adaptive component is also unmatched in the corpus.
  - P007 (edge visual inspection) is unresolved.
- **Targeted searches (Fact).** S09–S17. No full counterexample.
  - **arXiv 2603.16451 (TinyGLASS)** is a researcher-confirmed **partial** counterexample. It runs in-sensor industrial visual anomaly detection on a Sony IMX500 attached to a Raspberry Pi 5 (edge, not smartphone, under Decision C) and reports 4.0 mJ per inference and 470 GMAC/J. It reports no thermal results and uses a static model. How the energy figure was obtained is not described in detail.
  - Six further edge or edge-oriented visual-inspection papers were read and report **no** energy or thermal results: arXiv 2603.20288, 2410.11591, 2606.07659, 2512.13497 and 2608.14727, and PMC11435656.
  - arXiv 2309.00022 measures energy with an external power meter on an edge camera device, but its task is pedestrian detection.
  - **Potential:** Electronics 15(17):3915; the FOMO/Edge Impulse solar-panel paper; P007.
- **Assessment by dimension.**

  | Dimension | Assessment | Confidence |
  | :-- | :-- | :-- |
  | Literature evidence strength | supports_candidate | low |
  | Unknown burden | weakens_candidate | moderate |
  | Counterexample risk | mixed | moderate |
  | PocketInspect alignment | supports_candidate | high |
  | Research feasibility | feasible_with_conditions | moderate |
  | Smartphone measurability | feasible_with_conditions | moderate |
  | Dataset feasibility | feasible | moderate |
  | Experimental feasibility | feasible_with_conditions | moderate |
  | Baseline availability | feasible | moderate |
  | Ablation potential | feasible | moderate |
  | Quantitative evaluation potential | feasible | moderate |
  | Engineering complexity | feasible_with_conditions | moderate |
  | Contribution depth | mixed | low |
  | Publication relevance | feasible | moderate |

- **Counterexample interpretation (observation, not a gap claim).**
  - Energy evaluation exists in at least one edge visual-inspection counterexample (TinyGLASS). What remains as the candidate is specifically joint energy + thermal evaluation of resource-adaptive smartphone visual inspection.
  - No thermal evaluation of a smartphone or edge visual-inspection system was found in these searches. That is a search result, not evidence of absence.
  - The searches were designed against the Step 9.7 wording; the joint, resource-adaptive form was not searched as one query.

## 6. GC-03 evaluation

**Candidate.** Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus.

**Not claimed.** That confidence-aware inspection is generally absent; that active view selection is absent; that adaptive visual inspection is absent; that edge systems do not combine adaptation and confidence-aware actions. PMC11435656 and ActiveInspect are explicit partial counterexamples. The candidate concerns the integration of (1) resource awareness, (2) a smartphone platform, (3) visual inspection, (4) runtime adaptation and (5) confidence-aware downstream verification.

- **Corpus evidence (Fact).**
  - No in-scope paper meets three of the four components (smartphone; visual inspection; runtime adaptation; confidence-aware downstream decision).
  - `confidence_gating` is Yes 1 (P016, edge, not smartphone) / No 2 / Unknown 24.
  - P011 has smartphone and visual inspection, but No for adaptation and gating.
- **Targeted searches (Fact).** S18–S27. No full counterexample.
  - **PMC11435656** (confirmed partial) meets visual inspection, runtime per-sample adaptation and confidence-triggered escalation to the cloud outside the corpus. The smartphone component is absent (Raspberry Pi 4), and resource awareness is not established (Unknown). Its full text was keyword-scanned, not read end to end.
  - **ActiveInspect** (Sensors 26(15):4932; confirmed partial) selects additional views or modalities with sample-adaptive termination. It runs a 7B VLM on A100 GPUs over a pre-acquired pool. Under Decision B, learned view selection alone is not confidence gating; the keyword scan did not establish that confidence drives the selection, so `confidence_gating` stays Unknown.
  - **arXiv 2608.14727** (confirmed partial) is an edge content-driven cascade serving as AI-assisted triage (`adaptive_inference` Yes, `resource_awareness` No). Its trigger is a reconstruction-error score that is not described as confidence.
  - **Potential:** arXiv 2608.21967 (uncertainty-based human referral; online deferral not yet evaluated; platform not stated) and P001.
- **Assessment by dimension.**

  | Dimension | Assessment | Confidence |
  | :-- | :-- | :-- |
  | Literature evidence strength | supports_candidate | low |
  | Unknown burden | weakens_candidate | moderate |
  | Counterexample risk | mixed | moderate |
  | PocketInspect alignment | supports_candidate | high |
  | Research feasibility | feasible_with_conditions | moderate |
  | Smartphone measurability | feasible_with_conditions | low |
  | Dataset feasibility | difficult | moderate |
  | Experimental feasibility | feasible_with_conditions | low |
  | Baseline availability | feasible | moderate |
  | Ablation potential | feasible | moderate |
  | Quantitative evaluation potential | feasible | moderate |
  | Engineering complexity | difficult | moderate |
  | Contribution depth | mixed | low |
  | Publication relevance | feasible | moderate |

- **Counterexample interpretation (observation, not a gap claim).** Edge systems already demonstrate combinations of adaptation, confidence-aware decisions and/or active view selection (PMC11435656, ActiveInspect, arXiv 2608.14727). What remains as the candidate is specifically their integrated, resource-aware smartphone visual-inspection realization.

## 7. Counterexample analysis

| Strength | GC-01 | GC-02 | GC-03 |
| :-- | :-- | :-- | :-- |
| Full | None found | None found | None found |
| Partial (corpus) | P011 (no runtime component); P029, P031, P033, P034 (outside visual-inspection scope) | None in corpus | P011 (no adaptation or gating); P016 (edge; gating only) |
| Partial (external, verified; researcher-confirmed) | arXiv 2608.14727; PMC11435656 | arXiv 2603.16451 (TinyGLASS) | PMC11435656; ActiveInspect; arXiv 2608.14727 |
| Potential (unresolved) | P001; Electronics 15(17):3915 | P007; Electronics 15(17):3915; FOMO/Edge Impulse paper | P001; arXiv 2608.21967 |
| Notable non-counterexamples | arXiv 2603.20288 (static); PMC12074420 (not inspection); smartphone-as-product screen papers | arXiv 2603.20288, 2410.11591, 2606.07659, 2512.13497 (no energy or thermal results); arXiv 2309.00022 (energy measured, not inspection); Corun (desktop GPU) | arXiv 2608.30997 and PMC12716720 (phone as product) |

**Evidence level of the important counterexamples (Fact).**

| Paper | Evidence level | Notes |
| :-- | :-- | :-- |
| arXiv 2603.16451 (TinyGLASS) | `verified_full_text` | arXiv v3, accepted at AICAS 2026; edge (in-sensor), not smartphone |
| arXiv 2608.14727 | `verified_full_text` | |
| PMC11435656 | `verified_full_text` | Keyword scan of the PMC full text; `resource_awareness` left Unknown |
| ActiveInspect (PMC13468834) | `verified_full_text` | Keyword scan; `confidence_gating` (Decision B) and `resource_awareness` left Unknown |
| arXiv 2608.21967 | `verified_full_text` | |
| Electronics 15(17):3915 | `search_snippet_only` | |
| FOMO/Edge Impulse paper | `unresolved` | |
| P001, P007 | `abstract_only` | Corpus records |

**False-positive patterns observed (Fact).**
- The smartphone is the inspected product (screen, cover glass, phone surface).
- Thermography, i.e. a thermal camera used as the inspection modality.
- "Energy-based" detection methods.
- "Adaptive" multi-scale feature modules.
- Vendor or blog pages.
- Search-engine summaries that mix sources. One attributed a latency figure that is in none of the papers checked; it was not used.

## 8. Unknown/evidence limitations

- **Corpus Unknowns (Fact).** Within the 27 in-scope papers, 23 are Unknown for each runtime field and for each of energy and thermal, and 24 are Unknown for `confidence_gating`. These are mostly abstract-level codings. Under the project rules they are **not** evidence of absence.
- **Unresolved records that could flip a candidate (Fact).**
  - P001 (smartphone; visual scope, runtime and gating fields Unknown) could become a GC-01 or GC-03 counterexample.
  - P007 (edge visual inspection; energy and thermal Unknown) could become a GC-02 counterexample.

  Neither full text was reachable in this environment.
- **Search limitations (Fact).**
  - One page (about 10 links) per web query.
  - English-only.
  - No Scopus, Web of Science, IEEE Xplore or ACM DL access.
  - Publisher pages (ACM, MDPI, Wiley, Frontiers, NCBI direct) were blocked or returned interstitials.
  - alphaXiv discovery covers arXiv only.
  - Several hits were judged by title or snippet alone (listed as unresolved in the search log).
- **Verification depth (Fact).** Some external papers were keyword-scanned rather than read end to end: PMC11435656, ActiveInspect, PMC12074420 and Corun. Fields that the scan could not establish were left Unknown.
- **Coding judgement (resolved).** The question of whether cascades and per-sample offloading count against GC-01 is settled by Decision A: they count as adaptive inference but not as resource-aware inference, and GC-01 is now worded as resource-driven adaptation. 2608.14727 and PMC11435656 therefore remain partial, not full, counterexamples.

## 9. Dataset and experimental feasibility

- **Public optical data (Fact).** Verified papers use MVTec AD and VisA (2603.20288, 2410.11591, 2603.16451), PCB defect sets (PMC11435656), Real-IAD multi-view data (ActiveInspect) and 3D-print datasets (P015, P016).
- **Phone-specific data (Assumption).** None of these was captured on a smartphone. A PocketInspect study would need at least a small phone-captured set for the target parts. GC-03 additionally needs multi-view or recapture sequences.
- **Measurement (Fact + Assumption).**
  - *Fact:* verified work measures energy with an external power meter (2309.00022) and thermal behaviour on phones (P031).
  - *Assumption:* Android exposes thermal status and battery counters with device-dependent accuracy.
  - GC-02 is the most measurement-centred candidate and, after narrowing, also needs a resource-adaptive workload; GC-03 is the most data-demanding.
- **Experimental control (Assumption).** All three are sensitive to ambient temperature, background load and OS throttling policy. arXiv 2608.14727 shows that the data path (image decode) can dominate wall time on an edge device, so a live camera pipeline should be measured, not only replayed images.

## 10. Research contribution considerations

All statements below are **Hypotheses** or **Proposed ideas**, not findings.

- **GC-01.** Could support a measured study of resource-driven runtime adaptation for a smartphone inspection task against a static baseline. The verified outside-scope mechanisms (P029, P033, P034) mean that any contribution would concern the inspection setting and its evaluation, not the adaptation mechanism itself.
- **GC-02.** Could support an empirical characterisation of joint energy and thermal behaviour of resource-adaptive smartphone inspection. Whether inspection workloads behave differently from general vision workloads is untested.
- **GC-03.** Could support an integration study with explicit sub-questions, e.g. whether confidence-triggered recapture compensates for accuracy lost under resource-driven downgrades. Edge integration of adaptation with confidence-triggered escalation already exists (PMC11435656).
- **Overlap (Fact).** GC-03 contains GC-01's runtime-adaptation component. After narrowing, GC-02 concerns resource-adaptive inspection, so it also depends on a GC-01-type mechanism; thermal and energy signals are among GC-01's resource inputs. The candidates are not independent.

## 11. Candidate-by-candidate strengths

- **GC-01.**
  - Four full-text-verified No records, plus a verified smartphone visual-inspection paper (P011) without runtime adaptation.
  - No full counterexample in 9 targeted searches.
  - Direct mapping to `adaptation/` and `monitoring/`.
  - Natural static baseline.
- **GC-02.**
  - Four full-text-verified No records.
  - Six externally verified edge visual-inspection papers without energy or thermal results.
  - No thermal counterexample found, and no core paper is coded Yes for both energy and thermal.
  - Workload-driven, so public datasets suffice for the energy/thermal part.
- **GC-03.**
  - No in-corpus paper meets three of the four components.
  - No full counterexample in 10 targeted searches (9 discovery searches and 1 verification lookup).
  - Mapping to `uncertainty/`, `adaptation/`, `quality/` and multi-view inspection in `PROJECT_SPEC.md`.
  - Natural factorial ablation.

## 12. Candidate-by-candidate weaknesses

- **GC-01.**
  - High Unknown burden (22/27 unresolved).
  - Rests on a single verified smartphone visual-inspection paper.
  - Verified edge visual-inspection papers already adapt computation at runtime (content-driven), so only the narrowed smartphone, resource-driven form remains.
- **GC-02.**
  - High Unknown burden (23/27).
  - A confirmed partial counterexample (TinyGLASS) reports energy for edge visual inspection.
  - After narrowing, it requires a resource-adaptive pipeline as well as a measurement harness, which raises engineering demand.
  - The narrowed (joint, resource-adaptive) form was not searched as one query.
  - A measurement study alone may be judged an evaluation rather than a method contribution.
- **GC-03.**
  - The most Unknown-dependent candidate (`confidence_gating` Unknown 24/27).
  - Confirmed edge systems already combine adaptation with confidence-aware decisions or active view selection (PMC11435656, ActiveInspect, arXiv 2608.14727).
  - Highest engineering complexity and the most demanding data needs (multi-view or recapture).
  - Shares GC-01's thin smartphone evidence.

## 13. Evidence that could overturn each candidate

- **GC-01.** Any of the following:
  - a verified paper (in or outside the corpus) running smartphone-based optical inspection with resource-driven runtime adaptation (model, sub-network, resolution or partition switching driven by battery, thermal or load state);
  - P001's full text showing such adaptation;
  - full-text resolution of the in-scope Unknowns to Yes.
- **GC-02.** Any of the following:
  - a verified paper directly measuring **both** energy and thermal behaviour of resource-adaptive optical inspection on a resource-constrained smartphone;
  - P001 or another unresolved smartphone record whose full text shows such a joint evaluation.

  Edge-only energy results (TinyGLASS) or the unresolved edge papers (P007, Electronics 15(17):3915, FOMO/Edge Impulse) would weaken the broad Step 9.7 wording but would not on their own overturn the narrowed candidate.
- **GC-03.** Any of the following:
  - a verified resource-aware smartphone inspection system in which runtime adaptation and a confidence-triggered downstream verification (recapture, additional view, referral, fallback) are both implemented and evaluated;
  - a smartphone deployment of PMC11435656-style confidence-triggered escalation combined with resource-driven runtime adaptation.

## 14. Remaining uncertainty

- **Corpus coding (Fact).** About 85% of the in-scope records are Unknown on the relevant fields, so the corpus observations remain weak for all three candidates.
- **Search coverage.**
  - *Fact:* coverage is partial (§8).
  - *Assumption:* indexed scholarly databases may contain counterexamples that web search and arXiv discovery did not surface.
- **Counterexample sources not resolved (Fact).** The following were not read in full or not opened:
  - P001 and P007;
  - Electronics 15(17):3915;
  - the FOMO/Edge Impulse paper;
  - the SPIE uncertainty-propagation paper;
  - the iieta surface-quality paper;
  - the mobile-inspection-robot paper;
  - the arXiv 2603.26603 on-device trade-off paper;
  - patents.
- **Definitional choices.** Resolved by Decisions A–C (§3.4). Remaining coding uncertainty concerns facts, not definitions:
  - whether ActiveInspect's step-level confidences drive its view selection (keyword scan only; Unknown);
  - whether PMC11435656 uses any device-resource signal (keyword scan only; Unknown);
  - how TinyGLASS obtained its energy figure.
- **Search alignment (Fact).** The targeted searches were designed against the Step 9.7 wording. No new search was run for the narrowed wording, as instructed.

## 15. Researcher decision required

The researcher is asked to:

Already decided by the researcher (recorded in §3.4): the four partial-counterexample classifications, Decisions A–C, and the narrowed wording of GC-01, GC-02 and GC-03.

Still open:

1. **Review the corrected evidence.** Check the documented `resource_awareness` recodings of external rows under Decision A (§3.4).
2. **Decide on unresolved items.** Decide whether the unresolved sources in §14 should be obtained, or a search aligned with the narrowed wording run, before any selection.
3. **Select or reject candidates.** This remains entirely with the researcher.

No candidate is ranked. No final research gap is selected, and `research_gap.md` has not been created. Novelty is not claimed for any candidate.

Final research-gap selection remains a researcher decision and is outside Step 9.8.
