package org.pocketinspect.characterization

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.ImageFormat
import android.hardware.camera2.CameraCaptureSession
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import android.hardware.camera2.CameraMetadata
import android.hardware.camera2.CaptureRequest
import android.hardware.camera2.TotalCaptureResult
import android.media.CamcorderProfile
import android.media.ImageReader
import android.os.Handler
import android.os.HandlerThread
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/**
 * B6-B8: camera characterization (protocol P3, §5.3).
 *
 * - Camera IDs are exactly CameraManager.getCameraIdList() (strings, never generated).
 * - Lens facing, hardware level and capabilities come from CameraCharacteristics of each ID; a key that returns
 *   null is UNAVAILABLE, never a default.
 * - Advertised vs honoured: for a camera advertising MANUAL_SENSOR, a capture session requests a locked exposure
 *   time and sensitivity (AE off) and reports the requested values and the CaptureResult values. The host decides
 *   "honoured" (configs/device_characterization.yaml camera_manual_control_check). Without the CAMERA runtime
 *   permission the check is PERMISSION_REQUIRED; grant it with
 *   `adb shell pm grant org.pocketinspect.characterization android.permission.CAMERA` before launching the app.
 */
class CameraTelemetryCollector(private val context: Context) {
    companion object {
        /** Requested exposure time: 1/60 s, clamped into the advertised range (app procedure constant). */
        const val TARGET_EXPOSURE_NS = 16_666_666L
        /** Frames captured with the locked request; the last CaptureResult is compared. */
        const val CAPTURE_FRAMES = 5
        const val CAPTURE_TIMEOUT_S = 8L
        private val FACING = mapOf(CameraMetadata.LENS_FACING_FRONT to "FRONT",
            CameraMetadata.LENS_FACING_BACK to "BACK", CameraMetadata.LENS_FACING_EXTERNAL to "EXTERNAL")
        private val CAPABILITY_NAMES = mapOf(
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_BACKWARD_COMPATIBLE to "BACKWARD_COMPATIBLE",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_SENSOR to "MANUAL_SENSOR",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_POST_PROCESSING to "MANUAL_POST_PROCESSING",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_RAW to "RAW",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_READ_SENSOR_SETTINGS to "READ_SENSOR_SETTINGS",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_BURST_CAPTURE to "BURST_CAPTURE",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_DEPTH_OUTPUT to "DEPTH_OUTPUT",
            CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_LOGICAL_MULTI_CAMERA to "LOGICAL_MULTI_CAMERA")
        private val VIDEO_QUALITIES = mapOf(
            "QUALITY_LOW" to CamcorderProfile.QUALITY_LOW, "QUALITY_HIGH" to CamcorderProfile.QUALITY_HIGH,
            "QUALITY_480P" to CamcorderProfile.QUALITY_480P, "QUALITY_720P" to CamcorderProfile.QUALITY_720P,
            "QUALITY_1080P" to CamcorderProfile.QUALITY_1080P, "QUALITY_2160P" to CamcorderProfile.QUALITY_2160P)
    }

    fun collect(): List<CapabilityResult> {
        val results = mutableListOf<CapabilityResult>()
        val cm = context.getSystemService(Context.CAMERA_SERVICE) as? CameraManager
        if (cm == null) {
            results.add(notAvailable("camera_probe", RuntimeState.UNAVAILABLE, "Context.CAMERA_SERVICE",
                notes = "CameraManager system service not available"))
            return results
        }
        val ids: Array<String> = try {
            cm.cameraIdList
        } catch (e: Exception) {
            results.add(failure("camera_probe", "CameraManager.getCameraIdList()", e))
            return results
        }
        results.add(observed("camera_id_list", ids.toList(), "CameraManager.getCameraIdList()"))
        results.add(observed("camera_count", ids.size, "CameraManager.getCameraIdList()"))

        val permitted = context.checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
        for (id in ids) {
            val chars = try {
                cm.getCameraCharacteristics(id)
            } catch (e: Exception) {
                results.add(failure("hardware_level", "CameraManager.getCameraCharacteristics($id)", e, id))
                continue
            }
            results.addAll(characteristics(id, chars))
            results.addAll(manualControlCheck(cm, id, chars, permitted))
        }
        return results
    }

