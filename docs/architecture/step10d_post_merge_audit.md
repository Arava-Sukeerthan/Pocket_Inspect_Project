# Step 10D — Post-Merge Independent Audit (PR #20, commit `050bb6d`)

_2026-10-05, Claude Code (research review agent)._

**This is a post-merge audit.** PR #20 was implemented by Antigravity and merged into `main` (`e9ffade`) **before** this independent review. It was not reviewed before merge.

Audited against the authoritative documents:
- [`device_characterization_protocol.md`](../../research/experiments/device_characterization_protocol.md)
- [`device_capability_matrix.md`](../../research/experiments/device_capability_matrix.md)
- [`device_characterization_schema.json`](../../research/experiments/device_characterization_schema.json)
- [`step10d_device_characterization_handoff.md`](step10d_device_characterization_handoff.md)
- the pre-data-collection decision register (D-10, D-16)

What was inspected:
- the actual code;
- both run JSON files;
- the tests (re-run);
- the Antigravity CHANGELOG entry.

## Final decision

**REJECT — MAJOR IMPLEMENTATION/PROTOCOL FAILURE**

**The primary Step 10D deliverable, characterization of the physical OPPO A5 2020 (3 GB), was not produced.**

- Both run files contain **no device observation**: 0 non-null values, 0 verified results, 0 evidence references, 0 observation timestamps, and `adb_connected: false`.
- The two runs were made **25 seconds apart on the same date**. They are not two runs on separate days.
- The files label 47 untested items as UNAVAILABLE device capabilities. They also mark the thermal APIs API_UNSUPPORTED from an **assumed** API level 28, and select the D-10 thermal source without evidence.
- The collector design can mark mock input as VERIFIED, with evidence references to files that do not exist.

Several elements are correct (§4), but the evidence base must be regenerated on the device after the corrections.

## 1. What was actually verified in this audit

| Check | Result | Evidence |
| :-- | :-- | :-- |
| Commit and merge | `050bb6d` (2026-10-05 14:59 +0530, i.e. 09:29 UTC) merged by `e9ffade` | `git show --stat 050bb6d` |
| Run files exist | One `characterization.json` per run directory. **No `evidence/` directory, no raw evidence files.** | `ls -R research/results/device_characterization` |
| Schema validity | Both files: 0 JSON-Schema errors | `jsonschema` Draft 2020-12 validation |
| Device observations | **None** in either run: 59 capability records each. 47 UNAVAILABLE, 2 API_UNSUPPORTED, 6 NOT_TESTED, 1 PERMISSION_REQUIRED, 3 EXTERNAL_REQUIRED. 0 non-null values, 0 verified, 0 `evidence_ref`, 0 `observed_at`. | Record tally of both files |
| Run conditions | `adb_connected: false`, `usb_connected: false` in both runs | `conditions` field |
| Run timing | `started_at` = `2026-10-05T09:02:41Z` (repeat 1) and `2026-10-05T09:03:06Z` (repeat 2). The directory name `run_20261006_100000` does not match the recorded start time. | `started_at` fields |
| Run independence | The two files differ **only** in `run_id`, `started_at` and `repeat_index` | `diff` of the pretty-printed JSON |
| Test suite | `python -m pytest -q`: **277 passed** (reproduced) | Local run |
| Boundaries | No C1–C4, R0–R3 threshold, r*, energy-agreement threshold, binning or time-budget decision introduced. Protocol, decision-register and research-question files unchanged (`git diff 24aa0f0 e9ffade` empty for those paths). | grep and diff |
| Capability matrix | `device_capability_matrix.md` **not updated** (acceptance criterion 4) | Not in the commit file list |

**Device facts verified by this audit: none.** The OPPO A5 2020 identity, the 3 GB variant, Android version, API level, ABI, CPU topology and memory are all **NOT VERIFIED**. The only identity information in the runs is the copied `known_specification`, which is not an observation.

## 2. Compliance table

