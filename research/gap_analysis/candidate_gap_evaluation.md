# Step 9.8 Candidate-Gap Evaluation

**Status.** Pending researcher review.

**Scope.** This document evaluates the three Step 9.7 candidate gaps against an explicit framework and against targeted searches designed to disprove them.

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

Step 9.7 produced three evidence-supported candidate gaps. Each is a corpus-bounded observation, not a claim about the wider literature:

| ID | Candidate (verbatim from Step 9.7) |
| :-- | :-- |
| GC-01 | Limited representation of runtime resource-aware/adaptive inference in smartphone visual inspection within the reviewed corpus |
| GC-02 | Limited direct evaluation of energy/thermal behaviour in smartphone or edge visual inspection within the reviewed corpus |
| GC-03 | Limited evidence of integrated smartphone visual inspection combining runtime adaptation with confidence-aware downstream decisions within the reviewed corpus |

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

These follow [`research/literature/README.md`](../literature/README.md):
- **`adaptive_inference`.** Cascades and per-sample dynamic offloading count as `adaptive_inference = Yes`.
- **`resource_awareness`.** Resource-driven *deployment-time* choices count as `resource_awareness = Yes`. Such cases are labelled "deployment time only" in the notes, because GC-01 concerns *runtime* resource-driven adaptation.
- **`confidence_gating = Yes`** requires that a score described as confidence triggers an action. Anomaly or reconstruction scores and learned selection policies are left `Unknown`.
- **Phone as product.** "Smartphone" means the platform running inference. Papers where the phone is the inspected product are false positives. Their `smartphone` value is left `Unknown`, not `No`, when the inference platform is not stated.

## 4. GC-01 evaluation

**Candidate.** Limited representation of runtime resource-aware/adaptive inference in smartphone visual inspection within the reviewed corpus.

- **Corpus evidence (Fact).**
  - 27 in-scope papers. `resource_awareness` and `adaptive_inference` are each Yes 0 / No 4 / Unknown 23; 22 of 27 are unresolved for the combination.
  - P011, the only full-text-verified smartphone visual-inspection paper, is No on both runtime fields.
  - Smartphone runtime adaptation appears in the corpus only outside the visual-inspection scope (P029, P031, P033, P034).
- **Targeted searches (Fact).** S01–S08 and S17. No full counterexample. Two verified partial counterexamples show runtime adaptation in **edge** visual inspection:
  - **arXiv 2608.14727.** Two-stage fabric-defect cascade on a Jetson Nano. Stage 2 runs only on frames flagged by Stage 1, which is input-dependent computation. The adaptation is content-driven; the only resource-driven decision is deployment-time (FP16 forced by memory).
  - **PMC11435656** (Sensors 24(18):5921). PCB inspection on Raspberry Pi 4 edge devices. Low-confidence samples are escalated to a high-precision cloud model, which is dynamic offloading per sample. It is confidence-driven, not resource-driven.
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

- **Effect of Step 9.8 on the wording (Fact + interpretation).** The searches did not overturn GC-01. They do show that runtime adaptation in visual inspection exists on edge platforms outside the corpus. The candidate is therefore informative only in its smartphone-specific and resource-driven form.

## 5. GC-02 evaluation

**Candidate.** Limited direct evaluation of energy/thermal behaviour in smartphone or edge visual inspection within the reviewed corpus.

- **Corpus evidence (Fact).**
  - 27 in-scope papers. `energy_evaluation` and `thermal_evaluation` are each Yes 0 / No 4 / Unknown 23. The four No values (P011, P015, P016, P020) are full-text-verified.
  - Every core paper coded Yes for energy or thermal evaluation is outside the visual-inspection scope.
  - P007 (edge visual inspection) is unresolved.
