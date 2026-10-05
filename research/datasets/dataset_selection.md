# Dataset Evaluation and Selection — GC-03

_Step 10B, 2026-10-05, Claude Code. Research design only: no dataset was downloaded, opened or inspected._

Approved gap: [`research_gap.md`](../gap_analysis/research_gap.md). Hypotheses: [`hypotheses.md`](../research_questions/hypotheses.md). Matrix: [`dataset_device_model_matrix.csv`](dataset_device_model_matrix.csv). Verification steps: [`verification_checklist.md`](verification_checklist.md). Declarative record: [`configs/dataset_device_model.yaml`](../../configs/dataset_device_model.yaml).

## 1. Evidence Rules

**Evidence levels.** Each fact below carries one of these levels:

| Level | Meaning |
| :-- | :-- |
| `official_repo` | Read on 2026-10-05 from the dataset's official GitHub repository. |
| `search_summary` | Taken from a web-search result summary on 2026-10-05. The official page was not read; secondary evidence only. |
| `corpus_record` | As recorded in `papers.csv` or the Step 9.8–9.9 configs; not re-checked against the dataset itself. |
| `not_found` | No evidence obtained. |

**Blocked hosts.** The egress proxy blocked `mvtec.com`, `realiad4ad.github.io`, `arxiv.org` and `huggingface.co`. Those pages could not be read. Sources actually read or searched are listed in §8.

**Licence status.**
- A licence stated on an official page is recorded as `stated_by_source`, never as verified.
- Verifying a licence also needs the full terms to be read, any access agreement to be accepted, and use to be confirmed compatible with the project.
- No dataset licence is VERIFIED.

**Decision statuses** (Step 10B rule): VERIFIED, SUPPORTED, PROVISIONAL, REQUIRES_VERIFICATION.
- **Nothing in this document is VERIFIED.** Nothing was downloaded or inspected.

**Suitability classes:** SUITABLE, POSSIBLY_SUITABLE, UNSUITABLE, REQUIRES_VERIFICATION.
- **No candidate is SUITABLE.** That class needs verified access, licence and content.

## 2. What GC-03 Needs from Data

| Need | Why | Hypotheses |
| :-- | :-- | :-- |
| Optical defect-inspection images with item-level defect labels | Recall, precision and F1 need ground truth. | H1, H2, H5 |
| Enough defective samples for a held-out calibration split and a test split | Calibration (H4) and thresholds must not be fitted on test data. | H2, H4 |
| One task, one label space for all configurations | Comparable outputs across C1–C4. | H1, H4 |
| Multiple views of the same physical item, linked by item identity | Action A2 (additional view) and item-level decisions. | H2, H2.b |
| Repeated capture of the same view of the same item | Action A1 (recapture). | H2 |
| Smartphone-camera imaging | External validity of smartphone inspection. | All |
| Access and licence compatible with research use | Feasibility. | All |

Resource adaptation (R0–R3, C1–C4) and escalation (A3) do not depend on the dataset. Any image set can be replayed through the on-device models while device pressure is induced.

## 3. Candidate Evaluation

All candidates were already documented in the repository (Step 9.9 Phase A, `configs/gap_selection.yaml` `datasets`, and Step 9.9B). No new survey was run.

