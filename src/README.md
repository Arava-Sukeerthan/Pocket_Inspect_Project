# PocketInspect Core Source Package (`src/`)

This directory contains the primary modular Python library for PocketInspect.

## Modules Overview

- **`acquisition/`**: Camera frame capture abstractions, sensor metadata ingestion, and optical configuration.
- **`quality/`**: Pre-inference image quality assessment (blur detection, illumination checks, ROI alignment).
- **`inference/`**: Runtime-agnostic model execution wrappers (ONNX Runtime, TFLite, PyTorch mobile placeholders).
- **`adaptation/`**: Dynamic execution control engines driven by device resource feedback.
- **`inspection/`**: Visual defect classification, surface anomaly scoring, and 3D-print defect detection heads.
- **`uncertainty/`**: Prediction confidence calibration and out-of-distribution (OOD) uncertainty estimation.
- **`monitoring/`**: Hardware telemetry collectors (CPU/GPU utilization, thermals, battery, RAM).

## Design Rules
1. Every submodule must be decoupled and importable independently.
2. Configuration parameters must be injected via `configs/` objects.
3. No hardcoded file paths or model parameters inside source modules.
