package org.pocketinspect.characterization

import android.app.Activity
import android.os.Bundle
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

        val outFile = File(filesDir, "characterization_output.json")
        outFile.writeText(jsonOutput)
    }
}
