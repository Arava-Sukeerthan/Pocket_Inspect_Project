"""
Step 10D researcher decisions (2026-10-07): backend capability scope, reference graph, delegation verification,
output validity, runtime provenance, camera manual-control tolerances (±5 %), D-16 E-1 safety gate and E-2 evidence.

End-to-end tests drive the real pipeline (run_characterization -> ADB parser -> bridge -> collectors -> validator ->
sign-off) with a synthetic ADB transport and synthetic app records. Synthetic values are test fixtures only;
nothing here is a device observation.
"""

import copy
import hashlib
import math
from pathlib import Path

import pytest
import yaml

from scripts.device_characterization import generate_reference_graph as gen
from src.monitoring.characterization import reference_graph as rg
from src.monitoring.characterization.collectors import (
    CameraCapabilityCollector,
    InferenceBackendCapabilityCollector,
    validate_backend_check_config,
)
from src.monitoring.characterization.coverage import check_matrix_coverage
from src.monitoring.characterization.energy_evidence import (
    select_energy_level,
    unmet_selection_requirements,
    validate_energy_evidence,
)
from src.monitoring.characterization.signoff import evaluate_d16_energy_level
from tests.test_device_characterization_correction_round import (
    BACKEND_SPECS,
    CONFIG,
    E1_COMPLETE,
    E2_COMPLETE,
    _level,
    backend_check,
    backend_runtime,
    backend_section,
    camera_records,
    expected_values,
    full_app,
    item,
    run_pipeline,
)

CFG = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
BACKEND_CFG = CFG["inference_backend_check"]
RULES = BACKEND_CFG["output_validation"]


def backend(data, name):
    return next(b for b in data["backends"] if b["backend"] == name)


def app_with(overrides):
    return full_app(backend_capability=backend_section(overrides))


# ---------------------------------------------------------------------------------------------------------------
# A. Backend scope
# ---------------------------------------------------------------------------------------------------------------

def test_backend_scope_is_the_approved_families_only():
    assert list(BACKEND_CFG["backends"]) == ["TFLite_CPU", "TFLite_GPU", "TFLite_NNAPI", "ONNXRuntime_CPU",
                                             "ONNXRuntime_NNAPI"]
    assert {s["runtime_family"] for s in BACKEND_CFG["backends"].values()} == {"LiteRT / TensorFlow Lite",
                                                                                "ONNX Runtime Mobile"}
    assert BACKEND_CFG["other_approved_runtimes"] == []


def test_app_probes_exactly_the_configured_backends():
    kt = Path("mobile/characterization/src/main/kotlin/org/pocketinspect/characterization/BackendProbes.kt"
              ).read_text(encoding="utf-8")
    for name, spec in BACKEND_CFG["backends"].items():
        assert f'Spec("{name}", "{spec["runtime_family"]}", "{spec["artifact_format"]}", "{spec["requested_delegate"]}")' in kt
    assert "executorch" not in kt.lower()


OTHER_ROW = "5/Other approved runtimes (e.g. ExecuTorch)"
SCOPE_ROWS = ["5/TFLite (LiteRT) CPU / XNNPACK", "5/TFLite GPU delegate", "5/TFLite NNAPI delegate",
              "5/ONNX Runtime Mobile CPU", "5/ONNX Runtime NNAPI EP"]


def _row(cov, rid):
    return next(r for r in cov["rows"] if r["row_id"] == rid)


def test_f02_other_runtimes_row_passes_only_with_complete_scope(tmp_path):
    """F-02: no other runtime approved; the row is satisfied exactly when every in-scope runtime row passes."""
    _, data, _ = run_pipeline(tmp_path, full_app())
    cov = check_matrix_coverage(data)
    assert all(_row(cov, rid)["passed"] for rid in SCOPE_ROWS)
    row = _row(cov, OTHER_ROW)
    assert row["passed"] is True and row["problem"] is None and row["records"] == []
    assert "F-02" in row["basis"] and row["failing_required_rows"] == []
    # No runtime or record was added for the row.
    assert {b["backend"] for b in data["backends"]} == set(BACKEND_SPECS)


