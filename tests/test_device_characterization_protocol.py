"""
Step 10D tests: device-characterization specification and Antigravity handoff.

The specification must keep the OPPO A5 2020 (3 GB) as the experimental
platform, assume no device capability, separate status from value (no fake
zeros), record no device observation or experimental result, keep C1-C4 and
R0-R3 thresholds open, and define the Claude Code / Antigravity roles and the
CHANGELOG synchronization cycle.
"""
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "research" / "experiments"
PROTOCOL = EXP / "device_characterization_protocol.md"
MATRIX = EXP / "device_capability_matrix.md"
SCHEMA = EXP / "device_characterization_schema.json"
HANDOFF = ROOT / "docs" / "architecture" / "step10d_device_characterization_handoff.md"
EXP_CFG = ROOT / "configs" / "experiment_protocol.yaml"
FREEZE = ROOT / "configs" / "pre_data_collection.yaml"

COMPONENTS = [
    "DeviceIdentityCollector", "AndroidCapabilityCollector", "BatteryTelemetryCollector",
    "MemoryTelemetryCollector", "CPUTelemetryCollector", "GPUTelemetryCollector", "ThermalTelemetryCollector",
    "CameraCapabilityCollector", "InferenceBackendCapabilityCollector", "ProfilingCapabilityCollector",
    "EnergyMeasurementCapabilityChecker", "CharacterizationReportGenerator",
]
RUNTIME_STATES = ["AVAILABLE", "UNAVAILABLE", "PERMISSION_REQUIRED", "API_UNSUPPORTED", "EXTERNAL_REQUIRED",
                  "NOT_TESTED", "ERROR"]
REPORT_STATUSES = ["VERIFIED", "AVAILABLE", "CONDITIONALLY AVAILABLE", "UNAVAILABLE",
                   "REQUIRES EXTERNAL INSTRUMENTATION", "REQUIRES PILOT VALIDATION", "NOT YET VERIFIED"]
SCHEMA_DEFS = ["device_identity", "capability_result", "telemetry_capability", "camera_capability",
               "backend_capability", "thermal_capability", "energy_capability", "characterization_run"]
# A number with a performance / measurement unit, or a metric assigned a number, would be fabricated.
MEASURED = re.compile(
    r"\d+(\.\d+)?\s*(ms\b|seconds?\b|fps\b|FPS\b|mJ\b|J\b|mWh\b|Wh\b|mW\b|W\b|°\s*C|%|MHz\b|GHz\b|kHz\b|mA\b|µA\b|"
    r"uA\b|mV\b|MB\b|MiB\b)"
    r"|(accuracy|recall|precision|latency|energy|temperature|utili[sz]ation|frequency)\s*(=|:|of|≈|~)\s*\d"
)


def _text(path):
    return path.read_text(encoding="utf-8")


def _section(text, start, end="\n## "):
    return text.split(start, 1)[1].split(end, 1)[0]


def _check_capability_result(schema, record):
    """Minimal structural validator for capability_result (no external dependency)."""
    spec = schema["$defs"]["capability_result"]
    errors = []
    for key in spec["required"]:
        if key not in record:
            errors.append(f"missing {key}")
    if set(record) - set(spec["properties"]):
        errors.append("unexpected keys")
    if record.get("state") not in RUNTIME_STATES:
        errors.append("bad state")
    if record.get("state") != "AVAILABLE":
        if record.get("value") is not None:
            errors.append("non-available state with a value")
        if record.get("verified"):
            errors.append("non-available state marked verified")
    if record.get("verified") and not (record.get("evidence_ref") and record.get("observed_at")):
        errors.append("verified without evidence")
    if record.get("report_status") == "VERIFIED" and not record.get("verified"):
        errors.append("VERIFIED report status without verified flag")
    return errors


class TestDeviceCharacterizationSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.protocol = _text(PROTOCOL)
        cls.matrix = _text(MATRIX)
        cls.handoff = _text(HANDOFF)
        cls.schema = json.loads(_text(SCHEMA))
        with open(EXP_CFG, encoding="utf-8") as f:
            cls.exp = yaml.safe_load(f)
        with open(FREEZE, encoding="utf-8") as f:
            cls.freeze = yaml.safe_load(f)
        cls.docs = {"protocol": cls.protocol, "matrix": cls.matrix, "handoff": cls.handoff}

    # OPPO A5 2020 3 GB is the platform; 4/6 GB not substituted
    def test_platform_and_variant(self):
        self.assertEqual((self.exp["platform"]["model"], self.exp["platform"]["ram_variant"]), ("OPPO A5 2020", "3 GB"))
        spec = self.schema["$defs"]["known_specification"]["properties"]
        self.assertEqual(spec["ram_variant"]["const"], "3 GB")
        self.assertEqual(spec["excluded_variants"]["const"], ["4 GB", "6 GB"])
        self.assertIn("**The experimental device is the 3 GB RAM variant only.**", self.protocol)
        self.assertIn("**Device: OPPO A5 2020, 3 GB RAM variant (experimental platform).**", self.matrix)
        for name, text in self.docs.items():
            for m in re.finditer(r"[46] GB", text):
                window = text[max(0, m.start() - 120):m.end() + 120].lower()
                self.assertTrue("not" in window or "exclud" in window or "never" in window, (name, window))

    # methodology device-independent; OPPO is not the contribution
    def test_device_independent(self):
        self.assertIn("The OPPO A5 2020 is the experimental platform, not the research contribution.", self.protocol)
        self.assertIn("The characterization procedure is written device-independently", self.protocol)
        procedure = _section(self.protocol, "## 4. Characterization Procedure (device-independent)")
        self.assertNotIn("OPPO", procedure)
        self.assertIn("**Methodology stays device-independent.**", self.handoff)
        self.assertFalse(self.exp["positioning"]["experimental_platform_is_contribution"])

    # no fake telemetry values; explicit unavailable states; schema enforces null values
    def test_no_fake_values(self):
        defs = self.schema["$defs"]
        for name in SCHEMA_DEFS:
            self.assertIn(name, defs, name)
        self.assertEqual(defs["runtime_state"]["enum"], RUNTIME_STATES)
        self.assertEqual(defs["report_status"]["enum"], REPORT_STATUSES)
        rule = defs["capability_result"]["allOf"][0]
        self.assertEqual(sorted(rule["if"]["properties"]["state"]["enum"]),
                         sorted(s for s in RUNTIME_STATES if s != "AVAILABLE"))
        self.assertEqual(rule["then"]["properties"]["value"], {"type": "null"})
        fake_zero = {"metric": "gpu_utilization", "state": "UNAVAILABLE", "report_status": "UNAVAILABLE", "value": 0,
                     "unit": "percent", "source": "kgsl sysfs", "verified": False, "verification_method": "read"}
        self.assertIn("non-available state with a value", _check_capability_result(self.schema, fake_zero))
        explicit = dict(fake_zero, value=None)
        self.assertEqual(_check_capability_result(self.schema, explicit), [])
        unverified = dict(explicit, state="AVAILABLE", report_status="VERIFIED", value=None, verified=True)
        self.assertIn("verified without evidence", _check_capability_result(self.schema, unverified))
        self.assertIn("GPU utilisation unavailable is **not** \"GPU utilisation = 0\"", self.protocol)
        self.assertIn("**No fake zeros.**", self.handoff)
        negative_example = 'GPU utilisation unavailable is **not** "GPU utilisation = 0"'
        for name, text in self.docs.items():
            text = text.replace(negative_example, "")
            self.assertIsNone(MEASURED.search(text), (name, MEASURED.search(text)))
        json_text = _text(SCHEMA)
        self.assertNotIn('"examples"', json_text)
        self.assertNotIn('"default"', json_text)

    # nothing observed yet: every device row NOT YET VERIFIED; no VERIFIED claim
    def test_no_device_observation_claimed(self):
        status_cells = []
        for line in self.matrix.splitlines():
            if line.startswith("| ") and not line.startswith(("| Item", "| Dimension", "| Backend", "| Variable",
                                                              "| Aspect", "| Level", "| :--")):
                status_cells.append(line)
        self.assertTrue(status_cells)
        for line in status_cells:
            self.assertNotRegex(line, r"\|\s*VERIFIED\s*\|", line[:60])
        self.assertGreaterEqual(self.matrix.count("NOT YET VERIFIED"), 50)
        self.assertIn("**Nothing in this handoff is a device observation.**", self.handoff)
        self.assertIn("No code has been run on the device, and no device observation exists.", self.protocol)

    # Android version and API 29 thermal status not assumed
    def test_android_and_thermal_not_assumed(self):
        api = _section(self.protocol, "### 5.1 Android / API", "\n### ")
        self.assertIn("**The installed version is NOT assumed.**", api)
        self.assertIn("**API_UNSUPPORTED**", api)
        self.assertIn("NOT YET VERIFIED (**not assumed**)", self.matrix)
        self.assertIn("NOT YET VERIFIED (launch version Android 9; installed version **not assumed**)", self.matrix)
        self.assertIn("**minSdk must not exceed 28.**", self.handoff)
        self.assertIn("**Every API ≥ 29 call** is guarded by `Build.VERSION.SDK_INT`.", self.handoff)
        thermal_enum = self.schema["$defs"]["thermal_capability"]["properties"]["selected_thermal_source"]["enum"]
        self.assertIn("fallback_temperature_and_frequency_capping", thermal_enum)
        self.assertFalse(self.freeze["frozen_now"]["D-10_rule"]["thermal_platform_api_assumed"])

    # temperature measurement vs throttling state; no zone assumed to be SoC
    def test_thermal_separation(self):
        self.assertIn("**Temperature measurement** and **thermal throttling state** are characterised separately",
                      self.protocol)
        self.assertIn("Surface temperature is never converted into SoC temperature without validation.", self.protocol)
        self.assertIn("**no zone assumed to be SoC**", self.matrix)
        props = self.schema["$defs"]["thermal_capability"]["properties"]
        self.assertIn("temperature_sources", props)
        self.assertIn("thermal_status_api", props)
        self.assertIn("frequency_capping_observable", props)

    # C1-C4 open; R0-R3 thresholds pilot-dependent
    def test_ladder_and_thresholds_open(self):
        for text in (self.protocol, self.matrix):
            self.assertIn("TO BE EMPIRICALLY DETERMINED", text)
        self.assertIn("**R0–R3 thresholds remain PILOT-DEPENDENT.**", self.protocol)
        self.assertIn("**R0–R3 thresholds: PILOT-DEPENDENT.**", self.matrix)
        self.assertEqual(self.exp["methodology"]["ladder_identities"], "to_be_empirically_determined")
        for fam in ("EfficientNet", "ConvNeXt", "MobileNet", "ResNet", "YOLO"):
            for name, text in self.docs.items():
                self.assertNotIn(fam, text, (name, fam))

    # energy not claimed validated; D-16 hierarchy intact
    def test_energy_not_validated(self):
        energy = self.schema["$defs"]["energy_capability"]["properties"]
        self.assertEqual(energy["absolute_energy_claimed"], {"const": False})
        self.assertEqual(energy["selected_level"]["enum"], ["E-1", "E-2", "E-3", None])
        section = _section(self.protocol, "## 6. Energy-Measurement Feasibility (D-16 hierarchy unchanged)")
        self.assertIn("Absolute energy is **not claimed** until a level is validated.", section)
        self.assertIn("No energy accuracy value is invented.", section)
        for level in ("E-1", "E-2", "E-3"):
            self.assertIn(f"| {level} ", section)
        self.assertEqual(self.freeze["frozen_now"]["D-16"]["energy_fallback_levels"][0], "E-1_battery_side_reference")

    # camera manual controls not assumed
    def test_camera_not_assumed(self):
        self.assertIn("**Manual control is not claimed unless the advertised-vs-honoured check passes.**", self.protocol)
        self.assertIn("NOT YET VERIFIED (**manual control not assumed**)", self.matrix)
        self.assertIn("manual_control_honoured", self.schema["$defs"]["camera_capability"]["required"])

    # no experimental accuracy / latency / energy / thermal results
    def test_no_experimental_results(self):
        backend = self.schema["$defs"]["backend_capability"]["properties"]
        for forbidden in ("latency", "accuracy", "throughput", "energy"):
            self.assertFalse(any(forbidden in k for k in backend), forbidden)
        self.assertEqual(self.schema["$defs"]["characterization_run"]["properties"]["performance_results"],
                         {"const": None, "description": "Step 10D records no performance results"})
        self.assertIn("**No latency is recorded or reported.**", self.protocol)
        self.assertIn("No latency is recorded in this matrix.", self.matrix)
        self.assertFalse((ROOT / "research" / "results" / "device_characterization").exists())
        self.assertEqual(sorted(p.name for p in (ROOT / "mobile").iterdir()), ["README.md"])

    # roles, components, synchronization cycle
    def test_roles_and_handoff(self):
        roles = self.handoff.split("Protocol:", 1)[0]
        self.assertIn("| **Implementation agent** | **Antigravity** |", roles)
        self.assertIn("| **Review/specification agent** | **Claude Code** |", roles)
        self.assertIn("**Claude Code does not silently replace Antigravity's implementation.**", roles)
        components = _section(self.handoff, "## 4. Components")
        for i, comp in enumerate(COMPONENTS, start=1):
            self.assertIn(f"| {i} | **{comp}** |", components)
        sync = _section(self.handoff, "## 8. CHANGELOG Synchronization Policy")
        self.assertIn("IMPLEMENT → CHANGELOG → CLAUDE REVIEW → CHANGELOG → ANTIGRAVITY CORRECTION → CHANGELOG → TEST → "
                      "NEXT STAGE", sync)
        for item in ("implementation changes", "files changed", "tests run and results", "limitations",
                     "unresolved issues", "commit hash"):
            self.assertIn(item, sync)
        self.assertIn("narrow each guard to an explicit Step 10D allow-list", self.handoff)
        changelog = _text(ROOT / "docs" / "agent_sync" / "CHANGELOG.md")
        last = changelog.rsplit("\n## ", 1)[1]
        self.assertTrue(last.startswith("2026-10-05 — Claude Code"))
        self.assertIn("Step 10D", last)
        self.assertIn("Antigravity", last)


if __name__ == "__main__":
    unittest.main()
