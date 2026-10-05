"""
Step 10C-DR tests: pre-data-collection decision register.

Checks that D-01 to D-16 are registered, traceable and given an allowed status;
that the freeze configuration holds only frozen rules and no numerical
parameters; that no measurement, telemetry, ladder identity or threshold is
fabricated; and that the statistical refinements (clustered repeated runs,
precision safeguard) are recorded without changing the approved gap, RQ1,
baselines or recovery metric.
"""
import csv
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "research" / "experiments"
REGISTER = EXP / "pre_data_collection_decision_register.md"
TRACE = EXP / "decision_traceability.csv"
FREEZE = ROOT / "configs" / "pre_data_collection.yaml"
EXP_CFG = ROOT / "configs" / "experiment_protocol.yaml"
RP_CFG = ROOT / "configs" / "research_protocol.yaml"

IDS = [f"D-{i:02d}" for i in range(1, 17)]
STATUSES = ("RESOLVED", "PRE-DATA-COLLECTION FREEZE", "PILOT-DEPENDENT", "DEVICE-VERIFICATION DEPENDENT", "DEFERRED",
            "NOT APPLICABLE")
CATEGORY_KEYS = ("frozen_now", "pilot_dependent", "device_verification_dependent", "requires_future_approval")
SUMMARY_COLUMNS = ["Decision ID", "Decision", "Current status", "Resolution", "Rationale", "Evidence/source",
                   "Depends on measurement?", "Freeze point", "Impact on experiment"]
TRACE_COLUMNS = ["decision_id", "decision", "related_RQ", "related_hypothesis", "related_protocol_section", "status",
                 "freeze_point", "evidence", "impact"]
RQ1 = ("Can confidence-aware downstream verification recover inspection accuracy lost when a resource-constrained "
       "smartphone dynamically downgrades its inference configuration under changing device conditions?")
# Decimal numbers allowed in the register, each with its required context.
ALLOWED_DECIMALS = {"0.05": "α", "0.80": "power", "0.5": "argmax", "1.96": "Bland–Altman"}
MEASURED_VALUE = re.compile(
    r"\d+(\.\d+)?\s*(ms\b|seconds?\b|fps\b|FPS\b|mJ\b|J\b|mWh\b|Wh\b|mW\b|W\b|°\s*C|%|MB\b|kB\b|GHz\b|mAh\b)"
    r"|(accuracy|recall|precision|F1|latency|energy|temperature|threshold|τ)\w*\s*(=|≈|~)\s*\d"
)


def _text(path):
    return path.read_text(encoding="utf-8")


def _section(text, start, end="\n### "):
    return text.split(start, 1)[1].split(end, 1)[0]


class TestDecisionRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reg = _text(REGISTER)
        with open(FREEZE, encoding="utf-8") as f:
            cls.freeze = yaml.safe_load(f)
        with open(EXP_CFG, encoding="utf-8") as f:
            cls.exp = yaml.safe_load(f)
        with open(RP_CFG, encoding="utf-8") as f:
            cls.rp = yaml.safe_load(f)
        with open(TRACE, encoding="utf-8", newline="") as f:
            cls.trace = list(csv.DictReader(f))
        summary = cls.reg.split("## 3. Register Summary", 1)[1].split("\n## ", 1)[0]
        cls.summary_rows = {}
        for line in summary.splitlines():
            m = re.match(r"^\| (D-\d\d) \|", line)
            if m:
                cls.summary_rows[m.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]

    # all D-01..D-16 exist with allowed statuses, details, mapping and traceability
    def test_all_decisions_registered(self):
        header = next(ln for ln in self.reg.splitlines() if ln.startswith("| Decision ID |"))
        self.assertEqual([c.strip() for c in header.strip("|").split("|")], SUMMARY_COLUMNS)
        self.assertEqual(list(self.summary_rows), IDS)
        for did, cells in self.summary_rows.items():
            self.assertEqual(len(cells), len(SUMMARY_COLUMNS), did)
            self.assertTrue(cells[2].startswith(STATUSES), (did, cells[2]))
            self.assertNotRegex(" ".join(cells), r"\bTBD\b", did)
            self.assertIsNotNone(re.search(rf"^### {did} — .+ · ({'|'.join(STATUSES)})", self.reg, flags=re.MULTILINE),
                                 did)
        mapping = self.reg.split("## 2. ID Mapping to Step 10C", 1)[1].split("\n## ", 1)[0]
        mapped = re.findall(r"^\| (D-\d\d) \|", mapping, flags=re.MULTILINE)
        self.assertEqual(mapped, IDS)
        step10c_ids = set(self.exp["decisions_required"])
        mapped_10c = set(re.findall(r"D-\d\d", " ".join(ln.split("|", 2)[2] for ln in mapping.splitlines()
                                                      if re.match(r"^\| D-\d\d \|", ln))))
        self.assertEqual(mapped_10c, step10c_ids)

    def test_traceability(self):
        with open(TRACE, encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), TRACE_COLUMNS)
        self.assertEqual([r["decision_id"] for r in self.trace], IDS)
        for r in self.trace:
            for col in TRACE_COLUMNS:
                self.assertTrue(r[col].strip(), (r["decision_id"], col))
            self.assertEqual(r["status"], self.summary_rows[r["decision_id"]][2].split(" (")[0], r["decision_id"])
            self.assertRegex(r["related_RQ"], r"RQ[1-6]")
            self.assertRegex(r["related_hypothesis"], r"H[1-5]")

    # pre-data freeze configuration: four categories; the only numbers are the approved alpha and power
    def test_freeze_config_has_no_values(self):
        self.assertEqual(self.freeze["freeze_categories"],
                         ["FROZEN NOW", "PILOT-DEPENDENT", "DEVICE-VERIFICATION DEPENDENT", "REQUIRES FUTURE APPROVAL"])
        for key in CATEGORY_KEYS:
            self.assertIn(key, self.freeze)
        self.assertNotIn("frozen", self.freeze)
        self.assertNotIn("not_frozen", self.freeze)
        numbers = []

        def walk(node, path=""):
            if isinstance(node, dict):
                for k, v in node.items():
                    walk(v, f"{path}.{k}")
            elif isinstance(node, list):
                for v in node:
                    walk(v, path)
            elif isinstance(node, (int, float)) and not isinstance(node, bool):
                numbers.append((path, node))
            elif isinstance(node, str):
                self.assertIsNone(re.search(r"\d+\.\d+|\d+\s*(%|ms|J|W|°C)", node), (path, node))
        for key in CATEGORY_KEYS:
            walk(self.freeze[key], key)
        self.assertEqual(numbers, [("frozen_now.D-02.alpha", 0.05), ("frozen_now.D-03.target_power", 0.8)])
        for key in ("pilot_dependent", "device_verification_dependent", "requires_future_approval"):
            for did, entry in self.freeze[key].items():
                self.assertNotIn("value", entry, did)
        for key in self.freeze["frozen_now"]:
            did = key.split("_")[0]
            self.assertIn(did, IDS, key)

    # D-02 / D-03: approved alpha, Holm, power; sample size not fabricated
    def test_alpha_and_power(self):
        d02 = self.freeze["frozen_now"]["D-02"]
        self.assertEqual(d02["alpha"], 0.05)
        self.assertEqual(d02["sidedness"], "two-sided")
        self.assertEqual(d02["multiple_comparison"], "Holm")
        self.assertEqual(d02["family"], ["H1", "H2", "H3", "H4", "H5"])
        self.assertIn("new pre-data-collection decision", d02["approval"])
        text = _section(self.reg, "### D-02")
        self.assertIn("This is a **newly approved pre-data-collection decision**. It is not an earlier project decision",
                      text)
        d03 = self.freeze["frozen_now"]["D-03"]
        self.assertEqual(d03["target_power"], 0.80)
        self.assertEqual(d03["sample_size"], "PILOT-DEPENDENT")
        self.assertFalse(d03["runs_treated_as_independent"])
        self.assertIn("D-03_sample_size", self.freeze["pilot_dependent"])
        d03_text = _section(self.reg, "### D-03")
        self.assertIn("| Required item count | **PILOT-DEPENDENT.**", d03_text)
        self.assertIn("No count is stated before the pilot.", d03_text)
        self.assertIsNone(re.search(r"\bn(_\w+)?\s*=\s*\d", self.reg))
        recon = self.reg.split("## 5. Statistical Plan Reconciliation", 1)[1].split("\n## ", 1)[0]
        for item in ("α = 0.05;", "two-sided tests;", "Holm correction over H1–H5;", "target power 0.80;",
                     "sample size PILOT-DEPENDENT (D-03);", "repeated observations clustered at item level (D-14);"):
            self.assertIn(item, recon)

    # no fabricated measurements / telemetry; numbers only as approved values or method constants
    def test_no_fabricated_numbers(self):
        self.assertIsNone(MEASURED_VALUE.search(self.reg), MEASURED_VALUE.search(self.reg))
        for line in self.reg.splitlines():
            for dec in re.findall(r"(?<![\w.])\d+\.\d+(?![\w.])", line):
                self.assertIn(dec, ALLOWED_DECIMALS, line[:80])
                self.assertIn(ALLOWED_DECIMALS[dec], line, line[:80])
        self.assertNotIn("PROPOSAL", self.reg)
        self.assertIn("**NO NUMERICAL VALUE IS JUSTIFIED BEFORE PILOT CHARACTERIZATION.**", self.reg)
        self.assertIn("No numerical value in this register is a measurement.", self.reg)
        # the Step 10A record is untouched; the freeze is recorded in Step 10C-DR files
        self.assertEqual(self.rp["statistics"]["significance_level"], "to_be_preregistered")

    # D-06: risk-controlled procedure, not C1 equivalence; no threshold value; test set unused
    def test_threshold_rule(self):
        d06 = self.freeze["frozen_now"]["D-06"]
        self.assertFalse(d06["uses_test_set"])
        self.assertFalse(d06["anchored_to_C1_equivalence"])
        self.assertEqual(d06["confidence"], "configuration_specific_temperature_scaling")
        self.assertIn("D-06_risk_target", self.freeze["requires_future_approval"])
        text = _section(self.reg, "### D-06")
        self.assertIn("The earlier rule (the smallest threshold whose accepted predictions are statistically as accurate "
                      "as C1) is **withdrawn**.", text)
        self.assertIn("**The numerical value of r* is UNSET (REQUIRES FUTURE APPROVAL).**", text)
        self.assertIn("**The final test set is never used for threshold selection.**", text)
        self.assertIn("**No numerical confidence threshold is stated in this register.**", text)
        self.assertIsNone(re.search(r"(r\*|τ\w*|threshold)\s*(=|≤|≥|<|>)\s*\d", self.reg))
        self.assertNotIn("≤ r₁", text)

    # D-12: inference and verification latency separate
    def test_latency_separation(self):
        d12 = self.freeze["frozen_now"]["D-12"]
        self.assertEqual(d12["separate_quantities"], ["inference_latency", "verification_latency", "total_decision_time"])
        self.assertFalse(d12["verification_forced_into_C1_inference_latency"])
        self.assertTrue(d12["verification_overhead_reported_separately"])
        self.assertFalse(d12["total_decision_budget_in_primary_design"])
        text = _section(self.reg, "### D-12")
        self.assertIn("**Verification is never forced to fit inside the C1 inference latency.**", text)
        for q in ("| A. Inference latency |", "| B. Verification latency |", "| C. Total per-item decision time |"):
            self.assertIn(q, text)
        props = __import__("json").loads(_text(EXP / "log_schema.json"))["properties"]
        self.assertIn("inference_latency", props)
        self.assertIn("verification_latency", props)

    # D-10: thermal API availability not assumed; no fabricated mapping
    def test_thermal_not_assumed(self):
        rule = self.freeze["frozen_now"]["D-10_rule"]
        self.assertFalse(rule["thermal_platform_api_assumed"])
        self.assertIn("D-10_thermal_source", self.freeze["device_verification_dependent"])
        self.assertIn("D-10_thermal_status_mapping", self.freeze["requires_future_approval"])
        text = _section(self.reg, "### D-10")
        self.assertIn("**Platform thermal-status API availability is NOT assumed.**", text)
        self.assertIn("**No thermal mapping is inserted in this register.**", text)
        self.assertIsNone(re.search(r"(NONE|LIGHT|MODERATE|SEVERE)\s*→\s*\d", self.reg))
        self.assertTrue(self.summary_rows["D-10"][2].startswith("DEVICE-VERIFICATION DEPENDENT"))

    # no C1-C4 identities, no R0-R3 thresholds fabricated
    def test_no_ladder_or_threshold_fabrication(self):
        self.assertEqual(self.freeze["frozen_now"]["D-04"]["ladder_identities"], "TO BE EMPIRICALLY DETERMINED")
        self.assertIn("**C1–C4 identities: TO BE EMPIRICALLY DETERMINED.**", self.reg)
        for fam in ("EfficientNet", "ConvNeXt", "MobileNet", "ResNet", "YOLO", "ViT"):
            self.assertNotIn(fam, self.reg)
        self.assertIn("D-10_thresholds", self.freeze["pilot_dependent"])
        self.assertIsNone(re.search(r"\bR[0-3]\b[^|\n]{0,40}(=|≥|>|<|≤)\s*\d", self.reg))
        self.assertEqual(self.freeze["frozen_now"]["D-10_rule"]["excluded_from_state"], ["latency", "accuracy", "confidence"])

    # test-set tuning prohibited; item-level split enforced
    def test_test_isolation_and_item_split(self):
        self.assertFalse(self.freeze["frozen_now"]["D-06"]["uses_test_set"])
        d06 = _section(self.reg, "### D-06")
        self.assertIn("The test manifest is never loaded by fitting code.", d06)
        self.assertIn("No fusion rule is chosen on test data.", _section(self.reg, "### D-08"))
        split = self.freeze["frozen_now"]["D-09_procedure"]
        self.assertEqual(split["unit"], "physical_item")
        self.assertIn("no_item_in_two_splits", split["leakage_checks"])
        self.assertIn("all_views_same_split", split["leakage_checks"])
        self.assertIn("Split by **physical item**", _section(self.reg, "### D-09"))

    # repeated runs are not independent; McNemar validity stated; refinement recorded
    def test_repeated_runs(self):
        d14 = self.freeze["frozen_now"]["D-14"]
        self.assertFalse(d14["runs_treated_as_independent"])
        self.assertEqual(d14["unit_accuracy"], "item_aggregated_across_runs")
        self.assertEqual(d14["ci"], "item_cluster_bootstrap")
        text = _section(self.reg, "### D-14")
        self.assertIn("**McNemar is retained exactly where valid:**", text)
        self.assertIn('**Recorded as:** "Step 10A method refined because of repeated/clustered design."', text)
        self.assertIn("Runs are never treated as independent observations.", _section(self.reg, "### D-03"))
        recon = self.reg.split("## 5. Statistical Plan Reconciliation", 1)[1].split("\n## ", 1)[0]
        for row in ("| RQ2 / H1 |", "| RQ3 / H2 |", "| RQ3 / H2.b |", "| RQ5 / H3 |", "| RQ4 / H4 |", "| RQ6 / H5 |",
                    "| RQ1 |", "| Multiplicity |"):
            line = next(ln for ln in recon.splitlines() if ln.startswith(row))
            self.assertTrue("Step 10A method refined because of repeated/clustered design" in line
                            or "Step 10A method retained" in line, row)
        # Step 10A hypotheses text untouched
        self.assertIn("Paired item-level McNemar test on correct/incorrect decisions",
                      _text(ROOT / "research" / "research_questions" / "hypotheses.md"))

    # Real-IAD views not physical recapture; OPPO platform; no multi-device claim
    def test_stage_and_platform_boundaries(self):
        d07 = _section(self.reg, "### D-07")
        a1 = next(ln for ln in d07.splitlines() if ln.startswith("| A1"))
        self.assertIn("**No: Real-IAD has no physical recapture**", a1)
        self.assertIn("Yes, as simulation", next(ln for ln in d07.splitlines() if ln.startswith("| A2")))
        self.assertEqual(self.freeze["frozen_now"]["D-16"]["experimental_platforms"], ["OPPO A5 2020 (3 GB RAM variant)"])
        self.assertEqual(self.freeze["frozen_now"]["D-16"]["multi_device_validation"], "future_work_not_in_scope")
        self.assertIn("which is not the research contribution", self.reg)
        self.assertNotRegex(self.reg.lower(), r"(validated|demonstrated) (across|on) (multiple|several|other) (devices|phones|smartphones)")
        self.assertEqual(self.exp["platform"]["additional_devices"], [])

    # B1-B5 unchanged, B5-F ablation, recovery preserved, precision safeguard
    def test_baselines_and_recovery_preserved(self):
        self.assertEqual(self.exp["baselines"], self.rp["baselines"])
        self.assertFalse(self.exp["ablation_variants"]["B5-F"]["primary_baseline"])
        self.assertEqual(self.exp["recovery"]["formula"], "(B5 - B3) / (B1 - B3)")
        self.assertEqual(self.rp["primary_rq"], RQ1)
        d15 = self.freeze["frozen_now"]["D-15"]
        self.assertEqual(d15["primary_recovery_metric"], "item_level_defect_recall")
        self.assertEqual(d15["h2_support_requires"], ["recall_recovery", "precision_non_inferiority_B5_vs_B3"])
        text = _section(self.reg, "### D-15")
        self.assertIn("**Preserved.** Recovery = (B5 − B3) / (B1 − B3)", text)
        self.assertIn("**Precision safeguard (pre-specified).**", text)
        self.assertIn("the outcome is classified as a **trade-off**, not recovery", text)
        self.assertEqual(self.freeze["unchanged"],
                         ["GC-03", "RQ1", "B1", "B2", "B3", "B4", "B5", "B5-F_ablation", "recovery_metric"])

    # energy: external reference preferred, fallback, no fabricated agreement threshold; network policy
    def test_energy_and_network(self):
        d16 = self.freeze["frozen_now"]["D-16"]
        self.assertTrue(d16["external_energy_validation_required"])
        self.assertEqual(d16["energy_reference_preferred"], "battery_side_external_reference")
        self.assertEqual(len(d16["energy_fallback_levels"]), 3)
        self.assertFalse(d16["absolute_energy_forced"])
        self.assertFalse(d16["software_counters_ground_truth"])
        self.assertNotIn("energy_tolerance", d16)
        self.assertEqual(self.freeze["requires_future_approval"]["D-16_agreement_threshold"]["status"],
                         "PRE-DATA-COLLECTION DECISION REQUIRED")
        self.assertEqual(d16["network"], "fully_offline_airplane_mode_wifi_bluetooth_data_off")
        self.assertEqual(d16["usb_during_battery_runs"], "disconnected")
        self.assertEqual(d16["inference"], "on_device_only")
        text = _section(self.reg, "### D-16")
        self.assertIn("No numeric tolerance is invented.", text)
        self.assertIn("**PRE-DATA-COLLECTION DECISION REQUIRED: the agreement threshold.**", text)
        self.assertIn("**No absolute energy is reported.**", text)
        self.assertIn("**Absolute energy is never forced**", text)
        self.assertIn("**USB is disconnected during battery-powered runs.**", text)
        self.assertIn("The OPPO A5 2020 (3 GB) is the **only current experimental device**.", text)

    # unresolved decisions clearly marked; blockers listed
    def test_unresolved_marked(self):
        for did, cells in self.summary_rows.items():
            if cells[2].startswith(("PILOT-DEPENDENT", "PRE-DATA-COLLECTION FREEZE", "DEVICE-VERIFICATION DEPENDENT")):
                open_keys = [k for cat in CATEGORY_KEYS[1:] for k in self.freeze[cat]]
                self.assertTrue(any(k.split("_")[0] == did for k in open_keys), did)
        section = self.reg.split("## 3a. Freeze Classification", 1)[1].split("\n## ", 1)[0]
        for cat in ("**FROZEN NOW**", "**PILOT-DEPENDENT**", "**DEVICE-VERIFICATION DEPENDENT**",
                    "**REQUIRES FUTURE APPROVAL**"):
            self.assertIn(f"| {cat}", section)
        self.assertIn("## 6. Remaining Blockers Before Step 10D", self.reg)
        self.assertIn("**No experiments, measurements, model benchmarking, dataset collection, or empirical results "
                      "were produced.**", self.reg)
        self.assertEqual(self.exp["decision_register"], "research/experiments/pre_data_collection_decision_register.md")


if __name__ == "__main__":
    unittest.main()