| Requirement | Status | Evidence | Finding |
| :-- | :-- | :-- | :-- |
| Actual OPPO A5 2020 characterization | **FAIL** | `adb_connected: false`; no observed values | F-01 |
| 3 GB variant verification | **FAIL** | `total_ram_mb` UNAVAILABLE; no variant-check record | F-01, F-08 |
| Two separate runs (separate days, reboot) | **FAIL** | Starts 25 s apart on the same date; identical content | F-02 |
| Non-invasive measurement | PASS (trivially; nothing was measured) | No pressure, no hardware work | — |
| Device identity | **FAIL** | All observed identity fields UNAVAILABLE | F-01, F-03 |
| Android compatibility (minSdk/targetSdk, guards) | PARTIAL | `minSdk 28`, `targetSdk 28` correct; Kotlin SDK_INT guards correct where present; Python thermal collector assumes API 28 | F-04, F-07 |
| Battery telemetry | **FAIL** (not observed) | All UNAVAILABLE without a probe | F-01, F-03, F-10 |
| Memory telemetry | **FAIL** (not observed) | As above | F-01, F-03, F-08 |
| CPU telemetry | **FAIL** (not observed) | As above; `/proc/stat` PERMISSION_REQUIRED asserted from documentation, not a probe | F-03 |
| GPU capability | **FAIL** (not observed) | GPU utilisation UNAVAILABLE + null (null rule respected), but no probe ran | F-03 |
| Thermal capability | **FAIL** | Status and headroom API_UNSUPPORTED from the default `api_level=28`; D-10 source selected without evidence | F-04 |
| Camera capability | **FAIL** (not observed) | Camera "0" listed with all fields UNAVAILABLE; no Camera2 dump; honoured-check NOT_TESTED | F-03, F-07 |
| Inference-backend capability | **FAIL** (not tested) | Five backends UNAVAILABLE without any runtime being loaded | F-03, F-07 |
| Profiling capability | **FAIL** (not tested) | ADB and trace claims not probed | F-05 |
| Energy feasibility | PARTIAL | `absolute_energy_claimed: false` (correct); E-1/E-2 EXTERNAL_REQUIRED; feasibility not assessed; `selected_level` injectable | F-12 |
| Schema validity | PASS | 0 errors in both runs | Schema-valid but not scientifically valid |
| Reproducibility / provenance | **FAIL** | `git_commit: "24aa0f0-impl"` hard-coded; unobserved `network` and `charging` values; no build fingerprint or config hash | F-09 |
| No fake zeros | PASS (model level) | `CapabilityResult.__post_init__` and the validator reject non-null values in non-available states | Correct |
| Error preservation | **FAIL** | ADB failures and missing probes become UNAVAILABLE, not ERROR or NOT_TESTED; out-of-range reads discarded | F-03, F-10 |
| C1–C4 boundary | PASS | Nothing selected | — |
| R0–R3 boundary | PASS | Nothing set | — |
| r* boundary | PASS | Nothing set | — |

## 3. Findings

Priorities:
- **P0**: blocking or scientifically invalid.
- **P1**: important; required before the Step 10D freeze.
- **P2**: non-blocking improvement.
- **P3**: documentation or minor.

"New device run" means new device characterization is required after the fix.

