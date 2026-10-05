# GC-03 Evidence Closure (Step 9.9B)

_2026-10-05, Claude Code, branch `claude/step-9-9b-gc03-evidence-closure` (from `origin/main` `f8e0d2e`). Status: **Pending researcher review**. Configuration: [`configs/gc03_evidence_closure.yaml`](../../configs/gc03_evidence_closure.yaml). Evidence rows: [`counterexample_candidates.csv`](counterexample_candidates.csv). Searches S46–S57: [`targeted_search_log.md`](targeted_search_log.md)._

## 1. Purpose

This is a targeted evidence-closure pass for GC-03 only. It addresses the three Step 9.9 Phase A gate questions that were left `unresolved` for GC-03:
- **Q2:** the Unknown burden;
- **Q8:** whether a contribution is distinguishable from integration;
- **Q10:** the risk of being overturned by further literature.

It is not a broad literature survey. It does not select, rank or score GC-03 against GC-01 or GC-02, and it does not create `research_gap.md`.

**Frozen corpus.** `research/literature/papers.csv`, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. It has 54 records, 31 columns and 0 duplicate IDs, and was verified before and after this step. It was not modified, and no paper found here was added to it.

**Dependency note.** Step 9.9 Phase A (`d8894d9`, branch `claude/step-9-9-gap-selection-framework`) is not merged into `main`. As instructed, this branch was created from `origin/main`, so `final_gap_selection.md`, `final_gap_selection_matrix.csv`, `configs/gap_selection.yaml` and `tests/test_gap_selection.py` do not exist here. They were read from the Phase A branch and not modified. The Q2/Q8/Q10 answers below are meant to replace the `unresolved` GC-03 entries in Phase A's `selection_gate` once both branches are reconciled. That reconciliation is a researcher decision.

## 2. GC-03 exact wording

> "Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus."

The wording is identical to `configs/gap_evaluation.yaml` (Step 9.8). It is a corpus-bounded observation, not a claim about the literature as a whole.

## 3. Five full-counterexample criteria

A **full** counterexample must satisfy all five of the following. The Step 9.8 rule is `full_counterexample_criteria.GC-03` in `configs/gap_evaluation.yaml`.

| # | Criterion | Operational meaning |
| --: | :-- | :-- |
| 1 | `smartphone` | The actual inference platform is a smartphone. |
| 2 | `visual_inspection` | The actual inspection input is optical image/video/camera data of a physical object, component, surface, structure or manufactured item. |
| 3 | `resource_awareness` | Device or resource state (battery, CPU/GPU load, memory, temperature, available compute, power state, resource budget) drives an inference or system decision. Content complexity alone does not count (Decision A). |
| 4 | `adaptive_inference` | The executed computation, model or path changes at runtime. |
| 5 | `confidence_gating` | Confidence, uncertainty or an inspection-quality signal explicitly triggers a downstream action: recapture, additional view, stronger model, extra inference, human referral, rejection, fallback or escalation. Learned view selection alone does not count (Decision B). |

**Strength rules.**
- **Full:** all five Yes.
- **Potential:** no criterion clearly failed, with at least one Unknown.
- **Partial:** at least one criterion clearly failed (explicit No).
- **Not counterexample:** the task, platform and mechanism are all outside GC-03.

Unknown is never converted to No. Title- or snippet-level evidence is never treated as full text.

## 4. P001 verification

**Paper.** *Deep learning smartphone application for real-time detection of defects in buildings* (Perez & Tah, 2021, *Structural Control and Health Monitoring*, doi 10.1002/stc.2751).

**Access attempted (legitimate routes only).**
- Wiley open-access HTML/PDF: `onlinelibrary.wiley.com` is blocked by the egress proxy.
- Repository search: two WebSearch queries. The Oxford Brookes RADAR, arXiv 1908.04392 and PMC6720984 hits belong to a **different** paper: Perez, Tah & Mosavi, *Sensors* 2019, a CNN building-defect classifier. It is not used as P001 evidence.
- Abstract re-read through Consensus (S52). It describes a smartphone app using the phone's camera for real-time detection of four building-defect types. It mentions no runtime adaptation, no resource signal and no confidence-triggered action.

