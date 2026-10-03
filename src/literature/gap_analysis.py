"""
Configuration-driven combination gap analysis for PocketInspect.

Reads characteristic combinations, analysis populations and derived
attributes from a YAML file (``configs/gap_analysis.yaml``) and evaluates
them against ``research/literature/papers.csv``.

The analysis is descriptive. For every combination it reports which records
satisfy all criteria (counterexamples to a gap claim), which are unresolved
because a criterion is ``Unknown``, and which are excluded by an explicit
``No``. ``Unknown`` is never treated as ``No``. It does not score, rank or
select a research gap, and it never writes ``research_gap.md``.
"""
import csv
import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.literature.schema import BOOLEAN_FIELDS, PAPERS_SCHEMA_HEADERS, parse_boolean_field

YES, NO, UNKNOWN = "Yes", "No", "Unknown"
REVIEW_STATUS = "Pending researcher review"

GAP_MATRIX_FIELDS = [
    "combination_id",
    "label",
    "research_dimensions",
    "criteria",
    "analysis_population",
    "population_size",
    "all_yes_count",
    "all_yes_ids",
    "unresolved_count",
    "unresolved_ids",
    "excluded_by_no_count",
    "near_miss",
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


class CombinationGapAnalyzer:
    """Evaluates configured characteristic combinations over literature records."""

    def __init__(self, records: List[Dict[str, str]], config: Dict[str, Any],
                 corpus_sha256: str = ""):
        self.records = records
        self.config = config
        self.corpus_sha256 = corpus_sha256
        pops = config.get("populations", {})
        self.peripheral_ids = list(pops.get("peripheral_contextual", {}).get("paper_ids", []))
        self.review_ids = list(pops.get("review_records", {}).get("paper_ids", []))
        self.derived = config.get("derived_attributes", {})
        self._validate_config()

    @classmethod
    def from_files(cls, papers_path: str | Path, config_path: str | Path) -> "CombinationGapAnalyzer":
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        records: List[Dict[str, str]] = []
        with open(papers_path, mode="r", encoding="utf-8-sig", newline="") as f:
            records = list(csv.DictReader(f))
        return cls(records, config, file_sha256(papers_path))

    # ------------------------------------------------------------------ setup
    def _validate_config(self) -> None:
        known = set(BOOLEAN_FIELDS) | set(self.derived)
        for combo in self.config.get("combinations", []):
            for group in combo.get("criteria", []):
                for field in group:
                    if field not in known:
                        raise ValueError(f"{combo.get('id')}: unknown criterion field '{field}'")
        for name, attr in self.derived.items():
            overlap = set(attr.get("yes_ids", [])) & set(attr.get("no_ids", []))
            if overlap:
                raise ValueError(f"derived attribute '{name}' lists {sorted(overlap)} as both Yes and No")

    # --------------------------------------------------------------- values
    def field_value(self, record: Dict[str, str], field: str) -> str:
        """Yes/No/Unknown for a papers.csv characteristic or a derived attribute."""
        if field in self.derived:
            pid = record.get("paper_id", "").strip()
            attr = self.derived[field]
            if pid in attr.get("yes_ids", []):
                return YES
            if pid in attr.get("no_ids", []):
                return NO
            return UNKNOWN
        return _tri(record.get(field, ""))

    def group_value(self, record: Dict[str, str], group: List[str]) -> str:
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
            assigned = set(attr.get("yes_ids", [])) | set(attr.get("no_ids", []))
            out[name] = [r["paper_id"] for r in self.records if r.get("paper_id") not in assigned]
        return out

    # ------------------------------------------------------------ populations
    def core_records(self) -> List[Dict[str, str]]:
        return [r for r in self.records if r.get("paper_id") not in self.peripheral_ids]

    def primary_core_records(self) -> List[Dict[str, str]]:
        return [r for r in self.core_records() if r.get("paper_id") not in self.review_ids]

    # ------------------------------------------------------------- evaluation
    def evaluate(self, combo: Dict[str, Any]) -> Dict[str, Any]:
        criteria = combo["criteria"]
        all_yes, unresolved, excluded, near = [], [], [], []
        for r in self.primary_core_records():
            pid = r["paper_id"]
            groups = [self.group_value(r, g) for g in criteria]
            if all(v == YES for v in groups):
                all_yes.append(pid)
            elif NO in groups:
                excluded.append(pid)
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
        if all_yes:
            observation = "Core records satisfy every criterion (counterexample to a gap claim)"
        elif unresolved:
            observation = (f"No core record satisfies every criterion; {len(unresolved)} "
                           "record(s) unresolved because of Unknown values")
        else:
            observation = "No core record satisfies every criterion; none unresolved"
        return {
            "combination_id": combo["id"],
            "label": combo["label"],
            "research_dimensions": "; ".join(str(d) for d in combo.get("dimensions", [])),
            "criteria": self.criteria_text(criteria),
            "analysis_population": "Core primary studies (full corpus minus peripheral/contextual and review records)",
            "population_size": str(len(self.primary_core_records())),
            "all_yes_count": str(len(all_yes)),
            "all_yes_ids": _ids(all_yes),
            "unresolved_count": str(len(unresolved)),
            "unresolved_ids": _ids(unresolved),
            "excluded_by_no_count": str(len(excluded)),
            "near_miss": _ids(near),
            "review_record_ids": _ids(reviews),
            "peripheral_results": _ids(peripheral),
            "coverage_observation": observation,
            "corpus_sha256": self.corpus_sha256,
            "review_status": REVIEW_STATUS,
        }

    def gap_matrix_rows(self) -> List[Dict[str, str]]:
        return [self.evaluate(c) for c in self.config.get("combinations", [])]

    def characteristic_coverage(self) -> List[Dict[str, Any]]:
        """Yes/No/Unknown counts per field over the core primary studies."""
        rows = []
        fields = [h for h in PAPERS_SCHEMA_HEADERS if h in BOOLEAN_FIELDS] + list(self.derived)
        for field in fields:
            counts = {YES: [], NO: [], UNKNOWN: []}
            for r in self.primary_core_records():
                counts[self.field_value(r, field)].append(r["paper_id"])
            rows.append({"field": field, "yes": counts[YES], "no": counts[NO], "unknown": counts[UNKNOWN]})
        return rows

    # ----------------------------------------------------------------- output
    def write_gap_matrix_csv(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=GAP_MATRIX_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.gap_matrix_rows())
        return str(path)

    def _record(self, pid: str) -> Optional[Dict[str, str]]:
        for r in self.records:
            if r.get("paper_id") == pid:
                return r
        return None

    def _evidence_items(self, pid: str, field: str) -> List[str]:
        r = self._record(pid)
        if not r:
            return []
        # An item runs from its "[field]" marker to the next "[" marker.
        pattern = re.compile(r"\[" + re.escape(field) + r"\][^\[]*")
        return [" ".join(m.group(0).split()).rstrip(" ;|") for m in pattern.finditer(r.get("evidence", ""))]

    def generate_gap_candidates_markdown(self) -> str:
        cfg = self.config
        freeze = cfg.get("corpus_freeze", {})
        rows = self.gap_matrix_rows()
        by_id = {r["combination_id"]: r for r in rows}
        dims = cfg.get("dimensions", {})
        md: List[str] = []
        add = md.append

        add("# PocketInspect: Candidate Research Gaps (Step 9.7)")
        add("")
        add("> **Status: candidate gaps only — pending researcher review.** This report is generated by "
            "`python scripts/manage_literature.py gap` from `research/literature/papers.csv` and "
            "`configs/gap_analysis.yaml`. It does not select, approve, score or rank a research gap. "
            "No candidate below is a final gap. `research/gap_analysis/research_gap.md` is not written by this tool.")
        add("")
        frozen = freeze.get("papers_sha256", "")
        if frozen and frozen != self.corpus_sha256:
            add(f"> **WARNING: corpus changed since the freeze.** The candidate narratives were written against "
                f"`papers.csv` SHA-256 `{frozen}`; the current file is `{self.corpus_sha256}`. "
                "Counts below are current, but every narrative must be re-reviewed.")
            add("")

        add("## 1. Evidence base")
        add("")
        add(f"- Corpus freeze record: `{freeze.get('record', 'n/a')}`")
        add(f"- Frozen at commit `{freeze.get('git_commit', 'n/a')}`; `papers.csv` SHA-256 `{frozen or 'n/a'}`")
        add(f"- Current `papers.csv` SHA-256: `{self.corpus_sha256}`")
        add(f"- Full corpus: {len(self.records)} records")
        add(f"- Peripheral/contextual (researcher-approved, kept in `papers.csv`, not core evidence): "
            f"{', '.join(self.peripheral_ids) or 'none'}")
        add(f"- Review/survey records (in the core subset, but never counted as primary evidence of absence): "
            f"{', '.join(self.review_ids) or 'none'}")
        add(f"- Core primary studies used for every count below: {len(self.primary_core_records())}")
        add("")
        add("**Reading the counts.** For each combination a core primary study is either:")
        add("- *all-Yes*: every criterion is Yes (a counterexample to any \"gap\" claim);")
        add("- *unresolved*: no criterion is No but at least one is Unknown (cannot be counted either way);")
        add("- *excluded by No*: at least one criterion is an explicit No.")
        add("")
        add("`Unknown` is never treated as `No`. Most `Unknown` values come from abstract-level coding "
            "(full text not yet read). A missing value in a free-text field (e.g. `accuracy_metrics`) "
            "is an unresolved evidence field, not evidence that something was not done.")
        add("")
        for name, attr in self.derived.items():
            add(f"**Derived attribute `{name}`** ({attr.get('status', '')}): {attr.get('definition', '')} "
                f"Basis: {attr.get('basis', '')}. Yes: {', '.join(attr.get('yes_ids', []))}.")
            add("")
        unassigned = {k: v for k, v in self.unassigned_derived().items() if v}
        if unassigned:
            add(f"> Records without a derived-attribute value (Unknown): {unassigned}")
            add("")

        add("## 2. Characteristic coverage (core primary studies)")
        add("")
        add("| Field | Yes | No | Unknown | Yes records |")
        add("| :-- | --: | --: | --: | :-- |")
        for c in self.characteristic_coverage():
            add(f"| `{c['field']}` | {len(c['yes'])} | {len(c['no'])} | {len(c['unknown'])} | "
                f"{', '.join(c['yes']) or '—'} |")
        add("")

        add("## 3. Combination matrix")
        add("")
        add("Data: [`gap_matrix.csv`](gap_matrix.csv). No ranking is implied by the order.")
        add("")
        add("| ID | Combination | All-Yes | All-Yes records | Unresolved | Excluded by No | Peripheral |")
        add("| :-- | :-- | --: | :-- | --: | --: | :-- |")
        for r in rows:
            add(f"| {r['combination_id']} | {r['label']} | {r['all_yes_count']} | {r['all_yes_ids']} | "
                f"{r['unresolved_count']} | {r['excluded_by_no_count']} | {r['peripheral_results']} |")
        add("")
        add("### Combination details")
        add("")
        for combo, r in zip(cfg.get("combinations", []), rows):
            add(f"#### {r['combination_id']}: {r['label']}")
            add(f"- Criteria: `{r['criteria']}`")
            add(f"- Research dimensions: " + ", ".join(f"{d} ({dims.get(d, '')})" for d in combo.get("dimensions", [])))
            add(f"- Observation: {r['coverage_observation']}")
            add(f"- All-Yes (counterexamples): {r['all_yes_ids']}")
            add(f"- Near miss (exactly one criterion not Yes): {r['near_miss']}")
            add(f"- Unresolved ({r['unresolved_count']}): {r['unresolved_ids']}")
            add(f"- Peripheral/contextual records (not counted): {r['peripheral_results']}")
            if combo.get("note"):
                add(f"- Note: {' '.join(str(combo['note']).split())}")
            add("")

        add("## 4. Confidence-gating actions and accuracy reporting (evidence text)")
        add("")
        add("The schema records *that* a confidence gate exists, not *which* action it triggers. "
            "The action of every core `confidence_gating = Yes` record, from its `evidence` field:")
        add("")
        cg = next(c for c in self.characteristic_coverage() if c["field"] == "confidence_gating")
        for pid in cg["yes"]:
            for item in self._evidence_items(pid, "confidence_gating") or ["(no evidence item found)"]:
                add(f"- **{pid}**: {item}")
        add("")
        add("Accuracy reporting (`accuracy_metrics`) for records satisfying C-K (smartphone + latency + energy):")
        add("")
        for pid in [p for p in by_id.get("C-K", {}).get("all_yes_ids", "None").split("; ") if p != "None"]:
            acc = (self._record(pid) or {}).get("accuracy_metrics", "").strip()
            add(f"- **{pid}**: {acc or '(blank — unresolved evidence field)'}")
        add("")

        add("## 5. Candidate gaps (pending researcher review)")
        add("")
        add("Unordered. No candidate is scored, ranked or recommended. Each must be confirmed, "
            "reworded or rejected by the researcher before any use.")
        add("")
        for cand in cfg.get("candidate_gaps", []):
            add(f"### {cand['id']}: {cand['title']}")
            add("")
            add("| Item | Content |")
            add("| :-- | :-- |")
            add(f"| Description | {' '.join(str(cand.get('description', '')).split())} |")
            add(f"| Research dimensions | " + "; ".join(f"{d} {dims.get(d, '')}" for d in cand.get("dimensions", [])) + " |")
            add(f"| Combinations examined | {', '.join(cand.get('combinations', []))} |")
            support = []
            for cid in cand.get("combinations", []):
                cr = by_id.get(cid)
                if cr:
                    support.append(f"{cid}: all-Yes {cr['all_yes_ids']}; unresolved {cr['unresolved_count']}; "
                                   f"excluded by No {cr['excluded_by_no_count']}")
            add(f"| Generated counts | {' / '.join(support) or 'n/a'} |")
            add(f"| Supporting paper IDs | {' '.join(str(cand.get('supporting', '')).split())} |")
            add(f"| Counterexample paper IDs | {' '.join(str(cand.get('counterexamples', '')).split())} |")
            add(f"| Relevant core papers | {' '.join(str(cand.get('relevant_count', '')).split())} |")
            add(f"| Evidence basis | {' '.join(str(cand.get('evidence_basis', '')).split())} |")
            add(f"| Characteristics involved | {', '.join(cand.get('characteristics', []))} |")
            add(f"| Known limitations | {' '.join(str(cand.get('limitations', '')).split())} |")
            add(f"| Gap type | {cand.get('gap_type', '')} |")
            add(f"| Evidence strength (descriptive) | {' '.join(str(cand.get('evidence_strength', '')).split())} |")
            add(f"| Researcher-review status | {REVIEW_STATUS} |")
            add("")

        if cfg.get("not_proposed"):
            add("## 6. Combinations not proposed as candidate gaps")
            add("")
            for item in cfg["not_proposed"]:
                add(f"- **{item['combination']}**: {' '.join(str(item['reason']).split())}")
            add("")
        if cfg.get("not_coded"):
            add("## 7. Dimensions not coded in `papers.csv`")
            add("")
            for d, text in cfg["not_coded"].items():
                add(f"- Dimension {d} ({dims.get(d, '')}): {text}")
            add("")
        if cfg.get("limitations"):
            add("## 8. Evidence and search limitations")
            add("")
            for item in cfg["limitations"]:
                add(f"- {' '.join(str(item).split())}")
            add("")
        if cfg.get("research_question_alignment"):
            add("## 9. Research-question alignment (researcher-review issues)")
            add("")
            add("Observations only. `PROJECT_SPEC.md` and the research questions were not changed.")
            add("")
            for item in cfg["research_question_alignment"]:
                add(f"- {' '.join(str(item).split())}")
            add("")
        add("---")
        add("")
        add("No final research gap was selected or approved. All candidates: *Pending researcher review*.")
        add("")
        return "\n".join(md)

    def write_gap_candidates_markdown(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(self.generate_gap_candidates_markdown())
        return str(path)
