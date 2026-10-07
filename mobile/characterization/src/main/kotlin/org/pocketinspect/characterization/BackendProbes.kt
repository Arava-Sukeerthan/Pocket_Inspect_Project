package org.pocketinspect.characterization

import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import ai.onnxruntime.providers.NNAPIFlags
import android.content.Context
import android.os.Build
import android.os.Process
import android.util.Log
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import org.tensorflow.lite.DataType
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.TensorFlowLite
import org.tensorflow.lite.gpu.CompatibilityList
import org.tensorflow.lite.gpu.GpuDelegate
import org.tensorflow.lite.nnapi.NnApiDelegate
import java.io.File
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.FloatBuffer
import java.util.EnumSet

/**
 * Backend capability probes (protocol §4 P4, §5.4, §5.5). Capability only: no latency, throughput or accuracy is
 * measured or reported.
 *
 * For each backend (LiteRT/TFLite CPU-XNNPACK, GPU delegate, NNAPI delegate; ONNX Runtime CPU, NNAPI EP) the app
 * reports raw observations only; the host decides every status (scripts/device_characterization/adb_collector.py,
 * InferenceBackendCapabilityCollector, configs/device_characterization.yaml `inference_backend_check`):
 * - `backend_runtime`: the runtime library initialised, its runtime-reported version, and whether the requested
 *   delegate / execution provider could be constructed or is listed by the runtime.
 * - `reference_graph_check` (one per graph variant fp32 / fp16 / int8): the SHA-256 of the artifact bytes loaded,
 *   graph load, one inference on the deterministic manifest input, the raw output, and delegation evidence.
 *   AVAILABLE here means "the check executed and its observations are in `value`", never "the backend works".
 *
 * Delegation evidence:
 * - TFLite: the interpreter's execution-plan length (InterpreterImpl.getExecutionPlanLength(), package-private, read
 *   by reflection) next to the graph's node count. Delegated nodes are replaced by delegate kernels, so a shorter
 *   plan shows that the requested delegate took nodes. XNNPACK is disabled for the GPU and NNAPI backends, so a
 *   reduction there can only come from the requested delegate. Delegate log lines (tag "tflite") of this process are
 *   attached as supplementary evidence.
 * - ONNX Runtime: the session profile, reduced to (node, operator, execution provider) per executed kernel; timing
 *   fields are discarded.
 * The NNAPI accelerator identity is not observable through these Java APIs (device enumeration needs the NDK).
 */
class BackendCapabilityCollector(private val context: Context) {
    companion object {
        const val SECTION = "backend_capability"
        const val ASSET_DIR = "reference_graph"
        const val MANIFEST = "reference_graph_manifest.json"
        const val LOG_TAG = "POCKETINSPECT_BACKEND"
        const val NUM_THREADS = 1
        const val MAX_LOG_LINES = 40
        val VARIANTS = listOf("fp32", "fp16", "int8")
        val BACKENDS = listOf(
            Spec("TFLite_CPU", "LiteRT / TensorFlow Lite", "tflite", "XNNPACK"),
            Spec("TFLite_GPU", "LiteRT / TensorFlow Lite", "tflite", "GPU"),
            Spec("TFLite_NNAPI", "LiteRT / TensorFlow Lite", "tflite", "NNAPI"),
            Spec("ONNXRuntime_CPU", "ONNX Runtime Mobile", "onnx", "CPUExecutionProvider"),
            Spec("ONNXRuntime_NNAPI", "ONNX Runtime Mobile", "onnx", "NnapiExecutionProvider"),
        )
        /** NNAPI is available from API 27. */
        const val NNAPI_MIN_API = 27
    }

    data class Spec(val backend: String, val family: String, val format: String, val requestedDelegate: String)

    private data class Manifest(val json: JsonObject, val sha256: String)

    fun collect(): List<CapabilityResult> {
        val out = mutableListOf<CapabilityResult>()
        var manifestError: String? = null
        val manifest = try {
            val bytes = readAsset(MANIFEST)
            Manifest(JsonParser.parseString(String(bytes, Charsets.UTF_8)).asJsonObject, AppJsonLogFormatter.sha256Hex(bytes))
        } catch (e: Exception) {
            manifestError = "${e.javaClass.simpleName}: ${e.message}"
            null
        }
        for (spec in BACKENDS) {
            val runtimeSource = "Runtime initialisation (${spec.backend})"
            val runtime = tag(probe("backend_runtime", runtimeSource) { runtime(spec) }, spec, null)
            out.add(runtime)
            for (variant in VARIANTS) {
                val source = "Reference graph check (${spec.backend}, $variant)"
                val rec = when {
                    runtime.state != RuntimeState.AVAILABLE.name ->
                        notAvailable("reference_graph_check", RuntimeState.NOT_TESTED, source,
                            notes = "Not run: backend_runtime is ${runtime.state}.")
                    manifest == null ->
                        notAvailable("reference_graph_check", RuntimeState.ERROR, source,
                            errorMessage = "Reference graph manifest assets/$ASSET_DIR/$MANIFEST unreadable: $manifestError")
                    else -> probe("reference_graph_check", source) { check(spec, variant, manifest) }
                }
                out.add(tag(rec, spec, variant))
            }
        }
        return out
    }

