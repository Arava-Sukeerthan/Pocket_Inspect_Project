# Research Gap — GC-03 (Approved)

_Step 10A, 2026-10-05, Claude Code._

This document is the **source of truth for the approved PocketInspect research gap**. It was created only after explicit researcher approval (see §8). Configuration: [`configs/research_protocol.yaml`](../../configs/research_protocol.yaml). Research questions, objectives, hypotheses and variables are in [`research/research_questions/`](../research_questions/).

Epistemic labels follow `RESEARCH_RULES.md`: **Fact** (established in the repository's evidence record), **Assumption**, **Hypothesis** and **Proposed idea**.

## 1. Research Gap

> Within the reviewed literature corpus, there is limited evidence of an integrated resource-aware smartphone visual-inspection system in which device-state-driven runtime adaptation is coupled with confidence-aware downstream verification, particularly for recovering inspection performance under resource-induced model/configuration degradation.

The statement is corpus-bounded. It says what the reviewed corpus and the logged targeted searches do and do not show. It does not say that such a system does not exist elsewhere.

The Step 9.8 evaluated wording ("Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus.") remains the wording against which every evidence row in `counterexample_candidates.csv` was coded. The approved wording refines it; it does not widen it.

## 2. Literature Boundary

- **Frozen corpus (Fact).** `research/literature/papers.csv`: 54 records, 31 columns, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. The core-analysis subset is 46 records; the visual-inspection in-scope set is 27 records.
- **Targeted searches (Fact).** S01–S57 in [`targeted_search_log.md`](targeted_search_log.md), 16 of them aimed at GC-03 in Step 9.8 and 12 more (S46–S57) in Step 9.9B.
- **External papers (Fact).** Papers found by the targeted searches are recorded only in [`counterexample_candidates.csv`](counterexample_candidates.csv); they were never added to the corpus.
- **Not covered.** Direct IEEE Xplore, ACM DL, Scopus and Web of Science access (substitutes were used); non-English literature; only one results page per search; literature published after the searches were run.
- **Full-counterexample rule.** A study is a full counterexample only if `smartphone`, `visual_inspection`, `resource_awareness`, `adaptive_inference` and `confidence_gating` are all Yes. **Full counterexamples identified: 0** (Fact, corpus- and search-bounded). Partial counterexamples exist for every individual component.

## 3. Primary Research Question

> **RQ1.** Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained smartphone dynamically downgrades its inference configuration under changing device conditions?

Secondary questions RQ2–RQ6 decompose RQ1; see [`research_questions.md`](../research_questions/research_questions.md).

## 4. Scope

**In scope.**
- One task family: optical visual-defect inspection of physical items (the approved `visual_inspection_scope` definition), with 3D-printed parts and small manufactured components as the initial domain (`PROJECT_SPEC.md` §1).
- On-device inference on a resource-constrained Android smartphone.
- Runtime adaptation driven by device state (battery, thermal, compute load, memory), acting through a pre-defined configuration ladder (C1–C4).
- Confidence-aware downstream verification actions (A0–A4) applied after inference.
- Accuracy, calibration, latency, energy/power, thermal behaviour, memory and verification overhead.

**Out of scope.**
- Cloud or backend inference as the primary inference path.
- Content-driven early-exit cascades that are not triggered by device state (Step 9.8 Decision A).
- Learned view-selection policies that are not triggered by a confidence signal (Step 9.8 Decision B).
- Training new architectures as a research contribution; model choice is an enabling step (Step 10B).
- Claims about inspection tasks, devices or platforms that are not tested.

## 5. Research Motivation

- **Fact.** Each component of the gap is demonstrated somewhere in the literature: smartphone visual inspection (e.g. P011), confidence-triggered re-detection or cloud routing at the edge (PMC11435656, SAEC arXiv 2509.17136), confidence-informed additional-view acquisition on a GPU (ActiveInspect), and resource-adaptive inference outside inspection (RAMS, HAPI, Choi et al. 2026).
- **Fact.** In the reviewed corpus and searches, no study couples device-state-driven configuration downgrading with confidence-triggered downstream verification on a smartphone for visual inspection.
- **Assumption.** Smartphones repurposed for inspection experience battery, thermal and load changes during sustained use, so a fixed high-accuracy configuration cannot always be sustained.
- **Hypothesis.** Downgrading to cheaper configurations under pressure lowers inspection performance (H1), and selectively verifying low-confidence outputs recovers part of that loss at a cost lower than staying on the highest-accuracy configuration (H2, H5).
- **Why it matters (Proposed idea).** If recovery is possible, a low-cost device could keep inspection performance closer to its best configuration while respecting resource limits. If it is not, the experiment documents a limit on combining these mechanisms. Both outcomes are reportable.

## 6. Candidate Contribution

**CANDIDATE CONTRIBUTION — TO BE VALIDATED EXPERIMENTALLY**

> An empirical investigation of whether confidence-aware downstream verification can recover inspection performance degraded by resource-driven runtime configuration changes on a resource-constrained smartphone, including analysis of accuracy, calibration, latency, energy, thermal behavior, and verification overhead.

Integrating resource-aware inference, smartphone inspection and confidence gating is **not** by itself the contribution; each component is already demonstrated in the literature. The candidate contribution is the empirical answer to RQ1–RQ6, which does not yet exist. The contribution boundary (what will not be claimed) is in [`experimental_framework.md`](../research_questions/experimental_framework.md) §7.

## 7. Known Limitations

- **Unresolved full texts:** P001 (potential; publisher host blocked), P007 (partial at abstract level), AIVD arXiv 2601.04734 (potential; snippet only), Choi et al. 2026 IEEE TVT (potential; abstract only), Zakaria et al. 2022 and Electronics 15(17):3915 (potential).
- **Unverified DOIs** for the Consensus-sourced records (Yan 2025, Choi 2026, Zakaria 2022).
- **ActiveInspect `confidence_gating`** remains an operational-definition issue ("explicitly informs" versus "explicitly triggers").
- **Search coverage:** substituted database access; English only; one results page per search; leaking domain filters.
- **Unknown burden:** most in-scope records remain Unknown for the runtime and gating fields. Unknown is never treated as No.
- **Literature-overturn risk: moderate.** A single study demonstrating smartphone optical inspection, device-state-driven runtime configuration changes and confidence-triggered recapture or escalation in one system would overturn the gap.
- **Selection gate.** Gate questions Q1, Q3, Q5, Q6, Q7 and (after Step 9.9B) Q2, Q8, Q10 are `partially_satisfied` for GC-03, so the automated `can_select()` predicate in `src/literature/gap_selection.py` remains False. The approval in §8 is a researcher judgement that accepts these limitations; it does not convert them into satisfied criteria.
- **Datasets:** access, licence, smartphone suitability and multi-view/recapture suitability are unverified for every reviewed dataset.
- **Nothing has been tested.** All hypotheses are TO BE TESTED; no experiment has been run.

## 8. Approval Status

**APPROVED — GC-03 is the approved PocketInspect research gap.**

| Field | Value |
| :-- | :-- |
| Approved by | Researcher |
| Date | 2026-10-05 |
| Explicit approval | "Approve GC-03 as the final research gap." |
| Selection state | `configs/gap_selection.yaml`: `selection_status: researcher_approved`, `selected_candidate: GC-03` |
| Decision record | `research_gap_approval.md` §14: "DECISION: GC-03 APPROVED AS THE FINAL RESEARCH GAP" |
| Repository state before Step 10A | `researcher_approval_required` / pending (commit `72a828b`), kept as audit context in `research_gap_approval.md`. |

GC-01 and GC-02 are not approved and remain candidate gaps with their Phase A status. No candidate was ranked.

## 9. Traceability to Steps 9.7–9.9C

| Step | Artefact | What it established |
| :-- | :-- | :-- |
| 9.7 | [`gap_candidates.md`](gap_candidates.md), [`gap_matrix.csv`](gap_matrix.csv), [`combination_matrix.csv`](combination_matrix.csv), [`corpus_freeze.md`](corpus_freeze.md) | GC-03 emerged as an evidence-supported candidate from the frozen 54-record corpus; no core record meets three of the components. |
| 9.8 | [`candidate_gap_evaluation.md`](candidate_gap_evaluation.md), [`candidate_gap_matrix.csv`](candidate_gap_matrix.csv), [`counterexample_candidates.csv`](counterexample_candidates.csv), [`targeted_search_log.md`](targeted_search_log.md) | Narrowed wording, Decisions A–C, partial counterexamples, 16 GC-03 searches with no full counterexample. |
| 9.9 (Phase A) | [`final_gap_selection.md`](final_gap_selection.md), [`final_gap_selection_matrix.csv`](final_gap_selection_matrix.csv), `configs/gap_selection.yaml` | Criteria A–Q and gate Q1–Q10; candidate RQs; feasibility; no selection. |
| 9.9B | [`gc03_evidence_closure.md`](gc03_evidence_closure.md), `configs/gc03_evidence_closure.yaml` | Full-text reads (PMC11435656, ActiveInspect, PMC10280690), S46–S57, Q2 conditionally acceptable, Q8 conditionally distinct, Q10 moderate, minimum viable experiment. |
| 9.9C | [`research_gap_approval.md`](research_gap_approval.md) | Reconciliation; approval-ready wording, RQ1, H1–H5, B1–B5; decision pending. |
| 10A | this document; `research/research_questions/` | Researcher approval recorded; formal RQs, objectives, hypotheses, variables, resource states, configuration ladder, verification actions, baselines and falsification criteria. |

The Step 9.7–9.9C artefacts are kept as the historical record of the pre-approval state. Statements in them such as "GC-03 is not selected" describe that state and are superseded by §8.
