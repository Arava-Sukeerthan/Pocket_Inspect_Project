# Datasets Metadata (`research/datasets/`)

Contains dataset specifications, annotation schemas, download scripts, and train/val/test split manifests for 3D-printing and industrial inspection datasets.

## Guidelines
1. Do not store binary dataset images directly in git.
2. Record dataset provenance, licenses, sample counts, and class distributions in markdown specs.

## Step 10B design documents (GC-03)
Research design only; no dataset is stored or downloaded here.
- [`dataset_selection.md`](dataset_selection.md): candidate evaluation, primary/secondary selection, custom-capture protocol
- [`device_requirements.md`](device_requirements.md): smartphone requirements and telemetry access
- [`model_ladder.md`](model_ladder.md): C1–C4 ladder criteria and confidence signal
- [`measurement_hardware.md`](measurement_hardware.md): energy, thermal and hardware setup
- [`verification_checklist.md`](verification_checklist.md): checks required before implementation
- [`dataset_device_model_matrix.csv`](dataset_device_model_matrix.csv): dataset × device × model matrix