| Dataset | Domain | Inspection task | Modality | Classes / categories | Normal / defect structure | Resolution | Multi-view | Object identity | Defect annotation | Replay | Smartphone | Recapture | Custom capture required | Access | Licence | Known limitations | Evidence | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **Real-IAD** | Industrial components | Multi-view industrial anomaly detection | RGB | 30 objects (`official_repo`) | 99,721 normal / 51,329 anomalous samples, about 150K images (`search_summary`) | "2K ~ 5K" original (`search_summary`); a 1024-px version is distributed (`official_repo`) | Yes, five viewing angles (`search_summary`); single- and multi-view experiment configs (`official_repo`) | Per-object directories (`official_repo`); per-sample view linkage REQUIRES_VERIFICATION | Pixel masks + multi-view image labels | Yes (any image set) | Not phone-captured (professional camera, `search_summary`) | No | Yes, for A1 and smartphone realism | Download host not established: the official repository's README describes the archives (`realiad_jsons.zip`, per-object ZIPs at 1024 px and original resolution) but the project page was blocked; REQUIRES_VERIFICATION | **Dataset terms not established.** The code repository's `LICENSE` says "Real-IAD is licensed under the Apache License Version 2.0 except for the third-party components"; it is a code-repository licence file and does not by itself establish the terms of the image data. REQUIRES_VERIFICATION | Professional imaging, not a phone; not 3D-printed parts; anomaly-detection benchmark, so the supervised-split protocol must be designed | `official_repo` (github.com/Tencent/AnomalyDetection_Real-IAD), `search_summary` (counts, resolution, views), `corpus_record` P037 | POSSIBLY_SUITABLE |
| **MANTA** | Tiny objects (five domains) | Multi-view visual-text anomaly detection | RGB + text | 38 categories | over 137.3K images; 8.6K anomalous (`search_summary`) | Not obtained | Yes, five viewpoints (`search_summary`) | REQUIRES_VERIFICATION | Pixel-level | Yes | Not established | No | Yes | Project page `grainnet.github.io/MANTA` (not read) | Not found | Tiny objects; few anomalous images relative to size | `search_summary`, `corpus_record` P038 | REQUIRES_VERIFICATION |
| **MVTec AD** | Industrial objects and textures | Unsupervised anomaly detection / localisation | RGB | 15 categories; over 70 defect types (`search_summary`) | 5,354 images; defect-free training images, defects only in the test set (`search_summary`) | High resolution (exact not read) | No evidence of multiple views | No | Pixel masks | Yes | Not phone-captured (not established) | No | Yes | Official page blocked | CC BY-NC-SA 4.0, non-commercial (`search_summary`; official page not read) | Few defective images for supervised calibration plus test; single view | `search_summary`, `corpus_record` P009 | POSSIBLY_SUITABLE (replay / calibration sanity check only) |
| **VisA** | PCBs, capsules, food items, etc. | Visual anomaly detection | RGB | 12 categories | 10,821 images: 9,621 normal / 1,200 anomalous; 12 objects incl. four PCB types and multi-instance subsets (`official_repo`) | Not stated in repository | No evidence of multiple views | No | Pixel masks | Yes | Not established | No | Yes | S3 download URL in official repository | Data: CC BY 4.0 per README (`stated_by_source`, `official_repo`); the repository's own `LICENSE` file is Apache-2.0 (code) | Single view; anomalous share is small | `official_repo` (github.com/amazon-science/spot-diff) | POSSIBLY_SUITABLE (replay only) |
| **MVTec 3D-AD** | Industrial objects | 3D anomaly detection | RGB + 3D scans (structured-light industrial sensor) | 10 categories (`search_summary`) | over 4,000 scans; defects only in test (`search_summary`) | Not obtained | Multi-view per P043 corpus record; not confirmed by any source read | REQUIRES_VERIFICATION | Pixel masks | Partly (3D modality unused on phone) | No | No | Yes | Official page blocked | CC BY-NC-SA 4.0 (`search_summary`) | Main signal is 3D; RGB-only use discards it | `search_summary`, `corpus_record` P043 | UNSUITABLE as primary |
| **Eyecandies** | Synthetic candies | Multimodal anomaly detection | Rendered RGB (6 lightings) + depth + normals | 10 categories (`search_summary`) | Defect-free train/validation; anomalies only in test (`search_summary`) | Not obtained | Lighting variants, not physical views | Yes (synthetic objects) | Masks | Yes | No (synthetic) | No | Yes | Not read | "Research use" per a third-party summary (`search_summary`); official terms not read; REQUIRES_VERIFICATION | Synthetic rendering; no real camera noise | `search_summary`, `corpus_record` P043 | UNSUITABLE as primary |
| **DeepPCB** | PCBs | PCB defect detection | Template/test image pairs | 6 defect types | 1,500 aligned image pairs | 640 × 640 sub-images (about 48 px/mm) | No | Template/test pair only | Bounding boxes with class | Yes | No (linear-scan CCD) | No | Yes | Official GitHub repository | Repository `LICENSE` file is MIT (`official_repo`); the README states no separate data licence, so data terms REQUIRES_VERIFICATION | Template-differencing task; single view; scanner imaging; the README states that artificial defects were added manually to each tested image (3–12 defects per image), so defect realism is limited | `official_repo` (github.com/tangsanli5201/DeepPCB) | UNSUITABLE as primary |
| **NEU-DET** | Hot-rolled steel strip | Defect classification / detection | Grayscale | 6 classes | 1,800 grayscale images, all defective (300 per class); no normal class (`search_summary`) | 200 × 200 (`search_summary`) | No | No | Class labels; boxes (DET) | Yes | No | No | Yes | IEEE DataPort, DOI 10.21227/j84r-f770 (`search_summary`; page not read) | Not found; REQUIRES_VERIFICATION | No normal class; low resolution; single view | `search_summary`, Step 9.8 external | UNSUITABLE as primary |
| **KolektorSDD2** | Production items (surface) | Surface defect detection | RGB | Defect vs no defect | 356 defective / 2,979 defect-free; train 246+2,085, test 110+894 (`search_summary`) | about 230 × 630 (`search_summary`) | No | No | Masks | Yes | No | No | Yes | vicos.si (not read) | CC BY-NC-SA 4.0; commercial use by contact (`search_summary`) | Single view; small positive count | `search_summary`, Step 9.8 external | POSSIBLY_SUITABLE (replay only) |
| **MMS** | Micro-components | Cross-device anomaly detection | Microscope + IMX500 sensor | Defect types as reported | Not obtained | Not obtained | No (cross-device, same objects) | Same objects across devices | As reported | Yes | No | No | Yes | Not checked | Not found | Microscope / in-sensor imaging | `corpus_record` (TinyGLASS, Step 9.8) | UNSUITABLE as primary |
| **CAXTON** | 3D printing (FDM) | Extrusion-error detection | Printer-mounted camera frames | Not checked | 1,272,273 images from 192 prints (corpus) | Not obtained | No | Print-level | Process labels | Yes | No (printer-mounted) | No | Yes | Not checked | Not found | In-process monitoring, not post-print part inspection | `corpus_record` P015 | UNSUITABLE as primary |
| **P016 stringing set** | 3D printing | Stringing detection | Camera frames | Stringing | 500 images, augmented to 2,500 (corpus) | Not obtained | No | No | As reported | Yes | No | No | Yes | Unknown | Not found | Small; availability unknown | `corpus_record` P016 | UNSUITABLE as primary |
| **P020 layer images** | 3D printing (FDM) | Layer-wise fault detection | Raspberry Pi camera | Good / bad | 1,700 images (corpus) | Not obtained | No | No | Image labels | Yes | No | No | Yes | Unknown | Not found | Layer images during print | `corpus_record` P020 | UNSUITABLE as primary |
| **Phone-captured 3D-printed-part set** (Proposed idea) | 3D-printed parts (`PROJECT_SPEC.md` §1) | Post-print part inspection | Smartphone RGB | To be designed (seeded defects) | To be designed | Device-dependent | Yes, by protocol | Yes, by protocol (fiducial ID) | To be designed | Yes | Yes | Yes | **Is** the custom capture | To be created | Owned by the project; consent/licensing of any third-party parts to check | Does not exist; collection effort; annotation reliability | Proposed idea | REQUIRES_VERIFICATION (protocol only) |

