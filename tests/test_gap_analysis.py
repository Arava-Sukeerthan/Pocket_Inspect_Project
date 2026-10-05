"""
Tests for the configuration-driven combination gap analysis (src/literature/gap_analysis.py),
the committed gap-analysis configuration (configs/gap_analysis.yaml) and the analysis-only
visual-inspection classification (research/gap_analysis/visual_inspection_scope.csv).
"""
import csv
import tempfile
import unittest
from pathlib import Path
from src.literature.gap_evaluation import lifecycle_errors

import yaml

from src.literature import BOOLEAN_FIELDS, CombinationGapAnalyzer
from src.literature.gap_analysis import (
    CATEGORY_LABELS,
    COMBINATION_MATRIX_FIELDS,
    GAP_MATRIX_FIELDS,
    LIMITATION_CAUSES,
    SCOPE_STATEMENT,
    load_classification_file,
)

ROOT = Path(__file__).resolve().parent.parent
PAPERS_CSV = ROOT / "research" / "literature" / "papers.csv"
GAP_CONFIG = ROOT / "configs" / "gap_analysis.yaml"
GAP_DIR = ROOT / "research" / "gap_analysis"
VIS_CSV = GAP_DIR / "visual_inspection_scope.csv"
RANKING_WORDS = ("score", "rank", "ranking", "priority", "weight")


def _record(pid, **values):
    rec = {"paper_id": pid, "evidence": "", "accuracy_metrics": ""}
    for field in BOOLEAN_FIELDS:
        rec[field] = values.get(field, "Unknown")
    return rec


def _committed():
    return CombinationGapAnalyzer.from_files(PAPERS_CSV, GAP_CONFIG, project_root=ROOT)


