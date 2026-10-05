"""
Configuration-driven combination gap analysis for PocketInspect.

Reads characteristic combinations, analysis populations, derived attributes
and candidate definitions from a YAML file (``configs/gap_analysis.yaml``) and
evaluates them against ``research/literature/papers.csv``.

The analysis is descriptive and corpus-bounded:

* every characteristic is read three-valued; ``Unknown`` is never treated as
  ``No`` and never counts as evidence of absence;
* researcher-approved peripheral records and review/survey records stay in the
  canonical corpus but are not counted as primary evidence;
* derived attributes (e.g. ``visual_inspection_scope``) are analysis-only and
  are read from a per-paper classification file with a documented basis;
* candidates are separated into evidence-supported candidate gaps and evidence
  limitations; none is scored, ranked, selected or written to
  ``research_gap.md``.
"""
import csv
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.literature.schema import BOOLEAN_FIELDS, PAPERS_SCHEMA_HEADERS, parse_boolean_field

YES, NO, UNKNOWN = "Yes", "No", "Unknown"
TRI_VALUES = (YES, NO, UNKNOWN)
REVIEW_STATUS = "Pending researcher review"

CATEGORY_GAP = "candidate_gap"
CATEGORY_LIMITATION = "evidence_limitation"
CATEGORY_LABELS = {
    CATEGORY_GAP: "Evidence-supported candidate gap",
    CATEGORY_LIMITATION: "Evidence limitation / unresolved question",
}

# Keys that would turn a candidate list into a ranking or a selection.
FORBIDDEN_CANDIDATE_KEYS = ("score", "rank", "ranking", "priority", "final", "selected", "weight")

CLASSIFICATION_POPULATIONS = ("core", "peripheral/contextual", "review/survey")

GAP_MATRIX_FIELDS = [
    "candidate_gap",
    "category",
    "description",
    "primary_combination",
    "criteria",
    "supporting_papers",
    "counterexamples",
    "relevant_core_papers",
    "yes_count",
    "no_count",
    "unknown_count",
    "evidence_basis",
    "evidence_limitations",
    "visual_inspection_basis",
    "researcher_review_status",
]

COMBINATION_MATRIX_FIELDS = [
    "combination_id",
    "label",
    "research_dimensions",
    "criteria",
    "scope",
    "records_in_scope",
    "all_yes_count",
    "all_yes_ids",
    "unresolved_count",
    "unresolved_ids",
    "excluded_by_no_count",
    "excluded_by_no_ids",
    "near_miss",
    "out_of_scope_matches",
    "review_record_ids",
    "peripheral_results",
    "coverage_observation",
    "corpus_sha256",
    "review_status",
]


