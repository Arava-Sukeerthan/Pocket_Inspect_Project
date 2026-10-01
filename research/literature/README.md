# Literature Management Subsystem (`research/literature/`)

This directory houses verified academic literature records, systematic survey matrices, and export tools for PocketInspect.

---

## 1. Literature Review Workflow

All literature added to PocketInspect follows a strict 6-step human-in-the-loop ingestion workflow:

1. **Identification**: ChatGPT/researcher identifies candidate papers relevant to mobile Edge AI, industrial visual inspection, or 3D-print defect detection.
2. **Verification**: Researcher verifies paper details (title, authors, year, venue, DOI, verified URL, and quantitative evidence).
3. **Ingestion**: Verified paper records are added to `research/literature/papers.csv`.
4. **Validation & Matrix Generation**: Automated scripts validate schema integrity, check for duplicate DOIs/titles, and compile `literature_matrix.csv`.
5. **Gap Extraction**: Literature coverage counts across research dimensions are evaluated objectively in `research/gap_analysis/`.
6. **Decision**: Final decisions on research gap claims are made after human researcher verification.

---

## 2. Schema Specification (`papers.csv`)

`papers.csv` contains exactly 29 mandatory columns:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `paper_id` | String (Required) | Unique identifier key (e.g. `P001` or `Author2024`) |
| `title` | String (Required) | Full verified title of paper |
| `authors` | String (Required) | Author names (e.g., "Smith J., Doe A.") |
| `year` | Integer (Required) | Year of publication (e.g., `2023`) |
| `venue` | String | Journal or conference venue (e.g., "IEEE TIM", "CVPR") |
| `doi` | String | Digital Object Identifier (e.g., `10.1109/...`) |
| `url` | String | Direct URL link to publisher or arXiv page |
| `domain` | String | Primary domain (e.g., "3D-Print Inspection", "Edge AI") |
| `application` | String | Specific target application |
| `dataset` | String | Dataset used in paper |
| `model` | String | Neural architecture or computer vision algorithm |
| `hardware` | String | Hardware platform tested (e.g., "Snapdragon 888", "Jetson Nano") |
| `smartphone` | Boolean (`true`/`false`) | Evaluated specifically on a smartphone device |
| `edge_device` | Boolean (`true`/`false`) | Evaluated on an edge device |
| `on_device` | Boolean (`true`/`false`) | Inference executed fully on-device without cloud |
| `cloud` | Boolean (`true`/`false`) | Offloads compute to cloud servers |
| `adaptive_inference` | Boolean (`true`/`false`) | Implements dynamic runtime adaptation |
| `resource_awareness` | Boolean (`true`/`false`) | Considers CPU/GPU/RAM constraints |
| `energy_evaluation` | Boolean (`true`/`false`) | Quantifies power consumption or battery drain |
| `thermal_evaluation` | Boolean (`true`/`false`) | Quantifies device temperature or thermal throttling |
| `multi_view` | Boolean (`true`/`false`) | Uses multi-camera angle inspection |
| `uncertainty` | Boolean (`true`/`false`) | Evaluates prediction uncertainty or OOD detection |
| `anomaly_detection` | Boolean (`true`/`false`) | Evaluates unsupervised/semi-supervised anomaly detection |
| `latency_evaluation` | Boolean (`true`/`false`) | Reports inference latency or FPS |
| `accuracy_metrics` | String | Primary accuracy metric values reported (e.g. "mAP@0.5: 88.4%") |
| `limitations` | String | Explicitly documented limitations |
| `future_work` | String | Future work directions noted by authors |
| `evidence` | String | Verified empirical evidence quotes or metric summaries |
| `notes` | String | Additional notes |

*Note: For missing or unknown information, leave the column empty or enter `unknown`. Never guess or infer unsupported metadata.*

---

## 3. Literature Management Commands

Use `scripts/manage_literature.py` to manage and process literature:

```bash
# Validate papers.csv schema and check for duplicates
python scripts/manage_literature.py validate

# View summary statistics across verified literature
python scripts/manage_literature.py stats

# Generate literature_matrix.csv
python scripts/manage_literature.py matrix

# Generate gap_matrix.csv and gap_candidates.md
python scripts/manage_literature.py gap

# Export literature matrix to LaTeX or Markdown format
python scripts/manage_literature.py export --format latex --out research/tables/literature_table.tex

# Run complete pipeline
python scripts/manage_literature.py all
```