| Criterion | Value | Evidence |
| :-- | :-- | :-- |
| smartphone | Yes | Corpus coding (abstract) |
| visual_inspection | Unknown | `visual_inspection_scope.csv`: input modality not stated in the coded fields. The abstract mentions phone cameras, but the frozen classification is not recoded here. |
| resource_awareness | Unknown | Not stated |
| adaptive_inference | Unknown | Not stated |
| confidence_gating | Unknown | Not stated |

**Result: unresolved.**
- Evidence level: `abstract_only` (locked).
- Strength: **potential**. Four of the five criteria are undeterminable, and none is clearly failed.
- The abstract gives no indication of adaptation or gating, but that absence is not evidence of No.

## 5. P007 verification

**Paper.** *Pothole Detection Using Deep Learning: A Real-Time and AI-on-the-Edge Perspective* (Asad et al., 2022, *Advances in Civil Engineering*, doi 10.1155/2022/9221211).

**Access attempted.** Wiley/Hindawi open-access full text (`onlinelibrary.wiley.com`, `downloads.hindawi.com`) and `structurae.de` are all blocked by the egress proxy. No legitimate repository copy was found.

| Criterion | Value | Evidence |
| :-- | :-- | :-- |
| smartphone | **No** | The abstract places inference on an OAK-D AI kit attached to a Raspberry Pi (corpus coding) |
| visual_inspection | Yes | Pothole image dataset and real-time vehicle video |
| resource_awareness | Unknown | Not stated |
| adaptive_inference | Unknown | Not stated |
| confidence_gating | Unknown | Not stated |

**Result: unresolved full text.**
- Evidence level: `abstract_only` (locked).
- Strength: **partial**, because it clearly fails criterion 1.
- P007 cannot become a full counterexample unless the full text contradicts its own abstract on the platform.

## 6. PMC11435656 full-text verification

**Paper.** *Cloud-Edge Collaborative Defect Detection Based on Efficient Yolo Networks and Incremental Learning* (*Sensors* 24(18):5921, doi 10.3390/s24185921).

**Source.** Read in full, end to end (introduction to conclusions), through the PubMed Central full-text service. Step 9.8 had only scanned it by keyword.

| Question | Answer from the full text | Coded value |
| :-- | :-- | :-- |
| Does device resource state drive routing/adaptation? | **No.** Routing is driven only by detection confidence (§2.1.1, §3.5). The task split over three Raspberry Pi 4 units is a design-time allocation ("load distribution and parallel processing"). No battery, CPU, memory, temperature or other device-state signal enters any runtime decision. The "resource awareness module" in the introduction belongs to a *cited* system. | `resource_awareness` Unknown → **No** |
| Does confidence trigger escalation? | **Yes.** When Raspberry Pi A detects a defect below the 0.6 confidence threshold, it signals Raspberry Pi B, which re-detects and sends the image to the cloud (YoloV5s). Cloud-confirmed defects trigger sorting by a robotic arm (§3.5). | `confidence_gating` Yes (unchanged) |
| Is the actual inspection visual? | **Yes.** A camera video stream of PCB components, with six PCB defect classes (§2.3.1, §3.2). | Yes |
| Is the computing platform a smartphone? | **No.** Raspberry Pi 4 edge devices plus a cloud server (§2.1.1, §3.5). | No |
| Runtime path change? | **Yes.** Low-confidence samples follow a different computation path. | `adaptive_inference` Yes (unchanged) |

**Result: partial** (confirmed partial; never upgraded). It fails criteria 1 and 3.
- Evidence level stays `verified_full_text` (locked); verification status becomes `verified_by_full_text_read`.
- For consistency, the same `resource_awareness` correction is applied to the paper's GC-01 and GC-02 rows; their strengths are unchanged.

## 7. ActiveInspect full-text verification

**Paper.** *ActiveInspect: GRPO-Optimized Multi-Sensor Evidence Selection for Industrial Defect Detection* (*Sensors* 26(15):4932, doi 10.3390/s26154932).

**Source.** Read in full, all sections, through the PubMed Central full-text service (PMC13468834).

