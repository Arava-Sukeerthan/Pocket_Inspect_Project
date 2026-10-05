"""
Step 10B tests: dataset, smartphone, model-ladder and measurement design for GC-03.

Checks that nothing is marked verified without evidence, that no device is
claimed, that C1-C4 carry no fabricated performance values, that the
resource/decision layers and confidence gating stay distinct, that the
measurement limitations are documented, and that Step 10B created no data,
experiments or results and left the Step 10A artefacts unchanged.
"""
import csv
import hashlib
import re
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "research" / "datasets"
SELECTION = DS / "dataset_selection.md"
DEVICE = DS / "device_requirements.md"
LADDER = DS / "model_ladder.md"
MEASURE = DS / "measurement_hardware.md"
CHECKLIST = DS / "verification_checklist.md"
MATRIX = DS / "dataset_device_model_matrix.csv"
CFG = ROOT / "configs" / "dataset_device_model.yaml"

MATRIX_COLUMNS = [
    "Dataset", "Task", "Visual_Inspection", "Defect_Labels", "Multi_View", "Custom_Capture", "Replay_Suitable",
    "Smartphone_Suitable", "Access_Status", "License_Status", "Primary_or_Secondary", "Device", "C1", "C2", "C3", "C4",
    "Confidence_Signal", "Resource_Telemetry", "Energy_Measurement", "Thermal_Measurement", "Decision", "Evidence",
    "Notes",
]
STATUSES = ("VERIFIED", "SUPPORTED", "PROVISIONAL", "REQUIRES_VERIFICATION")
# SHA-256 of the Step 10A artefacts as merged in PR #14 (main 544fe17).
STEP_10A_HASHES = {
    "research/gap_analysis/research_gap.md": "ca1e6feb9b38e33d21f420011d8fa8e2098cd212dc66003f4f18ae169b5ebb54",
    "research/research_questions/experimental_framework.md":
        "a8b629614e9a1b06d929b959ce304243feeee45497ece230e62c868378ed58c3",
    "research/research_questions/hypotheses.md": "b7117509008f38ceb1e78e48a35fd0f6be3ee9372866e3530995abae7bdfa1cf",
    "research/research_questions/objectives.md": "22f0f80949994d5138c9a8b117c21af711c668a7007543c2e79cae824d144ce9",
    "research/research_questions/research_questions.md":
        "8f44e3b495743a4d27a44ca10441c49f9e7b8bbd853e9e1098468a8ac19459a4",
    "research/research_questions/traceability_matrix.csv":
        "f1e8ee8ea2650176241756783108b26153f802ced8100e14b3d64e65a489e80e",
    "research/research_questions/variables_and_factors.md":
        "2214519d6f20041fac6f02204f85f741aa80d71cb72cb7acb7616fa47957b3f7",
    "configs/research_protocol.yaml": "840535c57a3400c8fa7773ac03a106623018e5e4518dfe62e72e3b1c11f53535",
}
# Numbers with performance units would be fabricated benchmark values.
PERFORMANCE_VALUE = re.compile(
    r"\d+(\.\d+)?\s*(%|\bms\b|\bfps\b|\bFPS\b|\bmW\b|\bmJ\b|\bJ\b|\bmAh\b|\bMB\b|\bGB\b|\bGFLOPs?\b|\bM params\b"
    r"|\bM parameters\b|°\s*C)"
    r"|(accuracy|recall|precision|F1|mAP|AUROC|ECE|latency)\s*(=|:|of|≈|~)\s*\d"
)


def _text(path):
    return path.read_text(encoding="utf-8")


