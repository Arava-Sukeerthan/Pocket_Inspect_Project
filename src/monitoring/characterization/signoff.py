"""
Step 10D sign-off evaluation (protocol §9).

§9 criteria:
1. every item in device_capability_matrix.md has a non-default status with evidence  -> coverage.py
2. the variant check confirms the 3 GB unit                                         -> evaluate_variant_signoff (R-08)
3. the D-10 thermal source and the D-16 energy level are decided from evidence      -> this module
4. Claude Code has recorded a review entry with no open blocking findings           -> HUMAN/REVIEW GATE

Criterion 4 is a review act, not a software check. Software never marks it satisfied: `review_confirmed` must be
passed explicitly by whoever records the review, and defaults to False. So `signoff_allowed` is False whenever
the review gate is open, even if every automated criterion passes.
"""

from typing import Any, Dict, Optional

from src.monitoring.characterization.coverage import check_matrix_coverage

_UNSUPPORTED = ("API_UNSUPPORTED", "UNAVAILABLE")


def _has_evidence(rec: Optional[Dict[str, Any]], state: Optional[str] = "AVAILABLE") -> bool:
    return bool(isinstance(rec, dict) and (state is None or rec.get("state") == state) and rec.get("evidence_ref"))


def evaluate_d10_thermal_source(run: Dict[str, Any]) -> Dict[str, Any]:
    """D-10: the selected thermal source must be supported by the run's evidence."""
    thermal = run.get("thermal") or {}
    selected = thermal.get("selected_thermal_source")
    status_api = thermal.get("thermal_status_api")
    sources = thermal.get("temperature_sources") or []
    capping = thermal.get("frequency_capping_observable")
    if selected == "platform_thermal_status":
        ok = _has_evidence(status_api)
        reason = ("thermal_status_api AVAILABLE with evidence" if ok
                  else "platform_thermal_status selected but thermal_status_api is not AVAILABLE with evidence")
    elif selected == "fallback_temperature_and_frequency_capping":
        api_ok = isinstance(status_api, dict) and status_api.get("state") in _UNSUPPORTED and status_api.get("evidence_ref")
        temp_ok = any(_has_evidence(r) for r in sources)
        cap_ok = _has_evidence(capping)
        ok = bool(api_ok and temp_ok and cap_ok)
        reason = (f"fallback: status API unsupported with evidence={bool(api_ok)}, temperature source with "
                  f"evidence={temp_ok}, frequency-capping observability with evidence={cap_ok}")
    else:
        ok = False
        reason = "no thermal source selected"
    return {"passed": ok, "selected_thermal_source": selected, "reason": reason,
            "note": "Mapping of platform thermal-status levels to L_thermal remains REQUIRES FUTURE APPROVAL (D-10)."}


def evaluate_d16_energy_level(run: Dict[str, Any]) -> Dict[str, Any]:
    """D-16: a level is decided from evidence without skipping a preferred, unassessed level."""
    energy = run.get("energy") or {}
    level = energy.get("selected_level")
    e1, e2, e3 = (energy.get(k) or {} for k in ("E1_battery_side_reference", "E2_supply_powered_session",
                                                 "E3_software_counters"))
    assessed = lambda r: r.get("state") == "EXTERNAL_REQUIRED" and bool(r.get("evidence_ref"))  # noqa: E731
    problems = []
    if energy.get("absolute_energy_claimed") is not False:
        problems.append("absolute energy must not be claimed")
    if level is None:
        problems.append("no energy level selected (E-1/E-2 evidence not yet established)")
    elif level == "E-1":
        if not assessed(e1):
            problems.append("E-1 selected without researcher E-1 evidence")
    elif level == "E-2":
        if not (assessed(e1) and assessed(e2)):
            problems.append("E-2 selected without researcher E-1 and E-2 evidence")
    elif level == "E-3":
        if not (assessed(e1) and assessed(e2)):
            problems.append("E-3 selected while a preferred level is unassessed")
        if e3.get("state") != "AVAILABLE":
            problems.append("E-3 selected without demonstrated software counters")
    else:
        problems.append(f"unknown energy level {level!r}")
    return {"passed": not problems, "selected_level": level, "problems": problems,
            "note": "The D-16 agreement threshold remains a pre-data-collection decision; no absolute energy is claimed."}


def evaluate_step10d_signoff(run: Dict[str, Any], coverage: Optional[Dict[str, Any]] = None,
                             review_confirmed: bool = False) -> Dict[str, Any]:
    """Full §9 evaluation for one run. `review_confirmed` is never set by the characterization software."""
    from src.monitoring.characterization.report_generator import evaluate_variant_signoff

    cov = coverage if coverage is not None else check_matrix_coverage(run)
    variant = evaluate_variant_signoff(run)
    d10 = evaluate_d10_thermal_source(run)
    d16 = evaluate_d16_energy_level(run)
    automated = {
        "criterion_1_matrix_coverage": {"passed": cov["passed"], "rows_failed": cov["rows_failed"],
                                        "rows_total": cov["rows_total"]},
        "criterion_2_variant_check": {"passed": variant["signoff_allowed"], "reason": variant["reason"]},
        "criterion_3_d10_thermal_source": d10,
        "criterion_3_d16_energy_level": d16,
    }
    automated_ok = all(c["passed"] for c in automated.values())
    review = {
        "passed": bool(review_confirmed),
        "status": "CONFIRMED" if review_confirmed else "PENDING_HUMAN_REVIEW",
        "requirement": "Claude Code review entry with no open blocking findings (protocol §9 criterion 4); "
                       "recorded by a reviewer, never inferred by software.",
    }
    return {
        "criteria": {**automated, "criterion_4_review_gate": review},
        "automated_criteria_passed": automated_ok,
        "signoff_allowed": automated_ok and bool(review_confirmed),
    }
