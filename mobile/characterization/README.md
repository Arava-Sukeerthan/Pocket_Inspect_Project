# Step 10D — Android Characterization Module (`mobile/characterization/`)

Android Kotlin module for on-device capability checks and telemetry collection on the OPPO A5 2020 experimental platform.

## Environmental Prerequisites (R-05)

To build this Android module from source, the environment requires:
- **JDK Version**: Java Development Kit (JDK) 17 (`JAVA_HOME` pointing to JDK 17)
- **Android SDK**: `ANDROID_HOME` or `ANDROID_SDK_ROOT` environment variable configured
- **SDK Platforms & Build Tools**: Android SDK Platform 34, SDK Build-Tools 34.0.0
- **Gradle Version**: Gradle 8.5 (managed via `./gradlew` standard wrapper)
- **Android Gradle Plugin (AGP)**: Version 8.2.2
- **Kotlin Version**: 1.9.22

Build Commands:
```bash
./gradlew --version
./gradlew clean assembleDebug
./gradlew testDebugUnitTest   # JVM unit tests (AppJsonLogFormatterTest)
```

## Architecture

- `minSdk` <= 28
- `targetSdk` >= 28
- Every API 29+ feature (`PowerManager.getCurrentThermalStatus`, `Build.SOC_MODEL`, `Build.VERSION.SDK_INT >= 29`) is guarded by explicit SDK gates.
- Below the gate, state is `API_UNSUPPORTED` with `value = null` (no fake zeros).
- Outputs schema-valid JSON matching `device_characterization_schema.json`.

## Components

The Android characterization client consists of 4 Kotlin source files:
1. `MainActivity.kt`: Android UI activity and entry point for initiating on-device characterization tasks; writes the report file and logs it.
2. `Collectors.kt`: On-device telemetry and capability collectors for Android services and hardware properties.
3. `CharacterizationRunner.kt`: Runner for executing characterization probes and outputting canonical JSON results to app file storage.
4. `AppJsonLogFormatter.kt`: Pure-JVM formatter that logs the report one record per logcat line, with the report file's SHA-256.

Unit test: `src/test/kotlin/.../AppJsonLogFormatterTest.kt` (JUnit 4, no device needed).

## Evidence artifact and where to find it

The **evidence artifact** is the report file the app writes on every launch. The same bytes are written to two places:

| Location | Path on the device | How to read it |
| :-- | :-- | :-- |
| App internal storage | `files/characterization_output.json` (absolute path printed in the `ARTIFACT` log line) | `adb shell run-as org.pocketinspect.characterization cat files/characterization_output.json` (debug build) |
| App external storage | `/sdcard/Android/data/org.pocketinspect.characterization/files/characterization_output.json` | `adb shell cat <path>` or `adb pull <path>` |

There is **no** `files/evidence/android_app_evidence.json` on the device. `evidence/android_app_evidence.json` is
the name the **host** gives the retrieved copy inside its run directory
(`research/results/device_characterization/<run_id>/evidence/android_app_evidence.json`, hashed in `manifest.json`).
Every `evidence_ref` of the form `evidence/android_app_evidence.json#<metric>` is relative to that host run directory.
`scripts/device_characterization/adb_collector.py` (`retrieve_android_app_output`) performs the retrieval.

## Logcat output (observation aid, not the evidence)

A logcat entry is limited to about 4 KB (`LOGGER_ENTRY_MAX_PAYLOAD` = 4068 bytes including the tag). The full report
is larger (about 4.3 KB on an OPPO CPH1931), so it is not logged as one entry. Under tag `POCKETINSPECT_APP_JSON` the
app logs, for each launch:

```
BEGIN run_id=<id> records=<n> bytes=<report bytes> sha256=<report sha256>
SECTION run_id=<id> section=<name> records=<k>          (or status=MISSING)
RECORD run_id=<id> n=<i>/<n> section=<name> <compact JSON of one record>
RECORD run_id=<id> n=<i>/<n> section=<name> part=<p>/<m> <slice>   (only if one record exceeds 3000 bytes)
ARTIFACT run_id=<id> path=<device path> bytes=<report bytes> sha256=<report sha256> host_copy=evidence/android_app_evidence.json
END run_id=<id> records=<n>
```

Capture with `adb logcat -d -s POCKETINSPECT_APP_JSON`. Each `RECORD` line comes only from the app's report, so it is
never mixed with system logs. The `sha256` in `BEGIN`/`ARTIFACT` is the SHA-256 of the file as written on the device.
When the host copy is transferred unchanged, it equals the hash listed for `evidence/android_app_evidence.json` in the
run's `manifest.json`; a mismatch means the copy differs from the device file and should be investigated. This check is
manual: the host pipeline does not read logcat. An empty camera section is logged as `section=camera_telemetry records=0`.

## Camera telemetry states

| Situation | Record |
| :-- | :-- |
| `CameraManager.getCameraIdList()` succeeds | `camera_count` AVAILABLE |
| Camera 0 reports `INFO_SUPPORTED_HARDWARE_LEVEL` | `camera_0_hardware_level` AVAILABLE |
| Camera 0 returns no hardware level | `camera_0_hardware_level` UNAVAILABLE, value null |
| `CameraManager` throws (e.g. `CameraAccessException`) | `camera_probe` ERROR with the exception message |
| No `CameraManager` system service | `camera_probe` UNAVAILABLE |

No camera value is inferred when a probe does not return one.


