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

        val runner = CharacterizationRunner(this)
        val jsonOutput = runner.runAll()

        // 1. Private storage
        val outFile = File(filesDir, "characterization_output.json")
        outFile.writeText(jsonOutput)

        // 2. External app storage (easily accessible via ADB pull without root/run-as)
        val extDir = getExternalFilesDir(null)
        if (extDir != null) {
            val extFile = File(extDir, "characterization_output.json")
            extFile.writeText(jsonOutput)
        }

        // 3. Logcat output for direct stream capture
        Log.i("POCKETINSPECT_APP_JSON", jsonOutput)
    }
}