@pytest.mark.parametrize("override", [
    ("TFLite_GPU", "fp32", dict(plan=None)),          # delegation unobservable -> NOT_TESTED
    ("ONNXRuntime_NNAPI", "fp32", dict(load_ok=False)),  # graph load ERROR
])
def test_f02_other_runtimes_row_fails_when_scope_incomplete(tmp_path, override):
    name, variant, kw = override
    _, data, _ = run_pipeline(tmp_path, app_with({(name, variant): backend_check(name, variant, **kw)}))
    row = _row(check_matrix_coverage(data), OTHER_ROW)
    assert row["passed"] is False and row["problem"] == "SCOPE_NOT_FULLY_CHARACTERIZED"
    assert row["failing_required_rows"]


def test_f02_other_runtimes_row_fails_without_backend_output(tmp_path):
    app = full_app()
    del app["backend_capability"]
    _, data, _ = run_pipeline(tmp_path, app)
    row = _row(check_matrix_coverage(data), OTHER_ROW)
    assert row["passed"] is False and set(row["failing_required_rows"]) == set(SCOPE_ROWS)


def test_f02_an_approved_extra_runtime_without_collector_fails(tmp_path, monkeypatch):
    from src.monitoring.characterization import coverage as cov_mod
    cfg = copy.deepcopy(CFG)
    cfg["inference_backend_check"]["other_approved_runtimes"] = ["ExecuTorch"]
    path = tmp_path / "cfg.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    _, data, _ = run_pipeline(tmp_path, full_app())
    monkeypatch.setattr(cov_mod, "CHARACTERIZATION_CONFIG_PATH", path)
    row = _row(check_matrix_coverage(data), OTHER_ROW)
    assert row["passed"] is False and row["problem"] == "NO_COLLECTOR"


def test_f02_scope_row_does_not_unblock_signoff_alone(tmp_path):
    from src.monitoring.characterization.signoff import evaluate_step10d_signoff
    _, data, _ = run_pipeline(tmp_path, full_app())
    s = evaluate_step10d_signoff(data)
    assert s["signoff_allowed"] is False      # GPU memory row, D-16 evidence and the human review gate remain


def test_f01_approved_tolerances_exact():
    assert RULES == {"float": {"max_abs_error": 0.01, "probability_sum_tolerance": 0.01},
                     "int8": {"output_scale": 0.00390625, "max_abs_error_lsb": 2, "probability_sum_tolerance_lsb": 4}}
    assert CFG["camera_manual_control_check"] == {"exposure_time_relative_tolerance": 0.05,
                                                  "sensitivity_relative_tolerance": 0.05}
    # The float rule applies to both fp32 and fp16; int8 uses the quantization-step rule.
    exp = rg.expected_output()
    off = [exp[0] + 0.0099, exp[1] - 0.0099] + exp[2:]
    for v in ("fp32", "fp16"):
        assert rg.validate_output({"shape": [1, 4], "values": off}, v, RULES)[0]
    assert not rg.validate_output({"shape": [1, 4], "values": off}, "int8", RULES)[0]


# ---------------------------------------------------------------------------------------------------------------
# B. Reference graph
# ---------------------------------------------------------------------------------------------------------------

def test_reference_graph_is_deterministic_and_pinned():
    first, second = rg.build_artifacts(), rg.build_artifacts()
    assert first == second
    assert gen.check() == []
    pinned = BACKEND_CFG["reference_graph"]["artifacts"]
    assert set(pinned) == {rg.artifact_name(f, v) for f in rg.FORMATS for v in rg.VARIANTS} | {rg.MANIFEST_NAME}
    assert all(pinned[k] == hashlib.sha256(v).hexdigest() for k, v in first.items())
    assert BACKEND_CFG["reference_graph"]["graph_id"] == rg.GRAPH_ID


def test_reference_graph_structure_and_expected_output():
    assert rg.OPERATORS == ("CONV_2D", "DEPTHWISE_CONV_2D", "AVERAGE_POOL_2D", "FULLY_CONNECTED", "SOFTMAX")
    assert rg.INPUT_SHAPE_NHWC == [1, 8, 8, 3] and rg.INPUT_SHAPE_NCHW == [1, 3, 8, 8] and rg.OUTPUT_SHAPE == [1, 4]
    exp = rg.expected_output()
    assert len(exp) == 4 and abs(sum(exp) - 1) < 1e-12 and all(0 < p < 1 for p in exp)
    # Every weight and input value is an exact float16 value, so the fp16 variant computes the same function.
    p = rg.parameters()
    for values in p.values():
        rg._f16_bytes(values)
    # The documented tolerance is below the smallest gap between expected class probabilities.
    gaps = [abs(a - b) for i, a in enumerate(exp) for b in exp[i + 1:]]
    assert RULES["float"]["max_abs_error"] < min(gaps)


