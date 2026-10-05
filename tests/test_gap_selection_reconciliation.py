"""
Step 9.9C tests: reconciliation of Step 9.9 Phase A and Step 9.9B, and the
researcher approval gate for GC-03.

At Step 9.9C GC-03 was approval-ready but not selected. Step 10A recorded the
researcher's explicit approval, so these tests now check the approved state
(the pending wording is kept in the approval document as audit context).
"""
import csv
import hashlib
import re
import unittest
from pathlib import Path

import yaml

from src.literature.gap_selection import GapSelectionValidator

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "research" / "literature" / "papers.csv"
GAP_DIR = ROOT / "research" / "gap_analysis"
SEL_CFG = ROOT / "configs" / "gap_selection.yaml"
CLOSURE_CFG = ROOT / "configs" / "gc03_evidence_closure.yaml"
APPROVAL = GAP_DIR / "research_gap_approval.md"
SELECTION_DOC = GAP_DIR / "final_gap_selection.md"
MATRIX = GAP_DIR / "final_gap_selection_matrix.csv"
COUNTEREXAMPLES = GAP_DIR / "counterexample_candidates.csv"
FROZEN_SHA = "c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521"

APPROVAL_WORDING = (
    "Within the reviewed literature corpus, there is limited evidence of an integrated resource-aware smartphone "
    "visual-inspection system in which device-state-driven runtime adaptation is coupled with confidence-aware "
    "downstream verification, particularly for recovering inspection performance under resource-induced "
    "model/configuration degradation."
)
PRIMARY_RQ = (
    "Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained "
    "smartphone dynamically downgrades its inference configuration under changing device conditions?"
)
CONTRIBUTION = (
    "An empirical investigation of whether confidence-aware downstream verification can recover inspection "
    "performance degraded by resource-driven runtime configuration changes on a resource-constrained smartphone, "
    "including analysis of accuracy, calibration, latency, energy, thermal behavior, and verification overhead."
)
APPROVAL_SECTIONS = [
    "Candidate Status", "Candidate Research Gap", "Candidate Research Question", "Evidence Supporting the Candidate",
    "Counterexamples", "Q2 — Unknown Burden", "Q8 — Contribution Distinctiveness", "Q10 — Literature Overturn Risk",
    "Candidate Contribution", "Candidate Hypotheses", "Candidate Experimental Design", "Dataset Feasibility",
    "Known Limitations", "Researcher Decision",
]
NOVELTY_PATTERNS = [
    r"\bno existing (system|work|study|research)\b", r"\bno one has\b", r"\bthis is the first\b", r"\bthe first\b",
    r"\bfirst to\b", r"\bis novel\b", r"\bnovel contribution\b", r"\bunprecedented\b", r"\bnever been (studied|done)\b",
]


def _load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _gc03_row(pid):
    rows = [r for r in _rows(COUNTEREXAMPLES) if r["candidate_id"] == "GC-03" and r["paper_id_or_external_id"] == pid]
    assert len(rows) == 1, (pid, len(rows))
    return rows[0]


