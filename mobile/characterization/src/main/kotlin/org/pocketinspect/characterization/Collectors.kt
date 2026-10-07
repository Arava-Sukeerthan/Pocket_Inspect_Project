package org.pocketinspect.characterization

import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import android.os.Debug
import android.os.Environment
import android.os.PowerManager
import android.os.StatFs
import java.text.SimpleDateFormat
import java.util.Date
import java.util.TimeZone

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

/**
 * One app observation. The host (scripts/device_characterization/adb_collector.py) consumes `metric`, `state`,
 * `value`, `unit`, `error_message`, `notes`, `details` and, for per-camera records, `camera_id`. The host
 * recomputes `report_status`/`verified` from its own rules; the app's values are informative only.
 * A state other than AVAILABLE always has value = null (no fake zeros).
 */
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
    val notes: String? = null,
    val camera_id: String? = null,
    val details: Any? = null
)

fun getIsoTimestamp(): String {
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")
    sdf.timeZone = TimeZone.getTimeZone("UTC")
    return sdf.format(Date())
}

// ---------------------------------------------------------------------------------------------------------
// Record helpers. Every evidence_ref names the host copy of this report (AppJsonLogFormatter.HOST_EVIDENCE_PATH).
// ---------------------------------------------------------------------------------------------------------

fun observed(
    metric: String, value: Any, source: String, unit: String? = null, minApi: Int? = null,
    cameraId: String? = null, details: Any? = null, notes: String? = null
) = CapabilityResult(
    metric = metric,
    state = RuntimeState.AVAILABLE.name,
    report_status = ReportStatus.AVAILABLE.name,
    value = value,
    unit = unit,
    source = source,
    min_api = minApi,
    verification_method = "android_api",
    observed_at = getIsoTimestamp(),
    evidence_ref = "evidence/android_app_evidence.json#$metric",
    notes = notes,
    camera_id = cameraId,
    details = details
)

fun notAvailable(
    metric: String, state: RuntimeState, source: String, notes: String? = null, errorMessage: String? = null,
    minApi: Int? = null, cameraId: String? = null, details: Any? = null
) = CapabilityResult(
    metric = metric,
    state = state.name,
    report_status = if (state == RuntimeState.ERROR) ReportStatus.NOT_YET_VERIFIED.name else ReportStatus.UNAVAILABLE.name,
    value = null,
    source = source,
    min_api = minApi,
    verification_method = "android_api",
    observed_at = getIsoTimestamp(),
    evidence_ref = "evidence/android_app_evidence.json#$metric",
    error_message = errorMessage,
    notes = notes,
    camera_id = cameraId,
    details = details
)

fun failure(metric: String, source: String, e: Throwable, cameraId: String? = null): CapabilityResult =
    if (e is SecurityException) {
        notAvailable(metric, RuntimeState.PERMISSION_REQUIRED, source,
            errorMessage = "${e.javaClass.simpleName}: ${e.message}", cameraId = cameraId)
    } else {
        notAvailable(metric, RuntimeState.ERROR, source,
            errorMessage = "${e.javaClass.simpleName}: ${e.message}", cameraId = cameraId)
    }

/** Runs [probe]; a thrown exception becomes PERMISSION_REQUIRED (SecurityException) or ERROR, never a value. */
inline fun guarded(metric: String, source: String, cameraId: String? = null, probe: () -> CapabilityResult): CapabilityResult =
    try {
        probe()
    } catch (e: Exception) {
        failure(metric, source, e, cameraId)
    }

class DeviceIdentityCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()

        results.add(observed("manufacturer", Build.MANUFACTURER, "Build.MANUFACTURER"))
        results.add(observed("model", Build.MODEL, "Build.MODEL"))

        if (Build.VERSION.SDK_INT >= 31) {
            results.add(observed("soc_model", Build.SOC_MODEL, "Build.SOC_MODEL", minApi = 31))
        } else {
            results.add(notAvailable("soc_model", RuntimeState.API_UNSUPPORTED, "Build.SOC_MODEL", minApi = 31,
                notes = "Build.SOC_MODEL requires API >= 31"))
        }

        // Storage (matrix §1): StatFs on the data partition.
        results.add(guarded("storage_total_bytes", "StatFs(Environment.getDataDirectory())") {
            val stat = StatFs(Environment.getDataDirectory().path)
            observed("storage_total_bytes", stat.totalBytes, "StatFs(Environment.getDataDirectory()).getTotalBytes()",
                unit = "bytes")
        })
        return results
    }
}

class MemoryTelemetryCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()
        val am = context.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
        if (am != null) {
            val memInfo = ActivityManager.MemoryInfo()
            am.getMemoryInfo(memInfo)
            results.add(observed("total_ram_mb", memInfo.totalMem / (1024 * 1024),
                "ActivityManager.MemoryInfo.totalMem", unit = "MB"))
            results.add(observed("available_memory_mb", memInfo.availMem / (1024 * 1024),
                "ActivityManager.MemoryInfo.availMem", unit = "MB"))
            // B3: the platform low-memory flag and its threshold (not a /proc/meminfo field).
            results.add(observed("low_memory_flag", memInfo.lowMemory, "ActivityManager.MemoryInfo.lowMemory",
                unit = "boolean"))
            results.add(observed("memory_threshold_mb", memInfo.threshold / (1024 * 1024),
                "ActivityManager.MemoryInfo.threshold", unit = "MB"))
        } else {
            for (m in listOf("low_memory_flag", "memory_threshold_mb")) {
                results.add(notAvailable(m, RuntimeState.UNAVAILABLE, "ActivityManager.MemoryInfo",
                    notes = "ActivityManager system service not available"))
            }
        }

        results.add(guarded("app_heap_allocated_mb", "Runtime.totalMemory() - Runtime.freeMemory()") {
            val rt = Runtime.getRuntime()
            observed("app_heap_allocated_mb", (rt.totalMemory() - rt.freeMemory()) / (1024 * 1024),
                "Runtime.totalMemory() - Runtime.freeMemory()", unit = "MB")
        })
        results.add(guarded("app_pss_kb", "Debug.getMemoryInfo()") {
            val mi = Debug.MemoryInfo()
            Debug.getMemoryInfo(mi)
            observed("app_pss_kb", mi.totalPss, "Debug.getMemoryInfo(Debug.MemoryInfo).getTotalPss()", unit = "kB")
        })
        return results
    }
}

class ThermalTelemetryCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()
        if (Build.VERSION.SDK_INT < 29) {
            results.add(notAvailable("thermal_status_api", RuntimeState.API_UNSUPPORTED,
                "PowerManager.getCurrentThermalStatus()", minApi = 29, notes = "getCurrentThermalStatus requires API >= 29"))
            results.add(notAvailable("thermal_status_listener", RuntimeState.API_UNSUPPORTED,
                "PowerManager.addThermalStatusListener()", minApi = 29, notes = "Thermal status listener requires API >= 29"))
            return results
        }
        val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager
        if (pm == null) {
            results.add(notAvailable("thermal_status_api", RuntimeState.UNAVAILABLE,
                "PowerManager.getCurrentThermalStatus()", minApi = 29, notes = "PowerManager system service not available"))
            results.add(notAvailable("thermal_status_listener", RuntimeState.UNAVAILABLE,
                "PowerManager.addThermalStatusListener()", minApi = 29, notes = "PowerManager system service not available"))
            return results
        }
        results.add(guarded("thermal_status_api", "PowerManager.getCurrentThermalStatus()") {
            observed("thermal_status_api", pm.currentThermalStatus, "PowerManager.getCurrentThermalStatus()", minApi = 29)
        })
        // Listener registration (protocol §5.1). Callback delivery under a thermal change is not exercised.
        results.add(guarded("thermal_status_listener", "PowerManager.addThermalStatusListener()") {
            val listener = PowerManager.OnThermalStatusChangedListener { }
            pm.addThermalStatusListener(context.mainExecutor, listener)
            pm.removeThermalStatusListener(listener)
            observed("thermal_status_listener", "registered and removed", "PowerManager.addThermalStatusListener()",
                minApi = 29)
        })
        return results
    }
}

class BatteryTelemetryCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()
        val batteryStatus: Intent? = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))

        if (batteryStatus != null) {
            val level = batteryStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
            val scale = batteryStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
            val voltage = batteryStatus.getIntExtra(BatteryManager.EXTRA_VOLTAGE, -1)
            val temp10 = batteryStatus.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, Int.MIN_VALUE)
            val statusInt = batteryStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1)

            results.add(if (level >= 0 && scale > 0) observed("battery_level_percent", (level * 100) / scale,
                "BatteryManager.EXTRA_LEVEL / EXTRA_SCALE", unit = "percent")
            else notAvailable("battery_level_percent", RuntimeState.UNAVAILABLE, "BatteryManager.EXTRA_LEVEL",
                notes = "EXTRA_LEVEL/EXTRA_SCALE missing from ACTION_BATTERY_CHANGED"))
            results.add(if (voltage > 0) observed("battery_voltage", voltage, "BatteryManager.EXTRA_VOLTAGE", unit = "mV")
            else notAvailable("battery_voltage", RuntimeState.UNAVAILABLE, "BatteryManager.EXTRA_VOLTAGE",
                notes = "EXTRA_VOLTAGE missing or non-positive"))
            results.add(if (temp10 != Int.MIN_VALUE) observed("battery_temperature", temp10 / 10.0,
                "BatteryManager.EXTRA_TEMPERATURE", unit = "degC")
            else notAvailable("battery_temperature", RuntimeState.UNAVAILABLE, "BatteryManager.EXTRA_TEMPERATURE",
                notes = "EXTRA_TEMPERATURE missing from ACTION_BATTERY_CHANGED"))
            if (statusInt >= 0) {
                results.add(observed("is_charging", statusInt == BatteryManager.BATTERY_STATUS_CHARGING ||
                    statusInt == BatteryManager.BATTERY_STATUS_FULL, "BatteryManager.EXTRA_STATUS", unit = "boolean"))
            }
        }

        // B2: BatteryManager properties. With targetSdk >= 28 an unsupported property returns Integer.MIN_VALUE
        // (Long.MIN_VALUE for getLongProperty): recorded as UNAVAILABLE with the raw sentinel, never as a value.
        val bm = context.getSystemService(Context.BATTERY_SERVICE) as? BatteryManager
        val apiDetails = mapOf("sdk_int" to Build.VERSION.SDK_INT,
            "target_sdk" to context.applicationInfo.targetSdkVersion)
        val intProps = listOf(
            Triple("battery_property_current_now", BatteryManager.BATTERY_PROPERTY_CURRENT_NOW, "uA"),
            Triple("battery_property_current_average", BatteryManager.BATTERY_PROPERTY_CURRENT_AVERAGE, "uA"),
            Triple("battery_property_charge_counter", BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER, "uAh")
        )
        for ((metric, id, unit) in intProps) {
            val source = "BatteryManager.getIntProperty(${metric.removePrefix("battery_property_").uppercase()})"
            results.add(when {
                bm == null -> notAvailable(metric, RuntimeState.UNAVAILABLE, source,
                    notes = "BatteryManager system service not available")
                else -> guarded(metric, source) {
                    val raw = bm.getIntProperty(id)
                    if (raw == Int.MIN_VALUE) {
                        notAvailable(metric, RuntimeState.UNAVAILABLE, source, notes = "Unsupported-property sentinel",
                            details = apiDetails + mapOf("raw" to "Integer.MIN_VALUE", "sentinel" to true))
                    } else {
                        observed(metric, raw, source, unit = unit, details = apiDetails + mapOf("raw" to raw))
                    }
                }
            })
        }
        val energySource = "BatteryManager.getLongProperty(ENERGY_COUNTER)"
        results.add(when {
            bm == null -> notAvailable("battery_property_energy_counter", RuntimeState.UNAVAILABLE, energySource,
                notes = "BatteryManager system service not available")
            else -> guarded("battery_property_energy_counter", energySource) {
                val raw = bm.getLongProperty(BatteryManager.BATTERY_PROPERTY_ENERGY_COUNTER)
                if (raw == Long.MIN_VALUE) {
                    notAvailable("battery_property_energy_counter", RuntimeState.UNAVAILABLE, energySource,
                        notes = "Unsupported-property sentinel",
                        details = apiDetails + mapOf("raw" to "Long.MIN_VALUE", "sentinel" to true))
                } else {
                    observed("battery_property_energy_counter", raw, energySource, unit = "nWh",
                        details = apiDetails + mapOf("raw" to raw))
                }
            }
        })
        return results
    }
}
