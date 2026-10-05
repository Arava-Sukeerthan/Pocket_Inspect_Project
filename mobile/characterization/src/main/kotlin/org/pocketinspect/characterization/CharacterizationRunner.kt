package org.pocketinspect.characterization

import android.content.Context
import com.google.gson.GsonBuilder

class CharacterizationRunner(private val context: Context) {
    fun runAll(): String {
        val identity = DeviceIdentityCollector(context).collect()
        val memory = MemoryTelemetryCollector(context).collect()
        val thermal = ThermalTelemetryCollector(context).collect()
        val battery = BatteryTelemetryCollector(context).collect()
        val camera = CameraTelemetryCollector(context).collect()

        val report = mapOf(
            "run_id" to "android_run_${System.currentTimeMillis()}",
            "observed_at" to getIsoTimestamp(),
            "device_identity" to identity,
            "memory_telemetry" to memory,
            "thermal_capability" to thermal,
            "battery_telemetry" to battery,
            "camera_telemetry" to camera
        )

        val gson = GsonBuilder().setPrettyPrinting().create()
        return gson.toJson(report)
    }
}
