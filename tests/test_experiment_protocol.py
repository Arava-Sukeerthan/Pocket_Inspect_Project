"""
Step 10C tests: generalizable resource-aware experimental protocol for GC-03.

Checks that the protocol keeps the approved gap, RQ1 and baselines unchanged,
records the OPPO A5 2020 (3 GB) as the experimental platform rather than the
contribution, describes the methodology independently of that device,
fabricates no ladder, threshold, telemetry or result, and keeps the Stage 1 /
Stage 2, energy and thermal boundaries explicit.
"""
import csv
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "research" / "experiments"
PROTOCOL = EXP / "experimental_protocol.md"
STATES = EXP / "resource_states.md"
LADDER = EXP / "model_selection_protocol.md"
CONFVER = EXP / "confidence_verification_protocol.md"
MEASURE = EXP / "measurement_protocol.md"
GENERAL = EXP / "generalization_framework.md"
MATRIX = EXP / "experimental_matrix.csv"
SCHEMA = EXP / "log_schema.json"
CFG = ROOT / "configs" / "experiment_protocol.yaml"
RP_CFG = ROOT / "configs" / "research_protocol.yaml"
SEL_CFG = ROOT / "configs" / "gap_selection.yaml"

GC03 = (
    "Within the reviewed literature corpus, there is limited evidence of an integrated resource-aware smartphone "
    "visual-inspection system in which device-state-driven runtime adaptation is coupled with confidence-aware "
    "downstream verification, particularly for recovering inspection performance under resource-induced "
    "model/configuration degradation."
)
RQ1 = (
    "Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained "
    "smartphone dynamically downgrades its inference configuration under changing device conditions?"
)
PRINCIPLE = (
    "The OPPO A5 2020 serves as the primary experimental platform rather than defining the scope of the proposed "
    "methodology. The methodology is intended for resource-constrained and legacy smartphones more generally. "
    "Device-specific results are reported as evidence obtained on the selected platform, while claims of "
    "generalization beyond the evaluated device are limited to what the experimental design supports."
)
HYPOTHESES = {
    "H1": "Resource-driven runtime downgrading decreases inspection performance relative to the best static "
          "configuration under equivalent task conditions.",
    "H2": "Confidence-aware downstream verification recovers a measurable portion of the performance degradation "
          "introduced by resource-driven downgrading.",
    "H3": "Confidence-aware verification introduces measurable latency, energy, memory, or thermal overhead.",
    "H4": "Confidence distributions and calibration characteristics differ between inference configurations "
          "operating under different resource conditions.",
    "H5": "A joint resource-adaptation + confidence-verification policy provides a more favorable "
          "accuracy–efficiency trade-off than either mechanism alone.",
}
AVAILABILITY = ("REQUIRED / DIRECTLY AVAILABLE", "CONDITIONALLY AVAILABLE", "EXTERNAL INSTRUMENTATION REQUIRED",
                "UNAVAILABLE", "Design element")
SCHEMA_FIELDS = [
    "experiment_id", "run_id", "timestamp", "device_id", "device_model", "ram_variant", "dataset", "item_id",
    "image_id", "view_id", "ground_truth", "resource_state", "battery_level", "battery_temperature", "ram_usage",
    "cpu_usage", "gpu_usage", "model_config", "model_load_time", "inference_latency", "prediction", "confidence",
    "calibrated_confidence", "verification_triggered", "verification_action", "verification_latency",
    "final_prediction", "correct", "energy_measurement", "thermal_measurement", "thermal_state",
    "environment_metadata",
]
# A number followed by a latency/energy/power/thermal/accuracy unit, or a metric assigned a number,
# would be a fabricated measurement.
MEASURED_VALUE = re.compile(
    r"\d+(\.\d+)?\s*(ms\b|s\b|seconds?\b|minutes?\b|fps\b|FPS\b|J\b|mJ\b|Wh\b|mWh\b|W\b|mW\b|°\s*C|degrees?\b|%|"
    r"percent\b|MB\b|kB\b)"
    r"|(accuracy|recall|precision|F1|mAP|AUROC|ECE|latency|energy|power|temperature)\s*(=|:|of|≈|~)\s*\d"
    r"|\b0\.\d+\b"
)
SPEC_LINES = ("| Storage |", "| SoC |", "| CPU |", "| Battery |", "| Rear cameras |", "| Experimental RAM variant |",
              "| Manufacturer / model |", "| GPU |", "| Android launch version |")


def _text(path):
    return path.read_text(encoding="utf-8")


