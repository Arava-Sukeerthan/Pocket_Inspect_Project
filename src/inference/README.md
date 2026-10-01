# Inference Module (`src/inference/`)

Defines unified execution abstractions for running machine learning models across heterogeneous edge runtimes.

## Responsibilities
- Runtime-agnostic inference engine interfaces (ONNX Runtime, TFLite wrappers).
- Input tensor preprocessing and layout formatting (NCHW / NHWC).
- Acceleration provider setup (CPU, GPU/OpenCL, NPU execution backends).
