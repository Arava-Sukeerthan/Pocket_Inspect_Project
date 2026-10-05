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
```

## Architecture

- `minSdk` <= 28
- `targetSdk` >= 28
- Every API 29+ feature (`PowerManager.getCurrentThermalStatus`, `Build.SOC_MODEL`, `Build.VERSION.SDK_INT >= 29`) is guarded by explicit SDK gates.
- Below the gate, state is `API_UNSUPPORTED` with `value = null` (no fake zeros).
- Outputs schema-valid JSON matching `device_characterization_schema.json`.

## Components

The Android characterization client consists of 3 Kotlin source files:
1. `MainActivity.kt`: Android UI activity and entry point for initiating on-device characterization tasks.
2. `Collectors.kt`: On-device telemetry and capability collectors for Android services and hardware properties.
3. `CharacterizationRunner.kt`: Runner for executing characterization probes and outputting canonical JSON results to app file storage.


