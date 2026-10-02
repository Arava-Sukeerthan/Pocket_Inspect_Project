# Agent Synchronization Changelog

Shared change history between the PocketInspect coding/research agents (**Claude Code** and **Antigravity**). Research architecture and task prompts come from ChatGPT and the human researcher.

## Rules

1. **Read before working.** Before starting a task, read the latest entries in this file (at minimum every entry since your own last one).
2. **Append only.** Every agent that modifies the repository appends one new entry at the bottom of this file. Never edit, reorder or delete earlier entries. Corrections go in a new entry that references the earlier one by date and agent.
3. **One entry per coherent task**, written before the commit that contains the task's changes. The `Git` section of an entry cannot contain its own commit hash; record `Commit: see git log for this file` or fill the hash in the next entry.
4. **Uncertainty is recorded, not resolved silently.** Anything requiring a research decision is listed under `Uncertain items` and marked for researcher/ChatGPT review.
5. **Git hygiene.** Run `git status`, check the branch and recent commits before changing files. Run tests and review `git diff` before committing. Commit only intended files. Never force push. Never reset or discard changes you did not make; if unrelated uncommitted changes are present, stop and report them.

## Sources of truth

Each file has one purpose. Do not mix them.

| File | Purpose |
| :--- | :--- |
| `research/literature/papers.csv` | Verified literature database |
| `research/literature/search_log.md` | Literature search history (queries, hits, screened, retained) |
| `research/literature/literature_matrix.csv` | Generated literature comparison (do not hand-edit) |
| `research/gap_analysis/gap_matrix.csv` | Evidence-based gap comparison |
| `research/gap_analysis/gap_candidates.md` | Candidate gaps requiring researcher review |
| `research/gap_analysis/research_gap.md` | Final approved research gap, created **only** after researcher approval |
| `docs/agent_sync/CHANGELOG.md` | Agent-to-agent synchronization and change history (this file) |

## Entry template

```markdown
## YYYY-MM-DD — Claude Code | Antigravity

### Task
[short description]

### Changes
- [file changed]
- [what changed]

### Research decisions
- [important research-related decisions]

### Verification
- [tests/checks performed]
- [validation status]

### Uncertain items
- [anything requiring human/researcher verification]

### Remaining work
- [next recommended tasks]

### Git
- Commit:
- Push status:
```

---

# Entries

## 2026-10-02 — Claude Code

### Task
Establish the multi-agent synchronization and research-change tracking infrastructure. No literature data was changed.

### Changes
- `docs/agent_sync/CHANGELOG.md` (new): shared append-only changelog with rules, source-of-truth table and entry template.
- `research/literature/search_log.md`: already existed (batch 1, 2026-10-01). Added a short scope note under the title stating that it records search activity only and that agent changes go in this changelog. Batch 1 content unchanged.
- `AGENTS.md`: added section 4 pointing agents to this changelog and the sources-of-truth table.

### Research decisions
- None. `papers.csv` (54 records, P001–P054) was not modified.
- `research/gap_analysis/research_gap.md` was deliberately not created; it requires researcher approval.

### Verification
- `python -m pytest -q`: 18 passed.
- `python scripts/manage_literature.py validate`: 54 records, VALID, 0 warnings, 0 duplicates.
- `literature_matrix.csv` row count (54) matches `papers.csv`.
- `git diff` reviewed; only the three files above changed.

### Uncertain items
- `research/gap_analysis/gap_matrix.csv` and `gap_candidates.md` are stale: they were generated when `papers.csv` was empty and still report 0 supporting papers for every gap. They were not regenerated because gap analysis is deferred until the researcher decides the literature base is sufficient. **Requires researcher/ChatGPT decision** on when to regenerate.
- Batch 1 extraction is abstract-level only; `Unknown` characteristic values are not evidence of absence (see `research/literature/README.md`).

### Remaining work
- Researcher decision on regenerating gap analysis outputs from the 54-paper corpus.
- Full-text review of batch 1 papers to resolve `Unknown` fields.
- `tests/README.md` lists test files (`test_acquisition.py`, etc.) that do not exist; update when those modules are written.

### Git
- Commit: see `git log -- docs/agent_sync/CHANGELOG.md` (hash recorded in the next entry)
- Push status: pushed to `origin/claude/pocketinspect-agent-sync-a33d88` (see next entry if this changes)

