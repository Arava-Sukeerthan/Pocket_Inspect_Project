# Corpus Freeze — Step 9.7

_2026-10-03, Claude Code. Branch `claude/affectionate-ride-9uem3p`, started from `main` at the Step 9.6 merge._

This record fixes the exact literature state used as the evidence base for Step 9.7 (gap-candidate analysis). `papers.csv` was **not modified** during the freeze or at any point in Step 9.7. No column was added to represent the freeze.

## Frozen state

| Item | Value |
| :-- | :-- |
| Date | 2026-10-03 |
| Git commit | `c6ba9d5185cd4924e4280345142a5dfd4983666d` (`main` = `origin/main`, merge of PR #8, Step 9.6 recovery) |
| File | `research/literature/papers.csv` |
| SHA-256 | `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521` |
| Records | 54 (P001–P054, sequential) |
| Columns | 31; header identical to `PAPERS_SCHEMA_HEADERS` in `src/literature/schema.py` (13 Yes/No/Unknown characteristic fields) |
| Coding definitions | `research/literature/README.md` §7, version 1.1 |
| Duplicate paper IDs | 0 |
| Duplicate DOIs / titles | 0 / 0 |
| Rows with a wrong field count | 0 |
| `python scripts/manage_literature.py validate` | 54 records, VALID |
| `python -m pytest -q` (before Step 9.7 changes) | 24 passed |

**This corpus is the evidence base for Step 9.7.** Every count in [`gap_matrix.csv`](gap_matrix.csv) and [`gap_candidates.md`](gap_candidates.md) is computed from this file. `configs/gap_analysis.yaml` stores the SHA-256 above. If `papers.csv` changes, `manage_literature.py gap` warns in `gap_candidates.md` that the candidate narratives need re-review.

## Populations used for gap reasoning

The full 54-record corpus stays in `papers.csv`. Gap counts use an **analysis-only** subset. The subset definition is in `configs/gap_analysis.yaml`; nothing in the canonical database was rewritten.

| Population | Records | Status |
| :-- | :-- | :-- |
| Full corpus | 54 | Canonical (`papers.csv`) |
| Peripheral/contextual, not core | P002, P013 | **Researcher-approved** (Step 9.6 recovery; `fulltext_version_verification.md` §13). Reported separately in every combination and never counted as core evidence. Not deleted; no relevance column added; `audit_report.csv` unchanged. |
| Review/survey records | P010, P024, P026, P035, P036, P052 | Analysis-only proposal, pending researcher review. Their coded `No` values describe the review, not the field, so they are never counted as primary evidence of absence. |
| Core primary studies (counted) | 46 | Full corpus minus the two groups above |

**Why no other inclusion rule was used.** The audit A–E relevance classes (`audit_report.csv`) were never approved; they remain proposals and were not used as a filter. The repository has no other formal inclusion rule.

**Derived attributes (analysis-only, pending researcher review).** These are not columns of `papers.csv`. Each is assigned per record in the config, from the `domain`, `application` and `dataset` fields:
- `visual_inspection`: camera/optical image-based inspection of physical objects, components, structures or infrastructure.
- `three_d_print_inspection`: optical inspection of 3D-printed parts.

## Known unresolved evidence in the frozen corpus

- **P013 Tables 4–5.** Not visually verified; `accuracy_metrics` is blank.
  - This is an unresolved evidence field, not evidence of poor accuracy, missing evaluation or a gap.
  - P013 is also peripheral/contextual and not core evidence.
- **Full text not read.** Full text was not obtained for P001, P007, P017, P032 (inaccessible) or for P018, P019, P022, P023 (abstract only). 36 further records are coded from abstracts only.
- **Version limitations.**
  - P029, P031 and P033 were read from same-version camera-ready or journal-layout copies; the ACM PDFs were not compared.
  - P011 Fig. 4 labels were read in arXiv v2 only.

## Generated artifacts regenerated from this freeze

| Artifact | Command | Result |
| :-- | :-- | :-- |
| `research/literature/literature_matrix.csv` | `python scripts/manage_literature.py matrix` | Regenerated. Byte-identical to the committed file (already current after Step 9.6): 54 rows, every coded value matches `papers.csv`. |
| `research/gap_analysis/gap_matrix.csv` | `python scripts/manage_literature.py gap` | Regenerated with `configs/gap_analysis.yaml` (17 combinations). Replaces the stale empty-corpus matrix. |
| `research/gap_analysis/gap_candidates.md` | same | Regenerated: evidence tables plus 9 candidate gaps, all *Pending researcher review*. |

`research/gap_analysis/research_gap.md` does not exist and was not created. No final gap was selected.

## Step 9.7 revision (methodology correction)

The frozen state above is unchanged:
- `papers.csv` SHA-256 `c8fac51d…da521`;
- 54 records, 31 columns;
- 0 duplicate IDs.

The revision changed only the analysis layer, which supersedes the description above:

- **Visual-inspection attribute.** The analysis-only attribute is now `visual_inspection_scope` (Yes/No/Unknown). It is read from [`visual_inspection_scope.csv`](visual_inspection_scope.csv), which gives a written basis for every one of the 54 records. Core-analysis subset: Yes 20, No 19, Unknown 7. It replaces the earlier `visual_inspection` ID lists.
- **3D-print attribute.** `three_d_print_inspection` now means the 3D-print task domain in any modality. It is combined with `visual_inspection_scope` where visual input matters.
- **Core rule unchanged in substance, now documented explicitly.**
  - The 54 records minus P002 and P013 (researcher-approved peripheral) minus P010, P024, P026, P035, P036 and P052 (survey/review) gives 46.
  - The lists do not overlap, so 54 − 2 − 6 = 46, matching the computed subset.
- **Outputs.**
  - `gap_matrix.csv` now has one row per candidate (3 evidence-supported candidate gaps + 6 evidence limitations).
  - Combination-level counts moved to [`combination_matrix.csv`](combination_matrix.csv) (20 combinations).

`research_gap.md` still does not exist. No final gap was selected.