    private fun <T> key(id: String, metric: String, source: String, value: T?, unit: String? = null,
                        transform: (T) -> Any = { it as Any }): CapabilityResult =
        guarded(metric, source, id) {
            if (value == null) notAvailable(metric, RuntimeState.UNAVAILABLE, source, cameraId = id,
                notes = "Characteristic key returned null")
            else observed(metric, transform(value), source, unit = unit, cameraId = id)
        }

    private fun characteristics(id: String, c: CameraCharacteristics): List<CapabilityResult> {
        val out = mutableListOf<CapabilityResult>()
        val facing = c.get(CameraCharacteristics.LENS_FACING)
        out.add(key(id, "lens_facing", "CameraCharacteristics.LENS_FACING", facing) { FACING[it] ?: "UNKNOWN_$it" })
        out.add(key(id, "hardware_level", "CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL",
            c.get(CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL)))
        val caps = c.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES)
        out.add(key(id, "available_capabilities", "CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES", caps) { arr ->
            arr.map { CAPABILITY_NAMES[it] ?: "CAPABILITY_$it" }
        })
        val manual = caps?.contains(CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_SENSOR)
        out.add(when (manual) {
            null -> notAvailable("manual_exposure_advertised", RuntimeState.UNAVAILABLE,
                "REQUEST_AVAILABLE_CAPABILITIES", cameraId = id, notes = "Capabilities key returned null")
            true -> observed("manual_exposure_advertised", true, "REQUEST_AVAILABLE_CAPABILITIES contains MANUAL_SENSOR",
                cameraId = id)
            false -> notAvailable("manual_exposure_advertised", RuntimeState.UNAVAILABLE,
                "REQUEST_AVAILABLE_CAPABILITIES contains MANUAL_SENSOR", cameraId = id,
                notes = "MANUAL_SENSOR is not advertised")
        })
        out.add(key(id, "stream_configurations", "CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP",
            c.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)) { map ->
            map.outputFormats.associate { fmt ->
                "format_$fmt" to (map.getOutputSizes(fmt)?.map { "${it.width}x${it.height}" } ?: emptyList())
            }
        })
        out.add(key(id, "ae_target_fps_ranges", "CameraCharacteristics.CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES",
            c.get(CameraCharacteristics.CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES), "fps") { arr ->
            arr.map { listOf(it.lower, it.upper) }
        })
        out.add(key(id, "af_available_modes", "CameraCharacteristics.CONTROL_AF_AVAILABLE_MODES",
            c.get(CameraCharacteristics.CONTROL_AF_AVAILABLE_MODES)) { it.toList() })
        out.add(key(id, "lens_min_focus_distance", "CameraCharacteristics.LENS_INFO_MINIMUM_FOCUS_DISTANCE",
            c.get(CameraCharacteristics.LENS_INFO_MINIMUM_FOCUS_DISTANCE), "diopters"))
        out.add(key(id, "exposure_time_range_ns", "CameraCharacteristics.SENSOR_INFO_EXPOSURE_TIME_RANGE",
            c.get(CameraCharacteristics.SENSOR_INFO_EXPOSURE_TIME_RANGE), "ns") { listOf(it.lower, it.upper) })
        out.add(key(id, "sensitivity_range", "CameraCharacteristics.SENSOR_INFO_SENSITIVITY_RANGE",
            c.get(CameraCharacteristics.SENSOR_INFO_SENSITIVITY_RANGE), "ISO") { listOf(it.lower, it.upper) })
        out.add(key(id, "awb_available_modes", "CameraCharacteristics.CONTROL_AWB_AVAILABLE_MODES",
            c.get(CameraCharacteristics.CONTROL_AWB_AVAILABLE_MODES)) { it.toList() })
        out.add(key(id, "ae_lock_available", "CameraCharacteristics.CONTROL_AE_LOCK_AVAILABLE",
            c.get(CameraCharacteristics.CONTROL_AE_LOCK_AVAILABLE)))
        out.add(key(id, "awb_lock_available", "CameraCharacteristics.CONTROL_AWB_LOCK_AVAILABLE",
            c.get(CameraCharacteristics.CONTROL_AWB_LOCK_AVAILABLE)))
        out.add(guarded("physical_camera_ids", "CameraCharacteristics.getPhysicalCameraIds()", id) {
            observed("physical_camera_ids", c.physicalCameraIds.toList(), "CameraCharacteristics.getPhysicalCameraIds()",
                minApi = 28, cameraId = id)
        })
        val numericId = id.toIntOrNull()
        out.add(if (numericId == null) notAvailable("video_profiles", RuntimeState.UNAVAILABLE,
            "CamcorderProfile.hasProfile(int, quality)", cameraId = id,
            notes = "CamcorderProfile takes an integer camera ID; this ID is not an integer")
        else guarded("video_profiles", "CamcorderProfile.hasProfile(cameraId, QUALITY_*)", id) {
            observed("video_profiles", VIDEO_QUALITIES.mapValues { CamcorderProfile.hasProfile(numericId, it.value) },
                "CamcorderProfile.hasProfile(cameraId, QUALITY_*)", cameraId = id)
        })
        return out
    }

    /**
     * Returns the manual_control_honoured and capture_sensor_timestamp records for one camera. The capture runs
     * for every camera when permitted (the timestamp is recorded in auto mode when manual control is not advertised).
     */
    private fun manualControlCheck(cm: CameraManager, id: String, c: CameraCharacteristics,
                                   permitted: Boolean): List<CapabilityResult> {
        val honouredSource = "CaptureRequest (AE off, SENSOR_EXPOSURE_TIME, SENSOR_SENSITIVITY) vs TotalCaptureResult"
        val tsSource = "CaptureResult.SENSOR_TIMESTAMP"
        val advertised = c.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES)
            ?.contains(CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_SENSOR) == true
        if (!permitted) {
            val note = "CAMERA runtime permission not granted; grant with " +
                "`adb shell pm grant org.pocketinspect.characterization android.permission.CAMERA`."
            return listOf(
                notAvailable("manual_control_honoured", RuntimeState.PERMISSION_REQUIRED, honouredSource, cameraId = id,
                    notes = note),
                notAvailable("capture_sensor_timestamp", RuntimeState.PERMISSION_REQUIRED, tsSource, cameraId = id,
                    notes = note))
        }
        val expRange = c.get(CameraCharacteristics.SENSOR_INFO_EXPOSURE_TIME_RANGE)
        val isoRange = c.get(CameraCharacteristics.SENSOR_INFO_SENSITIVITY_RANGE)
        val manual = advertised && expRange != null && isoRange != null
        val reqExposure = expRange?.let { TARGET_EXPOSURE_NS.coerceIn(it.lower, it.upper) }
        val reqIso = isoRange?.let { (it.lower + it.upper) / 2 }

        val thread = HandlerThread("pi-camera-$id").apply { start() }
        val handler = Handler(thread.looper)
        var device: CameraDevice? = null
        var session: CameraCaptureSession? = null
        var reader: ImageReader? = null
        return try {
            val opened = CountDownLatch(1)
            var openError: String? = null
            cm.openCamera(id, object : CameraDevice.StateCallback() {
                override fun onOpened(camera: CameraDevice) { device = camera; opened.countDown() }
                override fun onDisconnected(camera: CameraDevice) { openError = "disconnected"; camera.close(); opened.countDown() }
                override fun onError(camera: CameraDevice, error: Int) { openError = "onError $error"; camera.close(); opened.countDown() }
            }, handler)
            if (!opened.await(CAPTURE_TIMEOUT_S, TimeUnit.SECONDS) || device == null) {
                throw IllegalStateException("openCamera failed: ${openError ?: "timeout"}")
            }
            val sizes = c.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)?.getOutputSizes(ImageFormat.YUV_420_888)
            val size = sizes?.minByOrNull { it.width * it.height }
                ?: throw IllegalStateException("No YUV_420_888 output size")
            reader = ImageReader.newInstance(size.width, size.height, ImageFormat.YUV_420_888, 4).apply {
                setOnImageAvailableListener({ r -> r.acquireLatestImage()?.close() }, handler)
            }
            val configured = CountDownLatch(1)
            @Suppress("DEPRECATION")
            device!!.createCaptureSession(listOf(reader!!.surface), object : CameraCaptureSession.StateCallback() {
                override fun onConfigured(s: CameraCaptureSession) { session = s; configured.countDown() }
                override fun onConfigureFailed(s: CameraCaptureSession) { configured.countDown() }
            }, handler)
            if (!configured.await(CAPTURE_TIMEOUT_S, TimeUnit.SECONDS) || session == null) {
                throw IllegalStateException("createCaptureSession failed")
            }
            val request = device!!.createCaptureRequest(
                if (manual) CameraDevice.TEMPLATE_MANUAL else CameraDevice.TEMPLATE_PREVIEW).apply {
                addTarget(reader.surface)
                if (manual) {
                    set(CaptureRequest.CONTROL_AE_MODE, CameraMetadata.CONTROL_AE_MODE_OFF)
                    set(CaptureRequest.SENSOR_EXPOSURE_TIME, reqExposure)
                    set(CaptureRequest.SENSOR_SENSITIVITY, reqIso)
                }
            }.build()
            val frames = CountDownLatch(CAPTURE_FRAMES)
            var last: TotalCaptureResult? = null
            var count = 0
            session!!.setRepeatingRequest(request, object : CameraCaptureSession.CaptureCallback() {
                override fun onCaptureCompleted(s: CameraCaptureSession, r: CaptureRequest, result: TotalCaptureResult) {
                    last = result; count += 1; frames.countDown()
                }
            }, handler)
            val completed = frames.await(CAPTURE_TIMEOUT_S, TimeUnit.SECONDS)
            session!!.stopRepeating()
            val result = last ?: throw IllegalStateException("No CaptureResult within ${CAPTURE_TIMEOUT_S}s")
            val ts = result.get(android.hardware.camera2.CaptureResult.SENSOR_TIMESTAMP)
            val tsSourceKey = c.get(CameraCharacteristics.SENSOR_INFO_TIMESTAMP_SOURCE)
            val timestampRecord = if (ts == null) notAvailable("capture_sensor_timestamp", RuntimeState.UNAVAILABLE,
                tsSource, cameraId = id, notes = "SENSOR_TIMESTAMP absent from CaptureResult")
            else observed("capture_sensor_timestamp", ts, tsSource, unit = "ns", cameraId = id,
                details = mapOf("frames" to count, "timestamp_source" to tsSourceKey))

            val honoured = if (!advertised) {
                notAvailable("manual_control_honoured", RuntimeState.UNAVAILABLE, honouredSource, cameraId = id,
                    notes = "MANUAL_SENSOR is not advertised; manual control is not requested or claimed")
            } else if (!manual) {
                notAvailable("manual_control_honoured", RuntimeState.ERROR, honouredSource, cameraId = id,
                    errorMessage = "MANUAL_SENSOR advertised but exposure/sensitivity ranges are missing")
            } else {
                val repExposure = result.get(android.hardware.camera2.CaptureResult.SENSOR_EXPOSURE_TIME)
                val repIso = result.get(android.hardware.camera2.CaptureResult.SENSOR_SENSITIVITY)
                if (repExposure == null || repIso == null) {
                    notAvailable("manual_control_honoured", RuntimeState.ERROR, honouredSource, cameraId = id,
                        errorMessage = "CaptureResult lacks SENSOR_EXPOSURE_TIME or SENSOR_SENSITIVITY")
                } else {
                    observed("manual_control_honoured", mapOf(
                        "requested_exposure_time_ns" to reqExposure,
                        "reported_exposure_time_ns" to repExposure,
                        "requested_sensitivity" to reqIso,
                        "reported_sensitivity" to repIso,
                        "frames_compared" to count,
                        "all_frames_received" to completed), honouredSource, cameraId = id,
                        notes = "Raw requested and reported values; the host decides whether they were honoured.")
                }
            }
            listOf(honoured, timestampRecord)
        } catch (e: Exception) {
            listOf(failure("manual_control_honoured", honouredSource, e, id),
                failure("capture_sensor_timestamp", tsSource, e, id))
        } finally {
            try { session?.close() } catch (_: Exception) {}
            try { device?.close() } catch (_: Exception) {}
            try { reader?.close() } catch (_: Exception) {}
            thread.quitSafely()
        }
    }
}
