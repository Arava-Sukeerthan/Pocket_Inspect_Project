"""
Step 9.9B tests: GC-03 evidence closure.

Checks the frozen corpus, the exact GC-03 wording, the full-counterexample rule,
Unknown handling, the P001/P007 and full-text-review status, the explicit Q2/Q8/Q10
answers, dataset availability, and that no gap is selected, ranked or finalised.
"""
import csv
import hashlib
import re
import unittest
from pathlib import Path

import yaml

from src.literature.gap_evaluation import GapEvaluationValidator

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "research" / "literature" / "papers.csv"
GAP_DIR = ROOT / "research" / "gap_analysis"
DOC = GAP_DIR / "gc03_evidence_closure.md"
CSV_PATH = GAP_DIR / "counterexample_candidates.csv"
CLOSURE_CFG = ROOT / "configs" / "gc03_evidence_closure.yaml"
EVAL_CFG = ROOT / "configs" / "gap_evaluation.yaml"

REQUIRED_SECTIONS = [
    "Purpose", "GC-03 exact wording", "Five full-counterexample criteria", "P001 verification",
    "P007 verification", "PMC11435656 full-text verification", "ActiveInspect full-text verification",
    "Additional high-value papers", "Indexed-database search", "Counterexample assessment",
    "Q2 — Unknown burden", "Q8 — Contribution distinctiveness", "Q10 — Literature overturn risk",
    "Dataset feasibility", "Minimum viable experiment", "Remaining limitations", "Decision readiness",
]
CLOSING = ("GC-03 has been evaluated for evidence closure. This document does not select GC-03 as the "
           "final research gap. Final selection remains a researcher decision.")
CHARACTERISTICS = ["smartphone", "visual_inspection", "resource_awareness", "adaptive_inference",
                   "energy_evaluation", "thermal_evaluation", "confidence_gating", "multi_view"]


def _load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _rows():
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _row(pid, cid="GC-03"):
    match = [r for r in _rows() if r["paper_id_or_external_id"] == pid and r["candidate_id"] == cid]
    assert len(match) == 1, (pid, cid, len(match))
    return match[0]


