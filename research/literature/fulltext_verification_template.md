# Full-Text Verification Template

_Step 9.1 prepared the blank tables (commit `b77072f`). **Step 9.2 (2026-10-03, Claude Code) filled them with full-text evidence.** The "Current CSV Value" column is unchanged from `papers.csv` (commit `9ebbf89`); `papers.csv` was not modified. Proposed changes are summarised in [`fulltext_conflicts.md`](fulltext_conflicts.md) and explained per paper in [`fulltext_evidence_report.md`](fulltext_evidence_report.md)._

## Instructions

1. **Use the existing definitions only.** Code against [`README.md` §7 v1.1](README.md#7-literature-coding-definitions) and [`coding_decisions.md`](coding_decisions.md). Do not create new definitions; raise borderline cases as `Needs researcher decision`.
2. **Record the source used** at the top of each paper section: exact source, URL or identifier, version, version type (publisher version / accepted manuscript / preprint / submitted version), whether it may differ from the version of record, and which parts were read. Do not assume a preprint is identical to the published paper.
3. **Evidence Location:** section number or title, page number **as printed in the source used**, and figure/table/equation number where relevant. Never estimate or invent page numbers. If the source has no page numbers (HTML, PMC text), give the section heading only.
4. **Evidence Quote/Paraphrase:**
   - Prefer a short paraphrase.
   - Use a direct quote only when the wording decides the coding. Keep it under 15 words and in quotation marks.
   - Never reconstruct a quote from memory.
   - `full text read; no occurrence` means the whole text was read and the characteristic does not occur.
5. **Confidence** must be one of:
   - `Confirmed`: the full text clearly supports the value under the definition;
   - `Not supported`: the full text contradicts the value, or nothing supports it after reading the relevant sections;
   - `Ambiguous`: the text is unclear, or the case falls between definitions.
6. **Action** (extended in Step 9.2 to the four recommended actions; the coding definitions are unchanged):
   - `Keep current value`: the CSV value stands (Step 9.1 `Keep`);
   - `Candidate change`: the full text supports a different value, given in the Full-Text Value column (Step 9.1 `Change`). Not applied until reviewed;
   - `Needs researcher decision`: every `Ambiguous` row and anything touching relevance class. The current value is kept meanwhile;
   - `Insufficient evidence`: the full text was not available, or the deciding content (e.g. a figure) was not visible. The current value is kept.
7. **Do not edit `papers.csv` while verifying.** Proposed changes are reviewed by the researcher/ChatGPT first and then applied as a separate, logged task (README §7.7).
8. **Fields not in the CSV schema** (inference location, adaptation mechanism, resource signals, evaluation metrics, deployment setting) are recorded here for context. Changes they imply go through the related CSV field.
9. **Verification status** of each paper is one of: `Fully verified` (full text of the version of record, or a copy in the publisher's final layout, read); `Partially verified` (full text read, but only a preprint or a copy whose version could not be confirmed); `Blocked` (no legitimate full text obtained; abstract-level coding stands).

## Blank template (for papers added to the queue later)

### Pxxx — <title>

- **Verification status:** 
- **Source used:** 
- **URL / identifier:** 
- **Version:** 
- **Version type:** 
- **May differ from version of record:** 
- **Parts read:** 
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
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (Wiley Online Library), open access CC BY-NC; full-text HTML confirmed in browser. Alternative: —.
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** none obtained. Open access (Wiley, CC BY-NC; Semantic Scholar/OpenAlex list https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/stc.2751), but Wiley Online Library could not be fetched from this environment (egress policy and fetch failures).
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** on_device Unknown: where inference runs (on the phone vs a server) is not stated in the abstract; latency_evaluation Unknown: "real-time" claimed without a reported timing value; hardware: smartphone model not stated; model architecture not stated in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | Smartphone / Mobile AI / Real-time detection of building defects (cracks, mould, stain, paint deterioration) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Smartphone (model not stated in abstract) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | Deep learning model (architecture not stated in abstract) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P002 — A Road Defect Detection System Using Smartphones

- **DOI:** [10.3390/s24072099](https://doi.org/10.3390/s24072099) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (MDPI Sensors), open access CC BY; full-text HTML confirmed in browser. Alternative: PubMed Central PMC11014122 (page responded HTTP 200).
- **Verification status (Step 9.2):** Fully verified
- **Source used:** PubMed Central full text of the published article (PMC11014122), retrieved through the PubMed full-text service
- **URL / identifier:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11014122/ (DOI 10.3390/s24072099)
- **Version:** Publisher version of record as deposited in PMC (Sensors 2024, 24(7), 2099; CC BY)
- **Version type:** publisher version
- **May differ from version of record:** No (version of record). The PMC text extraction omits table bodies, figure images and figure/table numbers, so evidence is cited by section heading; values that exist only inside tables or figures were not seen.
- **Parts read:** All running text read (Introduction to Conclusions). Tables and figures not available in the extraction.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** **Modality check:** the publisher page section headings (seen 2026-10-04 while checking access, text not read) include "Vibration Sensor-Based ..." and "1D-CNN". Verify whether the system uses camera images at all; this bears on relevance class A, which is a researcher decision; latency_evaluation recoded Yes→Unknown (Decision 3): check for a measured timing value; on_device Unknown: where the CNN runs (phone vs server); Audit: latency claim was comparative only

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | §3.1.1; §4.1 | An Android app records 3-axis accelerometer data at 100 Hz on three phones (Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7). The phone is the sensing device; its camera is not used. | Confirmed | Keep current value |
| edge_device | Unknown | Unknown | §3.2 (last paragraph); §4.1; §5 | The quantized RDD-CNN is converted with the TFLite Converter and is "designed for execution on smartphones"; the conclusions state the scope is real-time classification on local smartphones. No on-phone run or on-phone timing is described. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §3.2; §4.1; §5 | Same evidence as edge_device: on-phone execution is stated as intended and as the scope, but not described as executed or measured. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | §5 | A cloud server for a live defect map is future work only; no cloud processing in the evaluated system. | Confirmed | Candidate change |
| adaptive_inference | Unknown | Unknown | §3.2 (Algorithm 1); §4.3 | The RDD-CNN is fixed. A sliding window (3 s, 0.1 s stride) jumps ahead after a detection, so the number of tests per minute depends on the input. This changes how often the model is invoked, not the model's computation; whether such stream-level skipping counts is not covered by the §7.3 table. Leaning No. | Ambiguous | Needs researcher decision |
| resource_awareness | Unknown | No | §3.2; §4.3 | 32-bit to 16-bit quantization lightens the model for phones (59.11% smaller). Design-time lightweighting with no stated device budget or runtime resource signal. | Confirmed | Candidate change |
| energy_evaluation | Unknown | No | full text read; no occurrence | No energy, power or battery result. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No temperature or throttling measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §3.2; §4.1 | The deployed input is a 300x1 accelerometer RMS series. Dashcam video (front/rear) is used only to label training data. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation or calibration. | Confirmed | Candidate change |
| confidence_gating | Unknown | Unknown | §3.1.2; §4.2 | Label quality verifier: a sliced sample is kept only if at least 90% of its 30 YOLOv5m frame classifications agree; otherwise it is discarded. This is a vote-consistency gate during dataset construction, not a confidence score acting on the deployed classifier. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | §3.2; §4.3 | Supervised classification of speed bumps, manholes and potholes from labelled data. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Unknown | §4.1; §4.3; §5 | Average time per model to evaluate 1 min of test data is reported (about 0.1 s per minute of driving for RDD-CNN), but the hardware used for the timing is not stated; preprocessing ran in a Linux/Python 3.8.10 environment. README §7.3 requires stated or identifiable hardware. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | RDD-CNN accuracy stated as "exceeding 86.77%" vs other models (§5); speed bump vs no-defect 99% (§4.3); YOLOv5m labeller 95.17% average per image (§4.2); automatic collection missed 15.21% of data with 100% label accuracy (§5) | §4.2; §4.3; §5 | Values as stated in the running text; per-model accuracies are in a figure not visible in the extraction. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB | §4.1; §4.3; §5 | Values as stated in the running text. | Confirmed | Candidate change |
| paper type | system/method | system/method | §3-§5 | Proposes an automatic data-collection system and the RDD-CNN classifier and evaluates both. | Confirmed | Keep current value |
| application/domain | Smartphone / Mobile AI / Road defect classification (speed bumps, manholes, potholes) | Road defect classification (speed bump, manhole, pothole) from smartphone accelerometer (vibration) signals in moving vehicles. Not image-based inspection. | §1 (last paragraph); §3 | "a road defect detection system based on vibration sensors, specifically accelerometers" (§1). | Confirmed | Needs researcher decision |
| dataset | Automatically collected and labelled smartphone data | Self-collected: 20 h / 300 km training drive and 8 h / 120 km test drive (Cheongju, Korea); 576 speed bumps, 290 manholes, 271 potholes after automatic labelling; 696 training / 300 test samples; YOLOv5m labeller trained on 3,000/3,500/4,000 images plus open data | §4.1; §4.3 | Counts as stated. | Confirmed | Candidate change |
| hardware/device | Commercial smartphones | Acquisition: Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7 (accelerometer, 100 Hz); INAVI QHD5000 dashcam (labelling only). Processing: Linux/Python environment (machine not stated). TFLite model designed for the three phones | §4.1 | Device list and roles as stated. | Confirmed | Candidate change |
| model(s) | CNN-based classifier | RDD-CNN (1D-CNN, Swish, softmax; TFLite, 16-bit quantization); YOLOv5m for automatic labelling; SVM, Random Forest, LSTM baselines | §3.1.2; §3.2; §4.3 | As stated. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Stated as local smartphones (scope); not described as executed or measured on a phone | §3.2; §5 | See on_device. | Ambiguous | Needs researcher decision |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None in the model; sliding-window stride policy only | §3.2 | See adaptive_inference. | Ambiguous | Needs researcher decision |
| resource signals | not a CSV field — see resource_awareness / evidence | None | full text read; no occurrence | No runtime resource signal. | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Accuracy, confusion matrices, discarded-data ratio, processing time per minute of data, model size | §4.2; §4.3 | As stated. | Confirmed | Keep current value |
| limitations | (blank) | Threshold segmentation misses mild defects (painted speed bumps, shallow manholes/potholes); accuracy drops when the phone is in unstable places (cup holder, door pocket, clothes pocket); raw data limited to daytime, good weather, front dashcam | §4.2; §4.3 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Two vehicles (YF Sonata, Kia All New Sportage) on public roads around Cheongju, South Korea | §4.1 | As stated. | Confirmed | Keep current value |

---

## P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

- **DOI:** [10.1155/2022/9221211](https://doi.org/10.1155/2022/9221211) · **Year:** 2022 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (Wiley/Hindawi Advances in Civil Engineering), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** none obtained. Open access (CC BY; listed PDF https://downloads.hindawi.com/journals/ace/2022/9221211.pdf), but neither Hindawi nor Wiley could be fetched from this environment.
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** on_device / edge_device: confirm inference runs on the OAK-D (vs the Raspberry Pi host) and the measurement conditions of 31.76 FPS; latency type: throughput/FPS; check whether per-frame latency is also reported; energy_evaluation / thermal_evaluation Unknown; Provenance note: assigned G1, retrieved by a G4 query

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | No | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | Tiny-YOLOv4 31.76 FPS on OAK-D | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | Edge AI / Embedded vision / Real-time pothole detection on an edge AI device | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Pothole image dataset (diverse road and illumination conditions) plus real-time vehicle video | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | OAK-D AI kit on Raspberry Pi | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetV2 | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

- **DOI:** [10.1016/j.inffus.2024.102782](https://doi.org/10.1016/j.inffus.2024.102782) · **Year:** 2025 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (Elsevier Information Fusion) listed as open access CC BY-NC by OpenAlex, but ScienceDirect returned a bot check, so access was not confirmed. Alternative: arXiv 2407.11771 (author preprint; same title and authors; PDF responded). May differ from the version of record.
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 2407.11771v2 (25 Oct 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2407.11771v2 (version of record: Information Fusion 2025, DOI 10.1016/j.inffus.2024.102782)
- **Version:** Author preprint (arXiv v2)
- **Version type:** preprint
- **May differ from version of record:** Possibly. The Information Fusion version of record was not accessible (ScienceDirect blocked) and was not compared.
- **Parts read:** Full preprint text read (pp. 1-26 plus references). Page numbers are the preprint's own.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** smartphone Unknown: identify the "mobile devices" used for deployment; on_device Yes rests on deployment wording (audit): confirm inference runs on the device; cloud Unknown: check where the vision-language-model explanation step runs; efficiency_metrics blank: abstract reports model-size reduction without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §5.5.1-5.5.2, pp. 13-14; Fig. 7, p. 15 | The mobile model is converted for "smartphone devices"; an app is built for Android and iOS; field engineers capture images with the device camera; the iOS interface is designed for an iPhone 11 Pro. No on-phone measurement is reported. | Confirmed | Candidate change |
| edge_device | Yes | Yes | §5.5, pp. 13-14 | Quantized and pruned model deployed in the mobile app. | Confirmed | Keep current value |
| on_device | Yes | Yes | §5.5.2, p. 14; §5.6 | The mobile model performs semantic segmentation on the uploaded image inside the app. | Confirmed | Keep current value |
| cloud | Unknown | Unknown | §4 (module 6); §5.6, p. 14; Fig. 4 | Textual explanations are generated by calling the GPT-4 Vision API, and Fig. 4 places the domain-expert web app in a "Cloud Environment". The segmentation (the inspection inference) stays on the device. Whether remote explanation generation counts as "inference or decision processing" under README §7.3 is open. | Ambiguous | Needs researcher decision |
| adaptive_inference | Unknown | No | §5.5 | Static quantized and pruned model. | Confirmed | Candidate change |
| resource_awareness | Unknown | No | §5.5.1, pp. 13-14 | Dynamic int8 quantization and 10% structured channel pruning are design-time lightweighting with no device budget. | Confirmed | Candidate change |
| energy_evaluation | Unknown | No | full text read; no occurrence | No energy or power result ("Energy-Based Pointing Game" is an XAI metric). | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §6.1; §7.1 | Aerial images (TTPLA) and substation images from handheld, AGV-mounted and fixed cameras, each segmented on its own. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | "Confidence" refers to user trust; no uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | full text read; no occurrence | No action triggered by a confidence score. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §5.1 | Supervised semantic segmentation trained with Dice loss. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Unknown | Table 4 caption; §8.3, p. 25 | No inference timing is reported. The Table 4 caption mentions running time in seconds, but the table has no time column in the text read. §8.3 says explanation generation on edge devices "may introduce latency" (limitation). Leaning No. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | TTPLA validation mIoU (Table 3, p. 17), base/enhanced/mobile: MobileNetV2 77.18/77.82/75.48%; ResNet50 83.20/83.90/81.53%; ResNet101 84.97/86.35/83.95%. Substation validation mIoU (Table 6, p. 23), ResNet101: 73.45/75.79/72.58% | Table 3, p. 17; Table 6, p. 23 | As stated. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | Model size (Table 3), base vs mobile: MobileNetV2 4.37M / 16.71 MB vs 3.51M / 13.39 MB; ResNet50 26.67M / 101.76 MB vs 21.36M / 81.48 MB; ResNet101 45.66M / 174.21 MB vs 36.57M / 139.52 MB | Table 3, p. 17 | As stated. | Confirmed | Candidate change |
| paper type | system/method | system/method | §4-§9 | Proposes and evaluates the framework. | Confirmed | Keep current value |
| application/domain | Industrial Visual Inspection / Edge AI / Explainable visual quality inspection with semantic segmentation on low-resource edge devices | Visual inspection of power-grid assets (transmission towers, power lines, substation equipment) with explainable segmentation and LVLM text explanations | §6.1; §7.1 | Not manufactured parts. | Confirmed | Candidate change |
| dataset | Unknown | TTPLA (1,242 aerial images, 4 classes); Substation Equipment dataset (1,660 images, 15 categories, 50,705 objects; handheld, AGV-mounted and fixed cameras) | §6.1, p. 15; §7.1 | As stated. | Confirmed | Candidate change |
| hardware/device | Low-resource edge / mobile devices (models not stated in abstract) | Inference: smartphones through an Android/iOS app (iOS UI designed for iPhone 11 Pro). Explanations: GPT-4 Vision API. Training hardware not stated | §5.5.2; §5.6; Fig. 7 | Roles as stated. | Confirmed | Candidate change |
| model(s) | Semantic segmentation model + XAI + Large Vision Language Model explanations | DeepLabv3+ (MobileNetV2, ResNet50, ResNet101 backbones); 10 XAI methods (RISE selected); GPT-4 Vision; PyTorch dynamic quantization, 10% structured pruning, TorchScript mobile optimisation | §4; §5 | As stated. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Segmentation on the phone; explanation text through a remote API | §5.5.2; §5.6 | See on_device / cloud. | Ambiguous | Needs researcher decision |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None at runtime (XAI-guided annotation augmentation is a training step) | §4; §6.4 | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | mIoU and per-class IoU; XAI plausibility (EBPG, IoU, BBox) and faithfulness (deletion, insertion); model size | §5.4; Tables 3-4 | As stated. | Confirmed | Keep current value |
| limitations | (blank) | Annotation augmentation needs expert manual effort; explanation generation on edge devices may add latency and overhead; generalisation to other domains untested | §8.3, p. 25 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Mobile app for field engineers (UI demonstrated); evaluation on public datasets | §5.5.2; §6 | No field study timing. | Confirmed | Keep current value |

---

## P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

- **DOI:** [10.1038/s41467-022-31985-y](https://doi.org/10.1038/s41467-022-31985-y) · **Year:** 2022 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (Nature Communications), open access CC BY; PDF responded. Alternative: PubMed Central PMC9378646; Cambridge Apollo repository.
- **Verification status (Step 9.2):** Fully verified
- **Source used:** PubMed Central full text of the published article (PMC9378646), retrieved through the PubMed full-text service
- **URL / identifier:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9378646/ (DOI 10.1038/s41467-022-31985-y)
- **Version:** Publisher version of record as deposited in PMC (Nature Communications 13:4654, 2022; CC BY)
- **Version type:** publisher version
- **May differ from version of record:** No (version of record). The PMC text extraction omits table bodies, figure images and figure numbers; Table 1 baseline values and figure content were not seen. Evidence is cited by section heading.
- **Parts read:** All running text read (Introduction, Results, Discussion, Methods). Tables, figures and supplementary information not examined.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** edge_device / on_device Unknown: identify the hardware running real-time detection and the control loop; latency_evaluation Unknown: real-time detection/correction claimed without values; confidence_gating Unknown: check whether prediction confidence triggers corrections; multi_view Unknown: camera configuration (number of cameras/poses)

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Methods - CAXTON system | Logitech C270 USB webcams on Raspberry Pi 4 gateways; a Raspberry Pi Camera v1 on the direct-ink-writing printer. No phone. | Confirmed | Candidate change |
| edge_device | Unknown | No | Online correction and parameter discovery pipeline; Computing and software requirements | Images are sent to a local server for inference. The final models were trained on a workstation with two Quadro RTX 5000 GPUs, and "this setup was also used for the online correction". The Raspberry Pi only relays G-code commands and acknowledgements. | Confirmed | Candidate change |
| on_device | Unknown | No | Same as edge_device | Inference runs on the local server, not on the capture device. | Confirmed | Candidate change |
| cloud | Unknown | No | Online correction pipeline; Computing and software requirements | Local server; an HPC cluster was used only for prototyping/training. No remote cloud processing. | Confirmed | Candidate change |
| adaptive_inference | Unknown | No | Online correction and parameter discovery pipeline | Fixed network. The feedback loop adjusts printing parameters, which README §7.3 treats as process adaptation, not inference adaptation. | Confirmed | Candidate change |
| resource_awareness | Unknown | No | full text read; no occurrence | No resource-driven decision. The crop size is tuned for accuracy versus response time at setup, not at runtime. | Confirmed | Candidate change |
| energy_evaluation | Unknown | No | full text read; no occurrence | No energy or power result. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | Hotend temperature is a corrected printing parameter, not a device thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | Methods - CAXTON system; Discussion | One nozzle-facing camera per printer. Different camera positions occur only across different setups (generalisation tests), not as joint views of one object. Adding a global camera is future work. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | Unknown | Online correction and parameter discovery pipeline | Predictions per parameter are stored in lists of length L; a correction is made only if one class reaches the mode-threshold share of the list, and that share scales the update. A vote frequency over repeated predictions, not a model confidence score. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | Results - Dataset generation; Model architecture | Supervised three-class labels (low/good/high) per parameter, derived automatically from known printer settings. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Unknown | Online correction pipeline; Methods; Discussion | Images are captured at 2.5 Hz and an order-of-magnitude faster correction is claimed, but no inference timing on stated hardware appears in the running text. Figures and supplementary material were not available. | Ambiguous | Insufficient evidence |
| accuracy_metrics | (blank) | Test accuracy 84.3% overall; per parameter: flow rate 87.1%, lateral speed 86.4%, Z offset 85.5%, hotend temperature 78.3%; flow-rate accuracy 77.5% single-head vs 82.1% multi-head (ResNet18, 50 epochs) | Results - Model architecture, training and performance; Methods - Training procedure | Values as stated in the running text. Table 1 baselines not visible in the extraction. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | (blank) | full text read; no occurrence | No efficiency value in the running text. | Confirmed | Keep current value |
| paper type | system/method | system/method | full text | Proposes and evaluates the CAXTON network and multi-head detector/corrector. | Confirmed | Keep current value |
| application/domain | 3D-Print Inspection / Real-time error detection and correction in material extrusion 3D printing | Error detection and closed-loop correction in material-extrusion 3D printing from nozzle-camera images | Introduction (last paragraph) | As stated. | Confirmed | Keep current value |
| dataset | 1.2 million images from 192 parts labelled with printing parameters | CAXTON: 1,272,273 images from 192 prints on eight Creality CR-20 Pro printers (PLA); 1,166,552 after removing failed prints; 946,283 after cleaning (74.4%); 81 class combinations; 0.7/0.2/0.1 split | Results - Dataset generation, filtering and augmentation; Methods - Training procedure | Refines the current "1.2 million images" value. | Confirmed | Candidate change |
| hardware/device | Unknown | Inference and training: workstation with 2x NVIDIA Quadro RTX 5000, i9-9900K, 64 GB RAM. Acquisition: Logitech C270 webcam (1280x720, 2.5 Hz) per printer. Gateway: Raspberry Pi 4 Model B with OctoPrint. Other setups: Raspberry Pi Camera v1 (DIW printer), Lulzbot Taz 6 | Methods - CAXTON system; Computing and software requirements | Roles as stated. | Confirmed | Candidate change |
| model(s) | Multi-head neural network with control loop | Multi-head residual attention network (Attention-56-based shared backbone, four heads x three classes) | Results - Model architecture | As stated. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Local server (workstation) | Online correction pipeline; Computing requirements | See edge_device. | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None in inference; proportional printer-parameter updates via mode thresholding | Online correction pipeline | Process control, not inference adaptation. | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Classification accuracy per parameter; qualitative correction demonstrations | Results | As stated. | Confirmed | Keep current value |
| limitations | (blank) | Weakness on small Z-offset changes and dataset bias; correction oscillations possible; mechanical/electrical failures and large errors (cracking, warping, detachment) not solved; local view only | Discussion | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Lab printers, including unseen Lulzbot Taz 6 and a modified Ender 3 Pro for direct ink writing | Results; Methods | As stated. | Confirmed | Keep current value |

---

## P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

- **DOI:** [10.3390/pr8111464](https://doi.org/10.3390/pr8111464) · **Year:** 2020 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (MDPI Processes), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Verification status (Step 9.2):** Fully verified
- **Source used:** MDPI publisher PDF, served from MDPI's content host
- **URL / identifier:** https://mdpi-res.com/d_attachment/processes/processes-08-01464/article_deploy/processes-08-01464.pdf (DOI 10.3390/pr8111464)
- **Version:** Publisher version of record (Processes 2020, 8, 1464; CC BY; pages 1-15 printed)
- **Version type:** publisher version
- **May differ from version of record:** No (version of record).
- **Parts read:** Pages 1-14 read (all sections; reference list partially).
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** edge_device / on_device Unknown: abstract mentions "microprocessors and a camera" generically; latency_evaluation Unknown: "fast speed" claimed without values; confidence_gating Unknown: check whether detections trigger stop/correction via a confidence threshold

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §3, p. 12 | Raspberry Pi 4 with a connected camera; no phone. | Confirmed | Candidate change |
| edge_device | Unknown | Yes | §3, p. 12 | The model was deployed by running it on a Raspberry Pi 4 "with a connected camera" in front of the print bed. | Confirmed | Candidate change |
| on_device | Unknown | Yes | §3, p. 12 | Inference runs on the Raspberry Pi 4 to which the camera is attached. | Confirmed | Candidate change |
| cloud | Unknown | No | §2.2, p. 8; §3, p. 12 | Training on an NVIDIA Tesla K80; live inference on the Pi. No cloud processing. | Confirmed | Candidate change |
| adaptive_inference | Unknown | No | full text read; no occurrence | Fixed SSD-300 model. | Confirmed | Candidate change |
| resource_awareness | Unknown | No | §2.2, p. 7 | SSD-300 chosen over SSD-512 for its published FPS and low input resolution: a design-time choice, not a resource-driven decision. | Confirmed | Candidate change |
| energy_evaluation | Unknown | No | full text read; no occurrence | No energy or power result. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §3, p. 12; §1.2, p. 3 | A single camera. Multiple camera angles appear only in related work, where the authors note they add complexity. | Confirmed | Candidate change |
| uncertainty | Unknown | No | §2.3, p. 10; §3 | Probability scores are used for precision-recall ranking and for gating; no uncertainty estimation or calibration. | Confirmed | Candidate change |
| confidence_gating | Unknown | Yes | §3, pp. 12-13; §4, p. 13 | A wrapper algorithm checks each frame: if a predicted defect's probability score is "greater than a predefined value", the user is notified whether to stop the print (human referral). | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §2.1-2.2, p. 7 | Supervised SSD trained on 500 manually annotated stringing images. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Yes | §3, p. 12; §2.2, p. 7 | latency type: throughput/FPS. The setup ran at 14 FPS on live video, and the model ran at the same FPS on the Raspberry Pi 4. The 59 FPS in §4 is the published SSD-300 benchmark (§2.2), not the authors' measurement. | Confirmed | Candidate change |
| accuracy_metrics | (blank) | Test: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training data: precision 0.75, recall 0.92 (F1 0.82) | §3, pp. 11-12 | As stated. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | 14 FPS on live video; same FPS on Raspberry Pi 4 | §3, p. 12 | As stated. | Confirmed | Candidate change |
| paper type | system/method | system/method | full text | Develops and deploys a stringing detector. | Confirmed | Keep current value |
| application/domain | 3D-Print Inspection / Real-time stringing defect detection during FFF printing from camera video | Real-time stringing detection in FFF 3D printing with operator notification | Abstract; §3 | As stated. | Confirmed | Keep current value |
| dataset | Images showing stringing defects | 500 images of a stringing test object (Prusa i3 MK3S), augmented x5 to 2,500; PASCAL VOC annotations (LabelImg) | §2.1, p. 7 | As stated. | Confirmed | Candidate change |
| hardware/device | Microprocessor plus camera (not specified in abstract) | Inference: Raspberry Pi 4 with connected camera. Training: NVIDIA Tesla K80 (12 GB) | §2.2, p. 8; §3, p. 12 | Roles as stated. | Confirmed | Candidate change |
| model(s) | Deep CNN | SSD-300 with VGG16 base network (TensorFlow Object Detection API) | §2.2, pp. 7-8 | As stated. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Raspberry Pi 4 next to the printer | §3, p. 12 | See on_device. | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Precision, recall, F1, average precision at IoU 0.4-0.6; FPS | §2.3; §3 | As stated. | Confirmed | Keep current value |
| limitations | (blank) | Poor generalisation to external web images; case-specific training data (few shapes, one printer); 500 images considered insufficient | §3, pp. 11-12 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Remote monitoring of long prints on one printer, shapes similar to the training data | §3, p. 13 | As stated. | Confirmed | Keep current value |

---

## P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

- **DOI:** [10.1016/j.promfg.2018.07.111](https://doi.org/10.1016/j.promfg.2018.07.111) · **Year:** 2018 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Inaccessible (from this environment). Publisher (Elsevier Procedia Manufacturing) listed as gold open access CC BY-NC-ND by OpenAlex and Semantic Scholar; ScienceDirect bot check blocked confirmation. Likely readable in a normal browser. Alternative: None found (arXiv exact-title search: no match).
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** none obtained. Gold open access per Semantic Scholar (https://www.sciencedirect.com/science/article/pii/S2351978918307820/pdf, CC BY-NC-ND), but ScienceDirect could not be fetched; bot checks were not bypassed.
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** multi_view Unknown: images taken "at several critical stages" — verify whether the camera pose changes (CD-09); Inference hardware and location not stated; latency_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | 3D-Print Inspection / Good/defective classification of semi-finished 3D printed parts | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | ABS and PLA printed parts imaged at critical print stages | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Camera integrated with printer | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | Support vector machine | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

- **DOI:** [10.1007/s00170-024-14452-4](https://doi.org/10.1007/s00170-024-14452-4) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Abstract only. Publisher (Springer IJAMT) subscription; abstract on landing page. Alternative: None found (OpenAlex closed; arXiv exact-title search: no match; Semantic Scholar: no open PDF).
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** none obtained. Subscription article (Springer IJAMT); no legitimate open copy known (Step 9.1).
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** edge_device / on_device Unknown: identify the hardware on which FPS was measured and whether the detection system is deployed on edge hardware; latency type: throughput/FPS (relative +18.1%); check for absolute values; hardware not stated in abstract

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | mAP50 97.5% | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8 | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | 3D-Print Inspection / Real-time detection of five common FFF printing defects | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Deliberately designed defect dataset (five defect types) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | Improved YOLOv8 with lightweight group-convolution detection head | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P019 — Real-time defect detection in 3D printing using machine learning

- **DOI:** [10.1016/j.matpr.2020.10.482](https://doi.org/10.1016/j.matpr.2020.10.482) · **Year:** 2021 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Abstract only. Publisher (Elsevier Materials Today: Proceedings) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** none obtained. Subscription article (Elsevier Materials Today: Proceedings); no legitimate open copy known (Step 9.1).
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** Inference hardware and location not stated (printer-integrated camera only); latency_evaluation Unknown: "real-time" claimed without values; anomaly_detection Unknown: confirm supervised vs normal-only training

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | 3D-Print Inspection / Real-time detection of infill defects in 3D printing | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Camera integrated with 3D printer | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | CNN image classifier | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

- **DOI:** [10.3390/asi4020034](https://doi.org/10.3390/asi4020034) · **Year:** 2021 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Full text available. Publisher (MDPI Applied System Innovation), open access CC BY; full-text HTML confirmed in browser. Alternative: —.
- **Verification status (Step 9.2):** Fully verified
- **Source used:** MDPI publisher PDF, served from MDPI's content host
- **URL / identifier:** https://mdpi-res.com/d_attachment/asi/asi-04-00034/article_deploy/asi-04-00034.pdf (DOI 10.3390/asi4020034)
- **Version:** Publisher version of record (Appl. Syst. Innov. 2021, 4, 34; CC BY; pages 1-20 printed)
- **Version type:** publisher version
- **May differ from version of record:** No (version of record).
- **Parts read:** Pages 1-20 read.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** anomaly_detection Unknown: abstract says "anomaly detection" but describes supervised classifiers (CD-14); Hardware / inference location not stated; "low computing costs" and real-time suitability claimed without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §3, p. 5; §4.1, p. 13 | 8 MP Raspberry Pi camera; phones appear only in the literature review (p. 3). | Confirmed | Candidate change |
| edge_device | Unknown | Unknown | §3, p. 5; §4.1, p. 13; §5.4, p. 17 | A Raspberry Pi 4B "is used for the processing" with a 7-inch display, but "all the programming, training, and testing are done in Matlab". Where the real-time classification runs is not stated. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §3, p. 5; §4.1, p. 13 | Same ambiguity as edge_device. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | full text read; no occurrence | No cloud processing described. | Confirmed | Candidate change |
| adaptive_inference | Unknown | No | full text read; no occurrence | Fixed feature extractor plus classifier. | Confirmed | Candidate change |
| resource_awareness | Unknown | No | full text read; no occurrence | No resource-driven decision. | Confirmed | Candidate change |
| energy_evaluation | Unknown | No | full text read; no occurrence | No energy or power result. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | Table 3, p. 14 | Printing temperature is a process parameter, not a device thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §4.2, p. 13; §5.4, p. 17 | One camera mounted beside the nozzle; 4-5 images per layer captured on key press. The text does not say the viewpoints differ, and each image is classified on its own (no joint use). | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | §3.3, pp. 9-10 | The ensemble assigns Good if more than two of five classifiers vote Good. No downstream action is triggered by a confidence score. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §3.4, p. 10 | Despite the "anomaly detection" wording, layers are labelled good/bad manually by eye and classified with supervised models (README §7.3, CD-14). | Confirmed | Candidate change |
| latency_evaluation | Unknown | Unknown | §5.4, p. 17; §6, p. 18 | AlexNet+SVM is chosen for "less computational time" with no timing value. README Decision 3 keeps qualitative claims Unknown, while §7.3 says No once the full text is read and no timing is reported. Which rule applies after full-text reading is a researcher decision. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | Feature+classifier (Table 5): AlexNet+SVM 99.70%, EfficientNet-B0+SVM 99.70%, EfficientNet-B0+KNN 99.70%, AlexNet+KNN 99.40%, ResNet50+SVM 99.40%; Naive Bayes lowest (85.90-91.10%). Ensemble (Table 6): AlexNet 100%, ResNet18 99.40%, EfficientNet-B0 99.10%, ResNet50 98.80%, GoogLeNet 97.80%. Density-wise (Table 7): ResNet50 100%, AlexNet and EfficientNet-B0 99.22% | Tables 5-7, pp. 15-17 | As stated. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | (blank) | full text read; no occurrence | No timing, size or energy value reported. | Confirmed | Keep current value |
| paper type | system/method | system/method | full text | Comparative study plus a real-time monitoring demonstration. | Confirmed | Keep current value |
| application/domain | 3D-Print Inspection / Layer-wise fault detection in FDM printing | Layer-wise surface fault detection in FDM printing from camera images | §3, p. 5 | As stated. | Confirmed | Keep current value |
| dataset | Unknown | 1,700 layer images (good/bad, labelled by eye) of a 25 x 25 x 5 mm PLA cube on a Dreamer FDM printer; 4-5 images per layer; parameter variants of density, temperature and printing speed | §3.4, p. 10; §4.2, pp. 13-14 | As stated. | Confirmed | Candidate change |
| hardware/device | Unknown | Acquisition: 8 MP Raspberry Pi camera beside the nozzle. Processing: Raspberry Pi 4B with 7-inch display (role in inference unclear). Programming, training and testing in MATLAB (machine not stated) | §3, p. 5; §4.1, p. 13 | Roles as stated. | Confirmed | Candidate change |
| model(s) | Pretrained CNN features + ML classifiers (AlexNet + SVM best) | Pre-trained CNN features (AlexNet, GoogLeNet, ResNet18, ResNet50, EfficientNet-b0) with SVM, KNN, Random Forest, Decision Tree, Naive Bayes; majority-vote ensemble; AlexNet+SVM used for real-time monitoring | §3.2-3.3, pp. 6-10; §5.4, p. 17 | Matches the essence of the current value. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Not stated | §3; §4.1 | See edge_device. | Ambiguous | Needs researcher decision |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | None | full text read; no occurrence | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Accuracy, loss (100 - accuracy), confusion matrices | §5 | As stated. | Confirmed | Keep current value |
| limitations | (blank) | None explicitly stated; future work: real-time condition-monitoring data, explainable fault visualisation, reinforcement learning | §6, p. 18 | Future work only. | Confirmed | Keep current value |
| deployment setting | not a CSV field — see application / notes | Lab FDM printer with mounted Raspberry Pi camera; layer-wise real-time demonstration | §4.1; §5.4 | As stated. | Confirmed | Keep current value |

---

## P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

- **DOI:** [10.1108/rpj-09-2024-0395](https://doi.org/10.1108/rpj-09-2024-0395) · **Year:** 2025 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Abstract only. Publisher (Emerald Rapid Prototyping Journal) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** none obtained. Subscription article (Emerald Rapid Prototyping Journal); no legitimate open copy known (Step 9.1).
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** edge_device / on_device Unknown: Raspberry Pi is the acquisition system; verify whether inference runs on it; latency_evaluation Unknown; efficiency figures not in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | Warping 98.59% (DenseNet121); stringing 99.38% (MobileNetV2); cracking 99.32% (XceptionNet); multi-class 98.90% (MobileNetV2) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | 3D-Print Inspection / Warping, stringing and cracking detection in 3D-printed PLA/ABS parts | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Defect images from Taguchi L9 design (extruder temp, bed temp, print speed) on a Delta printer | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Raspberry Pi-based data acquisition | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | DenseNet121, MobileNetV2, ResNet50, VGG16, XceptionNet (transfer learning) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

- **DOI:** [10.1016/j.mfglet.2019.09.005](https://doi.org/10.1016/j.mfglet.2019.09.005) · **Year:** 2019 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Abstract only. Publisher (Elsevier Manufacturing Letters) subscription. Alternative: None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF).
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** none obtained. Subscription article (Elsevier Manufacturing Letters); no legitimate open copy known (Step 9.1).
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** Inference hardware and location not stated; latency_evaluation Unknown: "faster than the speed of a human's response" is qualitative; confidence_gating Unknown: check whether correction is triggered by prediction confidence

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | 3D-Print Inspection / Real-time monitoring and autonomous correction of FDM extrusion errors | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | Deep learning model with feedback loop | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

- **DOI:** [10.1145/3241539.3241559](https://doi.org/10.1145/3241539.3241559) · **Year:** 2018 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (ACM MobiCom) listed as open access by OpenAlex; ACM returned a bot check, not confirmed. Alternative: arXiv 1810.10090 (same title; PDF responded). May differ from the version of record.
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 1810.10090v1 (23 Oct 2018), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/1810.10090v1 (version of record: MobiCom 2018, DOI 10.1145/3241539.3241559)
- **Version:** Author preprint carrying the MobiCom '18 ACM permission block
- **Version type:** preprint
- **May differ from version of record:** Possibly. The ACM version of record was not accessible and was not compared.
- **Parts read:** Full preprint text read.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** smartphone Unknown: identify the evaluation platforms (abstract lists smartphones only as examples); Confirm efficiency_metrics values and baselines (up to 2.0x frame rate, 1.7x energy); thermal_evaluation / confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §4.3.1 | Implemented on three smartphones (Samsung Galaxy S8, Galaxy S7, LG Nexus 5; Android 7.0); results reported from the Galaxy S8. | Confirmed | Candidate change |
| edge_device | Yes | Yes | §4.3.1 | Runs on the smartphones. | Confirmed | Keep current value |
| on_device | Yes | Yes | §4.3.1; Fig. 8 | On-device inference and model switching measured on the Galaxy S8. | Confirmed | Keep current value |
| cloud | Unknown | No | §4.3.1; §6 | The authors state their on-device framework "does not rely on cloud connectivity"; no cloud processing in the evaluation. | Confirmed | Candidate change |
| adaptive_inference | Yes | Yes | §2-§3; §4.3 | Runtime selection among nested descendant models of a multi-capacity model. | Confirmed | Keep current value |
| resource_awareness | Yes | Yes | §3; §4.3.1 | Resource-aware scheduler allocates runtime resources (benchmark memory budget 400 MB) and picks resource-accuracy trade-offs. | Confirmed | Keep current value |
| energy_evaluation | Yes | Yes | §4.2 (model switching); §4.3.1; §4.3.3; Figs. 8 and 11 | Power measured with a Monsoon power monitor; switching energy and inference energy reported. | Confirmed | Keep current value |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §4.1 | Image classification benchmarks; no multi-view. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | full text read; no occurrence | No confidence-triggered action. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §4.1 | Supervised classification tasks. | Confirmed | Candidate change |
| latency_evaluation | Yes | Yes | §4.3.2; Fig. 10 | latency type: throughput/FPS (frame-rate speedup on the Galaxy S8). | Confirmed | Keep current value |
| accuracy_metrics | Up to +4.2% inference accuracy vs resource-agnostic baseline | Up to +4.2% inference accuracy vs resource-agnostic baseline | §4.3.2 | Supported: 4.1% (MinTotalCost) and 4.2% (MinMaxCost) at equal frame rate; 2.6% / 2.1% at the knee. | Confirmed | Keep current value |
| efficiency_metrics | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | §4.3.2-4.3.3 | Supported: 2.0x / 1.9x frame rate at equal accuracy; 1.7x / 1.5x energy reduction. Model-switching energy reduction per 1,000 switches: 602.1 J (VC) and 4.0 J (VS) (§4.2). | Confirmed | Keep current value |
| paper type | system/method | system/method | full text | - | Confirmed | Keep current value |
| application/domain | Adaptive Inference / Mobile Vision / Resource-aware multi-tenant on-device deep learning for continuous mobile vision | Resource-aware multi-tenant on-device inference for continuous mobile vision (not inspection) | §1; §4.1 | - | Confirmed | Keep current value |
| dataset | Unknown | CIFAR-10, ImageNet-50, ImageNet-100, GTSRB, Adience-Gender, Places-32 | §4.1, Table 2 | Current value is "Unknown". | Confirmed | Candidate change |
| hardware/device | Mobile vision systems (platform not stated in abstract) | Inference: Samsung Galaxy S8 (reported), Galaxy S7, LG Nexus 5 (Android 7.0); power: Monsoon power monitor | §4.3.1 | - | Confirmed | Candidate change |
| model(s) | NestDNN | NestDNN multi-capacity models built from VGG-16 and ResNet-50 | §4.1, Table 2 | Refines the current value. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | On the smartphone | §4.3.1 | - | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | Runtime switching among nested descendant models | §2-§3 | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | Available memory and compute; number of concurrent applications | §3; §4.3.1 | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Accuracy gain, frame-rate speedup, energy, memory, model-switching cost | §4 | - | Confirmed | Keep current value |
| limitations | (blank) | Filter-importance (TRR) pruning costs much more than L1-norm pruning, raising the cost of generating multi-capacity models | §5 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Benchmark emulating application launches and kills (2-6 concurrent apps; 60 s simulations, 100 repeats) | §4.3.1 | - | Confirmed | Keep current value |

---

## P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

- **DOI:** [10.1145/3649329.3657310](https://doi.org/10.1145/3649329.3657310) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (ACM/IEEE DAC 2024) closed per OpenAlex. Alternative: arXiv 2410.10847 (same title and 8 authors; PDF responded). May differ from the version of record.
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 2410.10847v1 (1 Oct 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2410.10847v1 (version of record: DAC 2024, DOI 10.1145/3649329.3657310)
- **Version:** Author preprint carrying the DAC '24 ACM copyright block
- **Version type:** preprint
- **May differ from version of record:** Possibly. The DAC version of record is closed access and was not compared.
- **Parts read:** Full preprint text read (6 pages plus references). The preprint has no printed page numbers; evidence is cited by section, table and figure.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** adaptive_inference recoded Yes→Unknown (Decision 4): confirm whether any model-level adaptation exists beyond CPU/GPU DVFS; latency_evaluation recoded Yes→Unknown (Decision 3): check for measured latency/variation values; smartphone: confirm Mi 11 Lite variant (4G/5G) used; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | §4.4; Table 2 caption | The text names the "Mi 11 Lite" with a Snapdragon 780G; the Table 2 caption names the "Mi 11 Lite 5G". The Step 8.3 external identification stands. | Confirmed | Keep current value |
| edge_device | Yes | Yes | §4.4; §5 | Jetson Orin Nano and Mi 11 Lite 5G. | Confirmed | Keep current value |
| on_device | Yes | Yes | §5.1.2; §5.2.1 | The two-stage detectors are "on-device" and run 3,000 iterations on the device. Note: the Lotus agent runs on a separate desktop (see cloud). | Confirmed | Keep current value |
| cloud | Unknown | No | §4.4 | The DRL agent runs on a desktop with an RTX 2080Ti and controls the device's frequencies over a socket. This is off-device control, but not a cloud/datacenter server. | Confirmed | Candidate change |
| adaptive_inference | Unknown | No | §4.1-4.4 | Lotus only scales CPU and GPU frequencies, twice per frame. The detector computation is unchanged; the varying proposal count is a property of the unmodified detectors; the two-width execution belongs to the agent's Q-network, not the detector. DVFS with unchanged model computation is No (Decision 4, README §7.4 #2). Requires researcher confirmation because of the Step 8.3 recode. | Confirmed | Candidate change |
| resource_awareness | Yes | Yes | §4.3.2 | Agent state includes CPU/GPU temperature, frequency level, remaining time to the latency constraint and the number of proposals. | Confirmed | Keep current value |
| energy_evaluation | Unknown | No | full text read; no occurrence | Power appears only as motivation; no energy or power result. | Confirmed | Candidate change |
| thermal_evaluation | Yes | Yes | §4.1; §5.2; Figs. 4-7 | Device temperatures measured and compared with baselines; throttling threshold in the reward. | Confirmed | Keep current value |
| multi_view | Unknown | No | §5.1.2 | KITTI and VisDrone2019 detection; no multi-view inspection. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | full text read; no occurrence | No confidence-triggered action. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §5.1.2 | Object-detection benchmarks. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Yes | Tables 1-2; §5.2.1 | latency type: inference latency (mean and standard deviation per image on Jetson Orin Nano and Mi 11 Lite 5G). | Confirmed | Candidate change |
| accuracy_metrics | (blank) | (blank) | Fig. 1; §5 | No detection accuracy is reported for Lotus; the Fig. 1 mAP values are motivation for the baseline models. | Confirmed | Keep current value |
| efficiency_metrics | (blank) | Jetson Orin Nano, MaskRCNN on VisDrone2019 (Table 1): mean latency 768.4 / 584.3 / 531.4 ms and SD 260.4 / 114.2 / 70.7 ms (default / zTT / Lotus), i.e. latency -30.8% vs default and -9.1% vs zTT; SD -72.8% / -38.1%; constraint-satisfaction rate 39.0% / 50.1% / 74.9%. Mi 11 Lite 5G (Table 2): MaskRCNN on KITTI SD 781.8 / 610.5 / 552.3 ms (-29.4% / -9.5%); FasterRCNN on VisDrone2019 satisfaction 92.5%. Lotus overhead 8.52 ms per inference (Q-network 0.42 ms on the desktop GPU; socket 1.92 ms per message) | Tables 1-2; §4.4.2; §5.2.1 | The "+35.9% / +24.8%" satisfaction gains in §5.2.1 are percentage-point differences (74.9 - 39.0; 74.9 - 50.1). | Confirmed | Candidate change |
| paper type | system/method | system/method | full text | - | Confirmed | Keep current value |
| application/domain | Thermal-aware Edge AI / Thermal and latency-variation management for two-stage detectors | Thermal and latency-variation management for two-stage detectors on edge devices (autonomous-driving and drone datasets; not inspection) | §1; §5.1.2 | - | Confirmed | Keep current value |
| dataset | Unknown | KITTI; VisDrone2019 | §5.1.2 | Current value is "Unknown". | Confirmed | Candidate change |
| hardware/device | NVIDIA Jetson Orin Nano; Mi 11 Lite mobile platform | Inference: NVIDIA Jetson Orin Nano (6-core Cortex-A78AE, 1024-core Ampere GPU, 8 GB); Xiaomi Mi 11 Lite 5G (Snapdragon 780G, Kryo 670, Adreno 642). DRL agent: desktop with NVIDIA RTX 2080Ti, connected by socket | §4.4 | - | Confirmed | Candidate change |
| model(s) | LOTUS (DRL-based joint CPU/GPU frequency scaling) | Faster R-CNN and Mask R-CNN detectors; Lotus DQN agent (4-layer MLP executed at 0.75x and 1x width) | §4.3.4; §4.4.1; §5.1.2 | Refines the current value. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Detector on the device; frequency-control agent on a separate desktop | §4.4 | - | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | DRL-driven joint CPU/GPU DVFS, two decisions per frame (system-level) | §4.2-4.3 | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | CPU/GPU temperature, CPU/GPU frequency level, remaining time to the latency constraint, number of proposals | §4.3.2 | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Mean and standard deviation of latency, latency-constraint satisfaction rate, device temperature | §5; Tables 1-2 | - | Confirmed | Keep current value |
| limitations | (blank) | (blank) - none stated | §6 | - | Confirmed | Keep current value |
| deployment setting | not a CSV field — see application / notes | Lab: 25 °C indoor static environment; warm (25 °C) and cold (0 °C) zones; dataset switching | §5.2 | - | Confirmed | Keep current value |

---

## P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

- **DOI:** [10.1145/3793860](https://doi.org/10.1145/3793860) · **Year:** 2026 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Inaccessible (from this environment). Publisher (ACM TECS) closed; OpenAlex lists a green copy in the Uppsala DiVA repository (urn:nbn:se:uu:diva-587035). Alternative: DiVA record did not respond from this environment (connection failed; browser navigation refused). Needs a manual check.
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** none obtained. Publisher (ACM TECS) closed; the only open copy is a submitted version in the Uppsala DiVA repository (urn:nbn:se:uu:diva-587035, per OpenAlex and Semantic Scholar). The resolver returned an Anubis bot challenge, which was not bypassed.
- **Version:** -
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** latency_evaluation recoded Yes→Unknown (Decision 3): check for measured frame-rate values; smartphone Unknown: identify the evaluation devices; confidence_gating Unknown: check whether multi-exit decisions use prediction confidence or only thermal state; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| edge_device | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| on_device | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| cloud | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptive_inference | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource_awareness | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| energy_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| thermal_evaluation | Yes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| multi_view | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| uncertainty | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| confidence_gating | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| anomaly_detection | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| latency_evaluation | Unknown | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| accuracy_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| efficiency_metrics | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| paper type | system/method | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| application/domain | Thermal-aware Edge AI / Thermal-aware multi-DNN on-device inference for mobile video | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| dataset | Two benchmarks + Virtual YouTuber streaming app | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| hardware/device | Mobile devices with heterogeneous processors | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| model(s) | Phoenix (RL task allocation + multi-exit networks) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| inference location | not a CSV field — see on_device / cloud / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| resource signals | not a CSV field — see resource_awareness / evidence | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| limitations | (blank) | not examined | - | No legitimate full text obtained | - | Insufficient evidence |
| deployment setting | not a CSV field — see application / notes | not examined | - | No legitimate full text obtained | - | Insufficient evidence |

---

## P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

- **DOI:** [10.1145/3665868](https://doi.org/10.1145/3665868) · **Year:** 2024 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (ACM TECS) listed as open access CC BY by OpenAlex; ACM returned a bot check, not confirmed. Alternative: arXiv 2409.01089 (same title; PDF responded). May differ from the version of record.
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv copy 2409.01089v1 (2 Sep 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2409.01089v1 (version of record: ACM TECS 23(4), Article 60, June 2024, DOI 10.1145/3665868)
- **Version:** arXiv copy typeset in the ACM TECS journal layout (pages 60:1-60:31)
- **Version type:** preprint server copy in journal layout
- **May differ from version of record:** Unlikely (journal layout and pagination), but not confirmed against the ACM page, which was not accessible.
- **Parts read:** Full text read. Page numbers 60:xx are given only where the page break was clear in the extracted text.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** smartphone Unknown: identify the evaluation devices; latency_evaluation Unknown: check for measured latency/SLO results; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §6.3, p. 60:19 | Evaluated on three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71. | Confirmed | Candidate change |
| edge_device | Yes | Yes | §6.3 | The smartphones above. | Confirmed | Keep current value |
| on_device | Yes | Yes | §6.3-§7 | On-device execution with TFLite on CPU/GPU/NPU (DSP on A71). | Confirmed | Keep current value |
| cloud | Unknown | No | Fig. 2, p. 60:15 | A server is used only for offline model conversion and design generation; inference and the runtime manager run on the device. | Confirmed | Candidate change |
| adaptive_inference | Yes | Yes | §4.3; §7.2 | The runtime manager switches model, processor or both at runtime from a precomputed design set. | Confirmed | Keep current value |
| resource_awareness | Yes | Yes | §4.3; §7.2 | Switching is triggered by processor overload and memory pressure under user-defined SLOs. | Confirmed | Keep current value |
| energy_evaluation | Unknown | Unknown | §4.1; §6.4, pp. 60:19-60:20; §7 | Energy is a listed objective and is profiled on the device (100 runs per configuration), but no energy value is reported in the results. Leaning No. | Ambiguous | Needs researcher decision |
| thermal_evaluation | Unknown | No | §2.1.2; §4.3; §6.4 | Overheating is discussed as a cause of slowdowns, and 2-minute idle periods keep device temperature consistent during profiling, but temperature is not measured or reported. | Confirmed | Candidate change |
| multi_view | Unknown | No | full text read; no occurrence | No multi-view. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | full text read; no occurrence | No confidence-triggered action. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §6.2 | Supervised tasks. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Yes | §7; Figs. 7-8 | latency type: inference latency (average and standard deviation in ms per design) and, separately, throughput/FPS (images per second). | Confirmed | Candidate change |
| accuracy_metrics | (blank) | UC1 initial design on S20 (EfficientNet Lite0 FFX8, CPU, 4 threads, XNNPACK): 75.11%; UC1 vs transferred baselines: +0.156 average accuracy; UC3 memory-efficient switch: 8.5% accuracy decrease | §7.1.2; §7.2.1; §7.2.2 | As stated. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | vs transferred baselines: UC1 +32.7% throughput; UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory 16 MB; UC3 switch saved 92 MB RAM; storage vs OODIn e.g. UC1 on A71 13.83 MB vs 276.36 MB (Table 10). Optimality (a composite metric, not pure efficiency): UC3 1.47x average (up to 3.24x) over the multi-DNN-unaware baseline and 1.87x (up to 4.06x) over transferred baselines | §7.1.2-7.1.3; §7.2; Tables 9-10, p. 60:25 | The 4.06x figure is an optimality gain over transferred baselines, not a throughput value. | Confirmed | Candidate change |
| paper type | system/method | system/method | full text | - | Confirmed | Keep current value |
| application/domain | Adaptive Inference / Mobile / Constraint-aware runtime adaptation for single- and multi-DNN workloads on heterogeneous mobile devices | Constraint-aware runtime adaptation of single- and multi-DNN workloads on smartphones (not inspection) | §1; §6.2 | - | Confirmed | Keep current value |
| dataset | Text classification, scene recognition, face analysis tasks | Use cases covering image classification (ImageNet ILSVRC 2012 evaluation), scene recognition, face analysis (gender, age, ethnicity), text classification and audio (YAMNet) | §6.2 | Current value omits image classification and audio. | Confirmed | Candidate change |
| hardware/device | Heterogeneous mobile devices | Inference: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71 (CPU, GPU, NPU; DSP on A71); TFLite | §6.3 | - | Confirmed | Candidate change |
| model(s) | CARIn (multi-objective optimisation + RASS solver) | CARIn (MOO formulation, RASS solver, runtime manager); model suites including EfficientNet Lite variants, MobileViT and YAMNet | §4; §6.2 | Refines the current value. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | On the smartphone | §6.3 | - | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | Model and/or processor switching from a precomputed design set | §4.3 | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | Processor workload (overload) and aggregate memory use | §4.3 | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Optimality, accuracy, latency (mean and SD), throughput, memory, model size, storage, solving time | §4.1; §7 | - | Confirmed | Keep current value |
| limitations | (blank) | Exhaustive on-device profiling is too costly for realistic deployment; generative models not evaluated | §8, p. 60:26 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Lab evaluation on three phones with emulated runtime issues | §6-§7 | - | Confirmed | Keep current value |

---

## P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

- **DOI:** [10.1109/tmc.2025.3594214](https://doi.org/10.1109/tmc.2025.3594214) · **Year:** 2026 · **Relevance class (audit):** A · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (IEEE TMC) listed as open access CC BY by OpenAlex; IEEE Xplore page not confirmed automatically. Alternative: FH JOANNEUM ePUB repository (submitted version, CC BY; PDF responded).
- **Verification status (Step 9.2):** Fully verified
- **Source used:** FH JOANNEUM ePUB institutional repository PDF
- **URL / identifier:** https://epub.fh-joanneum.at/obvfhjoa/content/titleinfo/13393868/full.pdf (DOI 10.1109/TMC.2025.3594214)
- **Version:** PDF in the IEEE Transactions on Mobile Computing final layout (vol. 25, no. 1, Jan 2026, pp. 451-464), bearing "© 2025 The Authors" and a CC BY 4.0 licence line
- **Version type:** publisher layout (repository copy)
- **May differ from version of record:** Unlikely. OpenAlex labels this repository copy "submittedVersion", which conflicts with the publisher layout and pagination; the label conflict is recorded, not resolved.
- **Parts read:** Pages 451-464 read.
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** latency_evaluation recoded Yes→Unknown: only adaptation time is in the abstract; check for inference latency on the four platforms; smartphone Unknown: identify the four "mobile and embedded" platforms; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §VI, p. 461; Fig. 10, p. 462 | Evaluated on two phones (Xiaomi Redmi Note 9 Pro, Google Pixel 6) with the TFLite benchmarking tool on Android. | Confirmed | Candidate change |
| edge_device | Yes | Yes | §VI, p. 461 | Phones and IoT boards (Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2). | Confirmed | Keep current value |
| on_device | Yes | Yes | §VI, p. 461 | On-device inference and submodel switching measured (TFLMicro extended for REDS). | Confirmed | Keep current value |
| cloud | Unknown | No | §IV-A, p. 458; Acknowledgment, p. 463 | Workstations and computing clusters used for training only; no cloud inference. | Confirmed | Candidate change |
| adaptive_inference | Yes | Yes | §II, p. 453; §VI, p. 462 | Nested subnetworks; switching changes the active layer widths at runtime (38 ± 1 µs adaptation). | Confirmed | Keep current value |
| resource_awareness | Yes | Yes | §I, p. 451; §III-D, pp. 455-457 | Subnetworks built under MAC and peak-memory constraints and switched in response to dynamic resource constraints. | Confirmed | Keep current value |
| energy_evaluation | Unknown | Yes | Table VI and text, p. 463 | Inference energy measured with a Power Profiler Kit (PPK2) on a Nordic nRF52840: 20-61 mJ for DS-CNN; switching < 0.01 mJ. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | full text read; no occurrence | No multi-view. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | No | §I, p. 452; Fig. 11, p. 462 | Early-exit methods appear only as related work and as a comparison baseline; REDS triggers no action from a confidence score. | Confirmed | Candidate change |
| anomaly_detection | Unknown | No | §IV | Supervised benchmark tasks. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Yes | §VI, pp. 461-463; Fig. 10 | latency type: inference latency (TFLite benchmark on phones; on-device timing on IoT boards, e.g. 2-layer FC network on Arduino Nano 33 BLE Sense: 2,131 ± 27 µs at 25% MACs and 4,548 ± 13 µs at 50% MACs). | Confirmed | Candidate change |
| accuracy_metrics | (blank) | ViT-Base on ImageNet-1K (Table IV, p. 460), REDS full / medium / low subnetworks: 79.88% / 78.42% / 68.21% top-1; MobileNetV1 on VWW: 27% lower peak memory for 0.9% lower accuracy (§IV-B, p. 458; Table III, p. 460) | §IV-B, p. 458; Tables III-IV, p. 460 | Most other accuracies are in figures and were not extracted. | Confirmed | Candidate change |
| efficiency_metrics | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | Adaptation time 38 ± 1 µs (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 ± 27 µs (25% MACs) and 4,548 ± 13 µs (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2); cache-hit rate above 97% with the optimized matrix multiplication (RP2040, Table V) | §V-B, p. 461; §VI, pp. 462-463; Table VI | Extends the current single-value entry. | Confirmed | Candidate change |
| paper type | system/method | system/method | full text | - | Confirmed | Keep current value |
| application/domain | Adaptive Inference / Edge / Deep subnetworks that adapt to dynamic resource constraints on edge devices | Resource-adaptive nested subnetworks for mobile and IoT devices (keyword spotting, visual wake words, image classification; not inspection) | §I; §IV | - | Confirmed | Keep current value |
| dataset | Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K | Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K | Abstract; §IV-A | Matches the current value. | Confirmed | Keep current value |
| hardware/device | Four mobile and embedded platforms incl. Arduino Nano 33 BLE | Inference: Xiaomi Redmi Note 9 Pro, Google Pixel 6, Arduino Nano 33 BLE Sense (nRF52840), Infineon CY8CKIT-062S2. Cache benchmark: Raspberry Pi Pico (RP2040). Energy: PPK2 on nRF52840. Training: workstations with Tesla K80 / A100 GPUs | §IV-A, p. 458; §V-B, p. 461; §VI, pp. 461-463 | - | Confirmed | Candidate change |
| model(s) | REDS | REDS (iterative knapsack, bottom-up / top-down heuristics) applied to DNN, CNN, DS-CNN (S/L), MobileNetV1 (0.25x) and ViT-Base | §III; §IV-A | Refines the current value. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | On device | §VI | - | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | Runtime switching among nested subnetworks by changing layer widths | §II; §VI | - | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | MACs, peak memory, dynamic resource constraints | §III | - | Confirmed | Keep current value |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Accuracy, parameters, MACs, peak memory, inference time, adaptation time, energy, cache-hit rate | §IV-§VI | - | Confirmed | Keep current value |
| limitations | (blank) | Not tested as NAS for large language or multimodal models; cache optimisation for convolutions unexplored; energy as a solver constraint left for future work | §VII, p. 463 | Stated as future directions. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Lab benchmarks on phones and IoT boards | §VI | - | Confirmed | Keep current value |

---

## P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

- **DOI:** [10.1016/j.aei.2020.101101](https://doi.org/10.1016/j.aei.2020.101101) · **Year:** 2020 · **Relevance class (audit):** D · **Priority:** HIGH
- **Accessibility (Step 9.1, dated 2026-10-04):** Alternative legitimate source. Publisher (Elsevier Advanced Engineering Informatics) listed as open access CC BY-NC-ND by OpenAlex; ScienceDirect bot check, not confirmed. Alternative: UTS institutional repository hdl:10453/147577 (hosts the publisher PDF of the article; PDF responded).
- **Verification status (Step 9.2):** Fully verified
- **Source used:** UTS institutional repository (OPUS) copy of the publisher PDF
- **URL / identifier:** https://opus.lib.uts.edu.au/bitstream/10453/147577/2/1-s2.0-S1474034620300707-main.pdf (hdl:10453/147577; DOI 10.1016/j.aei.2020.101101)
- **Version:** Publisher PDF (Advanced Engineering Informatics 45 (2020) 101101; CC BY-NC-ND; pages 1-9 printed)
- **Version type:** publisher version
- **May differ from version of record:** No (publisher PDF).
- **Parts read:** Pages 1-9 read (all sections; reference list partially).
- **Verifier / date:** Claude Code / 2026-10-03
- **Issues to resolve:** **Relevance (audit class D):** verify whether the quality inspection is image/vision-based or uses process data; edge_device and cloud recoded Yes→Unknown: identify the hardware behind "Edge Cloud Computing" and where models run; on_device / latency_evaluation Unknown; Relevance class must not be changed without researcher review

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §4.2, p. 7 | The edge device is an industrial PC; no smartphone role. | Confirmed | Candidate change |
| edge_device | Unknown | Unknown | §2.2, p. 2; §4.2, p. 7 | The GBT model runs on an edge device at the SMT line: an industrial PC with an Intel Celeron N2930. The paper defines an edge device as any computing or networking resource between data sources and the cloud. Whether a low-power industrial PC counts as resource-constrained hardware (README §7.3) or as plant IT is open. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §4.2, p. 7 | The edge PC receives and parses SPI result files (CAMX-XML) over TCP/IP; it is not the capturing device or hardware attached to it. Leaning No, but tied to the industrial-PC question. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | §4.2, p. 7; §5, p. 8 | Training on a company-owned Spark cluster, storage in AWS S3; "trained ... in the cloud and deployed on local edge devices" (§5). Inference runs on the edge PC. Cloud used only for training and storage (does not qualify). | Confirmed | Candidate change |
| adaptive_inference | Unknown | No | §3.3, p. 5; §4.2, pp. 6-7 | Static GBT model. "Dynamic" inspection refers to routing panels around X-ray, not to inference. | Confirmed | Candidate change |
| resource_awareness | Unknown | Unknown | §3.2, p. 4; §3.4, p. 5; §4.1, p. 6 | GBT chosen over SVM because its scoring time was eight times faster, "with future scaling" in mind; takt time sets the real-time constraint. A deployment-time choice informed by timing, without an explicit device budget. | Ambiguous | Needs researcher decision |
| energy_evaluation | Unknown | No | §3.4, p. 5 | Energy constraints are listed as a general deployment challenge; nothing is measured. | Confirmed | Candidate change |
| thermal_evaluation | Unknown | No | full text read; no occurrence | No thermal measurement. | Confirmed | Candidate change |
| multi_view | Unknown | No | §4, Table 2, p. 6 | Inputs are seven numeric SPI features per solder joint, not images. | Confirmed | Candidate change |
| uncertainty | Unknown | No | full text read; no occurrence | No uncertainty estimation. | Confirmed | Candidate change |
| confidence_gating | Unknown | Unknown | §3.3, p. 5; §4.1-4.2, pp. 6-7 | Fields of view predicted defect-free skip X-ray; the model is tuned to be conservative (penalising false negatives). The routing is triggered by the predicted class; no confidence score or threshold is described. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | §3.2, p. 4; §4.1, p. 6 | Supervised classifiers trained on X-ray labels. | Confirmed | Candidate change |
| latency_evaluation | Unknown | Unknown | §4.1, Table 3, pp. 6-7; §4.2, p. 7 | Table 3 gives scoring times per 1,000 rows, but "the description of hardware used is omitted". On the edge PC (Celeron N2930), current test sets are processed in under one minute: an upper bound, not a per-item timing. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | Initial balanced sample, 5-fold CV (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9% / 96.4% / 89.3%; DT 88.2%; NB 83.5%; LR 71.9%. Highly conservative GBT, solder-joint level (Table 4): class recall 98.8% / 86.4%. FOV level (Table 5): average X-ray volume reduced by about 29% | Tables 3-5, p. 7 | Table 3 values are clear. Some Table 4 and Table 5 cell values look inconsistent in the extracted text and should be checked visually before recoding. | Confirmed | Candidate change |
| efficiency_metrics | (blank) | Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets in under 1 min. Edge-cloud link: 2-150 ms latency, 10 MB per 14 s (about 1 Mbit/s per line) | Table 3, p. 7; §4.2, p. 7 | As stated. | Confirmed | Candidate change |
| paper type | system/method | system/method (industrial case study) | §3-§4 | Proposes a framework and evaluates it in a Siemens SMT line. | Confirmed | Keep current value |
| application/domain | Industrial Quality Inspection / Edge-Cloud / Predictive model-based quality inspection in SMT manufacturing | Predictive quality inspection of PCB solder joints in SMT assembly: predicting X-ray results from numeric solder-paste-inspection (SPI) measurements to reduce X-ray inspection volume. The ML model does not process images. | §1, p. 1; §4, pp. 5-6 | SPI is described as a visual inspection station, but the model input is its numeric output. | Confirmed | Needs researcher decision |
| dataset | Real industrial SMT use case | Five production months of SPI and X-ray records for one connector PCB variant (48-board panel), Siemens Amberg: 1,461,037,321 data points, ~0.0008% not OK; seven SPI features (height, shape 2D, shape 3D, surface, volume, offset X, offset Y) with binary X-ray label | §4, Table 2, p. 6 | As stated. | Confirmed | Candidate change |
| hardware/device | Edge Cloud Computing infrastructure | Inference: edge industrial PC with Intel Celeron N2930 at the SMT line. Training: company Spark cluster (up to 24 workstations, 16-core CPUs, 32-64 GB RAM). Storage: AWS S3 | §4.2, p. 7 | Roles as stated. | Confirmed | Candidate change |
| model(s) | Machine learning (models not stated in abstract) | Gradient Boosted Tree (selected); Decision Tree, Naive Bayes, Logistic Regression, SVM compared | §4.1, p. 6 | As stated. | Confirmed | Candidate change |
| inference location | not a CSV field — see on_device / cloud / notes | Edge industrial PC at the manufacturing line | §4.2, p. 7; §5, p. 8 | See edge_device / on_device. | Confirmed | Keep current value |
| adaptation mechanism | not a CSV field — see adaptive_inference / evidence | None | full text read; no occurrence | Static model; routing of panels is a process decision. | Confirmed | Keep current value |
| resource signals | not a CSV field — see resource_awareness / evidence | Takt time and model scoring time (model selection only) | §3.4, p. 5; §4.1, p. 6 | See resource_awareness. | Ambiguous | Needs researcher decision |
| evaluation metrics | not a CSV field — see accuracy_metrics / efficiency_metrics | Accuracy, standard deviation, recall, precision, training and scoring time, class recall, inspection-volume reduction | Tables 3-5, p. 7 | As stated. | Confirmed | Keep current value |
| limitations | (blank) | Deployment limited to one product variant, one manufacturing line and the SPI and X-ray data sources | §4.3, p. 7 | Stated by the authors. | Confirmed | Candidate change |
| deployment setting | not a CSV field — see application / notes | Siemens electronics plant, Amberg (Germany): SMT line with SPI station, edge PC and X-ray routing | §4, pp. 5-7 | As stated. | Confirmed | Keep current value |