class TestCombinationGapAnalyzer(unittest.TestCase):
    """Synthetic records: three-valued logic, populations and scope."""

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
                "visual_inspection_scope": {"values": {"P1": "Yes", "P2": "Unknown", "P3": "No",
                                                       "P4": "Yes", "P5": "No", "P6": "Yes"}},
            },
            "combinations": [
                {"id": "C-1", "label": "phone + on-device", "criteria": [["smartphone"], ["on_device"]]},
                {"id": "C-2", "label": "phone + VI", "criteria": [["smartphone"], ["visual_inspection_scope"]],
                 "scope_excludes_no": ["visual_inspection_scope"]},
                {"id": "C-3", "label": "phone + (edge or on-device)",
                 "criteria": [["smartphone"], ["edge_device", "on_device"]]},
            ],
            "candidates": [
                {"id": "GC-X", "category": "candidate_gap", "title": "t", "primary_combination": "C-1"},
                {"id": "EL-X", "category": "evidence_limitation", "title": "u",
                 "limitation_causes": ["missing_schema_field"]},
            ],
        }
        self.analyzer = CombinationGapAnalyzer(self.records, self.config, "abc")

    def _row(self, cid):
        return [r for r in self.analyzer.combination_matrix_rows() if r["combination_id"] == cid][0]

    def test_core_subset_excludes_peripheral_and_reviews(self):
        ids = [r["paper_id"] for r in self.analyzer.primary_core_records()]
        self.assertEqual(ids, ["P1", "P2", "P3", "P6"])

    def test_unknown_is_unresolved_not_no(self):
        row = self._row("C-1")
        self.assertEqual(row["all_yes_ids"], "P1")
        self.assertEqual(row["unresolved_ids"], "P2; P6")
        self.assertEqual(row["excluded_by_no_ids"], "P3[smartphone=No]")
        self.assertEqual(row["peripheral_results"], "P4=Yes")

    def test_review_no_values_are_not_evidence_of_absence(self):
        # P5 is coded No for everything but must not appear among excluded-by-No records.
        for row in self.analyzer.combination_matrix_rows():
            self.assertNotIn("P5", row["excluded_by_no_ids"])
            self.assertNotIn("P5", row["unresolved_ids"])
            self.assertEqual(row["review_record_ids"], "P5")

    def test_visual_scope_no_is_out_of_scope_unknown_stays(self):
        row = self._row("C-2")
        self.assertEqual(row["records_in_scope"], "3")      # P1, P2, P6; P3 coded No is out of scope
        self.assertEqual(row["all_yes_ids"], "P1; P6")
        self.assertEqual(row["unresolved_ids"], "P2")       # visual scope Unknown stays in scope
        self.assertEqual(row["excluded_by_no_count"], "0")

    def test_or_group_unknown_not_no(self):
        # P6: edge_device No, on_device Unknown -> group Unknown (not No)
        row = self._row("C-3")
        self.assertEqual(row["all_yes_ids"], "P1")
        self.assertIn("P6", row["unresolved_ids"])

    def test_near_miss_reports_missing_criterion(self):
        self.assertIn("P2[on_device=Unknown]", self._row("C-1")["near_miss"])
        self.assertIn("P3[smartphone=No]", self._row("C-1")["near_miss"])

    def test_candidate_rows_are_pending_and_categorised(self):
        rows = self.analyzer.candidate_rows()
        self.assertEqual([r["category"] for r in rows], [CATEGORY_LABELS["candidate_gap"],
                                                          CATEGORY_LABELS["evidence_limitation"]])
        self.assertEqual(rows[0]["yes_count"], "1")
        self.assertEqual(rows[0]["unknown_count"], "2")
        self.assertEqual(rows[1]["yes_count"], "n/a")
        for r in rows:
            self.assertEqual(r["researcher_review_status"], "Pending researcher review")

    def test_ranking_key_rejected(self):
        bad = dict(self.config, candidates=[{"id": "GC-X", "category": "candidate_gap", "title": "t",
                                             "primary_combination": "C-1", "rank": 1}])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_camera_input_classified_yes_is_counted(self):
        # A Yes visual-inspection value (camera/image input) puts the record in scope and can satisfy it.
        row = self._row("C-2")
        self.assertIn("P1", row["all_yes_ids"])

    def test_limitation_without_cause_rejected(self):
        bad = dict(self.config, candidates=[{"id": "EL-X", "category": "evidence_limitation", "title": "u"}])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_unknown_limitation_cause_rejected(self):
        bad = dict(self.config, candidates=[{"id": "EL-X", "category": "evidence_limitation", "title": "u",
                                             "limitation_causes": ["absence_of_work"]}])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_invalid_category_rejected(self):
        bad = dict(self.config, candidates=[{"id": "GC-X", "category": "final_gap", "title": "t"}])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_unknown_criterion_field_rejected(self):
        bad = dict(self.config, combinations=[{"id": "X", "label": "x", "criteria": [["accuracy_metrics"]]}],
                   candidates=[])
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, bad)

    def test_invalid_visual_scope_value_rejected(self):
        cfg = dict(self.config)
        cfg["derived_attributes"] = {"visual_inspection_scope": {"values": {
            "P1": "Maybe", "P2": "Yes", "P3": "No", "P4": "No", "P5": "No", "P6": "No"}}}
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, cfg)

    def test_missing_visual_scope_record_rejected(self):
        cfg = dict(self.config)
        cfg["derived_attributes"] = {"visual_inspection_scope": {"values": {"P1": "Yes"}}}
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, cfg)

    def test_overlapping_populations_rejected(self):
        cfg = dict(self.config, populations={"peripheral_contextual": {"paper_ids": ["P4"]},
                                             "review_records": {"paper_ids": ["P4"]}})
        with self.assertRaises(ValueError):
            CombinationGapAnalyzer(self.records, cfg)

    def test_freeze_mismatch_warning(self):
        cfg = dict(self.config, corpus_freeze={"papers_sha256": "different"})
        md = CombinationGapAnalyzer(self.records, cfg, "abc").generate_gap_candidates_markdown()
        self.assertIn("WARNING: corpus changed since the freeze", md)
        md_ok = CombinationGapAnalyzer(self.records, dict(self.config, corpus_freeze={"papers_sha256": "abc"}),
                                       "abc").generate_gap_candidates_markdown()
        self.assertNotIn("WARNING", md_ok)
        self.assertIn("No final research gap was selected, ranked, or approved.", md_ok)