class TestGC03EvidenceClosure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cfg = _load(CLOSURE_CFG)
        cls.eval_cfg = _load(EVAL_CFG)
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.validator = GapEvaluationValidator.from_file(EVAL_CFG, ROOT)

    # 1. papers.csv remains frozen
    def test_papers_csv_frozen(self):
        frozen = self.cfg["frozen_corpus"]
        self.assertEqual(hashlib.sha256(PAPERS.read_bytes()).hexdigest(), frozen["sha256"])
        with open(PAPERS, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(len(rows[0]), frozen["columns"])
        self.assertEqual(len(rows) - 1, frozen["records"])
        ids = [r[0] for r in rows[1:]]
        self.assertEqual(len(ids), len(set(ids)))

    # 2. GC-03 wording remains exact
    def test_gc03_wording_exact(self):
        wording = self.eval_cfg["candidates"]["GC-03"]
        self.assertEqual(self.cfg["candidate_wording"], wording)
        self.assertIn(wording, self.doc)
        for r in _rows():
            if r["candidate_id"] == "GC-03":
                self.assertEqual(r["candidate_gap"], wording)

    # 3. full counterexample requires all five criteria
    def test_full_requires_all_five(self):
        criteria = ["smartphone", "visual_inspection", "resource_awareness", "adaptive_inference", "confidence_gating"]
        self.assertEqual(self.cfg["full_counterexample_criteria"], criteria)
        self.assertEqual(self.eval_cfg["full_counterexample_criteria"]["GC-03"], criteria)
        probe = dict(_row("PMC11435656"))
        for missing in criteria:
            row = dict(probe, **{c: "Yes" for c in criteria})
            row[missing] = "Unknown"
            self.assertFalse(self.validator.meets_full_criteria(row), missing)
        self.assertTrue(self.validator.meets_full_criteria(dict(probe, **{c: "Yes" for c in criteria})))
        self.assertFalse(any(r["counterexample_strength"] == "full" for r in _rows() if r["candidate_id"] == "GC-03"))
        self.assertEqual(self.validator.check_full_criteria(), [])

    # 4. Unknown never becomes No
    def test_unknown_never_becomes_no(self):
        # snippet/unresolved rows may only carry No with a stated basis (Step 9.8 rule)
        self.assertEqual(self.validator.check_counterexamples(), [])
        # ActiveInspect confidence_gating stays Unknown (definitional decision pending)
        self.assertEqual(_row("doi:10.3390/s26154932")["confidence_gating"], "Unknown")
        # P001 fields that are Unknown in the corpus stay Unknown
        p001 = _row("P001")
        for field in ("visual_inspection", "resource_awareness", "adaptive_inference", "confidence_gating"):
            self.assertEqual(p001[field], "Unknown", field)
        # every No introduced in Step 9.9B on a previously Unknown field is backed by a full-text read
        for pid in ("PMC11435656", "doi:10.3390/s26154932"):
            row = _row(pid)
            self.assertEqual(row["resource_awareness"], "No")
            self.assertEqual(row["evidence_level"], "verified_full_text")
            self.assertIn("Step 9.9B", row["notes"])

    # 5. P001/P007 unresolved status preserved when full text is unavailable
    def test_p001_p007_unresolved(self):
        for pid in ("P001", "P007"):
            spec = self.cfg["priority_papers"][pid]
            self.assertFalse(spec["full_text_accessed"])
            self.assertEqual(spec["evidence_level"], "abstract_only")
            self.assertEqual(spec["status"], "unresolved")
            row = _row(pid)
            self.assertEqual(row["evidence_level"], "abstract_only")
            self.assertEqual(row["verification_status"], "corpus_record_reproduced")
        self.assertEqual(_row("P001")["counterexample_strength"], "potential")
        self.assertEqual(_row("P007")["counterexample_strength"], "partial")
        self.assertEqual(self.validator.check_corrections(), [])

    # 6. PMC11435656 and ActiveInspect based on full-text review
    def test_full_text_review(self):
        for key, pid in (("PMC11435656", "PMC11435656"), ("ActiveInspect", "doi:10.3390/s26154932")):
            spec = self.cfg["priority_papers"][key]
            self.assertTrue(spec["full_text_accessed"])
            self.assertEqual(spec["review_mode"], "full_text_read_end_to_end")
            row = _row(pid)
            self.assertEqual(row["verification_status"], "verified_by_full_text_read")
            self.assertEqual(row["evidence_level"], "verified_full_text")
            self.assertEqual(row["counterexample_strength"], "partial")
            for q in ("smartphone", "visual_inspection", "resource_awareness", "adaptive_inference", "confidence_gating"):
                self.assertIn(q, spec["findings"])

    # 7-9. Q2, Q8, Q10 explicitly answered
    def test_gate_questions_answered(self):
        answers = self.cfg["gate_answers"]
        for q, heading in (("Q2", "## 11. Q2"), ("Q8", "## 12. Q8"), ("Q10", "## 13. Q10")):
            self.assertIn(answers[q]["result"], answers[q]["allowed"], q)
            self.assertNotEqual(answers[q]["result"], "unresolved")
            section = self.doc.split(heading, 1)[1].split("\n## ", 1)[0]
            self.assertIn(f"**Result: `{answers[q]['result']}`", section, q)

    # 10, 13. no final research gap; research_gap.md does not exist
    def test_no_research_gap_file(self):
        self.assertFalse((GAP_DIR / "research_gap.md").exists())
        self.assertFalse(self.cfg["selection"]["research_gap_file_created"])
        self.assertTrue(self.doc.rstrip().endswith(CLOSING))

    # 11. no ranking; 12. no candidate selection
    def test_no_ranking_or_selection(self):
        self.assertIsNone(self.cfg["selection"]["selected_candidate"])
        forbidden_keys = {"score", "rank", "ranking", "priority", "weight", "winner", "selected"}

        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    self.assertNotIn(str(k).lower(), forbidden_keys)
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(self.cfg)
        self.assertNotIn("score", ",".join(self.eval_cfg["counterexample_fields"]))

    # 14. dataset availability cannot be silently assumed
    def test_dataset_availability_not_assumed(self):
        allowed = set(self.cfg["dataset_availability_values"])
        self.assertEqual(allowed, {"verification_required", "unknown"})
        self.assertEqual(len(self.cfg["datasets"]), 13)
        for d in self.cfg["datasets"]:
            self.assertIn(d["access_licence"], allowed, d["name"])
        self.assertNotRegex(self.doc.lower(), r"\b(freely available|publicly available under|licen[cs]ed under)\b")

    # 15. no unsupported novelty language
    def test_no_novelty_language(self):
        text = self.doc.lower().replace(CLOSING.lower(), "")
        for phrase in self.eval_cfg["guards"]["forbidden_phrases"] + ["novel", "best candidate", "we recommend"]:
            self.assertNotIn(phrase, text, phrase)
        self.assertNotRegex(text, r"\bno (such|other) (work|study|system) exists\b")

    def test_document_structure(self):
        headings = re.findall(r"^## (\d+)\. (.+)$", self.doc, flags=re.MULTILINE)
        self.assertEqual([h[1] for h in headings], REQUIRED_SECTIONS)
        self.assertEqual([int(h[0]) for h in headings], list(range(1, 18)))

    def test_searches_logged_and_capped(self):
        ids = self.cfg["searches"]["ids"]
        self.assertLessEqual(len(ids), 12)
        entries = self.validator.search_entries()
        for sid in ids:
            self.assertIn(sid, entries)
            self.assertIn("GC-03", entries[sid]["Candidate"])
        self.assertEqual(self.validator.check_search_log(), [])

    def test_baselines_and_overturn_candidates_documented(self):
        self.assertEqual(sorted(self.cfg["candidate_baselines"]), ["B1", "B2", "B3", "B4", "B5"])
        for pid in self.cfg["overturn_candidates"]:
            self.assertTrue(any(r["paper_id_or_external_id"] == pid and r["candidate_id"] == "GC-03" for r in _rows()), pid)

    def test_external_rows_not_in_corpus(self):
        self.assertEqual(self.validator.externals_absent_from_corpus(), [])
        self.assertEqual(self.validator.validate(), [])


if __name__ == "__main__":
    unittest.main()