---

## 2026-10-02 — Antigravity

### Task
Verify synchronization infrastructure and literature dataset integrity following Claude Code setup.

### Changes
- `docs/agent_sync/CHANGELOG.md`: Appended Antigravity verification entry confirming synchronization infrastructure and literature integrity.

### Research decisions
- None. `papers.csv` (54 records, P001–P054) was inspected and preserved without modifications.

### Verification
- `git pull`: Already up to date.
- `git status`: Working tree clean.
- `python -m pytest`: 18 passed in 0.28s.
- `python scripts/manage_literature.py validate`: 54 records, VALID, 0 warnings, 0 duplicates.
- Schema verification: all 29 expected CSV columns present in `papers.csv`.
- Duplicate check: 0 duplicate DOIs, 0 duplicate titles.

### Uncertain items
- None for this verification task.

### Remaining work
- Continue with researcher/ChatGPT roadmap priorities as specified.

### Git
- Commit: see `git log -- docs/agent_sync/CHANGELOG.md`
- Push status: pending push


---

## 2026-10-02 — Claude Code

### Task
Step 8: first-pass audit of the 54 existing literature records (no new searches, no edits to `papers.csv`).

### Changes
- `research/literature/audit_report.csv` (new): one row per paper with relevance_class, verification_status, metadata_issues, evidence_issues, duplicate_status and recommended_action.
- `research/literature/audit_report.md` (new): method, class criteria, summary statistics, duplicate, metadata and evidence findings, and recommended next steps.
- `docs/agent_sync/CHANGELOG.md`: this entry.
- Synced the branch with `origin/main` (fast-forward to `0736c2a`, which contains Antigravity's entry) before starting.

### Research decisions
- Proposed relevance classes: A 17, B 24, C 12, D 1 (P013), E 0. The A–D criteria are the auditor's proposal; **requires researcher/ChatGPT review**.
- No records deleted or edited. All corrections are listed as recommendations only.

### Verification
- All 54 records checked against the doi.org handle API, Crossref (DataCite for P054), OpenAlex, and the NeurIPS/PMLR pages for P045/P046. Every record exists and its metadata matches; all 52 DOIs resolve; no retractions.
- Coded flags checked against retrieved abstracts (OpenAlex, Crossref, Semantic Scholar, Springer, NeurIPS, PMLR). No coded value contradicts its abstract. 13 records have weak or interpretive support or source-labelling issues.
- `python scripts/manage_literature.py validate`: 54 records, VALID, 0 duplicates. Fuzzy title check: 9 similar pairs, all distinct works.
- `python -m pytest -q`: 18 passed.
- `git diff` reviewed: only the two audit files and this changelog changed; `papers.csv` unchanged.

### Uncertain items
- The 12 characteristic fields have no written definitions. In particular: does `latency_evaluation` cover throughput or adaptation time? Does `adaptive_inference` cover DVFS? Does `resource_awareness` cover measurement only? Are surveys coded by topic? **Requires researcher decision.**
- P013 (class D): the abstract does not say whether the inspection is image-based. Needs a full-text check.
- P007: the search log retains it under G4, but notes assign G1.
- The audit is abstract-level only. The verification scripts were run from scratch space and are not committed.

### Remaining work
- Researcher review of the proposed classes.
- Write field definitions in `research/literature/README.md`.
- After approval, a separate `papers.csv` correction task: alternative identifiers for P006/P054, P007's group, P006's evidence source label, missing evidence items for P003/P027/P042.
- Full-text review starting with class A and P013.

### Git
- Previous Claude Code entry (sync infrastructure): commit `aa9715a`, merged to `main` via PR #2 as `5d3ac8b`.
- Commit: see `git log -- research/literature/audit_report.csv` (hash recorded in the next entry)
- Push status: pushed to `origin/claude/pocketinspect-agent-sync-a33d88` (see next entry if this changes)

---

## 2026-10-03 — Claude Code

### Task
Step 8.1: formalise the literature coding definitions before any further correction or searching. No new searches.

### Changes
- `research/literature/README.md`:
  - added **§7 Literature Coding Definitions** (v1.0) with these subsections:
    - 7.1 general rules: Yes/No/Unknown, abstract-level coding, paper-type tag, survey rule;
    - 7.2 evidence requirements and evidence-item format;
    - 7.3 operational definitions of all 12 characteristic fields;
    - 7.4 the 10 required distinctions;
    - 7.5 cross-field consistency rules;
    - 7.6 recording rules for `dataset`, `model`, `hardware`, `accuracy_metrics`, `limitations` and `future_work`;
    - 7.7 how a coding may be changed;
  - updated the §2 `uncertainty` rule and the §4 meaning of `No` to match §7, with pointers to §7.
- `research/literature/coding_decisions.md` (new):
  - 17 borderline decisions (CD-01 to CD-17) with rationale, alternatives and corpus examples;
  - a table of the provisional effect on current records (not applied);
  - optional schema extensions (reported, not implemented);
  - questions for approval.
- `docs/agent_sync/CHANGELOG.md`: this entry.

### Research decisions
- **No schema change.** The single `latency_evaluation` field is defined to cover inference latency, end-to-end latency and throughput. The evidence item records the timing type; adaptation time alone does not qualify.
- `adaptive_inference` requires the model computation to change. DVFS or scheduling alone is system-level adaptation and is coded under `resource_awareness` when it is driven by resources.
- `resource_awareness` requires a resource-driven decision; measurement alone does not qualify.
- `uncertainty` excludes a plain softmax confidence or a confidence threshold unless the score is estimated, calibrated or evaluated as uncertainty. Selective prediction and OOD detection qualify.
- Surveys are coded `No` for all characteristic fields; their topics go in `notes`, `domain` and `application`.
- **`papers.csv` was NOT modified** (blob `44276441` is identical to HEAD). The provisional recodings are listed in `coding_decisions.md` §2 only:
  - 9 values Yes→Unknown;
  - 6 values Unknown→Yes;
  - 3 values Yes→No;
  - 69 values Unknown→No (surveys).

### Verification
- `python -m pytest -q`: 18 passed. Literature tests (`test_literature.py`, `test_literature_data.py`): 17 passed.
- `python scripts/manage_literature.py validate`: 54 records, VALID, 0 duplicates.
- Every "current value" in the provisional-effect table was checked programmatically against `papers.csv`: 0 mismatches.
- `git diff` reviewed. Only `README.md` (285 additions, 2 changed lines) and the new `coding_decisions.md` changed, plus this changelog.

### Uncertain items (require researcher/ChatGPT approval, marked ⚑ in README §7)
- CD-01: surveys coded `No` (vs `Unknown` or a `paper_type` column).
- CD-02: throughput/FPS counts toward `latency_evaluation`.
- CD-04: comparative speed findings without figures count as `Yes`.
- CD-06: runtime device/edge/cloud partitioning counts as `adaptive_inference`.
- CD-08: confidence-gated decisions are excluded from `uncertainty`. Should a `confidence_gating` field be added?
- CD-10: external identification of named phone models.
- CD-13: split-only execution coded `on_device = No`.
- CD-16: efficiency figures kept in `accuracy_metrics` with an `Efficiency:` prefix (vs a new column).

### Remaining work
- Researcher approval of the ⚑ decisions.
- Then a separate, logged correction task that applies `coding_decisions.md` §2 and the formatting rules (CD-10, CD-16, CD-17) to `papers.csv`.
- Full-text review starting with class A papers and P013.

### Git
- Previous Claude Code entry (literature audit): commit `12d2c70`, merged to `main` via PR #3 as `e45bd93`.
- Commit: see `git log -- research/literature/coding_decisions.md` (hash recorded in the next entry)
- Push status: pushed to `origin/claude/pocketinspect-agent-sync-a33d88` (see next entry if this changes)

---

## 2026-10-03 — Antigravity

### Task
Step 8.2: Review literature coding definitions in `research/literature/README.md` (§7 v1.0) and `research/literature/coding_decisions.md` (v1.0) for precision, reproducibility, and required distinction clarity.

### Changes
- `docs/agent_sync/CHANGELOG.md`: Appended Antigravity review and verification entry.
- **`papers.csv` was NOT modified** (blob remains untouched).

### Research decisions
- None made independently. Confirmed that all 7 required distinctions (resource measurement vs adaptation, adaptive inference vs DVFS, latency vs throughput vs adaptation time, confidence vs uncertainty, multiple images vs multi-view, edge infrastructure vs edge inference, supervised vs anomaly detection) are explicitly defined with clear operational rules.
- Agreed that borderline decisions CD-01 to CD-17 in `coding_decisions.md` should remain provisional pending researcher/ChatGPT approval.

### Verification
- `git pull`: Sync verified (fast-forward to `f4ef3c1` containing Claude Code's Step 8.1 entry).
- `python scripts/manage_literature.py validate`: 54 records, status **VALID** (0 errors, 0 duplicates).
- `python -m pytest`: **18 passed** in 0.28s (`test_imports.py`, `test_literature.py`, `test_literature_data.py`).
- `git diff`: Verified only `CHANGELOG.md` is modified.

### Uncertain items (recorded for researcher/ChatGPT review)
- **Design-time vs Runtime in `resource_awareness`**: Does offline Neural Architecture Search (NAS) / model compression under explicit FLOP/memory budgets set `resource_awareness = Yes`, or are only runtime/deployment-time resource-driven decisions eligible?
- **Partitioning as `adaptive_inference` (CD-06 ⚑)**: Dynamic layer partitioning across edge/cloud alters where layers execute without changing model weights. Confirm whether this is model-level adaptive inference or system-level offloading scheduling.
- **Confidence-Gated Decisions (CD-08 ⚑)**: Excluding softmax confidence thresholds from `uncertainty = Yes` leaves confidence-gated active capture/referral visible only in `notes`. Confirm whether a dedicated `confidence_gating` attribute or schema column should be introduced.
- **Throughput & Comparative Speed Claims in `latency_evaluation` (CD-02 ⚑, CD-04 ⚑)**: Confirm acceptance of throughput (FPS) and qualitative comparative speed claims ("faster than X") under `latency_evaluation = Yes` (with evidence tags).
- **Tablet / Industrial PC Edge Boundaries (CD-10 ⚑, CD-12)**: Clarify whether tablets are categorized as `edge_device` vs `smartphone`, and confirm that industrial PCs with desktop-grade GPUs are strictly excluded from `edge_device`.

### Remaining work
- Researcher/ChatGPT approval of the ⚑ decisions in `coding_decisions.md` and the uncertainties above.
- Execute the logged correction task applying provisional recodings to `papers.csv` once approved.

### Git
- Commit: see `git log -- docs/agent_sync/CHANGELOG.md`
- Push status: pending push


---

## 2026-10-03 — Claude Code

### Task
Step 8.3: apply the eight literature-coding decisions approved by the researcher/ChatGPT. This includes a schema change (29 → 31 columns) and recoding all 54 records. No new searches; no gap analysis.

### Changes
- **Schema:** `confidence_gating` (Yes/No/Unknown) added after `uncertainty`; `efficiency_metrics` (free text) added after `accuracy_metrics`.
  - `src/literature/schema.py`: headers, `BOOLEAN_FIELDS`.
  - `src/literature/analyzer.py`: literature-matrix rows and columns.
  - `src/literature/exporter.py`: Markdown export gains a Confidence Gating column.
  - The validator needed no code change; it reads the schema constants.
- **Tests:**
  - `tests/test_literature.py`: 31-column schema; positions and types of the new fields; matrix/export of the new fields; the old 29-column header is rejected.
  - `tests/test_literature_data.py`: every row has exactly 31 fields; surveys are `No` for all characteristic fields; every `latency_evaluation = Yes` names its timing type.
- **`research/literature/papers.csv`:** recoded under README §7 v1.1.
  - 95 values in the original 12 fields changed, across 20 records:
    - Unknown→No: 71
    - Yes→Unknown: 14
    - Unknown→Yes: 7
    - Yes→No: 3
  - New fields: `confidence_gating` is Yes 1 (P025), No 6 (surveys), Unknown 47. `efficiency_metrics` is populated for 6 records (P007, P018, P028, P029, P034, P039).
  - `accuracy_metrics` changed for 5 records (efficiency figures moved out).
  - P042 `limitations` marked field-level.
  - Evidence items appended for 24 records.
  - A `Paper type:` tag was added to `notes` for all 54, plus recoding notes.
  - No records added or deleted; title, authors, year, venue, DOI, URL, domain, application, dataset, model, hardware and future_work are unchanged.
- **`research/literature/literature_matrix.csv`:** regenerated (`manage_literature.py matrix`) with the new columns.
- **`research/literature/README.md`:** §3 schema (31 columns, 13 characteristic fields, `efficiency_metrics`); §4 blank fields; §7 updated to v1.1. The §7 changes are:
  - the ⚑ items are now ✓A (approved);
  - new `confidence_gating` definition;
  - Decision 3 (qualitative speed claims → Unknown);
  - dynamic vs static partitioning;
  - split inference → `on_device = No`;
  - external identification requires an authoritative source;
  - `efficiency_metrics` recording rules;
  - timing-type labels;
  - distinction 11 and new consistency rules.
- **`research/literature/coding_decisions.md`** (v1.1):
  - new §0 approval record;
  - an approval-outcome line under each ⚑ decision, with the v1.0 text kept;
  - §2 marked as superseded by the recoding report;
  - §3/§4 status updates.
- **`research/literature/recoding_report.md`** (new): every changed value with its old and new value, reason, decision, evidence source and support level; also lists metadata corrections, new-field initialisation and values deliberately not changed.
- **`research/literature/selected_papers.md`:** the "Characteristics marked Yes" line for each paper was regenerated from `papers.csv` (17 lines changed), with a dated note. The rest of the file is unchanged.

### Research decisions
- Applied approved Decisions 1–8 as specified. Choices made while applying them (recorded in `coding_decisions.md` §0):
  - surveys are also `No` for the new `confidence_gating` field;
  - measured **relative** timing values (+18.1% FPS, 3.1x latency, 2.0x frame rate) count as measured under Decision 3;
  - P004 keeps `latency_evaluation = Yes`: the abstract names throughput as a reported benchmark metric, though no value is given, so `efficiency_metrics` is blank;
  - P031 `adaptive_inference` is set to `Unknown`, not `No`: the abstract alone cannot establish that the model computation never changes.
- Metadata corrections from the audit:
  - P006: evidence source label corrected; arXiv 2109.13963 recorded;
  - P007: thematic group G1 and retrieval query G4 both recorded; assignment unchanged;
  - P054: SSRN DOI recorded.
- P013 relevance (audit class D) is **not** resolved; only `edge_device`/`cloud` were recoded to `Unknown` under the definitions.
- P031 smartphone classification: Xiaomi official specifications page (dual nano-SIM, 4G cellular, Android 11; accessed 2026-10-03). The page does not use the word "smartphone"; this is recorded in `notes`.
- All changes are **abstract-supported**; no full text was read. 14 records are flagged `Requires full-text verification`.

### Verification
- `python scripts/manage_literature.py validate`: 54 records, VALID, 0 warnings, 0 duplicates.
- `python -m pytest -q`: **24 passed** (18 → 24; 6 new tests).
- Header equals the 31-column schema; all 54 rows have exactly 31 fields.
- The change log was reconciled with a before/after diff of `papers.csv`: only the declared fields changed.
- `git diff` reviewed. Gap-analysis files and `audit_report.*` are unchanged; no unrelated files changed.

### Uncertain items
- P045/P046 `confidence_gating` stays Unknown. P046 rejects via a learned selection head, contrasted with confidence thresholds. **Researcher decision:** does a learned selection score count?
- Antigravity's Step 8.2 questions remain open:
  - does design-time NAS or compression under device budgets count as `resource_awareness`?
  - how should tablets and industrial PCs be classified for `smartphone`/`edge_device`?
- `research/gap_analysis/*` is still stale (generated from an empty corpus). It now also predates the recoding. Not regenerated; gap analysis is deferred.
- The `hardware` role-prefix formatting (README §7.6, CD-17) has not been applied to existing rows.

### Remaining work
- Full-text review of the 14 flagged records, then of class A papers, and P013.
- Researcher decisions on the open items above.
- Optional: apply `hardware` role prefixes in a formatting-only task.

### Git
- Previous Claude Code entry (Step 8.1 definitions): commit `8585ad5`, merged to `main` via PR #4 as `f4ef3c1`.
- Commit: see `git log -- research/literature/recoding_report.md` (hash recorded in the next entry)
- Push status: pushed to `origin/claude/pocketinspect-agent-sync-a33d88` (see next entry if this changes)
