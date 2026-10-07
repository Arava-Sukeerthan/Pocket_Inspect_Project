package org.pocketinspect.characterization

import android.app.ActivityManager
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.camera2.CameraManager
import android.opengl.EGL14
import android.opengl.EGLConfig
import android.opengl.GLES20
import android.os.BatteryManager
import android.os.Build
import android.os.HardwarePropertiesManager
import android.os.PowerManager
import android.os.Process
import android.os.SystemClock
import android.os.Trace

/**
 * B1: platform services. Each service is obtained AND one minimal operation is performed. Obtaining a service
 * object is never taken as proof that its operations are permitted: a SecurityException is PERMISSION_REQUIRED.
 */
class ServiceCapabilityCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()

        results.add(serviceProbe("service_PowerManager", "getSystemService(POWER_SERVICE) + isPowerSaveMode()") {
            val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager ?: return@serviceProbe null
            "isPowerSaveMode() returned ${pm.isPowerSaveMode}"
        })
        results.add(serviceProbe("service_HardwarePropertiesManager",
            "getSystemService(HARDWARE_PROPERTIES_SERVICE) + getDeviceTemperatures(CPU, CURRENT)") {
            val hpm = context.getSystemService(Context.HARDWARE_PROPERTIES_SERVICE) as? HardwarePropertiesManager
                ?: return@serviceProbe null
            // Throws SecurityException unless the caller is device/profile owner or in VR mode.
            val temps = hpm.getDeviceTemperatures(HardwarePropertiesManager.DEVICE_TEMPERATURE_CPU,
                HardwarePropertiesManager.TEMPERATURE_CURRENT)
            "getDeviceTemperatures() returned ${temps.size} values"
        })
        results.add(serviceProbe("service_CameraManager", "getSystemService(CAMERA_SERVICE) + getCameraIdList()") {
            val cm = context.getSystemService(Context.CAMERA_SERVICE) as? CameraManager ?: return@serviceProbe null
            "getCameraIdList() returned ${cm.cameraIdList.size} IDs"
        })
        results.add(serviceProbe("service_ActivityManager", "getSystemService(ACTIVITY_SERVICE) + getMemoryInfo()") {
            val am = context.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager ?: return@serviceProbe null
            am.getMemoryInfo(ActivityManager.MemoryInfo())
            "getMemoryInfo() succeeded"
        })
        results.add(serviceProbe("service_BatteryManager",
            "getSystemService(BATTERY_SERVICE) + getIntProperty(BATTERY_PROPERTY_CAPACITY)") {
            val bm = context.getSystemService(Context.BATTERY_SERVICE) as? BatteryManager ?: return@serviceProbe null
            val cap = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
            "getIntProperty(CAPACITY) returned ${if (cap == Int.MIN_VALUE) "the unsupported sentinel" else cap}"
        })

        val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager
        results.add(if (pm == null) notAvailable("power_save_mode", RuntimeState.UNAVAILABLE, "PowerManager.isPowerSaveMode()",
            notes = "PowerManager system service not available")
        else guarded("power_save_mode", "PowerManager.isPowerSaveMode()") {
            observed("power_save_mode", pm.isPowerSaveMode, "PowerManager.isPowerSaveMode()", unit = "boolean")
        })
        return results
    }

    /** [operation] returns a description, or null when getSystemService returned null (UNAVAILABLE). */
    private inline fun serviceProbe(metric: String, source: String, operation: () -> String?): CapabilityResult =
        guarded(metric, source) {
            val outcome = operation()
            if (outcome == null) notAvailable(metric, RuntimeState.UNAVAILABLE, source,
                notes = "getSystemService returned null")
            else observed(metric, outcome, source)
        }
}

/** B4: process CPU time of this app (not a utilisation figure). */
class CpuTelemetryCollector {
    fun collect(): List<CapabilityResult> = listOf(
        guarded("app_cpu_time", "Process.getElapsedCpuTime()") {
            observed("app_cpu_time", Process.getElapsedCpuTime(), "Process.getElapsedCpuTime()", unit = "ms")
        }
    )
}

/** B5: GPU identity from an EGL/GLES2 context, and the Vulkan hardware feature. No utilisation is derived. */
class GpuCapabilityCollector(private val context: Context) {
    fun collect(): List<CapabilityResult> = listOf(renderer(), vulkan())