def test_artifacts_carry_their_format_identity():
    arts = rg.build_artifacts()
    for v in rg.VARIANTS:
        assert arts[rg.artifact_name("tflite", v)][4:8] == b"TFL3"
        assert rg.GRAPH_ID.encode() in arts[rg.artifact_name("onnx", v)]
    manifest = __import__("json").loads(arts[rg.MANIFEST_NAME])
    assert manifest["expected_output"] == rg.expected_output()
    assert manifest["input"]["onnx"] == rg.nhwc_to_nchw(manifest["input"]["tflite"])
    assert manifest["graph_node_count"] == rg.graph_node_counts()


def test_no_model_binary_is_committed():
    import subprocess
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    assert not [f for f in files if f.endswith((".tflite", ".onnx"))]


# ---------------------------------------------------------------------------------------------------------------
# C/D. Delegation and output validity (end to end)
# ---------------------------------------------------------------------------------------------------------------

def test_all_stages_valid_end_to_end(tmp_path):
    out_dir, data, _ = run_pipeline(tmp_path, full_app())
    for name in BACKEND_SPECS:
        b = backend(data, name)
        for k in ("availability", "graph_load", "inference_execution", "probability_output", "delegation"):
            assert b[k]["state"] == "AVAILABLE", (name, k, b[k])
            assert b[k]["evidence_ref"].startswith("evidence/android_app_evidence.json#backend_capability/" + name)
        assert [r["metric"] for r in b["quantization_support"]] == ["quantization_fp16", "quantization_int8"]
        assert all(r["state"] == "AVAILABLE" for r in b["quantization_support"])
        art = b["reference_graph_artifacts"]["fp32"]
        assert art["match"] is True and b["reference_graph_hash"] == art["sha256_pinned"]
    # Distinct stages: availability is never the delegation record.
    gpu = backend(data, "TFLite_GPU")
    assert "delegation is verified separately" in gpu["availability"]["value"]
    assert gpu["delegation"]["verified"] is True and gpu["delegation_evidence"]["fp32"]["cpu_fallback"] is False


def test_runtime_unavailable(tmp_path):
    over = {("TFLite_GPU", "runtime"): backend_runtime("TFLite_GPU", "UNAVAILABLE")}
    over.update({("TFLite_GPU", v): backend_check("TFLite_GPU", v, state="NOT_TESTED") for v in ("fp32", "fp16", "int8")})
    _, data, _ = run_pipeline(tmp_path, app_with(over))
    b = backend(data, "TFLite_GPU")
    assert b["availability"]["state"] == "UNAVAILABLE" and b["availability"]["value"] is None
    for k in ("graph_load", "inference_execution", "probability_output", "delegation"):
        assert b[k]["state"] == "NOT_TESTED" and b[k]["verified"] is False
    assert b["runtime_version"] is None


def test_graph_load_failure(tmp_path):
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_NNAPI", "fp32"): backend_check("TFLite_NNAPI", "fp32", load_ok=False)}))
    b = backend(data, "TFLite_NNAPI")
    assert b["availability"]["state"] == "AVAILABLE"
    assert b["graph_load"]["state"] == "ERROR" and "Internal error" in b["graph_load"]["error_message"]
    for k in ("inference_execution", "probability_output", "delegation"):
        assert b[k]["state"] == "NOT_TESTED"


def test_inference_failure(tmp_path):
    _, data, _ = run_pipeline(tmp_path, app_with({("ONNXRuntime_CPU", "fp32"): backend_check("ONNXRuntime_CPU", "fp32", infer_ok=False)}))
    b = backend(data, "ONNXRuntime_CPU")
    assert b["graph_load"]["state"] == "AVAILABLE"
    assert b["inference_execution"]["state"] == "ERROR" and "invoke failed" in b["inference_execution"]["error_message"]
    assert b["probability_output"]["state"] == "NOT_TESTED"
    assert b["delegation"]["state"] == "NOT_TESTED"


