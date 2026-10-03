# Gap Analysis Subsystem (`research/gap_analysis/`)

This directory maintains systematic research gap matrices, candidate lists, and decision records for PocketInspect.

---

## 1. Research Gap Analysis Principles

1. **Evidence-Based Gaps Only**: Gaps are identified exclusively by analyzing coverage across verified publications ingested into `research/literature/papers.csv`.
2. **No Automatic Novelty Claims**: Zero-coverage dimension intersections are tagged as `Candidate Gaps (Requires Researcher Verification)`, never as absolute novel contributions until verified.
3. **Epistemic Hygiene**: Unsupported assumptions or missing literature fields are marked as `unknown`, not inferred.

---

## 2. Key Research Dimensions Evaluated

The evaluated combinations, analysis populations and derived attributes are declared in [`configs/gap_analysis.yaml`](../../configs/gap_analysis.yaml) (Step 9.7). The current set is combinations C-A to C-L plus supplementary checks C-S1 to C-S5.

- Each combination reports three groups of core records:
  - all-Yes records (counterexamples to a gap claim);
  - unresolved records (Unknown);
  - records excluded by an explicit No.
- `Unknown` is never treated as `No`.
- Peripheral/contextual records (researcher-approved: P002, P013) are reported separately and are not counted as core evidence.
- The frozen evidence base is recorded in [`corpus_freeze.md`](corpus_freeze.md).

The earlier hard-coded prototype combinations (GAP-001 to GAP-006, generated when the corpus was empty) are retired. They remain only as the fallback used when no configuration file is present.

---

## 3. Workflow for Researcher Gap Verification

1. Ingest candidate literature into `research/literature/papers.csv`.
2. Run `python scripts/manage_literature.py gap` (reads `configs/gap_analysis.yaml`) to regenerate `gap_matrix.csv` and `gap_candidates.md`. If `papers.csv` no longer matches the freeze hash in the config, the report warns that the candidate narratives need re-review.
3. Review `gap_candidates.md` to verify whether candidate gaps are genuine research opportunities or missing literature.
4. Record final decision in `docs/decisions/` before freezing the paper contribution.
