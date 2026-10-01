# Quality Assessment Module (`src/quality/`)

Provides fast pre-inference image validation routines to filter unusable frames before invoking heavy neural networks.

## Responsibilities
- Motion and defocus blur detection (e.g. Laplacian variance analysis).
- Under/over-exposure and illumination variance checks.
- Subject framing and Region of Interest (ROI) alignment verification.
