"""
Validation of the Step 9.8 candidate-gap evaluation artefacts.

Reads the framework in ``configs/gap_evaluation.yaml`` and checks the evidence
files it names:

* ``counterexample_candidates.csv``: papers assessed as possible
  counterexamples to GC-01, GC-02 and GC-03;
* ``targeted_search_log.md``: the targeted disproof searches;
* ``candidate_gap_matrix.csv``: one qualitative row per candidate x criterion;
* ``candidate_gap_evaluation.md``: the written evaluation.

The validator is read-only. It never writes to ``research/literature/`` and
never scores, ranks or selects candidates. Its checks enforce the Step 9.8
guard-rails:

* the canonical corpus is frozen;
* ``Unknown`` is never silently converted to ``No``;
* every claim carries an evidence level;
* every search records its limitations;
* no ranking, selection or novelty language appears;
* the researcher-approved operational definitions (Decisions A-C) are applied,
  confirmed partial counterexamples stay partial, and locked evidence levels
  are not upgraded;
* ``research_gap.md`` follows the approval lifecycle (``approval_state_errors``).
"""
import csv
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from src.literature.schema import PAPERS_SCHEMA_HEADERS

CORPUS_ID_PATTERN = re.compile(r"^P\d{3}$")
SEARCH_HEADING_PATTERN = re.compile(r"^###\s+(S\d{2})\b.*$", re.MULTILINE)
TABLE_ROW_PATTERN = re.compile(r"^\|\s*(?P<key>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*$")

SEARCH_LOG_REQUIRED_FIELDS = (
    "Date",
    "Candidate",
    "Exact query",
    "Database / engine",
    "Results returned",
    "Relevant results inspected",
    "Strongest relevant papers",
    "Potential counterexamples",
    "Unresolved items",
    "Search limitations",
)

EVALUATION_SECTIONS = (
    "Purpose",
    "Frozen corpus boundary",
    "Evaluation methodology",
    "GC-01 evaluation",
    "GC-02 evaluation",
    "GC-03 evaluation",
    "Counterexample analysis",
    "Unknown/evidence limitations",
    "Dataset and experimental feasibility",
    "Research contribution considerations",
    "Candidate-by-candidate strengths",
    "Candidate-by-candidate weaknesses",
    "Evidence that could overturn each candidate",
    "Remaining uncertainty",
    "Researcher decision required",
)

# Characteristic columns of the counterexample file mapped to their corpus source.
# ``visual_inspection`` comes from the analysis-only scope classification, not papers.csv.
VISUAL_SCOPE_FILE = "research/gap_analysis/visual_inspection_scope.csv"

YES, NO, UNKNOWN = "Yes", "No", "Unknown"


def _tri(value: Optional[bool]) -> str:
    """Map True/False/None (not established) to Yes/No/Unknown."""
    if value is None:
        return UNKNOWN
    return YES if value else NO


# ---------------------------------------------------------------------------
# Operational definitions (configs/gap_evaluation.yaml: operational_definitions)
# ---------------------------------------------------------------------------
def code_adaptive_inference(runtime_path_changes: Optional[bool]) -> str:
    """Decision A: a runtime change of the executed path, model, cascade stage,
    depth, width or inference configuration (including content-driven cascades)
    is adaptive inference."""
    return _tri(runtime_path_changes)


def code_resource_awareness(resource_state_drives_adaptation: Optional[bool]) -> str:
    """Decision A: resource awareness requires device/resource state to drive the
    adaptation. Content-driven adaptation alone passes ``False`` (No) when the
    trigger is established to be content, or ``None`` (Unknown) when the role of
    resource state is not established."""
    return _tri(resource_state_drives_adaptation)


def code_confidence_gating(triggers_downstream_action: bool,
                           quality_signal_drives_action: Optional[bool]) -> str:
    """Decision B: a downstream action (additional view, re-inference, referral,
    recapture, fallback) counts as confidence gating only when confidence,
    uncertainty, prediction quality or an equivalent inspection-quality signal
    explicitly triggers it. A learned view-selection policy alone is not gating."""
    if not triggers_downstream_action:
        return NO
    return _tri(quality_signal_drives_action)


PLATFORMS = ("smartphone", "in_sensor", "embedded_board", "server_gpu", "unknown")


