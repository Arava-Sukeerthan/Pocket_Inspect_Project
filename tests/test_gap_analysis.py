"""
Tests for the configuration-driven combination gap analysis (src/literature/gap_analysis.py)
and for the committed gap-analysis configuration (configs/gap_analysis.yaml).
"""
import csv
import unittest
from pathlib import Path

import yaml

from src.literature import BOOLEAN_FIELDS, CombinationGapAnalyzer

ROOT = Path(__file__).resolve().parent.parent
PAPERS_CSV = ROOT / "research" / "literature" / "papers.csv"
GAP_CONFIG = ROOT / "configs" / "gap_analysis.yaml"


def _record(pid, **values):
    rec = {"paper_id": pid, "evidence": "", "accuracy_metrics": ""}
    for field in BOOLEAN_FIELDS:
        rec[field] = values.get(field, "Unknown")
    return rec


class TestCombinationGapAnalyzer(unittest.TestCase):

    def setUp(self):
        self.records = [
            _record("P1", smartphone="Yes", on_device="Yes", uncertainty="Yes"),
            _record("P2", smartphone="Yes", on_device="Unknown"),
            _record("P3", smartphone="No", on_device="Yes"),
            _record("P4", smartphone="Yes", on_device="Yes", uncertainty="Yes"),  # peripheral
            _record("P5", smartphone="No", on_device="No"),                       # review
            _record("P6", smartphone="Yes", edge_device="No", on_device="Unknown"),
        ]
        self.config = {
            "populations": {
                "peripheral_contextual": {"paper_ids": ["P4"]},
                "review_records": {"paper_ids": ["P5"]},
            },
            "derived_attributes": {
                "visual_inspection": {"yes_ids": ["P1", "P2"], "no_ids": ["P3"]},
            },
            "combinations": [
                {"id": "C-1", "label": "phone + on-device", "criteria": [["smartphone"], ["on_device"]]},
                {"id": "C-2", "label": "phone + VI", "criteria": [["smartphone"], ["visual_inspection"]]},
                {"id": "C-3", "label": "phone + (edge or on-device)",
                 "criteria": [["smartphone"], ["edge_device", "on_device"]]},
            ],
        }
        self.analyzer = CombinationGapAnalyzer(self.records, self.config, "abc")

    def _row(self, cid):
        return [r for r in self.analyzer.gap_matrix_rows() if r["combination_id"] == cid][0]

    def test_populations_exclude_peripheral_and_reviews(self):
        ids = [r["paper_id"] for r in self.analyzer.primary_core_records()]
        self.assertEqual(ids, ["P1", "P2", "P3", "P6"])

    def test_unknown_is_unresolved_not_no(self):
        row = self._row("C-1")
        self.assertEqual(row["all_yes_ids"], "P1")
        self.assertEqual(row["unresolved_ids"], "P2; P6")
        self.assertEqual(row["excluded_by_no_count"], "1")  # P3 only
        self.assertEqual(row["review_record_ids"], "P5")
        self.assertEqual(row["peripheral_results"], "P4=Yes")

    def test_derived_attribute_unassigned_is_unknown(self):
        row = self._row("C-2")
        self.assertEqual(row["all_yes_ids"], "P1; P2")
        self.assertEqual(row["unresolved_ids"], "P6")
        self.assertEqual(self.analyzer.unassigned_derived()["visual_inspection"], ["P4", "P5", "P6"])

    def test_or_group(self):
        # P6: edge_device No, on_device Unknown -> group Unknown (not No)
        row = self._row("C-3")
        self.assertEqual(row["all_yes_ids"], "P1")
        self.assertIn("P6", row["unresolved_ids"])

    def test_near_miss_reports_missing_criterion(self):
        self.assertIn("P2[on_device=Unknown]", self._row("C-1")["near_miss"])
        self.assertIn("P3[smartphone=No]", self._row("C-1")["near_miss"])

    def test_observation_and_status_are_descriptive(self):
        for row in self.analyzer.gap_matrix_rows():
            self.assertEqual(row["review_status"], "Pending researcher review")
            self.assertNotIn("score", row["coverage_observation"].lower())
            self.assertNotIn("rank", row["coverage_observation"].lower())

    def test_unknown_criterion_field_rejected(self):
        bad = dict(self.config, combinations=[{"id": "X", "label": "x", "criteria": [["no_such_field"]]}])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_freeze_mismatch_warning(self):
        cfg = dict(self.config, corpus_freeze={"papers_sha256": "different"})
        md = CombinationGapAnalyzer(self.records, cfg, "abc").generate_gap_candidates_markdown()
        self.assertIn("WARNING: corpus changed since the freeze", md)
        md_ok = CombinationGapAnalyzer(self.records, dict(self.config, corpus_freeze={"papers_sha256": "abc"}),
                                       "abc").generate_gap_candidates_markdown()
        self.assertNotIn("WARNING", md_ok)
        self.assertIn("No final research gap was selected or approved.", md_ok)


class TestCommittedGapConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(GAP_CONFIG, encoding="utf-8") as f:
            cls.config = yaml.safe_load(f)
        with open(PAPERS_CSV, encoding="utf-8-sig", newline="") as f:
            cls.ids = {r["paper_id"] for r in csv.DictReader(f)}

    def test_config_loads_against_committed_corpus(self):
        analyzer = CombinationGapAnalyzer.from_files(PAPERS_CSV, GAP_CONFIG)
        self.assertEqual(len(analyzer.gap_matrix_rows()), len(self.config["combinations"]))

    def test_config_paper_ids_exist(self):
        pops = self.config["populations"]
        referenced = set(pops["peripheral_contextual"]["paper_ids"]) | set(pops["review_records"]["paper_ids"])
        for attr in self.config["derived_attributes"].values():
            referenced |= set(attr["yes_ids"]) | set(attr["no_ids"])
        self.assertEqual(referenced - self.ids, set())

    def test_approved_peripheral_records(self):
        self.assertEqual(self.config["populations"]["peripheral_contextual"]["paper_ids"], ["P002", "P013"])

    def test_candidates_are_pending_and_unranked(self):
        for cand in self.config["candidate_gaps"]:
            for key in ("score", "rank", "priority", "final"):
                self.assertNotIn(key, cand)


if __name__ == "__main__":
    unittest.main()
