package org.pocketinspect.characterization

import com.google.gson.GsonBuilder
import com.google.gson.JsonArray
import com.google.gson.JsonParser
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * JVM unit tests for [AppJsonLogFormatter]. The fixture is synthetic: it has the shape and size of
 * the CharacterizationRunner report (Gson pretty printing, fields in alphabetical order as ART
 * returns them) and is not device evidence.
 */
class AppJsonLogFormatterTest {

    private val prettyGson = GsonBuilder().setPrettyPrinting().create()
    private val ts = "2026-10-05T17:02:21Z"

    private fun record(metric: String, value: Any?, unit: String? = null, source: String = "android_api",
                       state: String = "AVAILABLE", extra: Map<String, Any> = emptyMap()): Map<String, Any> {
        val m = sortedMapOf<String, Any>(
            "metric" to metric, "state" to state,
            "report_status" to if (state == "AVAILABLE") "VERIFIED" else "UNAVAILABLE",
            "source" to source, "verified" to (state == "AVAILABLE"), "verification_method" to "android_api",
        )
        if (state == "AVAILABLE") {
            m["observed_at"] = ts
            m["evidence_ref"] = "evidence/android_app_evidence.json#$metric"
        }
        if (value != null) m["value"] = value
        if (unit != null) m["unit"] = unit
        m.putAll(extra)
        return m
    }

    private fun report(camera: List<Map<String, Any>>?): String {
        val r = linkedMapOf<String, Any>(
            "run_id" to "android_run_test",
            "observed_at" to ts,
            "device_identity" to listOf(
                record("manufacturer", "OPPO", source = "Build.MANUFACTURER"),
                record("model", "CPH1931", source = "Build.MODEL"),
                record("soc_model", null, state = "API_UNSUPPORTED", extra = mapOf("min_api" to 31, "notes" to "Build.SOC_MODEL requires API >= 31")),
            ),
            "memory_telemetry" to listOf(
                record("total_ram_mb", 2642, "MB", "ActivityManager.MemoryInfo.totalMem"),
                record("available_memory_mb", 1074, "MB", "ActivityManager.MemoryInfo.availMem"),
            ),
            "thermal_capability" to record("thermal_status_api", 0, source = "PowerManager.getCurrentThermalStatus()", extra = mapOf("min_api" to 29)),
            "battery_telemetry" to listOf(
                record("battery_level_percent", 34, "percent", "BatteryManager.EXTRA_LEVEL"),
                record("battery_voltage", 3746, "mV", "BatteryManager.EXTRA_VOLTAGE"),
                record("battery_temperature", 37.0, "degC", "BatteryManager.EXTRA_TEMPERATURE"),
                record("is_charging", true, "boolean", "BatteryManager.EXTRA_STATUS"),
            ),
        )
        if (camera != null) r["camera_telemetry"] = camera
        return prettyGson.toJson(r)
    }

    private val camera = listOf(
        record("camera_count", 4, source = "CameraManager.getCameraIdList()"),
        record("camera_0_hardware_level", 1, source = "CameraCharacteristics.INFO_SUPPORTED_HARDWARE_LEVEL"),
    )

    private fun recordsOf(lines: List<String>, section: String): List<String> =
        lines.filter { it.startsWith("RECORD ") && it.contains(" section=$section ") }
            .map { it.substring(it.indexOf('{')) }

    @Test
    fun reportExceedsSingleLogcatEntryButEveryLineFits() {
        val json = report(camera)
        // A single entry holding the whole report would exceed the ~4 KB logcat payload limit.
        assertTrue(AppJsonLogFormatter.utf8Length(json) > 4068)
        val lines = AppJsonLogFormatter.formatLines(json, listOf("/data/user/0/x/files/characterization_output.json"))
        lines.forEach { assertTrue("line too long: ${it.length}", AppJsonLogFormatter.utf8Length(it) <= AppJsonLogFormatter.MAX_LINE_BYTES) }
    }