def file_sha256(path: str | Path) -> str:
    """SHA-256 of a file's bytes."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tri(value: Any) -> str:
    parsed = parse_boolean_field(value)
    if parsed is True:
        return YES
    if parsed is False:
        return NO
    return UNKNOWN


def _ids(ids: List[str]) -> str:
    return "; ".join(ids) if ids else "None"


def _text(value: Any) -> str:
    return " ".join(str(value or "").split())


def load_classification_file(path: str | Path, column: str) -> Dict[str, Dict[str, str]]:
    """Reads an analysis-only per-paper classification CSV into {paper_id: row}."""
    with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out: Dict[str, Dict[str, str]] = {}
    for row in rows:
        pid = (row.get("paper_id") or "").strip()
        if not pid:
            raise ValueError(f"{path}: row without paper_id")
        if pid in out:
            raise ValueError(f"{path}: duplicate paper_id {pid}")
        if column not in row:
            raise ValueError(f"{path}: missing column '{column}'")
        out[pid] = row
    return out


class CombinationGapAnalyzer:
    """Evaluates configured characteristic combinations and candidates over literature records."""

    def __init__(self, records: List[Dict[str, str]], config: Dict[str, Any],
                 corpus_sha256: str = ""):
        self.records = records
        self.config = config
        self.corpus_sha256 = corpus_sha256
        pops = config.get("populations", {})
        self.peripheral_ids = list(pops.get("peripheral_contextual", {}).get("paper_ids", []))
        self.review_ids = list(pops.get("review_records", {}).get("paper_ids", []))
        self.derived = config.get("derived_attributes", {})
        self.combos = {c["id"]: c for c in config.get("combinations", [])}
        self._validate_config()

    @classmethod
    def from_files(cls, papers_path: str | Path, config_path: str | Path,
                   project_root: Optional[str | Path] = None) -> "CombinationGapAnalyzer":
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        root = Path(project_root) if project_root else Path(config_path).resolve().parent.parent
        for name, attr in config.get("derived_attributes", {}).items():
            if attr.get("classification_file"):
                column = attr.get("column", name)
                rows = load_classification_file(root / attr["classification_file"], column)
                attr["values"] = {pid: (row.get(column) or "").strip() for pid, row in rows.items()}
                attr["rows"] = rows
        with open(papers_path, mode="r", encoding="utf-8-sig", newline="") as f:
            records = list(csv.DictReader(f))
        return cls(records, config, file_sha256(papers_path))

    # ------------------------------------------------------------------ setup
    def _validate_config(self) -> None:
        known = set(BOOLEAN_FIELDS) | set(self.derived)
        if set(self.peripheral_ids) & set(self.review_ids):
            raise ValueError("a record cannot be both peripheral/contextual and a review record")
        for combo in self.combos.values():
            for group in combo.get("criteria", []):
                for field in group:
                    if field not in known:
                        raise ValueError(f"{combo.get('id')}: unknown criterion field '{field}'")
            for field in combo.get("scope_excludes_no", []):
                if field not in known:
                    raise ValueError(f"{combo.get('id')}: unknown scope field '{field}'")
        record_ids = [r.get("paper_id", "") for r in self.records]
        for name, attr in self.derived.items():
            overlap = set(attr.get("yes_ids", [])) & set(attr.get("no_ids", []))
            if overlap:
                raise ValueError(f"derived attribute '{name}' lists {sorted(overlap)} as both Yes and No")
            values = attr.get("values")
            if values is None:
                continue
            bad = {pid: v for pid, v in values.items() if v not in TRI_VALUES}
            if bad:
                raise ValueError(f"derived attribute '{name}': invalid values {bad}")
            if record_ids:
                missing = [pid for pid in record_ids if pid not in values]
                extra = sorted(set(values) - set(record_ids))
                if missing or extra:
                    raise ValueError(f"derived attribute '{name}': missing {missing}, unknown ids {extra}")
            for pid, row in attr.get("rows", {}).items():
                if not _text(row.get("basis")):
                    raise ValueError(f"derived attribute '{name}': {pid} has no documented basis")
                pop = _text(row.get("analysis_population"))
                if pop and pop not in CLASSIFICATION_POPULATIONS:
                    raise ValueError(f"derived attribute '{name}': {pid} has invalid analysis_population '{pop}'")
                if pop and pop != self.population_of(pid):
                    raise ValueError(f"derived attribute '{name}': {pid} population '{pop}' "
                                     f"disagrees with config ('{self.population_of(pid)}')")
        for cand in self.config.get("candidates", []):
            for key in cand:
                if key.lower() in FORBIDDEN_CANDIDATE_KEYS:
                    raise ValueError(f"{cand.get('id')}: ranking/selection key '{key}' is not allowed")
            if cand.get("category") not in CATEGORY_LABELS:
                raise ValueError(f"{cand.get('id')}: invalid category '{cand.get('category')}'")
            for cid in [cand.get("primary_combination")] + list(cand.get("supplementary_combinations", [])):
                if cid and cid not in self.combos:
                    raise ValueError(f"{cand.get('id')}: unknown combination '{cid}'")

    def population_of(self, pid: str) -> str:
        if pid in self.peripheral_ids:
            return "peripheral/contextual"
        if pid in self.review_ids:
            return "review/survey"
        return "core"

    # --------------------------------------------------------------- values
    def field_value(self, record: Dict[str, str], field: str) -> str:
        """Yes/No/Unknown for a papers.csv characteristic or a derived attribute."""
        if field in self.derived:
            pid = record.get("paper_id", "").strip()
            attr = self.derived[field]
            values = attr.get("values")
            if values is not None:
                return values.get(pid, UNKNOWN)
            if pid in attr.get("yes_ids", []):
                return YES
            if pid in attr.get("no_ids", []):
                return NO
            return UNKNOWN
        return _tri(record.get(field, ""))

    def group_value(self, record: Dict[str, str], group: List[str]) -> str:
        """Yes if any field is Yes; No only if every field is No; otherwise Unknown."""
        values = [self.field_value(record, f) for f in group]
        if YES in values:
            return YES
        if all(v == NO for v in values):
            return NO
        return UNKNOWN

    @staticmethod
    def criteria_text(criteria: List[List[str]]) -> str:
        parts = []
        for group in criteria:
            parts.append(group[0] if len(group) == 1 else "(" + " OR ".join(group) + ")")
        return " AND ".join(f"{p}=Yes" for p in parts)

    def unassigned_derived(self) -> Dict[str, List[str]]:
        """Records with no explicit value for each derived attribute."""
        out = {}
        for name, attr in self.derived.items():
            if attr.get("values") is not None:
                assigned = set(attr["values"])
            else:
                assigned = set(attr.get("yes_ids", [])) | set(attr.get("no_ids", []))
            out[name] = [r["paper_id"] for r in self.records if r.get("paper_id") not in assigned]
        return out

    # ------------------------------------------------------------ populations
    def core_records(self) -> List[Dict[str, str]]:
        """Full corpus minus researcher-approved peripheral/contextual records."""
        return [r for r in self.records if r.get("paper_id") not in self.peripheral_ids]

    def primary_core_records(self) -> List[Dict[str, str]]:
        """Core-analysis subset: full corpus minus peripheral/contextual and review/survey records."""
        return [r for r in self.core_records() if r.get("paper_id") not in self.review_ids]

    def in_scope(self, record: Dict[str, str], combo: Dict[str, Any]) -> bool:
        """A record is out of scope only if a scope field is an explicit No (Unknown stays in scope)."""
        return all(self.field_value(record, f) != NO for f in combo.get("scope_excludes_no", []))

    # ------------------------------------------------------------- evaluation
    def evaluate(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        criteria = combo["criteria"]
        scope_fields = combo.get("scope_excludes_no", [])
        all_yes, unresolved, excluded, near, out_of_scope = [], [], [], [], []
        in_scope_ids = []
        for r in self.primary_core_records():
            pid = r["paper_id"]
            groups = [self.group_value(r, g) for g in criteria]
            if not self.in_scope(r, combo):
                rest = [v for g, v in zip(criteria, groups) if not set(g) & set(scope_fields)]
                if rest and all(v == YES for v in rest):
                    out_of_scope.append(pid)
                continue
            in_scope_ids.append(pid)
            if all(v == YES for v in groups):
                all_yes.append(pid)
            elif NO in groups:
                nos = ["|".join(g) for g, v in zip(criteria, groups) if v == NO]
                excluded.append(f"{pid}[{','.join(nos)}=No]")
            else:
                unresolved.append(pid)
            missing = [(g, v) for g, v in zip(criteria, groups) if v != YES]
            if len(criteria) > 1 and len(missing) == 1:
                g, v = missing[0]
                near.append(f"{pid}[{'|'.join(g)}={v}]")
        reviews = [r["paper_id"] for r in self.core_records() if r["paper_id"] in self.review_ids]
        peripheral = []
        for r in self.records:
            if r.get("paper_id") in self.peripheral_ids:
                groups = [self.group_value(r, g) for g in criteria]
                overall = YES if all(v == YES for v in groups) else (NO if NO in groups else UNKNOWN)
                peripheral.append(f"{r['paper_id']}={overall}")
        n = len(in_scope_ids)
        if all_yes:
            observation = (f"{len(all_yes)} of {n} in-scope core records satisfy every criterion "
                           "(counterexamples to a gap claim)")
        elif unresolved:
            observation = (f"No in-scope core record satisfies every criterion; the available coding is "
                           f"insufficient to determine the combination for {len(unresolved)} of {n} records")
        else:
            observation = f"No in-scope core record satisfies every criterion; all {n} are excluded by a coded No"
        scope = ("Core-analysis subset" if not scope_fields else
                 "Core-analysis subset, excluding records coded No for " + ", ".join(scope_fields))
        return {
            "combination_id": combo["id"],
            "label": combo["label"],
            "research_dimensions": "; ".join(str(d) for d in combo.get("dimensions", [])),
            "criteria": self.criteria_text(criteria),
            "scope": scope,
            "records_in_scope": str(n),
            "all_yes_count": str(len(all_yes)),
            "all_yes_ids": _ids(all_yes),
            "unresolved_count": str(len(unresolved)),
            "unresolved_ids": _ids(unresolved),
            "excluded_by_no_count": str(len(excluded)),
            "excluded_by_no_ids": _ids(excluded),
            "near_miss": _ids(near),
            "out_of_scope_matches": _ids(out_of_scope),
            "review_record_ids": _ids(reviews),
            "peripheral_results": _ids(peripheral),
            "coverage_observation": observation,
            "corpus_sha256": self.corpus_sha256,
            "review_status": REVIEW_STATUS,
        }

    def combination_matrix_rows(self) -> List[Dict[str, str]]:
        return [self.evaluate(c) for c in self.config.get("combinations", [])]

    def _visual_basis(self, combo: Dict[str, Any], row: Dict[str, str]) -> str:
        fields = {f for g in combo.get("criteria", []) for f in g} | set(combo.get("scope_excludes_no", []))
        if "visual_inspection_scope" not in fields or "visual_inspection_scope" not in self.derived:
            return "Not used by this combination"
        yes, unk = [], []
        for r in self.primary_core_records():
            if not self.in_scope(r, combo):
                continue
            v = self.field_value(r, "visual_inspection_scope")
            (yes if v == YES else unk if v == UNKNOWN else []).append(r["paper_id"])
        src = self.derived["visual_inspection_scope"].get("classification_file", "configured values")
        return (f"visual_inspection_scope (analysis-only; {src}); records coded No are out of scope; "
                f"in scope: Yes {len(yes)} ({_ids(yes)}), Unknown {len(unk)} ({_ids(unk)})")

    def candidate_rows(self) -> List[Dict[str, str]]:
        rows = []
        for cand in self.config.get("candidates", []):
            if not cand.get("primary_combination"):
                rows.append(self._not_assessable_row(cand))
                continue
            combo = self.combos[cand["primary_combination"]]
            ev = self.evaluate(combo)
            counter = f"Full: {ev['all_yes_ids']}; partial (one criterion short): {ev['near_miss']}"
            if ev["out_of_scope_matches"] != "None":
                counter += f"; outside scope, all other criteria Yes: {ev['out_of_scope_matches']}"
            rows.append({
                "candidate_gap": f"{cand['id']}: {_text(cand['title'])}",
                "category": CATEGORY_LABELS[cand["category"]],
                "description": _text(cand.get("description")),
                "primary_combination": combo["id"],
                "criteria": ev["criteria"],
                "supporting_papers": ev["excluded_by_no_ids"],
                "counterexamples": counter,
                "relevant_core_papers": f"{ev['records_in_scope']} ({ev['scope']})",
                "yes_count": ev["all_yes_count"],
                "no_count": ev["excluded_by_no_count"],
                "unknown_count": ev["unresolved_count"],
                "evidence_basis": _text(cand.get("evidence_basis")),
                "evidence_limitations": _text(cand.get("evidence_limitations")),
                "visual_inspection_basis": self._visual_basis(combo, ev),
                "researcher_review_status": REVIEW_STATUS,
            })
        return rows

    @staticmethod
    def _not_assessable_row(cand: Dict[str, Any]) -> Dict[str, str]:
        na = "Not assessable (dimension not coded in papers.csv)"
        return {
            "candidate_gap": f"{cand['id']}: {_text(cand['title'])}",
            "category": CATEGORY_LABELS[cand["category"]],
            "description": _text(cand.get("description")),
            "primary_combination": "None",
            "criteria": na,
            "supporting_papers": "None",
            "counterexamples": "Not assessable",
            "relevant_core_papers": na,
            "yes_count": "n/a",
            "no_count": "n/a",
            "unknown_count": "n/a",
            "evidence_basis": _text(cand.get("evidence_basis")),
            "evidence_limitations": _text(cand.get("evidence_limitations")),
            "visual_inspection_basis": "Not used",
            "researcher_review_status": REVIEW_STATUS,
        }

    # Backwards-compatible name used by the CLI.
    def gap_matrix_rows(self) -> List[Dict[str, str]]:
        return self.candidate_rows()

    def characteristic_coverage(self) -> List[Dict[str, Any]]:
        """Yes/No/Unknown counts per field over the core-analysis subset."""
        rows = []
        fields = [h for h in PAPERS_SCHEMA_HEADERS if h in BOOLEAN_FIELDS] + list(self.derived)
        for field in fields:
            counts = {YES: [], NO: [], UNKNOWN: []}
            for r in self.primary_core_records():
                counts[self.field_value(r, field)].append(r["paper_id"])
            rows.append({"field": field, "yes": counts[YES], "no": counts[NO], "unknown": counts[UNKNOWN]})
        return rows

    # ----------------------------------------------------------------- output
    @staticmethod
    def _write_csv(path: str | Path, fields: List[str], rows: List[Dict[str, str]]) -> str:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        return str(path)

    def write_gap_matrix_csv(self, output_path: str | Path) -> str:
        return self._write_csv(output_path, GAP_MATRIX_FIELDS, self.candidate_rows())

    def write_combination_matrix_csv(self, output_path: str | Path) -> str:
        return self._write_csv(output_path, COMBINATION_MATRIX_FIELDS, self.combination_matrix_rows())

    def _record(self, pid: str) -> Optional[Dict[str, str]]:
        for r in self.records:
            if r.get("paper_id") == pid:
                return r
        return None

    def _component_lines(self, combo: Dict[str, Any]) -> List[str]:
        """Per-criterion Yes/No/Unknown coverage inside the combination's scope."""
        lines = []
        scoped = [r for r in self.primary_core_records() if self.in_scope(r, combo)]
        for group in combo["criteria"]:
            vals = {YES: [], NO: [], UNKNOWN: []}
            for r in scoped:
                vals[self.group_value(r, group)].append(r["paper_id"])
            name = group[0] if len(group) == 1 else "(" + " OR ".join(group) + ")"
            lines.append(f"| `{name}` | {len(vals[YES])} | {len(vals[NO])} | {len(vals[UNKNOWN])} | "
                         f"{', '.join(vals[YES]) or '—'} |")
        return lines

    def generate_gap_candidates_markdown(self) -> str:
        cfg = self.config
        freeze = cfg.get("corpus_freeze", {})
        combos = self.combination_matrix_rows()
        by_combo = {r["combination_id"]: r for r in combos}
        dims = cfg.get("dimensions", {})
        cands = cfg.get("candidates", [])
        md: List[str] = []
        add = md.append

        add("# PocketInspect: Candidate Research Gaps (Step 9.7, revised)")
        add("")
        add("> **Status: pending researcher review.** Generated by `python scripts/manage_literature.py gap` from "
            "`research/literature/papers.csv`, `configs/gap_analysis.yaml` and the analysis-only classification "
            "files. Candidates are unordered. None is scored, ranked, recommended or selected, and this tool never "
            "writes `research/gap_analysis/research_gap.md`.")
        add("")
        add("> **Scope of every statement below.** Statements are *corpus observations* about the frozen "
            "54-record corpus, or *evidence limitations* of that corpus. They are not claims about the wider "
            "literature: the search (§7) is not sufficient to support statements such as \"few or no studies "
            "in the field have ...\".")
        add("")
        frozen = freeze.get("papers_sha256", "")
        if frozen and frozen != self.corpus_sha256:
            add(f"> **WARNING: corpus changed since the freeze.** The candidate narratives were written against "
                f"`papers.csv` SHA-256 `{frozen}`; the current file is `{self.corpus_sha256}`. "
                "Counts below are current, but every narrative must be re-reviewed.")
            add("")

        # 1. Corpus freeze
        add("## 1. Corpus freeze")
        add("")
        add(f"- Freeze record: [`corpus_freeze.md`](corpus_freeze.md)")
        add(f"- Frozen at commit `{freeze.get('git_commit', 'n/a')}`; `papers.csv` SHA-256 `{frozen or 'n/a'}`")
        add(f"- Current `papers.csv` SHA-256: `{self.corpus_sha256}`")
        add(f"- Records: {len(self.records)} (canonical corpus; unchanged by this analysis)")
        add("")

        # 2. Core subset
        n_full, n_per, n_rev = len(self.records), len(self.peripheral_ids), len(self.review_ids)
        n_core = len(self.primary_core_records())
        add("## 2. Analysis-only core subset")
        add("")
        add("| Population | Records | Count | Treatment |")
        add("| :-- | :-- | --: | :-- |")
        add(f"| Canonical corpus | P001–P054 | {n_full} | Unchanged in `papers.csv` |")
        add(f"| Peripheral/contextual (researcher-approved) | {', '.join(self.peripheral_ids)} | {n_per} | "
            "Excluded from core counting; reported separately in `combination_matrix.csv` |")
        add(f"| Review/survey records | {', '.join(self.review_ids)} | {n_rev} | Excluded from core counting |")
        add(f"| **Core-analysis subset** | all other records | **{n_core}** | Every count below |")
        add("")
        add(f"Arithmetic check: {n_full} − {n_per} − {n_rev} = {n_full - n_per - n_rev}; "
            f"core subset computed from the data: {n_core}. The two exclusion lists do not overlap.")
        add("")
        for item in cfg.get("core_subset_rationale", []):
            add(f"- {_text(item)}")
        add("")

        # 3. Visual-inspection classification
        add("## 3. Visual-inspection classification methodology")
        add("")
        vis = self.derived.get("visual_inspection_scope")
        if vis:
            add(f"**`visual_inspection_scope`** ({_text(vis.get('status'))}). Per-paper values and their basis: "
                f"[`{Path(vis.get('classification_file', '')).name}`]({Path(vis.get('classification_file', '')).name}).")
            add("")
            for key in ("yes", "no", "unknown"):
                if vis.get("definition", {}).get(key):
                    add(f"- **{key.capitalize()}**: {_text(vis['definition'][key])}")
            for item in vis.get("rules", []):
                add(f"- {_text(item)}")
            add("")
            cov = next(c for c in self.characteristic_coverage() if c["field"] == "visual_inspection_scope")
            add(f"Core-analysis subset: Yes {len(cov['yes'])} ({', '.join(cov['yes'])}); "
                f"Unknown {len(cov['unknown'])} ({', '.join(cov['unknown'])}); No {len(cov['no'])}.")
            add("")
            if vis.get("rows"):
                cats: Dict[str, List[str]] = {}
                for pid, row in vis["rows"].items():
                    if self.population_of(pid) == "core":
                        cats.setdefault(f"{row['visual_inspection_scope']} — {row['basis_category']}", []).append(pid)
                add("| Value — basis category (core) | Records |")
                add("| :-- | :-- |")
                for k in sorted(cats):
                    add(f"| {k} | {', '.join(cats[k])} |")
                add("")
        add("**Reading the counts.** Inside a combination's scope, a core record is *all-Yes* (a counterexample), "
            "*unresolved* (no criterion No, at least one Unknown) or *excluded by No* (at least one criterion coded "
            "No). `Unknown` is never treated as `No`: an unresolved record means the available coding is "
            "insufficient to decide, not that the capability is absent. A blank free-text field such as "
            "`accuracy_metrics` is never used as a criterion.")
        add("")
        add("### Characteristic coverage (core-analysis subset)")
        add("")
        add("| Field | Yes | No | Unknown | Yes records |")
        add("| :-- | --: | --: | --: | :-- |")
        for c in self.characteristic_coverage():
            add(f"| `{c['field']}` | {len(c['yes'])} | {len(c['no'])} | {len(c['unknown'])} | "
                f"{', '.join(c['yes']) or '—'} |")
        add("")

        def candidate_block(cand: Dict[str, Any]) -> None:
            add(f"### {cand['id']}: {_text(cand['title'])}")
            add("")
            if cand.get("formerly"):
                add(f"_Formerly {cand['formerly']} in the first Step 9.7 version._")
                add("")
            if not cand.get("primary_combination"):
                add("| Item | Content |")
                add("| :-- | :-- |")
                add(f"| Category | {CATEGORY_LABELS[cand['category']]} |")
                for label, key in (("Corpus observation", "description"), ("Evidence basis", "evidence_basis"),
                                   ("Evidence limitations", "evidence_limitations"), ("Gap type", "gap_type"),
                                   ("Evidence strength (descriptive)", "evidence_strength"),
                                   ("Not claimed", "not_claimed")):
                    add(f"| {label} | {_text(cand.get(key))} |")
                add("| Counts | Not assessable: the dimension is not coded in `papers.csv` |")
                add(f"| Researcher-review status | {REVIEW_STATUS} |")
                add("")
                return
            combo = self.combos[cand["primary_combination"]]
            ev = by_combo[combo["id"]]
            add("| Item | Content |")
            add("| :-- | :-- |")
            add(f"| Category | {CATEGORY_LABELS[cand['category']]} |")
            add(f"| Corpus observation | {_text(cand.get('description'))} |")
            add(f"| Research dimensions | " + "; ".join(f"{d} {dims.get(d, '')}" for d in cand.get('dimensions', [])) + " |")
            add(f"| Primary combination | {combo['id']} — `{ev['criteria']}` |")
            add(f"| Relevant core papers | {ev['records_in_scope']} ({ev['scope']}) |")
            add(f"| Yes / No / Unknown | {ev['all_yes_count']} all-Yes / {ev['excluded_by_no_count']} excluded by No / "
                f"{ev['unresolved_count']} unresolved |")
            add(f"| Supporting papers (excluded by a coded No) | {ev['excluded_by_no_ids']} |")
            add(f"| Counterexamples (all-Yes) | {ev['all_yes_ids']} |")
            add(f"| Partial counterexamples (one criterion short) | {ev['near_miss']} |")
            add(f"| Outside scope, all other criteria Yes | {ev['out_of_scope_matches']} |")
            add(f"| Unresolved (coding insufficient) | {ev['unresolved_ids']} |")
            add(f"| Counterexample assessment | {_text(cand.get('counterexample_assessment'))} |")
            add(f"| Evidence basis | {_text(cand.get('evidence_basis'))} |")
            add(f"| Evidence limitations | {_text(cand.get('evidence_limitations'))} |")
            add(f"| Visual-inspection basis | {self._visual_basis(combo, ev)} |")
            add(f"| Gap type | {_text(cand.get('gap_type'))} |")
            add(f"| Evidence strength (descriptive) | {_text(cand.get('evidence_strength'))} |")
            add(f"| Not claimed | {_text(cand.get('not_claimed'))} |")
            add(f"| Researcher-review status | {REVIEW_STATUS} |")
            add("")
            add("Component coverage inside the scope of the primary combination:")
            add("")
            add("| Criterion | Yes | No | Unknown | Yes records |")
            add("| :-- | --: | --: | --: | :-- |")
            md.extend(self._component_lines(combo))
            add("")
            supp = cand.get("supplementary_combinations", [])
            if supp:
                add("Supplementary combinations: " + "; ".join(
                    f"{cid} ({by_combo[cid]['label']}): all-Yes {by_combo[cid]['all_yes_ids']}, "
                    f"unresolved {by_combo[cid]['unresolved_count']}, excluded by No "
                    f"{by_combo[cid]['excluded_by_no_count']}" for cid in supp) + ".")
                add("")

        add("## 4. Evidence-supported candidate gaps")
        add("")
        add("Unordered. Each states a corpus observation only. Pending researcher review.")
        add("")
        for cand in cands:
            if cand["category"] == CATEGORY_GAP:
                candidate_block(cand)

        add("## 5. Evidence limitations / unresolved questions")
        add("")
        add("Unordered. These are not gap claims: the frozen coding cannot support a gap statement for them. "
            "Pending researcher review.")
        add("")
        for cand in cands:
            if cand["category"] == CATEGORY_LIMITATION:
                candidate_block(cand)

        add("## 6. Counterexamples")
        add("")
        add("All counterexamples (all-Yes records) and partial counterexamples for every evaluated combination. "
            "Data: [`combination_matrix.csv`](combination_matrix.csv). Order implies nothing.")
        add("")
        add("| ID | Combination | In scope | All-Yes | Unresolved | Excluded by No | Partial (one criterion short) |")
        add("| :-- | :-- | --: | :-- | --: | --: | :-- |")
        for r in combos:
            add(f"| {r['combination_id']} | {r['label']} | {r['records_in_scope']} | {r['all_yes_ids']} | "
                f"{r['unresolved_count']} | {r['excluded_by_no_count']} | {r['near_miss']} |")
        add("")
        for item in cfg.get("counterexample_notes", []):
            add(f"- {_text(item)}")
        add("")
        add("Confidence-gating actions (the schema does not code the action; read from each record's evidence):")
        add("")
        cg = next(c for c in self.characteristic_coverage() if c["field"] == "confidence_gating")
        for pid in cg["yes"]:
            note = cfg.get("confidence_gating_actions", {}).get(pid, "(not documented)")
            add(f"- **{pid}**: {_text(note)}")
        add("")

        add("## 7. Search limitations")
        add("")
        add("These limit what the corpus can show. They are not evidence of any gap.")
        add("")
        for item in cfg.get("search_limitations", []):
            add(f"- {_text(item)}")
        add("")

        add("## 8. P013 unresolved evidence")
        add("")
        for item in cfg.get("p013_unresolved", []):
            add(f"- {_text(item)}")
        add("")

        add("## 9. Researcher review required")
        add("")
        for item in cfg.get("researcher_review", []):
            add(f"- {_text(item)}")
        add("")
        add("---")
        add("")
        add("No final research gap was selected, ranked, or approved. All items: *Pending researcher review*.")
        add("")
        return "\n".join(md)

    def write_gap_candidates_markdown(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(self.generate_gap_candidates_markdown())
        return str(path)