- **Targeted searches (Fact).** S09–S17. No full counterexample.
  - **arXiv 2603.16451 (TinyGLASS)** is a verified **partial** counterexample. It runs in-sensor industrial visual anomaly detection on a Sony IMX500 attached to a Raspberry Pi 5 and reports 4.0 mJ per inference and 470 GMAC/J. It reports no thermal results and does not use a smartphone. How the energy figure was obtained is not described in detail.
  - Six further edge or edge-oriented visual-inspection papers were read and report **no** energy or thermal results: arXiv 2603.20288, 2410.11591, 2606.07659, 2512.13497 and 2608.14727, and PMC11435656.
  - arXiv 2309.00022 measures energy with an external power meter on an edge camera device, but its task is pedestrian detection.
  - **Potential:** Electronics 15(17):3915; the FOMO/Edge Impulse solar-panel paper; P007.
- **Assessment by dimension.**

  | Dimension | Assessment | Confidence |
  | :-- | :-- | :-- |
  | Literature evidence strength | supports_candidate | low |
  | Unknown burden | weakens_candidate | moderate |
  | Counterexample risk | weakens_candidate | moderate |
  | PocketInspect alignment | supports_candidate | high |
  | Research feasibility | feasible_with_conditions | moderate |
  | Smartphone measurability | feasible_with_conditions | moderate |
  | Dataset feasibility | feasible | moderate |
  | Experimental feasibility | feasible_with_conditions | moderate |
  | Baseline availability | feasible | moderate |
  | Ablation potential | feasible | moderate |
  | Quantitative evaluation potential | feasible | moderate |
  | Engineering complexity | feasible | moderate |
  | Contribution depth | mixed | low |
  | Publication relevance | feasible | moderate |

- **Effect of Step 9.8 on the wording (Fact + interpretation).**
  - TinyGLASS shows that energy evaluation of an edge visual-inspection system exists outside the corpus. The "edge" and "energy" parts of the GC-02 wording are therefore weaker than the "smartphone" and "thermal" parts.
  - No thermal evaluation of a smartphone or edge visual-inspection system was found in these searches. That is a search result, not evidence of absence.

## 6. GC-03 evaluation

**Candidate.** Limited evidence of integrated smartphone visual inspection combining runtime adaptation with confidence-aware downstream decisions within the reviewed corpus.

- **Corpus evidence (Fact).**
  - No in-scope paper meets three of the four components (smartphone; visual inspection; runtime adaptation; confidence-aware downstream decision).
  - `confidence_gating` is Yes 1 (P016, edge, not smartphone) / No 2 / Unknown 24.
  - P011 has smartphone and visual inspection, but No for adaptation and gating.
- **Targeted searches (Fact).** S18–S27. No full counterexample.
  - **PMC11435656** meets three of the four components outside the corpus. Visual inspection is Yes; a per-sample runtime change of the computation path is Yes; confidence-triggered escalation to the cloud is Yes. The smartphone component is absent: it runs on Raspberry Pi 4. The adaptation is triggered by confidence, not by resources. Its full text was keyword-scanned, not read end to end.
  - **ActiveInspect** (Sensors 26(15):4932) selects additional views or modalities when the evidence is ambiguous, with sample-adaptive termination. It runs a 7B VLM on A100 GPUs over a pre-acquired pool, and a learned policy (not a confidence threshold) drives it.
  - **arXiv 2608.14727** is an edge cascade that serves as AI-assisted triage. Its trigger is a reconstruction-error score that is not described as confidence.
  - **Potential:** arXiv 2608.21967 (uncertainty-based human referral; online deferral not yet evaluated; platform not stated) and P001.
- **Assessment by dimension.**

  | Dimension | Assessment | Confidence |
  | :-- | :-- | :-- |
  | Literature evidence strength | supports_candidate | low |
  | Unknown burden | weakens_candidate | moderate |
  | Counterexample risk | weakens_candidate | moderate |
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