    /** Like [guarded], but a native-library LinkageError is also recorded (ERROR) instead of ending the app. */
    private inline fun probe(metric: String, source: String, block: () -> CapabilityResult): CapabilityResult =
        try {
            guarded(metric, source) { block() }
        } catch (e: LinkageError) {
            notAvailable(metric, RuntimeState.ERROR, source, errorMessage = "${e.javaClass.simpleName}: ${e.message}")
        }

    private fun tag(r: CapabilityResult, spec: Spec, variant: String?) = r.copy(
        backend = spec.backend, graph_variant = variant,
        evidence_ref = "evidence/android_app_evidence.json#$SECTION/${spec.backend}/${r.metric}" +
            (variant?.let { "/$it" } ?: ""))

    // -----------------------------------------------------------------------------------------------------------
    // Runtime availability
    // -----------------------------------------------------------------------------------------------------------

    private fun runtime(spec: Spec): CapabilityResult {
        val source = "Runtime initialisation (${spec.backend})"
        val info = linkedMapOf<String, Any?>(
            "runtime_family" to spec.family,
            "requested_delegate" to spec.requestedDelegate,
            "sdk_int" to Build.VERSION.SDK_INT,
        )
        if (spec.requestedDelegate in setOf("NNAPI", "NnapiExecutionProvider") && Build.VERSION.SDK_INT < NNAPI_MIN_API) {
            return notAvailable("backend_runtime", RuntimeState.API_UNSUPPORTED, source, minApi = NNAPI_MIN_API,
                notes = "NNAPI requires API >= $NNAPI_MIN_API", details = info)
        }
        try {
            if (spec.format == "tflite") {
                info["declared_dependency"] = BuildConfig.TFLITE_ARTIFACT
                TensorFlowLite.init()
                info["runtime_version"] = TensorFlowLite.runtimeVersion()
                info["runtime_version_source"] = "TensorFlowLite.runtimeVersion()"
                info["schema_version"] = TensorFlowLite.schemaVersion()
                when (spec.requestedDelegate) {
                    "GPU" -> {
                        info["declared_delegate_dependency"] = BuildConfig.TFLITE_GPU_ARTIFACT
                        info["gpu_compatibility_list_supported"] =
                            CompatibilityList().use { it.isDelegateSupportedOnThisDevice }
                        GpuDelegate().close()
                        info["delegate_constructed"] = true
                    }
                    "NNAPI" -> {
                        NnApiDelegate(NnApiDelegate.Options().setUseNnapiCpu(false)).close()
                        info["delegate_constructed"] = true
                    }
                }
            } else {
                info["declared_dependency"] = BuildConfig.ONNXRUNTIME_ARTIFACT
                val env = OrtEnvironment.getEnvironment()
                info["runtime_version"] = env.version
                info["runtime_version_source"] = "OrtEnvironment.getVersion()"
                val providers = OrtEnvironment.getAvailableProviders().map { it.name }
                info["available_providers"] = providers
                if (spec.requestedDelegate == "NnapiExecutionProvider" && "NNAPI" !in providers) {
                    return notAvailable("backend_runtime", RuntimeState.UNAVAILABLE, source, details = info,
                        notes = "NNAPI is not listed by OrtEnvironment.getAvailableProviders()")
                }
            }
        } catch (e: UnsatisfiedLinkError) {
            return notAvailable("backend_runtime", RuntimeState.UNAVAILABLE, source, details = info,
                errorMessage = "${e.javaClass.simpleName}: ${e.message}",
                notes = "Native runtime library could not be loaded on this device")
        }
        return observed("backend_runtime", info, source, details = info)
    }

    // -----------------------------------------------------------------------------------------------------------
    // Reference graph check
    // -----------------------------------------------------------------------------------------------------------