## 4. Selection

| Role | Dataset | Decision status |
| :-- | :-- | :-- |
| **Primary dataset** | **Real-IAD** | **PROVISIONAL**: access, dataset licence, per-sample view linkage and annotation format REQUIRES_VERIFICATION |
| **Secondary dataset** | **Phone-captured 3D-printed-part set** | **PROVISIONAL — PROTOCOL ONLY**: it does not exist yet and is not an existing dataset (§6) |
| Fallback primary (if Real-IAD terms are unacceptable) | MANTA (multi-view) | REQUIRES_VERIFICATION |
| Optional replay-only sanity set | VisA (licence stated as CC BY 4.0 by its official repository) | SUPPORTED (licence statement only) |

**Not chosen for popularity.** MVTec AD is the most widely used of these benchmarks. It is not selected as primary because it has no multiple views and has few defective images for separate calibration and test splits.

### Why Real-IAD supports the central question

| Requirement | How Real-IAD meets it | Caveat |
| :-- | :-- | :-- |
| Defect inspection | Real industrial components with labelled anomalies and pixel masks. | Not 3D-printed parts. |
| Configuration comparison | One label space across 30 objects; the same images can be replayed through C1–C4. | Item-level labels must be derived from per-view labels (verify). |
| Confidence evaluation | The reported anomalous count (about 51K) is large enough for disjoint calibration and test splits, split by sample so views do not leak. | Counts are from search summaries; verify. |
| Resource adaptation | Dataset-independent: replay on the phone under induced R0–R3. | Replay uses stored images, so it measures inference cost, not capture cost. |
| Quantitative evaluation | Image- and sample-level labels support recall, precision, F1 and calibration metrics. | The supervised-classification protocol differs from the benchmark's unsupervised AD protocol (see [`model_ladder.md`](model_ladder.md) §1). |
| Additional view (A2) | Five views per sample can stand in for "acquire another view". | Fixed pre-recorded views, not chosen or captured by the phone; a stated limitation. |