    private fun renderer(): CapabilityResult {
        val source = "EGL14 pbuffer context + GLES20.glGetString(GL_RENDERER, GL_VENDOR, GL_VERSION)"
        return guarded("gpu_renderer", source) {
            val display = EGL14.eglGetDisplay(EGL14.EGL_DEFAULT_DISPLAY)
            if (display == EGL14.EGL_NO_DISPLAY) {
                return@guarded notAvailable("gpu_renderer", RuntimeState.UNAVAILABLE, source, notes = "No EGL display")
            }
            val version = IntArray(2)
            if (!EGL14.eglInitialize(display, version, 0, version, 1)) {
                return@guarded notAvailable("gpu_renderer", RuntimeState.ERROR, source,
                    errorMessage = "eglInitialize failed: 0x${Integer.toHexString(EGL14.eglGetError())}")
            }
            try {
                val configs = arrayOfNulls<EGLConfig>(1)
                val num = IntArray(1)
                val attribs = intArrayOf(EGL14.EGL_RENDERABLE_TYPE, EGL14.EGL_OPENGL_ES2_BIT,
                    EGL14.EGL_SURFACE_TYPE, EGL14.EGL_PBUFFER_BIT, EGL14.EGL_NONE)
                if (!EGL14.eglChooseConfig(display, attribs, 0, configs, 0, 1, num, 0) || num[0] == 0) {
                    return@guarded notAvailable("gpu_renderer", RuntimeState.ERROR, source,
                        errorMessage = "eglChooseConfig found no GLES2 pbuffer config")
                }
                val ctx = EGL14.eglCreateContext(display, configs[0], EGL14.EGL_NO_CONTEXT,
                    intArrayOf(EGL14.EGL_CONTEXT_CLIENT_VERSION, 2, EGL14.EGL_NONE), 0)
                val surface = EGL14.eglCreatePbufferSurface(display, configs[0],
                    intArrayOf(EGL14.EGL_WIDTH, 1, EGL14.EGL_HEIGHT, 1, EGL14.EGL_NONE), 0)
                try {
                    if (!EGL14.eglMakeCurrent(display, surface, surface, ctx)) {
                        return@guarded notAvailable("gpu_renderer", RuntimeState.ERROR, source,
                            errorMessage = "eglMakeCurrent failed: 0x${Integer.toHexString(EGL14.eglGetError())}")
                    }
                    val renderer = GLES20.glGetString(GLES20.GL_RENDERER)
                    val vendor = GLES20.glGetString(GLES20.GL_VENDOR)
                    val glVersion = GLES20.glGetString(GLES20.GL_VERSION)
                    if (renderer.isNullOrEmpty()) {
                        notAvailable("gpu_renderer", RuntimeState.ERROR, source, errorMessage = "GL_RENDERER returned null")
                    } else {
                        observed("gpu_renderer", mapOf("renderer" to renderer, "vendor" to vendor, "version" to glVersion),
                            source, details = mapOf("egl_version" to "${version[0]}.${version[1]}"))
                    }
                } finally {
                    EGL14.eglMakeCurrent(display, EGL14.EGL_NO_SURFACE, EGL14.EGL_NO_SURFACE, EGL14.EGL_NO_CONTEXT)
                    EGL14.eglDestroySurface(display, surface)
                    EGL14.eglDestroyContext(display, ctx)
                }
            } finally {
                EGL14.eglTerminate(display)
            }
        }
    }

    private fun vulkan(): CapabilityResult {
        val source = "PackageManager system features FEATURE_VULKAN_HARDWARE_VERSION / LEVEL"
        return guarded("gpu_vulkan_support", source) {
            val features = context.packageManager.systemAvailableFeatures
            val version = features.firstOrNull { it.name == PackageManager.FEATURE_VULKAN_HARDWARE_VERSION }
            val level = features.firstOrNull { it.name == PackageManager.FEATURE_VULKAN_HARDWARE_LEVEL }
            if (version == null) {
                notAvailable("gpu_vulkan_support", RuntimeState.UNAVAILABLE, source,
                    notes = "No Vulkan hardware feature declared")
            } else {
                observed("gpu_vulkan_support", mapOf(
                    "vulkan_hardware_version_encoded" to version.version,
                    "vulkan_hardware_level" to level?.version), source)
            }
        }
    }
}

/**
 * B9/B10: clock sources and android.os.Trace. Clock characterization only (protocol P5): monotonicity, smallest
 * observed positive step and mean interval between consecutive calls over [CLOCK_SAMPLES] calls. Not a benchmark.
 */
class ProfilingCapabilityCollector {
    companion object {
        /** Consecutive clock reads per clock (app procedure constant, recorded in the output). */
        const val CLOCK_SAMPLES = 2000
        const val TRACE_SECTION = "PocketInspect.characterization.trace_probe"
    }

    fun collect(): List<CapabilityResult> = listOf(clocks(), trace())

    private fun clockStats(read: () -> Long): Map<String, Any?> {
        val values = LongArray(CLOCK_SAMPLES)
        for (i in 0 until CLOCK_SAMPLES) values[i] = read()
        var monotonic = true
        var minPositive = Long.MAX_VALUE
        for (i in 1 until CLOCK_SAMPLES) {
            val d = values[i] - values[i - 1]
            if (d < 0) monotonic = false
            if (d in 1 until minPositive) minPositive = d
        }
        return mapOf(
            "monotonic" to monotonic,
            "samples" to CLOCK_SAMPLES,
            "min_positive_step_ns" to (if (minPositive == Long.MAX_VALUE) null else minPositive),
            "mean_interval_between_calls_ns" to (values[CLOCK_SAMPLES - 1] - values[0]).toDouble() / (CLOCK_SAMPLES - 1)
        )
    }

    private fun clocks(): CapabilityResult {
        val source = "System.nanoTime() / SystemClock.elapsedRealtimeNanos()"
        return guarded("system_nano_time", source) {
            val nano = clockStats { System.nanoTime() }
            val elapsed = clockStats { SystemClock.elapsedRealtimeNanos() }
            observed("system_nano_time", mapOf("system_nano_time" to nano, "elapsed_realtime_nanos" to elapsed),
                source, unit = "ns", notes = "Clock characterization only; not a performance result.")
        }
    }

    private fun trace(): CapabilityResult {
        val source = "android.os.Trace.beginSection/endSection; Trace.isEnabled (API 29)"
        return guarded("android_trace_api", source) {
            Trace.beginSection(TRACE_SECTION)
            Trace.endSection()
            val enabled: Boolean? = if (Build.VERSION.SDK_INT >= 29) Trace.isEnabled() else null
            observed("android_trace_api", mapOf("section" to TRACE_SECTION, "is_enabled" to enabled), source,
                notes = "API calls succeeded; visibility of the section in a captured system trace is not verified.")
        }
    }
}