    @Test
    fun cameraRecordsAreLoggedCompletelyAndLosslessly() {
        val json = report(camera)
        val lines = AppJsonLogFormatter.formatLines(json, emptyList())
        val logged = recordsOf(lines, "camera_telemetry").map { JsonParser.parseString(it) }
        val original = JsonParser.parseString(json).asJsonObject.getAsJsonArray("camera_telemetry")
        assertEquals(original.toList(), logged)
        assertEquals(4, logged[0].asJsonObject.get("value").asInt)
        assertTrue(lines.contains("SECTION run_id=android_run_test section=camera_telemetry records=2"))
        // Every section is reconstructable from its RECORD lines.
        val root = JsonParser.parseString(json).asJsonObject
        for (section in AppJsonLogFormatter.SECTIONS) {
            val el = root.get(section) ?: continue  // sections absent from this fixture are logged as MISSING
            val expected = if (el.isJsonArray) el.asJsonArray.toList() else listOf(el)
            assertEquals(section, expected, recordsOf(lines, section).map { JsonParser.parseString(it) })
        }
    }

    @Test
    fun beginAndArtifactLinesCarryTheFileDigest() {
        val json = report(camera)
        val bytes = json.toByteArray(Charsets.UTF_8)
        val sha = AppJsonLogFormatter.sha256Hex(bytes)
        val paths = listOf("/data/user/0/org.pocketinspect.characterization/files/characterization_output.json",
                           "/storage/emulated/0/Android/data/org.pocketinspect.characterization/files/characterization_output.json")
        val lines = AppJsonLogFormatter.formatLines(json, paths)
        assertEquals("BEGIN run_id=android_run_test records=12 bytes=${bytes.size} sha256=$sha", lines.first())
        assertEquals("END run_id=android_run_test records=12", lines.last())
        val artifacts = lines.filter { it.startsWith("ARTIFACT ") }
        assertEquals(paths.map { "ARTIFACT run_id=android_run_test path=$it bytes=${bytes.size} sha256=$sha host_copy=evidence/android_app_evidence.json" }, artifacts)
        assertEquals(64, sha.length)
    }

    @Test
    fun emptyAndMissingCameraSectionsAreExplicit() {
        val empty = AppJsonLogFormatter.formatLines(report(emptyList()), emptyList())
        assertTrue(empty.contains("SECTION run_id=android_run_test section=camera_telemetry records=0"))
        assertTrue(recordsOf(empty, "camera_telemetry").isEmpty())
        val missing = AppJsonLogFormatter.formatLines(report(null), emptyList())
        assertTrue(missing.contains("SECTION run_id=android_run_test section=camera_telemetry status=MISSING"))
    }

    @Test
    fun overLongRecordIsSplitIntoNumberedPartsThatRejoin() {
        val longError = "CameraAccessException: " + "x".repeat(9000)
        val cam = listOf(record("camera_probe", null, state = "ERROR", extra = mapOf("error_message" to longError)))
        val json = report(cam)
        val lines = AppJsonLogFormatter.formatLines(json, emptyList())
        val parts = lines.filter { it.contains(" section=camera_telemetry part=") }
        assertTrue(parts.size >= 3)
        parts.forEach { assertTrue(AppJsonLogFormatter.utf8Length(it) <= AppJsonLogFormatter.MAX_LINE_BYTES) }
        val joined = parts.joinToString("") { it.substring(it.indexOf(" ", it.indexOf("part=")) + 1) }
        val original = JsonParser.parseString(json).asJsonObject.getAsJsonArray("camera_telemetry")
        assertEquals(original[0], JsonParser.parseString(joined))
    }

    @Test
    fun splitUtf8NeverBreaksACodePoint() {
        val s = "é漢😀".repeat(500)
        val parts = AppJsonLogFormatter.splitUtf8(s, 10)
        assertEquals(s, parts.joinToString(""))
        parts.forEach { assertTrue(AppJsonLogFormatter.utf8Length(it) <= 10) }
    }

    private fun JsonArray.toList() = (0 until size()).map { get(it) }
}