def code_platform(platform: str) -> Dict[str, str]:
    """Decision C: return ``{"edge_device", "smartphone"}`` for a computing platform.

    In-sensor processing is edge computing but is never smartphone evidence
    unless the actual computing platform is a smartphone."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")
    return {
        "smartphone": {"smartphone": YES, "in_sensor": NO, "embedded_board": NO,
                       "server_gpu": NO, "unknown": UNKNOWN}[platform],
        "edge_device": {"smartphone": YES, "in_sensor": YES, "embedded_board": YES,
                        "server_gpu": NO, "unknown": UNKNOWN}[platform],
    }


def sha256_of(path: Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------
# Research-gap approval lifecycle (Step 10A).
#
# STATE 1  selection_status = researcher_approval_required, no candidate:
#          research_gap.md MUST NOT exist.
# STATE 2  selection_status = researcher_approved, candidate approved:
#          research_gap.md MUST exist and carry the approved wording, and
#          research_gap_approval.md §14 MUST record the explicit approval.
# Any other combination is an inconsistent state and is rejected.
# --------------------------------------------------------------------------
RESEARCH_GAP_FILE = "research/gap_analysis/research_gap.md"
APPROVAL_DOCUMENT = "research/gap_analysis/research_gap_approval.md"
SELECTION_CONFIG = "configs/gap_selection.yaml"
STATE_PENDING = "researcher_approval_required"
STATE_APPROVED = "researcher_approved"
DECISION_HEADING = "## 14. Researcher Decision"


def approved_decision(candidate_id: str) -> str:
    """The exact §14 decision line that records approval of ``candidate_id``."""
    return f"DECISION: {candidate_id} APPROVED AS THE FINAL RESEARCH GAP"


def _decision_lines(approval_text: str) -> List[str]:
    if DECISION_HEADING not in approval_text:
        return []
    section = approval_text.split(DECISION_HEADING, 1)[1].split("\n## ", 1)[0]
    return [ln.strip() for ln in section.splitlines() if ln.strip().startswith("DECISION:")]


def _gap_statement(gap_text: str) -> Optional[str]:
    """The blockquoted statement of §1 of research_gap.md (one line, '> ...')."""
    if "## 1. Research Gap" not in gap_text:
        return None
    section = gap_text.split("## 1. Research Gap", 1)[1].split("\n## ", 1)[0]
    quotes = [ln[2:].strip() for ln in section.splitlines() if ln.startswith("> ")]
    return quotes[0] if len(quotes) == 1 else None


def approval_state_errors(project_root: Path, selection_config: dict) -> List[str]:
    """Return the errors of the research-gap approval lifecycle (empty = consistent)."""
    root = Path(project_root)
    sel = selection_config.get("selection") or {}
    ready = selection_config.get("approval_ready") or {}
    status = sel.get("selection_status")
    gap_path, doc_path = root / RESEARCH_GAP_FILE, root / APPROVAL_DOCUMENT
    errors: List[str] = []
    if status == STATE_PENDING:
        if sel.get("selected_candidate") is not None or sel.get("approved_by") is not None:
            errors.append("pending state: a candidate is selected or approved")
        if sel.get("research_gap_file_created"):
            errors.append("pending state: research_gap_file_created must be false")
        if gap_path.exists():
            errors.append(f"pending state: {RESEARCH_GAP_FILE} exists")
        if doc_path.exists():
            for line in _decision_lines(doc_path.read_text(encoding="utf-8")):
                if " APPROVED AS THE FINAL RESEARCH GAP" in line:
                    errors.append("pending state: approval document records an approval")
        return errors
    if status != STATE_APPROVED:
        return [f"unknown selection_status {status!r}"]

    cid = sel.get("selected_candidate")
    entry = ready.get(cid) if cid else None
    if cid is None:
        errors.append("approved state: selected_candidate is null")
    elif cid not in selection_config.get("candidate_ids", []):
        errors.append(f"approved state: unknown candidate {cid!r}")
    elif not isinstance(entry, dict):
        errors.append(f"approved state: {cid} is not an approval-ready candidate")
    if not sel.get("approved_by") or not sel.get("approval_date"):
        errors.append("approved state: approved_by and approval_date are required")
    if not sel.get("research_gap_file_created"):
        errors.append("approved state: research_gap_file_created must be true")
    if isinstance(entry, dict):
        if entry.get("status") != STATE_APPROVED or entry.get("selected") is not True:
            errors.append(f"approved state: approval_ready.{cid} not marked approved/selected")
        if entry.get("researcher_decision") != approved_decision(cid):
            errors.append(f"approved state: approval_ready.{cid}.researcher_decision inconsistent")
        if sel.get("approval_date") and entry.get("approval_date") not in (None, sel.get("approval_date")):
            errors.append(f"approved state: approval_ready.{cid}.approval_date inconsistent")
    if not gap_path.exists():
        errors.append(f"approved state: {RESEARCH_GAP_FILE} missing")
    elif isinstance(entry, dict):
        if _gap_statement(gap_path.read_text(encoding="utf-8")) != entry.get("candidate_gap"):
            errors.append(f"approved state: {RESEARCH_GAP_FILE} wording differs from the approved wording")
    if not doc_path.exists():
        errors.append(f"approved state: {APPROVAL_DOCUMENT} missing")
    elif cid:
        doc = doc_path.read_text(encoding="utf-8")
        if _decision_lines(doc) != [approved_decision(cid)]:
            errors.append("approved state: approval document §14 does not record the explicit approval")
        statement = sel.get("approval_statement")
        if not statement or statement not in doc:
            errors.append("approved state: approval statement not recorded in the approval document")
    return errors


def lifecycle_errors(project_root: Path) -> List[str]:
    """Lifecycle errors for a project root. Without a selection config the
    project is treated as STATE 1, so research_gap.md must not exist."""
    root = Path(project_root)
    cfg_path = root / SELECTION_CONFIG
    if not cfg_path.exists():
        return [f"{RESEARCH_GAP_FILE} exists without an approval lifecycle"] if (root / RESEARCH_GAP_FILE).exists() else []
    with open(cfg_path, "r", encoding="utf-8") as f:
        return approval_state_errors(root, yaml.safe_load(f) or {})


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _csv_header(path: Path) -> List[str]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


class GapEvaluationValidator:
    """Read-only checks for the Step 9.8 evaluation artefacts."""

    def __init__(self, config: dict, project_root: Path):
        self.config = config
        self.root = Path(project_root)

    @classmethod
    def from_file(cls, config_path: Path, project_root: Optional[Path] = None) -> "GapEvaluationValidator":
        config_path = Path(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        root = Path(project_root) if project_root else config_path.resolve().parent.parent
        return cls(config, root)

    # ------------------------------------------------------------------ paths
    def path(self, key: str) -> Path:
        return self.root / self.config["files"][key]

    @property
    def candidate_ids(self) -> List[str]:
        return list(self.config["candidates"].keys())

    @property
    def guards(self) -> dict:
        return self.config["guards"]

    # ---------------------------------------------------------- frozen corpus
    def check_frozen_corpus(self) -> List[str]:
        """Return errors if papers.csv differs from the recorded freeze."""
        frozen = self.config["frozen_corpus"]
        papers = self.root / frozen["path"]
        errors = []
        actual_sha = sha256_of(papers)
        if actual_sha != frozen["sha256"]:
            errors.append(f"papers.csv SHA-256 {actual_sha} != frozen {frozen['sha256']}")
        header = _csv_header(papers)
        if len(header) != frozen["columns"] or header != list(PAPERS_SCHEMA_HEADERS):
            errors.append(f"papers.csv header has {len(header)} columns or differs from the schema")
        records = _read_csv(papers)
        if len(records) != frozen["records"]:
            errors.append(f"papers.csv has {len(records)} records, expected {frozen['records']}")
        return errors

    def corpus_records(self) -> Dict[str, Dict[str, str]]:
        papers = self.root / self.config["frozen_corpus"]["path"]
        return {r["paper_id"]: r for r in _read_csv(papers)}

    def visual_scope(self) -> Dict[str, str]:
        return {r["paper_id"]: r["visual_inspection_scope"] for r in _read_csv(self.root / VISUAL_SCOPE_FILE)}

    # -------------------------------------------------------- counterexamples
    def counterexamples(self) -> List[Dict[str, str]]:
        return _read_csv(self.path("counterexamples"))

    def check_counterexamples(self) -> List[str]:
        """Validate fields, vocabularies, corpus reproduction and Unknown handling."""
        errors = []
        path = self.path("counterexamples")
        expected = list(self.config["counterexample_fields"])
        if _csv_header(path) != expected:
            errors.append("counterexample_candidates.csv header does not match configs/gap_evaluation.yaml")
        allowed_values = set(self.config["characteristic_values"])
        levels = set(self.config["evidence_levels"])
        strengths = set(self.config["counterexample_strengths"])
        statuses = set(self.config["verification_statuses"])
        corpus = self.corpus_records()
        scope = self.visual_scope()
        for i, row in enumerate(self.counterexamples(), start=2):
            where = f"row {i} ({row.get('paper_id_or_external_id')}, {row.get('candidate_id')})"
            if row["candidate_id"] not in self.candidate_ids:
                errors.append(f"{where}: unknown candidate_id {row['candidate_id']!r}")
            elif row["candidate_gap"] != self.config["candidates"][row["candidate_id"]]:
                errors.append(f"{where}: candidate_gap text differs from the configuration")
            for field in self.config["characteristic_fields"]:
                if row[field] not in allowed_values:
                    errors.append(f"{where}: {field}={row[field]!r} is not Yes/No/Unknown")
            if row["evidence_level"] not in levels:
                errors.append(f"{where}: evidence_level {row['evidence_level']!r} not allowed")
            if row["counterexample_strength"] not in strengths:
                errors.append(f"{where}: counterexample_strength {row['counterexample_strength']!r} not allowed")
            if row["verification_status"] not in statuses:
                errors.append(f"{where}: verification_status {row['verification_status']!r} not allowed")
            for required in ("title", "source_url", "reason"):
                if not row[required].strip():
                    errors.append(f"{where}: empty {required}")
            pid = row["paper_id_or_external_id"]
            if CORPUS_ID_PATTERN.match(pid):
                errors.extend(self._check_corpus_row(where, row, corpus, scope))
            errors.extend(self._check_unknown_not_converted(where, row))
        return errors

    def _check_corpus_row(self, where, row, corpus, scope) -> List[str]:
        """A corpus record must reproduce its frozen values exactly (no recoding)."""
        errors = []
        pid = row["paper_id_or_external_id"]
        if pid not in corpus:
            return [f"{where}: {pid} is not in papers.csv"]
        if row["verification_status"] != "corpus_record_reproduced":
            errors.append(f"{where}: corpus record must have verification_status corpus_record_reproduced")
        for field in self.config["characteristic_fields"]:
            expected = scope.get(pid) if field == "visual_inspection" else corpus[pid][field]
            if row[field] != expected:
                errors.append(f"{where}: {field}={row[field]!r} differs from corpus value {expected!r}")
        return errors

    @staticmethod
    def _check_unknown_not_converted(where, row) -> List[str]:
        """Snippet-level or unresolved evidence cannot support a No without a stated basis."""
        if row["evidence_level"] not in ("search_snippet_only", "unresolved"):
            return []
        errors = []
        for field in ("smartphone", "visual_inspection", "resource_awareness", "adaptive_inference",
                      "energy_evaluation", "thermal_evaluation", "confidence_gating", "multi_view"):
            if row[field] == "No" and f"{field} No because" not in row["notes"]:
                errors.append(f"{where}: {field}=No at {row['evidence_level']} without a stated basis")
        return errors

    def check_corrections(self) -> List[str]:
        """Confirmed partial counterexamples stay partial; locked evidence levels are not upgraded."""
        errors = []
        rows = self.counterexamples()
        for pid, spec in (self.config.get("confirmed_partial_counterexamples") or {}).items():
            for cid in spec["candidates"]:
                match = [r for r in rows if r["paper_id_or_external_id"] == pid and r["candidate_id"] == cid]
                if not match:
                    errors.append(f"{pid}: confirmed partial counterexample to {cid} is missing")
                for r in match:
                    if r["counterexample_strength"] != "partial":
                        errors.append(f"{pid}/{cid}: strength {r['counterexample_strength']!r}, must stay partial")
        for pid, level in (self.config.get("locked_evidence_levels") or {}).items():
            for r in rows:
                if r["paper_id_or_external_id"] == pid and r["evidence_level"] != level:
                    errors.append(f"{pid}/{r['candidate_id']}: evidence_level {r['evidence_level']!r} != locked {level!r}")
        return errors

    def meets_full_criteria(self, row: Dict[str, str]) -> bool:
        """True only if every criterion of the row's narrowed candidate is Yes."""
        fields = self.config["full_counterexample_criteria"][row["candidate_id"]]
        return all(row[f] == YES for f in fields)

    def check_full_criteria(self) -> List[str]:
        """'full' requires every criterion; a row meeting every criterion must be 'full'."""
        errors = []
        for r in self.counterexamples():
            where = f"{r['paper_id_or_external_id']}/{r['candidate_id']}"
            meets = self.meets_full_criteria(r)
            if r["counterexample_strength"] == "full" and not meets:
                errors.append(f"{where}: classified full but does not meet every criterion")
            if meets and r["counterexample_strength"] != "full":
                errors.append(f"{where}: meets every criterion but is classified {r['counterexample_strength']!r}")
        return errors

    def external_rows(self) -> List[Dict[str, str]]:
        return [r for r in self.counterexamples() if not CORPUS_ID_PATTERN.match(r["paper_id_or_external_id"])]

    def externals_absent_from_corpus(self) -> List[str]:
        """Return external counterexample titles that appear in papers.csv (should be none)."""
        def norm(text):
            return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
        corpus_titles = {norm(r["title"]) for r in self.corpus_records().values()}
        return sorted({r["title"] for r in self.external_rows() if norm(r["title"]) in corpus_titles})

    # ------------------------------------------------------------- search log
    def search_entries(self) -> Dict[str, Dict[str, str]]:
        """Parse each '### Snn' block of the search log into a field dictionary."""
        text = self.path("search_log").read_text(encoding="utf-8")
        entries = {}
        matches = list(SEARCH_HEADING_PATTERN.finditer(text))
        for idx, match in enumerate(matches):
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            block = re.split(r"\n---|\n#{2,3} ", text[match.end():end], maxsplit=1)[0]
            fields = {}
            for line in block.splitlines():
                m = TABLE_ROW_PATTERN.match(line.strip())
                if m and not set(m.group("key")) <= set(":- "):
                    fields[m.group("key").strip()] = m.group("value").strip()
            entries[match.group(1)] = fields
        return entries

    def check_search_log(self) -> List[str]:
        errors = []
        entries = self.search_entries()
        if not entries:
            return ["targeted_search_log.md has no search entries"]
        for sid, fields in entries.items():
            for name in SEARCH_LOG_REQUIRED_FIELDS:
                if not fields.get(name, "").strip() or fields.get(name, "").strip() == "Value":
                    errors.append(f"{sid}: missing '{name}'")
            if fields.get("Results returned") and not re.match(r"^\d+", fields["Results returned"]):
                errors.append(f"{sid}: 'Results returned' must start with the returned count")
            if fields.get("Relevant results inspected") and not re.match(r"^\d+", fields["Relevant results inspected"]):
                errors.append(f"{sid}: 'Relevant results inspected' must start with a count")
            if not any(c in fields.get("Candidate", "") for c in self.candidate_ids):
                errors.append(f"{sid}: candidate not one of {self.candidate_ids}")
        return errors

    # ----------------------------------------------------------------- matrix
    def matrix(self) -> List[Dict[str, str]]:
        return _read_csv(self.path("matrix"))

    def check_matrix(self) -> List[str]:
        errors = []
        path = self.path("matrix")
        if _csv_header(path) != list(self.config["matrix_fields"]):
            errors.append("candidate_gap_matrix.csv header does not match configs/gap_evaluation.yaml")
        dims = [d["name"] for d in self.config["dimensions"]]
        assessments = set(self.config["assessment_values"])
        confidences = set(self.config["confidence_values"])
        burdens = set(self.config["unknown_burden_values"])
        level_tokens = set(self.config["evidence_levels"]) | {"not_applicable"}
        seen = {}
        for i, row in enumerate(self.matrix(), start=2):
            where = f"row {i} ({row.get('candidate_id')}, {row.get('criterion')})"
            seen.setdefault(row["candidate_id"], []).append(row["criterion"])
            if row["candidate_id"] not in self.candidate_ids:
                errors.append(f"{where}: unknown candidate_id")
            if row["criterion"] not in dims:
                errors.append(f"{where}: criterion not defined in the framework")
            if row["assessment"] not in assessments:
                errors.append(f"{where}: assessment {row['assessment']!r} not in the qualitative vocabulary")
            if row["confidence"] not in confidences:
                errors.append(f"{where}: confidence {row['confidence']!r} not allowed")
            if row["unknown_burden"] not in burdens:
                errors.append(f"{where}: unknown_burden {row['unknown_burden']!r} not allowed")
            if not any(tok in row["evidence_level"] for tok in level_tokens):
                errors.append(f"{where}: evidence_level names no recognised level")
            for field in ("evidence", "limitations"):
                if not row[field].strip():
                    errors.append(f"{where}: empty {field}")
        for cid in self.candidate_ids:
            if sorted(seen.get(cid, [])) != sorted(dims):
                errors.append(f"{cid}: matrix must contain each of the {len(dims)} criteria exactly once")
        return errors

    # ---------------------------------------------------------- language/ranking
    def forbidden_language(self, text: str) -> List[str]:
        """Return forbidden novelty, ranking or selection phrases found in ``text``."""
        lowered = " ".join(text.lower().split())
        for allowed in self.guards.get("allowed_negations", []):
            lowered = lowered.replace(allowed.lower(), " ")
        return [p for p in self.guards["forbidden_phrases"] if p.lower() in lowered]

    def check_no_ranking(self) -> List[str]:
        """Detect columns, config keys or values that would rank, score or select a candidate."""
        errors = []
        keys = [k.lower() for k in self.guards["forbidden_candidate_keys"]]
        for name in ("counterexamples", "matrix"):
            for column in _csv_header(self.path(name)):
                if any(k == column.lower() or column.lower().startswith(k + "_") for k in keys):
                    errors.append(f"{name}: column {column!r} implies ranking or selection")
        for cid, text in self.config["candidates"].items():
            if not isinstance(text, str):
                errors.append(f"{cid}: candidate entry must be plain text, not a structured (scorable) entry")
        for row in self.matrix():
            if re.search(r"\d", row["assessment"] + row["confidence"]):
                errors.append(f"{row['candidate_id']}/{row['criterion']}: numeric assessment or confidence")
        doc = self.path("evaluation").read_text(encoding="utf-8")
        if re.search(r"\b(rank(ed|ing)?|score)\s*[:=#]?\s*\d", doc, re.IGNORECASE):
            errors.append("evaluation: numeric rank or score found")
        return errors

    # ------------------------------------------------------------- evaluation
    def check_evaluation(self) -> List[str]:
        errors = []
        doc = self.path("evaluation").read_text(encoding="utf-8")
        headings = re.findall(r"^##\s+(\d+)\.\s+(.+?)\s*$", doc, re.MULTILINE)
        titles = [t for _, t in headings]
        if titles != list(EVALUATION_SECTIONS):
            errors.append(f"evaluation sections differ from the required 15: {titles}")
        lines = [ln.strip() for ln in doc.strip().splitlines() if ln.strip()]
        if not lines or lines[-1] != self.guards["required_closing_sentence"]:
            errors.append("evaluation does not end with the required closing sentence")
        found = self.forbidden_language(doc)
        if found:
            errors.append(f"evaluation contains forbidden phrases: {found}")
        for name in self.config["dimensions"]:
            if name["name"] not in doc:
                errors.append(f"evaluation does not define dimension {name['name']!r}")
        return errors

    def check_forbidden_files(self) -> List[str]:
        """Forbidden files must not exist. Files listed under ``lifecycle_governed_files``
        (research_gap.md) are instead governed by the approval lifecycle: allowed only in
        a consistent approved state, rejected in every other state."""
        governed = set(self.guards.get("lifecycle_governed_files", []))
        errors = [f"{p} exists" for p in self.guards["forbidden_files"]
                  if p not in governed and (self.root / p).exists()]
        if governed:
            errors += lifecycle_errors(self.root)
        return errors

    # ------------------------------------------------------------------- all
    def validate(self) -> List[str]:
        """Run every check and return the combined list of errors (empty = valid)."""
        errors = []
        errors += self.check_frozen_corpus()
        errors += self.check_counterexamples()
        errors += self.check_corrections()
        errors += self.check_full_criteria()
        errors += self.check_search_log()
        errors += self.check_matrix()
        errors += self.check_no_ranking()
        errors += self.check_evaluation()
        errors += self.check_forbidden_files()
        errors += [f"external counterexample present in papers.csv: {t}" for t in self.externals_absent_from_corpus()]
        for name in ("counterexamples", "search_log", "matrix"):
            found = self.forbidden_language(self.path(name).read_text(encoding="utf-8"))
            if found:
                errors.append(f"{name}: forbidden phrases {found}")
        return errors
