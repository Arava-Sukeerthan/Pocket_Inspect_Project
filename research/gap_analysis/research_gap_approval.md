# Research Gap Approval — GC-03

_Step 9.9C, 2026-10-05, Claude Code._

This is an approval document. It is **not** `research_gap.md`, it does not select GC-03, and it is not a ranking. GC-01 and GC-02 remain candidate gaps.

Sources:
- `configs/gap_selection.yaml` (`approval_ready.GC-03`, `evidence_closure.GC-03`, `selection`);
- [`gc03_evidence_closure.md`](gc03_evidence_closure.md);
- [`final_gap_selection.md`](final_gap_selection.md);
- [`counterexample_candidates.csv`](counterexample_candidates.csv).

Frozen corpus: `research/literature/papers.csv`, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. It has 54 records and 31 columns and was not modified.

## 1. Candidate Status

Status:
RESEARCHER APPROVAL REQUIRED

- `selection_status: researcher_approval_required`; `selected_candidate: null`.
- Evidence closure is complete for GC-03, but final research-gap selection requires explicit researcher approval.
- GC-03 is an approval-ready candidate. It is not selected.

## 2. Candidate Research Gap

> Within the reviewed literature corpus, there is limited evidence of an integrated resource-aware smartphone visual-inspection system in which device-state-driven runtime adaptation is coupled with confidence-aware downstream verification, particularly for recovering inspection performance under resource-induced model/configuration degradation.

This statement is corpus-bounded. It refines the evaluated Step 9.8 wording ("Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines runtime adaptation with confidence-aware downstream verification within the reviewed corpus."), and all evidence rows refer to that wording. It makes no claim about literature outside the reviewed corpus and searches.

## 3. Candidate Research Question

**GC-03-RQ1 (primary; candidate research question, not final):**

> Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained smartphone dynamically downgrades its inference configuration under changing device conditions?

| Role | Variables |
| :-- | :-- |
| Independent variables | resource/device state; selected inference configuration; adaptation state |
| Dependent variables | recall; precision; F1; mAP where appropriate; calibration/error; latency; energy/power; temperature; memory; recapture rate; escalation rate |
| Potential mediating variable | confidence threshold / uncertainty |

**Falsified if:** confidence-aware verification does not recover recall beyond the downgraded baseline, or recovers it only at a cost equal to running the static best configuration.

**The hypothesis is not proven.** No experiment has been run.

## 4. Evidence Supporting the Candidate

All of this is evidence already established in Steps 9.7, 9.8, 9.9A and 9.9B. No new evidence was gathered in Step 9.9C.

- **Step 9.7 (frozen corpus).**
  - No core record meets three of the Step 9.7 components.
  - In scope, `confidence_gating` is Yes for one record (P016, an edge device, not a smartphone).
  - The only verified smartphone visual-inspection record, P011, is No for adaptation and gating.
- **Step 9.8.**
  - The narrowed wording was set (Decisions A–C).
  - Confidence-triggered verification was found at the edge (PMC11435656, SAEC) and with backend inference (RobustDefect-LLM), but not on a smartphone and not resource-driven.
  - No full counterexample appeared in 16 GC-03 searches.
- **Step 9.9A.**
  - GC-03 was evaluated against criteria A–Q and gate Q1–Q10.
  - Q4 (precision) and Q9 (quantitative evidence) are satisfied; Q1, Q3, Q5, Q6 and Q7 are partially satisfied.
- **Step 9.9B.**
  - End-to-end full-text reads:
    - PMC11435656: confidence-only routing on Raspberry Pi 4, `resource_awareness` No;
    - ActiveInspect: fixed observation budget on an A100, `resource_awareness` No;
    - PMC10280690: not a counterexample.
  - 12 further GC-03 searches (S46–S57) found no full counterexample.
  - No record meets four criteria with only the fifth unresolved.

## 5. Counterexamples

**Full counterexamples identified: 0**