class TestReconciliationAndApprovalGate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sel = _load(SEL_CFG)
        cls.closure = _load(CLOSURE_CFG)
        cls.approval = APPROVAL.read_text(encoding="utf-8")
        cls.selection_doc = SELECTION_DOC.read_text(encoding="utf-8")
        cls.validator = GapSelectionValidator.from_file(SEL_CFG, ROOT)

    # 1-4. frozen corpus
    def test_frozen_corpus(self):
        self.assertEqual(hashlib.sha256(PAPERS.read_bytes()).hexdigest(), FROZEN_SHA)
        with open(PAPERS, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(len(rows) - 1, 54)
        self.assertEqual(len(rows[0]), 31)
        ids = [r[0] for r in rows[1:]]
        self.assertEqual(len(ids), len(set(ids)))

    # 5-6. selection state (Step 10A: researcher approved GC-03)
    def test_selection_state(self):
        sel = self.sel["selection"]
        self.assertEqual(sel["selected_candidate"], "GC-03")
        self.assertEqual(sel["approved_by"], "researcher")
        self.assertEqual(sel["selection_status"], "researcher_approved")
        self.assertEqual(sel["previous_status"], "researcher_approval_required")
        self.assertEqual(sel["approval_statement"], "Approve GC-03 as the final research gap.")
        self.assertTrue(sel["research_gap_file_created"])
        self.assertTrue(self.sel["approval_ready"]["GC-03"]["selected"])
        # the automated gate is unchanged (partially satisfied items remain)
        for cid in ("GC-01", "GC-02", "GC-03"):
            self.assertFalse(self.validator.can_select(cid))
        self.assertEqual(self.validator.validate(), [])

    # 7-8. research_gap.md present; approval document records the approval with audit trail
    def test_approval_document(self):
        self.assertTrue((GAP_DIR / "research_gap.md").exists())
        self.assertTrue(APPROVAL.exists())
        self.assertTrue(self.approval.startswith("# Research Gap Approval — GC-03\n"))
        headings = re.findall(r"^## (\d+)\. (.+)$", self.approval, flags=re.MULTILINE)
        self.assertEqual([h[1] for h in headings], APPROVAL_SECTIONS)
        self.assertEqual([int(h[0]) for h in headings], list(range(1, 15)))
        status = self.approval.split("## 1. Candidate Status", 1)[1].split("\n## ", 1)[0]
        self.assertIn("Status:\nRESEARCHER APPROVED — GC-03", status)
        self.assertIn('Audit trail (Step 9.9C, commit `72a828b`): status was "RESEARCHER APPROVAL REQUIRED"', status)
        decision = self.approval.split("## 14. Researcher Decision", 1)[1].strip()
        self.assertEqual(decision.splitlines()[0], "DECISION: GC-03 APPROVED AS THE FINAL RESEARCH GAP")
        self.assertEqual([ln for ln in decision.splitlines() if ln.startswith("DECISION:")],
                         ["DECISION: GC-03 APPROVED AS THE FINAL RESEARCH GAP"])
        self.assertIn('this section read "PENDING EXPLICIT RESEARCHER APPROVAL"', decision)
        self.assertIn('"Approve GC-03 as the final research gap."', decision)

    # 9. corpus-bounded GC-03 wording
    def test_wording_corpus_bounded(self):
        wording = self.sel["approval_ready"]["GC-03"]["candidate_gap"]
        self.assertEqual(wording, APPROVAL_WORDING)
        self.assertTrue(wording.startswith("Within the reviewed literature corpus"))
        self.assertIn(APPROVAL_WORDING, self.approval)
        self.assertEqual(self.sel["approval_ready"]["GC-03"]["status"], "researcher_approved")
        self.assertEqual(self.sel["approval_ready"]["GC-03"]["previous_status"], "approval_ready_candidate")
        rq1 = self.sel["candidate_research_questions"]["GC-03"][0]
        self.assertEqual(rq1["text"], PRIMARY_RQ)
        self.assertIn(PRIMARY_RQ, self.approval)
        self.assertEqual(rq1["independent_variables"],
                         ["resource/device state", "selected inference configuration", "adaptation state"])
        self.assertEqual(rq1["potential_mediator"], "confidence threshold / uncertainty")

    # 10-12. Q2, Q8, Q10
    def test_gate_answers(self):
        expected = {"Q2": "conditionally_acceptable", "Q8": "conditionally_distinct", "Q10": "moderate"}
        closure = self.sel["evidence_closure"]["GC-03"]
        for q, value in expected.items():
            self.assertEqual(closure[q], value)
            self.assertEqual(self.closure["gate_answers"][q]["result"], value)
            status, why = self.sel["selection_gate"]["GC-03"][q]
            self.assertEqual(status, "partially_satisfied")
            self.assertIn("Step 9.9B", why)
            for limitation in ("P001", "AIVD", "Choi 2026", "substituted", "English-only", "one results page",
                               "Unknown burden", "ActiveInspect"):
                self.assertIn(limitation, why, (q, limitation))
        self.assertIn("**Conditionally acceptable.**", self.approval)
        self.assertIn("**Conditionally distinct.**", self.approval)
        self.assertIn("**Moderate.**", self.approval)
        # GC-01 and GC-02 keep their Phase A unresolved status
        for cid in ("GC-01", "GC-02"):
            for q in ("Q2", "Q8", "Q10"):
                self.assertEqual(self.sel["selection_gate"][cid][q][0], "unresolved")

    # 13. full counterexamples == 0
    def test_zero_full_counterexamples(self):
        self.assertEqual(self.sel["evidence_closure"]["GC-03"]["full_counterexamples"], 0)
        self.assertFalse(any(r["counterexample_strength"] == "full" for r in _rows(COUNTEREXAMPLES)))
        self.assertIn("**Full counterexamples identified: 0**", self.approval)
        self.assertIn("**Full counterexamples identified: 0.**", self.selection_doc)

    # 14-16. P001, AIVD, Choi 2026 remain unresolved/potential
    def test_unresolved_potentials(self):
        for pid in ("P001", "arXiv:2601.04734", "IEEE TVT 2026 (Choi et al.)"):
            row = _gc03_row(pid)
            self.assertEqual(row["counterexample_strength"], "potential", pid)
            self.assertIn(row["evidence_level"], ("abstract_only", "search_snippet_only"), pid)
        self.assertEqual(self.closure["priority_papers"]["P001"]["status"], "unresolved")
        unresolved = " ".join(self.sel["evidence_closure"]["GC-03"]["unresolved_evidence"])
        for name in ("P001", "AIVD", "Choi"):
            self.assertIn(name, unresolved)

    # 17. no automatic novelty claim
    def test_no_novelty_claims(self):
        for name, text in (("approval", self.approval), ("selection", self.selection_doc)):
            lowered = " ".join(text.lower().split())
            for allowed in self.sel["guards"]["allowed_negations"]:
                lowered = lowered.replace(allowed.lower(), " ")
            for pattern in NOVELTY_PATTERNS:
                self.assertIsNone(re.search(pattern, lowered), (name, pattern))
        self.assertEqual(self.validator.forbidden_language(self.approval), [])

    # 18. no numerical ranking
    def test_no_numeric_ranking(self):
        self.assertEqual(self.validator.check_no_ranking(), [])
        with open(MATRIX, encoding="utf-8", newline="") as f:
            header = next(csv.reader(f))
        self.assertEqual(header, self.sel["matrix_fields"])
        for r in _rows(MATRIX):
            self.assertNotRegex(r["assessment"] + r["confidence"], r"\d")
            self.assertNotIn("selected", r["assessment"])
        self.assertNotRegex(self.approval, r"\b(rank(ed|ing)?|score|weight(ed)?)\s*[:=#]?\s*\d")
        gc03 = [r for r in _rows(MATRIX) if r["candidate_id"] == "GC-03"]
        self.assertTrue(any("approval-ready candidate" in r["verification_needed"] for r in gc03))
        self.assertTrue(all("NOT selected" in r["verification_needed"]
                            for r in gc03 if "approval-ready" in r["verification_needed"]))

    # 19. no implementation code started
    def test_no_implementation_started(self):
        for module in ("acquisition", "adaptation", "inference", "inspection", "monitoring", "quality", "uncertainty"):
            files = sorted(p.name for p in (ROOT / "src" / module).iterdir() if p.name != "__pycache__")
            self.assertEqual(files, ["README.md", "__init__.py"], module)
            self.assertLessEqual(len((ROOT / "src" / module / "__init__.py").read_text().splitlines()), 5, module)
        for folder in ("mobile", "experiments", "models", "backend"):
            files = sorted(p.name for p in (ROOT / folder).iterdir())
            self.assertEqual(files, ["README.md"], folder)
        self.assertEqual(self.sel["approval_ready"]["GC-03"]["experiment_status"], "planning_artifact_only")

    # 20. hypotheses untested
    def test_hypotheses_untested(self):
        hyps = self.sel["candidate_hypotheses"]["GC-03"]
        self.assertEqual([h.split(" ")[0] for h in hyps], ["H1", "H2", "H3", "H4", "H5"])
        for h in hyps:
            self.assertIn("CANDIDATE — NOT YET TESTED", h)
        section = self.approval.split("## 10. Candidate Hypotheses", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(section.count("CANDIDATE — NOT YET TESTED"), 6)  # header line + 5 rows

    # 21. contribution unvalidated
    def test_contribution_unvalidated(self):
        items = self.sel["contributions"]["GC-03"]["potential_contribution"]
        self.assertTrue(any(CONTRIBUTION in i["item"] for i in items))
        for i in items:
            self.assertEqual(i["label"], "requires_empirical_validation")
        section = self.approval.split("## 9. Candidate Contribution", 1)[1].split("\n## ", 1)[0]
        self.assertIn("**CANDIDATE CONTRIBUTION — REQUIRES EXPERIMENTAL VALIDATION**", section)
        self.assertIn(CONTRIBUTION, section)
        self.assertIn("not a confirmed contribution", section)

    # 22. dataset access/licensing not represented as verified
    def test_dataset_access_not_verified(self):
        for d in self.sel["datasets"]:
            self.assertIn(d["availability"], ("verification_required", "unknown"), d["name"])
        for d in self.closure["datasets"]:
            self.assertIn(d["access_licence"], ("verification_required", "unknown"), d["name"])
        statement = ("The reviewed dataset candidates appear technically suitable for visual-defect inspection "
                     "experiments, but access, licensing, smartphone suitability, and multi-view/recapture "
                     "suitability require dataset-specific verification.")
        self.assertEqual(self.sel["approval_ready"]["GC-03"]["dataset_statement"], statement)
        for text in (self.approval, self.selection_doc):
            self.assertIn(statement, " ".join(text.split()))
        lowered = self.approval.lower()
        for claim in ("all 13 datasets are available", "all 13 datasets are licensed",
                      "all 13 datasets are smartphone datasets"):
            self.assertNotIn(claim, lowered)

    def test_selection_document_status_section(self):
        self.assertIn("## GC-03 Evidence Closure Status", self.selection_doc)
        self.assertIn("Evidence closure is complete for GC-03, but final research-gap selection requires explicit "
                      "researcher approval.", self.selection_doc)
        self.assertIn("At this stage, GC-03 is the strongest approval-ready candidate based on the completed evidence "
                      "closure, but it has NOT been formally selected. Final selection requires explicit researcher "
                      "approval.", self.selection_doc)
        self.assertIn("It is not a ranking of merit", self.selection_doc)

    def test_reconciliation_preserves_both_branches(self):
        for rel in ("configs/gap_selection.yaml", "src/literature/gap_selection.py", "tests/test_gap_selection.py",
                    "research/gap_analysis/final_gap_selection.md", "research/gap_analysis/final_gap_selection_matrix.csv",
                    "configs/gc03_evidence_closure.yaml", "research/gap_analysis/gc03_evidence_closure.md",
                    "tests/test_gc03_evidence_closure.py"):
            self.assertTrue((ROOT / rel).exists(), rel)
        self.assertEqual(len(_rows(MATRIX)), 51)
        self.assertEqual(len(self.sel["datasets"]), 13)
        self.assertEqual(self.sel["candidate_ids"], ["GC-01", "GC-02", "GC-03"])


if __name__ == "__main__":
    unittest.main()