@pytest.mark.parametrize("values, shape, why", [
    ([0.25, 0.25, 0.25, 0.25], None, "max abs error"),
    ([float("nan"), 0.3, 0.3, 0.4], None, "non-finite"),
    (None, [1, 5], "shape"),
    ([0.5, 0.2, 0.3, 0.33368361], None, "probability sum"),
])
def test_invalid_output_is_unavailable(tmp_path, values, shape, why):
    rec = backend_check("TFLite_CPU", "fp32", values=values, shape=shape)
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_CPU", "fp32"): rec}))
    p = backend(data, "TFLite_CPU")["probability_output"]
    assert p["state"] == "UNAVAILABLE" and p["value"] is None and p["verified"] is False
    assert "INVALID" in p["notes"] and why in p["notes"]


def test_missing_output_is_unavailable(tmp_path):
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_CPU", "fp32"): backend_check("TFLite_CPU", "fp32", output=False)}))
    p = backend(data, "TFLite_CPU")["probability_output"]
    assert p["state"] == "UNAVAILABLE" and "output missing" in p["notes"]


def test_delegate_requested_but_not_active(tmp_path):
    nodes = rg.graph_node_counts()["tflite"]["fp32"]
    over = {("TFLite_GPU", "fp32"): backend_check("TFLite_GPU", "fp32", plan=nodes),
            ("ONNXRuntime_NNAPI", "fp32"): backend_check("ONNXRuntime_NNAPI", "fp32", kernels=[
                {"node": "conv", "op": "Conv", "provider": "CPUExecutionProvider"}])}
    _, data, _ = run_pipeline(tmp_path, app_with(over))
    gpu, ort = backend(data, "TFLite_GPU"), backend(data, "ONNXRuntime_NNAPI")
    assert gpu["availability"]["state"] == "AVAILABLE"            # the runtime accepted the delegate ...
    assert gpu["delegation"]["state"] == "UNAVAILABLE"             # ... but no delegation was observed
    assert gpu["delegation_evidence"]["fp32"]["delegated"] is False
    assert ort["delegation"]["state"] == "UNAVAILABLE" and "CPUExecutionProvider" in ort["delegation"]["notes"]
    assert gpu["probability_output"]["state"] == "AVAILABLE"       # output validity is a separate stage


def test_delegate_verified_and_partial_fallback(tmp_path):
    kernels = [{"node": "nnapi_0", "op": "fused", "provider": "NnapiExecutionProvider"},
               {"node": "softmax", "op": "Softmax", "provider": "CPUExecutionProvider"}]
    over = {("TFLite_GPU", "fp32"): backend_check("TFLite_GPU", "fp32", plan=3),
            ("ONNXRuntime_NNAPI", "fp32"): backend_check("ONNXRuntime_NNAPI", "fp32", kernels=kernels)}
    _, data, _ = run_pipeline(tmp_path, app_with(over))
    gpu, ort = backend(data, "TFLite_GPU"), backend(data, "ONNXRuntime_NNAPI")
    assert gpu["delegation"]["state"] == "AVAILABLE" and gpu["delegation"]["verified"] is True
    assert gpu["delegation_evidence"]["fp32"]["cpu_fallback"] is None   # not distinguishable from the plan length
    assert ort["delegation"]["state"] == "AVAILABLE"
    ev = ort["delegation_evidence"]["fp32"]
    assert ev["cpu_fallback"] is True and ev["kernels_by_provider"] == {"NnapiExecutionProvider": 1,
                                                                       "CPUExecutionProvider": 1}
    assert ev["requested_delegate"] == "NnapiExecutionProvider" and ev["evidence_ref"]


def test_nnapi_delegation_is_never_verified(tmp_path):
    """The NNAPI accelerator identity is not observable through the Java APIs: AVAILABLE, never VERIFIED."""
    _, data, _ = run_pipeline(tmp_path, full_app())
    for name in ("TFLite_NNAPI", "ONNXRuntime_NNAPI"):
        d = backend(data, name)["delegation"]
        assert d["state"] == "AVAILABLE" and d["verified"] is False and d["report_status"] == "AVAILABLE"
        assert any("NNAPI accelerator identity" in x for x in backend(data, name)["known_limitations"])


def test_delegation_unobservable_is_not_tested(tmp_path):
    over = {("TFLite_GPU", "fp32"): backend_check("TFLite_GPU", "fp32", plan=None),
            ("ONNXRuntime_NNAPI", "fp32"): backend_check("ONNXRuntime_NNAPI", "fp32", kernels=[])}
    _, data, _ = run_pipeline(tmp_path, app_with(over))
    for name in ("TFLite_GPU", "ONNXRuntime_NNAPI"):
        d = backend(data, name)["delegation"]
        assert d["state"] == "NOT_TESTED" and d["report_status"] == "NOT YET VERIFIED"
        assert "not observable" in d["notes"]


