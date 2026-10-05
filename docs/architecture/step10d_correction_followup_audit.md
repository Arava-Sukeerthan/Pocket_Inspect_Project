# Step 10D — Follow-up Audit of Post-Audit Corrections (PR #22, commit `97da8c7`)

_2026-10-05, Claude Code (research review agent)._

**Merge status.** The request described PR #22 as open. On inspection it had **already been merged** into `main` (`e918094`) before this review, so this is again a **post-merge** review. Corrections listed here must go through a follow-up PR **before any real-device characterization run**.

**Scope.** This review asks only whether the corrected Step 10D **software** is trustworthy enough to use on the real OPPO A5 2020. It does not ask whether the phone has been characterized: no real device is connected yet, and that is expected.

Baseline: previous audit [`step10d_post_merge_audit.md`](step10d_post_merge_audit.md), findings F-01 to F-15. Diff reviewed: `3ff12b3...97da8c7`.

## Final decision

**CONDITIONAL APPROVAL — CORRECTIONS REQUIRED BEFORE MERGE**

Because PR #22 is already merged, the condition becomes: **corrections R-01 to R-07 are required in a follow-up PR before the software is used for real-device characterization.**

**What the approval does not mean.** It is not "Step 10D software ready". The Step 10D software is **not yet ready** for real-device use, and **Step 10D device characterization is NOT complete**:
- 0 device capabilities are verified;
- current dry-run output is 58 NOT_TESTED records out of 59.

**Why conditional rather than reject.**
- The core correction design is sound:
  - protocol-compliant status mapping;
  - NOT_TESTED for unprobed items;
  - no API-28 default;
  - an evidence-existence gate for VERIFIED;
  - date-mismatch and overwrite guards;
  - honest relabelling of the historical runs.
- However, a connected-device run **aborts** (reproduced, R-01/R-02), and several gaps remain.

## 1. How the software was exercised (no device data produced)

