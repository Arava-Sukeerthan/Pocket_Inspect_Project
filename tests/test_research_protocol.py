"""
Step 10A tests: formal research specification for the approved gap GC-03.

Checks the official research_gap.md, the research questions, objectives,
hypotheses, variables, resource states, configuration ladder, verification
actions, baselines, contribution status and traceability matrix, and that
Step 10A created no implementation, datasets or results.
"""
import csv
import re
import subprocess
import unittest
from pathlib import Path

import yaml

from src.literature.gap_evaluation import lifecycle_errors

ROOT = Path(__file__).resolve().parent.parent
GAP_DOC = ROOT / "research" / "gap_analysis" / "research_gap.md"
RQ_DIR = ROOT / "research" / "research_questions"
RQ_DOC = RQ_DIR / "research_questions.md"
OBJ_DOC = RQ_DIR / "objectives.md"
HYP_DOC = RQ_DIR / "hypotheses.md"
VAR_DOC = RQ_DIR / "variables_and_factors.md"
FRAME_DOC = RQ_DIR / "experimental_framework.md"
MATRIX = RQ_DIR / "traceability_matrix.csv"
CFG = ROOT / "configs" / "research_protocol.yaml"

APPROVED_GAP = (
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
GAP_SECTIONS = [
    "Research Gap", "Literature Boundary", "Primary Research Question", "Scope", "Research Motivation",
    "Candidate Contribution", "Known Limitations", "Approval Status", "Traceability to Steps 9.7–9.9C",
]
RQS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5", "RQ6"]
OBJECTIVES = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"]
HYPOTHESES = ["H1", "H2", "H3", "H4", "H5"]
HYP_ELEMENTS = [
    "Null hypothesis", "Alternative", "Independent variable(s)", "Dependent variable(s)", "Expected direction",
    "Falsification condition", "Statistical comparison", "Practical significance",
]
MATRIX_COLUMNS = [
    "ID", "Type", "Statement", "Related_Gap", "Related_RQ", "Related_Objective", "Related_Hypothesis",
    "Independent_Variables", "Dependent_Variables", "Evaluation_Method", "Falsification_Condition", "Status",
]
# Quantities with units, percentages or numeric threshold assignments would be invented numbers.
NUMERIC_THRESHOLD = re.compile(
    r"\d+(\.\d+)?\s*(%|°\s*C|\bms\b|\bmW\b|\bW\b|\bmAh\b|\bfps\b|\bFPS\b|\bMB\b|\bGB\b|\bseconds?\b|\bminutes?\b)"
    r"|(threshold|alpha|α|SESOI|ECE|recall|precision|F1|mAP|accuracy)\s*(=|<|>|≤|≥|of)\s*\d"
    r"|\b0\.\d+\b|\bp\s*[<=]\s*\d"
)
RESULT_CLAIMS = re.compile(
    r"\b(results? (show|showed|indicate|demonstrate)|we (found|observed|measured)|was (confirmed|proven)"
    r"|is (proven|confirmed|supported)|hypothes[ie]s (is|are|was|were) (proven|confirmed|supported)"
    r"|achiev(ed|es) an? |improved by|outperform(ed|s) )",
    re.IGNORECASE,
)


def _text(path):
    return path.read_text(encoding="utf-8")


def _section(text, heading):
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def _split(cell):
    return [x.strip() for x in cell.split(";") if x.strip()]


def _matrix():
    with open(MATRIX, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class TestResearchProtocol(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gap = _text(GAP_DOC)
        cls.rq = _text(RQ_DOC)
        cls.obj = _text(OBJ_DOC)
        cls.hyp = _text(HYP_DOC)
        cls.var = _text(VAR_DOC)
        cls.frame = _text(FRAME_DOC)
        with open(CFG, encoding="utf-8") as f:
            cls.cfg = yaml.safe_load(f)
        cls.rows = _matrix()
        cls.by_id = {r["ID"]: r for r in cls.rows}
        cls.docs = {"gap": cls.gap, "rq": cls.rq, "obj": cls.obj, "hyp": cls.hyp, "var": cls.var,
                    "frame": cls.frame}

    # 1. research_gap.md exists with the required sections
    def test_research_gap_exists(self):
        self.assertTrue(GAP_DOC.exists())
        titles = re.findall(r"^## (\d+)\. (.+)$", self.gap, flags=re.MULTILINE)
        self.assertEqual([t for _, t in titles], GAP_SECTIONS)
        self.assertEqual([int(n) for n, _ in titles], list(range(1, 10)))

    # 2. GC-03 wording matches the approved wording; approval recorded; corpus-bounded
    def test_gap_wording_and_approval(self):
        self.assertIn(f"> {APPROVED_GAP}", self.gap)
        self.assertEqual(self.cfg["approved_gap"]["wording"], APPROVED_GAP)
        self.assertEqual(self.cfg["approved_gap"]["id"], "GC-03")
        self.assertEqual(self.cfg["approved_gap"]["approval_status"], "researcher_approved")
        sel = yaml.safe_load((ROOT / "configs" / "gap_selection.yaml").read_text(encoding="utf-8"))
        self.assertEqual(sel["selection"]["selection_status"], "researcher_approved")
        self.assertEqual(sel["selection"]["selected_candidate"], "GC-03")
        self.assertEqual(sel["approval_ready"]["GC-03"]["candidate_gap"], APPROVED_GAP)
        for key in ("approved_by", "approval_date", "approval_statement"):
            self.assertEqual(self.cfg["approved_gap"][key], sel["selection"][key], key)
        self.assertEqual(lifecycle_errors(ROOT), [])
        section1 = _section(self.gap, "## 1. Research Gap")
        self.assertEqual([ln[2:] for ln in section1.splitlines() if ln.startswith("> ")], [APPROVED_GAP])
        self.assertIn("**APPROVED — GC-03 is the approved PocketInspect research gap.**",
                      _section(self.gap, "## 8. Approval Status"))
        self.assertTrue(APPROVED_GAP.startswith("Within the reviewed literature corpus"))
        self.assertEqual(self.by_id["GC-03"]["Statement"], APPROVED_GAP)

    # 3. RQ1 matches the approved primary RQ
    def test_primary_rq(self):
        self.assertEqual(self.cfg["primary_rq"], PRIMARY_RQ)
        self.assertIn(f"> **RQ1.** {PRIMARY_RQ}", self.rq)
        self.assertIn(f"> **RQ1.** {PRIMARY_RQ}", self.gap)
        self.assertEqual(self.by_id["RQ1"]["Statement"], PRIMARY_RQ)
        for rq in RQS[1:]:
            self.assertRegex(self.rq, rf"\| {rq} \| [^|]+\? \|")

    # 4-5. RQ <-> objective coverage (documents and matrix agree)
    def test_rq_objective_mapping(self):
        rq_to_obj = {rq: set(_split(self.by_id[rq]["Related_Objective"])) for rq in RQS}
        obj_to_rq = {o: set(_split(self.by_id[o]["Related_RQ"])) for o in OBJECTIVES}
        for rq, objs in rq_to_obj.items():
            self.assertTrue(objs, rq)
            self.assertTrue(objs <= set(OBJECTIVES), rq)
            for o in objs:
                self.assertIn(rq, obj_to_rq[o], (rq, o))
        for o, rqs in obj_to_rq.items():
            self.assertTrue(rqs, o)
            self.assertTrue(rqs <= set(RQS), o)
            row = re.search(rf"^\| {o} \| [^|]+ \| ([^|]+) \|", self.obj, flags=re.MULTILINE)
            self.assertIsNotNone(row, o)
            self.assertEqual(set(re.findall(r"RQ\d", row.group(1))), rqs, o)
        for rq in RQS:
            self.assertTrue(any(rq in rqs for rqs in obj_to_rq.values()), rq)

    # 6-7. H1-H5 exist, each fully specified and marked TO BE TESTED
    def test_hypotheses_complete_and_untested(self):
        self.assertEqual(self.cfg["hypotheses"], HYPOTHESES)
        self.assertEqual(self.cfg["hypothesis_status"], "TO BE TESTED")
        for h in HYPOTHESES:
            heading = re.search(rf"^## \d+\. {h} — .+$", self.hyp, flags=re.MULTILINE)
            self.assertIsNotNone(heading, h)
            body = _section(self.hyp, heading.group(0))
            self.assertIn("**Statement.**", body)
            for element in HYP_ELEMENTS:
                self.assertIn(f"| {element}", body, (h, element))
            self.assertIn(f"| {h} | STATUS: TO BE TESTED |", self.hyp)
            self.assertEqual(self.by_id[h]["Status"], "TO BE TESTED")
        self.assertEqual(self.hyp.count("STATUS: TO BE TESTED"), len(HYPOTHESES))

    # 8, 17. no fabricated results anywhere in the Step 10A documents
    def test_no_fabricated_results(self):
        # explicit negations (the hypothesis status line and the "will not claim" list) are excluded
        negations = ("None of the hypotheses is proven, supported or refuted.",
                     _section(self.frame, "## 7. Contribution Boundary"))
        for name, text in self.docs.items():
            for negation in negations:
                text = text.replace(negation, "")
            self.assertIsNone(RESULT_CLAIMS.search(text), name)
        for h in HYPOTHESES:
            self.assertNotIn(self.by_id[h]["Status"], ("SUPPORTED", "REFUTED", "PROVEN"))
        self.assertIn("None of the hypotheses is proven, supported or refuted. No data exist.", self.hyp)

    # 9. no invented numerical thresholds
    def test_no_numerical_thresholds(self):
        for name, text in list(self.docs.items()) + [("config", _text(CFG)), ("matrix", _text(MATRIX))]:
            self.assertIsNone(NUMERIC_THRESHOLD.search(text), (name, NUMERIC_THRESHOLD.search(text)))
        for state in self.cfg["resource_states"].values():
            self.assertEqual(state["thresholds"], "to_be_calibrated")
        self.assertEqual(self.cfg["verification_thresholds"], "to_be_calibrated")
        for key in ("significance_level", "smallest_effect_size_of_interest"):
            self.assertEqual(self.cfg["statistics"][key], "to_be_preregistered")

    # 10. baselines B1-B5 with enabled/disabled/purpose/comparison
    def test_baselines(self):
        self.assertEqual(list(self.cfg["baselines"]), ["B1", "B2", "B3", "B4", "B5"])
        flags = {b: (v["resource_adaptation"], v["confidence_verification"]) for b, v in self.cfg["baselines"].items()}
        self.assertEqual(flags, {"B1": (False, False), "B2": (False, False), "B3": (True, False),
                                 "B4": (False, True), "B5": (True, True)})
        section = _section(self.frame, "## 4. Baselines")
        self.assertIn("| Baseline | Enabled | Disabled | Purpose | Comparison it enables |", section)
        for b, v in self.cfg["baselines"].items():
            self.assertIn(f"| **{b} — {v['name']}** |", section)
        self.assertIn("not a sixth baseline", section)

    # 11. resource states R0-R3; thresholds TO BE CALIBRATED
    def test_resource_states(self):
        self.assertEqual(list(self.cfg["resource_states"]), ["R0", "R1", "R2", "R3"])
        section = _section(self.frame, "## 1. Resource-State Framework (R0–R3)")
        for col in ("Transition trigger", "Permitted adaptation", "Possible configuration changes", "Must be recorded"):
            self.assertIn(col, section)
        for r, name in (("R0", "nominal"), ("R1", "moderate resource pressure"), ("R2", "high resource pressure"),
                        ("R3", "critical resource pressure")):
            self.assertIn(f"| **{r} — {name}** |", section)
        self.assertIn("TO BE CALIBRATED DURING EXPERIMENT DESIGN", section)

    # 12. configuration ladder C1-C4 with required properties, no architecture chosen
    def test_configuration_ladder(self):
        self.assertEqual(list(self.cfg["configuration_ladder"]), ["C1", "C2", "C3", "C4"])
        for c in self.cfg["configuration_ladder"].values():
            self.assertIsNone(c["model"])
        section = _section(self.frame, "## 2. Inference Configuration Ladder (C1–C4)")
        self.assertIn("| Configuration | Accuracy | Latency | Memory | Energy | Thermal behaviour | Input requirements |",
                      section)
        for c in ("C1 — highest-accuracy", "C2 — medium", "C3 — lightweight", "C4 — emergency / lowest-resource"):
            self.assertIn(f"| **{c}** |", section)
        self.assertIn("Step 10B", section)

    # 13. verification actions A0-A4; distinguishable from a fixed threshold
    def test_verification_actions(self):
        self.assertEqual(list(self.cfg["verification_actions"]), ["A0", "A1", "A2", "A3", "A4"])
        section = _section(self.frame, "## 3. Confidence-Aware Verification")
        self.assertIn("confidence → verification policy → downstream action", section)
        for a, name in self.cfg["verification_actions"].items():
            self.assertIn(f"| {a} — {name} |", section)
        self.assertIn("How the mechanism differs from a fixed confidence threshold", section)
        self.assertIn("B5-F", section)
        self.assertEqual(self.cfg["ablation_variants"]["B5-F"]["parent"], "B5")

    # 14. contribution is candidate / unvalidated; boundary explicit
    def test_contribution_candidate(self):
        label = "CANDIDATE CONTRIBUTION — TO BE VALIDATED EXPERIMENTALLY"
        self.assertEqual(self.cfg["contribution_status"], label)
        for text in (self.gap, self.frame):
            self.assertIn(f"**{label}**", text)
            self.assertIn(CONTRIBUTION, text)
        boundary = _section(self.frame, "## 7. Contribution Boundary")
        for claim in ("first smartphone inspection system", "first resource-aware inference system",
                      "first confidence-aware inspection system", "first adaptive inspection system",
                      "universal novelty", "superiority over all existing systems"):
            self.assertIn(claim, boundary)
        # outside the explicit "will not claim" list, no novelty language
        for name, text in self.docs.items():
            stripped = text.replace(boundary, "")
            for pattern in (r"\bthe first\b", r"\bfirst to\b", r"\bis novel\b", r"\bunprecedented\b",
                            r"\bno (prior|existing) work\b", r"\bstate-of-the-art\b"):
                self.assertIsNone(re.search(pattern, stripped, re.IGNORECASE), (name, pattern))
        self.assertTrue(self.by_id["CC-1"]["Status"].startswith("CANDIDATE"))

    # traceability matrix completeness
    def test_traceability_matrix(self):
        with open(MATRIX, encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), MATRIX_COLUMNS)
        ids = [r["ID"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ["GC-03"] + RQS + OBJECTIVES + HYPOTHESES + ["CC-1"]:
            self.assertIn(i, self.by_id, i)
        for r in self.rows:
            self.assertEqual(r["Related_Gap"], "GC-03", r["ID"])
            for col in MATRIX_COLUMNS:
                if col not in ("Independent_Variables", "Dependent_Variables") or r["Type"] != "Gap":
                    self.assertTrue(r[col].strip(), (r["ID"], col))
        experiments = {r["ID"] for r in self.rows if r["Type"].startswith("Experiment")}
        self.assertEqual(experiments, {"E1", "E2", "E3"})
        # every objective maps to a hypothesis or a measurement
        for o in OBJECTIVES:
            self.assertTrue(_split(self.by_id[o]["Related_Hypothesis"]) or self.by_id[o]["Dependent_Variables"], o)
        # every hypothesis maps to measurable variables
        for h in HYPOTHESES:
            self.assertTrue(_split(self.by_id[h]["Independent_Variables"]), h)
            self.assertTrue(_split(self.by_id[h]["Dependent_Variables"]), h)
        # every claimed contribution maps to at least one experiment
        for r in self.rows:
            if r["Type"] == "Candidate contribution":
                self.assertTrue(set(re.findall(r"\bE[1-3]\b", r["Evaluation_Method"])) & experiments, r["ID"])

    # variables: classes and measurement vs decision distinction
    def test_variables(self):
        for heading in ("Measurement Variables vs Decision Variables", "Independent Variables", "Dependent Variables",
                        "Control Variables", "Potential Mediators", "Potential Moderators"):
            self.assertIsNotNone(re.search(rf"^## \d+\. {re.escape(heading)}$", self.var, flags=re.MULTILINE), heading)
        for v in ("Battery state", "Temperature", "CPU/GPU utilisation", "Available memory",
                  "Resource-pressure condition", "Inference configuration", "Adaptation state", "Confidence threshold",
                  "Precision", "Recall", "F1", "mAP", "Calibration error", "Latency", "FPS", "Energy / power",
                  "Memory", "Recapture rate", "Escalation rate", "Verification overhead", "Dataset", "Test split",
                  "Device model", "Software version", "Defect type", "Scene complexity", "Image quality"):
            self.assertIn(v, self.var, v)

    # recovery metric retained, with the zero/negligible-denominator edge case
    def test_recovery_metric_edge_case(self):
        rec = self.hyp.split("- **Recovery proportion.**", 1)[1].split("\n- **Pairing", 1)[0]
        self.assertIn("Recovery = (B5 − B3) / (B1 − B3)", rec)
        self.assertIn("If the B1 − B3 denominator is zero or practically negligible, the recovery ratio is "
                      "undefined or uninformative and **must not be interpreted as evidence of recovery**.", rec)
        self.assertIn("`to_be_preregistered`; no numerical threshold is set here", rec)

    # telemetry vs experimental resource condition vs adaptation decision
    def test_resource_variable_layers(self):
        layers = self.var.split("### 1.1 Three layers of resource variables", 1)[1].split("\n## ", 1)[0]
        for layer in ("| 1. Measured resource telemetry |", "| 2. Experimental resource condition |",
                      "| 3. Adaptation decision |"):
            self.assertIn(layer, layers)
        self.assertIn("Not independently manipulated factors unless a later experimental protocol specifies it.", layers)
        ivs = _section(self.var, "## 2. Independent Variables")
        for telemetry in ("Battery state", "Temperature", "CPU/GPU utilisation", "Available memory"):
            row = next(ln for ln in ivs.splitlines() if ln.startswith(f"| {telemetry}"))
            self.assertIn("Layer 1: measured telemetry", row)
            self.assertIn("Not independently manipulated", row)
        for r in self.rows:
            for telemetry in ("battery state", "CPU/GPU utilization", "available memory"):
                self.assertNotIn(telemetry, _split(r["Independent_Variables"]), r["ID"])

    # B5-F is an ablation of B5, never a sixth primary baseline
    def test_b5f_is_ablation(self):
        self.assertNotIn("B5-F", self.cfg["baselines"])
        self.assertEqual(len(self.cfg["baselines"]), 5)
        self.assertEqual(self.cfg["ablation_variants"]["B5-F"]["parent"], "B5")

    # 15-16. no implementation files, no datasets, no results created
    def test_no_implementation_datasets_or_results(self):
        for module in ("acquisition", "adaptation", "inference", "inspection", "monitoring", "quality", "uncertainty"):
            files = sorted(p.name for p in (ROOT / "src" / module).iterdir() if p.name != "__pycache__")
            self.assertEqual(files, ["README.md", "__init__.py"], module)
        for folder in ("mobile", "experiments", "models", "backend"):
            self.assertEqual(sorted(p.name for p in (ROOT / folder).iterdir()), ["README.md"], folder)
        for folder in ("results", "figures", "tables", "manuscript_data"):
            self.assertEqual(sorted(p.name for p in (ROOT / "research" / folder).iterdir()), ["README.md"], folder)
        # research/experiments holds only the README and the Step 10C protocol documents (no runs, no results)
        step_10c_docs = {"experimental_protocol.md", "resource_states.md", "model_selection_protocol.md",
                         "confidence_verification_protocol.md", "measurement_protocol.md",
                         "generalization_framework.md", "experimental_matrix.csv", "log_schema.json"}
        self.assertLessEqual({p.name for p in (ROOT / "research" / "experiments").iterdir()} - {"README.md"},
                             step_10c_docs)
        # research/datasets holds only the README and the Step 10B design documents (no data)
        step_10b_docs = {"dataset_selection.md", "device_requirements.md", "model_ladder.md",
                         "measurement_hardware.md", "verification_checklist.md", "dataset_device_model_matrix.csv"}
        dataset_files = {p.name for p in (ROOT / "research" / "datasets").iterdir()}
        self.assertIn("README.md", dataset_files)
        self.assertLessEqual(dataset_files - {"README.md"}, step_10b_docs)
        data_ext = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".zip", ".tar", ".gz", ".npy", ".npz", ".h5",
                    ".pt", ".pth", ".onnx", ".tflite", ".ckpt", ".parquet"}
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT,
                                   capture_output=True, text=True).stdout.split()
        for rel in tracked + untracked:
            self.assertNotIn(Path(rel).suffix.lower(), data_ext, rel)
        self.assertEqual(sorted(p.name for p in RQ_DIR.iterdir()),
                         sorted(["research_questions.md", "objectives.md", "hypotheses.md",
                                 "variables_and_factors.md", "experimental_framework.md", "traceability_matrix.csv"]))


if __name__ == "__main__":
    unittest.main()