A full counterexample must have `smartphone`, `visual_inspection`, `resource_awareness`, `adaptive_inference` and `confidence_gating` all Yes.

**Partial counterexamples** (at least one criterion clearly failed):

| Paper | Clearly fails |
| :-- | :-- |
| PMC11435656 (full text) | smartphone, resource awareness |
| SAEC, arXiv 2509.17136 (full text) | smartphone, resource awareness |
| RobustDefect-LLM, arXiv 2608.08589 (full text) | smartphone, resource awareness, adaptive inference |
| ActiveInspect, doi 10.3390/s26154932 (full text) | smartphone, resource awareness |
| arXiv 2608.14727 (full text) | smartphone, resource awareness |
| P011, XEdgeAI (full text) | resource awareness, adaptive inference, confidence gating |
| P016 (full text) | smartphone, resource awareness, adaptive inference |
| P007 (abstract) | smartphone |
| Yan et al. 2025, IEEE Access (abstract) | smartphone |
| RAMS, arXiv 2606.14716 (snippet) | visual inspection |
| HAPI, arXiv 2008.03997 (snippet) | visual inspection |

**Potential counterexamples** (no criterion clearly failed; key criteria Unknown):

| Paper | Evidence level |
| :-- | :-- |
| P001 | abstract only |
| AIVD, arXiv 2601.04734 | snippet only |
| Choi et al. 2026, IEEE TVT | abstract only |
| Zakaria et al. 2022 | abstract only |
| Electronics 15(17):3915 | snippet only |
| arXiv 2608.21967 | full text; online deferral pipeline not evaluated |

**Unresolved papers:**
- P001 and P007 full texts (publisher hosts blocked);
- AIVD and Choi et al. 2026 full texts;
- ActiveInspect `confidence_gating`, an operational-definition issue.

## 6. Q2 — Unknown Burden

**Conditionally acceptable.**

The remaining Unknown burden is acceptable for a corpus-bounded candidate-gap statement, provided unresolved high-impact papers such as P001 and AIVD are explicitly retained as limitations. The evidence does not justify a universal claim that no counterexample exists.

## 7. Q8 — Contribution Distinctiveness

**Conditionally distinct.**

The individual mechanisms already exist in the literature, and integration alone is not sufficient novelty. The potentially distinctive contribution is the experimentally testable question of whether confidence-aware verification can recover inspection performance lost when resource-driven adaptation downgrades a smartphone inspection configuration, including whether confidence calibration changes across configurations.

## 8. Q10 — Literature Overturn Risk

**Moderate.**

Additional literature could overturn the candidate if a single study demonstrates smartphone-based optical inspection, device-state-driven runtime configuration changes, and confidence-triggered downstream recapture or escalation in one system. P001, AIVD, and Choi 2026 remain particularly important unresolved evidence.

## 9. Candidate Contribution

**CANDIDATE CONTRIBUTION — REQUIRES EXPERIMENTAL VALIDATION**

> An empirical investigation of whether confidence-aware downstream verification can recover inspection performance degraded by resource-driven runtime configuration changes on a resource-constrained smartphone, including analysis of accuracy, calibration, latency, energy, thermal behavior, and verification overhead.

This is not a confirmed contribution. Combining resource-aware inference, smartphone inspection and confidence gating is **not** by itself the contribution; each of those components is already demonstrated in the literature (`configs/gap_selection.yaml`, `contributions.GC-03`).

## 10. Candidate Hypotheses

All hypotheses: **CANDIDATE — NOT YET TESTED**.

| ID | Hypothesis | Status |
| :-- | :-- | :-- |
| H1 | Resource-driven runtime downgrading decreases inspection performance relative to the best static configuration under equivalent task conditions. | CANDIDATE — NOT YET TESTED |
| H2 | Confidence-aware downstream verification recovers a measurable portion of the performance degradation introduced by resource-driven downgrading. | CANDIDATE — NOT YET TESTED |
| H3 | Confidence-aware verification introduces measurable computational and/or energy/latency overhead. | CANDIDATE — NOT YET TESTED |
| H4 | Confidence distributions and calibration characteristics differ between inference configurations operating under different resource conditions. | CANDIDATE — NOT YET TESTED |
| H5 | A joint resource-adaptation + confidence-verification policy provides a more favorable accuracy–efficiency trade-off than either mechanism alone. | CANDIDATE — NOT YET TESTED |