- **Effect of Step 9.8 on the wording (Fact + interpretation).**
  - Outside the corpus, edge systems already integrate per-sample runtime adaptation with confidence-triggered downstream decisions (PMC11435656).
  - What remains unmatched in the evidence examined is the **smartphone** platform combined with **resource-driven** adaptation and a confidence-triggered action such as recapture, an additional view or referral.

## 7. Counterexample analysis

| Strength | GC-01 | GC-02 | GC-03 |
| :-- | :-- | :-- | :-- |
| Full | None found | None found | None found |
| Partial (corpus) | P011 (no runtime component); P029, P031, P033, P034 (outside visual-inspection scope) | None in corpus | P011 (no adaptation or gating); P016 (edge; gating only) |
| Partial (external, verified) | arXiv 2608.14727; PMC11435656 | arXiv 2603.16451 (TinyGLASS) | PMC11435656; ActiveInspect; arXiv 2608.14727 |
| Potential (unresolved) | P001; Electronics 15(17):3915 | P007; Electronics 15(17):3915; FOMO/Edge Impulse paper | P001; arXiv 2608.21967 |
| Notable non-counterexamples | arXiv 2603.20288 (static); PMC12074420 (not inspection); smartphone-as-product screen papers | arXiv 2603.20288, 2410.11591, 2606.07659, 2512.13497 (no energy or thermal results); arXiv 2309.00022 (energy measured, not inspection); Corun (desktop GPU) | arXiv 2608.30997 and PMC12716720 (phone as product) |

**Evidence level of the important counterexamples (Fact).**

| Paper | Evidence level | Notes |
| :-- | :-- | :-- |
| arXiv 2603.16451 (TinyGLASS) | `verified_full_text` | arXiv v3, accepted at AICAS 2026 |
| arXiv 2608.14727 | `verified_full_text` | |
| PMC11435656 | `verified_full_text` | Keyword scan of the PMC full text; `resource_awareness` left Unknown |
| ActiveInspect (PMC13468834) | `verified_full_text` | Keyword scan; `confidence_gating` and `resource_awareness` left Unknown |
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
- **Coding judgement (Assumption).** Counting a cascade or per-sample offloading as `adaptive_inference = Yes` follows the README table ("Input-dependent computation … cascades"; dynamic offloading, Decision 4). A researcher may read GC-01's "runtime resource-aware/adaptive" more narrowly as *resource-driven*. In that case 2608.14727 and PMC11435656 become weaker partial counterexamples for GC-01.

## 9. Dataset and experimental feasibility

- **Public optical data (Fact).** Verified papers use MVTec AD and VisA (2603.20288, 2410.11591, 2603.16451), PCB defect sets (PMC11435656), Real-IAD multi-view data (ActiveInspect) and 3D-print datasets (P015, P016).
- **Phone-specific data (Assumption).** None of these was captured on a smartphone. A PocketInspect study would need at least a small phone-captured set for the target parts. GC-03 additionally needs multi-view or recapture sequences.
- **Measurement (Fact + Assumption).**
  - *Fact:* verified work measures energy with an external power meter (2309.00022) and thermal behaviour on phones (P031).
  - *Assumption:* Android exposes thermal status and battery counters with device-dependent accuracy.
  - GC-02 is the most measurement-centred candidate; GC-03 is the most data-demanding.
- **Experimental control (Assumption).** All three are sensitive to ambient temperature, background load and OS throttling policy. arXiv 2608.14727 shows that the data path (image decode) can dominate wall time on an edge device, so a live camera pipeline should be measured, not only replayed images.

## 10. Research contribution considerations

All statements below are **Hypotheses** or **Proposed ideas**, not findings.