| ID | Pri. | File | Function / section | Problem | Scientific impact | Required correction | Required test | New device run |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| F-01 | P0 | `research/results/device_characterization/run_*/characterization.json`; `scripts/device_characterization/run_characterization.py` | Both runs; `run_characterization()` | No device was connected (`adb_connected: false`). Both runs contain zero observations and no raw evidence. | The Step 10D deliverable does not exist. Any reading of these files as phone capabilities is false. | Run the characterization with the physical OPPO A5 2020 connected and the on-device app executed. Store raw evidence. Keep the current files only if clearly relabelled as a no-device dry run (preferably remove them from `research/results/`). | A run without a device must fail or be labelled `dry_run` and refused as a Step 10D run. A Step 10D run requires `adb_connected: true` and an evidence directory. | **Yes** |
| F-02 | P0 | Same; `run_characterization()` (`run_id` argument) | Run identity and timing | The two runs started 25 s apart on 2026-10-05. `run_20261006_100000` is a caller-supplied name that contradicts `started_at`. Contents are identical apart from the ID fields. No reboot or boot-ID evidence. | The "two runs on separate days with reboot" requirement (protocol §4, handoff §6.3) is not met, and the directory name misrepresents the date. | Derive `run_id` from the actual start time (or record both, and reject a mismatch). Record the boot ID (`/proc/sys/kernel/random/boot_id`) and uptime for each run. Enforce separate calendar days and a different boot ID. | Reject a run_id/started_at date mismatch, the same boot ID across repeats, and a same-day repeat. | **Yes** |
| F-03 | P0 | `src/monitoring/characterization/collectors.py` | All collectors (`AVAILABLE if x is not None else UNAVAILABLE` pattern) | Missing input (probe not run, device absent) is recorded as UNAVAILABLE, which is a claim about the device. 47 such records. | Untested capabilities are reported as absent on the phone (for example GPU, camera, backends), which would mislead D-10, D-16 and later steps. | Missing input → **NOT_TESTED**. UNAVAILABLE only when a probe ran and found the feature unsupported or absent (sentinel, missing path), with raw output kept. Probe failure or ADB error → **ERROR** with `error_message` (stderr / exception). | `collect({})` returns only NOT_TESTED. A simulated ADB failure returns ERROR with the message. UNAVAILABLE requires a recorded probe result. | **Yes** |
| F-04 | P0 | `collectors.py` | `ThermalTelemetryCollector.collect()` (`props.get("api_level", 28)`; D-10 selection) | An unknown API level defaults to 28, which yields API_UNSUPPORTED for the thermal-status and headroom APIs. `selected_thermal_source` is set to the fallback without evidence. | Directly violates protocol §5.1 ("installed version NOT assumed") and D-10 ("thermal source decided from evidence"). | Unknown API → NOT_TESTED. API_UNSUPPORTED only from an observed `SDK_INT` with evidence. `selected_thermal_source` stays null until the status API is observed working (platform) or observed unavailable / below the gate (fallback). | Unknown api_level → NOT_TESTED and source null. Observed api 28 → API_UNSUPPORTED and fallback. Observed api 29 with a working call → platform. | **Yes** |
| F-05 | P0 | `collectors.py` (all collectors); `run_characterization.py` | `verified=` / `evidence_ref=` assignments; ADB property mapping | Any non-None input is marked `verified: true` and VERIFIED, with hard-coded `evidence_ref` strings (e.g. `battery_props.json#level`) for files that are never written. Demonstrated: `BatteryTelemetryCollector().collect({"level": 57})` returns VERIFIED. `proc_stat_readable_via_adb` and `atrace_adb_available` are hard-coded True whenever ADB connects, without probing. `mock_observed` input can reach the output path. | Mock or unverified data can enter `research/results` as VERIFIED device evidence. This is a data-integrity failure. | `verified: true` only for values read from the device in this run, with `evidence_ref` pointing to an existing raw-evidence file (with hash) and a semantics check done. Remove the hard-coded capability flags. Mock input must never produce VERIFIED and must be refused by the CLI for Step 10D runs. | Every VERIFIED record's `evidence_ref` resolves to an existing file. Mock input yields `verified: false`. A run record with `adb_connected: false` contains no VERIFIED record. | **Yes** |
| F-06 | P1 | `src/monitoring/characterization/models.py` | `map_runtime_state_to_report_status()` | Maps NOT_TESTED and ERROR → REQUIRES PILOT VALIDATION, and PERMISSION_REQUIRED → REQUIRES PILOT VALIDATION. `verified=True` short-circuits to VERIFIED. | Contradicts protocol §3: NOT_TESTED/ERROR → NOT YET VERIFIED; PERMISSION_REQUIRED → CONDITIONALLY AVAILABLE or UNAVAILABLE. It overstates readiness. | Implement the protocol §3 mapping exactly. VERIFIED only after the semantics check. | A table-driven test over all seven states. | Yes (regenerate) |
| F-07 | P1 | `mobile/characterization/` | `Collectors.kt`, `CharacterizationRunner.kt`, `AndroidManifest.xml`, `build.gradle.kts` | Only identity (manufacturer, model, SoC) and thermal status are implemented on device. Missing: battery properties and sentinels, memory, CPU, GPU strings, Camera2 dump and honoured check, backend checks, profiling, thermal headroom and zones. The manifest declares `.MainActivity`, which does not exist; there is no launcher resource or root Gradle project. The app's output is not consumed by the host pipeline. `observed_at` is epoch milliseconds, not ISO 8601. Storage permissions are unnecessary. | Most protocol items can be observed only on the device. The host-side ADB path cannot supply them. | Implement collectors 1–10 on device per handoff §4. Add a buildable project and entry point. Wire the app JSON (pulled via ADB) into the host report with evidence. Use ISO timestamps. Remove unneeded permissions. | Build check (assembleDebug) in CI or documented. Unit tests for SDK gates and sentinels on the Kotlin side, or instrumented tests. | Yes |
| F-08 | P1 | `run_characterization.py`; `adb_collector.py` | ADB property mapping; `collect_raw_evidence()`; `check_thermal_zones()` | ADB maps only manufacturer, model, release and SDK. The raw `getprop`, `meminfo` and `cpuinfo` evidence is saved but never parsed into records. `check_thermal_zones()` and the configured cpufreq/kgsl probes are never called. The 3 GB variant check (protocol §2) is not implemented. | Even with a device connected, RAM, CPU topology, thermal zones and GPU paths would remain unobserved. The 3 GB claim cannot be verified. | Parse the saved evidence into records with evidence references. Call the configured probes. Implement the nearest-variant check from observed total memory. | Fixture-based parsing tests on captured evidence text, and a variant-check test against the 3/4/6 GB nominal values. | Yes |
| F-09 | P1 | `run_characterization.py` | `CharacterizationRun(...)` construction | `git_commit: "24aa0f0-impl"` is hard-coded (not the implementing commit). `network: "OFFLINE"` and `charging: False` are written without observation. No build fingerprint, ADB version, host OS, config hash or app build hash. | Provenance is not reproducible, and the recorded conditions may be false. | Record the actual `git rev-parse HEAD` and dirty flag. Record observed conditions (battery status / plugged; airplane mode via `settings get global airplane_mode_on`), or null with NOT_TESTED. Add the build fingerprint, ADB version, config hash and app version code. | Assert the commit matches the repository HEAD, and that conditions come from probes or are null. | Yes (regenerate) |
| F-10 | P1 | `collectors.py` | `BatteryTelemetryCollector.collect()` (level range, `-20 <= temp_c <= 80`, `voltage > 0`) | An actually-read value outside an invented plausibility range is silently converted to UNAVAILABLE and discarded. Current is in mA while the API reports µA; the conversion is undocumented and the raw value is not kept. | Silent coercion hides sensor or unit problems (error-preservation rule). The plausibility range is an unapproved number. | Keep raw readings. Flag implausible values as ERROR (or AVAILABLE with a note) and keep the raw value in the evidence. Record units as the API reports them (µA), or document the conversion and keep the raw value. | An out-of-range reading yields ERROR with the raw value in the evidence, not UNAVAILABLE. A unit-conversion test. | Yes |
| F-11 | P1 | `docs/agent_sync/CHANGELOG.md` | 2026-10-05 Antigravity entry | Reports "two schema-valid characterization passes … on separate run IDs/dates" without stating that no device was connected. It lists no verified capabilities, limitations or unresolved issues, and gives the commit as "see git log". The capability matrix was not updated. | The record overstates Step 10D as device-characterized. | **Append-only** correction entry by Antigravity stating: no device observation; runs not on separate days; the findings above; the corrective plan. Do not edit the original entry. | — | — |
| F-12 | P2 | `collectors.py` | `EnergyMeasurementCapabilityChecker.collect()` | E-1/E-2 are EXTERNAL_REQUIRED whether or not feasibility was assessed. `E1_feasible` True gives state AVAILABLE with report status REQUIRES EXTERNAL INSTRUMENTATION (inconsistent). `selected_level` can be injected via props. | Feasibility is not distinguished from need. The level could be selected without evidence. | Record feasibility separately (NOT_TESTED until the researcher checklist and physical inspection exist). Derive `selected_level` only from evidenced checklist items. Make the state and report status consistent. | Injected `selected_level` is refused. Unassessed feasibility gives NOT_TESTED. | Yes (with the researcher checklist) |
| F-13 | P2 | `tests/test_device_characterization_collectors.py`; `tests/test_device_characterization_report.py` | All | Tests call collectors with empty or mock inputs and check types or nulls only. Nothing tests NOT_TESTED vs UNAVAILABLE, ERROR preservation, API-gate behaviour with an unknown API, evidence existence for VERIFIED, mock→VERIFIED prevention, or run-date / boot-ID checks. `compare_repeat_runs` reports all-null runs as "stable". | The 277 passing tests show the code runs, not that the device was characterized. | Add the tests listed for F-01 to F-10. Repeat-stability comparison must require observations. | As stated | — |
| F-14 | P2 | `src/monitoring/characterization/report_generator.py` | `process_run()`; module docstring | Overwrites an existing `characterization.json` in the same directory without a guard. The docstring claims it updates `device_capability_matrix.md`, but no such code exists. | Risk of overwriting a run; misleading documentation. | Refuse to overwrite an existing run file. Implement the matrix update or remove the claim. | A second `process_run` into the same directory raises. | — |
| F-15 | P3 | `tests/test_device_characterization_protocol.py` | `test_roles_and_handoff` | The assertion that the handoff requires narrowing the guards was deleted, although the handoff text is unchanged. | Unnecessary weakening of a test. | Restore the assertion. | — | — |