### Stage boundary: simulated vs actual additional views

| Stage | Data | What it supports | What it does not support |
| :-- | :-- | :-- | :-- |
| **Stage 1 — controlled additional-view simulation** | Existing multi-view benchmark (Real-IAD) replayed on the phone | **Simulated additional-view decision:** when verification triggers A2, the next stored view of the same sample is loaded and re-inferred. Resource adaptation, A3 escalation, A4 referral, calibration (H4) and cost (H3, H5). | **Not physical smartphone recapture.** The views were captured beforehand by a professional camera at fixed angles. The phone neither chooses nor captures them, and the acquisition cost and variability of real capture are absent. Same-view recapture (A1) is not available. |
| **Stage 2 — actual recapture / additional-view experiment** | Custom smartphone capture (§6) | Actual same-view recapture (A1) and actual additional-view capture (A2) on the phone, with real acquisition cost, camera metadata and smartphone imaging. | Depends on the protocol being confirmed and the data being collected (gate G3); nothing is collected in Step 10B. |

**Real-IAD does not provide smartphone recapture data**, and it is not smartphone-captured. Stage 1 results on A2 are reported as *simulated* additional-view results and are never presented as smartphone recapture results (gate G2).

### Statement on recapture

**CUSTOM SMARTPHONE CAPTURE REQUIRED.**
- **Recapture (A1).** No evaluated static benchmark contains repeated captures of the same view of the same item. Real-IAD's five views are distinct viewpoints, not recaptures.
- **Smartphone-camera imaging.** No evaluated benchmark is smartphone-captured.

Both therefore require the secondary custom set. Stage 1 (Real-IAD replay) can test H1, H3, H4, H5 and the A2/A3/A4 parts of H2. A1 and smartphone realism are tested only in Stage 2 (custom capture).

## 5. Task Formulation (PROVISIONAL)

**Primary task.** Supervised, item-level binary defect classification (defective vs normal) per view, with an item-level decision rule across views.

**Why supervised and not unsupervised anomaly detection.**
- A supervised classifier gives a class-probability output whose calibration can be measured and adjusted (H4).
- Recall and precision are defined directly.
- Unsupervised anomaly scores need a separately fitted threshold and score normalisation. That would make the confidence signal configuration-specific in a way that is harder to compare.

**Alternative kept open.** Anomaly detection with normalised scores, if the supervised split proves infeasible (REQUIRES_VERIFICATION after data inspection).

## 6. Secondary Dataset: Minimum Custom-Capture Requirements (protocol only)

