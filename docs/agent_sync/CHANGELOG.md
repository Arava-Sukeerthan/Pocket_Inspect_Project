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
