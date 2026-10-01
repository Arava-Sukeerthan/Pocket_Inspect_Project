# System & Experiment Configuration (`configs/`)

Houses declarative YAML/JSON configuration files for system defaults, adaptation policies, runtime engine parameters, and evaluation benchmarks.

## Rules
- All experiment parameters must originate from configurations stored in this directory.
- No hardcoded paths, hyper-parameters, thresholds, or device execution flags in Python code under `src/` or `experiments/`.
