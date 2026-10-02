# Full-Text Verification Template

_Step 9.1, prepared 2026-10-04 by Claude Code; **populated in Step 9.2 (2026-10-04)** with full-text evidence for the 12 accessible papers. The 6 blocked papers keep empty rows. One evidence table per queued paper (see [`fulltext_verification_queue.md`](fulltext_verification_queue.md)). The "Current CSV Value" column is copied from `papers.csv` at commit `9ebbf89`. All other columns are **blank on purpose** and are filled during full-text verification._

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

- **DOI:** [10.1002/stc.2751](https://doi.org/10.1002/stc.2751) · **Year:** 2021 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher full-text HTML, Wiley Online Library (open access) — https://onlinelibrary.wiley.com/doi/full/10.1002/stc.2751 — accessed 2026-10-04
- **Version:** Publisher version of record (Struct. Control Health Monit. 28(7) e2751; HTML). May differ from the published version: No (version of record).
- **Location convention:** HTML has no page numbers; locations are section numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** on_device Unknown: where inference runs (on the phone vs a server) is not stated in the abstract; latency_evaluation Unknown: "real-time" claimed without a reported timing value; hardware: smartphone model not stated; model architecture not stated in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | §4, §6.3, §7 | Android smartphone app; the TFLite model is installed on an Android phone. The phone model is not named. | Confirmed | Keep |
| edge_device | Unknown | Yes | §6.3, §7; README §7.5 | Inference runs on the Android phone (resource-constrained mobile hardware). | Confirmed | Change |
| on_device | Unknown | Yes | §6.3, §7, §8 | Trained model converted to TFLite and run on the phone; real-time detection on the phone camera video stream; conclusion says detection uses only smartphones. | Confirmed | Change |
| cloud | Unknown | No | §4, §6 | Training on a desktop GPU workstation; inference on the phone; no cloud or server processing described. | Confirmed | Change |
| adaptive_inference | Unknown | No | §4.2, §6 | Single fixed SSD MobileNet model; no runtime adaptation. | Confirmed | Change |
| resource_awareness | Unknown | No | §3, §4.2 | Model chosen for its published speed/accuracy trade-off: a design-time lightweight-model choice, not a resource-driven decision (README §7.3). | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No temperature or throttling measurement. | Confirmed | Change |
| multi_view | Unknown | No | §5, §7 | Single images and a single phone-camera video stream. | Confirmed | Change |
| uncertainty | Unknown | No | §6.2, §7 | Prediction percentage displayed as confidence; no uncertainty estimation or calibration. | Confirmed | Change |
| confidence_gating | Unknown | No | §6.2-§7 | Confidence is displayed in the app; no action is triggered by it. | Confirmed | Change |
| anomaly_detection | Unknown | No | §5.3, §6 | Supervised detector trained on four labelled defect classes. | Confirmed | Change |
| latency_evaluation | Unknown | Unknown | §4.2, §7, Fig. 7 | App GUI shows inference time and Fig. 7 screenshots include it, but no values are given in the text. The 56 ms in §4.2 is the pre-trained model's published COCO benchmark, not the authors' measurement. Values may be readable in Fig. 7. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | Per class at IoU 0.6 (Table 1), recall/precision/accuracy: crack 0.4/0.53/0.61; deterioration 0.68/0.68/0.83; mould 0.85/0.66/0.81; stain 0.71/0.85/0.95 | Table 1, §7 | Values from Table 1. The §7 text gives stain precision as 0.95 while Table 1 gives 0.85 (internal inconsistency; table value used). | Confirmed | Change |
| efficiency_metrics | (blank) | (blank) | §7 | No measured efficiency value reported in the text. | Confirmed | Keep |
| paper type | system/method | system/method | §1-§8 | Develops and evaluates a smartphone defect-detection app. | Confirmed | Keep |
| application/domain | Smartphone / Mobile AI / Real-time detection of building defects (cracks, mould, stain, paint deterioration) | Building defect detection (civil condition assessment): cracks, mould, stain, paint deterioration | Abstract, §1 | Civil/building domain, not manufactured parts. | Confirmed | Keep |
| dataset | Unknown | 876 images (700 train / 176 test), 4 classes; mobile-phone and hand-held camera photos, internet images, public 128x128 crack dataset | §5.1, §6.2 | Custom dataset assembled from several sources. | Confirmed | Change |
| hardware/device | Smartphone (model not stated in abstract) | Inference: Android smartphone (model not named); Training: Dell Precision 5820 with NVIDIA Quadro P4000 | §6.2, §6.3, §7 | Roles from the methods section. | Confirmed | Change |
| model(s) | Deep learning model (architecture not stated in abstract) | SSD MobileNet (TensorFlow, converted to TFLite) | §4.2, §6.3 | Pre-trained SSD MobileNet fine-tuned on four classes. | Confirmed | Change |
| inference location | (not a CSV field) | On the smartphone | §6.3, §7 | Local TFLite inference on the phone. | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None | §4-§6 | No runtime adaptation. | Confirmed | Keep |
| resource signals | (not a CSV field) | None used at runtime | §4.2 | Speed/accuracy trade-off considered only when selecting the model. | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Recall, precision, accuracy per class at IoU 0.6 | §3, Table 1 |  | Confirmed | Keep |
| limitations | (blank) | Small training set and low-resolution crack images limit crack detection; larger datasets and higher resolution need more compute | §7, §8 | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Android app on sample images and live camera video; no field study described | §7 |  | Confirmed | Keep |

## P002 — A Road Defect Detection System Using Smartphones

- **DOI:** [10.3390/s24072099](https://doi.org/10.3390/s24072099) · **Year:** 2024 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher full-text HTML, MDPI Sensors (CC BY) — https://www.mdpi.com/1424-8220/24/7/2099 — accessed 2026-10-04
- **Version:** Publisher version of record (Sensors 24(7):2099; HTML). May differ from the published version: No (version of record).
- **Location convention:** HTML has no page numbers; locations are section/table/figure numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** **Modality check:** the publisher page section headings (seen 2026-10-04 while checking access, text not read) include "Vibration Sensor-Based ..." and "1D-CNN". Verify whether the system uses camera images at all; this bears on relevance class A, which is a researcher decision; latency_evaluation recoded Yes→Unknown (Decision 3): check for a measured timing value; on_device Unknown: where the CNN runs (phone vs server); Audit: latency claim was comparative only

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | §3.1.1, §4.1 | An Android app on three phones (Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7) records 3-axis accelerometer data at 100 Hz. The phone is used as a vibration sensor, not as a camera. | Confirmed | Keep |
| edge_device | Unknown | Unknown | §4.3, §5 | Conclusions state classification runs in real time on local smartphones, and models were quantized to reduce load on phones. The text does not describe running or timing the CNN on a named phone. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §4.3, §5 | Same as edge_device: real-time on-phone classification is stated as the scope, but no on-device execution or benchmark is described. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | §5 | A cloud server for a live defect map is future work only. | Confirmed | Change |
| adaptive_inference | Unknown | No | keyword search of full text + methods/results read | Fixed models; the sliding window changes how often tests run, not the model computation. | Confirmed | Change |
| resource_awareness | Unknown | No | §4.3 | Quantization to lighten models for phones is design-time lightweighting, not a resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §3.1, §3.2 | Input modality is a 1-D accelerometer time series, not imaging. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | Unknown | §3.1.2 | In the automatic labelling pipeline, a dashcam sample is kept only if at least 90% of 30 YOLOv5m frame classifications agree. This is a consistency vote used to build the dataset, not a confidence score acting on the deployed classifier. Whether this counts needs a decision. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | §3.2, §4.3 | Supervised classification of speed bumps, manholes and potholes. | Confirmed | Change |
| latency_evaluation | Unknown | Unknown | §4.3 Fig. 9, §5 | Average processing time per minute of test data is reported (about 0.1 s per minute of driving), but the hardware on which it was measured is not stated (README §7.3 requires stated or identifiable hardware). | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | RDD-CNN accuracy reported as exceeding 86.77% (Conclusions); speed bump vs no-defect discrimination 99% (Fig. 7); automatic data collection missed 15.21% of data with 100% label accuracy (Conclusions) | §4.3, §5 | Wording of the 86.77% figure ("exceeding ... compared to other models") is ambiguous; per-model values are in Fig. 8. | Confirmed | Change |
| efficiency_metrics | (blank) | Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving data (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB | §4.1, §4.3, §5 |  | Confirmed | Change |
| paper type | system/method | system/method | §3-§5 |  | Confirmed | Keep |
| application/domain | Smartphone / Mobile AI / Road defect classification (speed bumps, manholes, potholes) | Road defect classification from smartphone accelerometer (vibration) signals; dashcam video used only for automatic labelling. Not image-based inspection | §3.1, §3.2 | Input modality is vibration. Relevance to smartphone visual inspection is a researcher decision. | Confirmed | Needs researcher decision |
| dataset | Automatically collected and labelled smartphone data | Self-collected: 20 h / 300 km driving (training) and 8 h / 120 km (test) in Cheongju; 576 speed bumps, 290 manholes, 271 potholes after preprocessing; 1,137 automatically vs 1,287 manually labelled samples | §4.1, §4.3 |  | Confirmed | Change |
| hardware/device | Commercial smartphones | Acquisition: Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7 accelerometers; INAVI QHD5000 dashcam (labelling only). Processing: Linux/Python environment (device not stated) | §4.1 |  | Confirmed | Change |
| model(s) | CNN-based classifier | RDD-CNN (1D-CNN); YOLOv5m for automatic labelling; SVM, Random Forest, LSTM compared | §3.1.2, §3.2, §4.3 |  | Confirmed | Change |
| inference location | (not a CSV field) | Stated as local smartphones in the conclusions; execution not described | §5 |  | Ambiguous | Needs researcher decision |
| adaptation mechanism | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Accuracy, confusion matrices, processing time, model size | §4.3 |  | Confirmed | Keep |
| limitations | (blank) | Threshold-based segmentation misses mild defects that cause little vibration; accuracy depends on phone placement in the vehicle | §4.2, §4.3 Table 7 | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Two vehicles driving public roads around Cheongju, South Korea | §4.1 |  | Confirmed | Keep |

## P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

- **DOI:** [10.1155/2022/9221211](https://doi.org/10.1155/2022/9221211) · **Year:** 2022 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher full-text HTML, Wiley Online Library / Hindawi (open access) — https://onlinelibrary.wiley.com/doi/full/10.1155/2022/9221211 — accessed 2026-10-04
- **Version:** Publisher version of record (Adv. Civil Eng. 2022, 9221211; HTML). May differ from the published version: No (version of record).
- **Location convention:** HTML has no page numbers; locations are section/table numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** on_device / edge_device: confirm inference runs on the OAK-D (vs the Raspberry Pi host) and the measurement conditions of 31.76 FPS; latency type: throughput/FPS; check whether per-frame latency is also reported; energy_evaluation / thermal_evaluation Unknown; Provenance note: assigned G1, retrieved by a G4 query

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | No | No | §2.2.4, §3.7 | Hardware is an OAK-D kit on a Raspberry Pi; no smartphone role. | Confirmed | Keep |
| edge_device | Yes | Yes | §2.2.4, §3.7 | Models are converted to OpenVINO blobs and run on the OAK-D (Myriad X VPU) with a Raspberry Pi host. | Confirmed | Keep |
| on_device | Yes | Yes | §2.2.4, §3.7 | Inference runs on the OAK-D camera kit attached to the Raspberry Pi host, mounted on the vehicle dashboard. | Confirmed | Keep |
| cloud | Unknown | No | §2, §3 | No cloud processing; training on a local workstation. | Confirmed | Change |
| adaptive_inference | Unknown | No | keyword search of full text + methods/results read | Fixed detectors. | Confirmed | Change |
| resource_awareness | Unknown | No | keyword search of full text + methods/results read | No resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §2.2.4 | OAK-D has stereo cameras, but detection uses the single RGB camera; no multi-view inspection. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | §3.4, §3.7 | Confidence thresholds only filter detections; no downstream action (recapture, referral, fallback) is triggered. | Confirmed | Change |
| anomaly_detection | Unknown | No | §3.2 | Supervised single-class pothole detection. | Confirmed | Change |
| latency_evaluation | Yes | Yes | Table 1, Table 3, §3.7 | latency type: throughput/FPS on OAK-D (Table 3, e.g. Tiny-YOLOv4 31.76 FPS) and inference latency per image (Table 1; hardware not stated, likely the training workstation). | Confirmed | Keep |
| accuracy_metrics | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | Table 1, Table 3 | Matches the current value. Table 1 also gives precision/recall/F1 per model. | Confirmed | Keep |
| efficiency_metrics | Tiny-YOLOv4 31.76 FPS on OAK-D | On OAK-D (Table 3): Tiny-YOLOv4 31.76 FPS, SSD-MobileNetv2 26.65 FPS, YOLOv5 18.25 FPS, YOLOv2 3.20 FPS, YOLOv3 2.39 FPS, YOLOv4 1.98 FPS. Inference time per image (Table 1, hardware not stated): Tiny-YOLOv4 4.86 ms, SSD-MobileNetv2 7 ms, YOLOv5 10 ms, YOLOv2 33.7 ms, YOLOv4 52.51 ms, YOLOv3 70.57 ms, YOLOv1 340 ms | Table 1, Table 3 | Extends the current single-value entry. | Confirmed | Change |
| paper type | system/method | system/method | §1-§4 |  | Confirmed | Keep |
| application/domain | Edge AI / Embedded vision / Real-time pothole detection on an edge AI device | Real-time pothole detection from a vehicle-mounted edge AI camera | §1, §3.7 |  | Confirmed | Keep |
| dataset | Pothole image dataset (diverse road and illumination conditions) plus real-time vehicle video | Public pothole image dataset (PID) stated as 665 images (~8,000 potholes); the train/test split is given as 1,066/264 images (internal inconsistency); real-time video from a moving vehicle | §2.1, §3.3, §3.7 | Inconsistent counts in the paper. | Confirmed | Change |
| hardware/device | OAK-D AI kit on Raspberry Pi | Inference: OAK-D (Myriad X VPU) with Raspberry Pi host; Training: Intel Xeon 3.0 GHz, 64 GB RAM, NVIDIA Titan Xp | §2.2.4, §3.3 |  | Confirmed | Change |
| model(s) | YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetV2 | YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetv2 | §2.2, Table 1 | Matches current value. | Confirmed | Keep |
| inference location | (not a CSV field) | On the OAK-D attached to the Raspberry Pi host | §2.2.4 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Precision, recall, F1, mAP@0.5, inference time per image, real-time detection accuracy and FPS | §3.4, Tables 1 and 3 | The text sets the IoU threshold to 0.3 while tables report mAP@0.5 (internal inconsistency). | Confirmed | Keep |
| limitations | (blank) | YOLOv5 and SSD-MobileNetv2 miss distant potholes; accuracy limitations in real-time deployment; the real-time test covers 10 potholes | §3.6, §3.7, §4 | Partly stated by the authors; test size from Table 3. | Confirmed | Change |
| deployment setting | (not a CSV field) | OAK-D on the dashboard of a vehicle at 65 km/h; three locations and distance ranges | §3.7 |  | Confirmed | Keep |

## P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

- **DOI:** [10.1016/j.inffus.2024.102782](https://doi.org/10.1016/j.inffus.2024.102782) · **Year:** 2025 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 2407.11771v2 (25 Oct 2024) — https://arxiv.org/abs/2407.11771 — accessed 2026-10-04
- **Version:** Author preprint (arXiv v2); published version is Information Fusion 2025 (10.1016/j.inffus.2024.102782). May differ from the published version: Possibly; preprint not compared with the version of record (ScienceDirect bot check).
- **Location convention:** Page numbers are arXiv PDF page numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** smartphone Unknown: identify the "mobile devices" used for deployment; on_device Yes rests on deployment wording (audit): confirm inference runs on the device; cloud Unknown: check where the vision-language-model explanation step runs; efficiency_metrics blank: abstract reports model-size reduction without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §5.5.1, §5.5.2, Fig. 7 (pp. 13-15) | Mobile model optimised for smartphones; app built for Android and iOS; iOS interface designed for an iPhone 11 Pro. | Confirmed | Change |
| edge_device | Yes | Yes | §5.5, §6.5 | Quantized and pruned model deployed on mobile devices. | Confirmed | Keep |
| on_device | Yes | Yes | §5.5.2 (p. 14) | Segmentation is produced by the mobile model inside the app on the device. | Confirmed | Keep |
| cloud | Unknown | Yes | §4 module 6, §5.6, Fig. 4 (pp. 9-14) | Textual explanations are generated by calling the GPT-4 Vision API (a remote large vision-language model). Cloud mode: cloud-assisted (explanation step only); segmentation stays on the device. | Confirmed | Change |
| adaptive_inference | Unknown | No | §5.5 | Static quantized/pruned model; no runtime adaptation. | Confirmed | Change |
| resource_awareness | Unknown | No | §5.5.1 | Quantization and pruning are design-time lightweighting with no explicit device budget or resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §6.1, §7.1 | Single images from aerial and handheld/AGV cameras; no joint use of multiple views. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation ("confidence" appears only as user trust). | Confirmed | Change |
| confidence_gating | Unknown | No | keyword search of full text + methods/results read | No action triggered by a confidence score. | Confirmed | Change |
| anomaly_detection | Unknown | No | §5 | Supervised semantic segmentation. | Confirmed | Change |
| latency_evaluation | Unknown | Unknown | Table 4, §8.3 | No segmentation inference timing reported. Table 4 gives XAI-method running times in seconds without stated hardware; the authors list explanation latency on edge devices as a limitation. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | TTPLA mIoU (Table 3): DLv3P-MobileNetv2 mobile 75.48%; DLv3P-ResNet101 enhanced 86.35%, mobile 83.95% | Table 3 (p. 17), §6.5 |  | Confirmed | Change |
| efficiency_metrics | (blank) | Model size (Table 3): DLv3P-MobileNetv2 mobile 3.51M parameters / 13.39 MB; DLv3P-ResNet101 mobile 36.57M / 139.52 MB vs base 45.66M / 174.21 MB | Table 3 (p. 17) |  | Confirmed | Change |
| paper type | system/method | system/method | §4-§9 |  | Confirmed | Keep |
| application/domain | Industrial Visual Inspection / Edge AI / Explainable visual quality inspection with semantic segmentation on low-resource edge devices | Visual inspection of power-grid assets (transmission towers, power lines, substation equipment) with explainable segmentation; not manufactured parts | §6.1, §7.1 |  | Confirmed | Change |
| dataset | Unknown | TTPLA (1,242 aerial images, 4 classes); Substation Equipment dataset (1,660 images, 15 classes) | §6.1, §7.1 |  | Confirmed | Change |
| hardware/device | Low-resource edge / mobile devices (models not stated in abstract) | Inference: smartphones via Android/iOS app (iOS UI designed for iPhone 11 Pro); Explanation: GPT-4 Vision API; Training hardware not stated | §5.5.2, §5.6, Fig. 7 |  | Confirmed | Change |
| model(s) | Semantic segmentation model + XAI + Large Vision Language Model explanations | DeepLabv3+ (MobileNetV2, ResNet50, ResNet101 backbones); 10 XAI methods (RISE selected); GPT-4 Vision for text | §4, §5 |  | Confirmed | Change |
| inference location | (not a CSV field) | Segmentation on device; explanation text via remote API | §5.5.2, §5.6 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None at runtime (XAI-guided data augmentation is a training-time step) | §4 |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | mIoU / per-class IoU; XAI plausibility (EBPG, IoU, Bbox) and faithfulness (deletion, insertion); model size | §5, Tables 3-4 |  | Confirmed | Keep |
| limitations | (blank) | Annotation augmentation needs expert manual effort; generating textual explanations on edge devices may add latency and overhead; generalisation to other domains untested | §8.3 (p. 25) | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Mobile app for field engineers; evaluated on public datasets; no field study timing | §5.5.2, §6 |  | Confirmed | Keep |

## P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

- **DOI:** [10.1038/s41467-022-31985-y](https://doi.org/10.1038/s41467-022-31985-y) · **Year:** 2022 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher PDF, Nature Communications (CC BY) — https://www.nature.com/articles/s41467-022-31985-y.pdf — accessed 2026-10-04
- **Version:** Publisher version of record (Nat. Commun. 13:4654, 2022). May differ from the published version: No (version of record).
- **Location convention:** Printed article page numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** edge_device / on_device Unknown: identify the hardware running real-time detection and the control loop; latency_evaluation Unknown: real-time detection/correction claimed without values; confidence_gating Unknown: check whether prediction confidence triggers corrections; multi_view Unknown: camera configuration (number of cameras/poses)

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Methods (p. 10) | Logitech C270 webcams and Raspberry Pi cameras; no smartphone. | Confirmed | Change |
| edge_device | Unknown | No | Online correction (p. 6); Computing requirements (p. 11) | Images are sent to a local server for inference; the final models ran on a workstation with two NVIDIA Quadro RTX 5000 GPUs, which was also used for online correction. The Raspberry Pi is only a networked gateway. | Confirmed | Change |
| on_device | Unknown | No | p. 6, p. 11 | Inference runs on the local server, not on the capture device. | Confirmed | Change |
| cloud | Unknown | No | p. 6, p. 11 | Local server; no remote cloud processing described. | Confirmed | Change |
| adaptive_inference | Unknown | No | Online correction pipeline (p. 6) | Fixed network; the control loop adapts printer parameters, not inference (README §7.3). | Confirmed | Change |
| resource_awareness | Unknown | No | full text | No resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | full text | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | full text | Hotend temperature is a printing parameter being corrected, not a device thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | Methods (p. 10), Discussion (p. 10) | A single nozzle-facing camera; combining with a global camera is suggested as future work. | Confirmed | Change |
| uncertainty | Unknown | No | full text | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | Unknown | Fig. 3, Online correction pipeline (p. 6) | Predictions are stored in lists of length L; a correction is made only if one prediction reaches the mode-threshold share of the list, and that share scales the adjustment. This is a vote frequency over repeated predictions rather than a model confidence score; whether it counts needs a decision. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | Network architecture section, Fig. 2 | Supervised multi-head classification of parameter deviation (too low/good/too high). | Confirmed | Change |
| latency_evaluation | Unknown | Unknown | p. 6, Methods (p. 10) | Images are captured at 2.5 Hz and correction speed is discussed, but no inference timing on stated hardware was found in the sections read. | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | Test accuracy across four parameters 84.3% (attention multi-head network; Table 1); single-stage ResNet18-101 baselines 80.4-82.5%; flow-rate accuracy 82.1% multi-head vs 77.5% single-head | Table 1 and Methods (p. 11) |  | Confirmed | Change |
| efficiency_metrics | (blank) | (blank) | full text | No efficiency measurement reported. | Confirmed | Keep |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | 3D-Print Inspection / Real-time error detection and correction in material extrusion 3D printing | Error detection and closed-loop correction in material-extrusion 3D printing from nozzle images | Introduction |  | Confirmed | Keep |
| dataset | 1.2 million images from 192 parts labelled with printing parameters | CAXTON dataset: 1,272,273 raw images, 946,283 after cleaning, from 192 prints on eight Creality CR-20 Pro printers (PLA), labelled with printing parameters | Dataset generation, filtering and augmentation section | Refines the current value. | Confirmed | Change |
| hardware/device | Unknown | Inference and training: workstation with 2x NVIDIA Quadro RTX 5000 and i9-9900K; Acquisition: Logitech C270 webcam per printer (Raspberry Pi Camera v1 on unseen setups); Gateway: Raspberry Pi 4 Model B | Methods (pp. 10-11) |  | Confirmed | Change |
| model(s) | Multi-head neural network with control loop | Multi-head residual attention network (shared backbone, four heads) | Network architecture section, Fig. 2 |  | Confirmed | Change |
| inference location | (not a CSV field) | Local server (workstation) | p. 6, p. 11 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None in inference; printer parameters corrected by a feedback loop | p. 6 |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | full text |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Classification accuracy per parameter; qualitative correction demonstrations | Table 1, Figs. 4-5 |  | Confirmed | Keep |
| limitations | (blank) | Weakness for small Z-offset changes; dataset bias; mechanical and electrical failures and large errors (cracking, warping, detachment) not solved; correction oscillations possible | Discussion (p. 10) | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Lab printers including unseen printers (Lulzbot Taz 6, modified Ender 3 Pro for direct ink writing) | Figs. 4-5 and text; Methods (p. 10) |  | Confirmed | Keep |

## P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

- **DOI:** [10.3390/pr8111464](https://doi.org/10.3390/pr8111464) · **Year:** 2020 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher full-text HTML, MDPI Processes (CC BY) — https://www.mdpi.com/2227-9717/8/11/1464 — accessed 2026-10-04
- **Version:** Publisher version of record (Processes 8(11):1464; HTML). May differ from the published version: No (version of record).
- **Location convention:** HTML has no page numbers; locations are section numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** edge_device / on_device Unknown: abstract mentions "microprocessors and a camera" generically; latency_evaluation Unknown: "fast speed" claimed without values; confidence_gating Unknown: check whether detections trigger stop/correction via a confidence threshold

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §3 | Raspberry Pi 4 with a camera; no smartphone. | Confirmed | Change |
| edge_device | Unknown | Yes | §3 | The trained SSD model runs on a Raspberry Pi 4 with a connected camera, at the same frame rate as the earlier setup. | Confirmed | Change |
| on_device | Unknown | Yes | §3 | Inference runs on the Raspberry Pi 4 with its attached camera placed in front of the print bed. | Confirmed | Change |
| cloud | Unknown | No | §2.2, §3 | Training on a Tesla K80 GPU; live inference on the Raspberry Pi; no cloud processing. | Confirmed | Change |
| adaptive_inference | Unknown | No | keyword search of full text + methods/results read | Fixed SSD-300 model. | Confirmed | Change |
| resource_awareness | Unknown | No | §2.2 | SSD-300 chosen over SSD-512 for its published FPS: design-time choice, not a resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §1.2, §3 | A single camera; the authors note that multiple angles add complexity. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | Probability scores are used for ranking and gating, but uncertainty is not estimated or calibrated. | Confirmed | Change |
| confidence_gating | Unknown | Yes | §3 | A wrapper algorithm checks each frame; if the probability score of a predicted defect exceeds a predefined value, it notifies the user whether to stop the print. | Confirmed | Change |
| anomaly_detection | Unknown | No | §2.1, §2.2 | Supervised SSD detector trained on annotated stringing images. | Confirmed | Change |
| latency_evaluation | Unknown | Yes | §3 | latency type: throughput/FPS. The setup ran at 14 FPS on live video, and at the same rate on the Raspberry Pi 4. The 59 FPS in the conclusions is the published SSD-300 benchmark, not the authors' measurement. | Confirmed | Change |
| accuracy_metrics | (blank) | Test set: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training set: precision 0.75, recall 0.92 | §3 |  | Confirmed | Change |
| efficiency_metrics | (blank) | 14 FPS on live video, same rate reported on Raspberry Pi 4 | §3 |  | Confirmed | Change |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | 3D-Print Inspection / Real-time stringing defect detection during FFF printing from camera video | Real-time stringing defect detection in FFF 3D printing with operator notification | Abstract, §3 |  | Confirmed | Keep |
| dataset | Images showing stringing defects | 500 images of a stringing test object printed on a Prusa i3 MK3S, augmented to 2,500 images; PASCAL VOC annotations | §2.1 |  | Confirmed | Change |
| hardware/device | Microprocessor plus camera (not specified in abstract) | Inference: Raspberry Pi 4 with connected camera; Training: NVIDIA Tesla K80 | §2.2, §3 |  | Confirmed | Change |
| model(s) | Deep CNN | SSD-300 with VGG16 base network (TensorFlow Object Detection API) | §2.2 |  | Confirmed | Change |
| inference location | (not a CSV field) | On the Raspberry Pi 4 next to the printer | §3 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Precision, recall, F1, average precision at IoU 0.4-0.6; FPS | §2.3, §3 |  | Confirmed | Keep |
| limitations | (blank) | Poor generalisation to external web images; small, case-specific training set (one printer, few shapes) | §3, §4 | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Live remote monitoring of long prints on one printer, with shapes similar to the training data | §3 |  | Confirmed | Keep |

## P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

- **DOI:** [10.1016/j.promfg.2018.07.111](https://doi.org/10.1016/j.promfg.2018.07.111) · **Year:** 2018 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** None obtained — https://doi.org/10.1016/j.promfg.2018.07.111 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Gold open access per OpenAlex/Semantic Scholar, but ScienceDirect served a bot check; not bypassed.
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** multi_view Unknown: images taken "at several critical stages" — verify whether the camera pose changes (CD-09); Inference hardware and location not stated; latency_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| on_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Unknown | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Unknown | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | 3D-Print Inspection / Good/defective classification of semi-finished 3D printed parts | not examined (full text unavailable) |  |  |  |  |
| dataset | ABS and PLA printed parts imaged at critical print stages | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Camera integrated with printer | not examined (full text unavailable) |  |  |  |  |
| model(s) | Support vector machine | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

- **DOI:** [10.1007/s00170-024-14452-4](https://doi.org/10.1007/s00170-024-14452-4) · **Year:** 2024 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** None obtained — https://doi.org/10.1007/s00170-024-14452-4 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Subscription article; no legitimate open copy found (Step 9.1).
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** edge_device / on_device Unknown: identify the hardware on which FPS was measured and whether the detection system is deployed on edge hardware; latency type: throughput/FPS (relative +18.1%); check for absolute values; hardware not stated in abstract

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| on_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Unknown | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Unknown | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Yes | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | mAP50 97.5% | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8 | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time detection of five common FFF printing defects | not examined (full text unavailable) |  |  |  |  |
| dataset | Deliberately designed defect dataset (five defect types) | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Unknown | not examined (full text unavailable) |  |  |  |  |
| model(s) | Improved YOLOv8 with lightweight group-convolution detection head | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P019 — Real-time defect detection in 3D printing using machine learning

- **DOI:** [10.1016/j.matpr.2020.10.482](https://doi.org/10.1016/j.matpr.2020.10.482) · **Year:** 2021 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** None obtained — https://doi.org/10.1016/j.matpr.2020.10.482 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Subscription article; no legitimate open copy found (Step 9.1).
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** Inference hardware and location not stated (printer-integrated camera only); latency_evaluation Unknown: "real-time" claimed without values; anomaly_detection Unknown: confirm supervised vs normal-only training

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| on_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Unknown | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Unknown | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time detection of infill defects in 3D printing | not examined (full text unavailable) |  |  |  |  |
| dataset | Unknown | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Camera integrated with 3D printer | not examined (full text unavailable) |  |  |  |  |
| model(s) | CNN image classifier | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

- **DOI:** [10.3390/asi4020034](https://doi.org/10.3390/asi4020034) · **Year:** 2021 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** Publisher full-text HTML, MDPI Applied System Innovation (CC BY) — https://www.mdpi.com/2571-5577/4/2/34 — accessed 2026-10-04
- **Version:** Publisher version of record (ASI 4(2):34; HTML). May differ from the published version: No (version of record).
- **Location convention:** HTML has no page numbers; locations are section numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** anomaly_detection Unknown: abstract says "anomaly detection" but describes supervised classifiers (CD-14); Hardware / inference location not stated; "low computing costs" and real-time suitability claimed without values

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §3, §4.1 | Raspberry Pi camera; no smartphone. | Confirmed | Change |
| edge_device | Unknown | Unknown | §3, §4.1, §5.4 | A Raspberry Pi 4B is described as "used for the processing" with a Pi camera and display, but all programming, training and testing were done in MATLAB. Where real-time classification runs is not stated. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §3, §4.1, §5.4 | Same ambiguity as edge_device. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | keyword search of full text + methods/results read | No cloud processing described. | Confirmed | Change |
| adaptive_inference | Unknown | No | keyword search of full text + methods/results read | Fixed feature extractor + classifier. | Confirmed | Change |
| resource_awareness | Unknown | No | keyword search of full text + methods/results read | No resource-driven decision. | Confirmed | Change |
| energy_evaluation | Unknown | No | keyword search of full text + methods/results read | No energy or power measurement. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | Printing temperature is a process parameter, not a device thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §4.2, §5.4 | Four to five images per layer from one mounted camera are each classified individually; views are not used jointly. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | §3.3 | The ensemble uses a vote count to assign the final label; no downstream action is triggered by a confidence score. | Confirmed | Change |
| anomaly_detection | Unknown | No | §3.4, §5 | Despite the "anomaly detection" wording, models are trained on manually labelled good and bad layer images (supervised; README §7.3, CD-14). | Confirmed | Change |
| latency_evaluation | Unknown | Unknown | §5.4, §6 | "Less computational time" is claimed without a measured value (Decision 3). | Confirmed | Keep |
| accuracy_metrics | (blank) | AlexNet+SVM and EfficientNet-B0+SVM 99.70% (§5.1); ensemble with AlexNet features 100% (§5.2); density-wise classification ResNet50 100% (§5.3) | §5.1-§5.3, §6 | Second-best values differ between §5 and the conclusions (internal inconsistency). | Confirmed | Change |
| efficiency_metrics | (blank) | (blank) | keyword search of full text + methods/results read | No efficiency measurement reported. | Confirmed | Keep |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | 3D-Print Inspection / Layer-wise fault detection in FDM printing | Layer-wise fault detection in FDM printing from camera images | §3, §5.4 |  | Confirmed | Keep |
| dataset | Unknown | 1,700 layer images (good/bad) of a 25 x 25 x 5 mm cube, 32 parameter variants, Dreamer FDM printer | §4.2 |  | Confirmed | Change |
| hardware/device | Unknown | Acquisition: 8MP Raspberry Pi camera; Processing: Raspberry Pi 4B (role in inference unclear); MATLAB used for programming, training and testing | §3, §4.1 |  | Confirmed | Change |
| model(s) | Pretrained CNN features + ML classifiers (AlexNet + SVM best) | Pre-trained CNN features (AlexNet, GoogLeNet, ResNet18/50, EfficientNet-b0) with SVM, KNN, Naive Bayes, Decision Tree, Random Forest; majority-vote ensemble | §3.2, §3.3 | Matches the essence of the current value. | Confirmed | Keep |
| inference location | (not a CSV field) | Not stated | §3, §4.1 |  | Ambiguous | Needs researcher decision |
| adaptation mechanism | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| resource signals | (not a CSV field) | None | keyword search of full text + methods/results read |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Accuracy, loss, confusion matrices | §5 |  | Confirmed | Keep |
| limitations | (blank) | None explicitly stated | §6 |  | Confirmed | Keep |
| deployment setting | (not a CSV field) | Lab FDM printer with mounted Raspberry Pi camera | §4.1 |  | Confirmed | Keep |

## P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

- **DOI:** [10.1108/rpj-09-2024-0395](https://doi.org/10.1108/rpj-09-2024-0395) · **Year:** 2025 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** None obtained — https://doi.org/10.1108/rpj-09-2024-0395 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Subscription article; no legitimate open copy found (Step 9.1).
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** edge_device / on_device Unknown: Raspberry Pi is the acquisition system; verify whether inference runs on it; latency_evaluation Unknown; efficiency figures not in abstract; confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| on_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Unknown | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Unknown | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | Warping 98.59% (DenseNet121); stringing 99.38% (MobileNetV2); cracking 99.32% (XceptionNet); multi-class 98.90% (MobileNetV2) | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | 3D-Print Inspection / Warping, stringing and cracking detection in 3D-printed PLA/ABS parts | not examined (full text unavailable) |  |  |  |  |
| dataset | Defect images from Taguchi L9 design (extruder temp, bed temp, print speed) on a Delta printer | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Raspberry Pi-based data acquisition | not examined (full text unavailable) |  |  |  |  |
| model(s) | DenseNet121, MobileNetV2, ResNet50, VGG16, XceptionNet (transfer learning) | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

- **DOI:** [10.1016/j.mfglet.2019.09.005](https://doi.org/10.1016/j.mfglet.2019.09.005) · **Year:** 2019 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (abstract only)
- **Source used:** None obtained — https://doi.org/10.1016/j.mfglet.2019.09.005 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Subscription article; no legitimate open copy found (Step 9.1).
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** Inference hardware and location not stated; latency_evaluation Unknown: "faster than the speed of a human's response" is qualitative; confidence_gating Unknown: check whether correction is triggered by prediction confidence

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| on_device | Unknown | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Unknown | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Unknown | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | 3D-Print Inspection / Real-time monitoring and autonomous correction of FDM extrusion errors | not examined (full text unavailable) |  |  |  |  |
| dataset | Unknown | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Unknown | not examined (full text unavailable) |  |  |  |  |
| model(s) | Deep learning model with feedback loop | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

- **DOI:** [10.1145/3241539.3241559](https://doi.org/10.1145/3241539.3241559) · **Year:** 2018 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 1810.10090v1 (23 Oct 2018) — https://arxiv.org/abs/1810.10090 — accessed 2026-10-04
- **Version:** Author preprint carrying the MobiCom 2018 ACM copyright block; not confirmed identical to the ACM version of record. May differ from the published version: Possibly; not compared (ACM bot check).
- **Location convention:** No reliable printed page numbers in the extracted text; locations are section/figure numbers
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** smartphone Unknown: identify the evaluation platforms (abstract lists smartphones only as examples); Confirm efficiency_metrics values and baselines (up to 2.0x frame rate, 1.7x energy); thermal_evaluation / confidence_gating Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §4.3.1 | Implemented on three smartphones (Samsung Galaxy S8, Galaxy S7, LG Nexus 5; Android 7.0); results reported for the Galaxy S8. | Confirmed | Change |
| edge_device | Yes | Yes | §4.3.1 | Runs on the smartphones. | Confirmed | Keep |
| on_device | Yes | Yes | §4.3.1, §5 | On-device deep learning on the phones. | Confirmed | Keep |
| cloud | Unknown | No | §6 (Related Work) | The authors state the framework does not rely on cloud connectivity. | Confirmed | Change |
| adaptive_inference | Yes | Yes | §3, §4.3.2 | Runtime selection among nested descendant models with different capacities. | Confirmed | Keep |
| resource_awareness | Yes | Yes | §3, §4.3.1 | Scheduler allocates runtime resources (e.g. 400 MB memory budget) and picks resource-accuracy trade-offs. | Confirmed | Keep |
| energy_evaluation | Yes | Yes | §4.3.1, §4.3.3, Figs. 8 and 11 | Power measured with a Monsoon power monitor; energy reductions reported. | Confirmed | Keep |
| thermal_evaluation | Unknown | No | keyword search of full text | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | keyword search of full text + methods/results read | Image classification benchmarks; no multi-view. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | keyword search of full text + methods/results read | No confidence-triggered action. | Confirmed | Change |
| anomaly_detection | Unknown | No | keyword search of full text + methods/results read | Supervised classification tasks. | Confirmed | Change |
| latency_evaluation | Yes | Yes | §4.3.2, Fig. 10 | latency type: throughput/FPS (frame-rate speedup on the Galaxy S8). | Confirmed | Keep |
| accuracy_metrics | Up to +4.2% inference accuracy vs resource-agnostic baseline | Up to +4.2% inference accuracy vs resource-agnostic baseline | §4.3.2 | Supported: 4.1% (MinTotalCost) and 4.2% (MinMaxCost) at equal frame rate. | Confirmed | Keep |
| efficiency_metrics | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | §4.3.2, §4.3.3 | Supported: 2.0x / 1.9x frame rate at equal accuracy; 1.7x / 1.5x energy reduction. | Confirmed | Keep |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | Adaptive Inference / Mobile Vision / Resource-aware multi-tenant on-device deep learning for continuous mobile vision | Resource-aware multi-tenant on-device inference for continuous mobile vision (not inspection) | §1, §4.1 |  | Confirmed | Keep |
| dataset | Unknown | CIFAR-10, ImageNet-50, ImageNet-100, GTSRB, Adience-Gender, Places-32 | §4.1.1 |  | Confirmed | Change |
| hardware/device | Mobile vision systems (platform not stated in abstract) | Inference: Samsung Galaxy S8 (reported), Galaxy S7, LG Nexus 5 (Android 7.0); power: Monsoon power monitor | §4.3.1 |  | Confirmed | Change |
| model(s) | NestDNN | NestDNN multi-capacity models built from VGG-16 and ResNet-50 | §4.1 |  | Confirmed | Change |
| inference location | (not a CSV field) | On the smartphone | §4.3.1 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | Runtime switching among nested descendant models (model switching / dynamic capacity) | §3 |  | Confirmed | Keep |
| resource signals | (not a CSV field) | Available memory and compute; number of concurrent applications | §3, §4.3.1 |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Accuracy gain, frame-rate speedup, energy, memory and model-switching cost | §4 |  | Confirmed | Keep |
| limitations | (blank) | Filter-importance (TRR) pruning has much higher computational cost than L1-norm pruning, raising the cost of generating multi-capacity models | §5 | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Benchmark emulating application launches and kills over 60 s simulations | §4.3.1 |  | Confirmed | Keep |

## P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

- **DOI:** [10.1145/3649329.3657310](https://doi.org/10.1145/3649329.3657310) · **Year:** 2024 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Partially verified
- **Source used:** arXiv preprint 2410.10847v1 (1 Oct 2024) — https://arxiv.org/abs/2410.10847 — accessed 2026-10-04
- **Version:** Author preprint carrying the DAC 2024 ACM copyright block; publisher version is closed access. May differ from the published version: Possibly; not compared (closed access).
- **Location convention:** Page numbers are arXiv PDF page numbers (1-5 plus references)
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** adaptive_inference recoded Yes→Unknown (Decision 4): confirm whether any model-level adaptation exists beyond CPU/GPU DVFS; latency_evaluation recoded Yes→Unknown (Decision 3): check for measured latency/variation values; smartphone: confirm Mi 11 Lite variant (4G/5G) used; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | §4.4 (p. 4), Table 2 (p. 5) | The Mi 11 Lite with a Snapdragon 780G is used; the Table 2 caption names it the Mi 11 Lite 5G. Earlier external verification (Step 8.3) stands. | Confirmed | Keep |
| edge_device | Yes | Yes | §4.4, §5 | Jetson Orin Nano and Mi 11 Lite 5G. | Confirmed | Keep |
| on_device | Yes | Yes | §5.1.2 (p. 5) | The two-stage detectors run on the devices. Note: the Lotus DRL agent itself runs on a desktop with an RTX 2080Ti and controls device frequencies over a socket (§4.4, p. 4). | Confirmed | Keep |
| cloud | Unknown | No | §4.4 (p. 4) | The off-device agent runs on a desktop machine over a socket, not on a cloud datacenter. | Confirmed | Change |
| adaptive_inference | Unknown | No | §4.2-§4.4 (pp. 3-4) | Lotus scales CPU and GPU frequencies twice per frame via DRL; the detector models are unchanged. The two-width network belongs to the agent's Q-network, not the detector. The variable proposal count is an inherent property of the unmodified detectors. | Confirmed | Change |
| resource_awareness | Yes | Yes | §4.3 (p. 4) | Agent state includes CPU/GPU temperature, frequency level and remaining time to the latency constraint. | Confirmed | Keep |
| energy_evaluation | Unknown | No | full text | Power is mentioned only as motivation; no energy or power results. | Confirmed | Change |
| thermal_evaluation | Yes | Yes | §5.2, Figs. 4-7 (pp. 4-5) | Device temperatures are measured and compared with baselines. | Confirmed | Keep |
| multi_view | Unknown | No | full text | KITTI and VisDrone2019 detection; no multi-view inspection. | Confirmed | Change |
| uncertainty | Unknown | No | full text | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | full text | No confidence-triggered action. | Confirmed | Change |
| anomaly_detection | Unknown | No | full text | Object detection benchmarks. | Confirmed | Change |
| latency_evaluation | Unknown | Yes | Tables 1-2 (pp. 4-5), §5.2.1 | latency type: inference latency (mean and standard deviation per image on Jetson Orin Nano and Mi 11 Lite 5G). | Confirmed | Change |
| accuracy_metrics | (blank) | (blank) | full text | No detection accuracy is reported for Lotus (Fig. 1 mAP values are motivation for the baseline models). | Confirmed | Keep |
| efficiency_metrics | (blank) | Jetson Orin Nano, MaskRCNN on VisDrone2019: latency -30.8% vs default governor and -9.1% vs zTT; latency standard deviation -72.8% / -38.1%; latency-constraint satisfaction +35.9% / +24.8% (§5.2.1). Mi 11 Lite 5G: latency variation -29.4% / -9.5% for MaskRCNN on KITTI; satisfaction rate 92.5% for FasterRCNN on VisDrone2019. Lotus overhead 8.52 ms per inference | §4.4.2, §5.2.1 (pp. 4-5) | Absolute per-model latencies are in Tables 1-2. | Confirmed | Change |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | Thermal-aware Edge AI / Thermal and latency-variation management for two-stage detectors | Thermal and latency-variation management for two-stage detectors on edge devices (autonomous-driving and drone datasets) | §1, §5.1.2 |  | Confirmed | Keep |
| dataset | Unknown | KITTI, VisDrone2019 | §5.1.2 (p. 5) |  | Confirmed | Change |
| hardware/device | NVIDIA Jetson Orin Nano; Mi 11 Lite mobile platform | Inference: NVIDIA Jetson Orin Nano; Xiaomi Mi 11 Lite 5G (Snapdragon 780G). DRL agent: desktop with NVIDIA RTX 2080Ti over socket | §4.4 (p. 4) |  | Confirmed | Change |
| model(s) | LOTUS (DRL-based joint CPU/GPU frequency scaling) | Faster R-CNN, Mask R-CNN (detectors); DQN agent with a 4-layer MLP at two widths | §4.4.1, §5.1.2 |  | Confirmed | Change |
| inference location | (not a CSV field) | Detector on device; frequency-control agent on a separate desktop | §4.4 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | DRL-driven joint CPU/GPU DVFS, two decisions per frame (system-level) | §4.2-§4.3 |  | Confirmed | Keep |
| resource signals | (not a CSV field) | CPU/GPU temperature, CPU/GPU frequency level, remaining time to latency constraint, number of proposals | §4.3.2 (p. 4) |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Mean and standard deviation of latency, latency-constraint satisfaction rate, device temperature | §5, Tables 1-2 |  | Confirmed | Keep |
| limitations | (blank) | None explicitly stated | §6 |  | Confirmed | Keep |
| deployment setting | (not a CSV field) | Lab: 25 C indoor static environment; warm (25 C) and cold (0 C) zones; dataset switching | §5.2 (p. 5) |  | Confirmed | Keep |

## P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

- **DOI:** [10.1145/3793860](https://doi.org/10.1145/3793860) · **Year:** 2026 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Blocked (inaccessible from this environment)
- **Source used:** None obtained — http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-587035 — accessed 2026-10-04
- **Version:** -. May differ from the published version: -.
- **Location convention:** -
- **Blocker:** Only open copy listed is the Uppsala DiVA repository; it did not respond from this environment (network connection failed; browser navigation refused).
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** latency_evaluation recoded Yes→Unknown (Decision 3): check for measured frame-rate values; smartphone Unknown: identify the evaluation devices; confidence_gating Unknown: check whether multi-exit decisions use prediction confidence or only thermal state; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | not examined (full text unavailable) |  |  |  |  |
| edge_device | Yes | not examined (full text unavailable) |  |  |  |  |
| on_device | Yes | not examined (full text unavailable) |  |  |  |  |
| cloud | Unknown | not examined (full text unavailable) |  |  |  |  |
| adaptive_inference | Yes | not examined (full text unavailable) |  |  |  |  |
| resource_awareness | Yes | not examined (full text unavailable) |  |  |  |  |
| energy_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| thermal_evaluation | Yes | not examined (full text unavailable) |  |  |  |  |
| multi_view | Unknown | not examined (full text unavailable) |  |  |  |  |
| uncertainty | Unknown | not examined (full text unavailable) |  |  |  |  |
| confidence_gating | Unknown | not examined (full text unavailable) |  |  |  |  |
| anomaly_detection | Unknown | not examined (full text unavailable) |  |  |  |  |
| latency_evaluation | Unknown | not examined (full text unavailable) |  |  |  |  |
| accuracy_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| efficiency_metrics | (blank) | not examined (full text unavailable) |  |  |  |  |
| paper type | system/method | not examined (full text unavailable) |  |  |  |  |
| application/domain | Thermal-aware Edge AI / Thermal-aware multi-DNN on-device inference for mobile video | not examined (full text unavailable) |  |  |  |  |
| dataset | Two benchmarks + Virtual YouTuber streaming app | not examined (full text unavailable) |  |  |  |  |
| hardware/device | Mobile devices with heterogeneous processors | not examined (full text unavailable) |  |  |  |  |
| model(s) | Phoenix (RL task allocation + multi-exit networks) | not examined (full text unavailable) |  |  |  |  |
| inference location | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| adaptation mechanism | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| resource signals | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| evaluation metrics | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |
| limitations | (blank) | not examined (full text unavailable) |  |  |  |  |
| deployment setting | (not a CSV field) | not examined (full text unavailable) |  |  |  |  |

## P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

- **DOI:** [10.1145/3665868](https://doi.org/10.1145/3665868) · **Year:** 2024 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** arXiv copy 2409.01089v1 with ACM TECS journal pagination — https://arxiv.org/abs/2409.01089 — accessed 2026-10-04
- **Version:** Copy formatted as the published article (ACM TECS 23(4), Article 60, June 2024; pages 60:1-60:xx). May differ from the published version: Unlikely (journal layout), but not formally confirmed against the ACM page.
- **Location convention:** Journal page numbers of the form 60:nn
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** smartphone Unknown: identify the evaluation devices; latency_evaluation Unknown: check for measured latency/SLO results; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §6.3 (p. 60:19) | Evaluated on three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71. | Confirmed | Change |
| edge_device | Yes | Yes | §6.3 | The smartphones above. | Confirmed | Keep |
| on_device | Yes | Yes | §6.3-§7 | On-device execution with TFLite on CPU/GPU/NPU/DSP. | Confirmed | Keep |
| cloud | Unknown | No | Fig. 2 (p. 60:15) | A server is used only for offline model conversion and evaluation; runtime inference is on the device. | Confirmed | Change |
| adaptive_inference | Yes | Yes | §4.3.3, §7.2 (pp. 60:12-60:24) | The Runtime Manager switches model, processor or both at runtime. | Confirmed | Keep |
| resource_awareness | Yes | Yes | §4.3.2-§4.3.4, §7.2 | Switching is triggered by processor overload and memory pressure, using workload and memory signals. | Confirmed | Keep |
| energy_evaluation | Unknown | Unknown | §4.1, §6.4 (p. 60:20), Fig. 2 | Energy is an objective and is profiled on the device, but no energy results were found in §7. | Ambiguous | Needs researcher decision |
| thermal_evaluation | Unknown | No | §4.3.2, §6.4, §7 (keyword search) | Overheating is discussed as a cause of processor issues and idle periods are used to keep temperatures consistent, but temperature is not measured or reported. | Confirmed | Change |
| multi_view | Unknown | No | keyword search of full text + methods/results read | No multi-view. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | keyword search of full text + methods/results read | No confidence-triggered action. | Confirmed | Change |
| anomaly_detection | Unknown | No | keyword search of full text + methods/results read | Supervised tasks. | Confirmed | Change |
| latency_evaluation | Unknown | Yes | §6.4, §7.1-§7.2, Fig. 8 (pp. 60:20-60:24) | latency type: inference latency (average latency in ms per design) and throughput/FPS (images per second). | Confirmed | Change |
| accuracy_metrics | (blank) | UC1 initial design on S20 (EfficientNet Lite0, FFX8, CPU): 75.11% accuracy; UC1 vs transferred baselines: +0.156 average accuracy | §7.1.2, §7.2.1 |  | Confirmed | Change |
| efficiency_metrics | (blank) | Up to 4.06x over hardware-unaware multi-DNN designs; vs transferred baselines: UC1 +32.7% throughput, UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory footprint 16 MB | §7.1.2, §7.2.1 |  | Confirmed | Change |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | Adaptive Inference / Mobile / Constraint-aware runtime adaptation for single- and multi-DNN workloads on heterogeneous mobile devices | Constraint-aware runtime adaptation of single- and multi-DNN workloads on smartphones (not inspection) | §1, §6.2 |  | Confirmed | Keep |
| dataset | Text classification, scene recognition, face analysis tasks | Use cases covering image classification, scene recognition, face analysis, text classification and audio (YAMNet) | §6.2 | Current value covers most tasks; audio use case not listed. | Confirmed | Change |
| hardware/device | Heterogeneous mobile devices | Inference: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71 (CPU, GPU, NPU; DSP on A71) | §6.3 |  | Confirmed | Change |
| model(s) | CARIn (multi-objective optimisation + RASS solver) | CARIn with the RASS solver; model suites including EfficientNet Lite variants and YAMNet | §4, §6.2, Table 8 |  | Confirmed | Keep |
| inference location | (not a CSV field) | On the smartphone | §6.3 |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | Model switching and processor switching from a precomputed design set | §4.3.3-§4.3.4 |  | Confirmed | Keep |
| resource signals | (not a CSV field) | Processor workload distribution and aggregate memory use | §4.3.4 |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Optimality, accuracy, latency (mean and standard deviation), throughput, memory, model size | §4.1, §7 |  | Confirmed | Keep |
| limitations | (blank) | Exhaustive on-device profiling is too costly for realistic deployment; generative models not evaluated | §8 (p. 60:26) | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Lab evaluation on three phones with controlled runtime fluctuations | §6-§7 |  | Confirmed | Keep |

## P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

- **DOI:** [10.1109/tmc.2025.3594214](https://doi.org/10.1109/tmc.2025.3594214) · **Year:** 2026 · **Relevance class (audit proposal):** A · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** FH JOANNEUM ePUB institutional repository PDF — https://epub.fh-joanneum.at/obvfhjoa/content/titleinfo/13393868/full.pdf — accessed 2026-10-04
- **Version:** Copy with IEEE TMC 25(1), Jan 2026 journal pagination (pp. 451-463); OpenAlex labels this repository copy "submittedVersion". May differ from the published version: Unlikely (journal layout), label conflict noted.
- **Location convention:** Printed journal page numbers 451-463
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** latency_evaluation recoded Yes→Unknown: only adaptation time is in the abstract; check for inference latency on the four platforms; smartphone Unknown: identify the four "mobile and embedded" platforms; energy_evaluation Unknown

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | §VI (p. 461) | Evaluated on two mobile phones: Xiaomi Redmi Note 9 Pro and Google Pixel 6, using the TFLite benchmark tool on Android. | Confirmed | Change |
| edge_device | Yes | Yes | §VI | Phones and IoT boards (Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2). | Confirmed | Keep |
| on_device | Yes | Yes | §VI | On-device inference and submodel switching measured. | Confirmed | Keep |
| cloud | Unknown | No | §VI, Acknowledgment | Computing clusters used only for training; no cloud inference. | Confirmed | Change |
| adaptive_inference | Yes | Yes | §III, §VI | Nested subnetworks are switched at runtime under changing resource constraints. | Confirmed | Keep |
| resource_awareness | Yes | Yes | §I, §III | Subnetworks are chosen to fit dynamic resource constraints (MACs, peak memory). | Confirmed | Keep |
| energy_evaluation | Unknown | Yes | §VI, Table VI (p. 463) | Inference energy measured with a Power Profiler Kit (PPK2) on the Nordic nRF52840: 20-61 mJ for DS-CNN; switching < 0.01 mJ. | Confirmed | Change |
| thermal_evaluation | Unknown | No | keyword search of full text + methods/results read | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | keyword search of full text + methods/results read | No multi-view. | Confirmed | Change |
| uncertainty | Unknown | No | keyword search of full text + methods/results read | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | No | §VI, Fig. 11 | Early-exit linear classifiers appear only as a comparison baseline; no confidence-triggered action in REDS. | Confirmed | Change |
| anomaly_detection | Unknown | No | keyword search of full text + methods/results read | Supervised benchmark tasks. | Confirmed | Change |
| latency_evaluation | Unknown | Yes | §VI, Fig. 10 (p. 462) | latency type: inference latency (inference time on phones via TFLite benchmark and on IoT boards; e.g. 2-layer FC network on Arduino Nano 33 BLE Sense: 2,131 +/- 27 us at 25% MACs and 4,548 +/- 13 us at 50% MACs). | Confirmed | Change |
| accuracy_metrics | (blank) | (blank) | Figs. 5-11 | Accuracy results are given mainly in figures; no single value extracted. | Confirmed | Keep |
| efficiency_metrics | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | Adaptation time 38 +/- 1 us (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 +/- 27 us (25% MACs) and 4,548 +/- 13 us (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2) | §VI, Table VI (pp. 462-463) | The extracted PDF text drops the micro sign; microsecond units follow the abstract (adaptation time under 40 us). | Confirmed | Change |
| paper type | system/method | system/method | full text |  | Confirmed | Keep |
| application/domain | Adaptive Inference / Edge / Deep subnetworks that adapt to dynamic resource constraints on edge devices | Resource-adaptive deep subnetworks for mobile and IoT devices (keyword spotting, visual wake words, image classification); not inspection | §I, §IV |  | Confirmed | Keep |
| dataset | Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K | Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K | Abstract, §IV | Matches current value. | Confirmed | Keep |
| hardware/device | Four mobile and embedded platforms incl. Arduino Nano 33 BLE | Inference: Xiaomi Redmi Note 9 Pro, Google Pixel 6, Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2; cache benchmark: Raspberry Pi Pico (RP2040) | §V-§VI |  | Confirmed | Change |
| model(s) | REDS | REDS subnetworks for DNN, CNN, DS-CNN and MobileNetV1-style architectures (iterative knapsack solver) | §III-§VI |  | Confirmed | Keep |
| inference location | (not a CSV field) | On device | §VI |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | Runtime switching among nested subnetworks | §III, §VI |  | Confirmed | Keep |
| resource signals | (not a CSV field) | MACs, peak memory, available resources | §III |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Accuracy, parameters, MACs, inference time, adaptation time, energy | §IV-§VI |  | Confirmed | Keep |
| limitations | (blank) | Not tested for large language or multimodal models; cache optimisation for convolutions not explored; energy as a solver constraint left for future work | §VII (p. 463) | Stated by the authors (as future work). | Confirmed | Change |
| deployment setting | (not a CSV field) | Lab benchmarks on phones and IoT boards | §VI |  | Confirmed | Keep |

## P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

- **DOI:** [10.1016/j.aei.2020.101101](https://doi.org/10.1016/j.aei.2020.101101) · **Year:** 2020 · **Relevance class (audit proposal):** D · **Priority:** HIGH
- **Verification status (Step 9.2):** Fully verified
- **Source used:** UTS institutional repository (OPUS) copy of the publisher PDF — https://opus.lib.uts.edu.au/handle/10453/147577 — accessed 2026-10-04
- **Version:** Publisher version of record PDF (Adv. Eng. Inform. 45 (2020) 101101; CC BY-NC-ND). May differ from the published version: No (publisher PDF).
- **Location convention:** Printed journal page numbers 1-8
- **Verifier / date:** Claude Code, 2026-10-04
- **Issues to resolve (from Step 9.1):** **Relevance (audit class D):** verify whether the quality inspection is image/vision-based or uses process data; edge_device and cloud recoded Yes→Unknown: identify the hardware behind "Edge Cloud Computing" and where models run; on_device / latency_evaluation Unknown; Relevance class must not be changed without researcher review

| Field | Current CSV Value | Full-Text Value | Evidence Location | Evidence Quote/Paraphrase | Confidence | Action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | §4.2 (p. 7) | Edge hardware is an industrial PC; no smartphone. | Confirmed | Change |
| edge_device | Unknown | Unknown | §4.2 (p. 7) | Inference ("deployment") runs on an edge industrial PC with an Intel Celeron N2930 at the manufacturing line. Whether a low-power industrial PC counts as a resource-constrained edge device is the open industrial-PC question. | Ambiguous | Needs researcher decision |
| on_device | Unknown | Unknown | §4.2 (p. 7) | The edge PC receives SPI data files over TCP/IP; it is not the capturing device or physically attached to it. Leaning No, but the case depends on the same open question. | Ambiguous | Needs researcher decision |
| cloud | Unknown | No | §4.2 (p. 7), §5 (p. 8) | Models are trained in a company-owned Spark cluster and data stored in AWS S3; inference runs on the edge device. Cloud used only for training and storage (README §7.3). | Confirmed | Change |
| adaptive_inference | Unknown | No | §3, §4 | Static GBT model; "dynamic inspection" refers to routing parts, not to inference. | Confirmed | Change |
| resource_awareness | Unknown | Unknown | §3.4 (p. 5), §4.1 (p. 6) | GBT chosen over SVM because its scoring time was eight times faster with future scaling in mind; real-time constraint set by takt time. A deployment-time choice under a timing constraint: depends on the open design-time question. | Ambiguous | Needs researcher decision |
| energy_evaluation | Unknown | No | §3.4 | Energy constraints are listed in general terms; nothing is measured. | Confirmed | Change |
| thermal_evaluation | Unknown | No | full text | No thermal measurement. | Confirmed | Change |
| multi_view | Unknown | No | §4 | Inputs are numeric SPI features, not images. | Confirmed | Change |
| uncertainty | Unknown | No | full text | No uncertainty estimation. | Confirmed | Change |
| confidence_gating | Unknown | Unknown | §3.3 (p. 5), §4.2 (p. 6) | Predicted class (with conservativeness tuning to avoid false negatives) decides which fields of view skip X-ray. No confidence score is described; whether a class-triggered routing decision counts needs a decision. | Ambiguous | Needs researcher decision |
| anomaly_detection | Unknown | No | §3.2, §4.1 | Supervised classifiers trained on X-ray labels. | Confirmed | Change |
| latency_evaluation | Unknown | Yes | Table 3 (p. 7), §4.2 (p. 7) | Scoring times per 1,000 rows (Table 3, hardware not stated) and processing of current test sets in under one minute on the Intel Celeron N2930 edge PC. latency type: end-to-end latency (coarse bound on stated hardware). | Ambiguous | Needs researcher decision |
| accuracy_metrics | (blank) | Initial balanced sample (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9%. Conservative GBT on solder joints (Table 4): class recall 98.8% (defective) / 86.4% (defect-free). FOV level (Table 5): average X-ray inspection volume reduced by about 29% | Tables 3-5 (p. 7) |  | Confirmed | Change |
| efficiency_metrics | (blank) | Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets processed in < 1 min. Edge-cloud link: 2-150 ms latency, about 1 Mbit/s per line | Table 3, §4.2 (p. 7) |  | Confirmed | Change |
| paper type | system/method | system/method (industrial case study) | §3-§5 |  | Confirmed | Keep |
| application/domain | Industrial Quality Inspection / Edge-Cloud / Predictive model-based quality inspection in SMT manufacturing | Quality prediction for PCB solder joints in SMT assembly from numeric solder-paste-inspection (SPI) measurements, to reduce X-ray inspection volume. The ML input is not images | §1, §4 (pp. 1, 5-6) | Key relevance finding: not image-based inspection. Relevance class decision is the researcher's. | Confirmed | Needs researcher decision |
| dataset | Real industrial SMT use case | Five months of SPI and X-ray records from one product variant at the Siemens Amberg plant; about 1.46 billion data points, ~0.0008% not OK; seven numeric SPI features (height, 2D/3D shape, surface, volume, X/Y offset) | §4 Table 2 (p. 6) |  | Confirmed | Change |
| hardware/device | Edge Cloud Computing infrastructure | Inference: industrial PC with Intel Celeron N2930 at the line; Training: company Spark cluster (up to 24 workstations); Storage: AWS S3 | §4.2 (p. 7) |  | Confirmed | Change |
| model(s) | Machine learning (models not stated in abstract) | Gradient Boosted Tree (selected); Decision Tree, Naive Bayes, Logistic Regression, SVM compared | §4.1 (p. 6) |  | Confirmed | Change |
| inference location | (not a CSV field) | Edge industrial PC at the manufacturing line (receives SPI files over TCP/IP) | §4.2 (p. 7) |  | Confirmed | Keep |
| adaptation mechanism | (not a CSV field) | None | full text |  | Confirmed | Keep |
| resource signals | (not a CSV field) | Takt time and model scoring time (model selection only) | §3.4, §4.1 |  | Confirmed | Keep |
| evaluation metrics | (not a CSV field) | Accuracy, recall, precision, TPR/FPR, training and scoring time, inspection-volume reduction | §3.2, Tables 3-5 |  | Confirmed | Keep |
| limitations | (blank) | Deployment limited to one product variant, one line and the SPI and X-ray data sources | §4.3 (p. 7) | Stated by the authors. | Confirmed | Change |
| deployment setting | (not a CSV field) | Siemens electronics plant, Amberg (Germany), SMT line with SPI and X-ray stations | §4 (p. 5) |  | Confirmed | Keep |