| Check | Result |
| :-- | :-- |
| `python -m pytest -q` | **272 passed** (reproduced) |
| Dry run via `run_characterization(..., dry_run=True)`, output in a scratch directory | Schema-valid; 58 NOT_TESTED, 1 EXTERNAL_REQUIRED; 0 verified; `is_dry_run: true` |
| **Connected-device code path** with a test stub standing in for `adb` (scratch only; the stub's synthetic output is not device evidence and was not committed) | **Run aborts with ValueError** at validation: `evidence/observed_props.json` (manufacturer) and `evidence/atrace_evidence.txt` (profiling) do not exist. A partially written run directory is left behind. |
| Collector outputs with device-like inputs (validator bypassed) | Identity, API level, release, total RAM, cores and `/proc/stat` come out VERIFIED. Thermal APIs NOT_TESTED; `selected_thermal_source` null. Battery, available memory, cpufreq, GPU, camera and backends are **always NOT_TESTED**, because nothing probes them. |
| Android build | The committed `mobile/characterization` project **fails Gradle configuration**: `Plugin [id: 'com.android.application'] was not found … plugin dependency must include a version number`. There is no `settings.gradle(.kts)`, root build file or Gradle wrapper. No Android SDK is available here, so an APK build cannot be confirmed either way, but the reported "BUILD SUCCESSFUL" is **not reproducible from the repository**. |
| Historical runs | Preserved, and labelled `is_dry_run: true`, `is_valid_step10d_device_evidence: false`, with a note. Schema-valid. Not presented as evidence. |
| CHANGELOG | The original 2026-10-05 Antigravity entry is untouched (no deleted lines). A new correction entry is appended. |
| Boundaries | No C1–C4, R0–R3, r*, energy-agreement threshold, calibration-binning or time-budget decision. Protocol, decision-register and research-question files are unchanged. |

## 2. F-01 to F-15 status

| ID | Status | Evidence |
| :-- | :-- | :-- |
| F-01 No device data | FIXED as far as software can fix it | Dry runs are labelled and cannot verify anything. Real runs are pending by design. |
| F-02 Run date integrity | FIXED (minor gap R-11) | `run_id` date must equal the actual UTC start date; historical runs relabelled; `compare_repeat_runs` requires separate dates and different boot IDs |
| F-03 NOT_TESTED vs UNAVAILABLE | PARTIALLY_FIXED | Missing input gives NOT_TESTED (correct). **ADB/probe failures never give ERROR**; stderr is discarded (R-03). |
| F-04 API level | FIXED | No `api_level` default. Unknown gives NOT_TESTED and `selected_thermal_source` null. Kotlin SDK_INT guards present. |
| F-05 Verified only with real evidence | PARTIALLY_FIXED | Validator gate (adb_connected, not dry-run, evidence file exists) is correct. But `evidence_ref` points to a never-written file (R-01), `atrace_adb_available = True` is still hard-coded (R-02), and `mock_observed` can still be merged into a connected run (R-10). |
| F-06 Status mapping | FIXED | `map_runtime_state_to_report_status` matches protocol §3 (NOT_TESTED/ERROR → NOT YET VERIFIED; PERMISSION_REQUIRED → CONDITIONALLY AVAILABLE or UNAVAILABLE) |
| F-07 Android app | PARTIALLY_FIXED | `MainActivity` exists and storage permissions are removed. Only 3 of 10 collectors. Output is written to private `filesDir` and never collected by the host. **The project is not buildable from the repository** (R-05). |
| F-08 ADB collector | PARTIALLY_FIXED | Invokes adb, saves raw getprop/meminfo/cpuinfo/stat/thermal text, parses meminfo and cpuinfo, gets the boot ID, and has a variant check. Battery, cpufreq, GPU and thermal service are not probed (R-04). No error preservation (R-03). |
| F-09 Provenance | PARTIALLY_FIXED | Real `git rev-parse HEAD` with dirty flag, adb version read, config SHA-256, boot ID. `network: "OFFLINE"` and `charging: False` are still hard-coded; the `soc_model` evidence file is wrong; evidence files are not hashed (R-07). |
| F-10 Invalid battery readings | FIXED (minor R-09) | Implausible values become ERROR, with the raw value in `error_message` |
| F-11 CHANGELOG | FIXED (new inaccuracies R-13) | Append-only correction entry added; original untouched |
| F-12 Energy | **NOT_FIXED** | `selected_level` is still accepted from props (`{"selected_level": "E-1"}` returns E-1 with no evidence). The `E1_feasible = True` path raises ValueError (EXTERNAL_REQUIRED with a non-null value) (R-06). `absolute_energy_claimed` stays false (correct). |
| F-13 Test quality | PARTIALLY_FIXED | Targeted unit tests for F-02/03/04/05/06/10/14 added. No end-to-end connected-path test (would have caught R-01/R-02), no ADB-failure tests, no repeat-run comparison tests (R-12). |
| F-14 Overwrite protection | FIXED (minor R-11) | `FileExistsError` in the CLI and in `process_run` |
| F-15 Restored assertion | FIXED | The handoff allow-list assertion is restored |

## 3. New findings (for Antigravity)

Priorities: **P0** blocking; **P1** required before the real-device run; **P2** non-blocking; **P3** minor.

| ID | Pri. | File | Function | Problem | Impact | Exact correction | Test required |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R-01 | P0 | `src/monitoring/characterization/collectors.py`; `scripts/device_characterization/adb_collector.py` | `_determine_state_and_verification()` (`evidence/observed_props.json#…`); `collect_raw_evidence_and_observations()` | Verified records cite `evidence/observed_props.json`, which no code writes. The validator then rejects the run. | **Any real-device run aborts.** The software cannot produce Step 10D evidence. | Cite the actual raw file and key (e.g. `evidence/getprop_evidence.txt#ro.product.manufacturer`), **or** write `observed_props.json` containing the parsed values plus the SHA-256 of each source evidence file. On validation failure, do not leave a partial run directory, or mark it failed. | End-to-end test with a stub `adb` (connected): the run completes; every VERIFIED `evidence_ref` resolves to an existing file. |
| R-02 | P0 | `scripts/device_characterization/adb_collector.py` | `collect_raw_evidence_and_observations()` (`observed_props["atrace_adb_available"] = True`) | Profiling capability is hard-coded True without a probe, and cites a non-existent `atrace_evidence.txt` | Fabricated capability (F-05 residue); also aborts the run | Probe it (e.g. capture `adb shell atrace --list_categories` stdout, stderr and exit code to `evidence/atrace_evidence.txt`) and set the key only from the probe result. Otherwise leave it NOT_TESTED. | Stub returns failure → no VERIFIED; success → VERIFIED with the file present. |
| R-03 | P1 | `adb_collector.py` | `_adb_cmd`, `get_properties`, `read_file`, `is_device_connected`, `_get_adb_binary` | Probe failures drop the key (→ NOT_TESTED) and discard stderr. "adb missing", "no device", "unauthorized" and "multiple devices" all collapse into a silent dry run. | Errors cannot be distinguished; failed probes are mislabelled as untested; an intended device run silently becomes a dry run | Log every command (argv, exit code, stdout/stderr paths) to `evidence/commands.log`. A failed probe → ERROR with the message. Classify connection state explicitly (`adb_missing`, `no_device`, `unauthorized`, `multiple_devices`, `device`). Add a CLI flag requiring a device that fails loudly instead of falling back to dry run. Record the device serial used. | Stub scenarios for each connection state and for command failure → expected ERROR or connection-state output |
| R-04 | P1 | `adb_collector.py`; `mobile/characterization/`; `run_characterization.py` | Probe set; Android output integration | Battery (`dumpsys battery`), available memory, cpufreq (configured paths), GPU kgsl paths (configured), thermal service, camera, backends and profiling are never probed. The app's JSON (identity, memory, thermal) stays in private storage and is never pulled or merged. | Real runs would leave most of the matrix NOT_TESTED, so Step 10D cannot complete | Add ADB probes for the configured paths and `dumpsys battery` / `dumpsys thermalservice`, with raw evidence. Integrate the app output (e.g. write to the app-specific external directory and `adb pull`, or use `run-as` on a debug build), saving the pulled JSON as evidence, with each record citing it. Implement the remaining on-device collectors per handoff §4 (battery properties and sentinels, Camera2 dump and honoured check, backend reference-graph checks), or record them explicitly as NOT_TESTED with the reason. | Fixture-based parsing tests for each probe; a test that pulled app JSON is merged with evidence references |
| R-05 | P1 | `mobile/characterization/` | Build setup; `AndroidManifest.xml` | No `settings.gradle.kts`, root build, plugin versions or Gradle wrapper; Gradle configuration fails as committed. The manifest `package` attribute duplicates `namespace` (rejected by recent Android Gradle Plugin versions). The CAMERA permission is declared without camera code. | The "BUILD SUCCESSFUL" claim is not reproducible; violates the protocol's reproducibility rule | Commit the Gradle wrapper, `settings.gradle.kts` and pinned plugin versions, and document the exact build command. Remove the manifest `package` attribute. Keep CAMERA only once Camera2 code exists. | A documented `./gradlew assembleDebug` on a clean checkout (CI optional) |
| R-06 | P1 | `collectors.py` | `EnergyMeasurementCapabilityChecker.collect()` | `selected_level` is accepted from props. `E1_feasible = True` raises ValueError (state EXTERNAL_REQUIRED with a non-null value). | F-12 not fixed; the energy level could be set without evidence; latent crash once the checklist is filled | Remove the props override. Derive `selected_level` only from an evidenced researcher checklist (file plus hash). For a feasible level, use a consistent state/value pair (e.g. AVAILABLE with evidence, or EXTERNAL_REQUIRED with `value: null` and the notes). Keep `absolute_energy_claimed: false`. | Injected `selected_level` is ignored or rejected; `E1_feasible` True does not crash |
| R-07 | P1 | `run_characterization.py`; `adb_collector.py`; `collectors.py` | `conditions`; evidence mapping | `network: "OFFLINE"` and `charging: False` are written without observation. `soc_model` (from getprop) cites `cpuinfo_evidence.txt`. getprop is executed twice, so the parsed values may differ from the saved file. Evidence files are not hashed (stale evidence cannot be detected). | Provenance does not describe the actual execution | Observe the conditions (`settings get global airplane_mode_on`, `dumpsys battery` status/plugged), or record null with NOT_TESTED. Parse the saved evidence text, not a second call. Cite the correct file. Record SHA-256 and capture time per evidence file in the run record. | Conditions come from probes or are null; the evidence reference matches the source; hashes are present |
| R-08 | P2 | `collectors.py` | `DeviceIdentityCollector` variant check | Uses a fixed 2400–3500 MB window, not the protocol's nearest-nominal-variant rule. The CHANGELOG states 2700–3300. A mismatch yields AVAILABLE, not a blocking disagreement. | An unapproved number in the code; documentation inconsistent | Implement nearest-nominal (3/4/6 GB) classification from observed total memory. A mismatch → ERROR and blocking. Correct the CHANGELOG through an append-only note. | Nearest-variant test cases; a mismatch blocks sign-off |
| R-09 | P2 | `collectors.py` | `BatteryTelemetryCollector` | `CURRENT_NOW` 0 is accepted as a reading, and the raw value is lost (notes show `None`). Plausibility ranges are unapproved numbers. | Sentinel semantics and the raw value are not preserved | Keep the raw value and unit (µA) in evidence. Treat 0 as suspect and flag it per protocol. Move plausibility limits to config with a justification. | Raw value present; 0 flagged |
| R-10 | P2 | `run_characterization.py`; `collectors.py` | `run_characterization(mock_observed=…)`; `is_real_device_observation` | `mock_observed` is merged even when a device is connected, and the real-observation flag is caller-supplied | Synthetic keys could be marked VERIFIED in a connected run (blocked today only if no evidence file exists) | Reject `mock_observed` when `adb_connected`. Set the real-observation flag only inside the ADB collector. | Mock + connected → error |
| R-11 | P2 | `run_characterization.py`; `report_generator.py` | `run_id` date check; `process_run` | The date check applies only to `x_YYYYMMDD` patterns. Exists-check then write is not atomic. A failed run leaves a partial directory. | Minor integrity gaps | Derive `run_id` only from the start time, or check any embedded date. Open the output file with exclusive create. Clean up or mark failed runs. | Tests for these cases |
| R-12 | P2 | `tests/` | — | No end-to-end connected-path test, ADB-failure tests or `compare_repeat_runs` tests | R-01/R-02 went undetected | Add the tests listed above | — |
| R-13 | P3 | `docs/agent_sync/CHANGELOG.md` | 2026-10-05 Antigravity correction entry | States 2700–3300 MB (code: 2400–3500); "ADB version `1.0.41`" reads as a device observation; "gradlew assembleDebug built cleanly" is not reproducible from the repository; "Addressed all audit findings" is overstated | Record accuracy | Append-only correction entry | — |
| R-14 | P3 | `research/results/device_characterization/run_20261006_100000/` | Directory name | The name still implies 6 October; the JSON labels make the run invalid | Possible misreading | Add a README in each historical run folder stating "pre-audit dry run, not device evidence; name does not reflect the run date". Keep the files (history preserved). | — |

## 4. Current state (unchanged by this review)

- **Real-device characterization:** NOT performed. **0** verified device capabilities. The current dry-run output is NOT_TESTED for 58 of 59 records (the corrected implementation reports 47 NOT_TESTED in its own summary; the count depends on the collector set).
- **Preserved as unresolved:**
  - C1–C4, R0–R3 thresholds, r*;
  - energy agreement threshold, calibration binning, total decision-time budget;
  - D-10 thermal source and D-16 energy level, both from device evidence.
- **Next action:**
  1. Antigravity fixes R-01 to R-07 (and ideally R-08 to R-14) in a follow-up PR, with an append-only CHANGELOG entry.
  2. Claude Code re-reviews.
  3. Then the physical OPPO A5 2020 (3 GB) is connected, and two genuine runs are made on separate days with a reboot between them.

**Step 10E not started.**
