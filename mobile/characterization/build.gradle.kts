// Backend capability runtimes (researcher decision 2026-10-07; configs/device_characterization.yaml
// inference_backend_check). Single declaration of the artifact versions: the app reports them as "declared" and
// separately reports the runtime-reported version. All resolve from Maven Central. TFLite 2.16.1 is the last
// org.tensorflow:tensorflow-lite release; 2.17.0 relocates to com.google.ai.edge.litert:litert:1.0.1 (Google Maven).
val tfliteVersion = "2.16.1"
val onnxRuntimeVersion = "1.30.0"

// Step 10D backend reference graph: generated at build time by the repository's deterministic generator
// (scripts/device_characterization/generate_reference_graph.py, standard-library Python, no download) and packaged as
// APK assets under reference_graph/. Model binaries are not committed to git. The SHA-256 of each artifact is pinned
// in configs/device_characterization.yaml; the app reports the hash of the bytes it loads and the host compares them.
// Python interpreter: -Ppocketinspect.python=<exe> (default: "python" on Windows, "python3" elsewhere).
val repositoryRoot: File = rootDir.parentFile.parentFile
val referenceGraphAssets = layout.buildDirectory.dir("generated/referenceGraphAssets")
val pythonExecutable = (findProperty("pocketinspect.python") as String?)
    ?: if (System.getProperty("os.name").lowercase().contains("windows")) "python" else "python3"

plugins {
    id("com.android.application") version "8.2.2"
    id("org.jetbrains.kotlin.android") version "1.9.22"
}

android {
    namespace = "org.pocketinspect.characterization"
    compileSdk = 34

    defaultConfig {
        applicationId = "org.pocketinspect.characterization"
        minSdk = 28
        targetSdk = 28
        versionCode = 1
        versionName = "1.0.0-characterization"

        buildConfigField("String", "TFLITE_ARTIFACT", "\"org.tensorflow:tensorflow-lite:$tfliteVersion\"")
        buildConfigField("String", "TFLITE_GPU_ARTIFACT", "\"org.tensorflow:tensorflow-lite-gpu:$tfliteVersion\"")
        buildConfigField("String", "ONNXRUNTIME_ARTIFACT", "\"com.microsoft.onnxruntime:onnxruntime-android:$onnxRuntimeVersion\"")
    }

    buildFeatures {
        buildConfig = true
    }

    sourceSets {
        getByName("main") {
            assets.srcDir(referenceGraphAssets)
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("org.tensorflow:tensorflow-lite:$tfliteVersion")
    implementation("org.tensorflow:tensorflow-lite-gpu:$tfliteVersion")
    implementation("org.tensorflow:tensorflow-lite-gpu-api:$tfliteVersion")
    implementation("com.microsoft.onnxruntime:onnxruntime-android:$onnxRuntimeVersion")
    testImplementation("junit:junit:4.13.2")
}

val generateReferenceGraph by tasks.registering(Exec::class) {
    description = "Generates the Step 10D backend reference-graph assets (deterministic; SHA-256 pinned in configs)."
    val outDir = referenceGraphAssets.get().dir("reference_graph").asFile
    inputs.file(File(repositoryRoot, "src/monitoring/characterization/reference_graph.py"))
    inputs.file(File(repositoryRoot, "scripts/device_characterization/generate_reference_graph.py"))
    outputs.dir(outDir)
    workingDir = repositoryRoot
    commandLine(pythonExecutable, "scripts/device_characterization/generate_reference_graph.py", "--out", outDir.absolutePath)
}

tasks.named("preBuild") {
    dependsOn(generateReferenceGraph)
}