## 11. Candidate Experimental Design

This is a planning artifact only: nothing is implemented, no experiments have been run, no results are reported and no device measurements exist.

| Baseline | Resource adaptation | Confidence verification |
| :-- | :-- | :-- |
| B1 — Static best model | No | No |
| B2 — Static lightweight model | No | No |
| B3 — Resource adaptation only | Yes | No |
| B4 — Confidence verification only | No | Yes |
| B5 — Resource adaptation + confidence verification | Yes | Yes |

**Planned comparisons (Proposed idea):**
- B3 vs B1: degradation from downgrades (H1).
- B5 vs B3: recovery by verification (H2).
- B5 vs B1/B3: verification overhead (H3).
- Per-configuration calibration (H4).
- B5 vs B3 and B4: joint trade-off (H5).

Device models, tolerances, thresholds and run counts are Assumptions to be pre-registered in `configs/`. The minimum viable experiment is described in [`gc03_evidence_closure.md`](gc03_evidence_closure.md) §15.

## 12. Dataset Feasibility

The reviewed dataset candidates appear technically suitable for visual-defect inspection experiments, but access, licensing, smartphone suitability, and multi-view/recapture suitability require dataset-specific verification.

| Category | Status (13 Step 9.9A entries) |
| :-- | :-- |
| 1. Existing visual inspection datasets | All 13 entries describe visual-defect inspection data as recorded in the repository (technical suitability only, unverified). |
| 2. Multi-view-capable datasets | Real-IAD, MANTA and MVTec3D-AD/Eyecandies, as recorded in the corpus. Access unverified. |
| 3. Datasets suitable for replay | In principle any image set could be replayed through an on-phone model. Unverified per dataset. |
| 4. Datasets requiring custom smartphone capture | Physical recapture and smartphone-domain realism need a custom phone-captured set (Proposed idea). No existing entry is verified as smartphone-captured. |
| 5. Dataset access/license status | Not verified for any entry: all 13 are `verification_required` or `unknown`. |

The 13 datasets are **not** claimed to be available, licensed or smartphone datasets.

## 13. Known Limitations

- **Full texts unresolved:**
  - P001 (potential; Wiley host blocked);
  - P007 (partial at abstract level; host blocked);
  - AIVD, arXiv 2601.04734 (potential; snippet only; arXiv and alphaXiv unreachable);
  - Choi et al. 2026 (potential; abstract only);
  - Zakaria et al. 2022 and Electronics 15(17):3915 (potential).
- **DOIs not verified** for the Consensus-sourced records (Yan 2025, Choi 2026, Zakaria 2022).
- **ActiveInspect `confidence_gating`** remains an operational-definition issue: Decision B "explicitly informs" vs Step 9.9B "explicitly triggers". It does not change its partial status.
- **Search limitations:**
  - access to IEEE Xplore, ACM DL, Scopus and Web of Science was substituted (domain-restricted WebSearch, Consensus, PubMed), not direct;
  - English only; one results page per search; domain filters leaked.
- **Unknown burden.** The corpus Unknown burden remains high (about 23–24 of 27 in-scope records Unknown per runtime or gating field). Unknown is never treated as No.
- **Hypotheses and contribution** are candidates only; nothing has been tested.
- **Datasets:** access, licence and smartphone/recapture suitability are unverified.
- **Evidence closure was performed for GC-03 only.** GC-01 and GC-02 keep their Phase A gate status.
- **P013 Tables 4–5** remain visually unverified (peripheral record; not used as a gap signal).

## 14. Researcher Decision

DECISION: PENDING EXPLICIT RESEARCHER APPROVAL
