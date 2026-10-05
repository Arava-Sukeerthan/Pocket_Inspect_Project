# Step 10D — Android Characterization Module (`mobile/characterization/`)

Android Kotlin module for on-device capability checks and telemetry collection on the OPPO A5 2020 experimental platform.

## Architecture

- `minSdk` <= 28
- `targetSdk` >= 28
- Every API 29+ feature (`PowerManager.getCurrentThermalStatus`, `Build.SOC_MODEL`, `Build.VERSION.SDK_INT >= 29`) is guarded by explicit SDK gates.
- Below the gate, state is `API_UNSUPPORTED` with `value = null` (no fake zeros).
- Outputs schema-valid JSON matching `device_characterization_schema.json`.

## Components

1. `DeviceIdentityCollector.kt`
2. `AndroidCapabilityCollector.kt`
3. `BatteryTelemetryCollector.kt`
4. `MemoryTelemetryCollector.kt`
5. `CPUTelemetryCollector.kt`
6. `GPUTelemetryCollector.kt`
7. `ThermalTelemetryCollector.kt`
8. `CameraCapabilityCollector.kt`
9. `InferenceBackendCapabilityCollector.kt`
10. `ProfilingCapabilityCollector.kt`
11. `EnergyMeasurementCapabilityChecker.kt`
12. `CharacterizationRunner.kt`