class TestVisualInspectionScope(unittest.TestCase):
    """The committed analysis-only classification file."""

    @classmethod
    def setUpClass(cls):
        cls.rows = load_classification_file(VIS_CSV, "visual_inspection_scope")
        with open(PAPERS_CSV, encoding="utf-8-sig", newline="") as f:
            cls.ids = [r["paper_id"] for r in csv.DictReader(f)]
        with open(GAP_CONFIG, encoding="utf-8") as f:
            cls.config = yaml.safe_load(f)

    def test_covers_every_record_exactly_once(self):
        self.assertEqual(sorted(self.rows), sorted(self.ids))

    def test_values_and_basis(self):
        for pid, row in self.rows.items():
            self.assertIn(row["visual_inspection_scope"], ("Yes", "No", "Unknown"), pid)
            self.assertTrue(row["basis"].strip(), pid)
            self.assertTrue(row["basis_category"].strip(), pid)
            self.assertIn(row["evidence_level"], ("full text", "abstract"), pid)

    def test_population_column_matches_config(self):
        pops = self.config["populations"]
        for pid, row in self.rows.items():
            if pid in pops["peripheral_contextual"]["paper_ids"]:
                expected = "peripheral/contextual"
            elif pid in pops["review_records"]["paper_ids"]:
                expected = "review/survey"
            else:
                expected = "core"
            self.assertEqual(row["analysis_population"], expected, pid)

    def test_core_distribution(self):
        core = [r["visual_inspection_scope"] for r in self.rows.values() if r["analysis_population"] == "core"]
        self.assertEqual(len(core), 46)
        self.assertEqual((core.count("Yes"), core.count("No"), core.count("Unknown")), (20, 19, 7))

    def test_non_optical_modalities_are_no(self):
        # Approved definition: point clouds, magnetic flux leakage and ultrasonic sensing are No, not Unknown.
        for pid in ("P021", "P040", "P048", "P051"):
            self.assertEqual(self.rows[pid]["visual_inspection_scope"], "No", pid)
            self.assertEqual(self.rows[pid]["basis_category"], "non-optical inspection input", pid)

    def test_camera_image_video_input_is_yes(self):
        # Full-text records whose actual inspection input is camera images or video frames.
        for pid in ("P011", "P015", "P016", "P020"):
            self.assertEqual(self.rows[pid]["visual_inspection_scope"], "Yes", pid)
            self.assertEqual(self.rows[pid]["evidence_level"], "full text", pid)

    def test_training_only_images_do_not_make_yes(self):
        # P002: dashcam video only labels training data; the deployed input is an accelerometer.
        self.assertEqual(self.rows["P002"]["visual_inspection_scope"], "No")
        self.assertIn("training", self.rows["P002"]["basis"])
        self.assertIn("accelerometer", self.rows["P002"]["basis"])

    def test_definition_is_researcher_approved(self):
        vis = self.config["derived_attributes"]["visual_inspection_scope"]
        self.assertIn("researcher-approved", vis["status"])
        self.assertIn("optical image/video/camera", vis["approved_definition"])

    def test_non_visual_peripheral_records(self):
        self.assertEqual(self.rows["P002"]["visual_inspection_scope"], "No")
        self.assertEqual(self.rows["P013"]["visual_inspection_scope"], "No")

    def test_yes_requires_explicit_visual_basis(self):
        for pid, row in self.rows.items():
            if row["visual_inspection_scope"] == "Yes" and row["analysis_population"] == "core":
                self.assertEqual(row["basis_category"], "explicit optical image/video/camera input", pid)


