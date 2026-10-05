"""
Tests for the Step 9.9 Phase A research-gap selection framework
(src/literature/gap_selection.py, configs/gap_selection.yaml and the
research/gap_analysis/final_gap_selection* artefacts).

Phase A must not rank, score or select a candidate; the tests check the
committed artefacts and that planted violations are rejected.
"""
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from src.literature.gap_evaluation import sha256_of
from src.literature.gap_selection import DOCUMENT_SECTIONS, GapSelectionValidator

ROOT = Path(__file__).resolve().parent.parent
SEL_CONFIG = ROOT / "configs" / "gap_selection.yaml"
GAP_DIR = ROOT / "research" / "gap_analysis"
PAPERS_CSV = ROOT / "research" / "literature" / "papers.csv"
FROZEN_SHA = "c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521"
CANDIDATES = ["GC-01", "GC-02", "GC-03"]
APPROVED = {
    "GC-01": ("Limited evidence of resource-driven runtime adaptation for visual inspection specifically on "
              "resource-constrained smartphones within the reviewed corpus."),
    "GC-02": ("Limited direct joint evaluation of energy and thermal behavior for resource-adaptive visual "
              "inspection on resource-constrained smartphones within the reviewed corpus."),
    "GC-03": ("Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines "
              "runtime adaptation with confidence-aware downstream verification within the reviewed corpus."),
}


def _v():
    return GapSelectionValidator.from_file(SEL_CONFIG, project_root=ROOT)


class _Sandbox:
    FILES = [
        "configs/gap_selection.yaml",
        "configs/gap_evaluation.yaml",
        "research/literature/papers.csv",
        "research/gap_analysis/final_gap_selection_matrix.csv",
        "research/gap_analysis/final_gap_selection.md",
    ]

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel in self.FILES:
            dst = self.root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        return self

    def __exit__(self, *exc):
        self.tmp.cleanup()

    def validator(self):
        return GapSelectionValidator.from_file(self.root / "configs/gap_selection.yaml", project_root=self.root)

    def edit_config(self, mutate):
        path = self.root / "configs/gap_selection.yaml"
        cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
        mutate(cfg)
        path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def edit_doc(self, old, new):
        path = self.root / "research/gap_analysis/final_gap_selection.md"
        text = path.read_text(encoding="utf-8")
        assert old in text, old
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def rewrite_matrix(self, mutate):
        path = self.root / "research/gap_analysis/final_gap_selection_matrix.csv"
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fields, rows = list(reader.fieldnames), list(reader)
        fields, rows = mutate(fields, rows)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)


