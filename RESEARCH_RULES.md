# PocketInspect: Research Rules & Principles

This document establishes the mandatory scientific methodology, operational constraints, and experimental rules governing all research and development work in **PocketInspect**.

---

## Core Research Rules

### 1. No Unsubstantiated Novelty Claims
- Do not claim that any technique, architecture, or workflow is novel, first-of-its-kind, or state-of-the-art (SOTA) without rigorous, verifiable literature evidence and empirical comparison.
- Every claim of contribution must be cross-referenced against existing baseline literature in `research/literature/` and documented in `research/gap_analysis/`.

### 2. Zero Invention of Literature, Data, or Results
- Never hallucinate or invent academic papers, author lists, dataset specifications, citations, benchmarks, or baseline performance figures.
- Cite only verified, real publications (with valid DOIs or arXiv identifiers) and real, accessible datasets.

### 3. Clear Epistemic Taxonomy
Every technical statement, document entry, and inline comment must strictly distinguish between four categories:
- **Fact**: Empirical observation backed by logged data, verified measurement, or established scientific consensus.
- **Assumption**: Operational premise taken as given for a specific experimental setup (must be explicitly declared).
- **Hypothesis**: Testable proposition requiring empirical validation through controlled experiments.
- **Proposed Idea**: Architectural design or algorithm candidate under exploration prior to hypothesis formulation.

### 4. Zero Generation of Fake Experimental Results
- Never mock, invent, synthesize, or estimate fake benchmark numbers, accuracy metrics, inference latencies, or energy consumption figures.
- All benchmark tables, figures, and manuscript data must originate directly from executed, reproducible evaluation scripts and verified log files.

### 5. Modularity and Reproducibility
- All code must be organized into modular, well-tested Python packages inside `src/`.
- Every experiment must be fully reproducible from source code, configuration files, and random seeds.
- Code should avoid monolithic scripts and monolithic notebooks for core logic.

### 6. Strict Configuration-Driven Parameterization
- Never hardcode hyper-parameters, thresholds, input dimensions, paths, hardware flags, or model structures inside execution scripts.
- Use declarative YAML/JSON configuration files managed within `configs/`.

### 7. Comprehensive Experiment Tracking
- Every execution of an experiment must automatically log:
  - Exact configuration snapshot (YAML/JSON)
  - Git commit hash
  - Hardware/device metrics (device model, CPU/GPU state, thermal state, battery level where applicable)
  - System environment & dependency versions
  - Raw output metrics and logs stored under `experiments/` or `research/results/`.

### 8. Mobile & Edge Deployment Awareness
- All algorithmic designs, model selections, preprocessing steps, and inference pipelines must consider the constraints of mobile execution (Android/TFLite/ONNX Runtime/NPU/CPU execution, battery constraints, thermal throttling, memory footprint).
- Avoid operations or dependencies that cannot be exported to edge inference runtimes.

### 9. Deferred Final Inspection Model Implementation
- Do not jump into implementing or training a final, fixed inspection neural network architecture prematurely.
- Focus first on system infrastructure, acquisition quality assessment, adaptive compute abstractions, resource monitoring, and evaluation frameworks.

### 10. Avoid Premature Freezing of Research Contributions
- Keep research dimensions open to exploration (e.g., adaptive inference, thermal dynamics, multi-view fusion, uncertainty calibration, anomaly detection vs. supervised defect classification).
- Allow experimental data and empirical findings on physical edge hardware to guide the final research scope and manuscript contributions.

---

## Enforcement Checklist for Agents and Contributors

- [ ] Has every parameter in this experiment been defined in `configs/`?
- [ ] Are all metric values backed by generated log artifacts in `research/results/`?
- [ ] Is every paper cited verified against real literature sources?
- [ ] Is the code compatible with edge runtimes (e.g., ONNX / TFLite)?
- [ ] Have assumptions and hypotheses been explicitly documented in `docs/research_questions/`?
