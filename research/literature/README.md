# Literature Management Subsystem (`research/literature/`)

This directory holds PocketInspect's verified literature records, search logs, human-readable summaries, and the generated literature matrix.

| File | Purpose |
| :--- | :--- |
| `papers.csv` | Main literature database (one row per verified paper, 29-column schema below) |
| `selected_papers.md` | Human-readable summary of every retained paper, with per-claim evidence records, plus rejected/deferred candidates |
| `search_log.md` | Every search batch: date, group, exact query, source, hits, screened count, retained IDs, rationale |
| `literature_matrix.csv` | Generated from `papers.csv` by `scripts/manage_literature.py matrix`. Do not edit by hand. |

> **Status:** Literature collection is ongoing. Nothing in this directory establishes a research gap or a novelty claim (see `RESEARCH_RULES.md`). Gap analysis in `research/gap_analysis/` is deferred until enough verified literature exists and a human researcher reviews it.

---

## 1. How papers are collected

Searches are organised into six groups:

| Group | Theme |
| :--- | :--- |
| G1 | Smartphone / mobile AI / on-device edge AI |
| G2 | Industrial visual inspection |
| G3 | 3D-printed part inspection |
| G4 | Adaptive / resource-aware inference (incl. energy, thermal, latency) |
| G5 | Multi-view / active inspection |
| G6 | Confidence / uncertainty / selective prediction |

For each group:

1. Run keyword queries against a scholarly index (batch 1 used the OpenAlex API). Broad queries are followed by narrower title/abstract queries when results are noisy. Known-item title lookups are allowed but must be labelled as such in `search_log.md`.
2. Screen the top-ranked results for relevance. Peer-reviewed venues and 2019–2026 publications are preferred. Foundational older works are kept only when later work builds on them. arXiv is used only when no peer-reviewed version is found.
3. Record every query, its hit count, how many results were screened and which paper IDs were retained in `search_log.md`.

## 2. How papers are verified

A paper is added only after all of the following succeed:

1. **Existence and metadata**: title, authors, year and venue are cross-checked between Crossref and OpenAlex. When the two disagree on year (online-first vs issue), the Crossref `issued` year is used and the difference is noted in `notes`.
2. **DOI resolution**: the DOI resolves via the doi.org handle API. Papers without a DOI (e.g., NeurIPS, PMLR) must have a verified proceedings landing page in `url`.
3. **Abstract retrieved**: from OpenAlex, Crossref, Semantic Scholar or the publisher landing page. If no abstract can be retrieved, the paper is **deferred**, not guessed.
4. **Evidence-backed fields**: every `Yes` in a characteristic field has a matching evidence item (claim → short paraphrase) in `evidence` and in `selected_papers.md`.

Rules that are never relaxed:
- Never infer `smartphone` from "edge" or "mobile device" wording.
- Never infer `on_device` unless the paper says inference runs on the device.
- Never infer `resource_awareness` just because a model is lightweight or runs on an edge device.
- Never infer `multi_view` unless multiple views or camera angles are actually captured.
- Set `uncertainty` only when confidence or uncertainty is explicitly used or evaluated.

Rejected and deferred candidates are listed with reasons at the end of `selected_papers.md`.

## 3. `papers.csv` schema

29 columns in this exact order (enforced by `src/literature/schema.py`):

| Field | Type | Description |
| :--- | :--- | :--- |
| `paper_id` | String (required) | Sequential ID `P001`, `P002`, … Never reused. |
| `title` | String (required) | Verified full title |
| `authors` | String (required) | Full author list, `;`-separated, as registered in Crossref/OpenAlex |
| `year` | Integer (required) | Version-of-record year (Crossref `issued`) |
| `venue` | String | Journal or proceedings name |
| `doi` | String | Bare DOI (e.g. `10.1109/...`); blank if the paper has no DOI |
| `url` | String | `https://doi.org/<doi>` or the verified proceedings page |
| `domain` | String | Primary domain (e.g. "3D-Print Inspection") |
| `application` | String | Specific target application |
| `dataset` | String | Dataset(s) as stated by the source |
| `model` | String | Model or algorithm as stated by the source |
| `hardware` | String | Hardware platform as stated by the source |
| `smartphone` … `latency_evaluation` | `Yes` / `No` / `Unknown` | 12 characteristic fields: `smartphone`, `edge_device`, `on_device`, `cloud`, `adaptive_inference`, `resource_awareness`, `energy_evaluation`, `thermal_evaluation`, `multi_view`, `uncertainty`, `anomaly_detection`, `latency_evaluation` |
| `accuracy_metrics` | String | Metric values exactly as reported by the source |
| `limitations` | String | Limitations stated by the authors |
| `future_work` | String | Future work stated by the authors |
| `evidence` | String | `[Verified; source: …]` followed by `claim -> evidence` items separated by ` \| ` |
| `notes` | String | Search group, extraction depth/date, caveats |

## 4. What `Unknown`, `No` and blank mean

- **`Unknown`** means the examined source (currently the abstract) does not establish the characteristic. It is **not** evidence of absence and must never be converted to `No` without a full-text check.
- **`No`** is used only when the source explicitly describes a contrary setup (e.g., the hardware is stated to be a Raspberry Pi, so `smartphone = No`).
- **Blank free-text fields** (`limitations`, `future_work`, `accuracy_metrics`) mean nothing was extracted at the current extraction depth, not that none exists.
- The validator also accepts legacy `true`/`false`/empty values (see `src/literature/schema.py`). New records should use `Yes`/`No`/`Unknown`.

Batch 1 extraction is **abstract-level**. Full-text review will upgrade `Unknown` fields and fill limitations and future work; each upgrade needs a new evidence item.

## 5. Duplicate handling

Before a paper is added:
1. Compare its normalised DOI (lower-case, `https://doi.org/` stripped) with existing rows.
2. Compare its normalised title (lower-case alphanumerics only) with existing rows.
3. If the same work has several DOIs (e.g., an arXiv preprint and a peer-reviewed version, or ACM reprints in SIG newsletters), keep **one** row for the version of record and record the other identifiers in `notes`.

`python scripts/manage_literature.py validate` reports duplicate IDs, DOIs and titles. `tests/test_literature_data.py` fails if the committed `papers.csv` has any.

## 6. Running the literature tools

```bash
# Validate papers.csv schema and check for duplicates
python scripts/manage_literature.py validate

# Summary statistics over the characteristic fields
python scripts/manage_literature.py stats

# Regenerate literature_matrix.csv
python scripts/manage_literature.py matrix

# Export literature matrix to LaTeX or Markdown
python scripts/manage_literature.py export --format latex --out research/tables/literature_table.tex

# Run the test suite (schema, validator and committed-data integrity)
python -m pytest -q
```

`python scripts/manage_literature.py gap` (and `all`, which calls it) regenerates `research/gap_analysis/gap_matrix.csv` and `gap_candidates.md`. Do not run them as part of routine literature updates; gap analysis is deferred until a human researcher decides the literature base is sufficient.