class TestCommittedSelectionFramework(unittest.TestCase):

    def test_full_validation_passes(self):
        self.assertEqual(_v().validate(), [])

    # 1. exactly three candidates
    def test_exactly_three_candidates(self):
        v = _v()
        self.assertEqual(v.config["candidate_ids"], CANDIDATES)
        self.assertEqual(sorted({r["candidate_id"] for r in v.matrix()}), CANDIDATES)
        self.assertEqual(len(v.matrix()), 3 * 17)
        for gid in ("GC-04", "GC-05", "EL-01"):
            self.assertNotIn(gid, v.document())

    # 2. wording matches approved Step 9.8 wording
    def test_wording_matches_step_9_8(self):
        v = _v()
        self.assertEqual(v.approved_wording(), APPROVED)
        for cid, text in APPROVED.items():
            self.assertIn(f"**Candidate (Step 9.8 wording).** {text}", v.document())

    # 3. no numerical rank; 4. no weighted score
    def test_no_rank_or_weighted_score(self):
        v = _v()
        self.assertEqual(v.check_no_ranking(), [])
        for key in ("score", "scores", "rank", "ranking", "weights", "weight", "winner", "priority"):
            self.assertNotIn(key, v.config)
        for row in v.matrix():
            self.assertIn(row["assessment"], v.config["assessment_values"])
            self.assertIn(row["confidence"], v.config["confidence_values"])
        self.assertIn("Listed in ID order; no ordering of merit is implied.", v.document())

    # 5. no winner/selection; 14. selection gate researcher-controlled
    def test_no_selection_and_gate_is_researcher_controlled(self):
        v = _v()
        sel = v.config["selection"]
        self.assertIsNone(sel["selected_candidate"])
        self.assertIsNone(sel["approved_by"])
        self.assertFalse(sel["research_gap_file_created"])
        for cid in CANDIDATES:
            self.assertFalse(v.can_select(cid))
        self.assertEqual(v.check_gate(), [])
        doc = v.document()
        self.assertTrue(doc.rstrip().endswith(
            "Step 9.9 Phase A is complete. Final research-gap selection requires explicit researcher approval "
            "and is not automatically performed by this workflow."))
        self.assertEqual(v.forbidden_language(doc), [])

    def test_gate_documents_why_no_selection(self):
        v = _v()
        for cid in CANDIDATES:
            gate = v.config["selection_gate"][cid]
            self.assertEqual(len(gate), 10)
            statuses = [s for s, _ in gate.values()]
            self.assertNotEqual(set(statuses), {"satisfied"}, cid)
        self.assertIn("not** grounds for eliminating any candidate", v.document())

    # 6. research_gap.md does not exist
    def test_research_gap_md_absent(self):
        self.assertFalse((GAP_DIR / "research_gap.md").exists())
        self.assertEqual(_v().check_selection_state(), [])

    # 7. papers.csv frozen
    def test_papers_csv_frozen(self):
        self.assertEqual(sha256_of(PAPERS_CSV), FROZEN_SHA)
        self.assertEqual(_v().check_frozen_corpus(), [])

    # 8. candidate RQs measurable; 9. not presented as final
    def test_rqs_measurable_and_candidate_only(self):
        v = _v()
        self.assertEqual(v.check_research_questions(), [])
        self.assertIn("not final", v.config["rq_status"].lower())
        for cid in CANDIDATES:
            rqs = v.config["candidate_research_questions"][cid]
            self.assertEqual(len(rqs), 3)
            for rq in rqs:
                self.assertTrue(rq["measurable_outcomes"])
                self.assertTrue(rq["falsified_if"].strip())
                self.assertTrue(rq["id"].startswith(cid + "-RQ"))
        self.assertIn("Final PocketInspect RQs are not set in Phase A.", v.document())

    # 10. Unknown evidence explicit
    def test_unknowns_explicit(self):
        v = _v()
        for row in v.matrix():
            self.assertTrue(row["unknowns"].strip(), row["criterion"])
        for cid in CANDIDATES:
            b = next(r for r in v.matrix() if r["candidate_id"] == cid and r["criterion"].startswith("B."))
            if cid == "GC-03":
                # Step 9.9C: Q2 closed by the Step 9.9B evidence closure (conditionally acceptable)
                self.assertEqual(b["assessment"], "mixed")
                self.assertEqual(v.config["selection_gate"][cid]["Q2"][0], "partially_satisfied")
                for name in ("P001", "AIVD", "Choi 2026"):
                    self.assertIn(name, b["unknowns"])
            else:
                self.assertEqual(b["assessment"], "weakens")
                self.assertEqual(v.config["selection_gate"][cid]["Q2"][0], "unresolved")

    # 11. counterexamples correctly represented
    def test_counterexamples_represented(self):
        v = _v()
        self.assertEqual(v.check_counterexamples(), [])
        for row in v.matrix():
            self.assertNotRegex(row["counterexamples"].lower(), r"(?<!no )full counterexample")
        doc = v.document()
        for name in ("TinyGLASS", "PMC11435656", "ActiveInspect", "2608.14727", "SAEC", "RobustDefect-LLM",
                     "2603.26603"):
            self.assertIn(name, doc)

    # 12. dataset uncertainty not converted to availability
    def test_dataset_uncertainty_not_converted(self):
        v = _v()
        self.assertEqual(v.check_datasets(), [])
        self.assertNotIn("available", v.config["dataset_availability_values"])
        for d in v.config["datasets"]:
            self.assertIn(d["availability"], ("verification_required", "unknown"))
        self.assertIn("Access, licence and download were **not** verified in this step.", v.document())

    # 13. existing components not labelled novel
    def test_existing_components_not_novel(self):
        v = _v()
        self.assertEqual(v.check_contributions(), [])
        for cid in CANDIDATES:
            for e in v.config["contributions"][cid]["existing_components"]:
                self.assertEqual(e["label"], "demonstrated_in_literature")
        self.assertIn("Integration of known components is not automatically a novel contribution.", v.document())

    def test_document_structure(self):
        v = _v()
        self.assertEqual(v.check_document(), [])
        self.assertEqual(len(DOCUMENT_SECTIONS), 16)
        self.assertEqual(len(v.config["criteria"]), 17)