| Question | Answer from the full text | Coded value |
| :-- | :-- | :-- |
| Does confidence/uncertainty actually drive view selection? | **Not by an explicit rule.** Step-level confidences are parsed from the VLM's JSON output and stored in the evidence memory the policy conditions on (§3.5). The paper reports that action A3 (normal-reference comparison) is "selected mainly when the step confidence lies between 0.4 and 0.7" (§4.8), and that A4 "terminates to convert confidence into budget savings" (§3.2). Selection itself is made by a GRPO-trained policy, with no threshold or rule (§3.3, §3.7). | `confidence_gating` **Unknown, kept and flagged** |
| Does device/resource state drive adaptation? | **No.** The observation budget B is a fixed task hyperparameter, and the length penalty uses a uniform observation count (§3.1, §3.7–3.8). The paper states that observation count is not a measure of time, energy or hardware cost (§5.5). | `resource_awareness` Unknown → **No** |
| Is the computing platform a smartphone? | **No.** Training uses eight A100 GPUs; all inference uses a single A100 80 GB with 21.4 GB peak memory (§4.1). | No |
| Is the task optical visual inspection? | **Yes.** RGB plus photometric-stereo and point-cloud renderings of industrial parts, from pre-acquired pools (§3.1, §3.4, §5.5). | Yes |
| Runtime path change? | **Yes.** A sample-adaptive number of views, actions and VLM calls (mean 2.7 observations). | `adaptive_inference` Yes (unchanged) |

**Researcher decision flagged (confidence_gating).**
- The two approved wordings point in different directions. Decision B: confidence "explicitly informs or triggers" the action. This task: confidence "explicitly triggers" the action.
- Confidence *informs* the learned policy, but no explicit rule *triggers* an action. The value is therefore kept Unknown rather than forced either way.
- Either reading leaves ActiveInspect **partial**, because it fails criteria 1 and 3.

## 8. Additional high-value papers

These are the Priority 5 candidates: the strongest remaining title- or snippet-level papers that could plausibly meet all five criteria, plus papers surfaced by the citation follow-up and searches. Papers that clearly cannot meet GC-03 were not pursued.

| Paper | Evidence level | smartphone | visual | resource | adaptive | confidence | Strength |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| PMC10280690, *Adaptive visual detection of industrial product defects* (PeerJ CS, doi 10.7717/peerj-cs.1264) | verified_full_text (PMC) | No | Yes | No | No | No | **not_counterexample** ("adaptive" means training-time MAML; DGX A100) |
| AIVD, arXiv 2601.04734, *Adaptive Edge-Cloud Collaboration for Accurate and Efficient Industrial Visual Detection* | search_snippet_only | Unknown | Yes | Unknown | Unknown | Unknown | **potential** |
| Yan et al. 2025, *Dynamic Swin Transformer With Early Exit…* (IEEE Access) | abstract_only | No | Yes | Unknown | Yes | Yes | **partial** (edge implementation is future work) |
| Choi et al. 2026, *Joint Optimization of Confidence Thresholds and Resource Allocation…* (IEEE TVT) | abstract_only | Unknown | Unknown | Unknown | Yes | Yes | **potential** |
| Zakaria et al. 2022, *Advanced bridge visual inspection using real-time ML in edge devices* | abstract_only | Unknown | Yes | Unknown | Unknown | Unknown | **potential** |
| RAMS, arXiv 2606.14716 (resource-adaptive, detection-conditioned model switching) | search_snippet_only | Unknown | No | Unknown | Unknown | Unknown | **partial** (road-user perception, not inspection) |
| HAPI, arXiv 2008.03997 (hardware-aware progressive inference) | search_snippet_only | Unknown | No | Unknown | Yes | Yes | **partial** (generic classification) |
| Electronics 15(17):3915 (resource-efficient surface-defect detection on edge devices) | search_snippet_only | Unknown | Yes | Unknown | Unknown | Unknown | **potential** (`www.mdpi.com` blocked) |

**AIVD is the highest-value unresolved item.**
- Its abstract-level snippets describe a "heterogeneous resource-aware dynamic scheduling algorithm" across heterogeneous edge devices for industrial visual detection, with a cloud MLLM.
- Neither `arxiv.org` nor the alphaXiv service was reachable in this session, so the edge platform, the role of device state and any confidence-triggered escalation could not be verified.

The DMS and Electronics 14(11):2188 title hits (Step 9.8) were not pursued. Both concern generic mobile or edge inference with no inspection task, so they cannot satisfy criterion 2.

## 9. Indexed-database search

Twelve searches, S46–S57, were logged in the required format in `targeted_search_log.md`. All four requested databases were blocked by this environment's egress proxy (CONNECT 403 / `EGRESS_BLOCKED`, 2026-10-05). No results were fabricated, and each substitute is labelled in the log.

