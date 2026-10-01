"""
Integrity tests for the committed literature database (research/literature/papers.csv).
"""
import csv
import re
import unittest
from pathlib import Path
from src.literature import BOOLEAN_FIELDS, LiteratureValidator

PAPERS_CSV = Path(__file__).resolve().parent.parent / "research" / "literature" / "papers.csv"
ALLOWED_CHARACTERISTIC_VALUES = {"Yes", "No", "Unknown"}
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")


class TestCommittedPapersCsv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(PAPERS_CSV, encoding="utf-8-sig", newline="") as f:
            cls.records = list(csv.DictReader(f))

    def test_schema_valid_without_duplicates_or_warnings(self):
        report = LiteratureValidator().validate_file(PAPERS_CSV)
        self.assertTrue(report["is_valid"], report["schema_errors"])
        self.assertEqual(report["duplicates"], [])
        self.assertEqual(report["warnings"], [])

    def test_paper_ids_sequential(self):
        ids = [r["paper_id"] for r in self.records]
        self.assertEqual(ids, [f"P{i:03d}" for i in range(1, len(ids) + 1)])

    def test_characteristic_fields_use_yes_no_unknown(self):
        for r in self.records:
            for field in BOOLEAN_FIELDS:
                self.assertIn(r[field], ALLOWED_CHARACTERISTIC_VALUES, f"{r['paper_id']}.{field}")

    def test_every_paper_has_source_link_and_evidence(self):
        for r in self.records:
            self.assertTrue(r["doi"] or r["url"], r["paper_id"])
            if r["doi"]:
                self.assertRegex(r["doi"], DOI_PATTERN)
                self.assertEqual(r["url"], f"https://doi.org/{r['doi']}")
            self.assertTrue(r["url"].startswith("https://"), r["paper_id"])
            self.assertTrue(r["evidence"].startswith("[Verified"), r["paper_id"])

    def test_no_unsupported_novelty_language_in_extracted_fields(self):
        # Paper titles are excluded: they are the authors' own wording.
        banned = re.compile(r"\b(novel|first|unique|unprecedented)\b", re.IGNORECASE)
        for r in self.records:
            for field in ("domain", "application", "notes"):
                self.assertIsNone(banned.search(r[field]), f"{r['paper_id']}.{field}: {r[field]}")


if __name__ == "__main__":
    unittest.main()