def test_runtime_version_unavailable_is_null_not_invented(tmp_path):
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_CPU", "runtime"): backend_runtime("TFLite_CPU", version=None)}))
    b = backend(data, "TFLite_CPU")
    assert b["availability"]["state"] == "AVAILABLE" and b["runtime_version"] is None
    assert "version not reported" in b["availability"]["value"]
    assert any("Runtime version not reported" in x for x in b["known_limitations"])
    assert backend(data, "ONNXRuntime_CPU")["runtime_version"] == "1.30.0"


def test_artifact_hash_mismatch_is_error(tmp_path):
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_CPU", "fp32"): backend_check("TFLite_CPU", "fp32", sha="0" * 64)}))
    b = backend(data, "TFLite_CPU")
    assert b["graph_load"]["state"] == "ERROR" and "artifact identity mismatch" in b["graph_load"]["error_message"]
    assert b["probability_output"]["state"] == "NOT_TESTED" and b["reference_graph_hash"] is None
    assert b["reference_graph_artifacts"]["fp32"]["match"] is False


def test_requested_delegate_mismatch_is_error(tmp_path):
    rec = backend_check("TFLite_GPU", "fp32", requested_delegate="NNAPI")
    _, data, _ = run_pipeline(tmp_path, app_with({("TFLite_GPU", "fp32"): rec}))
    assert backend(data, "TFLite_GPU")["graph_load"]["state"] == "ERROR"


def test_quantization_variants_are_separate_checks(tmp_path):
    over = {("TFLite_NNAPI", "int8"): backend_check("TFLite_NNAPI", "int8", load_ok=False),
            ("ONNXRuntime_CPU", "fp16"): backend_check("ONNXRuntime_CPU", "fp16", values=[0.1, 0.2, 0.3, 0.4])}
    _, data, _ = run_pipeline(tmp_path, app_with(over))
    q = {r["metric"]: r for r in backend(data, "TFLite_NNAPI")["quantization_support"]}
    assert q["quantization_fp16"]["state"] == "AVAILABLE" and q["quantization_int8"]["state"] == "ERROR"
    assert backend(data, "TFLite_NNAPI")["probability_output"]["state"] == "AVAILABLE"
    q = {r["metric"]: r for r in backend(data, "ONNXRuntime_CPU")["quantization_support"]}
    assert q["quantization_fp16"]["state"] == "UNAVAILABLE" and q["quantization_int8"]["state"] == "AVAILABLE"


def test_validate_output_rule():
    exp = rg.expected_output()
    ok = lambda vals, v="fp32": rg.validate_output({"shape": [1, 4], "values": vals}, v, RULES)[0]  # noqa: E731
    assert ok(exp)
    tol = RULES["float"]["max_abs_error"]
    assert ok([exp[0] + 0.9 * tol, exp[1] - 0.9 * tol] + exp[2:])
    assert not ok([exp[0] + 1.1 * tol, exp[1] - 1.1 * tol] + exp[2:])
    # int8: compared in output quantization steps (LSB = 1/256), not with the float rule.
    lsb = RULES["int8"]["output_scale"]
    q = expected_values("int8")
    assert ok(q, "int8")
    assert ok([q[0] + 1 * lsb, q[1] - 1 * lsb] + q[2:], "int8")
    assert not ok([q[0] + 3 * lsb, q[1] - 3 * lsb] + q[2:], "int8")
    # 0.009 is inside the float rule (0.01) but outside the int8 rule (2 LSB = 0.0078): int8 is never judged by floats.
    between = [exp[0] + 0.009, exp[1] - 0.009] + exp[2:]
    assert ok(between, "fp32") and not ok(between, "int8")
    assert not ok([math.inf, 0, 0, 0])
    assert rg.validate_output(None, "fp32", RULES)[1] == ["output missing"]


def test_backend_check_config_is_validated():
    bad = copy.deepcopy(BACKEND_CFG)
    del bad["output_validation"]["float"]["max_abs_error"]
    with pytest.raises(ValueError):
        validate_backend_check_config(bad)
    bad = copy.deepcopy(BACKEND_CFG)
    bad["backends"]["TFLite_CPU"]["artifact_format"] = "pte"
    with pytest.raises(ValueError):
        InferenceBackendCapabilityCollector(bad)


