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
- **Python 3** on `PATH` (`python3`; `python` on Windows; override with `-Ppocketinspect.python=<exe>`): the build runs
  the repository's deterministic reference-graph generator (Gradle task `generateReferenceGraph`, standard library only,
  no network access).
- **Runtime libraries** (Maven Central): `org.tensorflow:tensorflow-lite`, `-gpu`, `-gpu-api` 2.16.1 and
  `com.microsoft.onnxruntime:onnxruntime-android` 1.30.0, declared once in `build.gradle.kts`.

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

The Android characterization client consists of 7 Kotlin source files:
1. `MainActivity.kt`: entry point; runs every probe on a background thread (the camera capture check waits for camera callbacks), writes the report file and logs it.
2. `Collectors.kt`: record helpers; identity (incl. storage), memory (incl. `lowMemory`, `threshold`, heap, PSS), thermal status and listener, battery broadcast values and `BatteryManager` properties (`CURRENT_NOW`, `CURRENT_AVERAGE`, `CHARGE_COUNTER`, `ENERGY_COUNTER`; the unsupported sentinel becomes UNAVAILABLE, never a value).
3. `SystemProbes.kt`: platform services (each obtained **and** exercised; `SecurityException` is PERMISSION_REQUIRED), process CPU time, EGL `GL_RENDERER`/`GL_VENDOR` and Vulkan feature, clock monotonicity/resolution, `android.os.Trace`.
4. `CameraProbes.kt`: real camera IDs (`getCameraIdList()`), per-camera `CameraCharacteristics`, and the advertised-vs-honoured manual-control capture check.
5. `BackendProbes.kt`: backend capability checks with the deterministic reference graph (see below).
6. `CharacterizationRunner.kt`: runs the collectors and writes the report sections (`device_identity`, `memory_telemetry`, `thermal_capability`, `battery_telemetry`, `service_capability`, `cpu_telemetry`, `gpu_capability`, `profiling_capability`, `camera_telemetry`, `backend_capability`). The host bridge (`APP_SECTION_METRICS` in `scripts/device_characterization/adb_collector.py`) consumes exactly these sections.
7. `AppJsonLogFormatter.kt`: Pure-JVM formatter that logs the report one record per logcat line, with the report file's SHA-256.

Unit test: `src/test/kotlin/.../AppJsonLogFormatterTest.kt` (JUnit 4, no device needed).

## Backend capability checks (`backend_capability` section)

Scope (researcher decision 2026-10-07; `inference_backend_check` in `configs/device_characterization.yaml`):
LiteRT / TensorFlow Lite CPU (XNNPACK), GPU delegate, NNAPI delegate; ONNX Runtime Mobile CPU and NNAPI execution
provider. No other runtime is approved. Capability only: no latency, throughput or accuracy is recorded.

The reference graph (CONV → DEPTHWISE CONV → AVERAGE POOL → FULLY CONNECTED → SOFTMAX, input `[1,8,8,3]`, output
`[1,4]`, variants fp32 / fp16 / int8) is generated at build time from `src/monitoring/characterization/reference_graph.py`
into the APK assets `reference_graph/`. No model binary is committed; the SHA-256 of every artifact is pinned in the
config. Check the pins with `python scripts/device_characterization/generate_reference_graph.py --check`.

Per backend the app writes raw observations only; the host decides every status:

| Record | Content |
| :-- | :-- |
| `backend_runtime` | runtime initialised, runtime-reported version (null if not reported), declared dependency, requested delegate constructed (GPU: also the compatibility-list answer) or listed (ORT `getAvailableProviders()`) |
| `reference_graph_check` (per variant) | SHA-256 of the loaded bytes, graph load, one inference on the manifest input, raw output (shape, dtype, values), delegation evidence |

Delegation evidence: TFLite — execution-plan length vs graph node count (XNNPACK is disabled for the GPU and NNAPI
backends so a shorter plan can only come from the requested delegate), plus this process's `tflite` log lines;
ONNX Runtime — the session profile reduced to (node, operator, execution provider), with timing fields discarded.
The NNAPI accelerator identity is not observable through these Java APIs, so NNAPI delegation is never VERIFIED.

## Before launching the app: CAMERA runtime permission

The manual-control check opens each camera. The app targets API 28, so CAMERA is a runtime permission. Grant it
before launching the app, otherwise the check is recorded as PERMISSION_REQUIRED (never as honoured):

```bash
adb shell pm grant org.pocketinspect.characterization android.permission.CAMERA
adb shell am start -n org.pocketinspect.characterization/.MainActivity
```

Wait for the `END run_id=...` logcat line before running the host characterization.

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
is larger than one entry (about 4.3 KB on an OPPO CPH1931 before the correction round, larger now), so it is not logged as one entry. Under tag `POCKETINSPECT_APP_JSON` the
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
| `CameraManager.getCameraIdList()` succeeds | `camera_id_list` AVAILABLE (the exact ID strings) and `camera_count` |
| Per camera ID | `lens_facing`, `hardware_level`, `available_capabilities`, `manual_exposure_advertised`, stream configurations, FPS ranges, AF modes, minimum focus distance, exposure/ISO ranges, AWB modes, AE/AWB lock, physical IDs, video profiles (each with `camera_id`) |
| A characteristic key returns null | that record UNAVAILABLE, value null |
| `MANUAL_SENSOR` not advertised | `manual_exposure_advertised` UNAVAILABLE; `manual_control_honoured` UNAVAILABLE |
| `MANUAL_SENSOR` advertised, CAMERA granted | `manual_control_honoured` AVAILABLE with requested and `CaptureResult` exposure/sensitivity; the host decides honoured / NOT HONOURED: exposure and sensitivity each within ±5 % of the requested value (`camera_manual_control_check` in `configs/device_characterization.yaml`) |
| CAMERA not granted | `manual_control_honoured` and `capture_sensor_timestamp` PERMISSION_REQUIRED |
| `getCameraIdList()` throws | `camera_probe` ERROR with the exception message |
| No `CameraManager` system service | `camera_probe` UNAVAILABLE |

No camera value is inferred when a probe does not return one: IDs are never generated from a count, and lens facing
is never defaulted.
