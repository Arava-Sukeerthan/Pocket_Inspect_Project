"""
Tests for the Step 9.8 candidate-gap evaluation (src/literature/gap_evaluation.py,
configs/gap_evaluation.yaml and the research/gap_analysis/ evaluation artefacts).

The tests check the committed artefacts and verify that the validator rejects
planted violations (ranking columns, novelty language, Unknown converted to No,
missing evidence levels, missing search limitations, recoded corpus values).
"""
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from src.literature.gap_evaluation import (
    CORPUS_ID_PATTERN,
    EVALUATION_SECTIONS,
    SEARCH_LOG_REQUIRED_FIELDS,
    GapEvaluationValidator,
    code_adaptive_inference,
    code_confidence_gating,
    code_platform,
    code_resource_awareness,
    sha256_of,
)

ROOT = Path(__file__).resolve().parent.parent
EVAL_CONFIG = ROOT / "configs" / "gap_evaluation.yaml"
PAPERS_CSV = ROOT / "research" / "literature" / "papers.csv"
LITERATURE_DIR = ROOT / "research" / "literature"
GAP_DIR = ROOT / "research" / "gap_analysis"
FROZEN_SHA = "c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521"
CANDIDATES = ["GC-01", "GC-02", "GC-03"]
GC01_WORDING = ("Limited evidence of resource-driven runtime adaptation for visual inspection specifically on "
                "resource-constrained smartphones within the reviewed corpus.")
GC02_WORDING = ("Limited direct joint evaluation of energy and thermal behavior for resource-adaptive visual "
                "inspection on resource-constrained smartphones within the reviewed corpus.")
GC03_WORDING = ("Limited evidence of an integrated resource-aware smartphone visual-inspection system that combines "
                "runtime adaptation with confidence-aware downstream verification within the reviewed corpus.")
CONFIRMED_PARTIALS = {
    "arXiv:2603.16451": ["GC-02"],
    "PMC11435656": ["GC-01", "GC-03"],
    "doi:10.3390/s26154932": ["GC-03"],
    "arXiv:2608.14727": ["GC-01", "GC-03"],
}


def _validator():
    return GapEvaluationValidator.from_file(EVAL_CONFIG, project_root=ROOT)