    private fun check(spec: Spec, variant: String, manifest: Manifest): CapabilityResult {
        val name = "reference_graph_$variant.${spec.format}"
        val bytes = readAsset(name)
        val nodes = manifest.json.getAsJsonObject("graph_node_count").getAsJsonObject(spec.format).get(variant).asInt
        val input = manifest.json.getAsJsonObject("input").getAsJsonArray(spec.format).map { it.asFloat }.toFloatArray()
        val inputShape = manifest.json.getAsJsonObject("input_shape").getAsJsonArray(spec.format).map { it.asLong }.toLongArray()
        val value = linkedMapOf<String, Any?>(
            "graph_id" to manifest.json.get("graph_id").asString,
            "graph_variant" to variant,
            "artifact" to name,
            "artifact_sha256" to AppJsonLogFormatter.sha256Hex(bytes),
            "artifact_bytes" to bytes.size,
            "manifest_sha256" to manifest.sha256,
            "requested_backend" to spec.backend,
            "requested_delegate" to spec.requestedDelegate,
            "graph_node_count" to nodes,
        )
        if (spec.format == "tflite") runTflite(spec, bytes, input, nodes, value) else runOrt(spec, variant, bytes, input, inputShape, value)
        return observed("reference_graph_check", value, "Reference graph check (${spec.backend}, $variant)",
            notes = "Raw observations; the host decides load / inference / output validity / delegation.")
    }

    private fun stage(ok: Boolean, error: Throwable? = null) =
        linkedMapOf<String, Any?>("ok" to ok, "error" to error?.let { "${it.javaClass.simpleName}: ${it.message}" })

    private fun runTflite(spec: Spec, bytes: ByteArray, input: FloatArray, nodes: Int, value: MutableMap<String, Any?>) {
        val options = Interpreter.Options().setNumThreads(NUM_THREADS)
        var gpu: GpuDelegate? = null
        var nnapi: NnApiDelegate? = null
        when (spec.requestedDelegate) {
            "XNNPACK" -> options.setUseXNNPACK(true)
            "GPU" -> { options.setUseXNNPACK(false); gpu = GpuDelegate(); options.addDelegate(gpu) }
            "NNAPI" -> {
                options.setUseXNNPACK(false)
                nnapi = NnApiDelegate(NnApiDelegate.Options().setUseNnapiCpu(false)); options.addDelegate(nnapi)
            }
        }
        value["options"] = linkedMapOf("num_threads" to NUM_THREADS, "use_xnnpack" to (spec.requestedDelegate == "XNNPACK"),
            "gpu_delegate_options" to (if (gpu != null) "default GpuDelegate()" else null),
            "nnapi_use_nnapi_cpu" to (if (nnapi != null) false else null))
        val marker = "${spec.backend}/${value["graph_variant"]}/${System.nanoTime()}"
        Log.i(LOG_TAG, "BEGIN $marker")
        var interpreter: Interpreter? = null
        val delegation = linkedMapOf<String, Any?>("mechanism" to "tflite_execution_plan_length", "graph_node_count" to nodes)
        try {
            val model = ByteBuffer.allocateDirect(bytes.size).order(ByteOrder.nativeOrder())
            model.put(bytes).rewind()
            interpreter = try {
                Interpreter(model, options).also { value["load"] = stage(true) }
            } catch (e: Exception) {
                value["load"] = stage(false, e); null
            }
            if (interpreter != null) {
                executionPlanLength(interpreter, delegation)
                val inBuf = ByteBuffer.allocateDirect(4 * input.size).order(ByteOrder.nativeOrder())
                input.forEach { inBuf.putFloat(it) }
                inBuf.rewind()
                val outTensor = interpreter.getOutputTensor(0)
                val outBuf = ByteBuffer.allocateDirect(outTensor.numBytes()).order(ByteOrder.nativeOrder())
                try {
                    interpreter.run(inBuf, outBuf)
                    value["inference"] = stage(true)
                    outBuf.rewind()
                    val values = if (outTensor.dataType() == DataType.FLOAT32)
                        List(outTensor.numBytes() / 4) { outBuf.getFloat().toDouble() } else null
                    value["output"] = linkedMapOf("shape" to outTensor.shape().toList(),
                        "dtype" to outTensor.dataType().toString(), "values" to values)
                } catch (e: Exception) {
                    value["inference"] = stage(false, e)
                }
            }
            nnapi?.let { delegation["nnapi_errno"] = it.nnapiErrno; delegation["nnapi_has_errors"] = it.hasErrors() }
        } finally {
            try { interpreter?.close() } catch (_: Exception) {}
            try { gpu?.close() } catch (_: Exception) {}
            try { nnapi?.close() } catch (_: Exception) {}
            Log.i(LOG_TAG, "END $marker")
            delegation["log_lines"] = ownLogLines(marker)
            value["delegation"] = delegation
        }
    }

