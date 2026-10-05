"""
Validation of the Step 9.9 Phase A research-gap selection framework.

Reads ``configs/gap_selection.yaml`` and checks the artefacts it names:

* ``final_gap_selection_matrix.csv``: one qualitative row per candidate x
  criterion (A-Q);
* ``final_gap_selection.md``: the 16-section selection document.

The validator is read-only. It never writes to ``research/literature/`` and
never ranks, scores or selects a candidate. Phase A guard-rails enforced here:

* the canonical corpus is frozen and the candidate wording matches Step 9.8;
* assessments are qualitative (no numeric ranks, scores or weights);
* no candidate is selected and ``research_gap.md`` does not exist;
* candidate research questions are measurable, falsifiable and labelled as
  candidates rather than final RQs;
* Unknowns, counterexamples and dataset uncertainty stay explicit;
* existing literature components are never labelled novel;
* final selection stays researcher-controlled (``can_select``).
"""
import csv
import re
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from src.literature.gap_evaluation import sha256_of

DOCUMENT_SECTIONS = (
    "Purpose",
    "Frozen corpus boundary",
    "Selection principles",
    "Evaluation criteria",
    "GC-01 analysis",
    "GC-02 analysis",
    "GC-03 analysis",
    "Comparative strengths",
    "Comparative weaknesses",
    "Research-question feasibility",
    "Experimental feasibility",
    "Dataset feasibility",
    "Contribution analysis",
    "Risk analysis",
    "Evidence still required",
    "Researcher decision",
)

