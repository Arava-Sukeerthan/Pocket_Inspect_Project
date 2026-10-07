package org.pocketinspect.characterization

import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import java.security.MessageDigest

/**
 * Formats the characterization report for logcat without losing any record.
 *
 * A logcat entry is limited to about 4 KB (LOGGER_ENTRY_MAX_PAYLOAD = 4068 bytes, including the
 * tag), so logging the whole pretty-printed report as one entry truncates it. On an OPPO CPH1931
 * run the cut fell inside camera_telemetry. Instead, every record is logged as one compact JSON
 * line that is kept below [MAX_LINE_BYTES]; an over-long record is split into numbered parts.
 *
 * Logcat is only an observation aid. The evidence artifact is the report file the app writes
 * ([OUTPUT_FILE_NAME]); the host copies it into its run directory as [HOST_EVIDENCE_PATH], which
 * is the path every `evidence_ref` in the report refers to. The ARTIFACT lines give the device
 * path, byte count and SHA-256 of that file, so a retrieved copy can be checked against them.
 *
 * Pure JVM code (no Android API), so it is unit-tested off-device.
 */
object AppJsonLogFormatter {
    const val LOG_TAG = "POCKETINSPECT_APP_JSON"
    const val OUTPUT_FILE_NAME = "characterization_output.json"
    const val HOST_EVIDENCE_PATH = "evidence/android_app_evidence.json"

    /** Well below the ~4 KB logcat payload limit, leaving room for the tag and line prefix. */
    const val MAX_LINE_BYTES = 3000

    /** Report sections in the order CharacterizationRunner writes them. */
    val SECTIONS = listOf(
        "device_identity",
        "memory_telemetry",
        "thermal_capability",
        "battery_telemetry",
        "service_capability",
        "cpu_telemetry",
        "gpu_capability",
        "profiling_capability",
        "camera_telemetry",
        "backend_capability",
    )

    private val compactGson = GsonBuilder().disableHtmlEscaping().create()

    fun sha256Hex(bytes: ByteArray): String =
        MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }

    /**
     * Returns the logcat lines for [reportJson]. [artifactPaths] are the device paths the report
     * bytes were written to. Every returned line is at most [MAX_LINE_BYTES] bytes in UTF-8.
     */
    fun formatLines(reportJson: String, artifactPaths: List<String>): List<String> {
        val reportBytes = reportJson.toByteArray(Charsets.UTF_8)
        val sha256 = sha256Hex(reportBytes)
        val root = JsonParser.parseString(reportJson).asJsonObject
        val runId = root.get("run_id")?.takeIf { it.isJsonPrimitive }?.asString ?: "unknown"

        val records = mutableListOf<Pair<String, String>>()
        val sectionLines = mutableListOf<String>()
        for (section in SECTIONS) {
            val element = root.get(section)
            when {
                element == null || element.isJsonNull ->
                    sectionLines.add("SECTION run_id=$runId section=$section status=MISSING")
                element.isJsonArray -> {
                    val array = element.asJsonArray
                    sectionLines.add("SECTION run_id=$runId section=$section records=${array.size()}")
                    array.forEach { records.add(section to compactGson.toJson(it)) }
                }
                else -> {
                    sectionLines.add("SECTION run_id=$runId section=$section records=1")
                    records.add(section to compactGson.toJson(element))
                }
            }
        }

        val lines = mutableListOf<String>()
        lines.add("BEGIN run_id=$runId records=${records.size} bytes=${reportBytes.size} sha256=$sha256")
        lines.addAll(sectionLines)
        records.forEachIndexed { index, (section, json) ->
            val prefix = "RECORD run_id=$runId n=${index + 1}/${records.size} section=$section"
            val single = "$prefix $json"
            if (utf8Length(single) <= MAX_LINE_BYTES) {
                lines.add(single)
            } else {
                val parts = splitUtf8(json, MAX_LINE_BYTES - utf8Length(prefix) - 32)
                parts.forEachIndexed { p, part -> lines.add("$prefix part=${p + 1}/${parts.size} $part") }
            }
        }
        for (path in artifactPaths) {
            lines.add("ARTIFACT run_id=$runId path=$path bytes=${reportBytes.size} sha256=$sha256 host_copy=$HOST_EVIDENCE_PATH")
        }
        lines.add("END run_id=$runId records=${records.size}")
        return lines
    }

    fun utf8Length(s: String): Int = s.toByteArray(Charsets.UTF_8).size

    /** Splits [s] into pieces of at most [maxBytes] UTF-8 bytes without breaking a code point. */
    fun splitUtf8(s: String, maxBytes: Int): List<String> {
        require(maxBytes >= 4) { "maxBytes must allow at least one code point" }
        val parts = mutableListOf<String>()
        val current = StringBuilder()
        var currentBytes = 0
        var i = 0
        while (i < s.length) {
            val cp = s.codePointAt(i)
            val chars = Character.charCount(cp)
            val cpBytes = String(Character.toChars(cp)).toByteArray(Charsets.UTF_8).size
            if (currentBytes + cpBytes > maxBytes) {
                parts.add(current.toString())
                current.setLength(0)
                currentBytes = 0
            }
            current.appendCodePoint(cp)
            currentBytes += cpBytes
            i += chars
        }
        if (current.isNotEmpty() || parts.isEmpty()) parts.add(current.toString())
        return parts
    }
}