def _section(text, heading):
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def _matrix():
    with open(MATRIX, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class TestDatasetDeviceModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.selection = _text(SELECTION)
        cls.device = _text(DEVICE)
        cls.ladder = _text(LADDER)
        cls.measure = _text(MEASURE)
        cls.checklist = _text(CHECKLIST)
        cls.rows = _matrix()
        with open(CFG, encoding="utf-8") as f:
            cls.cfg = yaml.safe_load(f)
        cls.docs = {"selection": cls.selection, "device": cls.device, "ladder": cls.ladder,
                    "measure": cls.measure, "checklist": cls.checklist}

    # 1. no dataset marked VERIFIED (or SUITABLE) without evidence
    def test_no_dataset_verified(self):
        table = _section(self.selection, "## 3. Candidate Evaluation")
        for line in table.splitlines()[2:]:
            if line.startswith("| **") or line.startswith("| "):
                self.assertNotRegex(line.split("|")[-2], r"\bVERIFIED\b|\bSUITABLE\b(?! as)", line[:40])
        for r in self.rows:
            self.assertNotIn("VERIFIED", r["Decision"].replace("REQUIRES_VERIFICATION", ""), r["Dataset"])
            self.assertNotIn(r["Decision"], ("SUITABLE",), r["Dataset"])
        self.assertEqual(self.cfg["datasets"]["downloaded"], [])
        self.assertIn("**Nothing in this document is VERIFIED.**", self.selection)
        self.assertIn("**No candidate is SUITABLE.**", self.selection)
        for evidence in (r["Evidence"] for r in self.rows):
            self.assertTrue(evidence.strip())

    # 2. no licence marked verified
    def test_no_license_verified(self):
        self.assertEqual(self.cfg["datasets"]["verified_licenses"], [])
        for r in self.rows:
            lic = r["License_Status"].lower()
            self.assertFalse(re.search(r"(?<!not )\bverified\b", lic.replace("requires_verification", "")),
                             r["Dataset"])
        self.assertIn("No dataset licence is VERIFIED.", self.selection)
        self.assertIn("| Any dataset licence | REQUIRES_VERIFICATION (none verified) |", self.selection)

    # 3. no smartphone claimed available
    def test_no_device_claimed(self):
        self.assertIsNone(self.cfg["device"]["selected"])
        self.assertEqual(self.cfg["device"]["available_devices_known"], [])
        self.assertIn("**No smartphone is selected and none is claimed to be available.**", self.device)
        for r in self.rows:
            self.assertEqual(r["Device"], "ACTUAL DEVICE - REQUIRES RESEARCHER CONFIRMATION", r["Dataset"])
        shortlist = _section(self.device, "## 2. Candidate Device Classes (shortlist)")
        self.assertNotRegex(shortlist, r"\|\s*(VERIFIED|SUPPORTED)\s*\|")

    # 4-5. C1-C4 exist and carry no fabricated performance values
    def test_ladder_without_values(self):
        self.assertEqual(list(self.cfg["model_ladder"])[:4], ["C1", "C2", "C3", "C4"])
        for c in ("C1", "C2", "C3", "C4"):
            entry = self.cfg["model_ladder"][c]
            self.assertEqual(entry["metrics"], "requires_empirical_benchmarking")
            self.assertFalse(entry["selected"])
        ladder = _section(self.ladder, "## 3. Candidate Ladder (PROVISIONAL)")
        for head in ("C1 — highest accuracy", "C2 — medium", "C3 — lightweight", "C4 — lowest resource"):
            self.assertIn(head, ladder)
        for field in ("Model family candidate", "Parameter count", "Input size", "Expected accuracy",
                      "Expected latency", "Memory requirement", "Accelerator compatibility", "Quantization options",
                      "Confidence output", "Deployment format", "Limitations"):
            self.assertIn(f"| {field} |", ladder)
        self.assertEqual(ladder.count("REQUIRES EMPIRICAL BENCHMARKING"), 4)
        for name, text in list(self.docs.items()) + [("matrix", _text(MATRIX)), ("config", _text(CFG))]:
            self.assertIsNone(PERFORMANCE_VALUE.search(text), (name, PERFORMANCE_VALUE.search(text)))
        for r in self.rows:
            for c in ("C1", "C2", "C3", "C4"):
                self.assertNotRegex(re.sub(r"\bC[1-4]\b", "", r[c]), r"\d", (r["Dataset"], c))

    # 6. R0-R3 remain distinct from C1-C4
    def test_resource_layers_distinct(self):
        layers = _section(self.measure, "## 1. Telemetry, Resource Condition and Adaptation Decision")
        self.assertIn("| **A. Measured telemetry** |", layers)
        self.assertIn("| **B. Experimental resource condition** | R0 nominal, R1 moderate, R2 high, R3 critical |", layers)
        self.assertIn("| **C. Adaptation decision** | C1–C4 |", layers)
        b_row = next(ln for ln in layers.splitlines() if "B. Experimental resource condition" in ln)
        c_row = next(ln for ln in layers.splitlines() if "C. Adaptation decision" in ln)
        self.assertNotRegex(b_row, r"\bC[1-4]\b")
        self.assertNotRegex(c_row, r"\bR[0-3]\b")
        self.assertIn("manipulated factor", b_row)
        self.assertIn("Decision variable", c_row)

    # 7. confidence gating distinct from raw confidence reporting
    def test_gating_vs_reporting(self):
        section = _section(self.ladder, "## 4. Confidence Signal")
        self.assertIn("**Confidence gating** means that confidence, probability or uncertainty **triggers a downstream "
                      "action** (A1–A4)", section)
        self.assertIn("A logged softmax value that triggers nothing is reporting, not gating.", section)
        self.assertIn("**Raw softmax confidence is not formal uncertainty.**", section)
        self.assertIn("| Raw softmax probability | Max class probability | None (part of inference) | Yes | Reported but "
                      "not used for gating without calibration. |", section)
        self.assertEqual(self.cfg["confidence"]["thresholds"], "to_be_calibrated")
        self.assertIn("reporting, not gating", self.cfg["confidence"]["gating_definition"])

    # 8. energy limitations documented
    def test_energy_limitations(self):
        energy = _section(self.measure, "## 2. Energy Measurement")
        self.assertIn("**EXTERNAL-METER VALIDATION REQUIRED.**", energy)
        self.assertIn("No energy accuracy is claimed", energy)
        for option in ("**1. Android battery APIs**", "**2. Power/current telemetry**", "**3. External USB power meter**",
                       "**4. External power analyzer with battery bypass**"):
            self.assertIn(option, energy)
        for quantity in ("Energy per inference", "energy per inspected item", "energy per verified item",
                         "average power", "peak power"):
            self.assertIn(quantity, energy)
        self.assertIn("Sampling rates: **not chosen**", energy)
        self.assertTrue(self.cfg["energy"]["external_meter_validation_required"])

    # 9. thermal limitations documented
    def test_thermal_limitations(self):
        thermal = _section(self.measure, "## 3. Thermal Measurement")
        self.assertIn("**Temperature measurement vs thermal state.**", thermal)
        self.assertIn("No Android API is assumed to expose every required temperature.", thermal)
        for q in ("SoC / CPU temperature", "Battery temperature", "Skin / device temperature", "Ambient temperature",
                  "Thermal throttling state", "Sustained-performance degradation"):
            self.assertIn(f"| {q} |", thermal)
        self.assertTrue(self.cfg["thermal"]["temperature_and_throttling_state_logged_separately"])

    # 10. multi-view / recapture limitations documented
    def test_multiview_limitations(self):
        self.assertIn("**CUSTOM SMARTPHONE CAPTURE REQUIRED.**", self.selection)
        self.assertIn("No evaluated static benchmark contains repeated captures of the same view of the same item.",
                      self.selection)
        self.assertIn("Fixed pre-recorded views, not chosen or captured by the phone", self.selection)
        self.assertFalse(self.cfg["multi_view"]["same_view_recapture_in_static_benchmarks"])
        self.assertTrue(self.cfg["datasets"]["custom_smartphone_capture_required"])
        protocol = _section(self.selection, "## 6. Secondary Dataset: Minimum Custom-Capture Requirements (protocol only)")
        for item in ("**Items.**", "**Views.**", "**Recapture.**", "**Splits.**", "**Defect-preserving views.**"):
            self.assertIn(item, protocol)

    # 11. matrix exists with the required columns; primary/secondary consistent
    def test_matrix(self):
        with open(MATRIX, encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), MATRIX_COLUMNS)
        roles = {r["Dataset"]: r["Primary_or_Secondary"] for r in self.rows}
        self.assertEqual(roles["Real-IAD"], "Primary (PROVISIONAL)")
        self.assertEqual(roles["Phone-captured 3D-printed-part set"], "Secondary (PROVISIONAL)")
        self.assertEqual(sum(v.startswith("Primary") for v in roles.values()), 1)
        self.assertEqual(self.cfg["datasets"]["primary"]["name"], "Real-IAD")
        self.assertEqual(self.cfg["datasets"]["primary"]["status"], "PROVISIONAL")
        for r in self.rows:
            for col in MATRIX_COLUMNS:
                self.assertTrue(r[col].strip(), (r["Dataset"], col))

    # checklist covers the required areas; nothing is complete
    def test_checklist(self):
        for area in ("Dataset access verification", "Dataset license verification", "Smartphone availability",
                     "Android version", "Telemetry API verification", "Thermal API verification",
                     "Energy measurement verification", "Accelerator verification", "Model deployment verification",
                     "Confidence-output verification", "Multi-view/recapture verification"):
            self.assertIn(f"| {area} |", self.checklist)
        rows = [ln for ln in self.checklist.splitlines() if re.match(r"\| V-\d+ \|", ln)]
        self.assertTrue(rows)
        for ln in rows:
            status = ln.rstrip(" |").rsplit("|", 1)[-1].strip()
            self.assertTrue(status.startswith("REQUIRES"), ln[:12])

    # every major decision carries an allowed status
    def test_decision_statuses(self):
        self.assertEqual(tuple(self.cfg["decision_statuses"]), STATUSES)
        for section, doc in ((self.selection, "selection"), (self.ladder, "ladder"), (self.device, "device"),
                             (self.measure, "measure")):
            status = section.rsplit("\n## ", 1)[-1]
            self.assertTrue(any(s in status for s in STATUSES), doc)
            self.assertNotRegex(status, r"\|\s*VERIFIED", doc)

    # 12-14. no datasets downloaded, no experiments run, no results
    def test_no_data_experiments_or_results(self):
        data_ext = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".zip", ".tar", ".gz", ".npy", ".npz", ".h5",
                    ".pt", ".pth", ".onnx", ".tflite", ".ckpt", ".parquet", ".pte", ".pkl"}
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                             capture_output=True, text=True).stdout.split()
        for rel in out:
            self.assertNotIn(Path(rel).suffix.lower(), data_ext, rel)
        for folder in ("results", "experiments", "figures", "tables", "manuscript_data"):
            self.assertEqual(sorted(p.name for p in (ROOT / "research" / folder).iterdir()), ["README.md"], folder)
        for folder in ("experiments", "mobile", "models", "backend"):
            self.assertEqual(sorted(p.name for p in (ROOT / folder).iterdir()), ["README.md"], folder)
        for module in ("acquisition", "adaptation", "inference", "inspection", "monitoring", "quality", "uncertainty"):
            files = sorted(p.name for p in (ROOT / "src" / module).iterdir() if p.name != "__pycache__")
            self.assertEqual(files, ["README.md", "__init__.py"], module)
        claims = re.compile(r"\b(we (measured|benchmarked|observed|found)|(?<!nothing )was measured|benchmark results?|achieved)\b",
                            re.IGNORECASE)
        for name, text in self.docs.items():
            self.assertIsNone(claims.search(text), name)

    # 15. Step 10A artefacts unchanged
    def test_step_10a_unchanged(self):
        for rel, digest in STEP_10A_HASHES.items():
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest, rel)


