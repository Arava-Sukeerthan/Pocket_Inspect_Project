# Experiment Protocols (`research/experiments/`)

Documents formal research experiment plans, evaluation hypotheses, metric definitions, and execution procedures.

## Protocol Template
- **Experiment ID**: EXP-XXX
- **Hypothesis**: Specific testable statement.
- **Independent Variables**: Compute backend, resolution, model variant, thermal state.
- **Dependent Variables**: Accuracy, mAP, FPS, latency, temperature (°C), power (mW).
- **Control Parameters**: Fixed lighting, fixed part geometry, fixed ambient temperature.

## Step 10C protocol (GC-03)
Protocol design only; no experiment has been run and no result exists.
- [`experimental_protocol.md`](experimental_protocol.md): master protocol (positioning, architecture, stages, baselines, recovery, repetition, statistics, falsification, gates, decisions)
- [`generalization_framework.md`](generalization_framework.md): methodology vs experimental platform; result classes
- [`resource_states.md`](resource_states.md): R0–R3 framework, pressure, runtime adaptation; OPPO A5 2020 instantiation
- [`model_selection_protocol.md`](model_selection_protocol.md): seven-step C1–C4 selection
- [`confidence_verification_protocol.md`](confidence_verification_protocol.md): splits, calibration, thresholds, A0–A4 policy
- [`measurement_protocol.md`](measurement_protocol.md): device characterisation (E0), outcomes, energy, thermal
- [`experimental_matrix.csv`](experimental_matrix.csv), [`log_schema.json`](log_schema.json)
