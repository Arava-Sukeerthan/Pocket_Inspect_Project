# Step 10D Post-Merge Correction Round 2 Review

| Field | Value |
| :-- | :-- |
| Reviewer | Claude Code (independent review agent; no corrections implemented) |
| Date | 2026-10-05 |
| Reviewed change | Antigravity `3f4b7aa`, branch `antigravity/step-10d-final-correction` |
| Merge state | **Already merged into `main` as `8448967` (PR #26) when reviewed.** This is a post-merge review. |
| Previous audit | [`step10d_pr24_followup_audit.md`](step10d_pr24_followup_audit.md) (P-01 to P-07, R-01 to R-14) |
| Diff inspected | `git diff bd5048e 8448967` and `git show --stat 3f4b7aa` (8 files, +358/−94) |

## Decision

**CONDITIONAL APPROVAL — CORRECTIONS REQUIRED**

## Executive Summary

Round 2 fixes the two problems that could contaminate research artifacts:

- **P-01:** a run no longer rewrites `device_capability_matrix.md`.
- **P-02:** tests write only to temporary directories. `pytest` was run twice, and `git status` was clean both times.

It also adds a working `--serial` option, the `--require-device`/`--dry-run` conflict check, SHA-256 checking of the manifest, and retrieval of the Android app's output file.

The software is still **not ready** for the physical run. These gaps were confirmed by executing the code, not only by reading it:

1. **CPU frequency and GPU clock are still never reported** (P-03). The parser writes `cpu_scaling_cur_freq` and `gpu_clock_hz`, but the collectors still read `cur_freq_khz` and `gpu_freq_hz`. Both stay NOT_TESTED although their evidence is collected. The CHANGELOG states these keys were aligned; they were not.
2. **The app's observations are retrieved but never used.** The app JSON has top-level keys (`device_identity`, `battery_telemetry`, …) that no collector reads. `app_output_status` is not written to `characterization.json`.
3. **The SoC citation is still wrong** (P-04). `source_soc_prop` is recorded in `observed_props.json`, but the collector still always cites `getprop_evidence.txt#ro.soc.model`. When the value came from `ro.board.platform` or `/proc/cpuinfo`, the citation names a key, and in the cpuinfo case a file, that did not supply it. On the OPPO (API < 31) this is the normal path.
4. **A failed probe still becomes NOT_TESTED, not ERROR** (P-07). There was no change for this finding and no test.
5. **A battery current of 0 is VERIFIED as 0.0 mA** (R-09). The note mentions a possible sentinel, but the value is still reported as a verified zero. In addition, `dumpsys battery` "current now" is labelled mA with no unit check.
6. **Deleting `manifest.json` disables the integrity check** (P-05 residue). Validation then passes with tampered evidence.
7. **The Gradle wrapper jar is still missing** (R-05). `gradlew --version` cannot run.

Nothing in round 2 fabricates device data. A dry run still produces 0 VERIFIED results.

**Testing method.** I tested the connected path with a fake `adb` shell script kept outside the repository. Its output is synthetic and is not device evidence. Nothing from it was committed.

## P-01

**Status: FIXED (matrix isolation). Residue: no identity check against the known specification.**

**Evidence:**
- `report_generator.py` `process_run()` no longer calls `update_device_capability_matrix()`, and nothing else calls that method (grep).
- A fake `adb` run whose device reported `STUB`/`STUBMODEL` left `git status` clean; the matrix was unchanged.
- Run outputs go only to the results directory you pass in (`results_dir=`) or the configured one.
- The manufacturer specification in `models.py`'s `known_specification` stays separate from the observed values.
- Evidence refs are relative to the run directory, so they identify the run by location.

**Residue (non-blocking):**
- The run record still marks `manufacturer: STUB` as VERIFIED without flagging that it disagrees with the known specification. The previous audit required that disagreement to be reported as a finding (protocol line 51). VERIFIED here means "observed with evidence", so this is not fabrication.
- In-memory `report_status` values are `ReportStatus` enum objects (they print as `ReportStatus.VERIFIED`). They serialize correctly to JSON, so this is cosmetic now that the matrix writer is gone.

**Tests:**
- `test_p01_connected_run_does_not_mutate_matrix` asserts the matrix text is unchanged after a connected run.
- It replaces `collect_raw_evidence_and_observations` with a mock, so it guards against the regression but does not exercise a fake device.

## P-02

**Status: FIXED**

**Evidence:**
- `run_characterization(results_dir=…)` was added, and every E2E test passes a `tempfile.mkdtemp()` fixture.
- `test_f02_date_mismatch_rejection` now passes `tmp_path`.
- The run ID is built from `utcnow()` (`run_{today}_120000`). There is no hard-coded historical ID in a call to `run_characterization`; `run_20261005_120000` remains only as a string in a validation-only P-05 test.
- `overwrite=True` is used only inside a temporary directory.

**Tests:**
- `pytest` run twice: **282 passed / 282 passed**.
- `git status --short --untracked-files=all` was empty after each run, and no synthetic run directory remained.
- Minor: the test and the run read the clock separately, so a run that crosses midnight UTC could fail. This is not blocking.

## P-03

**Status: PARTIALLY_FIXED**

Trace through the pipeline, using the fake `adb` connected run (API 29, `current now: 0`):

| Metric | Probe → raw evidence | Parser key | Collector reads | Final |
| :-- | :-- | :-- | :-- | :-- |
| manufacturer, model, Android release, API level | `getprop` → `getprop_evidence.txt` | `manufacturer`, `model`, `release_version`, `api_level` | same | VERIFIED; refs resolve |
| total RAM, variant check | `/proc/meminfo` | `total_ram_mb` | same | VERIFIED |
| available memory | `/proc/meminfo` | `available_memory_mb` | `available_memory_mb` (**fixed**) | VERIFIED |
| battery level, voltage, temperature | `dumpsys battery` | `battery_level_percent`, `battery_voltage`, `battery_temperature` | same (**fixed**) | VERIFIED. The `#battery_level_percent` fragment names a parsed key; the raw file says `level:`. |
| battery current | `dumpsys battery` | `battery_current_now` | same (**fixed**) | **VERIFIED 0.0 mA** (see R-09) |
| charging | `dumpsys battery` | `charging_state` | `conditions.charging` | `true`; `null` if the probe fails |
| network / airplane mode | `settings get global airplane_mode_on` | `network_state` | `conditions.network` | `OFFLINE`. This is airplane mode only; Wi-Fi can be on in airplane mode. |
| CPU frequency | `scaling_cur_freq` → `cpufreq_evidence.txt` | `cpu_scaling_cur_freq` | **`cur_freq_khz`** | **NOT_TESTED despite evidence** |
| GPU clock | `kgsl gpuclk` → `gpu_evidence.txt` | `gpu_clock_hz` | **`gpu_freq_hz`** | **NOT_TESTED despite evidence** |
| GPU renderer | none on the host; app only | — | `gpu_renderer` | NOT_TESTED |
| thermal zones | sysfs → `thermal_evidence.txt` | `thermal_zones_readable_count` | same | VERIFIED |
| battery temperature as a thermal source | `dumpsys battery` | (`battery_temperature`) | `battery_temp_available` | NOT_TESTED despite evidence |
| camera | `dumpsys media.camera` → saved | not parsed | `camera_ids` / `camera_<id>` | NOT_TESTED |
| inference backends | none | — | — | NOT_TESTED (correct: no probe) |
| profiling / atrace | `atrace --list_categories` | `atrace_adb_available` | same | VERIFIED |
| SoC | `getprop` / `cpuinfo` | `soc_model`, `source_soc_prop` | `soc_model` | VERIFIED, **wrong citation** (P-04) |

Android app output, `retrieve_android_app_output()`:

| Fake-`adb` case | Result |
| :-- | :-- |
| `run-as` fails with "package not debuggable" | `APP_OUTPUT_MISSING`. An error is reported as missing. |
| Valid JSON | `APP_OUTPUT_COLLECTED`; `android_app_evidence.json` saved and hashed |
| Invalid JSON | `APP_OUTPUT_ERROR`; the raw text is saved |

Even when the output is collected, its content is merged only under its own top-level keys (`device_identity`, `battery_telemetry`, …), which no collector reads. So **no app observation reaches the report**, and `app_output_status` is not in `characterization.json`.

**Tests:** no test runs the real parser output through the real collectors. That is why the CPU and GPU mismatches were not caught.

## P-04

**Status: NOT_FIXED** (in the report; provenance is now recorded only in `observed_props.json`)

**Evidence:**
- The fallback order in `collect_raw_evidence_and_observations()` is `ro.soc.model` → `ro.board.platform` → cpuinfo `Hardware` → `None` with `UNAVAILABLE`.
- Each value comes from evidence that was actually read. There is no fabricated value.
- However, `DeviceIdentityCollector` still hard-codes `ev_soc = "evidence/getprop_evidence.txt#ro.soc.model"`. In the fake runs:
  - the `ro.board.platform` fallback gave value `trinket`, cited as `#ro.soc.model`;
  - the cpuinfo fallback gave value `STUBHW`, cited as `getprop_evidence.txt#ro.soc.model`. That is the wrong file as well as the wrong key.

**Tests:** `test_p04_soc_property_fallback_provenance` tests only `get_properties()` parsing. It does not check `source_soc_prop` or the collector's `evidence_ref`.

## P-05

**Status: PARTIALLY_FIXED**

**Evidence:**
- `validate_characterization_record()` recomputes SHA-256 for every manifest entry.
- `process_run()` validates before writing `characterization.json`, so the check happens before the result is accepted.

Results from executing it against a copy of a fake-`adb` run:

| Case | Errors |
| :-- | :-- |
| Valid, unchanged | 0 (accepted) |
| Cited evidence file missing | 5 (detected) |
| Evidence file tampered | 1 (SHA-256 mismatch) |
| Wrong hash in manifest | 1 (detected) |
| **`manifest.json` deleted** | **0 — accepted** |
| **Evidence tampered and `manifest.json` deleted** | **0 — accepted** |
| Evidence tampered and manifest re-hashed | 0. Inherent without anchoring: `characterization.json` stores no manifest hash. |

**Tests:** `test_p05_manifest_hash_verification` covers the valid and tampered cases only.

## P-06

**Status: PARTIALLY_FIXED**

`get_connection_status()` results with the fake `adb`:

| Case | Result |
| :-- | :-- |
| ADB missing | `ADB_MISSING` |
| no device | `NO_DEVICE` |
| unauthorized | `UNAUTHORIZED` |
| offline | `OFFLINE` |
| two devices | `MULTIPLE_DEVICES` |
| two devices with `--serial B2` | `CONNECTED` |
| two devices with `--serial ZZ` | `NO_DEVICE` |
| **Device `STUB123` with `--serial STUB1`** | **`CONNECTED`**: a prefix match (`startswith`), not an exact serial match |
| `no permissions` line | `NO_DEVICE` (should be a distinct state or UNAUTHORIZED-like) |

CLI behaviour:
- `--require-device --dry-run` raises `ValueError`.
- `--require-device` with multiple devices raises `RuntimeError`.
- The CLI with `--serial B2 --require-device` completed against the fake `adb`.
- `device_serial` is recorded in `conditions`. When none is given it records `null`, not the auto-detected serial.

**Tests:**
- `test_adb_serial_selection`, `test_p06_require_device_and_dry_run_collision`, and the classification test.
- None for `OFFLINE`, `ADB_MISSING` or a serial prefix collision.

## P-07

**Status: NOT_FIXED**

**Evidence:** No collector or parser code changed for this finding.

With `dumpsys battery` failing (exit code 1, error on stderr):
- battery level and voltage stay **NOT_TESTED**;
- charging becomes `null`;
- the failure is visible only in `commands.log`.

The same pattern holds for every `read_file`-based probe: a failure drops the key. The only failed probes that do not end up NOT_TESTED are atrace (reported as unavailable through `atrace_adb_available = False`) and the app output.

**Tests:** none.

## R-03 to R-14

| Requirement | Status | Evidence | Remaining issue |
|---|---|---|---|
| R-03 explicit ADB states / no silent dry run | PARTIALLY_FIXED | `adb_collector.get_connection_status()`; `run_characterization()` conflict check and `--serial` | Serial prefix match; `no permissions` → NO_DEVICE; failed probe → NOT_TESTED |
| R-04 actual device probes | PARTIALLY_FIXED | Probes and evidence saved; battery and available memory now reported | CPU frequency, GPU clock, camera and battery temperature as a thermal source not reported; app observations unused |
| R-05 reproducible Android build | **NOT_FIXED** | `gradle/wrapper/gradle-wrapper.jar` absent; `gradlew` is a 44-line hand-written stub, mode 100644, calls an undefined `die`. Only `mobile/characterization/README.md` was added. | The standard wrapper is needed; committing the jar is a binary and needs user approval |
| R-06 energy evidence safety | FIXED | E-1 and E-2 value `None`; no `selected_level` injection; `absolute_energy_claimed: false` (unchanged since PR #24, re-checked in the fake run) | — |
| R-07 observed conditions and evidence hashes | PARTIALLY_FIXED | Charging and network from probes; manifest hashes verified | SoC citation (P-04); a missing manifest bypasses the check |
| R-08 RAM semantics | PARTIALLY_FIXED | 2700–3300 MB window in `collectors.py` (unchanged) | Protocol uses a nearest-variant rule; the window is hard-coded (not in `configs/`); a mismatch does not block |
| R-09 battery current semantics | PARTIALLY_FIXED | Key aligned; note on zero | 0 reported as VERIFIED 0.0 mA (no-fake-zero risk); no µA/mA unit check on `dumpsys` |
| R-10 mock isolation | FIXED | `ValueError` on mock data in a connected run; dry run forces `is_real_device_observation=False` | — |
| R-11 atomic result integrity | PARTIALLY_FIXED | `process_run()` unchanged since PR #24 | No temp-file-and-rename; evidence directory left behind on failure |
| R-12 connected E2E testing | PARTIALLY_FIXED | 10 E2E tests, isolated, date-independent | The full-path tests mock the collector; no tests for failure paths (probe → ERROR, missing manifest, offline) |
| R-13 documentation accuracy | **NOT_FIXED** | The round-2 CHANGELOG entry claims CPU/GPU keys were aligned (false) and "regression tests for P-01 to P-07" (none for P-03 or P-07). The README says "Gradle 8.5 (managed via `./gradlew` standard wrapper)" (false) and lists 12 Kotlin component files, when only 3 `.kt` files exist. | Correct in the next append-only entry and in the README |
| R-14 historical / audit documentation | FIXED | `run_20261005_100000/README.txt` and `run_20261006_100000/README.txt` present | — |

## Android Build

| Item | Result |
| :-- | :-- |
| Wrapper scripts present? | Yes: `gradlew`, `gradlew.bat` |
| Wrapper JAR present? | **No** |
| Standard wrapper? | **No.** Hand-written stub, not executable (mode 100644), undefined `die`. |
| Reproducible configuration? | **PROJECT CONFIGURATION PLAUSIBLE, NOT VALIDATED.** `settings.gradle.kts`; AGP 8.2.2; Kotlin 1.9.22; Gradle 8.5 in `gradle-wrapper.properties`; compileSdk 34; minSdk 28. |
| `./gradlew --version` executable? | **No:** `Error: Unable to access jarfile …/gradle/wrapper/gradle-wrapper.jar` |
| Build actually executed? | **BUILD NOT EXECUTED.** The wrapper is broken. This environment also blocks `dl.google.com` (403) and has no Android SDK. |
| Build result | None. The round-2 CHANGELOG also reports "BUILD NOT EXECUTED"; no build success has been claimed. |

## Test Integrity

| Item | Result |
| :-- | :-- |
| Test count | 282 |
| First run | 282 passed |
| Second run | 282 passed |
| `git status` after run 1 | clean |
| `git status` after run 2 | clean |
| Synthetic results remaining? | None |

Weaknesses in what the tests check:
- The P-01 and full-path tests replace the collector with a mock.
- The P-04 test does not test the SoC fallback.
- The P-05 test omits the missing-file, wrong-hash and missing-manifest cases.
- There are no tests for P-03's parser-to-collector mapping or for P-07.

## Research Boundary

Unchanged. `git diff bd5048e 8448967 --stat -- research configs docs` lists only `docs/agent_sync/CHANGELOG.md` and the previous audit document from PR #25. Round 2 did not touch any of the following:
- GC-03, the research gap, the RQs or the hypotheses;
- C1–C4, R0–R3, the confidence-verification protocol or r*;
- D-01 to D-16;
- the experimental matrix or the dataset selection.

## Real Device

- REAL OPPO A5 2020 CONNECTED: **NO**
- REAL OPPO CHARACTERIZATION PERFORMED: **NO**
- REAL DEVICE EVIDENCE COLLECTED: **NO**

## No-Fake-Data Audit

- The only hard-coded OPPO identity is in `models.py` `known_specification` and the `device_unit_id` default. Both are labelled as specification and are never copied into observed values.
- No hard-coded `verified=True`.
- Dry run: 0 VERIFIED; all results NOT_TESTED, except `external_surface_probe`, which is EXTERNAL_REQUIRED.
- Fake-zero risk: battery current 0 → VERIFIED 0.0 mA (R-09).
- No fabricated RAM, thermal or camera values were found.
- Synthetic test evidence stays in temporary directories.

## Remaining Risks

1. CPU and GPU frequency not reported (key mismatch); app observations unused; `app_output_status` not in the report (P-03).
2. Wrong SoC citation on fallback, which is the normal path on the OPPO (P-04).
3. A failed probe gives NOT_TESTED instead of ERROR (P-07).
4. Battery current 0 is VERIFIED; no unit check (R-09).
5. A deleted manifest bypasses the integrity check (P-05).
6. The Gradle wrapper jar is missing, so the APK cannot be built from the repo (R-05).
7. Serial prefix match; `no permissions` → NO_DEVICE; the auto-detected serial is not recorded (P-06).
8. `APP_OUTPUT_MISSING` also covers `run-as` and command errors.
9. RAM window semantics and a non-blocking mismatch (R-08); no identity-mismatch finding (P-01 residue).
10. Non-atomic writes (R-11); tests bypass the collector (R-12); documentation inaccuracies (R-13).

## Final Recommendation

These are the corrections that must be made before physical characterization:

1. **P-03:** Make the collectors read `cpu_scaling_cur_freq` and `gpu_clock_hz`, or rename the parser keys. Map the app JSON sections into collector inputs, and record `app_output_status` in `conditions`. Add an E2E test that runs the real `collect_raw_evidence_and_observations()` with a fake `adb` and asserts that every metric whose probe succeeded is AVAILABLE with a resolving ref.
2. **P-04:** Build the SoC `evidence_ref` from `source_soc_prop`, using the right file and key. Test all three fallbacks.
3. **P-07:** An attempted probe that fails must give ERROR with the stderr text. Test it with the fake `adb`.
4. **R-09:** Do not report a battery current of 0 as VERIFIED. Classify it UNAVAILABLE (sentinel) unless corroborated, and verify the µA/mA unit.
5. **P-05:** A connected run with a missing `manifest.json` must fail validation. Record the manifest SHA-256 in `characterization.json`.
6. **R-05:** Commit the standard Gradle 8.5 wrapper, generated by `gradle wrapper`, including `gradle-wrapper.jar`, with `gradlew` executable. The jar is a binary, so this **requires the user's explicit approval** under AGENTS.md. Then record an actual `./gradlew clean assembleDebug` on a machine that has the SDK.

Non-blocking but expected: the remaining P-06 issues (serial exact match, `no permissions`), the R-13 documentation corrections, and the identity-mismatch finding.

Step 10E not started.