def test_no_tolerance_or_pass_decision_in_the_app():
    kt = Path("mobile/characterization/src/main/kotlin/org/pocketinspect/characterization/BackendProbes.kt"
              ).read_text(encoding="utf-8")
    for token in ("max_abs_error", "probability_sum", "0.01", "tolerance"):
        assert token not in kt
    # No timing is read or recorded (profile durations are discarded; the TFLite timing API is not called).
    for token in ("getLastNativeInferenceDuration", '"dur"', "nanoTime() -", "elapsedRealtime"):
        assert token not in kt


# ---------------------------------------------------------------------------------------------------------------
# F. Camera manual-control tolerance
# ---------------------------------------------------------------------------------------------------------------

def _honoured_state(exp_tol, iso_tol, req_e, rep_e, req_i, rep_i):
    cam = CameraCapabilityCollector({"exposure_time_relative_tolerance": exp_tol, "sensitivity_relative_tolerance": iso_tol})
    props = {"is_real_device_observation": True, "app_output_status": "APP_OUTPUT_COLLECTED",
             "app_records": {"camera_id_list": item("camera_id_list", value=["0"])},
             "app_camera_records": {"0": {r["metric"]: r for r in camera_records("0", honoured=item(
                 "manual_control_honoured", value={"requested_exposure_time_ns": req_e, "reported_exposure_time_ns": rep_e,
                                                   "requested_sensitivity": req_i, "reported_sensitivity": rep_i}))}}}
    return cam.collect(props)[0].manual_control_honoured


def test_camera_tolerances_are_the_researcher_decision():
    check = CFG["camera_manual_control_check"]
    assert check == {"exposure_time_relative_tolerance": 0.05, "sensitivity_relative_tolerance": 0.05}
    kt = Path("mobile/characterization/src/main/kotlin/org/pocketinspect/characterization/CameraProbes.kt"
              ).read_text(encoding="utf-8")
    assert "0.05" not in kt and "tolerance" not in kt.lower()


def test_zero_tolerance_means_exact_equality():
    assert _honoured_state(0.0, 0.0, 1_000_000, 1_000_000, 400, 400).state == "AVAILABLE"
    assert _honoured_state(0.0, 0.0, 1_000_000, 1_000_001, 400, 400).state == "UNAVAILABLE"
    assert _honoured_state(0.0, 0.0, 1_000_000, 1_000_000, 400, 401).state == "UNAVAILABLE"


@pytest.mark.parametrize("rep_e, rep_i, state", [
    (1_050_000, 400, "AVAILABLE"),     # +5 % exposure
    (950_000, 400, "AVAILABLE"),       # -5 % exposure
    (1_000_000, 420, "AVAILABLE"),     # +5 % ISO
    (1_000_000, 380, "AVAILABLE"),     # -5 % ISO
    (1_050_000, 420, "AVAILABLE"),     # both at the limit
    (1_050_001, 400, "UNAVAILABLE"),   # exposure just above 5 %
    (949_999, 400, "UNAVAILABLE"),
    (1_000_000, 421, "UNAVAILABLE"),   # ISO above 5 %
    (1_000_000, 379, "UNAVAILABLE"),
    (2_000_000, 400, "UNAVAILABLE"),   # exposure far off, ISO fine: checked independently
    (1_000_000, 800, "UNAVAILABLE"),   # ISO far off, exposure fine
])
def test_five_percent_tolerance(rep_e, rep_i, state):
    t = CFG["camera_manual_control_check"]
    res = _honoured_state(t["exposure_time_relative_tolerance"], t["sensitivity_relative_tolerance"],
                          1_000_000, rep_e, 400, rep_i)
    assert res.state == state
    # Requested and reported values are preserved in the record.
    assert f"requested 1000000 ns, reported {rep_e} ns" in res.notes and f"reported {rep_i}" in res.notes
    if state == "UNAVAILABLE":
        assert "NOT HONOURED" in res.notes and res.value is None