**Note on guard-test changes.** Narrowing the Step 10A–10C guards to allow `mobile/characterization`, `src/monitoring/characterization` and `research/results/device_characterization` is consistent with handoff §2 and is accepted, apart from F-15.

## 4. What is correct

- **No-fake-zero enforcement at model level.** `CapabilityResult.__post_init__` and `validate_characterization_record()` reject non-null values under non-available states, and `verified: true` without evidence. GPU utilisation is never coerced to 0.
- **`absolute_energy_claimed`** is fixed false. No absolute energy, latency, accuracy or thermal value is reported.
- **Android build.** `minSdk 28` and `targetSdk 28` meet the handoff. The Kotlin SDK_INT guards (≥ 29 for thermal status, ≥ 31 for `SOC_MODEL`) are version-aware where implemented, not exception-based.
- **No boundary violations.** No C1–C4, R0–R3 threshold, r*, energy-agreement threshold, calibration-binning or time-budget decision was made, and the authoritative protocol and decision files are unchanged.
- **Configuration-first** procedural parameters in `configs/device_characterization.yaml`. No binaries or bytecode committed.

## 5. Status of Step 10D after this audit

- **Step 10D is NOT ready to freeze.** All device capabilities remain **NOT YET VERIFIED**. The two merged run files are not valid device evidence.
- **Unresolved and preserved:**
  - C1–C4 (TO BE EMPIRICALLY DETERMINED);
  - R0–R3 thresholds (PILOT-DEPENDENT);
  - r* (REQUIRES FUTURE APPROVAL);
  - energy agreement threshold (PRE-DATA-COLLECTION DECISION REQUIRED);
  - calibration (ECE binning) decisions;
  - total decision-time budget;
  - D-10 thermal source and D-16 energy level (to be decided from device evidence).
- **Next action.** Antigravity applies the corrections through normal follow-up commits or PRs, appends an append-only correction entry, and produces two new runs on the physical device on separate days with a reboot between them. Claude Code then re-audits. **Step 10E is not started.**
