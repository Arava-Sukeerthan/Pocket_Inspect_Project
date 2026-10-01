# Uncertainty Module (`src/uncertainty/`)

Implements confidence calibration, epistemic/aleatoric uncertainty quantification, and Out-Of-Distribution (OOD) sample detection.

## Responsibilities
- Model output calibration (e.g. Temperature Scaling, Platt scaling).
- OOD defect score calculation for unseen defect types.
- Human-in-the-loop review trigger generation when model confidence is low.
