# Experiments Execution Harness (`experiments/`)

Contains declarative experiment scripts used to evaluate PocketInspect subsystems under controlled benchmark conditions.

## Execution Principles
1. Experiments must load parameters exclusively from `configs/`.
2. Execution scripts must log system environment, git commit hash, and random seed.
3. Metric logs must be exported directly to `research/results/`.