class TestStep10BBoundaries(unittest.TestCase):
    """Final Step 10B refinement: device, Stage 1/2, custom capture and C1-C4 boundaries."""

    @classmethod
    def setUpClass(cls):
        cls.selection = _text(SELECTION)
        cls.device = _text(DEVICE)
        cls.ladder = _text(LADDER)
        cls.checklist = _text(CHECKLIST)
        cls.rows = {r["Dataset"]: r for r in _matrix()}
        with open(CFG, encoding="utf-8") as f:
            cls.cfg = yaml.safe_load(f)

    def test_no_smartphone_falsely_available(self):
        self.assertIn("**ACTUAL DEVICE — REQUIRES RESEARCHER CONFIRMATION.**", self.device)
        self.assertEqual(self.cfg["device"]["actual_device_status"], "ACTUAL DEVICE — REQUIRES RESEARCHER CONFIRMATION")
        self.assertFalse(self.cfg["device"]["repository_evidence_of_available_device"])
        self.assertIsNone(self.cfg["device"]["selected"])
        self.assertTrue(self.cfg["device"]["candidate_classes_are_requirement_classes_only"])
        self.assertIn("**These are requirement classes only, not device selections.**", self.device)
        lowered = self.device.lower()
        for claim in ("device is available", "phone is available", "we have a", "selected device:", "has been selected"):
            self.assertNotIn(claim, lowered)

    def test_real_iad_not_smartphone_captured(self):
        row = self.rows["Real-IAD"]
        self.assertTrue(row["Smartphone_Suitable"].startswith("No"))
        self.assertIn("simulation only, not smartphone recapture", row["Multi_View"])
        self.assertFalse(self.cfg["multi_view"]["real_iad_smartphone_captured"])
        self.assertFalse(self.cfg["multi_view"]["real_iad_provides_smartphone_recapture"])
        self.assertEqual(self.cfg["multi_view"]["stage1_interpretation"], "controlled_additional_view_simulation")
        stages = self.selection.split("### Stage boundary: simulated vs actual additional views", 1)[1].split("\n### ", 1)[0]
        self.assertIn("**Stage 1 — controlled additional-view simulation**", stages)
        self.assertIn("**Stage 2 — actual recapture / additional-view experiment**", stages)
        self.assertIn("**Not physical smartphone recapture.**", stages)
        self.assertIn("**Real-IAD does not provide smartphone recapture data**", stages)

    def test_custom_capture_not_existing_dataset(self):
        self.assertFalse(self.cfg["datasets"]["secondary"]["exists"])
        row = self.rows["Phone-captured 3D-printed-part set"]
        self.assertTrue(row["Access_Status"].startswith("Does not exist"))
        self.assertIn("PROTOCOL ONLY", row["Decision"])
        self.assertIn("Not an existing dataset", row["Notes"])
        section = _section(self.selection, "## 6. Secondary Dataset: Minimum Custom-Capture Requirements (protocol only)")
        self.assertIn("**PROVISIONAL — PROTOCOL ONLY.**", section)
        self.assertIn("**does not exist** and must not be treated as an existing dataset", section)
        for req in ("physical parts", "controlled defect / non-defect conditions", "item identifiers", "repeated captures",
                    "same-view recapture", "additional views", "train/validation/test split by physical item",
                    "smartphone camera metadata", "lighting/environment metadata", "resource telemetry where appropriate"):
            self.assertIn(f"- {req}", section)
        self.assertIn("No data are collected in Step 10B.", section)

    def test_ladder_remains_provisional(self):
        ladder = self.cfg["model_ladder"]
        self.assertEqual(ladder["status"], "PROVISIONAL")
        self.assertEqual(ladder["final_assignment"], "deferred_to_implementation_benchmark_stage")
        self.assertEqual(len(ladder["selection_rule_preconditions"]), 7)
        for c in ("C1", "C2", "C3", "C4"):
            self.assertFalse(ladder[c]["selected"])
            self.assertIn("PROVISIONAL", self.rows["Real-IAD"][c])
        rule = self.ladder.split("### Formal C1–C4 selection rule", 1)[1].split("**Ladder-construction rule", 1)[0]
        self.assertIn("**Final C1–C4 model assignment is deferred to the implementation benchmark stage.**", rule)
        self.assertEqual(len(re.findall(r"^\d\. ", rule, flags=re.MULTILINE)), 7)
        for step in ("the smartphone is confirmed", "support the same inspection task", "offline deployment is verified",
                     "confidence/probability output is available", "ordered by **measured** resource cost",
                     "minimum functional inspection requirements", "empirical benchmarking confirms a meaningful"):
            self.assertIn(step, rule)

    def test_no_fabricated_model_performance(self):
        for name, text in (("ladder", self.ladder), ("matrix", _text(MATRIX)), ("config", _text(CFG)),
                           ("selection", self.selection), ("device", self.device)):
            self.assertIsNone(PERFORMANCE_VALUE.search(text), name)
        for r in self.rows.values():
            for c in ("C1", "C2", "C3", "C4"):
                self.assertNotRegex(re.sub(r"\bC[1-4]\b", "", r[c]), r"\d", (r["Dataset"], c))

    def test_four_gates_open(self):
        for gate, name in (("G1", "actual smartphone confirmed"), ("G2", "Real-IAD multi-view interpretation confirmed"),
                           ("G3", "custom smartphone capture protocol confirmed"),
                           ("G4", "C1–C4 empirical selection criteria confirmed")):
            line = next(ln for ln in self.checklist.splitlines() if ln.startswith(f"| {gate} — {name} |"))
            self.assertTrue(line.rstrip().endswith("| OPEN / REQUIRES VERIFICATION |"), gate)
            self.assertEqual(self.cfg["gates"][gate]["status"], "OPEN_REQUIRES_VERIFICATION")


if __name__ == "__main__":
    unittest.main()
