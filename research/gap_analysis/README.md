# Gap Analysis Subsystem (`research/gap_analysis/`)

This directory maintains systematic research gap matrices, candidate lists, and decision records for PocketInspect.

---

## 1. Research Gap Analysis Principles

1. **Evidence-Based Gaps Only**: Gaps are identified exclusively by analyzing coverage across verified publications ingested into `research/literature/papers.csv`.
2. **No Automatic Novelty Claims**: Zero-coverage dimension intersections are tagged as `Candidate Gaps (Requires Researcher Verification)`, never as absolute novel contributions until verified.
3. **Epistemic Hygiene**: Unsupported assumptions or missing literature fields are marked as `unknown`, not inferred.

---

## 2. Key Research Dimensions Evaluated

The evaluated combinations, analysis populations, derived attributes and candidate definitions are declared in [`configs/gap_analysis.yaml`](../../configs/gap_analysis.yaml) (Step 9.7, revised).

- **Core-analysis subset (46 records).** The 54-record corpus minus the researcher-approved peripheral/contextual records (P002, P013) and the six survey/review records. All excluded records stay in `papers.csv`; review `No` values are never evidence of absence.
- **Visual-inspection scope.** `visual_inspection_scope` (Yes/No/Unknown) is an analysis-only classification with a written basis per paper in [`visual_inspection_scope.csv`](visual_inspection_scope.csv). It is not a column of `papers.csv`.
- **Combinations.** For each combination, a core record inside its scope is all-Yes (a counterexample), unresolved (Unknown) or excluded by an explicit No. `Unknown` is never treated as `No`.
- **Outputs.**
  - [`gap_matrix.csv`](gap_matrix.csv): one row per candidate, separated into evidence-supported candidate gaps and evidence limitations / unresolved questions;
  - [`combination_matrix.csv`](combination_matrix.csv): one row per combination;
  - [`gap_candidates.md`](gap_candidates.md): the report.
- **No ranking or selection.** No candidate is scored, ranked or selected. `research_gap.md` is never written by the tool.
- The frozen evidence base is recorded in [`corpus_freeze.md`](corpus_freeze.md).
- **Step 9.8 candidate evaluation.** Framework and guard-rails are in [`configs/gap_evaluation.yaml`](../../configs/gap_evaluation.yaml); `src/literature/gap_evaluation.py` validates the artefacts (read-only).
  - [`counterexample_candidates.csv`](counterexample_candidates.csv): every paper assessed as a possible counterexample to GC-01 to GC-03. External papers are kept here only, never added to `papers.csv`.
  - [`targeted_search_log.md`](targeted_search_log.md): the targeted disproof searches, with counts and limitations.
  - [`candidate_gap_matrix.csv`](candidate_gap_matrix.csv): qualitative candidate × criterion assessments (14 criteria; no scores).
  - [`candidate_gap_evaluation.md`](candidate_gap_evaluation.md): the written evaluation. It does not rank or select a candidate.
  - Step 9.8 methodology correction (researcher-approved): narrowed GC-01/GC-02/GC-03 wording, operational Decisions A–C (content-driven cascades; learned view selection; in-sensor processors) and four confirmed partial counterexamples, all recorded in `configs/gap_evaluation.yaml` and §3.4 of the evaluation. The Step 9.7 files keep the original wording as the historical record.

The earlier hard-coded prototype combinations (GAP-001 to GAP-006) are retired. They remain only as the fallback used when no configuration file is present.

---

## 3. Workflow for Researcher Gap Verification

1. Ingest candidate literature into `research/literature/papers.csv`.
2. Run `python scripts/manage_literature.py gap` (reads `configs/gap_analysis.yaml`) to regenerate `gap_matrix.csv`, `combination_matrix.csv` and `gap_candidates.md`. If `papers.csv` no longer matches the freeze hash in the config, the report warns that the candidate narratives need re-review.
3. Review `gap_candidates.md` to verify whether candidate gaps are genuine research opportunities or missing literature.
4. Record final decision in `docs/decisions/` before freezing the paper contribution.