| Requested database | Access | Substitute used | Searches | Results (per search) |
| :-- | :-- | :-- | --: | :-- |
| IEEE Xplore | blocked | WebSearch restricted to `ieeexplore.ieee.org` | 3 (S46–S48) | 10, 9, 10 |
| ACM Digital Library | blocked | WebSearch restricted to `dl.acm.org` | 3 (S49–S51) | 9, 9, 9 |
| Scopus | blocked | Consensus (states coverage of Semantic Scholar, PubMed, Scopus, arXiv) | 3 (S52–S54) | 10, 10, 10 |
| Web of Science | blocked | PubMed | 3 (S55–S57) | 3, 0, 0 |

The queries combined the required concepts: smartphone/mobile; visual inspection, defect detection, industrial or manufacturing inspection; resource-aware; adaptive or dynamic inference; confidence.

Limitations:
- The domain filters leaked, so most WebSearch results came from PMC, arXiv or USPTO.
- One results page per search.
- English only.
- S53 drifted to battery fault detection, and the S55 hits were medical.

Verification lookups are listed separately in the log and not counted among the 12: three PMC full-text reads, two P001 and one P007 repository searches, one citation follow-up and one AIVD snippet lookup.

**Outcome.** No full counterexample. The new hits are partial (Yan 2025, RAMS, HAPI) or potential (AIVD, Choi 2026, Zakaria 2022).

## 10. Counterexample assessment

**No full counterexample to GC-03 was identified** in Steps 9.8 and 9.9B. This is an observation about the searches and the papers read, not about the literature as a whole.

| Paper | Criteria clearly met | Criteria clearly failed | Unknown | Strength |
| :-- | :-- | :-- | :-- | :-- |
| PMC11435656 | visual, adaptive, confidence | smartphone, resource | — | partial (confirmed) |
| SAEC, arXiv 2509.17136 | visual, adaptive, confidence | smartphone, resource | — | partial |
| Yan et al. 2025 | visual, adaptive, confidence | smartphone | resource | partial (abstract) |
| ActiveInspect | visual, adaptive | smartphone, resource | confidence (flagged) | partial (confirmed) |
| RobustDefect-LLM, arXiv 2608.08589 | visual, confidence | smartphone, resource, adaptive | — | partial |
| arXiv 2608.14727 | visual, adaptive | smartphone, resource | confidence | partial (confirmed) |
| P011 (XEdgeAI) | smartphone, visual | resource, adaptive, confidence | — | partial |
| P016 | visual, confidence | smartphone, resource, adaptive | — | partial |
| P007 | visual | smartphone | resource, adaptive, confidence | partial (abstract) |
| RAMS / HAPI | (resource-adaptive and/or confidence-conditioned mechanisms) | visual | platform | partial (snippet) |
| AIVD | visual | — | smartphone, resource, adaptive, confidence | potential (snippet) |
| Choi et al. 2026 | adaptive, confidence | — | smartphone, visual, resource | potential (abstract) |
| P001 | smartphone | — | visual, resource, adaptive, confidence | potential (abstract) |
| Zakaria et al. 2022; Electronics 15(17):3915 | visual | — | the other four | potential |

**Closest neighbours.**
- PMC11435656, SAEC and Yan 2025 each meet three criteria and fail the smartphone criterion; PMC11435656 and SAEC also clearly fail resource awareness.
- None meets four criteria with only the fifth unresolved. So no record reaches the "four satisfied, fifth unresolved" potential level.

## 11. Q2 — Unknown burden

**Result: `conditionally_acceptable`.**

1. **Unknowns that could realistically overturn GC-03.** Only five papers, none smartphone-verified:
   - P001: smartphone Yes, four criteria Unknown, full text blocked.
   - AIVD: resource-aware scheduling claimed, platform and confidence role Unknown, snippet only.
   - Choi et al. 2026: task and device Unknown.
   - Zakaria et al. 2022: smartphones named among the target devices; adaptation and gating not stated.
   - Electronics 15(17):3915: snippet only.