**PROVISIONAL — PROTOCOL ONLY.** The phone-captured 3D-printed-part set **does not exist** and must not be treated as an existing dataset. It is a capture protocol to be confirmed (gate G3) before any data are collected.

It requires all of the following:
- physical parts;
- controlled defect / non-defect conditions;
- item identifiers;
- repeated captures;
- same-view recapture;
- additional views;
- train/validation/test split by physical item;
- smartphone camera metadata;
- lighting/environment metadata;
- resource telemetry where appropriate (Stage 2 runs on the phone under R0–R3).

The numbered list below details them. No data are collected in Step 10B. Every count below is **TO BE DETERMINED BY POWER ANALYSIS / PILOT** and is not fixed here.

1. **Items.** 3D-printed parts of a pre-registered set of geometries, normal and with seeded defects from the project taxonomy (`PROJECT_SPEC.md` §1).
   - Each item carries a unique identifier: a fiducial or label outside the inspected region.
2. **Ground truth.** The defect presence and type of each item is fixed before capture. The method (design-seeded plus independent visual check) is recorded, and the defect must be visible in the views that are labelled defective.
3. **Views.** A pre-registered set of distinct viewpoints per item, held by a jig or turntable with indexed positions. This supports A2.
4. **Recapture.** Several repeated captures per (item, view), removing and re-placing the item between captures. This supports A1. The variation between recaptures (pose jitter, focus, exposure) is logged, not controlled away.
5. **Camera.** Fixed capture resolution. Exposure, focus, white balance and ISO are locked where the Camera2 API allows, and actual metadata is logged per frame.
6. **Lighting.** A fixed rig light, with ambient light recorded. An optional pre-registered lighting-variation factor.
7. **Splits.** By item, never by image, so that views and recaptures of one item never cross train/calibration/test.
8. **Defect-preserving views.** Each view's label records whether the defect is visible in that view. A view where the defect is hidden is labelled per view, so item-level and view-level ground truth can differ.
9. **Provenance.** Device, app version, capture time and rig configuration are stored with each image. Images are not committed to git.

## 7. Status

| Decision | Status |
| :-- | :-- |
| Candidates evaluated (14) | Done (desk evaluation) |
| Primary: Real-IAD | PROVISIONAL |
| Secondary: custom phone-captured set | PROVISIONAL — PROTOCOL ONLY (does not exist yet; gate G3) |
| Real-IAD multi-view use | Stage 1 controlled additional-view simulation only (gate G2) |
| Any dataset licence | REQUIRES_VERIFICATION (none verified) |
| Any dataset access | REQUIRES_VERIFICATION (none downloaded) |
| Recapture support in a static benchmark | Not available: CUSTOM SMARTPHONE CAPTURE REQUIRED |

## 8. Sources Read on 2026-10-05

| Source | Evidence level | Used for |
| :-- | :-- | :-- |
| `raw.githubusercontent.com/Tencent/AnomalyDetection_Real-IAD/main/README.md` and `LICENSE` | `official_repo` | Real-IAD objects, resolutions, configs, licence-file wording |
| `raw.githubusercontent.com/amazon-science/spot-diff/main/README.md` and `LICENSE` | `official_repo` | VisA counts, subsets, S3 host, data licence statement |
| `raw.githubusercontent.com/tangsanli5201/DeepPCB/master/README.md` and `LICENSE` | `official_repo` | DeepPCB counts, imaging, annotation, artificial defects, licence file |
| Web search summaries (Real-IAD CVPR 2024 paper pages; MVTec AD and MVTec 3D-AD pages and mirrors; vicos.si KolektorSDD2; MANTA CVPR 2025 pages; IEEE DataPort NEU-DET; Eyecandies summaries) | `search_summary` | Counts, resolutions and stated licences marked `search_summary` above |
| Blocked: `mvtec.com`, `realiad4ad.github.io`, `arxiv.org`, `huggingface.co` | `not_found` | — |

Search summaries are secondary evidence. No licence or access condition is VERIFIED.

