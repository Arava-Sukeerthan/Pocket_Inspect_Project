# AGENTS.md - AI Agent Operating Guidelines

Welcome to **PocketInspect**. This document specifies operational directives, architectural guidelines, and behavioral boundaries for AI coding assistants working in this repository.

---

## 1. Primary Operating Directives

1. **Strict Compliance with `RESEARCH_RULES.md`**:
   - Always read and abide by `RESEARCH_RULES.md`.
   - Never generate fake metrics, fake literature, or unsubstantiated novelty claims.
   - Always distinguish Facts, Assumptions, Hypotheses, and Proposed Ideas.

2. **No Premature Model Training or Heavy Dependency Installation**:
   - Do not install heavy deep learning packages (`torch`, `tensorflow`, `torchvision`) unless explicitly instructed by the user.
   - Do not write scripts that attempt to train models or download heavy pre-trained weights without explicit user request.

3. **Modular Code Architecture**:
   - Place reusable python modules under `src/<submodule>/`.
   - Ensure every module under `src/` contains an `__init__.py` and clear docstrings.
   - Avoid creating standalone monolithic scripts in the root directory.

4. **Configuration-First Design**:
   - All experiment parameters, device thresholds, model paths, and pipeline options MUST be stored in `configs/`.
   - Use standard formats (YAML/JSON/TOML) for configuration files.

5. **Edge & Mobile Compatibility**:
   - Keep Android on-device execution (Camera2 API, TFLite/ONNX Runtime, NNAPI/Vulkan backend, battery & thermal throttling constraints) in mind when designing interfaces in `src/` and `mobile/`.

---

## 2. Directory Layout & Allocation Rules

| Directory Path | Intended Usage | Rule |
| :--- | :--- | :--- |
| `src/` | Core Python package source code | Highly modular, covered by unit tests in `tests/` |
| `configs/` | Experiment & system configuration files | Declarative parameters only; no hardcoded parameters in `src/` |
| `research/` | Literature notes, gap analyses, experiment logs, tables, figures | Markdown reports and raw result logs; no executable code |
| `docs/` | Architecture specs, decision logs (ADRs), research questions | Design documentation and research hypotheses |
| `models/` | Model definition schemas, exported ONNX/TFLite model files | No binary files committed to git without explicit instruction |
| `experiments/` | Experiment scripts & execution harnesses | Always load parameters from `configs/` |
| `mobile/` | Android / edge mobile application code | Native/Cross-platform mobile client source |
| `backend/` | Optional lightweight edge backend / synchronization server | Telemetry collection and coordination |
| `scripts/` | Utility scripts (e.g. data validation, export scripts) | Clean CLI utilities using `argparse` or `click` |
| `tests/` | Automated test suite | pytest-compatible tests for code in `src/` |

---

## 3. Communication & Documentation Protocol

- **Traceability**: When answering questions or proposing architecture changes, reference specific files using Markdown links (e.g., [`PROJECT_SPEC.md`](file:///e:/ML/projects/PocketInspect/PROJECT_SPEC.md)).
- **Assumptions**: Explicitly list all technical or operational assumptions when delivering output.
- **Verification**: Run standard sanity checks (e.g., `pytest`, syntax verification) whenever modifying code or configurations.