2. **Peripheral Unknowns.** The corpus-level Unknown burden (about 23–24 of 27 in-scope records Unknown per runtime or gating field, Step 9.8) is dominated by visual-inspection papers coded from abstracts that show no smartphone platform. These are peripheral: they could only overturn GC-03 if their full texts revealed an unreported smartphone deployment, runtime adaptation and confidence gating together. No abstract indicates that.
3. **Unknowns on the exact five criteria.**
   - Resolved in this step:
     - PMC11435656 `resource_awareness` → No;
     - ActiveInspect `resource_awareness` → No;
     - PMC10280690 → not a counterexample;
     - P007 → clearly fails smartphone.
   - Still open: ActiveInspect `confidence_gating` (definitional; it cannot change the outcome because two criteria fail) and the five papers listed above.
4. **Potentially relevant papers still unresolved:** five, as above.
5. **Did the searches reduce uncertainty?** Partly.
   - The full-text reads closed two of the three open GC-03 fields on confirmed partials.
   - The 12 searches found no full or "four-plus-one" candidate.
   - They also added two abstract-level potentials (Choi 2026, Zakaria 2022) and one snippet-level potential (AIVD).

**Why conditional.**
- The burden is acceptable for the corpus-bounded wording of GC-03, because no remaining Unknown sits on a paper that already meets four criteria.
- It is not acceptable for any claim beyond the reviewed corpus.
- The condition is that P001 and AIVD are either read in full, or explicitly carried as named limitations in any gap statement.

## 12. Q8 — Contribution distinctiveness

**Result: `conditionally_distinct`.**

**A. Components already demonstrated** (each in the repository evidence; none is claimed as new):

| Component | Demonstrated by (examples) |
| :-- | :-- |
| Resource-aware inference on smartphones | P029 (NestDNN), P031 (LOTUS, DVFS), P033 (CARIn), P034 (REDS) |
| Adaptive inference | P025 (early exit), P029, P033, P034; PMC11435656, SAEC, arXiv 2608.14727 (inspection cascades) |
| Smartphone vision / inspection | P011 (on-phone segmentation for industrial inspection); P001 (abstract) |
| Confidence gating in inspection | P016 (stop-print referral), PMC11435656 (cloud escalation), SAEC (MLLM escalation), RobustDefect-LLM (human review), Yan 2025 (early exit) |
| Additional-view inspection | ActiveInspect (learned selection over a pre-acquired pool); multi-view datasets P037, P038 |
| Human escalation | RobustDefect-LLM; arXiv 2608.21967 (deferral, offline) |
| Energy/thermal monitoring on phones | P029 (energy), P031 (thermal), arXiv 2603.26603 (energy and temperature, LLM workload) |
| Resource adaptation combined with confidence-conditioned switching (outside inspection) | RAMS (snippet), HAPI (snippet), Choi et al. 2026 (abstract) |

Integration alone is therefore not distinctive. The last row matters most: confidence thresholds and resource allocation have already been optimised jointly for generic edge inference (Choi et al. 2026, abstract level). That has to be read and distinguished before any distinctiveness is asserted.

**B. Evaluation of the candidate question.**

> "Can confidence-aware downstream verification compensate for the accuracy degradation introduced when a resource-constrained smartphone dynamically downgrades its inspection configuration?"

- **Quantitatively testable: yes.**
  - Every element is measurable with a factorial design over B1–B5 (§15).
  - The recall/precision/F1 loss from a resource-driven downgrade is measured as B3 versus B1.
  - Recovery is measured as B5 versus B3.
  - The cost of recovery is measured as latency, energy, temperature, battery and memory for B5 versus B1.
  - Whether the two mechanisms interact is measured as B5 versus B3 and B4.
  - Calibration error per configuration covers ECE and risk-coverage.
  - Trigger rates are the recapture, additional-view, escalation and referral rates, recorded against the logged resource state.
- **What would be a meaningful contribution (Hypothesis, requires empirical validation):**
  1. Quantify how much defect recall is lost under realistic resource pressure on a phone, and how much confidence-triggered verification recovers, at a stated cost.
  2. Test whether confidence calibration shifts across downgraded configurations (H-GC03-1, Step 9.9 Phase A). If it does, thresholds calibrated at full capacity mis-trigger verification. A per-configuration recalibration that measurably changes trigger rates and residual error would then be a mechanism-level finding.
  3. Show a non-additive interaction: B5 differs from what B3 and B4 predict, in recall at a fixed review rate or in cost.