    /** InterpreterImpl.getExecutionPlanLength() is package-private; reflection failure is recorded, never guessed. */
    private fun executionPlanLength(interpreter: Interpreter, out: MutableMap<String, Any?>) {
        var c: Class<*>? = interpreter.javaClass
        while (c != null) {
            try {
                val m = c.getDeclaredMethod("getExecutionPlanLength")
                m.isAccessible = true
                out["execution_plan_length"] = m.invoke(interpreter) as Int
                return
            } catch (e: NoSuchMethodException) {
                c = c.superclass
            } catch (e: Exception) {
                out["execution_plan_error"] = "${e.javaClass.simpleName}: ${e.message}"
                return
            }
        }
        out["execution_plan_error"] = "getExecutionPlanLength() not found on ${interpreter.javaClass.name}"
    }

    private fun runOrt(spec: Spec, variant: String, bytes: ByteArray, input: FloatArray, shape: LongArray,
                       value: MutableMap<String, Any?>) {
        val env = OrtEnvironment.getEnvironment()
        val options = OrtSession.SessionOptions()
        val delegation = linkedMapOf<String, Any?>("mechanism" to "ort_profile_node_provider",
            "graph_node_count" to value["graph_node_count"])
        var session: OrtSession? = null
        try {
            options.setIntraOpNumThreads(NUM_THREADS)
            options.enableProfiling(File(context.cacheDir, "ort_profile_${spec.backend}_$variant").absolutePath)
            if (spec.requestedDelegate == "NnapiExecutionProvider") options.addNnapi(EnumSet.of(NNAPIFlags.CPU_DISABLED))
            value["options"] = linkedMapOf("intra_op_num_threads" to NUM_THREADS,
                "nnapi_flags" to (if (spec.requestedDelegate == "NnapiExecutionProvider") listOf("CPU_DISABLED") else null))
            session = try {
                env.createSession(bytes, options).also { value["load"] = stage(true) }
            } catch (e: Exception) {
                value["load"] = stage(false, e); null
            }
            if (session != null) {
                try {
                    OnnxTensor.createTensor(env, FloatBuffer.wrap(input), shape).use { tensor ->
                        session.run(mapOf("input" to tensor)).use { result ->
                            val out = result.get(0) as OnnxTensor
                            val fb = out.floatBuffer
                            value["inference"] = stage(true)
                            value["output"] = linkedMapOf("shape" to out.info.shape.toList(), "dtype" to out.info.type.toString(),
                                "values" to List(fb.remaining()) { fb.get().toDouble() })
                        }
                    }
                } catch (e: Exception) {
                    value["inference"] = stage(false, e)
                }
                try {
                    val path = session.endProfiling()
                    delegation["kernels"] = profileKernels(File(path))
                } catch (e: Exception) {
                    delegation["profile_error"] = "${e.javaClass.simpleName}: ${e.message}"
                }
            }
        } finally {
            try { session?.close() } catch (_: Exception) {}
            try { options.close() } catch (_: Exception) {}
            value["delegation"] = delegation
        }
    }

    /** Keeps only (node, operator, provider) of each executed kernel; durations are not recorded. */
    private fun profileKernels(file: File): List<Map<String, String?>> {
        try {
            val events = JsonParser.parseString(file.readText()).asJsonArray
            return events.mapNotNull { e ->
                val o = e.asJsonObject
                val name = o.get("name")?.asString ?: return@mapNotNull null
                val args = o.getAsJsonObject("args") ?: return@mapNotNull null
                if (o.get("cat")?.asString != "Node" || !name.endsWith("_kernel_time") || !args.has("provider")) null
                else linkedMapOf("node" to name.removeSuffix("_kernel_time"), "op" to args.get("op_name")?.asString,
                    "provider" to args.get("provider").asString)
            }
        } finally {
            file.delete()
        }
    }

    /** This process's log lines (tags tflite / onnxruntime) between the BEGIN and END markers; supplementary. */
    private fun ownLogLines(marker: String): List<String> = try {
        val proc = ProcessBuilder("logcat", "-d", "-v", "tag", "--pid=${Process.myPid()}").redirectErrorStream(true).start()
        val lines = proc.inputStream.bufferedReader().readLines()
        proc.waitFor()
        val start = lines.indexOfLast { it.contains("BEGIN $marker") }
        val end = lines.indexOfLast { it.contains("END $marker") }
        if (start < 0 || end < start) listOf("log markers not found")
        else lines.subList(start + 1, end).filter { it.contains("tflite") || it.contains("onnxruntime") }
            .take(MAX_LOG_LINES).map { it.take(300) }
    } catch (e: Exception) {
        listOf("logcat not readable: ${e.javaClass.simpleName}: ${e.message}")
    }

    private fun readAsset(name: String): ByteArray = context.assets.open("$ASSET_DIR/$name").use { it.readBytes() }
}