class TestSelectionViolationsRejected(unittest.TestCase):

    def test_rejects_selected_candidate(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c["selection"].update(selected_candidate="GC-01"))
            self.assertTrue(sb.validator().check_selection_state())

    def test_can_select_requires_approval_and_satisfied_gate(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c["selection"].update(selected_candidate="GC-01"))
            self.assertFalse(sb.validator().can_select("GC-01"))  # no approver
            sb.edit_config(lambda c: c["selection"].update(approved_by="researcher"))
            self.assertFalse(sb.validator().can_select("GC-01"))  # gate not satisfied

    def test_rejects_research_gap_file(self):
        with _Sandbox() as sb:
            (sb.root / "research/gap_analysis/research_gap.md").write_text("# gap\n", encoding="utf-8")
            self.assertTrue(sb.validator().check_selection_state())

    def test_rejects_score_column(self):
        with _Sandbox() as sb:
            sb.rewrite_matrix(lambda f, rows: (f + ["score"], [dict(r, score="3") for r in rows]))
            sb.edit_config(lambda c: c.update(matrix_fields=c["matrix_fields"] + ["score"]))
            self.assertTrue(any("score" in e for e in sb.validator().check_no_ranking()))

    def test_rejects_numeric_assessment(self):
        with _Sandbox() as sb:
            sb.rewrite_matrix(lambda f, rows: (f, [dict(rows[0], assessment="4")] + rows[1:]))
            self.assertTrue(sb.validator().check_matrix())

    def test_rejects_winner_language(self):
        with _Sandbox() as sb:
            sb.edit_doc("## 1. Purpose\n", "## 1. Purpose\n\nGC-01 is the winner.\n")
            self.assertTrue(any("winner" in e for e in sb.validator().check_document()))

    def test_rejects_novelty_language(self):
        v = _v()
        for sentence in ("This is the first smartphone inspection system.", "GC-03 is novel.",
                         "There is no prior work on this.", "GC-02 is the selected gap."):
            self.assertTrue(v.forbidden_language(sentence), sentence)

    def test_rejects_rq_without_falsification(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c["candidate_research_questions"]["GC-02"][0].update(falsified_if=""))
            self.assertTrue(sb.validator().check_research_questions())

    def test_rejects_final_rq_status(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c.update(rq_status="Final research question"))
            self.assertTrue(sb.validator().check_research_questions())

    def test_rejects_dataset_marked_available(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c["datasets"][0].update(availability="available"))
            self.assertTrue(sb.validator().check_datasets())

    def test_rejects_existing_component_labelled_novel(self):
        with _Sandbox() as sb:
            sb.edit_config(lambda c: c["contributions"]["GC-03"]["existing_components"][0].update(label="novel"))
            self.assertTrue(sb.validator().check_contributions())

    def test_rejects_wording_change(self):
        with _Sandbox() as sb:
            sb.edit_doc(APPROVED["GC-02"], "Energy evaluation is missing.")
            self.assertTrue(sb.validator().check_candidates())

    def test_rejects_missing_unknowns(self):
        with _Sandbox() as sb:
            sb.rewrite_matrix(lambda f, rows: (f, [dict(rows[1], unknowns="")] + rows[:1] + rows[2:]))
            self.assertTrue(any("unknowns" in e for e in sb.validator().check_matrix()))

    def test_rejects_dropped_counterexample(self):
        with _Sandbox() as sb:
            def mutate(f, rows):
                for r in rows:
                    if r["candidate_id"] == "GC-02" and r["criterion"].startswith("C."):
                        r["counterexamples"] = r["counterexamples"].replace("TinyGLASS (arXiv 2603.16451), ", "")
                        r["weakening_evidence"] = r["weakening_evidence"].replace("TinyGLASS", "an edge paper")
                        r["supporting_evidence"] = r["supporting_evidence"].replace("2603.16451", "")
                return f, rows
            sb.rewrite_matrix(mutate)
            self.assertTrue(any("2603.16451" in e for e in sb.validator().check_counterexamples()))


if __name__ == "__main__":
    unittest.main()
