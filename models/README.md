# Models Directory (`models/`)

Contains model definition schemas, configuration mappers, and exported edge runtime artifacts (e.g. ONNX, TFLite format specs).

## Rules
- Binary weights (.onnx, .tflite, .pt) must be kept out of git tracking or managed via LFS / external download scripts.
- Schema definitions and configuration metadata files reside here.
