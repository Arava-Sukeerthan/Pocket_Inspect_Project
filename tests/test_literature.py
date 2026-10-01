"""
Unit tests for PocketInspect literature management, validator, analyzer, and exporter.
"""
import unittest
import tempfile
from pathlib import Path
from src.literature import (
    PAPERS_SCHEMA_HEADERS,
    BOOLEAN_FIELDS,
    parse_boolean_field,
    normalize_title,
    normalize_doi,
    LiteratureValidator,
    LiteratureAnalyzer,
    MatrixExporter
)


class TestLiteratureSchemaAndUtils(unittest.TestCase):

    def test_schema_headers_count(self):
        self.assertEqual(len(PAPERS_SCHEMA_HEADERS), 29)
        self.assertIn("paper_id", PAPERS_SCHEMA_HEADERS)
        self.assertIn("adaptive_inference", PAPERS_SCHEMA_HEADERS)
        self.assertIn("thermal_evaluation", PAPERS_SCHEMA_HEADERS)

    def test_boolean_parsing(self):
        self.assertTrue(parse_boolean_field("true"))
        self.assertTrue(parse_boolean_field("1"))
        self.assertTrue(parse_boolean_field("YES"))

        self.assertFalse(parse_boolean_field("false"))
        self.assertFalse(parse_boolean_field("0"))
        self.assertFalse(parse_boolean_field("NO"))

        self.assertIsNone(parse_boolean_field(""))
        self.assertIsNone(parse_boolean_field("unknown"))
        self.assertIsNone(parse_boolean_field("N/A"))

    def test_normalize_title(self):
        t1 = "Adaptive Inference on Mobile Edge Devices!"
        t2 = "adaptive inference on mobile edge devices"
        self.assertEqual(normalize_title(t1), normalize_title(t2))

    def test_normalize_doi(self):
        d1 = "https://doi.org/10.1109/TPAMI.2023.1234567"
        d2 = "10.1109/tpami.2023.1234567"
        self.assertEqual(normalize_doi(d1), normalize_doi(d2))


class TestLiteratureValidator(unittest.TestCase):

    def setUp(self):
        self.validator = LiteratureValidator()

    def test_valid_records(self):
        records = [
            {
                "paper_id": "P001",
                "title": "Edge Inspection on Smartphones",
                "authors": "Smith et al.",
                "year": "2023",
                "doi": "10.1000/182",
                "smartphone": "true",
                "adaptive_inference": "true"
            }
        ]
        report = self.validator.validate_records(records)
        self.assertTrue(report["is_valid"])
        self.assertEqual(len(report["schema_errors"]), 0)
        self.assertEqual(len(report["duplicates"]), 0)

    def test_duplicate_doi_detection(self):
        records = [
            {
                "paper_id": "P001",
                "title": "Title One",
                "authors": "Author A",
                "year": "2022",
                "doi": "https://doi.org/10.1000/123"
            },
            {
                "paper_id": "P002",
                "title": "Title Two",
                "authors": "Author B",
                "year": "2023",
                "doi": "10.1000/123"
            }
        ]
        report = self.validator.validate_records(records)
        self.assertTrue(report["is_valid"])
        self.assertEqual(len(report["duplicates"]), 1)
        self.assertEqual(report["duplicates"][0]["type"], "DOI match")

    def test_duplicate_title_detection(self):
        records = [
            {
                "paper_id": "P001",
                "title": "Resource-Aware Edge Vision",
                "authors": "Author A",
                "year": "2022"
            },
            {
                "paper_id": "P002",
                "title": "resource aware edge vision!",
                "authors": "Author B",
                "year": "2023"
            }
        ]
        report = self.validator.validate_records(records)
        self.assertTrue(report["is_valid"])
        self.assertEqual(len(report["duplicates"]), 1)
        self.assertEqual(report["duplicates"][0]["type"], "Title match")

    def test_invalid_year_error(self):
        records = [
            {
                "paper_id": "P001",
                "title": "Title One",
                "authors": "Author A",
                "year": "INVALID_YEAR"
            }
        ]
        report = self.validator.validate_records(records)
        self.assertFalse(report["is_valid"])
        self.assertIn("invalid year value", report["schema_errors"][0])


class TestLiteratureAnalyzer(unittest.TestCase):

    def setUp(self):
        self.sample_records = [
            {
                "paper_id": "P001",
                "title": "Smart Inspection",
                "authors": "Alice et al.",
                "year": "2023",
                "domain": "3D-Print Inspection",
                "smartphone": "true",
                "edge_device": "true",
                "on_device": "true",
                "adaptive_inference": "true",
                "thermal_evaluation": "true",
                "resource_awareness": "true"
            },
            {
                "paper_id": "P002",
                "title": "Cloud Vision Defect Detection",
                "authors": "Bob et al.",
                "year": "2021",
                "domain": "Industrial Visual Inspection",
                "smartphone": "false",
                "edge_device": "false",
                "cloud": "true",
                "adaptive_inference": "false",
                "thermal_evaluation": "false"
            }
        ]
        self.analyzer = LiteratureAnalyzer(self.sample_records)

    def test_filter_papers(self):
        filtered = self.analyzer.filter_papers(boolean_criteria={"smartphone": True})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["paper_id"], "P001")

    def test_summary_stats(self):
        stats = self.analyzer.generate_summary_stats()
        self.assertEqual(stats["total_papers"], 2)
        self.assertEqual(stats["boolean_characteristics"]["smartphone"]["true_count"], 1)
        self.assertEqual(stats["boolean_characteristics"]["smartphone"]["false_count"], 1)

    def test_gap_matrix_generation(self):
        gap_rows = self.analyzer.generate_gap_matrix_rows()
        self.assertGreater(len(gap_rows), 0)
        # Check GAP-001 support count (P001 has smartphone=true, adaptive=true, thermal=true)
        gap_1 = [g for g in gap_rows if g["gap_id"] == "GAP-001"][0]
        self.assertEqual(gap_1["literature_support_count"], "1")
        self.assertEqual(gap_1["supporting_paper_ids"], "P001")

    def test_exporter_markdown_and_latex(self):
        matrix_rows = self.analyzer.generate_literature_matrix_rows()
        md = MatrixExporter.export_literature_markdown(matrix_rows)
        tex = MatrixExporter.export_literature_latex(matrix_rows)
        self.assertIn("| P001 |", md)
        self.assertIn("\\begin{table*}", tex)


if __name__ == "__main__":
    unittest.main()