class _Sandbox:
    """Copy the files the validator reads into a temporary project root."""

    FILES = [
        "configs/gap_evaluation.yaml",
        "research/literature/papers.csv",
        "research/gap_analysis/visual_inspection_scope.csv",
        "research/gap_analysis/counterexample_candidates.csv",
        "research/gap_analysis/targeted_search_log.md",
        "research/gap_analysis/candidate_gap_matrix.csv",
        "research/gap_analysis/candidate_gap_evaluation.md",
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
        return GapEvaluationValidator.from_file(self.root / "configs/gap_evaluation.yaml", project_root=self.root)

    def rewrite_csv(self, rel, mutate):
        path = self.root / rel
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fields, rows = reader.fieldnames, list(reader)
        fields, rows = mutate(list(fields), rows)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def edit_text(self, rel, old, new):
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        assert old in text, old
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


class TestCommittedEvaluation(unittest.TestCase):
    """The committed Step 9.8 artefacts satisfy every guard-rail."""

    def test_full_validation_passes(self):
        self.assertEqual(_validator().validate(), [])

    # 1. papers.csv is frozen
    def test_papers_csv_is_frozen(self):
        self.assertEqual(sha256_of(PAPERS_CSV), FROZEN_SHA)
        self.assertEqual(_validator().check_frozen_corpus(), [])
        config = yaml.safe_load(EVAL_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["frozen_corpus"]["sha256"], FROZEN_SHA)
        self.assertEqual(config["frozen_corpus"]["records"], 54)
        self.assertEqual(config["frozen_corpus"]["columns"], 31)

    # 2. candidate IDs are exactly GC-01, GC-02, GC-03
    def test_candidate_ids_are_exactly_gc01_to_gc03(self):
        v = _validator()
        self.assertEqual(v.candidate_ids, CANDIDATES)
        self.assertEqual(sorted({r["candidate_id"] for r in v.counterexamples()}), CANDIDATES)
        self.assertEqual(sorted({r["candidate_id"] for r in v.matrix()}), CANDIDATES)
        doc = v.path("evaluation").read_text(encoding="utf-8")
        for cid in CANDIDATES:
            self.assertIn(f"## {CANDIDATES.index(cid) + 4}. {cid} evaluation", doc)
        for gid in ("GC-04", "GC-05", "GC-06", "GC-07", "GC-08", "GC-09"):
            self.assertNotIn(gid, doc)

    # Narrowed wording (Step 9.8 methodology correction)
    def test_gc01_exact_narrowed_wording(self):
        self.assertEqual(_validator().config["candidates"]["GC-01"], GC01_WORDING)

    def test_gc02_exact_narrowed_wording(self):
        self.assertEqual(_validator().config["candidates"]["GC-02"], GC02_WORDING)

    def test_gc03_exact_narrowed_wording(self):
        self.assertEqual(_validator().config["candidates"]["GC-03"], GC03_WORDING)

    def test_narrowed_wording_used_in_outputs(self):
        v = _validator()
        for row in v.counterexamples():
            self.assertEqual(row["candidate_gap"], v.config["candidates"][row["candidate_id"]])
        doc = v.path("evaluation").read_text(encoding="utf-8")
        for wording in (GC01_WORDING, GC02_WORDING, GC03_WORDING):
            self.assertIn(f"**Candidate.** {wording}", doc)

    def test_step_9_7_wording_preserved_for_traceability(self):
        gap_config = yaml.safe_load((ROOT / "configs" / "gap_analysis.yaml").read_text(encoding="utf-8"))
        step97 = {c["id"]: c["title"] for c in gap_config["candidates"] if c["id"] in CANDIDATES}
        recorded = _validator().config["step_9_7_wording"]
        normalise = lambda text: text.replace("behavior", "behaviour")
        for cid in CANDIDATES:
            self.assertEqual(normalise(recorded[cid]), normalise(step97[cid]))

    # 3. no candidate is ranked
    def test_no_candidate_is_ranked(self):
        v = _validator()
        self.assertEqual(v.check_no_ranking(), [])
        for row in v.matrix():
            self.assertIn(row["assessment"], v.config["assessment_values"])
            self.assertIn(row["confidence"], v.config["confidence_values"])
        # every candidate is assessed on the same 14 criteria (no selective treatment)
        dims = [d["name"] for d in v.config["dimensions"]]
        self.assertEqual(len(dims), 14)
        for cid in CANDIDATES:
            self.assertEqual(sorted(r["criterion"] for r in v.matrix() if r["candidate_id"] == cid), sorted(dims))
        self.assertNotIn("rank", " ".join(v.config.keys()).lower())

    # 4. no final research gap exists outside the approval lifecycle: research_gap.md is
    # allowed only in a consistent researcher_approved state (Step 10A)
    def test_no_final_research_gap_exists(self):
        sel = yaml.safe_load((ROOT / "configs" / "gap_selection.yaml").read_text(encoding="utf-8"))
        approved = sel["selection"]["selection_status"] == "researcher_approved"
        self.assertEqual((GAP_DIR / "research_gap.md").exists(), approved)
        self.assertEqual(_validator().check_forbidden_files(), [])
        doc = (GAP_DIR / "candidate_gap_evaluation.md").read_text(encoding="utf-8")
        last = [ln.strip() for ln in doc.splitlines() if ln.strip()][-1]
        self.assertEqual(last, "Final research-gap selection remains a researcher decision and is outside Step 9.8.")

    # 5. Unknown is not converted to No
    def test_unknown_is_not_converted_to_no(self):
        v = _validator()
        corpus = v.corpus_records()
        scope = v.visual_scope()
        corpus_rows = [r for r in v.counterexamples() if CORPUS_ID_PATTERN.match(r["paper_id_or_external_id"])]
        self.assertTrue(corpus_rows)
        for row in corpus_rows:
            pid = row["paper_id_or_external_id"]
            for field in v.config["characteristic_fields"]:
                expected = scope[pid] if field == "visual_inspection" else corpus[pid][field]
                self.assertEqual(row[field], expected, f"{pid} {field} recoded")
                if expected == "Unknown":
                    self.assertNotEqual(row[field], "No")
        # P001 and P007 stay Unknown on the fields that keep them potential counterexamples
        p001 = next(r for r in corpus_rows if r["paper_id_or_external_id"] == "P001")
        self.assertEqual(p001["visual_inspection"], "Unknown")
        self.assertEqual(p001["counterexample_strength"], "potential")
        p007 = next(r for r in corpus_rows if r["paper_id_or_external_id"] == "P007")
        self.assertEqual((p007["energy_evaluation"], p007["thermal_evaluation"]), ("Unknown", "Unknown"))

    def test_snippet_level_rows_do_not_assert_no_without_basis(self):
        for row in _validator().counterexamples():
            if row["evidence_level"] in ("search_snippet_only", "unresolved"):
                for field in _validator().config["characteristic_fields"]:
                    if row[field] == "No":
                        self.assertIn(f"{field} No because", row["notes"])

    # 6. counterexample data does not modify papers.csv
    def test_counterexamples_are_not_added_to_papers_csv(self):
        v = _validator()
        self.assertEqual(v.externals_absent_from_corpus(), [])
        self.assertEqual(len(v.corpus_records()), 54)
        externals = v.external_rows()
        self.assertTrue(externals)
        corpus_ids = set(v.corpus_records())
        for row in externals:
            self.assertNotIn(row["paper_id_or_external_id"], corpus_ids)
            self.assertIn("not added to papers.csv", row["notes"])

    # 7. evaluation does not modify the canonical literature
    def test_validation_does_not_modify_canonical_literature(self):
        before = {p.name: (sha256_of(p), p.stat().st_mtime_ns) for p in LITERATURE_DIR.iterdir() if p.is_file()}
        _validator().validate()
        after = {p.name: (sha256_of(p), p.stat().st_mtime_ns) for p in LITERATURE_DIR.iterdir() if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(sha256_of(PAPERS_CSV), FROZEN_SHA)

    # 8. forbidden novelty language is rejected
    def test_committed_texts_have_no_forbidden_language(self):
        v = _validator()
        for key in ("evaluation", "search_log", "counterexamples", "matrix"):
            self.assertEqual(v.forbidden_language(v.path(key).read_text(encoding="utf-8")), [], key)

    def test_forbidden_language_detector(self):
        v = _validator()
        for sentence in (
            "There is no prior work on smartphone inspection.",
            "This is the first study of its kind.",
            "GC-03 is novel.",
            "We recommend GC-02 as the strongest candidate.",
            "The final research gap is GC-01.",
            "This has never been studied.",
            "GC-01 is the preferred candidate.",
            "This is the recommended gap.",
            "GC-03 is the final gap.",
            "PocketInspect would be the first system to do this.",
        ):
            self.assertTrue(v.forbidden_language(sentence), sentence)
        for sentence in (
            "No candidate is ranked.",
            "No final research gap is selected.",
            "No final gap is created.",
            "No complete match was found in the analyzed core corpus.",
        ):
            self.assertEqual(v.forbidden_language(sentence), [], sentence)

    # 9. candidate evidence includes an evidence level
    def test_every_evidence_row_has_an_evidence_level(self):
        v = _validator()
        for row in v.counterexamples():
            self.assertIn(row["evidence_level"], v.config["evidence_levels"])
            self.assertIn(row["counterexample_strength"], v.config["counterexample_strengths"])
        tokens = list(v.config["evidence_levels"]) + ["not_applicable"]
        for row in v.matrix():
            self.assertTrue(any(t in row["evidence_level"] for t in tokens), row["criterion"])

    # 10. targeted searches record limitations
    def test_targeted_searches_record_limitations(self):
        entries = _validator().search_entries()
        self.assertGreaterEqual(len(entries), 24)
        for sid, fields in entries.items():
            for name in SEARCH_LOG_REQUIRED_FIELDS:
                self.assertTrue(fields.get(name, "").strip(), f"{sid} lacks {name}")
            self.assertTrue(fields["Search limitations"].strip(), sid)
        candidates = {c for f in entries.values() for c in CANDIDATES if c in f["Candidate"]}
        self.assertEqual(sorted(candidates), CANDIDATES)

    def test_required_queries_were_logged(self):
        log = (GAP_DIR / "targeted_search_log.md").read_text(encoding="utf-8")
        for query in (
            "smartphone visual inspection confidence-aware",
            "mobile inspection confidence gating",
            "smartphone defect detection recapture",
            "mobile visual inspection additional view",
            "smartphone inspection adaptive inference confidence",
            "edge inspection confidence-triggered recapture",
            "mobile visual inspection uncertainty decision",
            "smartphone industrial inspection multi-view confidence",
        ):
            self.assertIn(f"`{query}`", log)

    def test_evaluation_has_required_sections_and_framework(self):
        v = _validator()
        self.assertEqual(v.check_evaluation(), [])
        self.assertEqual(len(EVALUATION_SECTIONS), 15)
        for dim in v.config["dimensions"]:
            for key in ("evidence_required", "strong_evidence", "weak_evidence", "disqualifying_or_weakening"):
                self.assertTrue(dim[key].strip(), f"{dim['id']} lacks {key}")


class TestValidatorRejectsViolations(unittest.TestCase):
    """Planted violations in a sandbox copy must be reported."""

    def test_rejects_modified_papers_csv(self):
        with _Sandbox() as sb:
            path = sb.root / "research/literature/papers.csv"
            path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            self.assertTrue(any("SHA-256" in e for e in sb.validator().check_frozen_corpus()))

    def test_rejects_ranking_column(self):
        with _Sandbox() as sb:
            sb.rewrite_csv("research/gap_analysis/candidate_gap_matrix.csv",
                           lambda f, rows: (f + ["rank"], [dict(r, rank="1") for r in rows]))
            self.assertTrue(any("rank" in e for e in sb.validator().check_no_ranking()))

    def test_rejects_numeric_assessment(self):
        with _Sandbox() as sb:
            sb.rewrite_csv("research/gap_analysis/candidate_gap_matrix.csv",
                           lambda f, rows: (f, [dict(rows[0], assessment="4")] + rows[1:]))
            v = sb.validator()
            self.assertTrue(v.check_matrix())
            self.assertTrue(v.check_no_ranking())

    def test_rejects_unknown_converted_to_no_for_corpus_record(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["paper_id_or_external_id"] == "P007":
                        r["energy_evaluation"] = "No"
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            errors = sb.validator().check_counterexamples()
            self.assertTrue(any("P007" in e and "energy_evaluation" in e for e in errors))

    def test_rejects_no_from_snippet_without_basis(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["evidence_level"] == "search_snippet_only":
                        r["thermal_evaluation"] = "No"
                        break
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            self.assertTrue(any("without a stated basis" in e for e in sb.validator().check_counterexamples()))

    def test_rejects_missing_evidence_level(self):
        with _Sandbox() as sb:
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv",
                           lambda f, rows: (f, [dict(rows[0], evidence_level="")] + rows[1:]))
            self.assertTrue(any("evidence_level" in e for e in sb.validator().check_counterexamples()))

    def test_rejects_extra_candidate(self):
        with _Sandbox() as sb:
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv",
                           lambda f, rows: (f, rows + [dict(rows[0], candidate_id="GC-04")]))
            self.assertTrue(any("GC-04" in e for e in sb.validator().check_counterexamples()))

    def test_rejects_missing_search_limitations(self):
        with _Sandbox() as sb:
            log = sb.root / "research/gap_analysis/targeted_search_log.md"
            lines = log.read_text(encoding="utf-8").splitlines()
            idx = next(i for i, ln in enumerate(lines) if ln.startswith("| Search limitations |"))
            lines[idx] = "| Search limitations |  |"
            log.write_text("\n".join(lines) + "\n", encoding="utf-8")
            self.assertTrue(any("Search limitations" in e for e in sb.validator().check_search_log()))

    def test_rejects_novelty_language_in_evaluation(self):
        with _Sandbox() as sb:
            sb.edit_text("research/gap_analysis/candidate_gap_evaluation.md",
                         "## 1. Purpose\n", "## 1. Purpose\n\nThis is the first work on GC-01.\n")
            self.assertTrue(any("forbidden" in e for e in sb.validator().check_evaluation()))

    def test_rejects_missing_closing_sentence(self):
        with _Sandbox() as sb:
            sb.edit_text("research/gap_analysis/candidate_gap_evaluation.md",
                         "Final research-gap selection remains a researcher decision and is outside Step 9.8.",
                         "GC-02 is selected.")
            self.assertTrue(any("closing sentence" in e for e in sb.validator().check_evaluation()))

    def test_rejects_research_gap_file(self):
        with _Sandbox() as sb:
            (sb.root / "research/gap_analysis/research_gap.md").write_text("# Gap\n", encoding="utf-8")
            self.assertTrue(sb.validator().check_forbidden_files())

    def test_rejects_external_paper_added_to_corpus(self):
        with _Sandbox() as sb:
            v = sb.validator()
            title = v.external_rows()[0]["title"]
            def mutate(fields, rows):
                rows.append(dict(rows[0], paper_id="P999", title=title))
                return fields, rows
            sb.rewrite_csv("research/literature/papers.csv", mutate)
            v = sb.validator()
            self.assertIn(title, v.externals_absent_from_corpus())
            self.assertTrue(v.check_frozen_corpus())


def _row(pid, cid):
    return next(r for r in _validator().counterexamples()
                if r["paper_id_or_external_id"] == pid and r["candidate_id"] == cid)


class TestOperationalDefinitions(unittest.TestCase):
    """Decisions A-C of the Step 9.8 controlled methodology correction."""

    # 1. content-driven cascade -> adaptive_inference Yes
    def test_content_driven_cascade_is_adaptive_inference(self):
        self.assertEqual(code_adaptive_inference(True), "Yes")
        for cid in ("GC-01", "GC-03"):
            self.assertEqual(_row("arXiv:2608.14727", cid)["adaptive_inference"], "Yes")

    # 2. content-driven cascade alone -> resource_awareness not automatically Yes
    def test_content_driven_cascade_is_not_automatically_resource_aware(self):
        self.assertEqual(code_resource_awareness(False), "No")
        self.assertEqual(code_resource_awareness(None), "Unknown")
        self.assertEqual(code_resource_awareness(True), "Yes")
        for cid in ("GC-01", "GC-02", "GC-03"):
            self.assertNotEqual(_row("arXiv:2608.14727", cid)["resource_awareness"], "Yes")
        # confidence-driven adaptation is never coded resource-aware Yes. Step 9.8 left it
        # Unknown (keyword scan); the Step 9.9B end-to-end read established confidence-only
        # routing, so it is now No, and only with a documented full-text basis.
        for cid in ("GC-01", "GC-03"):
            row = _row("PMC11435656", cid)
            self.assertEqual(row["adaptive_inference"], "Yes")
            self.assertEqual(row["resource_awareness"], "No")
            self.assertEqual(row["verification_status"], "verified_by_full_text_read")
            self.assertIn("Step 9.9B", row["notes"])
        defs = _validator().config["operational_definitions"]["A_content_driven_cascades"]
        self.assertIn("only when device/resource state", defs["resource_awareness"])

    # 3. learned view selection alone -> confidence_gating not automatically Yes
    def test_learned_view_selection_alone_is_not_confidence_gating(self):
        self.assertEqual(code_confidence_gating(True, False), "No")
        self.assertEqual(code_confidence_gating(True, None), "Unknown")
        self.assertEqual(code_confidence_gating(False, None), "No")
        self.assertNotEqual(_row("doi:10.3390/s26154932", "GC-03")["confidence_gating"], "Yes")
        self.assertEqual(_row("doi:10.3390/s26154932", "GC-03")["confidence_gating"], "Unknown")

    # 4. confidence-triggered view selection -> confidence_gating Yes
    def test_confidence_triggered_view_selection_is_confidence_gating(self):
        self.assertEqual(code_confidence_gating(True, True), "Yes")
        self.assertEqual(_row("PMC11435656", "GC-03")["confidence_gating"], "Yes")

    # 5. in-sensor processing -> edge Yes
    def test_in_sensor_processing_is_edge(self):
        self.assertEqual(code_platform("in_sensor")["edge_device"], "Yes")
        self.assertIn("edge_device Yes", _row("arXiv:2603.16451", "GC-02")["notes"])

    # 6. in-sensor processing -> smartphone No
    def test_in_sensor_processing_is_not_smartphone(self):
        self.assertEqual(code_platform("in_sensor")["smartphone"], "No")
        self.assertEqual(code_platform("smartphone")["smartphone"], "Yes")
        self.assertEqual(code_platform("unknown")["smartphone"], "Unknown")
        self.assertEqual(_row("arXiv:2603.16451", "GC-02")["smartphone"], "No")
        with self.assertRaises(ValueError):
            code_platform("phone_as_product")

    def test_decisions_documented_in_config_and_evaluation(self):
        v = _validator()
        self.assertEqual(sorted(v.config["operational_definitions"]),
                         ["A_content_driven_cascades", "B_learned_view_selection", "C_in_sensor_processors"])
        doc = v.path("evaluation").read_text(encoding="utf-8")
        for heading in ("Decision A: content-driven cascades", "Decision B: learned view-selection policies",
                        "Decision C: in-sensor processors"):
            self.assertIn(heading, doc)


class TestConfirmedPartialCounterexamples(unittest.TestCase):

    # 7. all four counterexamples remain partial
    def test_four_confirmed_counterexamples_remain_partial(self):
        v = _validator()
        self.assertEqual(sorted(v.config["confirmed_partial_counterexamples"]), sorted(CONFIRMED_PARTIALS))
        for pid, cids in CONFIRMED_PARTIALS.items():
            for cid in cids:
                self.assertEqual(_row(pid, cid)["counterexample_strength"], "partial", f"{pid} {cid}")
        self.assertFalse([r for r in v.counterexamples() if r["counterexample_strength"] == "full"])
        self.assertEqual(v.check_corrections(), [])

    def test_evidence_levels_not_upgraded(self):
        v = _validator()
        for pid, level in v.config["locked_evidence_levels"].items():
            rows = [r for r in v.counterexamples() if r["paper_id_or_external_id"] == pid]
            self.assertTrue(rows, pid)
            for r in rows:
                self.assertEqual(r["evidence_level"], level, pid)

    def test_tinyglass_established_fields(self):
        row = _row("arXiv:2603.16451", "GC-02")
        self.assertEqual((row["visual_inspection"], row["energy_evaluation"], row["thermal_evaluation"],
                          row["smartphone"]), ("Yes", "Yes", "No", "No"))

    def test_rejects_upgrade_to_full(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["paper_id_or_external_id"] == "arXiv:2603.16451":
                        r["counterexample_strength"] = "full"
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            self.assertTrue(any("must stay partial" in e for e in sb.validator().check_corrections()))

    def test_rejects_evidence_level_upgrade(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["paper_id_or_external_id"] == "Electronics 15(17):3915":
                        r["evidence_level"] = "verified_full_text"
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            self.assertTrue(any("locked" in e for e in sb.validator().check_corrections()))


class TestNarrowedClaimFalsificationCheck(unittest.TestCase):
    """Step 9.8 narrowed-claim falsification check (S28-S45)."""

    NEW_SEARCHES = [f"S{n}" for n in range(28, 46)]

    def test_eighteen_new_searches_logged_six_per_candidate(self):
        entries = _validator().search_entries()
        for sid in self.NEW_SEARCHES:
            self.assertIn(sid, entries)
            self.assertIn("narrowed wording", entries[sid]["Candidate"])
            self.assertTrue(entries[sid]["Search limitations"].strip())
            self.assertRegex(entries[sid]["Results returned"], r"^\d+")
        # Step 9.8 ended at S45; later entries (S46+) belong only to the Step 9.9B GC-03 closure
        for sid in entries:
            if int(sid[1:]) > 45:
                self.assertIn("Step 9.9B", entries[sid]["Candidate"], sid)
        for cid in CANDIDATES:
            n = sum(1 for sid in self.NEW_SEARCHES if cid in entries[sid]["Candidate"])
            self.assertEqual(n, 6, cid)

    def test_no_full_counterexample_statement(self):
        log = (GAP_DIR / "targeted_search_log.md").read_text(encoding="utf-8")
        doc = (GAP_DIR / "candidate_gap_evaluation.md").read_text(encoding="utf-8")
        statement = "No full counterexample was identified in this targeted falsification search."
        self.assertIn(statement, log)
        self.assertIn(statement, doc)
        for text in (log, doc):
            self.assertNotIn("no such work exists.", " ".join(text.lower().split()).replace(
                "does not establish that no such work exists.", ""))

    # full counterexample requires all criteria
    def test_full_counterexample_requires_all_criteria(self):
        v = _validator()
        self.assertEqual(v.check_full_criteria(), [])
        crit = v.config["full_counterexample_criteria"]
        self.assertEqual(sorted(crit), CANDIDATES)
        for cid in CANDIDATES:
            self.assertIn("smartphone", crit[cid])
            self.assertIn("visual_inspection", crit[cid])
            self.assertIn("resource_awareness", crit[cid])
            self.assertIn("adaptive_inference", crit[cid])
        self.assertIn("energy_evaluation", crit["GC-02"])
        self.assertIn("thermal_evaluation", crit["GC-02"])
        self.assertIn("confidence_gating", crit["GC-03"])
        base = {f: "Yes" for f in v.config["characteristic_fields"]}
        for cid in CANDIDATES:
            self.assertTrue(v.meets_full_criteria(dict(base, candidate_id=cid)))
            for field in crit[cid]:
                for value in ("No", "Unknown"):
                    self.assertFalse(v.meets_full_criteria(dict(base, candidate_id=cid, **{field: value})))

    def test_new_hits_classified_with_verified_evidence(self):
        expected = {
            ("arXiv:2509.17136", "GC-01"): "partial",
            ("arXiv:2509.17136", "GC-02"): "partial",
            ("arXiv:2509.17136", "GC-03"): "partial",
            ("arXiv:2603.26603", "GC-02"): "partial",
            ("arXiv:2608.08589", "GC-03"): "partial",
            ("arXiv:2010.06291", "GC-02"): "not_counterexample",
            ("arXiv:2606.24173", "GC-03"): "not_counterexample",
        }
        for (pid, cid), strength in expected.items():
            row = _row(pid, cid)
            self.assertEqual(row["counterexample_strength"], strength, pid)
            self.assertEqual(row["evidence_level"], "verified_full_text", pid)
        # SAEC: adaptation is content/confidence-driven, not resource-driven (Decision A)
        self.assertEqual(_row("arXiv:2509.17136", "GC-01")["resource_awareness"], "No")
        # smartphone energy + temperature paper is outside the visual-inspection scope
        row = _row("arXiv:2603.26603", "GC-02")
        self.assertEqual((row["smartphone"], row["visual_inspection"], row["energy_evaluation"],
                          row["thermal_evaluation"]), ("Yes", "No", "Yes", "Yes"))
        self.assertFalse(_validator().meets_full_criteria(row))
        # title-level hits are not upgraded
        for pid in ("arXiv:2010.10754", "arXiv:2303.11291"):
            self.assertEqual(_row(pid, "GC-01")["evidence_level"], "search_snippet_only")

    def test_no_row_classified_full(self):
        self.assertFalse([r for r in _validator().counterexamples() if r["counterexample_strength"] == "full"])

    def test_rejects_full_without_all_criteria(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["paper_id_or_external_id"] == "arXiv:2509.17136" and r["candidate_id"] == "GC-03":
                        r["counterexample_strength"] = "full"
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            self.assertTrue(any("does not meet every criterion" in e for e in sb.validator().check_full_criteria()))

    def test_rejects_row_meeting_all_criteria_not_marked_full(self):
        with _Sandbox() as sb:
            def mutate(fields, rows):
                for r in rows:
                    if r["paper_id_or_external_id"] == "arXiv:2509.17136" and r["candidate_id"] == "GC-01":
                        r["smartphone"] = "Yes"
                        r["resource_awareness"] = "Yes"
                return fields, rows
            sb.rewrite_csv("research/gap_analysis/counterexample_candidates.csv", mutate)
            self.assertTrue(any("meets every criterion" in e for e in sb.validator().check_full_criteria()))


if __name__ == "__main__":
    unittest.main()