CONFIRMED_PARTIALS = {
    "GC-01": ("2608.14727", "PMC11435656", "2509.17136"),
    "GC-02": ("2603.16451", "2509.17136", "2603.26603"),
    "GC-03": ("PMC11435656", "ActiveInspect", "2608.14727", "2509.17136", "RobustDefect-LLM"),
}


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class GapSelectionValidator:
    """Read-only checks for the Step 9.9 Phase A selection framework."""

    def __init__(self, config: dict, project_root: Path):
        self.config = config
        self.root = Path(project_root)

    @classmethod
    def from_file(cls, config_path: Path, project_root: Optional[Path] = None) -> "GapSelectionValidator":
        config_path = Path(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        root = Path(project_root) if project_root else config_path.resolve().parent.parent
        return cls(config, root)

    # ---------------------------------------------------------------- inputs
    def path(self, key: str) -> Path:
        return self.root / self.config["files"][key]

    def approved_wording(self) -> Dict[str, str]:
        with open(self.root / self.config["candidate_source"], "r", encoding="utf-8") as f:
            return yaml.safe_load(f)["candidates"]

    def matrix(self) -> List[Dict[str, str]]:
        return _read_csv(self.path("matrix"))

    def document(self) -> str:
        return self.path("document").read_text(encoding="utf-8")

    # ---------------------------------------------------------------- checks
    def check_frozen_corpus(self) -> List[str]:
        frozen = self.config["frozen_corpus"]
        papers = self.root / frozen["path"]
        errors = []
        if sha256_of(papers) != frozen["sha256"]:
            errors.append("papers.csv SHA-256 differs from the frozen value")
        rows = _read_csv(papers)
        if len(rows) != frozen["records"] or len(rows[0]) != frozen["columns"]:
            errors.append("papers.csv record or column count differs from the freeze")
        ids = [r["paper_id"] for r in rows]
        if len(ids) != len(set(ids)):
            errors.append("papers.csv contains duplicate IDs")
        return errors

    def check_candidates(self) -> List[str]:
        errors = []
        ids = self.config["candidate_ids"]
        if ids != ["GC-01", "GC-02", "GC-03"]:
            errors.append(f"candidate_ids must be exactly GC-01, GC-02, GC-03, got {ids}")
        wording = self.approved_wording()
        if sorted(wording) != sorted(ids):
            errors.append("approved wording does not cover exactly the three candidates")
        doc = self.document()
        for cid in ids:
            if f"**Candidate (Step 9.8 wording).** {wording[cid]}" not in doc:
                errors.append(f"{cid}: document does not quote the approved Step 9.8 wording")
        for row in self.matrix():
            if row["candidate_id"] not in ids:
                errors.append(f"matrix has unknown candidate {row['candidate_id']!r}")
        return errors

    def check_matrix(self) -> List[str]:
        errors = []
        with open(self.path("matrix"), "r", encoding="utf-8", newline="") as f:
            header = next(csv.reader(f))
        if header != list(self.config["matrix_fields"]):
            errors.append("matrix header differs from configs/gap_selection.yaml")
        expected = [f"{k}. {v}" for k, v in self.config["criteria"].items()]
        seen: Dict[str, List[str]] = {}
        for row in self.matrix():
            seen.setdefault(row["candidate_id"], []).append(row["criterion"])
            where = f"{row['candidate_id']}/{row['criterion']}"
            if row["assessment"] not in self.config["assessment_values"]:
                errors.append(f"{where}: assessment {row['assessment']!r} not in the qualitative vocabulary")
            if row["confidence"] not in self.config["confidence_values"]:
                errors.append(f"{where}: confidence {row['confidence']!r} not allowed")
            for field in ("supporting_evidence", "weakening_evidence", "unknowns", "counterexamples",
                          "verification_needed"):
                if not row[field].strip():
                    errors.append(f"{where}: empty {field}")
            if "full counterexample" in row["counterexamples"].lower() and "no full" not in row["counterexamples"].lower():
                errors.append(f"{where}: claims a full counterexample")
        for cid in self.config["candidate_ids"]:
            if seen.get(cid) != expected:
                errors.append(f"{cid}: matrix must list criteria A-Q exactly once, in order")
        return errors

    def check_no_ranking(self) -> List[str]:
        errors = []
        keys = [k.lower() for k in self.config["guards"]["forbidden_keys"]]
        for column in self.config["matrix_fields"]:
            if any(column.lower() == k or column.lower().startswith(k + "_") for k in keys):
                errors.append(f"matrix column {column!r} implies ranking or scoring")
        for key in self.config:
            if key.lower() in keys:
                errors.append(f"config key {key!r} implies ranking or scoring")
        for row in self.matrix():
            if re.search(r"\d", row["assessment"] + row["confidence"]):
                errors.append(f"{row['candidate_id']}/{row['criterion']}: numeric assessment or confidence")
        doc = self.document()
        if re.search(r"\b(rank(ed|ing)?|score|weight(ed)?)\s*[:=#]?\s*\d", doc, re.IGNORECASE):
            errors.append("document contains a numeric rank, score or weight")
        if re.search(r"\b(1st|2nd|3rd)\b", doc):
            errors.append("document contains ordinal placement")
        return errors

    def forbidden_language(self, text: str) -> List[str]:
        lowered = " ".join(text.lower().split())
        for allowed in self.config["guards"]["allowed_negations"]:
            lowered = lowered.replace(allowed.lower(), " ")
        return [p for p in self.config["guards"]["forbidden_phrases"] if p.lower() in lowered]

    def check_document(self) -> List[str]:
        errors = []
        doc = self.document()
        titles = [t for _, t in re.findall(r"^##\s+(\d+)\.\s+(.+?)\s*$", doc, re.MULTILINE)]
        if titles != list(DOCUMENT_SECTIONS):
            errors.append(f"document sections differ from the required 16: {titles}")
        lines = [ln.strip() for ln in doc.strip().splitlines() if ln.strip()]
        if not lines or lines[-1] != self.config["guards"]["required_closing_sentence"]:
            errors.append("document does not end with the required closing sentence")
        for text, name in ((doc, "document"), (self.path("matrix").read_text(encoding="utf-8"), "matrix")):
            found = self.forbidden_language(text)
            if found:
                errors.append(f"{name}: forbidden phrases {found}")
        return errors

    def check_selection_state(self) -> List[str]:
        errors = []
        sel = self.config["selection"]
        if sel.get("selected_candidate") is not None or sel.get("approved_by") is not None:
            errors.append("a candidate is selected or approved in Phase A")
        if sel.get("research_gap_file_created"):
            errors.append("research_gap_file_created must be false in Phase A")
        for rel in self.config["guards"]["forbidden_files"]:
            if (self.root / rel).exists():
                errors.append(f"{rel} exists")
        return errors

    def check_research_questions(self) -> List[str]:
        errors = []
        status = self.config["rq_status"]
        if "not final" not in status.lower() or "candidate" not in status.lower():
            errors.append("rq_status must label RQs as candidate, not final")
        doc = self.document()
        for cid in self.config["candidate_ids"]:
            rqs = self.config["candidate_research_questions"].get(cid, [])
            if [r["type"] for r in rqs] != ["primary", "secondary", "evaluation"]:
                errors.append(f"{cid}: needs RQ1 primary, RQ2 secondary, RQ3 evaluation")
            for rq in rqs:
                if not rq.get("measurable_outcomes"):
                    errors.append(f"{rq['id']}: no measurable outcomes")
                if not rq.get("falsified_if", "").strip():
                    errors.append(f"{rq['id']}: no falsification condition")
                if f"**{rq['id']} ({rq['type']}; {status}).**" not in doc:
                    errors.append(f"{rq['id']}: not presented as a candidate RQ in the document")
        if re.search(r"final (pocketinspect )?research questions? (is|are)\b", doc, re.IGNORECASE):
            errors.append("document presents final research questions")
        return errors

    def check_datasets(self) -> List[str]:
        errors = []
        allowed = set(self.config["dataset_availability_values"])
        for d in self.config["datasets"]:
            if d["availability"] not in allowed:
                errors.append(f"{d['name']}: availability {d['availability']!r} asserted without verification")
            if not d.get("source"):
                errors.append(f"{d['name']}: no source")
        return errors

    def check_contributions(self) -> List[str]:
        errors = []
        labels = set(self.config["contribution_labels"])
        for cid, c in self.config["contributions"].items():
            for e in c["existing_components"]:
                if e["label"] != "demonstrated_in_literature":
                    errors.append(f"{cid}: existing component labelled {e['label']!r}")
                if "novel" in (e["component"] + e["label"]).lower():
                    errors.append(f"{cid}: existing component described as novel")
                if not e.get("evidence"):
                    errors.append(f"{cid}: existing component without evidence")
            for p in c["potential_contribution"]:
                if p["label"] != "requires_empirical_validation" or p["label"] not in labels:
                    errors.append(f"{cid}: potential contribution not marked as requiring validation")
        return errors

    def check_counterexamples(self) -> List[str]:
        """Each candidate's counterexample-risk row names its known partial counterexamples."""
        errors = []
        for row in self.matrix():
            if not row["criterion"].startswith("C."):
                continue
            for name in CONFIRMED_PARTIALS[row["candidate_id"]]:
                if name not in row["counterexamples"] + row["weakening_evidence"] + row["supporting_evidence"]:
                    errors.append(f"{row['candidate_id']}: counterexample-risk row omits {name}")
            if "partial" not in row["counterexamples"].lower():
                errors.append(f"{row['candidate_id']}: counterexample-risk row does not mark partial counterexamples")
        return errors

    def check_gate(self) -> List[str]:
        errors = []
        statuses = set(self.config["gate_status_values"])
        qs = list(self.config["gate_questions"])
        for cid in self.config["candidate_ids"]:
            gate = self.config["selection_gate"].get(cid, {})
            if list(gate) != qs:
                errors.append(f"{cid}: gate must answer {qs}")
            for q, (status, why) in gate.items():
                if status not in statuses:
                    errors.append(f"{cid}/{q}: status {status!r} not allowed")
                if not why.strip():
                    errors.append(f"{cid}/{q}: no rationale")
        return errors

    def can_select(self, candidate_id: str) -> bool:
        """Selection is permitted only with explicit researcher approval for that candidate
        and every gate question satisfied. In Phase A this is always False."""
        sel = self.config["selection"]
        if not sel.get("approved_by") or sel.get("selected_candidate") != candidate_id:
            return False
        gate = self.config["selection_gate"].get(candidate_id, {})
        return bool(gate) and all(status == "satisfied" for status, _ in gate.values())

    def validate(self) -> List[str]:
        errors = []
        for check in (self.check_frozen_corpus, self.check_candidates, self.check_matrix, self.check_no_ranking,
                      self.check_document, self.check_selection_state, self.check_research_questions,
                      self.check_datasets, self.check_contributions, self.check_counterexamples, self.check_gate):
            errors += check()
        return errors