def test_camera_id_and_facing_preserved_with_config_tolerance(tmp_path):
    honoured = item("manual_control_honoured", value={
        "requested_exposure_time_ns": 16666666, "reported_exposure_time_ns": 17000000,   # +2 %
        "requested_sensitivity": 850, "reported_sensitivity": 850, "frames_compared": 5})
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", "BACK", honoured=honoured)
    _, data, _ = run_pipeline(tmp_path, app)
    cam = data["camera"][0]
    assert cam["camera_id"] == "0" and cam["lens_facing"] == "BACK"
    assert cam["manual_control_honoured"]["state"] == "AVAILABLE"
    assert "16666666" in cam["manual_control_honoured"]["notes"] and "17000000" in cam["manual_control_honoured"]["notes"]


def test_manual_control_untestable_semantics_unchanged(tmp_path):
    app = full_app()
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + [
        r for r in camera_records("0") if r["metric"] != "manual_control_honoured"]
    _, data, _ = run_pipeline(tmp_path, app)
    assert data["camera"][0]["manual_control_honoured"]["state"] == "NOT_TESTED"
    perm = item("manual_control_honoured", "PERMISSION_REQUIRED", notes="CAMERA runtime permission not granted")
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", honoured=perm)
    _, data, _ = run_pipeline(tmp_path, app, run_suffix="170001")
    assert data["camera"][0]["manual_control_honoured"]["state"] == "PERMISSION_REQUIRED"
    failed = item("manual_control_honoured", "ERROR", error_message="IllegalStateException: openCamera failed")
    app["camera_telemetry"] = [item("camera_id_list", value=["0"])] + camera_records("0", honoured=failed)
    _, data, _ = run_pipeline(tmp_path, app, run_suffix="170002")
    assert data["camera"][0]["manual_control_honoured"]["state"] == "ERROR"


# ---------------------------------------------------------------------------------------------------------------
# G/H/I. D-16 energy
# ---------------------------------------------------------------------------------------------------------------

E1_OK = _level(feasible=True, validated=True, **E1_COMPLETE)
E2_OK = _level(feasible=True, validated=True, **E2_COMPLETE)


@pytest.mark.parametrize("field, value", [
    ("safety_signoff", False), ("reference_validated", False), ("assessed_by", None), ("assessed_on", None),
    ("instrument_model", None), ("evidence_files", []),
])
def test_e1_needs_every_requirement(field, value):
    e1 = dict(E1_OK, **{field: value})
    assert select_energy_level(e1, E2_OK, True) is None       # never E-1, and never falls through to E-2/E-3
    assert field in unmet_selection_requirements("E1_battery_side_reference", e1)
    assert select_energy_level(E1_OK, None, None) == "E-1"


def test_e1_validated_without_safety_signoff_is_an_invalid_file():
    data = {"E1_battery_side_reference": dict(E1_OK, safety_signoff=False),
            "E2_supply_powered_session": _level(assessed=False, non_charging_verified=False)}
    assert any("safety_signoff" in e for e in validate_energy_evidence(data))


@pytest.mark.parametrize("field, value", [
    ("non_charging_verified", False), ("non_charging_evidence_files", []), ("meter_model", None),
    ("reference_validated", False), ("assessed_by", None), ("evidence_files", []),
])
def test_e2_needs_every_requirement(field, value):
    e2 = dict(E2_OK, **{field: value})
    assert select_energy_level(_level(), e2, True) is None
    assert select_energy_level(_level(), E2_OK, True) == "E-2"


def test_e2_non_charging_requires_its_evidence_files():
    data = {"E1_battery_side_reference": _level(**dict(E1_COMPLETE, safety_signoff=False)),
            "E2_supply_powered_session": dict(E2_OK, non_charging_evidence_files=[])}
    assert any("non_charging_evidence_files" in e for e in validate_energy_evidence(data))


def test_e3_never_premature():
    assert select_energy_level(None, None, True) is None
    assert select_energy_level(_level(assessed=False), _level(), True) is None
    assert select_energy_level(_level(feasible=True), _level(), True) is None          # E-1 feasible, incomplete
    assert select_energy_level(_level(), _level(assessed=False), True) is None
    assert select_energy_level(_level(), _level(feasible=True), True) is None          # E-2 feasible, incomplete
    assert select_energy_level(_level(), _level(), True) == "E-3"
    assert select_energy_level(_level(), _level(), None) is None


