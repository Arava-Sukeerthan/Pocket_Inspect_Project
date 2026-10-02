# Full-Text Verification Template

_Step 9.1, prepared 2026-10-04 by Claude Code. One evidence table per queued paper (see [`fulltext_verification_queue.md`](fulltext_verification_queue.md)). The "Current CSV Value" column is copied from `papers.csv` at commit `9ebbf89`. All other columns are **blank on purpose** and are filled during full-text verification._

## Instructions

1. **Use the existing definitions only.** Code against [`README.md` §7 v1.1](README.md#7-literature-coding-definitions) and [`coding_decisions.md`](coding_decisions.md). Do not create new definitions; raise borderline cases as `Needs researcher decision`.
2. **Record the source used** at the top of each paper section: version of record, accepted manuscript, or preprint. Give the URL and access date. Preprints can differ from the published version; note this when it matters.
3. **Evidence Location:** section number or title, page number **as printed in the source used**, and figure/table/equation number where relevant. Never estimate or invent page numbers. If the source has no page numbers (HTML), give the section heading only.
4. **Evidence Quote/Paraphrase:**
   - Prefer a short paraphrase.
   - Use a direct quote only when the wording decides the coding. Keep it under 15 words and in quotation marks.
   - Never reconstruct a quote from memory.
5. **Confidence** must be one of:
   - `Confirmed`: the full text clearly supports the value under the definition;
   - `Not supported`: the full text contradicts the value, or nothing supports it after reading the relevant sections;
   - `Ambiguous`: the text is unclear, or the case falls between definitions.
6. **Action** must be one of:
   - `Keep`: the CSV value stands;
   - `Change`: the CSV value should change; give the proposed value in the Full-Text Value column;
   - `Needs researcher decision`: use for every `Ambiguous` row and for anything touching relevance class.
7. **Do not edit `papers.csv` while verifying.** Proposed changes are reviewed by the researcher/ChatGPT first and then applied as a separate, logged task (README §7.7).
8. **Fields not in the CSV schema** (inference location, adaptation mechanism, resource signals, evaluation metrics, deployment setting) are recorded here for context. Changes they imply go through the related CSV field.

## Blank template (for papers added to the queue later)

### Pxxx — <title>

- **Source used:** <version of record / accepted manuscript / preprint> — <URL> — accessed <date>
- **Verifier / date:**

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone |  |  |  |  |  |  |
| edge_device |  |  |  |  |  |  |
| on_device |  |  |  |  |  |  |
| cloud |  |  |  |  |  |  |
| adaptive_inference |  |  |  |  |  |  |
| resource_awareness |  |  |  |  |  |  |
| energy_evaluation |  |  |  |  |  |  |
| thermal_evaluation |  |  |  |  |  |  |
| multi_view |  |  |  |  |  |  |
| uncertainty |  |  |  |  |  |  |
| confidence_gating |  |  |  |  |  |  |
| anomaly_detection |  |  |  |  |  |  |
| latency_evaluation |  |  |  |  |  |  |
| accuracy_metrics |  |  |  |  |  |  |
| efficiency_metrics |  |  |  |  |  |  |
| paper type |  |  |  |  |  |  |
| application/domain |  |  |  |  |  |  |
| dataset |  |  |  |  |  |  |
| hardware/device |  |  |  |  |  |  |
| model(s) |  |  |  |  |  |  |
| inference location |  |  |  |  |  |  |
| adaptation mechanism |  |  |  |  |  |  |
| resource signals |  |  |  |  |  |  |
| evaluation metrics |  |  |  |  |  |  |
| limitations |  |  |  |  |  |  |
| deployment setting |  |  |  |  |  |  |

---

## P001 — Deep learning smartphone application for real‐time detection of defects in buildings

- **DOI:** [10.1002/stc.2751](https://doi.org/10.1002/stc.2751) · **Year:** 2021 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (Wiley Online Library), open access CC BY-NC; full-text HTML confirmed in browser. Alternative: —.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** on_device Unknown: where inference runs (on the phone vs a server) is not stated in the abstract; latency_evaluation Unknown: "real-time" claimed without a reported timing value; hardware: smartphone model not stated; model architecture not stated in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Smartphone / Mobile AI / Real-time detection of building defects (cracks, mould, stain, paint deterioration) |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Smartphone (model not stated in abstract) |  |  |  |  |  |
| model(s) | Deep learning model (architecture not stated in abstract) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P002 — A Road Defect Detection System Using Smartphones

- **DOI:** [10.3390/s24072099](https://doi.org/10.3390/s24072099) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (MDPI Sensors), open access CC BY; full-text HTML confirmed in browser. Alternative: PubMed Central PMC11014122 (page responded HTTP 200).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** **Modality check:** the publisher page section headings (seen 2026-10-04 while checking access, text not read) include "Vibration Sensor-Based ..." and "1D-CNN". Verify whether the system uses camera images at all; this bears on relevance class A, which is a researcher decision; latency_evaluation recoded Yes→Unknown (Decision 3): check for a measured timing value; on_device Unknown: where the CNN runs (phone vs server); Audit: latency claim was comparative only

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Smartphone / Mobile AI / Road defect classification (speed bumps, manholes, potholes) |  |  |  |  |  |
| dataset | Automatically collected and labelled smartphone data |  |  |  |  |  |
| hardware/device | Commercial smartphones |  |  |  |  |  |
| model(s) | CNN-based classifier |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

- **DOI:** [10.1155/2022/9221211](https://doi.org/10.1155/2022/9221211) · **Year:** 2022 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (Wiley/Hindawi Advances in Civil Engineering), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** on_device / edge_device: confirm inference runs on the OAK-D (vs the Raspberry Pi host) and the measurement conditions of 31.76 FPS; latency type: throughput/FPS; check whether per-frame latency is also reported; energy_evaluation / thermal_evaluation Unknown; Provenance note: assigned G1, retrieved by a G4 query

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | No |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Yes |  |  |  |  |  |
| accuracy_metrics | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D |  |  |  |  |  |
| efficiency_metrics | Tiny-YOLOv4 31.76 FPS on OAK-D |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Edge AI / Embedded vision / Real-time pothole detection on an edge AI device |  |  |  |  |  |
| dataset | Pothole image dataset (diverse road and illumination conditions) plus real-time vehicle video |  |  |  |  |  |
| hardware/device | OAK-D AI kit on Raspberry Pi |  |  |  |  |  |
| model(s) | YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetV2 |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

- **DOI:** [10.1016/j.inffus.2024.102782](https://doi.org/10.1016/j.inffus.2024.102782) · **Year:** 2025 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (Elsevier Information Fusion) listed as open access CC BY-NC by OpenAlex, but ScienceDirect returned a bot check, so access was not confirmed. Alternative: arXiv 2407.11771 (author preprint; same title and authors; PDF responded). May differ from the version of record.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** smartphone Unknown: identify the "mobile devices" used for deployment; on_device Yes rests on deployment wording (audit): confirm inference runs on the device; cloud Unknown: check where the vision-language-model explanation step runs; efficiency_metrics blank: abstract reports model-size reduction without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Industrial Visual Inspection / Edge AI / Explainable visual quality inspection with semantic segmentation on low-resource edge devices |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Low-resource edge / mobile devices (models not stated in abstract) |  |  |  |  |  |
| model(s) | Semantic segmentation model + XAI + Large Vision Language Model explanations |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

- **DOI:** [10.1038/s41467-022-31985-y](https://doi.org/10.1038/s41467-022-31985-y) · **Year:** 2022 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (Nature Communications), open access CC BY; PDF responded. Alternative: PubMed Central PMC9378646; Cambridge Apollo repository.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** edge_device / on_device Unknown: identify the hardware running real-time detection and the control loop; latency_evaluation Unknown: real-time detection/correction claimed without values; confidence_gating Unknown: check whether prediction confidence triggers corrections; multi_view Unknown: camera configuration (number of cameras/poses)

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time error detection and correction in material extrusion 3D printing |  |  |  |  |  |
| dataset | 1.2 million images from 192 parts labelled with printing parameters |  |  |  |  |  |
| hardware/device | Unknown |  |  |  |  |  |
| model(s) | Multi-head neural network with control loop |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

- **DOI:** [10.3390/pr8111464](https://doi.org/10.3390/pr8111464) · **Year:** 2020 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (MDPI Processes), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** edge_device / on_device Unknown: abstract mentions "microprocessors and a camera" generically; latency_evaluation Unknown: "fast speed" claimed without values; confidence_gating Unknown: check whether detections trigger stop/correction via a confidence threshold

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time stringing defect detection during FFF printing from camera video |  |  |  |  |  |
| dataset | Images showing stringing defects |  |  |  |  |  |
| hardware/device | Microprocessor plus camera (not specified in abstract) |  |  |  |  |  |
| model(s) | Deep CNN |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

- **DOI:** [10.1016/j.promfg.2018.07.111](https://doi.org/10.1016/j.promfg.2018.07.111) · **Year:** 2018 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Inaccessible (from this environment). Publisher (Elsevier Procedia Manufacturing) listed as gold open access CC BY-NC-ND by OpenAlex and Semantic Scholar; ScienceDirect bot check blocked confirmation. Likely readable in a normal browser. Alternative: None found (arXiv exact-title search: no match).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** multi_view Unknown: images taken "at several critical stages" — verify whether the camera pose changes (CD-09); Inference hardware and location not stated; latency_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Good/defective classification of semi-finished 3D printed parts |  |  |  |  |  |
| dataset | ABS and PLA printed parts imaged at critical print stages |  |  |  |  |  |
| hardware/device | Camera integrated with printer |  |  |  |  |  |
| model(s) | Support vector machine |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

- **DOI:** [10.1007/s00170-024-14452-4](https://doi.org/10.1007/s00170-024-14452-4) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Abstract only. Publisher (Springer IJAMT) subscription; abstract on landing page. Alternative: None found (OpenAlex closed; arXiv exact-title search: no match; Semantic Scholar: no open PDF).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** edge_device / on_device Unknown: identify the hardware on which FPS was measured and whether the detection system is deployed on edge hardware; latency type: throughput/FPS (relative +18.1%); check for absolute values; hardware not stated in abstract

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Yes |  |  |  |  |  |
| accuracy_metrics | mAP50 97.5% |  |  |  |  |  |
| efficiency_metrics | FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8 |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time detection of five common FFF printing defects |  |  |  |  |  |
| dataset | Deliberately designed defect dataset (five defect types) |  |  |  |  |  |
| hardware/device | Unknown |  |  |  |  |  |
| model(s) | Improved YOLOv8 with lightweight group-convolution detection head |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P019 — Real-time defect detection in 3D printing using machine learning

- **DOI:** [10.1016/j.matpr.2020.10.482](https://doi.org/10.1016/j.matpr.2020.10.482) · **Year:** 2021 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Abstract only. Publisher (Elsevier Materials Today: Proceedings) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** Inference hardware and location not stated (printer-integrated camera only); latency_evaluation Unknown: "real-time" claimed without values; anomaly_detection Unknown: confirm supervised vs normal-only training

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time detection of infill defects in 3D printing |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Camera integrated with 3D printer |  |  |  |  |  |
| model(s) | CNN image classifier |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

- **DOI:** [10.3390/asi4020034](https://doi.org/10.3390/asi4020034) · **Year:** 2021 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Full text available. Publisher (MDPI Applied System Innovation), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** anomaly_detection Unknown: abstract says "anomaly detection" but describes supervised classifiers (CD-14); Hardware / inference location not stated; "low computing costs" and real-time suitability claimed without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Layer-wise fault detection in FDM printing |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Unknown |  |  |  |  |  |
| model(s) | Pretrained CNN features + ML classifiers (AlexNet + SVM best) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

- **DOI:** [10.1108/rpj-09-2024-0395](https://doi.org/10.1108/rpj-09-2024-0395) · **Year:** 2025 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Abstract only. Publisher (Emerald Rapid Prototyping Journal) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** edge_device / on_device Unknown: Raspberry Pi is the acquisition system; verify whether inference runs on it; latency_evaluation Unknown; efficiency figures not in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | Warping 98.59% (DenseNet121); stringing 99.38% (MobileNetV2); cracking 99.32% (XceptionNet); multi-class 98.90% (MobileNetV2) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Warping, stringing and cracking detection in 3D-printed PLA/ABS parts |  |  |  |  |  |
| dataset | Defect images from Taguchi L9 design (extruder temp, bed temp, print speed) on a Delta printer |  |  |  |  |  |
| hardware/device | Raspberry Pi-based data acquisition |  |  |  |  |  |
| model(s) | DenseNet121, MobileNetV2, ResNet50, VGG16, XceptionNet (transfer learning) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

- **DOI:** [10.1016/j.mfglet.2019.09.005](https://doi.org/10.1016/j.mfglet.2019.09.005) · **Year:** 2019 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Abstract only. Publisher (Elsevier Manufacturing Letters) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** Inference hardware and location not stated; latency_evaluation Unknown: "faster than the speed of a human's response" is qualitative; confidence_gating Unknown: check whether correction is triggered by prediction confidence

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time monitoring and autonomous correction of FDM extrusion errors |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Unknown |  |  |  |  |  |
| model(s) | Deep learning model with feedback loop |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

- **DOI:** [10.1145/3241539.3241559](https://doi.org/10.1145/3241539.3241559) · **Year:** 2018 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (ACM MobiCom) listed as open access by OpenAlex; ACM returned a bot check, not confirmed. Alternative: arXiv 1810.10090 (same title; PDF responded). May differ from the version of record.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** smartphone Unknown: identify the evaluation platforms (abstract lists smartphones only as examples); Confirm efficiency_metrics values and baselines (up to 2.0x frame rate, 1.7x energy); thermal_evaluation / confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Yes |  |  |  |  |  |
| resource_awareness | Yes |  |  |  |  |  |
| energy_evaluation | Yes |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Yes |  |  |  |  |  |
| accuracy_metrics | Up to +4.2% inference accuracy vs resource-agnostic baseline |  |  |  |  |  |
| efficiency_metrics | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Adaptive Inference / Mobile Vision / Resource-aware multi-tenant on-device deep learning for continuous mobile vision |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | Mobile vision systems (platform not stated in abstract) |  |  |  |  |  |
| model(s) | NestDNN |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

- **DOI:** [10.1145/3649329.3657310](https://doi.org/10.1145/3649329.3657310) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (ACM/IEEE DAC 2024) closed per OpenAlex. Alternative: arXiv 2410.10847 (same title and 8 authors; PDF responded). May differ from the version of record.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** adaptive_inference recoded Yes→Unknown (Decision 4): confirm whether any model-level adaptation exists beyond CPU/GPU DVFS; latency_evaluation recoded Yes→Unknown (Decision 3): check for measured latency/variation values; smartphone: confirm Mi 11 Lite variant (4G/5G) used; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Yes |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Yes |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Thermal-aware Edge AI / Thermal and latency-variation management for two-stage detectors |  |  |  |  |  |
| dataset | Unknown |  |  |  |  |  |
| hardware/device | NVIDIA Jetson Orin Nano; Mi 11 Lite mobile platform |  |  |  |  |  |
| model(s) | LOTUS (DRL-based joint CPU/GPU frequency scaling) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

- **DOI:** [10.1145/3793860](https://doi.org/10.1145/3793860) · **Year:** 2026 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Inaccessible (from this environment). Publisher (ACM TECS) closed; OpenAlex lists a green copy in the Uppsala DiVA repository (urn:nbn:se:uu:diva-587035). Alternative: DiVA record did not respond from this environment (connection failed; browser navigation refused). Needs a manual check.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** latency_evaluation recoded Yes→Unknown (Decision 3): check for measured frame-rate values; smartphone Unknown: identify the evaluation devices; confidence_gating Unknown: check whether multi-exit decisions use prediction confidence or only thermal state; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Yes |  |  |  |  |  |
| resource_awareness | Yes |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Yes |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Thermal-aware Edge AI / Thermal-aware multi-DNN on-device inference for mobile video |  |  |  |  |  |
| dataset | Two benchmarks + Virtual YouTuber streaming app |  |  |  |  |  |
| hardware/device | Mobile devices with heterogeneous processors |  |  |  |  |  |
| model(s) | Phoenix (RL task allocation + multi-exit networks) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

- **DOI:** [10.1145/3665868](https://doi.org/10.1145/3665868) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (ACM TECS) listed as open access CC BY by OpenAlex; ACM returned a bot check, not confirmed. Alternative: arXiv 2409.01089 (same title; PDF responded). May differ from the version of record.
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** smartphone Unknown: identify the evaluation devices; latency_evaluation Unknown: check for measured latency/SLO results; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Yes |  |  |  |  |  |
| resource_awareness | Yes |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Adaptive Inference / Mobile / Constraint-aware runtime adaptation for single- and multi-DNN workloads on heterogeneous mobile devices |  |  |  |  |  |
| dataset | Text classification, scene recognition, face analysis tasks |  |  |  |  |  |
| hardware/device | Heterogeneous mobile devices |  |  |  |  |  |
| model(s) | CARIn (multi-objective optimisation + RASS solver) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

- **DOI:** [10.1109/tmc.2025.3594214](https://doi.org/10.1109/tmc.2025.3594214) · **Year:** 2026 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (IEEE TMC) listed as open access CC BY by OpenAlex; IEEE Xplore page not confirmed automatically. Alternative: FH JOANNEUM ePUB repository (submitted version, CC BY; PDF responded).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** latency_evaluation recoded Yes→Unknown: only adaptation time is in the abstract; check for inference latency on the four platforms; smartphone Unknown: identify the four "mobile and embedded" platforms; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Yes |  |  |  |  |  |
| on_device | Yes |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Yes |  |  |  |  |  |
| resource_awareness | Yes |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Adaptive Inference / Edge / Deep subnetworks that adapt to dynamic resource constraints on edge devices |  |  |  |  |  |
| dataset | Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K |  |  |  |  |  |
| hardware/device | Four mobile and embedded platforms incl. Arduino Nano 33 BLE |  |  |  |  |  |
| model(s) | REDS |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |

## P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

- **DOI:** [10.1016/j.aei.2020.101101](https://doi.org/10.1016/j.aei.2020.101101) · **Year:** 2020 · **Relevance class (audit):** D · **Priority:** HIGH
- **Accessibility (2026-10-04):** Alternative legitimate source. Publisher (Elsevier Advanced Engineering Informatics) listed as open access CC BY-NC-ND by OpenAlex; ScienceDirect bot check, not confirmed. Alternative: UTS institutional repository hdl:10453/147577 (hosts the publisher PDF of the article; PDF responded).
- **Source used:** 
- **Verifier / date:** 
- **Issues to resolve:** **Relevance (audit class D):** verify whether the quality inspection is image/vision-based or uses process data; edge_device and cloud recoded Yes→Unknown: identify the hardware behind "Edge Cloud Computing" and where models run; on_device / latency_evaluation Unknown; Relevance class must not be changed without researcher review

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown |  |  |  |  |  |
| edge_device | Unknown |  |  |  |  |  |
| on_device | Unknown |  |  |  |  |  |
| cloud | Unknown |  |  |  |  |  |
| adaptive_inference | Unknown |  |  |  |  |  |
| resource_awareness | Unknown |  |  |  |  |  |
| energy_evaluation | Unknown |  |  |  |  |  |
| thermal_evaluation | Unknown |  |  |  |  |  |
| multi_view | Unknown |  |  |  |  |  |
| uncertainty | Unknown |  |  |  |  |  |
| confidence_gating | Unknown |  |  |  |  |  |
| anomaly_detection | Unknown |  |  |  |  |  |
| latency_evaluation | Unknown |  |  |  |  |  |
| accuracy_metrics | (blank) |  |  |  |  |  |
| efficiency_metrics | (blank) |  |  |  |  |  |
| paper type | system/method |  |  |  |  |  |
| application/domain | Industrial Quality Inspection / Edge-Cloud / Predictive model-based quality inspection in SMT manufacturing |  |  |  |  |  |
| dataset | Real industrial SMT use case |  |  |  |  |  |
| hardware/device | Edge Cloud Computing infrastructure |  |  |  |  |  |
| model(s) | Machine learning (models not stated in abstract) |  |  |  |  |  |
| inference location | not a CSV field — see on_device / cloud / notes |  |  |  |  |  |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence |  |  |  |  |  |
| resource signals | not a CSV field — see resource_awareness / evidence |  |  |  |  |  |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics |  |  |  |  |  |
| limitations | (blank) |  |  |  |  |  |
| deployment setting | not a CSV field — see application / notes |  |  |  |  |  |
