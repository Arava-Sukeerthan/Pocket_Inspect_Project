# Gap Analysis Subsystem (`research/gap_analysis/`)

This directory maintains systematic research gap matrices, candidate lists, and decision records for PocketInspect.

---

## 1. Research Gap Analysis Principles

1. **Evidence-Based Gaps Only**: Gaps are identified exclusively by analyzing coverage across verified publications ingested into `research/literature/papers.csv`.
2. **No Automatic Novelty Claims**: Zero-coverage dimension intersections are tagged as `Candidate Gaps (Requires Researcher Verification)`, never as absolute novel contributions until verified.
3. **Epistemic Hygiene**: Unsupported assumptions or missing literature fields are marked as `unknown`, not inferred.

---

## 2. Key Research Dimensions Evaluated

| Gap ID | Key Dimension Combination | Focus Area |
| :--- | :--- | :--- |
| **GAP-001** | Smartphone + Adaptive Inference + Thermal Awareness | Thermal-sustainability in mobile inspection |
| **GAP-002** | 3D-Print Defect Inspection + Resource-Aware Edge AI | Resource-aware vision for additive manufacturing |
| **GAP-003** | Smartphone + On-Device Inference + Uncertainty Estimation | Out-of-distribution detection on mobile edge |
| **GAP-004** | Smartphone + Multi-View Inspection + On-Device | Multi-angle defect aggregation on mobile |
| **GAP-005** | Adaptive Inference + Thermal & Energy Evaluation | Dynamic resource balancing across thermal/power |
| **GAP-006** | 3D-Print Inspection + Anomaly Detection + On-Device | Semi-supervised anomaly scoring on edge |

---

## 3. Workflow for Researcher Gap Verification

1. Ingest candidate literature into `research/literature/papers.csv`.
2. Run `python scripts/manage_literature.py gap` to regenerate `gap_matrix.csv` and `gap_candidates.md`.
3. Review `gap_candidates.md` to verify whether candidate gaps are genuine research opportunities or missing literature.
4. Record final decision in `docs/decisions/` before freezing the paper contribution.