- **What would be engineering integration only:** building the pipeline and reporting that it runs, or reporting component metrics without the downgrade-recovery and calibration analyses.

**Why conditional.**
- Distinctiveness depends on the interaction and calibration findings (items 2–3), which are untested Hypotheses.
- It also depends on full-text reads of Choi et al. 2026 and AIVD, the closest conceptual neighbours, to confirm they do not already study downgrade-induced calibration shift in inspection.
- No distinctiveness claim is made in this document.

## 13. Q10 — Literature overturn risk

**Result: `moderate`.** The risk is not zero.

**Factors lowering the risk:**
- 57 logged searches in total (S01–S57), plus full-text reads of every confirmed partial, found no full counterexample.
- None of the closest neighbours meets four criteria.
- The smartphone criterion is the one most often clearly failed.

**Factors raising the risk:**
- P001 and P007 are unresolved at abstract level.
- AIVD is resource-aware and inspection-oriented but snippet-only.
- Choi et al. 2026 and Zakaria et al. 2022 are abstract-level.
- The indexed databases were reached only through substitutes, with leaking domain filters.
- One page per search, and English only.
- The corpus Unknown burden is high.
- Converging neighbours (Yan 2025, RAMS, HAPI, Choi 2026) show the components being combined in adjacent settings.

**What would overturn GC-03.** A paper meeting all of the following:
- a smartphone or phone-class handset is the inference platform;
- it performs optical inspection of physical items (for example building, infrastructure, PCB or manufactured-part defects);
- device state (battery, thermal, load or memory) changes the executed model or configuration at runtime;
- a confidence or uncertainty signal triggers recapture, an additional view, escalation, referral or rejection.

**Most plausible locations:**
- the P001 or AIVD full texts;
- mobile structural or infrastructure inspection apps;
- mobile-systems venues (MobiSys, SenSys, MobiCom) and industrial-informatics journals that the substitutes may under-index.

## 14. Dataset feasibility

This checks only the 13 Step 9.9 Phase A dataset entries; no broad dataset survey was done. Access and licence details are **not** assumed: every entry stays `verification_required` or `unknown` (`configs/gc03_evidence_closure.yaml`).

| Dataset | Visual defect inspection | Smartphone-captured | Multi-view / recapture | Custom capture needed | Access / licence |
| :-- | :-- | :-- | :-- | :-- | :-- |
| MVTec AD | Yes | Unknown | Unknown | for smartphone realism | verification_required |
| Real-IAD | Yes | Unknown | multi-view (5 RGB viewpoints) | for recapture | verification_required |
| MANTA | Yes | Unknown | multi-view (5 viewpoints) | for recapture | verification_required |
| MVTec3D-AD + Eyecandies | Yes | Unknown | RGB + 3D; multi-view per P043 | for smartphone realism | verification_required |
| DeepPCB / PCB set | Yes | Unknown | Unknown | for multi-view/recapture | verification_required |
| CAXTON | Yes | No | No | yes | verification_required |
| P016 stringing | Yes | No | No | yes | unknown |
| P020 layer images | Yes | No | No | yes | unknown |
| VisA | Yes | Unknown | Unknown | for multi-view/recapture | verification_required |
| KolektorSDD2 | Yes | Unknown | Unknown | for multi-view/recapture | verification_required |
| NEU-DET | Yes | Unknown | Unknown | for multi-view/recapture | verification_required |
| MMS | Yes | No | No (cross-device) | yes | verification_required |
| Phone-captured 3D-printed-part set | Yes (by design) | Yes (by design) | Yes (by design) | yes (Proposed idea) | unknown |

1. **Visual defect inspection:** all 13 entries.
2. **Smartphone inference:** any image set can be replayed through an on-phone model, so all 13 can drive on-device *inference*. No existing entry is verified as *smartphone-captured*.
3. **Multi-view / recapture:** multi-view exists in Real-IAD, MANTA and MVTec3D-AD/Eyecandies, all pending access verification. No entry supports *physical recapture*.
4. **Custom capture required:** for physical recapture and for smartphone-domain realism (the phone-captured set, a Proposed idea).
5. **Unknown access/licence:** all 13. No licence or access term is asserted here.

## 15. Minimum viable experiment

Status: Proposed idea. No results are claimed, and device models, tolerances and run counts are Assumptions to be pre-registered in `configs/`.

