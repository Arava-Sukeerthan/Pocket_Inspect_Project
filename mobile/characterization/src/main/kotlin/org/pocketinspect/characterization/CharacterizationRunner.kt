package org.pocketinspect.characterization

import android.content.Context
import com.google.gson.GsonBuilder

class CharacterizationRunner(private val context: Context) {
    fun runAll(): String {
        val identity = DeviceIdentityCollector(context).collect()
        val thermal = ThermalTelemetryCollector(context).collect()

        val report = mapOf(
            "run_id" to "android_run_${System.currentTimeMillis()}",
            "device_identity" to identity,
            "thermal_capability" to thermal
        )

        val gson = GsonBuilder().setPrettyPrinting().create()
        return gson.toJson(report)
    }
}
