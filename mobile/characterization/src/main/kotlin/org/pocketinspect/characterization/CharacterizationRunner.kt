package org.pocketinspect.characterization

import android.content.Context
import android.os.Build
import com.google.gson.GsonBuilder

/**
 * Runs every on-device probe and returns the report JSON. Section names are the contract with the host bridge
 * (adb_collector.py APP_SECTION_METRICS) and with AppJsonLogFormatter.SECTIONS. Must not run on the main thread:
 * the camera capture check waits for camera callbacks.
 */
class CharacterizationRunner(private val context: Context) {
    fun runAll(): String {
        val report = linkedMapOf<String, Any>(
            "run_id" to "android_run_${System.currentTimeMillis()}",
            "observed_at" to getIsoTimestamp(),
            "app_procedure" to mapOf(
                "sdk_int" to Build.VERSION.SDK_INT,
                "target_sdk" to context.applicationInfo.targetSdkVersion,
                "clock_samples" to ProfilingCapabilityCollector.CLOCK_SAMPLES,
                "camera_target_exposure_ns" to CameraTelemetryCollector.TARGET_EXPOSURE_NS,
                "camera_capture_frames" to CameraTelemetryCollector.CAPTURE_FRAMES
            ),
            "device_identity" to DeviceIdentityCollector(context).collect(),
            "memory_telemetry" to MemoryTelemetryCollector(context).collect(),
            "thermal_capability" to ThermalTelemetryCollector(context).collect(),
            "battery_telemetry" to BatteryTelemetryCollector(context).collect(),
            "service_capability" to ServiceCapabilityCollector(context).collect(),
            "cpu_telemetry" to CpuTelemetryCollector().collect(),
            "gpu_capability" to GpuCapabilityCollector(context).collect(),
            "profiling_capability" to ProfilingCapabilityCollector().collect(),
            "camera_telemetry" to CameraTelemetryCollector(context).collect()
        )
        return GsonBuilder().setPrettyPrinting().create().toJson(report)
    }
}
