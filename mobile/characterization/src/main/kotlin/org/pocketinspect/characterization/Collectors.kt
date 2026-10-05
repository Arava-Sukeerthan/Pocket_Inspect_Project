package org.pocketinspect.characterization

import android.content.Context
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.os.BatteryManager
import android.os.Build
import android.os.PowerManager
import android.os.SystemClock
import java.io.File

enum class RuntimeState {
    AVAILABLE,
    UNAVAILABLE,
    PERMISSION_REQUIRED,
    API_UNSUPPORTED,
    EXTERNAL_REQUIRED,
    NOT_TESTED,
    ERROR
}

enum class ReportStatus {
    VERIFIED,
    AVAILABLE,
    CONDITIONALLY_AVAILABLE,
    UNAVAILABLE,
    REQUIRES_EXTERNAL_INSTRUMENTATION,
    REQUIRES_PILOT_VALIDATION,
    NOT_YET_VERIFIED
}

data class CapabilityResult(
    val metric: String,
    val state: String,
    val report_status: String,
    val value: Any? = null,
    val unit: String? = null,
    val source: String = "android_api",
    val min_api: Int? = null,
    val condition: String? = null,
    val verified: Boolean = false,
    val verification_method: String = "unverified",
    val evidence_ref: String? = null,
    val observed_at: String? = null,
    val error_message: String? = null,
    val notes: String? = null
)

class DeviceIdentityCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()
        val now = System.currentTimeMillis().toString()

        results.add(CapabilityResult(
            metric = "manufacturer",
            state = RuntimeState.AVAILABLE.name,
            report_status = ReportStatus.AVAILABLE.name,
            value = Build.MANUFACTURER,
            source = "Build.MANUFACTURER"
        ))

        results.add(CapabilityResult(
            metric = "model",
            state = RuntimeState.AVAILABLE.name,
            report_status = ReportStatus.AVAILABLE.name,
            value = Build.MODEL,
            source = "Build.MODEL"
        ))

        if (Build.VERSION.SDK_INT >= 31) {
            results.add(CapabilityResult(
                metric = "soc_model",
                state = RuntimeState.AVAILABLE.name,
                report_status = ReportStatus.AVAILABLE.name,
                value = Build.SOC_MODEL,
                source = "Build.SOC_MODEL",
                min_api = 31
            ))
        } else {
            results.add(CapabilityResult(
                metric = "soc_model",
                state = RuntimeState.API_UNSUPPORTED.name,
                report_status = ReportStatus.UNAVAILABLE.name,
                value = null,
                min_api = 31,
                notes = "Build.SOC_MODEL requires API >= 31"
            ))
        }

        return results
    }
}

class ThermalTelemetryCollector(private val context: Context) {
    fun collect(): CapabilityResult {
        return if (Build.VERSION.SDK_INT >= 29) {
            val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager
            val status = pm?.currentThermalStatus
            if (status != null) {
                CapabilityResult(
                    metric = "thermal_status_api",
                    state = RuntimeState.AVAILABLE.name,
                    report_status = ReportStatus.AVAILABLE.name,
                    value = status,
                    source = "PowerManager.getCurrentThermalStatus()",
                    min_api = 29
                )
            } else {
                CapabilityResult(
                    metric = "thermal_status_api",
                    state = RuntimeState.UNAVAILABLE.name,
                    report_status = ReportStatus.UNAVAILABLE.name,
                    value = null,
                    min_api = 29
                )
            }
        } else {
            CapabilityResult(
                metric = "thermal_status_api",
                state = RuntimeState.API_UNSUPPORTED.name,
                report_status = ReportStatus.UNAVAILABLE.name,
                value = null,
                min_api = 29,
                notes = "getCurrentThermalStatus requires API >= 29"
            )
        }
    }
}