def _section(text, start, end="\n## "):
    return text.split(start, 1)[1].split(end, 1)[0]


def _docs():
    return {p.name: _text(p) for p in (PROTOCOL, STATES, LADDER, CONFVER, MEASURE, GENERAL)}


def _without_spec(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.startswith(SPEC_LINES))


class TestExperimentProtocol(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.docs = _docs()
        cls.protocol = cls.docs["experimental_protocol.md"]
        with open(CFG, encoding="utf-8") as f:
            cls.cfg = yaml.safe_load(f)
        with open(RP_CFG, encoding="utf-8") as f:
            cls.rp = yaml.safe_load(f)
        with open(SEL_CFG, encoding="utf-8") as f:
            cls.sel = yaml.safe_load(f)
        with open(MATRIX, encoding="utf-8", newline="") as f:
            cls.matrix = list(csv.DictReader(f))
        cls.schema = json.loads(_text(SCHEMA))

    # GC-03 and RQ1 unchanged
    def test_gap_and_rq_unchanged(self):
        self.assertEqual(self.rp["approved_gap"]["wording"], GC03)
        self.assertEqual(self.sel["approval_ready"]["GC-03"]["candidate_gap"], GC03)
        self.assertIn(f"> {GC03}", _text(ROOT / "research" / "gap_analysis" / "research_gap.md"))
        self.assertEqual(self.rp["primary_rq"], RQ1)
        self.assertIn(f'**Primary RQ (unchanged).** "{RQ1}"', self.protocol)
        hyp_section = _section(self.protocol, "## 9. Hypotheses, Falsification and Outcome Categories")
        for h, statement in HYPOTHESES.items():
            self.assertIn(f"- **{h}.** {statement}", hyp_section)
        for f_id in ("F1", "F2", "F3", "F4", "F5", "F6"):
            self.assertIn(f"| {f_id} |", hyp_section)

    # B1-B5 unchanged; B5-F an ablation
    def test_baselines(self):
        self.assertEqual(self.cfg["baselines"], self.rp["baselines"])
        self.assertNotIn("B5-F", self.cfg["baselines"])
        self.assertEqual(self.cfg["ablation_variants"]["B5-F"]["parent"], "B5")
        self.assertFalse(self.cfg["ablation_variants"]["B5-F"]["primary_baseline"])
        table = _section(self.protocol, "## 5. Baselines")
        self.assertIn("| Baseline | Model policy | Resource adaptation | Confidence verification | Purpose |", table)
        for b, entry in self.cfg["baselines"].items():
            self.assertIn(f"| {b} — {entry['name']} |", table)
        self.assertIn("| B5-F — **ablation of B5**, not a sixth primary baseline |", table)
        self.assertNotIn("OPPO", table)

    # OPPO A5 2020 3 GB confirmed; 4/6 GB excluded
    def test_confirmed_platform(self):
        plat = self.cfg["platform"]
        self.assertEqual((plat["manufacturer"], plat["model"], plat["ram_variant"]), ("OPPO", "OPPO A5 2020", "3 GB"))
        self.assertEqual(plat["excluded_variants"], ["4 GB", "6 GB"])
        self.assertEqual(plat["confirmed_by"], "researcher")
        self.assertEqual(plat["capabilities_verified"], [])
        self.assertEqual(plat["measurements"], [])
        self.assertEqual(plat["installed_android_version"], "requires_device_verification")
        spec = _section(self.docs["measurement_protocol.md"], "**A. Known device specifications.**", "**B.")
        self.assertIn("| Experimental RAM variant | **3 GB** LPDDR4X (only this variant; the 4 GB and 6 GB variants "
                      "are **not** the experimental platform) |", spec)
        for name, text in self.docs.items():
            for m in re.finditer(r"[46] GB", text):
                window = text[max(0, m.start() - 120):m.end() + 120].lower()
                self.assertTrue("not" in window or "exclud" in window, (name, window))
        self.assertEqual(self.cfg["gates"]["G1"]["status"], "CLOSED_VERIFIED")

    # OPPO is the platform, not the contribution; methodology independent of OPPO
    def test_platform_not_contribution(self):
        self.assertFalse(self.cfg["positioning"]["experimental_platform_is_contribution"])
        self.assertEqual(self.cfg["positioning"]["generalization_principle"], PRINCIPLE)
        for name in ("experimental_protocol.md", "generalization_framework.md"):
            self.assertIn(f"> {PRINCIPLE}", self.docs[name])
        self.assertIn("It is not the contribution", self.docs["generalization_framework.md"])
        for name, text in self.docs.items():
            lowered = text.lower()
            for claim in ("designed specifically for the oppo", "system for the oppo a5 2020", "oppo-specific method",
                          "contribution is the oppo"):
                self.assertNotIn(claim, lowered, name)
        self.assertNotIn("OPPO", yaml.safe_dump(self.cfg["methodology"]))
        self.assertNotIn("OPPO", yaml.safe_dump(self.cfg["baselines"]))

    def test_methodology_described_independently(self):
        architecture = _section(self.protocol, "## 2. General Architecture (device-independent)").split("```")[1]
        self.assertNotIn("OPPO", architecture)
        general_states = _section(self.docs["resource_states.md"], "## Part I — General Resource-State Framework",
                                  "## Part II")
        self.assertNotIn("OPPO", general_states)
        self.assertIn("## Part II — OPPO A5 2020 (3 GB) Instantiation", self.docs["resource_states.md"])
        ladder_general = self.docs["model_selection_protocol.md"].split("## 4. OPPO A5 2020 (3 GB) Instantiation")[0]
        self.assertNotIn("OPPO", ladder_general)
        conf_general = self.docs["confidence_verification_protocol.md"].split("## 6. OPPO A5 2020")[0]
        self.assertNotIn("OPPO", conf_general)

    # C1-C4 not fabricated
    def test_ladder_not_fabricated(self):
        m = self.cfg["methodology"]
        self.assertEqual(m["ladder_identities"], "to_be_empirically_determined")
        self.assertEqual(len(m["ladder_selection_steps"]), 7)
        self.assertEqual(m["r_to_c_mapping"], "to_be_derived_from_E1_and_frozen")
        self.assertIn("**Final C1–C4 identities: TO BE EMPIRICALLY DETERMINED.**", self.docs["model_selection_protocol.md"])
        self.assertIn("**Candidate only.**", self.docs["resource_states.md"])
        families = ("EfficientNet", "ConvNeXt", "MobileNet", "ResNet", "ViT", "YOLO")
        for row in self.matrix:
            for fam in families:
                self.assertNotIn(fam, row["Model_Configuration"], row["Row_ID"])
        steps = _section(self.docs["model_selection_protocol.md"], "## 2. Seven-Step Empirical Selection Procedure")
        self.assertEqual(len(re.findall(r"^\| [1-7] \|", steps, flags=re.MULTILINE)), 7)

    # R0-R3 thresholds not fabricated
    def test_thresholds_not_fabricated(self):
        m = self.cfg["methodology"]
        for key in ("thresholds", "hysteresis", "minimum_dwell_time"):
            self.assertEqual(m[key], "to_be_derived_from_E0_and_frozen")
        self.assertIsNone(m["pressure_mechanism_selected"])
        self.assertEqual(m["thresholds_confidence"], "to_be_computed_by_frozen_rule")
        self.assertIn("No threshold is chosen for convenience", self.docs["resource_states.md"])
        for name, text in self.docs.items():
            self.assertIsNone(re.search(r"(threshold|τ|tau)\w*\s*(=|≥|<=|>=|<|>)\s*\d", text), name)

    # no experimental results; no fabricated latency/energy/thermal/accuracy values
    def test_no_results_or_fabricated_values(self):
        self.assertEqual(self.cfg["results"], [])
        res_files = sorted(p.name for p in (ROOT / "research" / "results").iterdir())
        self.assertLessEqual(set(res_files) - {"README.md"}, {"device_characterization"})
        for name, text in self.docs.items():
            hit = MEASURED_VALUE.search(_without_spec(text))
            self.assertIsNone(hit, (name, hit))
        for path in (MATRIX, SCHEMA):
            self.assertIsNone(MEASURED_VALUE.search(_text(path)), path.name)
        config_text = yaml.safe_dump({k: v for k, v in self.cfg.items() if k != "platform"})
        self.assertIsNone(MEASURED_VALUE.search(config_text))
        claims = re.compile(r"\b(we (measured|observed|found|benchmarked)|results show|was measured at|achieved)\b",
                            re.IGNORECASE)
        for name, text in self.docs.items():
            self.assertIsNone(claims.search(text), name)
        self.assertIn("**No experiments, measurements, model benchmarking, dataset collection, or empirical results "
                      "were produced in Step 10C.**", self.protocol)

    # Real-IAD views are not smartphone recapture; custom dataset does not exist
    def test_stage_boundaries(self):
        self.assertFalse(self.cfg["stages"]["stage1"]["smartphone_recapture"])
        self.assertEqual(self.cfg["stages"]["stage1"]["additional_view"], "controlled_simulation")
        self.assertEqual(self.cfg["methodology"]["verification_actions"]["A1"]["stage1"], "not_available")
        self.assertFalse(self.cfg["stages"]["stage2"]["exists"])
        self.assertEqual(self.cfg["stages"]["stage2"]["status"], "protocol_only_not_collected")
        self.assertIn("Real-IAD stored views are **not** smartphone recapture", self.protocol)
        self.assertIn("**PROTOCOL ONLY — NOT YET COLLECTED**", self.protocol)
        a1 = next(ln for ln in self.docs["confidence_verification_protocol.md"].splitlines() if ln.startswith("| A1 |"))
        self.assertIn("**NOT AVAILABLE.**", a1)
        rows = [r for r in self.matrix if "A1" in r["Verification_Action"] and r["Dataset"].startswith("Real-IAD")]
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(r["Status"], "NOT_APPLICABLE", r["Row_ID"])
        stage2 = [r for r in self.matrix if r["Stage"] == "Stage 2"]
        self.assertTrue(stage2)
        for r in stage2:
            self.assertIn("NOT YET COLLECTED", r["Dataset"])
            self.assertNotEqual(r["Status"], "REQUIRED")
        for name, text in self.docs.items():
            self.assertNotRegex(text.lower(), r"real-iad (provides|contains|offers) (smartphone )?recapture", name)
            self.assertNotRegex(text.lower(), r"custom (smartphone )?dataset (exists|was collected|has been collected)",
                                name)

    # recovery denominator edge case
    def test_recovery_edge_case(self):
        rec = _section(self.protocol, "## 6. Recovery Metric")
        self.assertIn("**Recovery** = (B5 − B3) / (B1 − B3)", rec)
        self.assertIn("If B1 − B3 is zero or practically negligible, ρ is **undefined or uninformative** and is **not** "
                      "interpreted as evidence of recovery.", rec)
        self.assertIn("**Value: PRE-DATA-COLLECTION DECISION REQUIRED.**", rec)
        self.assertEqual(self.cfg["recovery"]["metric"], "item_level_defect_recall")
        self.assertEqual(self.cfg["recovery"]["sesoi"], "pre_data_collection_decision_required")

    # telemetry availability classified, not fabricated
    def test_telemetry_classification(self):
        table = _section(self.docs["measurement_protocol.md"], "## 2. E0 — Device Characterisation (pilot only)")
        rows = [ln for ln in table.splitlines() if ln.startswith("| ") and not ln.startswith(("| Variable", "| :--"))]
        self.assertGreaterEqual(len(rows), 20)
        for ln in rows:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            self.assertEqual(len(cells), 7, ln[:40])
            self.assertTrue(cells[2].startswith(AVAILABILITY), cells)
            self.assertNotIn("VERIFIED", cells[2])
        self.assertIn("None is verified on the device.", self.docs["measurement_protocol.md"])
        for header in ("Variable", "Source / API", "Expected availability", "Unit", "Sampling interval", "Validation",
                       "Role"):
            self.assertIn(header, table.splitlines()[next(i for i, ln in enumerate(table.splitlines())
                                                          if ln.startswith("| Variable"))])

    # external energy validation; thermal measurement separate from thermal state
    def test_energy_and_thermal(self):
        self.assertTrue(self.cfg["energy_external_validation_required"])
        self.assertTrue(self.cfg["thermal_measurement_separate_from_thermal_state"])
        energy = _section(self.docs["measurement_protocol.md"], "## 4. Energy")
        self.assertIn("**EXTERNAL-METER VALIDATION REQUIRED.** Software battery counters are **not** ground truth.", energy)
        thermal = _section(self.docs["measurement_protocol.md"], "## 5. Thermal")
        self.assertIn("are logged in separate fields and analysed separately", thermal)
        props = self.schema["properties"]
        self.assertIn("thermal_measurement", props)
        self.assertIn("thermal_state", props)
        self.assertNotEqual(props["thermal_measurement"]["description"], props["thermal_state"]["description"])

    # device-specific vs methodological results
    def test_result_classification(self):
        self.assertEqual(self.cfg["positioning"]["result_classes"],
                         ["DEVICE_SPECIFIC_RESULT", "METHODOLOGICAL_RESULT", "GENERALIZATION_EVIDENCE",
                          "UNVALIDATED_GENERALIZATION"])
        table = _section(self.docs["generalization_framework.md"], "## 2. Result Classification")
        for cls in ("**A. DEVICE-SPECIFIC RESULT**", "**B. METHODOLOGICAL RESULT**", "**C. GENERALIZATION EVIDENCE**",
                    "**D. UNVALIDATED GENERALIZATION**"):
            self.assertIn(cls, table)
        self.assertIn("Numerical performance from the OPPO A5 2020 is never extrapolated to other legacy smartphones.",
                      table)
        self.assertEqual(self.cfg["platform"]["additional_devices"], [])
        legacy = _section(self.docs["generalization_framework.md"], "## 3. Legacy / Resource-Constrained Smartphone Class")
        self.assertIn('"Legacy" is not defined by chronological age.', legacy)
        self.assertIn("Not every old smartphone will meet them.", legacy)

    # log schema
    def test_log_schema(self):
        props = self.schema["properties"]
        for field in SCHEMA_FIELDS:
            self.assertIn(field, props, field)
        allowed = {"REQUIRED", "OPTIONAL", "CONDITIONALLY_AVAILABLE"}
        for name, spec in props.items():
            self.assertIn(spec["x-availability"], allowed, name)
            for key in ("examples", "default", "const"):
                self.assertNotIn(key, spec, name)
        self.assertEqual(sorted(self.schema["required"]),
                         sorted(k for k, v in props.items() if v["x-availability"] == "REQUIRED"))
        for name in ("gpu_usage", "cpu_usage", "energy_measurement", "thermal_state", "battery_current"):
            self.assertEqual(props[name]["x-availability"], "CONDITIONALLY_AVAILABLE", name)
        self.assertIn("calibrated_confidence", self.schema["required"])
        self.assertIn("not calibrated", props["confidence"]["description"])

    # experimental matrix
    def test_matrix(self):
        statuses = {"REQUIRED", "OPTIONAL", "PILOT_ONLY", "NOT_APPLICABLE"}
        for r in self.matrix:
            self.assertIn(r["Status"], statuses, r["Row_ID"])
            if r["Status"] != "NOT_APPLICABLE":
                self.assertEqual(r["Device"], "OPPO A5 2020 (3 GB)", r["Row_ID"])
        e1 = {(r["Model_Configuration"], r["Resource_State"]) for r in self.matrix
              if r["Experiment"] == "E1" and r["Status"] == "REQUIRED" and r["Model_Configuration"] in
              ("C1", "C2", "C3", "C4")}
        self.assertEqual(len(e1), 16)
        e2 = {r["Baseline"] for r in self.matrix if r["Experiment"] == "E2" and r["Status"] == "REQUIRED"}
        self.assertEqual(e2, {"B1", "B2", "B3", "B4", "B5"})
        e3 = [r for r in self.matrix if r["Experiment"] == "E3" and r["Status"] == "REQUIRED"]
        self.assertEqual([r["Baseline"] for r in e3], ["B5-F (ablation of B5)"])
        other = [r for r in self.matrix if r["Device"] == "Other smartphones"]
        self.assertEqual([r["Status"] for r in other], ["NOT_APPLICABLE"])
        self.assertIn("**Reduction rationale.**", self.protocol)

    # gates
    def test_gates(self):
        g = self.cfg["gates"]
        self.assertEqual(g["G1"]["status"], "CLOSED_VERIFIED")
        for gate in ("G2", "G3", "G4"):
            self.assertEqual(g[gate]["status"], "OPEN_REQUIRES_VERIFICATION", gate)
        self.assertFalse(g["G3"]["dataset_collected"])
        self.assertFalse(g["G4"]["empirical_selection_done"])
        checklist = _text(ROOT / "research" / "datasets" / "verification_checklist.md")
        for gate in ("G2", "G3", "G4"):
            line = next(ln for ln in checklist.splitlines() if ln.startswith(f"| {gate} — "))
            self.assertTrue(line.rstrip().endswith("| OPEN / REQUIRES VERIFICATION |"), gate)

    # unresolved decisions are explicit
    def test_decisions_required(self):
        section = _section(self.protocol, "## 14. Decisions Required Before Data Collection")
        ids = re.findall(r"^\| (D-\d\d) \|", section, flags=re.MULTILINE)
        self.assertEqual(ids, self.cfg["decisions_required"])
        self.assertIn("**Refinement issues** (recorded; not applied without researcher decision):", self.protocol)


if __name__ == "__main__":
    unittest.main()