**Chain under test:** resource pressure → configuration downgrade → accuracy degradation → confidence-aware verification → recovery.

**Defensible minimum version.**
- **Device:** one Android smartphone. Model and API access are Assumptions to verify, including Android thermal-status and battery APIs and the validity of on-device energy logging.
- **Data:**
  - Stage 1: a public multi-view inspection set (Real-IAD or MANTA, pending access and licence verification) replayed on the phone. The pool's additional viewpoints stand in for "additional view"; this is a stated limitation, because it is not physical recapture.
  - Stage 2 (optional): a small phone-captured set of seeded-defect 3D-printed parts with scripted recapture.
- **Configurations:** a pre-registered ladder of inspection configurations, for example model size, input resolution and precision (FP16/INT8).
- **Resource pressure:** induced reproducibly (background CPU load, thermal soak, low-battery or power-saver state) and logged with every inference.
- **Verification action:** when calibrated confidence falls below a threshold, take an additional view, escalate to a larger on-device model, or refer to a human. One action is pre-registered as primary.

**Candidate baselines.** They are consistent with this design because all share the same data, device, ladder and verification action.

| Baseline | Resource adaptation | Confidence verification | Purpose |
| :-- | :-- | :-- | :-- |
| B1 static best model | No (top of the ladder) | No | Accuracy reference; exposes throttling cost |
| B2 static lightweight model | No (bottom of the ladder) | No | Cost floor |
| B3 resource-aware adaptation | Yes | No | Isolates downgrade-induced degradation |
| B4 confidence verification only | No (fixed configuration, pre-registered) | Yes | Isolates the verification effect |
| B5 full system | Yes | Yes | Tests recovery and interaction |

**Outcomes.**
- **Accuracy:** defect recall (primary), precision, F1, and mAP where the task is detection.
- **Calibration:** ECE per configuration and risk-coverage curves.
- **Trigger behaviour:** threshold, trigger rate, additional-view rate, escalation rate and referral rate.
- **Cost:** latency per item, energy per item, temperature trajectory, battery drop and memory.
- **Context:** the logged resource state.

**Falsification.** The GC-03 RQ1 condition from Phase A: verification does not recover recall beyond the downgraded baseline, or recovers it only at a cost equal to running B1.

**Feasibility.** A defensible minimum experiment exists, conditional on:
- dataset access and licence verification;
- device and API verification;
- accepting replayed views as the Stage 1 proxy for recapture.

## 16. Remaining limitations

**Unresolved papers:**
- P001 and P007: full texts blocked; `abstract_only` (locked).
- AIVD, RAMS, HAPI and Electronics 15(17):3915: snippet only.
- Choi et al. 2026, Yan et al. 2025 and Zakaria et al. 2022: abstract only. The Consensus records were used as sources, and their DOIs were not verified from the tool output.

**Other limitations:**
- ActiveInspect `confidence_gating` needs a researcher decision (definitional).
- IEEE Xplore, ACM DL, Scopus and Web of Science were not searched directly; substitutes were used.
- One page per search; English only; leaking domain filters.
- The corpus Unknown burden is unchanged. `papers.csv` is frozen, and no corpus record was recoded.
- P013 Tables 4–5 remain visually unverified. This is not used as a gap signal; P013 is peripheral.
- Step 9.9 Phase A files are not on this branch (see §1).

## 17. Decision readiness

| Gate question (GC-03) | Phase A status | Step 9.9B result |
| :-- | :-- | :-- |
| Q2: Unknown burden | unresolved | **conditionally_acceptable** (corpus-bounded wording; P001 and AIVD named as limitations or read) |
| Q8: Distinct from integration | unresolved | **conditionally_distinct** (depends on the calibration-shift and interaction Hypotheses, plus full reads of Choi 2026 and AIVD) |
| Q10: Overturn risk | unresolved | **moderate** (overturning paper type specified in §13) |

**Evidence closure for GC-03 is as complete as this environment allows.** Three items remain, and each needs access this session did not have: the AIVD full text, the P001 full text and the Choi et al. 2026 full text. With these three Phase A questions answered, GC-03 is ready for the researcher's selection review. No candidate is ranked, and GC-01 and GC-02 were not re-evaluated in this step.

GC-03 has been evaluated for evidence closure. This document does not select GC-03 as the final research gap. Final selection remains a researcher decision.