def _write_energy(tmp_path, e1, e2):
    for f in ("photo.txt", "log.txt"):
        (tmp_path / f).write_text("researcher note", encoding="utf-8")
    e1 = {k: v for k, v in e1.items() if k not in ("non_charging_verified", "non_charging_evidence_files", "meter_model")}
    e2 = {k: v for k, v in e2.items() if k not in ("safety_signoff", "instrument_model")}
    for d in (e1, e2):
        d.setdefault("notes", None)
    e1.setdefault("safety_signoff", False)
    e2.setdefault("non_charging_verified", False)
    path = tmp_path / "energy.yaml"
    path.write_text(yaml.safe_dump({"E1_battery_side_reference": e1, "E2_supply_powered_session": e2}), encoding="utf-8")
    return path


def test_e1_selected_end_to_end_only_with_safety_signoff(tmp_path):
    e2 = _level(assessed=False)
    path = _write_energy(tmp_path, dict(E1_OK, safety_signoff=False, reference_validated=False), e2)
    _, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(path)})
    energy = data["energy"]
    assert energy["selected_level"] is None and energy["absolute_energy_claimed"] is False
    assert "safety_signoff" in energy["selection_basis"]["E1_battery_side_reference"]["unmet_selection_requirements"]
    assert "safety_signoff" in energy["E1_battery_side_reference"]["notes"]

    path = _write_energy(tmp_path, dict(E1_OK), e2)
    out_dir, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(path)},
                                    run_suffix="170001")
    assert data["energy"]["selected_level"] == "E-1" and data["energy"]["absolute_energy_claimed"] is False
    assert evaluate_d16_energy_level(data)["passed"] is True


def test_e2_selected_end_to_end_with_non_charging_evidence(tmp_path):
    path = _write_energy(tmp_path, _level(**dict(E1_COMPLETE, safety_signoff=False)), dict(E2_OK))
    out_dir, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(path)})
    assert data["energy"]["selected_level"] == "E-2"
    assert (out_dir / "evidence" / "energy_feasibility_log.txt").exists()   # non-charging log copied and hashed
    assert data["energy"]["absolute_energy_claimed"] is False


def test_signoff_rejects_forged_selection(tmp_path):
    path = _write_energy(tmp_path, dict(E1_OK, safety_signoff=False, reference_validated=False), _level(assessed=False))
    _, data, _ = run_pipeline(tmp_path, full_app(), cfg_overrides={"energy_feasibility_evidence": str(path)})
    forged = copy.deepcopy(data)
    forged["energy"]["selected_level"] = "E-1"
    d16 = evaluate_d16_energy_level(forged)
    assert d16["passed"] is False and any("unmet requirements" in p for p in d16["problems"])
    forged["energy"]["selected_level"] = "E-2"
    assert evaluate_d16_energy_level(forged)["passed"] is False
    del forged["energy"]["selection_basis"]
    assert any("selection basis" in p for p in evaluate_d16_energy_level(forged)["problems"])


def test_energy_template_unfilled_and_documents_the_gates():
    text = Path("configs/energy_feasibility_evidence_template.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    assert validate_energy_evidence(data) == []
    assert data["E2_supply_powered_session"]["non_charging_evidence_files"] == []
    assert all(data[k]["assessed"] is False for k in data)
    assert "safety_signoff" in text and select_energy_level(data["E1_battery_side_reference"],
                                                            data["E2_supply_powered_session"], True) is None
    assert CFG["energy_feasibility_evidence"] is None


# ---------------------------------------------------------------------------------------------------------------
# Status / provenance
# ---------------------------------------------------------------------------------------------------------------

def test_dry_run_has_no_verified_backend_or_camera_claim(tmp_path):
    from scripts.device_characterization.run_characterization import run_characterization
    import json
    import datetime
    run_id = f"run_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d')}_000000"
    out_dir, _ = run_characterization(CONFIG, run_id=run_id, dry_run=True, results_dir=tmp_path)
    data = json.loads((out_dir / "characterization.json").read_text(encoding="utf-8"))
    for b in data["backends"]:
        for k in ("availability", "graph_load", "inference_execution", "probability_output", "delegation"):
            assert b[k]["verified"] is False and b[k]["state"] == "NOT_TESTED"
    assert data["energy"]["selected_level"] is None


def test_app_and_host_evidence_stay_distinguishable(tmp_path):
    _, data, _ = run_pipeline(tmp_path, full_app())
    for b in data["backends"]:
        for k in ("availability", "graph_load", "inference_execution", "probability_output", "delegation"):
            assert b[k]["evidence_ref"].startswith("evidence/android_app_evidence.json#")