class TestCommittedGapAnalysis(unittest.TestCase):
    """The committed configuration evaluated against the frozen corpus."""

    @classmethod
    def setUpClass(cls):
        cls.analyzer = _committed()
        with open(GAP_CONFIG, encoding="utf-8") as f:
            cls.config = yaml.safe_load(f)
        cls.candidates = cls.analyzer.candidate_rows()
        cls.combos = {r["combination_id"]: r for r in cls.analyzer.combination_matrix_rows()}

    def test_core_subset_rule(self):
        core = [r["paper_id"] for r in self.analyzer.primary_core_records()]
        excluded = set(self.config["populations"]["peripheral_contextual"]["paper_ids"]) | \
            set(self.config["populations"]["review_records"]["paper_ids"])
        self.assertEqual(len(self.analyzer.records), 54)
        self.assertEqual(len(core), 54 - len(excluded))
        self.assertEqual(len(core), 46)
        self.assertFalse(set(core) & excluded)

    def test_peripheral_records_excluded_from_core_evidence(self):
        self.assertEqual(self.config["populations"]["peripheral_contextual"]["paper_ids"], ["P002", "P013"])
        for row in self.candidates:
            for field in ("supporting_papers", "counterexamples"):
                self.assertNotIn("P002", row[field])
                self.assertNotIn("P013", row[field])

    def test_review_records_not_evidence_of_absence(self):
        reviews = self.config["populations"]["review_records"]["paper_ids"]
        for row in self.combos.values():
            for pid in reviews:
                self.assertNotIn(pid, row["excluded_by_no_ids"])
                self.assertNotIn(pid, row["unresolved_ids"])

    def test_unknown_is_not_counted_as_no(self):
        # 38 of 46 core records are Unknown for confidence gating: they must be unresolved, not No.
        cov = {c["field"]: c for c in self.analyzer.characteristic_coverage()}
        self.assertEqual(len(cov["confidence_gating"]["unknown"]), 38)
        row = self.combos["C-H"]
        self.assertEqual(row["unresolved_count"], "38")
        # A record may be excluded by a *different* criterion coded No (e.g. P015: multi_view = No),
        # but an Unknown confidence_gating value must never be the reason for exclusion.
        reasons = {e.split("[", 1)[0]: e for e in row["excluded_by_no_ids"].split("; ")}
        for pid in cov["confidence_gating"]["unknown"]:
            if pid in reasons:
                self.assertNotIn("confidence_gating", reasons[pid], pid)

    def test_p013_unresolved_metrics_not_a_gap_signal(self):
        free_text = {"accuracy_metrics", "efficiency_metrics", "limitations", "future_work"}
        for combo in self.config["combinations"]:
            fields = {f for g in combo["criteria"] for f in g}
            self.assertFalse(fields & free_text, combo["id"])
        p013 = [r for r in self.analyzer.records if r["paper_id"] == "P013"][0]
        self.assertEqual(p013["accuracy_metrics"].strip(), "")
        for row in self.combos.values():
            self.assertNotIn("P013", row["excluded_by_no_ids"])
            self.assertNotIn("P013", row["unresolved_ids"])

    def test_candidates_separated_and_pending(self):
        cats = {r["category"] for r in self.candidates}
        self.assertEqual(cats, set(CATEGORY_LABELS.values()))
        gaps = [c["id"] for c in self.config["candidates"] if c["category"] == "candidate_gap"]
        self.assertEqual(gaps, ["GC-01", "GC-02", "GC-03"])
        for r in self.candidates:
            self.assertEqual(r["researcher_review_status"], "Pending researcher review")

    def test_candidates_not_promoted_to_final_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.analyzer.write_gap_matrix_csv(Path(tmp) / "gap_matrix.csv")
            self.analyzer.write_combination_matrix_csv(Path(tmp) / "combination_matrix.csv")
            self.analyzer.write_gap_candidates_markdown(Path(tmp) / "gap_candidates.md")
            self.assertFalse((Path(tmp) / "research_gap.md").exists())
            md = (Path(tmp) / "gap_candidates.md").read_text(encoding="utf-8").lower()
        # the generator never writes research_gap.md; the committed file is governed by the
        # approval lifecycle (Step 10A) and may exist only in a consistent approved state
        self.assertEqual(lifecycle_errors(GAP_DIR.parent.parent), [])
        for phrase in ("the research gap is", "selected gap", "final gap:", "recommended gap"):
            self.assertNotIn(phrase, md)

    def test_every_candidate_is_corpus_bounded(self):
        md = self.analyzer.generate_gap_candidates_markdown()
        self.assertEqual(md.count(f"| Scope | {SCOPE_STATEMENT} |"), len(self.config["candidates"]))
        for row in self.candidates:
            self.assertIn(SCOPE_STATEMENT, row["description"])
        lowered = md.lower()
        for phrase in ("novel", "the first", "no previous work", "no existing research", "nobody has"):
            self.assertNotIn(phrase, lowered)

    def test_evidence_limitations_name_their_causes(self):
        for cand in self.config["candidates"]:
            if cand["category"] == "evidence_limitation":
                self.assertTrue(cand["limitation_causes"], cand["id"])
                self.assertTrue(set(cand["limitation_causes"]) <= set(LIMITATION_CAUSES), cand["id"])

    def test_no_numerical_ranking(self):
        for name in GAP_MATRIX_FIELDS + COMBINATION_MATRIX_FIELDS:
            for word in RANKING_WORDS:
                self.assertNotIn(word, name.lower())
        for cand in self.config["candidates"]:
            for key in cand:
                self.assertNotIn(key.lower(), RANKING_WORDS + ("final", "selected"))

    def test_committed_outputs_match_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, writer in (("gap_matrix.csv", self.analyzer.write_gap_matrix_csv),
                                 ("combination_matrix.csv", self.analyzer.write_combination_matrix_csv),
                                 ("gap_candidates.md", self.analyzer.write_gap_candidates_markdown)):
                writer(Path(tmp) / name)
                self.assertEqual((Path(tmp) / name).read_text(encoding="utf-8"),
                                 (GAP_DIR / name).read_text(encoding="utf-8"), name)

    def test_freeze_hash_matches_corpus(self):
        self.assertEqual(self.config["corpus_freeze"]["papers_sha256"], self.analyzer.corpus_sha256)


if __name__ == "__main__":
    unittest.main()
