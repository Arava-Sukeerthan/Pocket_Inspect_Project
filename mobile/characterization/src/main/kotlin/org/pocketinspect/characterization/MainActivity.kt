package org.pocketinspect.characterization

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import java.io.File

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val textView = TextView(this)
        textView.text = "PocketInspect Characterization System Running..."
        setContentView(textView)

        // The probes run off the main thread: the camera capture check blocks on camera callbacks.
        Thread {
            val jsonOutput = CharacterizationRunner(this).runAll()
            val outputBytes = jsonOutput.toByteArray(Charsets.UTF_8)
            val writtenPaths = mutableListOf<String>()

            // 1. Private storage: the evidence artifact the host retrieves with
            //    `adb shell run-as org.pocketinspect.characterization cat files/characterization_output.json`
            //    and stores in its run directory as evidence/android_app_evidence.json.
            val outFile = File(filesDir, AppJsonLogFormatter.OUTPUT_FILE_NAME)
            outFile.writeBytes(outputBytes)
            writtenPaths.add(outFile.absolutePath)

            // 2. External app storage: the same bytes, readable by adb without run-as
            //    (/sdcard/Android/data/org.pocketinspect.characterization/files/characterization_output.json).
            val extDir = getExternalFilesDir(null)
            if (extDir != null) {
                val extFile = File(extDir, AppJsonLogFormatter.OUTPUT_FILE_NAME)
                extFile.writeBytes(outputBytes)
                writtenPaths.add(extFile.absolutePath)
            }

            // 3. Logcat: one compact line per record, each below the logcat entry limit, plus the
            //    artifact paths and SHA-256. A single entry holding the whole report was truncated.
            for (line in AppJsonLogFormatter.formatLines(jsonOutput, writtenPaths)) {
                Log.i(AppJsonLogFormatter.LOG_TAG, line)
            }
            runOnUiThread { textView.text = "PocketInspect Characterization complete: ${outFile.absolutePath}" }
        }.start()
    }
}