- **GC-01.** Could support a measured study of resource-driven runtime adaptation for a smartphone inspection task against a static baseline. The verified outside-scope mechanisms (P029, P033, P034) mean that any contribution would concern the inspection setting and its evaluation, not the adaptation mechanism itself.
- **GC-02.** Could support an empirical characterisation of energy and thermal behaviour of smartphone inspection workloads. Whether inspection workloads behave differently from general vision workloads is untested.
- **GC-03.** Could support an integration study with explicit sub-questions, e.g. whether confidence-triggered recapture compensates for accuracy lost under resource-driven downgrades. Edge integration of adaptation with confidence-triggered escalation already exists (PMC11435656).
- **Overlap (Fact).** GC-03 contains GC-01's runtime-adaptation component. Thermal or energy signals are among GC-01's resource inputs, which links GC-01 to GC-02. The candidates are not independent.

## 11. Candidate-by-candidate strengths

- **GC-01.**
  - Four full-text-verified No records, plus a verified smartphone visual-inspection paper (P011) without runtime adaptation.
  - No full counterexample in 9 targeted searches.
  - Direct mapping to `adaptation/` and `monitoring/`.
  - Natural static baseline.
- **GC-02.**
  - Four full-text-verified No records.
  - Six externally verified edge visual-inspection papers without energy or thermal results.
  - No thermal counterexample found.
  - Lowest engineering demand: a measurement harness and no controller.
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
  - Verified edge visual-inspection papers already adapt computation at runtime (content-driven), which narrows the candidate to smartphone and resource-driven forms.
- **GC-02.**
  - High Unknown burden (23/27).
  - A verified partial counterexample (TinyGLASS) reports energy for edge visual inspection.
  - The candidate's "edge" scope is broad, which raises counterexample risk.
  - A measurement study alone may be judged an evaluation rather than a method contribution.
- **GC-03.**
  - The most Unknown-dependent candidate (`confidence_gating` Unknown 24/27).
  - A verified edge system meets three of the four components (PMC11435656).
  - Highest engineering complexity and the most demanding data needs (multi-view or recapture).
  - Shares GC-01's thin smartphone evidence.

## 13. Evidence that could overturn each candidate

- **GC-01.** Any of the following:
  - a verified paper (in or outside the corpus) running smartphone-based optical inspection with resource-driven runtime adaptation (model, sub-network, resolution or partition switching driven by battery, thermal or load state);
  - P001's full text showing such adaptation;
  - full-text resolution of the in-scope Unknowns to Yes.
- **GC-02.** Any of the following:
  - a verified paper reporting energy or power **and/or** device thermal behaviour for a smartphone or edge optical inspection system;
  - the full texts of P007, Electronics 15(17):3915 or the FOMO/Edge Impulse paper reporting energy or thermal results.

  Under the current wording, TinyGLASS already partly does this for energy on an edge platform.
- **GC-03.** Any of the following:
  - a verified smartphone inspection system in which runtime adaptation and a confidence-triggered downstream action (recapture, additional view, referral, fallback) are both implemented and evaluated;
  - a smartphone deployment of the PMC11435656-style confidence-triggered escalation combined with runtime adaptation.

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
- **Definitional choices requiring researcher confirmation (Assumption).**
  - Whether content-driven cascades count against GC-01.
  - Whether a learned view-selection policy counts as a confidence-aware decision for GC-03.
  - Whether "edge" in GC-02 should include in-sensor processors.

## 15. Researcher decision required

The researcher is asked to:

1. **Review the evidence.** Confirm or correct the counterexample classifications in `counterexample_candidates.csv`, in particular:
   - TinyGLASS (GC-02, partial);
   - PMC11435656 (GC-01 and GC-03, partial);
   - ActiveInspect (GC-03, partial).
2. **Decide on wording.** Decide whether each candidate's wording should be kept, narrowed (e.g. smartphone-specific; resource-driven; thermal-specific) or rejected in light of §4–§6.
3. **Decide on unresolved items.** Decide whether the unresolved sources in §14 should be obtained before any selection.
4. **Decide on definitions.** Decide the open definitional questions in §8 and §14.

No candidate is ranked. No final research gap is selected, and `research_gap.md` has not been created. Novelty is not claimed for any candidate.

Final research-gap selection remains a researcher decision and is outside Step 9.8.
