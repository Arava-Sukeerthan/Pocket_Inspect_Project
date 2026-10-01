# PocketInspect 🔍📱

**Adaptive, Resource-Aware Edge AI Visual Inspection System for Repurposed Mobile Devices**

PocketInspect is an open research project exploring how legacy and low-cost smartphones can be transformed into autonomous, resource-aware Edge AI inspection nodes. The initial target application focuses on **visual inspection of 3D-printed parts and small manufactured components**.

---

## 🌟 Key Vision & Capabilities

PocketInspect enables a single repurposed mobile device to fulfill five core roles:
- 📷 **Optical Camera**: Capturing multi-angle macro imagery of target parts.
- ⚡ **Edge Computing Device**: Performing real-time image preprocessing and quality validation.
- 🧠 **AI Inference Platform**: Executing optimized lightweight computer vision models locally.
- 📊 **Inspection Interface**: Providing real-time visual feedback, anomaly heatmaps, and defect alerts.
- 🌡️ **Resource Monitoring Platform**: Tracking device thermals, battery health, and compute load to dynamically adapt inference workloads.

---

## 🔬 Research Scope & Dimensions

PocketInspect investigates key problems across Edge AI and industrial vision:
- **Mobile & Edge AI**: On-device neural model deployment under resource constraints.
- **Industrial Visual Inspection**: Defect identification in 3D-printed parts (layer shifts, stringing, surface voids).
- **Lightweight Deep Learning**: Quantization (INT8/FP16), model pruning, and architectural efficiency.
- **Adaptive & Thermal-Aware Inference**: Dynamic compute adaptation (resolution scaling, frame skipping, model routing) based on device thermals and battery levels.
- **Uncertainty & Anomaly Detection**: Out-of-distribution (OOD) defect detection and prediction confidence calibration.

---

## 📁 Repository Structure

```
PocketInspect/
├── README.md              # Project overview and entry point
├── AGENTS.md              # Operational instructions for AI assistants
├── PROJECT_SPEC.md        # Complete technical specification and architectural roadmap
├── RESEARCH_RULES.md      # Mandatory scientific methodology and experimental constraints
│
├── research/              # Literature reviews, gap analyses, experiment logs, tables & figures
│   ├── literature/        # Verified paper summaries and reference lists
│   ├── gap_analysis/      # Research gap mapping and novel hypothesis formulation
│   ├── datasets/          # Dataset metadata, schemas, and download instructions
│   ├── experiments/       # Formal experiment protocols and hypotheses
│   ├── results/           # Raw empirical benchmark logs (CSV/JSON)
│   ├── figures/           # Generated evaluation plots and figures
│   ├── tables/            # Formatted performance comparison tables
│   └── manuscript_data/   # Aggregated data for research publications
│
├── docs/                  # Architecture specs, decision records (ADRs), research questions
│   ├── architecture/      # Detailed subsystem architecture diagrams and specs
│   ├── decisions/         # Architectural Decision Records (ADRs)
│   └── research_questions/# Formulated testable research hypotheses
│
├── src/                   # Core modular Python library
│   ├── acquisition/       # Frame capture and camera parameter control
│   ├── quality/           # Image quality assessment (blur, illumination, alignment)
│   ├── inference/         # Hardware runtime wrappers (ONNX Runtime, TFLite)
│   ├── adaptation/        # Resource-aware dynamic execution and control policies
│   ├── inspection/        # Defect detection, classification, and anomaly scoring
│   ├── uncertainty/       # Model confidence calibration and OOD estimation
│   └── monitoring/        # System telemetry (CPU, GPU, thermal, battery, RAM)
│
├── models/                # Model architecture definitions and exported edge formats
├── experiments/           # Declarative experiment execution harnesses
├── mobile/                # Android / cross-platform edge application code
├── backend/               # Telemetry collection and coordination service
├── tests/                 # Unit and integration test suite
├── scripts/               # CLI utilities for data processing and export
└── configs/               # Declarative YAML/JSON configuration parameters
```

---

## 📑 Core Guidelines & Research Rules

All work in this repository is strictly bound by [`RESEARCH_RULES.md`](file:///e:/ML/projects/PocketInspect/RESEARCH_RULES.md):
1. **No unsubstantiated novelty claims** without baseline literature evidence.
2. **Zero invention** of papers, citations, datasets, or performance numbers.
3. **Explicit epistemic tagging**: Clearly separate Facts, Assumptions, Hypotheses, and Proposed Ideas.
4. **Configuration-driven**: All parameters reside in [`configs/`](file:///e:/ML/projects/PocketInspect/configs/).
5. **Edge compatibility**: Keep Android/ARM/NPU resource limits in mind at all times.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Git

### Setup Workspace
```bash
# Clone repository
git clone https://github.com/Arava-Sukeerthan/Pocket_Inspect_Project.git
cd Pocket_Inspect_Project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install editable package (development mode)
pip install -e .
```

---

## 📜 Documentation Links

- 📖 [Project Specification (`PROJECT_SPEC.md`)](file:///e:/ML/projects/PocketInspect/PROJECT_SPEC.md)
- 🔬 [Research Rules & Principles (`RESEARCH_RULES.md`)](file:///e:/ML/projects/PocketInspect/RESEARCH_RULES.md)
- 🤖 [AI Agent Guidelines (`AGENTS.md`)](file:///e:/ML/projects/PocketInspect/AGENTS.md)
