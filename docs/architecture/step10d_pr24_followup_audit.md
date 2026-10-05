# Step 10D — Final Follow-up Audit of PR #24 (software readiness)

| Field | Value |
| :-- | :-- |
| Reviewer | Claude Code (review agent; no corrections implemented) |
| Date | 2026-10-05 |
| PR | #24, branch `antigravity/step-10d-followup-correction`, commit `597298e` |
| Base before PR | `eb49c95` |
| Merge state | **Already merged into `main` as `bd5048e` when reviewed.** This is a post-merge review. |
| Previous audits | [`step10d_post_merge_audit.md`](step10d_post_merge_audit.md) (PR #20, F-01 to F-15); [`step10d_correction_followup_audit.md`](step10d_correction_followup_audit.md) (PR #22, R-01 to R-14) |
| Scope | Is the software trustworthy and reproducible enough to use on the real OPPO A5 2020 (3 GB)? Real-device characterization was **not** required and **not** performed. |

## Decision

**CONDITIONAL APPROVAL — CORRECTIONS REQUIRED**

PR #24 fixes the two P0 blockers from the previous audit:

- **R-01 (evidence files):** a connected run now completes, and every VERIFIED `evidence_ref` resolves to a file that exists.
- **R-02 (atrace):** the atrace capability now comes from a real probe.

The dry-run and no-device paths are safe. Every result stays NOT_TESTED or NOT YET VERIFIED, nothing is VERIFIED, and energy reports no level and no absolute claim.

The software is still **not ready** to run on the OPPO, for these reasons:

1. **A single connected run rewrites the authoritative capability matrix** (Finding P-01). Each run rewrites `research/experiments/device_capability_matrix.md`:
   - The status is written as the literal string `ReportStatus.VERIFIED`.
   - The run does not compare the observed identity with the known specification.
   - It does not wait for the required second run on a separate day, or for the reboot.

   In this audit, a scratch fake `adb` reporting manufacturer `STUB` turned the matrix's "Manufacturer" and "Model" rows into VERIFIED.
2. **The new end-to-end test writes into the real results tree** (P-02):
   - It writes a synthetic record marked `adb_connected: true` with identity VERIFIED as "OPPO A5 2020" into `research/results/device_characterization/run_20261005_120000/`, which git does not ignore.
   - It uses `overwrite=True`.
   - It is date-locked: it fails from 2026-10-06 onward.
3. **Most of the new probes are collected but never reported** (P-03). The keys the ADB parser writes do not match the keys the collectors read. Battery, cpufreq, available memory, battery temperature and camera stay NOT_TESTED even when their evidence file exists. The Android app's output is never retrieved by the host.
4. **The Android build is not reproducible from the repository** (R-05). The committed `gradlew` is a hand-written stub. It needs `gradle/wrapper/gradle-wrapper.jar`, which is not committed.

None of these fabricates a device result in a dry run. P-01 and P-02, however, can put unverified or synthetic content into research artifacts, so they must be fixed before the physical run.

## 1. What was inspected

| Item | Method |
| :-- | :-- |
| PR diff | `git show --stat 597298e`; `git diff eb49c95 597298e` (17 files, +823/−94) |
| CHANGELOG | The new Antigravity entry. Earlier entries are unchanged (append-only respected). |
| Authoritative docs | No change to `research/experiments/`, `configs/`, research questions or gap files (`git diff eb49c95 597298e --stat` on those paths is empty) |
| Python pipeline | Read `adb_collector.py`, `run_characterization.py`, `collectors.py` and `report_generator.py` |
| Android app | Read `MainActivity.kt`, `Collectors.kt`, the manifest and the Gradle files |
| Tests | `python -m pytest -q` → **278 passed** |
| Connected path | A scratch fake `adb` script, kept outside the repo, was put first on `PATH`; its responses are synthetic. Nothing from it was committed, and it is **not device evidence**. |
| Dry run / ADB missing | Real `run_characterization(dry_run=True)` with no `adb` installed |
| Android build | `./gradlew clean assembleDebug` attempted |

## 2. Runtime evidence gathered in this audit (scratch only)

| Scenario | Result |
| :-- | :-- |
| Fake `adb`, device state `device`, no flags | Run completes (R-01 resolved). The evidence directory holds 13 files plus `manifest.json`. VERIFIED: manufacturer, model, total RAM, soc_model, api_level, release, variant_check, cpu_core_count, device-wide CPU, `adb_atrace_profiling`, thermal zones. **NOT_TESTED despite evidence files existing:** battery level, voltage, temperature, current; cpufreq; available memory; camera; `temperature_battery`. |
| Same run: side effect | **`research/experiments/device_capability_matrix.md` was modified.** The Manufacturer and Model rows became `ReportStatus.VERIFIED` with run-relative evidence paths, and the device reported `STUB`. The change was reverted after the audit. |
| `--require-device` with `unauthorized` / `offline` / ADB missing | `RuntimeError` naming the state. **No fallback.** |
| `--require-device` and `--dry-run` together, device connected | **Silently runs as a dry run** (`adb_connected: false`). The contradictory flags are not rejected. |
| `dry_run=True`, `adb` absent | 58 results NOT_TESTED / NOT YET VERIFIED, 1 EXTERNAL_REQUIRED; 0 VERIFIED. `adb_connection_status: ADB_MISSING`; `charging: null`; `network: NOT_TESTED`. Energy: `selected_level: null`, `absolute_energy_claimed: false`. |
| `pytest` | 278 passed. **Side effect:** leaves an untracked `research/results/device_characterization/run_20261005_120000/` containing a synthetic run with `adb_connected: true` and identity VERIFIED (removed after the audit). |
| E2E suite with the clock set to 2026-10-06 | **1 failed, 5 passed.** `test_full_connected_path_schema_and_evidence_validation` raises the run-id date ValueError. |
| `sh ./gradlew clean assembleDebug` | `Error: Unable to access jarfile …/gradle/wrapper/gradle-wrapper.jar` |
| System Gradle 8.14.3 | Plugin `com.android.application` 8.2.2 not resolvable. `dl.google.com` is blocked (403) in this environment, and there is no Android SDK. |

**Android build: BUILD NOT EXECUTED — ENVIRONMENT LIMITATION.** This audit makes no claim that the APK builds. Separately from the environment limits, the committed wrapper cannot run on any machine as committed (see R-05).

## 3. Status of R-01 to R-14

| ID | Priority | Status | Evidence |
| :-- | :-- | :-- | :-- |
| R-01 | P0 | **FIXED** | `adb_collector.collect_raw_evidence_and_observations()` writes `observed_props.json`, `commands.log` and `manifest.json` (SHA-256 and size per file). The fake-`adb` run completes, and every VERIFIED ref resolves. Residual: the validator checks that files exist but never re-checks the manifest hashes (P-05). |
| R-02 | P0 | **FIXED** | `probe_profiling_capability()` runs `adb shell atrace --list_categories` and writes exit code, stdout and stderr to `atrace_evidence.txt`. The flag is True only when exit code is 0 and stdout is non-empty. Failure → False (tested). |
| R-03 | P1 | **PARTIALLY_FIXED** | Fixed: `get_connection_status()` returns the six states; `--require-device` fails loudly; every command is logged to `commands.log`; the connection status is recorded in `conditions`. Not fixed: (a) a failed probe still drops the key, giving NOT_TESTED instead of ERROR with the message; (b) the runner has no option to pass a serial, so MULTIPLE_DEVICES cannot be resolved and the serial used is not recorded; (c) a `no permissions` device line is classified as NO_DEVICE; (d) `--require-device` together with `--dry-run` silently runs a dry run. |
| R-04 | P1 | **PARTIALLY_FIXED** | The probes are executed and their evidence saved, but the parsed keys do not reach the collectors (P-03). The ADB parser writes `battery_level_percent`, `battery_voltage`, `battery_temperature`, `battery_current_now`, `cpu_scaling_cur_freq`, `gpu_clock_hz` and `available_memory_mb`; the collectors still report these as NOT_TESTED. The host never pulls the app's JSON (no `adb pull` or `logcat` call anywhere), and the Kotlin `evidence_ref`s cite `evidence/android_app_evidence.json`, which the host never writes. |
| R-05 | P1 | **PARTIALLY_FIXED** | Fixed: `settings.gradle.kts`; pinned AGP 8.2.2, Kotlin 1.9.22 and Gradle 8.5; manifest `package` attribute removed. Not fixed: `gradle/wrapper/gradle-wrapper.jar` is absent. `gradlew` is a non-standard stub, committed as mode 100644 (not executable), and it calls an undefined `die`. Running it fails immediately. |
| R-06 | P1 | **FIXED** | E-1 and E-2 values are always `None`; the injected `selected_level` override is removed (an injected `'E-3'` is ignored); the `E1_feasible=True` path no longer crashes. `absolute_energy_claimed` stays false. |
| R-07 | P1 | **PARTIALLY_FIXED** | Fixed: charging and network now come from `dumpsys battery` and `settings get global airplane_mode_on` (None or NOT_TESTED when unprobed), and evidence is hashed. Not fixed: `soc_model` falls back to `ro.board.platform` but still cites `getprop_evidence.txt#ro.soc.model`. `ro.soc.model` exists only from API 31, so on the OPPO (Android 9/10) the citation will name a key that is absent (P-04). |
| R-08 | P2 | **PARTIALLY_FIXED** | The code window is now 2700–3300 MB, matching the earlier CHANGELOG. Still open: (a) the protocol (§2, line 53) specifies a **nearest-to-3 GB-nominal** rule, which is not a fixed window; (b) the window is hard-coded in `collectors.py`, not set in `configs/` (AGENTS.md §1.4); (c) a mismatch yields a non-blocking `AVAILABLE` "DISAGREEMENT" record, although protocol line 51 says it blocks sign-off. |
| R-09 | P2 | **PARTIALLY_FIXED** | The raw value is now kept in `notes`. A current of 0 is still accepted as AVAILABLE 0.0 mA (checked directly). No code sets `current_now_is_sentinel`. The ADB key `battery_current_now` is never read, and the Kotlin app does not read `BATTERY_PROPERTY_CURRENT_NOW`. |
| R-10 | P2 | **FIXED** | `mock_observed` together with a connected run raises ValueError. In dry runs `is_real_device_observation` is forced to False after the mock is merged. |
| R-11 | P2 | **PARTIALLY_FIXED** | On an exception, `characterization.json` is deleted. But the write is not atomic (no temporary file and rename). The evidence directory is left behind when the run fails. With `overwrite=True` a failure deletes nothing, so a truncated file can remain. |
| R-12 | P2 | **PARTIALLY_FIXED** | Six tests were added and pass today. However: the full-path test replaces `collect_raw_evidence_and_observations` entirely, so the parser → collector mapping is never exercised (which is how P-03 went undetected). It writes into the real results directory (P-02). It is date-locked. There is no test for a probe failure turning into ERROR, for `OFFLINE`, or for `ADB_MISSING`. |
| R-13 | P3 | **NOT_FIXED** | The earlier inaccuracies were not addressed, and the new entry adds new ones: "Reproducible Gradle build setup committed" (false: the wrapper jar is missing); "Enforced atomic write" (the write is not atomic); "comprehensive end-to-end" (the collector mapping is mocked out). See P-07. |
| R-14 | P3 | **FIXED** | `run_20261005_100000/README.txt` and `run_20261006_100000/README.txt` state "Pre-audit dry run, not device evidence; folder name does not reflect actual run date." |

Summary: **5 FIXED** (R-01, R-02, R-06, R-10, R-14); **8 PARTIALLY_FIXED** (R-03, R-04, R-05, R-07, R-08, R-09, R-11, R-12); **1 NOT_FIXED** (R-13).

## 4. New findings (corrections for Antigravity; not implemented by Claude)

| ID | Priority | File / function | Issue | Impact | Required correction | Required test |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| P-01 | **P0** | `src/monitoring/characterization/report_generator.py` → `process_run()` → `update_device_capability_matrix()` | Every connected run rewrites the authoritative `research/experiments/device_capability_matrix.md`. (1) The status is written as `ReportStatus.VERIFIED` (enum repr). (2) The observed manufacturer and model are not compared with the known specification, so any device turns the "OPPO A5 2020" rows VERIFIED. (3) It runs after one run, ignoring the two-run, separate-day, reboot requirement. (4) The evidence path has no run ID. | Unverified or wrong-device data is written into the research matrix. One run on the wrong unit, or a fake `adb`, is enough. | Do not write the authoritative matrix from `process_run`. Write a per-run proposed-matrix file under the run directory instead. Promote it to the matrix only through an explicit step that requires two valid runs (`compare_repeat_runs` passing) and an identity match with `known_specification`. Write `.value` for the status and run-qualified evidence paths. | Connected fake-`adb` run with manufacturer ≠ OPPO → matrix unchanged and an identity-mismatch finding. Single valid run → matrix unchanged. Two valid runs → statuses written as `VERIFIED` (not `ReportStatus.VERIFIED`) with run-qualified paths. |
| P-02 | **P1** | `tests/test_device_characterization_connected_e2e.py` → `test_full_connected_path_schema_and_evidence_validation` | Writes a synthetic run with `adb_connected: true` and identity VERIFIED to the real `research/results/device_characterization/run_20261005_120000/`, with `overwrite=True`. Git does not ignore this path. The hard-coded run-id date fails the F-02 guard on any other day. | Synthetic data can be committed and mistaken for device evidence, and a real run with the same ID could be overwritten. The suite breaks from 2026-10-06. | Point `results_directory` at `tmp_path` through a temporary config. Derive the run ID from the current UTC date or freeze the clock. Never use `overwrite=True` against repository paths. | After `pytest`, `git status --porcelain research/` is empty. The suite passes with the clock set to another date. |
| P-03 | **P1** | `scripts/device_characterization/adb_collector.py` → `parse_dumpsys_battery()`, `collect_raw_evidence_and_observations()`; `src/monitoring/characterization/collectors.py` → Battery, Memory, CPU, GPU, Thermal and Camera collectors; host retrieval of app output | Parser keys do not match collector keys (e.g. `battery_current_now` vs `current_now_ua`). Battery, cpufreq, available memory and battery temperature stay NOT_TESTED although their evidence was collected. `media.camera` output is not parsed. The app JSON is never retrieved, and its `evidence/android_app_evidence.json` refs point at a file nobody writes. Collector evidence refs such as `battery_evidence.json` name files the host never writes. If the keys were aligned without fixing these refs, connected runs would abort validation. | Most protocol capabilities cannot be characterized even with the device connected. | Align a single key contract between the parser and the collectors, and cite the files that actually exist (e.g. `battery_dumpsys_evidence.txt#level`). Add a host step that runs `adb pull` on the app's `getExternalFilesDir()/characterization_output.json` into `evidence/android_app_evidence.json` (hashed in the manifest) and merges it. A `logcat` line is not a reliable channel for large JSON. | Fake-`adb` E2E test **using the real collector** (no mocking of `collect_raw_evidence_and_observations`): each metric whose probe succeeded is AVAILABLE with a resolving ref; each failed probe is ERROR. |
| P-04 | P2 | `collectors.py` → `DeviceIdentityCollector` (`soc_model`) | The value may come from `ro.board.platform`, but the citation always names `ro.soc.model`. | Wrong provenance on the actual device (API < 31). | Record which property supplied the value and cite that property. | getprop without `ro.soc.model` → the ref names `ro.board.platform`. |
| P-05 | P2 | `report_generator.py` → `validate_characterization_record()` | The manifest SHA-256 values are never verified. | Evidence edited after the run still validates. | Recompute and compare hashes for every manifest entry and every cited file. | Edit one evidence file after the run → validation error. |
| P-06 | P2 | `run_characterization.py` → `run_characterization()`, `main()`; `adb_collector.get_connection_status()` | `--require-device` with `--dry-run` silently runs a dry run. There is no `--serial` option. `no permissions` is classified as NO_DEVICE. A failed probe → NOT_TESTED, not ERROR (R-03 residue). | An intended device run can still degrade silently; with several devices attached, the target cannot be chosen. | Reject the contradictory flags. Add `--serial`, pass it to `ADBCollector`, and record it in `conditions`. Classify `no permissions`. Map a failed probe to ERROR with stderr. | One test per connection state, the flag-conflict test, and a probe-failure → ERROR test. |
| P-07 | P3 | `docs/agent_sync/CHANGELOG.md` (next entry) | The PR #24 entry overstates the work: reproducible build, atomic write, comprehensive E2E. | The record misleads the next agent. | The next Antigravity entry should correct these statements (append-only; do not edit the old entry). | — |

R-05 required test: on a machine with the Android SDK, run `./gradlew clean assembleDebug` from a fresh clone and record the output. The repo needs the real wrapper (`gradle wrapper --gradle-version 8.5` generates `gradlew`, `gradlew.bat` and `gradle-wrapper.jar`), with `gradlew` committed as executable. Committing `gradle-wrapper.jar` is standard practice, but it is a binary, so the user must explicitly approve it under AGENTS.md.

## 5. Specific checks

- **No-fake-zero:** dry run → every non-AVAILABLE value is null. Energy E-1 and E-2 are null in every path. The one zero risk is battery current 0 accepted as a real value (R-09).
- **Mock isolation:** passes (R-10).
- **Synthetic vs real evidence:** the E2E test module's docstring labels its outputs as TEST/MOCK. Its full-path test nevertheless writes them into the real results tree with `adb_connected: true` (P-02). The fake-`adb` outputs from this audit were kept in scratch and are not evidence.
- **Provenance:** run records carry the git commit, config SHA-256, Python and ADB versions, connection status and boot_id. Gaps: no device serial, no hash re-verification, wrong `soc_model` key on fallback.
- **Research boundaries:** PR #24 changes no research question, gap, hypothesis, C1–C4, R0–R3, r*, energy threshold, calibration binning, time budget or decision-register entry. Step 10E has not been started. No OPPO capability is marked VERIFIED in the repository.

## 6. Assumptions

- The fake `adb` script models the shape of real `adb` output only. Real OPPO output, such as the `dumpsys battery` field names on ColorOS, may differ. That is a further reason for P-03's test to use captured fixtures once a real run exists.
- "Ready" means ready to start the two physical characterization runs. It does not mean any capability has been established.

## 7. Next action

1. Antigravity: fix P-01, P-02 and P-03 (blocking), then R-05 (wrapper, pending the user's approval of the jar), then P-04 to P-07 and the residues in R-03, R-08, R-09, R-11 and R-12. Append a CHANGELOG entry.
2. Claude Code: re-review.
3. Then physical OPPO A5 2020 (3 GB) characterization: two runs on separate days with a reboot in between.

Step 10E not started.
