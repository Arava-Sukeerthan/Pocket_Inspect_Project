# Full-Text Evidence Report (Step 9.2)

_2026-10-04, Claude Code. Evidence only: **`papers.csv` was not modified**, relevance classes are unchanged, and no gap analysis was performed. Coding follows [`README.md` §7 v1.1](README.md#7-literature-coding-definitions). Field-by-field tables with locations are in [`fulltext_verification_template.md`](fulltext_verification_template.md). Proposed changes are summarised in [`fulltext_conflicts.md`](fulltext_conflicts.md)._

**Conventions:**
- Paraphrases are used instead of quotations.
- Page numbers are given only where the source has printed or PDF page numbers. HTML sources are cited by section, table or figure.
- "Keyword search" means the full text was searched for the field's terms, and the methods and results sections were read.
- Confidence is one of: Confirmed, Not supported, Ambiguous.
- The recommended action is one of: Keep current value, Candidate change, Needs researcher decision, Insufficient evidence.

## P001 — Deep learning smartphone application for real‐time detection of defects in buildings

### Source
Publisher full-text HTML, Wiley Online Library (open access) — https://onlinelibrary.wiley.com/doi/full/10.1002/stc.2751 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (Struct. Control Health Monit. 28(7) e2751; HTML). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Yes | Yes | Confirmed | §4, §6.3, §7 — Android smartphone app; the TFLite model is installed on an Android phone. The phone model is not named. |
| edge_device | Unknown | Yes | Confirmed | §6.3, §7; README §7.5 — Inference runs on the Android phone (resource-constrained mobile hardware). |
| on_device | Unknown | Yes | Confirmed | §6.3, §7, §8 — Trained model converted to TFLite and run on the phone; real-time detection on the phone camera video stream; conclusion says detection uses only smartphones. |
| cloud | Unknown | No | Confirmed | §4, §6 — Training on a desktop GPU workstation; inference on the phone; no cloud or server processing described. |
| adaptive_inference | Unknown | No | Confirmed | §4.2, §6 — Single fixed SSD MobileNet model; no runtime adaptation. |
| resource_awareness | Unknown | No | Confirmed | §3, §4.2 — Model chosen for its published speed/accuracy trade-off: a design-time lightweight-model choice, not a resource-driven decision (README §7.3). |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No temperature or throttling measurement. |
| multi_view | Unknown | No | Confirmed | §5, §7 — Single images and a single phone-camera video stream. |
| uncertainty | Unknown | No | Confirmed | §6.2, §7 — Prediction percentage displayed as confidence; no uncertainty estimation or calibration. |
| confidence_gating | Unknown | No | Confirmed | §6.2-§7 — Confidence is displayed in the app; no action is triggered by it. |
| anomaly_detection | Unknown | No | Confirmed | §5.3, §6 — Supervised detector trained on four labelled defect classes. |
| latency_evaluation | Unknown | Unknown | Ambiguous | §4.2, §7, Fig. 7 — App GUI shows inference time and Fig. 7 screenshots include it, but no values are given in the text. The 56 ms in §4.2 is the pre-trained model's published COCO benchmark, not the authors' measurement. Values may be readable in Fig. 7. |
| accuracy_metrics | (blank) | Per class at IoU 0.6 (Table 1), recall/precision/accuracy: crack 0.4/0.53/0.61; deterioration 0.68/0.68/0.83; mould 0.85/0.66/0.81; stain 0.71/0.85/0.95 | Confirmed | Table 1, §7 — Values from Table 1. The §7 text gives stain precision as 0.95 while Table 1 gives 0.85 (internal inconsistency; table value used). |
| efficiency_metrics | (blank) | (blank) | Confirmed | §7 — No measured efficiency value reported in the text. |

### Other evidence

- **paper type:** system/method (§1-§8). Develops and evaluates a smartphone defect-detection app.
- **application/domain:** Building defect detection (civil condition assessment): cracks, mould, stain, paint deterioration (Abstract, §1). Civil/building domain, not manufactured parts.
- **dataset:** 876 images (700 train / 176 test), 4 classes; mobile-phone and hand-held camera photos, internet images, public 128x128 crack dataset (§5.1, §6.2). Custom dataset assembled from several sources.
- **hardware/device:** Inference: Android smartphone (model not named); Training: Dell Precision 5820 with NVIDIA Quadro P4000 (§6.2, §6.3, §7). Roles from the methods section.
- **model(s):** SSD MobileNet (TensorFlow, converted to TFLite) (§4.2, §6.3). Pre-trained SSD MobileNet fine-tuned on four classes.
- **inference location:** On the smartphone (§6.3, §7). Local TFLite inference on the phone.
- **adaptation mechanism:** None (§4-§6). No runtime adaptation.
- **resource signals:** None used at runtime (§4.2). Speed/accuracy trade-off considered only when selecting the model.
- **evaluation metrics:** Recall, precision, accuracy per class at IoU 0.6 (§3, Table 1)
- **limitations:** Small training set and low-resolution crack images limit crack detection; larger datasets and higher resolution need more compute (§7, §8). Stated by the authors.
- **deployment setting:** Android app on sample images and live camera video; no field study described (§7)
- **Observation:** §7 text and Table 1 disagree on stain precision (0.95 vs 0.85).

### Conflicts with abstract-level coding

- `edge_device`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `on_device`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `accuracy_metrics`: (blank) → Per class at IoU 0.6 (Table 1), recall/precision/accuracy: crack 0.4/0.53/0.61; deterioration 0.68/0.68/0.83; mould 0.85/0.66/0.81; stain 0.71/0.85/0.95 (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P002 — A Road Defect Detection System Using Smartphones

### Source
Publisher full-text HTML, MDPI Sensors (CC BY) — https://www.mdpi.com/1424-8220/24/7/2099 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (Sensors 24(7):2099; HTML). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Yes | Yes | Confirmed | §3.1.1, §4.1 — An Android app on three phones (Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7) records 3-axis accelerometer data at 100 Hz. The phone is used as a vibration sensor, not as a camera. |
| edge_device | Unknown | Unknown | Ambiguous | §4.3, §5 — Conclusions state classification runs in real time on local smartphones, and models were quantized to reduce load on phones. The text does not describe running or timing the CNN on a named phone. |
| on_device | Unknown | Unknown | Ambiguous | §4.3, §5 — Same as edge_device: real-time on-phone classification is stated as the scope, but no on-device execution or benchmark is described. |
| cloud | Unknown | No | Confirmed | §5 — A cloud server for a live defect map is future work only. |
| adaptive_inference | Unknown | No | Confirmed | keyword search of full text + methods/results read — Fixed models; the sliding window changes how often tests run, not the model computation. |
| resource_awareness | Unknown | No | Confirmed | §4.3 — Quantization to lighten models for phones is design-time lightweighting, not a resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | §3.1, §3.2 — Input modality is a 1-D accelerometer time series, not imaging. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | Unknown | Ambiguous | §3.1.2 — In the automatic labelling pipeline, a dashcam sample is kept only if at least 90% of 30 YOLOv5m frame classifications agree. This is a consistency vote used to build the dataset, not a confidence score acting on the deployed classifier. Whether this counts needs a decision. |
| anomaly_detection | Unknown | No | Confirmed | §3.2, §4.3 — Supervised classification of speed bumps, manholes and potholes. |
| latency_evaluation | Unknown | Unknown | Ambiguous | §4.3 Fig. 9, §5 — Average processing time per minute of test data is reported (about 0.1 s per minute of driving), but the hardware on which it was measured is not stated (README §7.3 requires stated or identifiable hardware). |
| accuracy_metrics | (blank) | RDD-CNN accuracy reported as exceeding 86.77% (Conclusions); speed bump vs no-defect discrimination 99% (Fig. 7); automatic data collection missed 15.21% of data with 100% label accuracy (Conclusions) | Confirmed | §4.3, §5 — Wording of the 86.77% figure ("exceeding ... compared to other models") is ambiguous; per-model values are in Fig. 8. |
| efficiency_metrics | (blank) | Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving data (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB | Confirmed | §4.1, §4.3, §5 —  |

### Other evidence

- **paper type:** system/method (§3-§5)
- **application/domain:** Road defect classification from smartphone accelerometer (vibration) signals; dashcam video used only for automatic labelling. Not image-based inspection (§3.1, §3.2). Input modality is vibration. Relevance to smartphone visual inspection is a researcher decision.
- **dataset:** Self-collected: 20 h / 300 km driving (training) and 8 h / 120 km (test) in Cheongju; 576 speed bumps, 290 manholes, 271 potholes after preprocessing; 1,137 automatically vs 1,287 manually labelled samples (§4.1, §4.3)
- **hardware/device:** Acquisition: Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7 accelerometers; INAVI QHD5000 dashcam (labelling only). Processing: Linux/Python environment (device not stated) (§4.1)
- **model(s):** RDD-CNN (1D-CNN); YOLOv5m for automatic labelling; SVM, Random Forest, LSTM compared (§3.1.2, §3.2, §4.3)
- **inference location:** Stated as local smartphones in the conclusions; execution not described (§5)
- **adaptation mechanism:** None (keyword search of full text + methods/results read)
- **resource signals:** None (keyword search of full text + methods/results read)
- **evaluation metrics:** Accuracy, confusion matrices, processing time, model size (§4.3)
- **limitations:** Threshold-based segmentation misses mild defects that cause little vibration; accuracy depends on phone placement in the vehicle (§4.2, §4.3 Table 7). Stated by the authors.
- **deployment setting:** Two vehicles driving public roads around Cheongju, South Korea (§4.1)
- **Observation:** **Not image-based:** the deployed model classifies smartphone accelerometer signals; dashcam images are used only to label training data automatically.
- **Observation:** Relevance to smartphone *visual* inspection is low. The proposed class A is a researcher decision and is not changed here.

### Conflicts with abstract-level coding

- `edge_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `on_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `accuracy_metrics`: (blank) → RDD-CNN accuracy reported as exceeding 86.77% (Conclusions); speed bump vs no-defect discrimination 99% (Fig. 7); automatic data collection missed 15.21% of data with 100% label accuracy (Conclusions) (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving data (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Needs researcher decision.** Not an image-based inspection paper (accelerometer input). The researcher should decide whether the proposed class A still applies. Field-level candidate changes are listed in the conflicts file.

## P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

### Source
Publisher full-text HTML, Wiley Online Library / Hindawi (open access) — https://onlinelibrary.wiley.com/doi/full/10.1155/2022/9221211 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (Adv. Civil Eng. 2022, 9221211; HTML). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | No | No | Confirmed | §2.2.4, §3.7 — Hardware is an OAK-D kit on a Raspberry Pi; no smartphone role. |
| edge_device | Yes | Yes | Confirmed | §2.2.4, §3.7 — Models are converted to OpenVINO blobs and run on the OAK-D (Myriad X VPU) with a Raspberry Pi host. |
| on_device | Yes | Yes | Confirmed | §2.2.4, §3.7 — Inference runs on the OAK-D camera kit attached to the Raspberry Pi host, mounted on the vehicle dashboard. |
| cloud | Unknown | No | Confirmed | §2, §3 — No cloud processing; training on a local workstation. |
| adaptive_inference | Unknown | No | Confirmed | keyword search of full text + methods/results read — Fixed detectors. |
| resource_awareness | Unknown | No | Confirmed | keyword search of full text + methods/results read — No resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | §2.2.4 — OAK-D has stereo cameras, but detection uses the single RGB camera; no multi-view inspection. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | §3.4, §3.7 — Confidence thresholds only filter detections; no downstream action (recapture, referral, fallback) is triggered. |
| anomaly_detection | Unknown | No | Confirmed | §3.2 — Supervised single-class pothole detection. |
| latency_evaluation | Yes | Yes | Confirmed | Table 1, Table 3, §3.7 — latency type: throughput/FPS on OAK-D (Table 3, e.g. Tiny-YOLOv4 31.76 FPS) and inference latency per image (Table 1; hardware not stated, likely the training workstation). |
| accuracy_metrics | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | Confirmed | Table 1, Table 3 — Matches the current value. Table 1 also gives precision/recall/F1 per model. |
| efficiency_metrics | Tiny-YOLOv4 31.76 FPS on OAK-D | On OAK-D (Table 3): Tiny-YOLOv4 31.76 FPS, SSD-MobileNetv2 26.65 FPS, YOLOv5 18.25 FPS, YOLOv2 3.20 FPS, YOLOv3 2.39 FPS, YOLOv4 1.98 FPS. Inference time per image (Table 1, hardware not stated): Tiny-YOLOv4 4.86 ms, SSD-MobileNetv2 7 ms, YOLOv5 10 ms, YOLOv2 33.7 ms, YOLOv4 52.51 ms, YOLOv3 70.57 ms, YOLOv1 340 ms | Confirmed | Table 1, Table 3 — Extends the current single-value entry. |

### Other evidence

- **paper type:** system/method (§1-§4)
- **application/domain:** Real-time pothole detection from a vehicle-mounted edge AI camera (§1, §3.7)
- **dataset:** Public pothole image dataset (PID) stated as 665 images (~8,000 potholes); the train/test split is given as 1,066/264 images (internal inconsistency); real-time video from a moving vehicle (§2.1, §3.3, §3.7). Inconsistent counts in the paper.
- **hardware/device:** Inference: OAK-D (Myriad X VPU) with Raspberry Pi host; Training: Intel Xeon 3.0 GHz, 64 GB RAM, NVIDIA Titan Xp (§2.2.4, §3.3)
- **model(s):** YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetv2 (§2.2, Table 1). Matches current value.
- **inference location:** On the OAK-D attached to the Raspberry Pi host (§2.2.4)
- **adaptation mechanism:** None (keyword search of full text + methods/results read)
- **resource signals:** None (keyword search of full text + methods/results read)
- **evaluation metrics:** Precision, recall, F1, mAP@0.5, inference time per image, real-time detection accuracy and FPS (§3.4, Tables 1 and 3). The text sets the IoU threshold to 0.3 while tables report mAP@0.5 (internal inconsistency).
- **limitations:** YOLOv5 and SSD-MobileNetv2 miss distant potholes; accuracy limitations in real-time deployment; the real-time test covers 10 potholes (§3.6, §3.7, §4). Partly stated by the authors; test size from Table 3.
- **deployment setting:** OAK-D on the dashboard of a vehicle at 65 km/h; three locations and distance ranges (§3.7)
- **Observation:** Publisher page lists five authors (adds Afaq Ahmad); papers.csv and the registry record checked in the audit list four. Needs a metadata check; not changed.
- **Observation:** Dataset stated as 665 images, while the split is given as 1,066 train / 264 test images.
- **Observation:** Text sets the IoU threshold to 0.3 while tables report mAP@0.5.

### Conflicts with abstract-level coding

- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: Tiny-YOLOv4 31.76 FPS on OAK-D → On OAK-D (Table 3): Tiny-YOLOv4 31.76 FPS, SSD-MobileNetv2 26.65 FPS, YOLOv5 18.25 FPS, YOLOv2 3.20 FPS, YOLOv3 2.39 FPS, YOLOv4 1.98 FPS. Inference time per image (Table 1, hardware not stated): Tiny-YOLOv4 4.86 ms, SSD-MobileNetv2 7 ms, YOLOv5 10 ms, YOLOv2 33.7 ms, YOLOv4 52.51 ms, YOLOv3 70.57 ms, YOLOv1 340 ms (extends free text; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

### Source
arXiv preprint 2407.11771v2 (25 Oct 2024) — https://arxiv.org/abs/2407.11771 (accessed 2026-10-04). Status: **Partially verified**.

### Version
Author preprint (arXiv v2); published version is Information Fusion 2025 (10.1016/j.inffus.2024.102782). May differ from the published version: Possibly; preprint not compared with the version of record (ScienceDirect bot check).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §5.5.1, §5.5.2, Fig. 7 (pp. 13-15) — Mobile model optimised for smartphones; app built for Android and iOS; iOS interface designed for an iPhone 11 Pro. |
| edge_device | Yes | Yes | Confirmed | §5.5, §6.5 — Quantized and pruned model deployed on mobile devices. |
| on_device | Yes | Yes | Confirmed | §5.5.2 (p. 14) — Segmentation is produced by the mobile model inside the app on the device. |
| cloud | Unknown | Yes | Confirmed | §4 module 6, §5.6, Fig. 4 (pp. 9-14) — Textual explanations are generated by calling the GPT-4 Vision API (a remote large vision-language model). Cloud mode: cloud-assisted (explanation step only); segmentation stays on the device. |
| adaptive_inference | Unknown | No | Confirmed | §5.5 — Static quantized/pruned model; no runtime adaptation. |
| resource_awareness | Unknown | No | Confirmed | §5.5.1 — Quantization and pruning are design-time lightweighting with no explicit device budget or resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | §6.1, §7.1 — Single images from aerial and handheld/AGV cameras; no joint use of multiple views. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation ("confidence" appears only as user trust). |
| confidence_gating | Unknown | No | Confirmed | keyword search of full text + methods/results read — No action triggered by a confidence score. |
| anomaly_detection | Unknown | No | Confirmed | §5 — Supervised semantic segmentation. |
| latency_evaluation | Unknown | Unknown | Ambiguous | Table 4, §8.3 — No segmentation inference timing reported. Table 4 gives XAI-method running times in seconds without stated hardware; the authors list explanation latency on edge devices as a limitation. |
| accuracy_metrics | (blank) | TTPLA mIoU (Table 3): DLv3P-MobileNetv2 mobile 75.48%; DLv3P-ResNet101 enhanced 86.35%, mobile 83.95% | Confirmed | Table 3 (p. 17), §6.5 —  |
| efficiency_metrics | (blank) | Model size (Table 3): DLv3P-MobileNetv2 mobile 3.51M parameters / 13.39 MB; DLv3P-ResNet101 mobile 36.57M / 139.52 MB vs base 45.66M / 174.21 MB | Confirmed | Table 3 (p. 17) —  |

### Other evidence

- **paper type:** system/method (§4-§9)
- **application/domain:** Visual inspection of power-grid assets (transmission towers, power lines, substation equipment) with explainable segmentation; not manufactured parts (§6.1, §7.1)
- **dataset:** TTPLA (1,242 aerial images, 4 classes); Substation Equipment dataset (1,660 images, 15 classes) (§6.1, §7.1)
- **hardware/device:** Inference: smartphones via Android/iOS app (iOS UI designed for iPhone 11 Pro); Explanation: GPT-4 Vision API; Training hardware not stated (§5.5.2, §5.6, Fig. 7)
- **model(s):** DeepLabv3+ (MobileNetV2, ResNet50, ResNet101 backbones); 10 XAI methods (RISE selected); GPT-4 Vision for text (§4, §5)
- **inference location:** Segmentation on device; explanation text via remote API (§5.5.2, §5.6)
- **adaptation mechanism:** None at runtime (XAI-guided data augmentation is a training-time step) (§4)
- **resource signals:** None (keyword search of full text + methods/results read)
- **evaluation metrics:** mIoU / per-class IoU; XAI plausibility (EBPG, IoU, Bbox) and faithfulness (deletion, insertion); model size (§5, Tables 3-4)
- **limitations:** Annotation augmentation needs expert manual effort; generating textual explanations on edge devices may add latency and overhead; generalisation to other domains untested (§8.3 (p. 25)). Stated by the authors.
- **deployment setting:** Mobile app for field engineers; evaluated on public datasets; no field study timing (§5.5.2, §6)
- **Observation:** Verified against the arXiv v2 preprint; the Information Fusion version was not compared.
- **Observation:** Mobile-model accuracy (Table 3) may have been computed off-device; the text does not say where it was measured.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `accuracy_metrics`: (blank) → TTPLA mIoU (Table 3): DLv3P-MobileNetv2 mobile 75.48%; DLv3P-ResNet101 enhanced 86.35%, mobile 83.95% (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → Model size (Table 3): DLv3P-MobileNetv2 mobile 3.51M parameters / 13.39 MB; DLv3P-ResNet101 mobile 36.57M / 139.52 MB vs base 45.66M / 174.21 MB (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

### Source
Publisher PDF, Nature Communications (CC BY) — https://www.nature.com/articles/s41467-022-31985-y.pdf (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (Nat. Commun. 13:4654, 2022). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | Methods (p. 10) — Logitech C270 webcams and Raspberry Pi cameras; no smartphone. |
| edge_device | Unknown | No | Confirmed | Online correction (p. 6); Computing requirements (p. 11) — Images are sent to a local server for inference; the final models ran on a workstation with two NVIDIA Quadro RTX 5000 GPUs, which was also used for online correction. The Raspberry Pi is only a networked gateway. |
| on_device | Unknown | No | Confirmed | p. 6, p. 11 — Inference runs on the local server, not on the capture device. |
| cloud | Unknown | No | Confirmed | p. 6, p. 11 — Local server; no remote cloud processing described. |
| adaptive_inference | Unknown | No | Confirmed | Online correction pipeline (p. 6) — Fixed network; the control loop adapts printer parameters, not inference (README §7.3). |
| resource_awareness | Unknown | No | Confirmed | full text — No resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | full text — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | full text — Hotend temperature is a printing parameter being corrected, not a device thermal measurement. |
| multi_view | Unknown | No | Confirmed | Methods (p. 10), Discussion (p. 10) — A single nozzle-facing camera; combining with a global camera is suggested as future work. |
| uncertainty | Unknown | No | Confirmed | full text — No uncertainty estimation. |
| confidence_gating | Unknown | Unknown | Ambiguous | Fig. 3, Online correction pipeline (p. 6) — Predictions are stored in lists of length L; a correction is made only if one prediction reaches the mode-threshold share of the list, and that share scales the adjustment. This is a vote frequency over repeated predictions rather than a model confidence score; whether it counts needs a decision. |
| anomaly_detection | Unknown | No | Confirmed | Network architecture section, Fig. 2 — Supervised multi-head classification of parameter deviation (too low/good/too high). |
| latency_evaluation | Unknown | Unknown | Ambiguous | p. 6, Methods (p. 10) — Images are captured at 2.5 Hz and correction speed is discussed, but no inference timing on stated hardware was found in the sections read. |
| accuracy_metrics | (blank) | Test accuracy across four parameters 84.3% (attention multi-head network; Table 1); single-stage ResNet18-101 baselines 80.4-82.5%; flow-rate accuracy 82.1% multi-head vs 77.5% single-head | Confirmed | Table 1 and Methods (p. 11) —  |
| efficiency_metrics | (blank) | (blank) | Confirmed | full text — No efficiency measurement reported. |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Error detection and closed-loop correction in material-extrusion 3D printing from nozzle images (Introduction)
- **dataset:** CAXTON dataset: 1,272,273 raw images, 946,283 after cleaning, from 192 prints on eight Creality CR-20 Pro printers (PLA), labelled with printing parameters (Dataset generation, filtering and augmentation section). Refines the current value.
- **hardware/device:** Inference and training: workstation with 2x NVIDIA Quadro RTX 5000 and i9-9900K; Acquisition: Logitech C270 webcam per printer (Raspberry Pi Camera v1 on unseen setups); Gateway: Raspberry Pi 4 Model B (Methods (pp. 10-11))
- **model(s):** Multi-head residual attention network (shared backbone, four heads) (Network architecture section, Fig. 2)
- **inference location:** Local server (workstation) (p. 6, p. 11)
- **adaptation mechanism:** None in inference; printer parameters corrected by a feedback loop (p. 6)
- **resource signals:** None (full text)
- **evaluation metrics:** Classification accuracy per parameter; qualitative correction demonstrations (Table 1, Figs. 4-5)
- **limitations:** Weakness for small Z-offset changes; dataset bias; mechanical and electrical failures and large errors (cracking, warping, detachment) not solved; correction oscillations possible (Discussion (p. 10)). Stated by the authors.
- **deployment setting:** Lab printers including unseen printers (Lulzbot Taz 6, modified Ender 3 Pro for direct ink writing) (Figs. 4-5 and text; Methods (p. 10))
- **Observation:** Version of record; page numbers are printed article pages.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `edge_device`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `on_device`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `accuracy_metrics`: (blank) → Test accuracy across four parameters 84.3% (attention multi-head network; Table 1); single-stage ResNet18-101 baselines 80.4-82.5%; flow-rate accuracy 82.1% multi-head vs 77.5% single-head (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

### Source
Publisher full-text HTML, MDPI Processes (CC BY) — https://www.mdpi.com/2227-9717/8/11/1464 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (Processes 8(11):1464; HTML). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §3 — Raspberry Pi 4 with a camera; no smartphone. |
| edge_device | Unknown | Yes | Confirmed | §3 — The trained SSD model runs on a Raspberry Pi 4 with a connected camera, at the same frame rate as the earlier setup. |
| on_device | Unknown | Yes | Confirmed | §3 — Inference runs on the Raspberry Pi 4 with its attached camera placed in front of the print bed. |
| cloud | Unknown | No | Confirmed | §2.2, §3 — Training on a Tesla K80 GPU; live inference on the Raspberry Pi; no cloud processing. |
| adaptive_inference | Unknown | No | Confirmed | keyword search of full text + methods/results read — Fixed SSD-300 model. |
| resource_awareness | Unknown | No | Confirmed | §2.2 — SSD-300 chosen over SSD-512 for its published FPS: design-time choice, not a resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | §1.2, §3 — A single camera; the authors note that multiple angles add complexity. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — Probability scores are used for ranking and gating, but uncertainty is not estimated or calibrated. |
| confidence_gating | Unknown | Yes | Confirmed | §3 — A wrapper algorithm checks each frame; if the probability score of a predicted defect exceeds a predefined value, it notifies the user whether to stop the print. |
| anomaly_detection | Unknown | No | Confirmed | §2.1, §2.2 — Supervised SSD detector trained on annotated stringing images. |
| latency_evaluation | Unknown | Yes | Confirmed | §3 — latency type: throughput/FPS. The setup ran at 14 FPS on live video, and at the same rate on the Raspberry Pi 4. The 59 FPS in the conclusions is the published SSD-300 benchmark, not the authors' measurement. |
| accuracy_metrics | (blank) | Test set: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training set: precision 0.75, recall 0.92 | Confirmed | §3 —  |
| efficiency_metrics | (blank) | 14 FPS on live video, same rate reported on Raspberry Pi 4 | Confirmed | §3 —  |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Real-time stringing defect detection in FFF 3D printing with operator notification (Abstract, §3)
- **dataset:** 500 images of a stringing test object printed on a Prusa i3 MK3S, augmented to 2,500 images; PASCAL VOC annotations (§2.1)
- **hardware/device:** Inference: Raspberry Pi 4 with connected camera; Training: NVIDIA Tesla K80 (§2.2, §3)
- **model(s):** SSD-300 with VGG16 base network (TensorFlow Object Detection API) (§2.2)
- **inference location:** On the Raspberry Pi 4 next to the printer (§3)
- **adaptation mechanism:** None (keyword search of full text + methods/results read)
- **resource signals:** None (keyword search of full text + methods/results read)
- **evaluation metrics:** Precision, recall, F1, average precision at IoU 0.4-0.6; FPS (§2.3, §3)
- **limitations:** Poor generalisation to external web images; small, case-specific training set (one printer, few shapes) (§3, §4). Stated by the authors.
- **deployment setting:** Live remote monitoring of long prints on one printer, with shapes similar to the training data (§3)
- **Observation:** Conclusions cite 59 FPS, which is the published SSD-300 benchmark rather than the measured 14 FPS.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `edge_device`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `on_device`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `accuracy_metrics`: (blank) → Test set: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training set: precision 0.75, recall 0.92 (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → 14 FPS on live video, same rate reported on Raspberry Pi 4 (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

### Source
None obtained — https://doi.org/10.1016/j.promfg.2018.07.111 (accessed 2026-10-04). Status: **Blocked (inaccessible from this environment)**. Gold open access per OpenAlex/Semantic Scholar, but ScienceDirect served a bot check; not bypassed.

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

### Source
None obtained — https://doi.org/10.1007/s00170-024-14452-4 (accessed 2026-10-04). Status: **Blocked (abstract only)**. Subscription article; no legitimate open copy found (Step 9.1).

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P019 — Real-time defect detection in 3D printing using machine learning

### Source
None obtained — https://doi.org/10.1016/j.matpr.2020.10.482 (accessed 2026-10-04). Status: **Blocked (abstract only)**. Subscription article; no legitimate open copy found (Step 9.1).

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

### Source
Publisher full-text HTML, MDPI Applied System Innovation (CC BY) — https://www.mdpi.com/2571-5577/4/2/34 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record (ASI 4(2):34; HTML). May differ from the published version: No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §3, §4.1 — Raspberry Pi camera; no smartphone. |
| edge_device | Unknown | Unknown | Ambiguous | §3, §4.1, §5.4 — A Raspberry Pi 4B is described as "used for the processing" with a Pi camera and display, but all programming, training and testing were done in MATLAB. Where real-time classification runs is not stated. |
| on_device | Unknown | Unknown | Ambiguous | §3, §4.1, §5.4 — Same ambiguity as edge_device. |
| cloud | Unknown | No | Confirmed | keyword search of full text + methods/results read — No cloud processing described. |
| adaptive_inference | Unknown | No | Confirmed | keyword search of full text + methods/results read — Fixed feature extractor + classifier. |
| resource_awareness | Unknown | No | Confirmed | keyword search of full text + methods/results read — No resource-driven decision. |
| energy_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No energy or power measurement. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — Printing temperature is a process parameter, not a device thermal measurement. |
| multi_view | Unknown | No | Confirmed | §4.2, §5.4 — Four to five images per layer from one mounted camera are each classified individually; views are not used jointly. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | §3.3 — The ensemble uses a vote count to assign the final label; no downstream action is triggered by a confidence score. |
| anomaly_detection | Unknown | No | Confirmed | §3.4, §5 — Despite the "anomaly detection" wording, models are trained on manually labelled good and bad layer images (supervised; README §7.3, CD-14). |
| latency_evaluation | Unknown | Unknown | Confirmed | §5.4, §6 — "Less computational time" is claimed without a measured value (Decision 3). |
| accuracy_metrics | (blank) | AlexNet+SVM and EfficientNet-B0+SVM 99.70% (§5.1); ensemble with AlexNet features 100% (§5.2); density-wise classification ResNet50 100% (§5.3) | Confirmed | §5.1-§5.3, §6 — Second-best values differ between §5 and the conclusions (internal inconsistency). |
| efficiency_metrics | (blank) | (blank) | Confirmed | keyword search of full text + methods/results read — No efficiency measurement reported. |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Layer-wise fault detection in FDM printing from camera images (§3, §5.4)
- **dataset:** 1,700 layer images (good/bad) of a 25 x 25 x 5 mm cube, 32 parameter variants, Dreamer FDM printer (§4.2)
- **hardware/device:** Acquisition: 8MP Raspberry Pi camera; Processing: Raspberry Pi 4B (role in inference unclear); MATLAB used for programming, training and testing (§3, §4.1)
- **model(s):** Pre-trained CNN features (AlexNet, GoogLeNet, ResNet18/50, EfficientNet-b0) with SVM, KNN, Naive Bayes, Decision Tree, Random Forest; majority-vote ensemble (§3.2, §3.3). Matches the essence of the current value.
- **inference location:** Not stated (§3, §4.1)
- **adaptation mechanism:** None (keyword search of full text + methods/results read)
- **resource signals:** None (keyword search of full text + methods/results read)
- **evaluation metrics:** Accuracy, loss, confusion matrices (§5)
- **limitations:** None explicitly stated (§6)
- **deployment setting:** Lab FDM printer with mounted Raspberry Pi camera (§4.1)
- **Observation:** Second-best accuracy values differ between §5 and the conclusions.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `edge_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `on_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `accuracy_metrics`: (blank) → AlexNet+SVM and EfficientNet-B0+SVM 99.70% (§5.1); ensemble with AlexNet features 100% (§5.2); density-wise classification ResNet50 100% (§5.3) (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

### Source
None obtained — https://doi.org/10.1108/rpj-09-2024-0395 (accessed 2026-10-04). Status: **Blocked (abstract only)**. Subscription article; no legitimate open copy found (Step 9.1).

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

### Source
None obtained — https://doi.org/10.1016/j.mfglet.2019.09.005 (accessed 2026-10-04). Status: **Blocked (abstract only)**. Subscription article; no legitimate open copy found (Step 9.1).

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

### Source
arXiv preprint 1810.10090v1 (23 Oct 2018) — https://arxiv.org/abs/1810.10090 (accessed 2026-10-04). Status: **Partially verified**.

### Version
Author preprint carrying the MobiCom 2018 ACM copyright block; not confirmed identical to the ACM version of record. May differ from the published version: Possibly; not compared (ACM bot check).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §4.3.1 — Implemented on three smartphones (Samsung Galaxy S8, Galaxy S7, LG Nexus 5; Android 7.0); results reported for the Galaxy S8. |
| edge_device | Yes | Yes | Confirmed | §4.3.1 — Runs on the smartphones. |
| on_device | Yes | Yes | Confirmed | §4.3.1, §5 — On-device deep learning on the phones. |
| cloud | Unknown | No | Confirmed | §6 (Related Work) — The authors state the framework does not rely on cloud connectivity. |
| adaptive_inference | Yes | Yes | Confirmed | §3, §4.3.2 — Runtime selection among nested descendant models with different capacities. |
| resource_awareness | Yes | Yes | Confirmed | §3, §4.3.1 — Scheduler allocates runtime resources (e.g. 400 MB memory budget) and picks resource-accuracy trade-offs. |
| energy_evaluation | Yes | Yes | Confirmed | §4.3.1, §4.3.3, Figs. 8 and 11 — Power measured with a Monsoon power monitor; energy reductions reported. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | keyword search of full text + methods/results read — Image classification benchmarks; no multi-view. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | keyword search of full text + methods/results read — No confidence-triggered action. |
| anomaly_detection | Unknown | No | Confirmed | keyword search of full text + methods/results read — Supervised classification tasks. |
| latency_evaluation | Yes | Yes | Confirmed | §4.3.2, Fig. 10 — latency type: throughput/FPS (frame-rate speedup on the Galaxy S8). |
| accuracy_metrics | Up to +4.2% inference accuracy vs resource-agnostic baseline | Up to +4.2% inference accuracy vs resource-agnostic baseline | Confirmed | §4.3.2 — Supported: 4.1% (MinTotalCost) and 4.2% (MinMaxCost) at equal frame rate. |
| efficiency_metrics | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Confirmed | §4.3.2, §4.3.3 — Supported: 2.0x / 1.9x frame rate at equal accuracy; 1.7x / 1.5x energy reduction. |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Resource-aware multi-tenant on-device inference for continuous mobile vision (not inspection) (§1, §4.1)
- **dataset:** CIFAR-10, ImageNet-50, ImageNet-100, GTSRB, Adience-Gender, Places-32 (§4.1.1)
- **hardware/device:** Inference: Samsung Galaxy S8 (reported), Galaxy S7, LG Nexus 5 (Android 7.0); power: Monsoon power monitor (§4.3.1)
- **model(s):** NestDNN multi-capacity models built from VGG-16 and ResNet-50 (§4.1)
- **inference location:** On the smartphone (§4.3.1)
- **adaptation mechanism:** Runtime switching among nested descendant models (model switching / dynamic capacity) (§3)
- **resource signals:** Available memory and compute; number of concurrent applications (§3, §4.3.1)
- **evaluation metrics:** Accuracy gain, frame-rate speedup, energy, memory and model-switching cost (§4)
- **limitations:** Filter-importance (TRR) pruning has much higher computational cost than L1-norm pruning, raising the cost of generating multi-capacity models (§5). Stated by the authors.
- **deployment setting:** Benchmark emulating application launches and kills over 60 s simulations (§4.3.1)
- **Observation:** Verified against the arXiv v1 preprint that carries the MobiCom 2018 copyright block; the ACM version was not compared.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

### Source
arXiv preprint 2410.10847v1 (1 Oct 2024) — https://arxiv.org/abs/2410.10847 (accessed 2026-10-04). Status: **Partially verified**.

### Version
Author preprint carrying the DAC 2024 ACM copyright block; publisher version is closed access. May differ from the published version: Possibly; not compared (closed access).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Yes | Yes | Confirmed | §4.4 (p. 4), Table 2 (p. 5) — The Mi 11 Lite with a Snapdragon 780G is used; the Table 2 caption names it the Mi 11 Lite 5G. Earlier external verification (Step 8.3) stands. |
| edge_device | Yes | Yes | Confirmed | §4.4, §5 — Jetson Orin Nano and Mi 11 Lite 5G. |
| on_device | Yes | Yes | Confirmed | §5.1.2 (p. 5) — The two-stage detectors run on the devices. Note: the Lotus DRL agent itself runs on a desktop with an RTX 2080Ti and controls device frequencies over a socket (§4.4, p. 4). |
| cloud | Unknown | No | Confirmed | §4.4 (p. 4) — The off-device agent runs on a desktop machine over a socket, not on a cloud datacenter. |
| adaptive_inference | Unknown | No | Confirmed | §4.2-§4.4 (pp. 3-4) — Lotus scales CPU and GPU frequencies twice per frame via DRL; the detector models are unchanged. The two-width network belongs to the agent's Q-network, not the detector. The variable proposal count is an inherent property of the unmodified detectors. |
| resource_awareness | Yes | Yes | Confirmed | §4.3 (p. 4) — Agent state includes CPU/GPU temperature, frequency level and remaining time to the latency constraint. |
| energy_evaluation | Unknown | No | Confirmed | full text — Power is mentioned only as motivation; no energy or power results. |
| thermal_evaluation | Yes | Yes | Confirmed | §5.2, Figs. 4-7 (pp. 4-5) — Device temperatures are measured and compared with baselines. |
| multi_view | Unknown | No | Confirmed | full text — KITTI and VisDrone2019 detection; no multi-view inspection. |
| uncertainty | Unknown | No | Confirmed | full text — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | full text — No confidence-triggered action. |
| anomaly_detection | Unknown | No | Confirmed | full text — Object detection benchmarks. |
| latency_evaluation | Unknown | Yes | Confirmed | Tables 1-2 (pp. 4-5), §5.2.1 — latency type: inference latency (mean and standard deviation per image on Jetson Orin Nano and Mi 11 Lite 5G). |
| accuracy_metrics | (blank) | (blank) | Confirmed | full text — No detection accuracy is reported for Lotus (Fig. 1 mAP values are motivation for the baseline models). |
| efficiency_metrics | (blank) | Jetson Orin Nano, MaskRCNN on VisDrone2019: latency -30.8% vs default governor and -9.1% vs zTT; latency standard deviation -72.8% / -38.1%; latency-constraint satisfaction +35.9% / +24.8% (§5.2.1). Mi 11 Lite 5G: latency variation -29.4% / -9.5% for MaskRCNN on KITTI; satisfaction rate 92.5% for FasterRCNN on VisDrone2019. Lotus overhead 8.52 ms per inference | Confirmed | §4.4.2, §5.2.1 (pp. 4-5) — Absolute per-model latencies are in Tables 1-2. |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Thermal and latency-variation management for two-stage detectors on edge devices (autonomous-driving and drone datasets) (§1, §5.1.2)
- **dataset:** KITTI, VisDrone2019 (§5.1.2 (p. 5))
- **hardware/device:** Inference: NVIDIA Jetson Orin Nano; Xiaomi Mi 11 Lite 5G (Snapdragon 780G). DRL agent: desktop with NVIDIA RTX 2080Ti over socket (§4.4 (p. 4))
- **model(s):** Faster R-CNN, Mask R-CNN (detectors); DQN agent with a 4-layer MLP at two widths (§4.4.1, §5.1.2)
- **inference location:** Detector on device; frequency-control agent on a separate desktop (§4.4)
- **adaptation mechanism:** DRL-driven joint CPU/GPU DVFS, two decisions per frame (system-level) (§4.2-§4.3)
- **resource signals:** CPU/GPU temperature, CPU/GPU frequency level, remaining time to latency constraint, number of proposals (§4.3.2 (p. 4))
- **evaluation metrics:** Mean and standard deviation of latency, latency-constraint satisfaction rate, device temperature (§5, Tables 1-2)
- **limitations:** None explicitly stated (§6)
- **deployment setting:** Lab: 25 C indoor static environment; warm (25 C) and cold (0 C) zones; dataset switching (§5.2 (p. 5))
- **Observation:** The Lotus DRL agent runs off-device on a desktop RTX 2080Ti; only the detector runs on the phone/Jetson.
- **Observation:** Verified against the arXiv v1 preprint that carries the DAC 2024 copyright block; the publisher version is closed access.

### Conflicts with abstract-level coding

- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → Jetson Orin Nano, MaskRCNN on VisDrone2019: latency -30.8% vs default governor and -9.1% vs zTT; latency standard deviation -72.8% / -38.1%; latency-constraint satisfaction +35.9% / +24.8% (§5.2.1). Mi 11 Lite 5G: latency variation -29.4% / -9.5% for MaskRCNN on KITTI; satisfaction rate 92.5% for FasterRCNN on VisDrone2019. Lotus overhead 8.52 ms per inference (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

### Source
None obtained — http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-587035 (accessed 2026-10-04). Status: **Blocked (inaccessible from this environment)**. Only open copy listed is the Uppsala DiVA repository; it did not respond from this environment (network connection failed; browser navigation refused).

### Version
-. May differ from the published version: -.

### Evidence by characteristic
Not examined: no legitimate full text was available. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence
None.

### Conflicts with abstract-level coding
Cannot be assessed.

### Recommended action
**Insufficient evidence.** Obtain the full text (institutional access, interlibrary loan, or an author copy) before any recoding.

## P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

### Source
arXiv copy 2409.01089v1 with ACM TECS journal pagination — https://arxiv.org/abs/2409.01089 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Copy formatted as the published article (ACM TECS 23(4), Article 60, June 2024; pages 60:1-60:xx). May differ from the published version: Unlikely (journal layout), but not formally confirmed against the ACM page.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §6.3 (p. 60:19) — Evaluated on three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71. |
| edge_device | Yes | Yes | Confirmed | §6.3 — The smartphones above. |
| on_device | Yes | Yes | Confirmed | §6.3-§7 — On-device execution with TFLite on CPU/GPU/NPU/DSP. |
| cloud | Unknown | No | Confirmed | Fig. 2 (p. 60:15) — A server is used only for offline model conversion and evaluation; runtime inference is on the device. |
| adaptive_inference | Yes | Yes | Confirmed | §4.3.3, §7.2 (pp. 60:12-60:24) — The Runtime Manager switches model, processor or both at runtime. |
| resource_awareness | Yes | Yes | Confirmed | §4.3.2-§4.3.4, §7.2 — Switching is triggered by processor overload and memory pressure, using workload and memory signals. |
| energy_evaluation | Unknown | Unknown | Ambiguous | §4.1, §6.4 (p. 60:20), Fig. 2 — Energy is an objective and is profiled on the device, but no energy results were found in §7. |
| thermal_evaluation | Unknown | No | Confirmed | §4.3.2, §6.4, §7 (keyword search) — Overheating is discussed as a cause of processor issues and idle periods are used to keep temperatures consistent, but temperature is not measured or reported. |
| multi_view | Unknown | No | Confirmed | keyword search of full text + methods/results read — No multi-view. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | keyword search of full text + methods/results read — No confidence-triggered action. |
| anomaly_detection | Unknown | No | Confirmed | keyword search of full text + methods/results read — Supervised tasks. |
| latency_evaluation | Unknown | Yes | Confirmed | §6.4, §7.1-§7.2, Fig. 8 (pp. 60:20-60:24) — latency type: inference latency (average latency in ms per design) and throughput/FPS (images per second). |
| accuracy_metrics | (blank) | UC1 initial design on S20 (EfficientNet Lite0, FFX8, CPU): 75.11% accuracy; UC1 vs transferred baselines: +0.156 average accuracy | Confirmed | §7.1.2, §7.2.1 —  |
| efficiency_metrics | (blank) | Up to 4.06x over hardware-unaware multi-DNN designs; vs transferred baselines: UC1 +32.7% throughput, UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory footprint 16 MB | Confirmed | §7.1.2, §7.2.1 —  |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Constraint-aware runtime adaptation of single- and multi-DNN workloads on smartphones (not inspection) (§1, §6.2)
- **dataset:** Use cases covering image classification, scene recognition, face analysis, text classification and audio (YAMNet) (§6.2). Current value covers most tasks; audio use case not listed.
- **hardware/device:** Inference: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71 (CPU, GPU, NPU; DSP on A71) (§6.3)
- **model(s):** CARIn with the RASS solver; model suites including EfficientNet Lite variants and YAMNet (§4, §6.2, Table 8)
- **inference location:** On the smartphone (§6.3)
- **adaptation mechanism:** Model switching and processor switching from a precomputed design set (§4.3.3-§4.3.4)
- **resource signals:** Processor workload distribution and aggregate memory use (§4.3.4)
- **evaluation metrics:** Optimality, accuracy, latency (mean and standard deviation), throughput, memory, model size (§4.1, §7)
- **limitations:** Exhaustive on-device profiling is too costly for realistic deployment; generative models not evaluated (§8 (p. 60:26)). Stated by the authors.
- **deployment setting:** Lab evaluation on three phones with controlled runtime fluctuations (§6-§7)
- **Observation:** arXiv copy carries the ACM TECS journal pagination.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `accuracy_metrics`: (blank) → UC1 initial design on S20 (EfficientNet Lite0, FFX8, CPU): 75.11% accuracy; UC1 vs transferred baselines: +0.156 average accuracy (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → Up to 4.06x over hardware-unaware multi-DNN designs; vs transferred baselines: UC1 +32.7% throughput, UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory footprint 16 MB (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

### Source
FH JOANNEUM ePUB institutional repository PDF — https://epub.fh-joanneum.at/obvfhjoa/content/titleinfo/13393868/full.pdf (accessed 2026-10-04). Status: **Fully verified**.

### Version
Copy with IEEE TMC 25(1), Jan 2026 journal pagination (pp. 451-463); OpenAlex labels this repository copy "submittedVersion". May differ from the published version: Unlikely (journal layout), label conflict noted.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §VI (p. 461) — Evaluated on two mobile phones: Xiaomi Redmi Note 9 Pro and Google Pixel 6, using the TFLite benchmark tool on Android. |
| edge_device | Yes | Yes | Confirmed | §VI — Phones and IoT boards (Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2). |
| on_device | Yes | Yes | Confirmed | §VI — On-device inference and submodel switching measured. |
| cloud | Unknown | No | Confirmed | §VI, Acknowledgment — Computing clusters used only for training; no cloud inference. |
| adaptive_inference | Yes | Yes | Confirmed | §III, §VI — Nested subnetworks are switched at runtime under changing resource constraints. |
| resource_awareness | Yes | Yes | Confirmed | §I, §III — Subnetworks are chosen to fit dynamic resource constraints (MACs, peak memory). |
| energy_evaluation | Unknown | Yes | Confirmed | §VI, Table VI (p. 463) — Inference energy measured with a Power Profiler Kit (PPK2) on the Nordic nRF52840: 20-61 mJ for DS-CNN; switching < 0.01 mJ. |
| thermal_evaluation | Unknown | No | Confirmed | keyword search of full text + methods/results read — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | keyword search of full text + methods/results read — No multi-view. |
| uncertainty | Unknown | No | Confirmed | keyword search of full text + methods/results read — No uncertainty estimation. |
| confidence_gating | Unknown | No | Confirmed | §VI, Fig. 11 — Early-exit linear classifiers appear only as a comparison baseline; no confidence-triggered action in REDS. |
| anomaly_detection | Unknown | No | Confirmed | keyword search of full text + methods/results read — Supervised benchmark tasks. |
| latency_evaluation | Unknown | Yes | Confirmed | §VI, Fig. 10 (p. 462) — latency type: inference latency (inference time on phones via TFLite benchmark and on IoT boards; e.g. 2-layer FC network on Arduino Nano 33 BLE Sense: 2,131 +/- 27 us at 25% MACs and 4,548 +/- 13 us at 50% MACs). |
| accuracy_metrics | (blank) | (blank) | Confirmed | Figs. 5-11 — Accuracy results are given mainly in figures; no single value extracted. |
| efficiency_metrics | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | Adaptation time 38 +/- 1 us (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 +/- 27 us (25% MACs) and 4,548 +/- 13 us (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2) | Confirmed | §VI, Table VI (pp. 462-463) — The extracted PDF text drops the micro sign; microsecond units follow the abstract (adaptation time under 40 us). |

### Other evidence

- **paper type:** system/method (full text)
- **application/domain:** Resource-adaptive deep subnetworks for mobile and IoT devices (keyword spotting, visual wake words, image classification); not inspection (§I, §IV)
- **dataset:** Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K (Abstract, §IV). Matches current value.
- **hardware/device:** Inference: Xiaomi Redmi Note 9 Pro, Google Pixel 6, Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2; cache benchmark: Raspberry Pi Pico (RP2040) (§V-§VI)
- **model(s):** REDS subnetworks for DNN, CNN, DS-CNN and MobileNetV1-style architectures (iterative knapsack solver) (§III-§VI)
- **inference location:** On device (§VI)
- **adaptation mechanism:** Runtime switching among nested subnetworks (§III, §VI)
- **resource signals:** MACs, peak memory, available resources (§III)
- **evaluation metrics:** Accuracy, parameters, MACs, inference time, adaptation time, energy (§IV-§VI)
- **limitations:** Not tested for large language or multimodal models; cache optimisation for convolutions not explored; energy as a solver constraint left for future work (§VII (p. 463)). Stated by the authors (as future work).
- **deployment setting:** Lab benchmarks on phones and IoT boards (§VI)
- **Observation:** Repository copy carries the IEEE TMC journal pagination, although OpenAlex labels it "submittedVersion".

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `energy_evaluation`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Yes (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) → Adaptation time 38 +/- 1 us (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 +/- 27 us (25% MACs) and 4,548 +/- 13 us (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2) (extends free text; Confirmed; action: Change).

### Recommended action

**Candidate change.** Apply the listed candidate changes only after researcher/ChatGPT review; resolve Ambiguous rows first.

## P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

### Source
UTS institutional repository (OPUS) copy of the publisher PDF — https://opus.lib.uts.edu.au/handle/10453/147577 (accessed 2026-10-04). Status: **Fully verified**.

### Version
Publisher version of record PDF (Adv. Eng. Inform. 45 (2020) 101101; CC BY-NC-ND). May differ from the published version: No (publisher PDF).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Evidence (location — paraphrase) |
|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §4.2 (p. 7) — Edge hardware is an industrial PC; no smartphone. |
| edge_device | Unknown | Unknown | Ambiguous | §4.2 (p. 7) — Inference ("deployment") runs on an edge industrial PC with an Intel Celeron N2930 at the manufacturing line. Whether a low-power industrial PC counts as a resource-constrained edge device is the open industrial-PC question. |
| on_device | Unknown | Unknown | Ambiguous | §4.2 (p. 7) — The edge PC receives SPI data files over TCP/IP; it is not the capturing device or physically attached to it. Leaning No, but the case depends on the same open question. |
| cloud | Unknown | No | Confirmed | §4.2 (p. 7), §5 (p. 8) — Models are trained in a company-owned Spark cluster and data stored in AWS S3; inference runs on the edge device. Cloud used only for training and storage (README §7.3). |
| adaptive_inference | Unknown | No | Confirmed | §3, §4 — Static GBT model; "dynamic inspection" refers to routing parts, not to inference. |
| resource_awareness | Unknown | Unknown | Ambiguous | §3.4 (p. 5), §4.1 (p. 6) — GBT chosen over SVM because its scoring time was eight times faster with future scaling in mind; real-time constraint set by takt time. A deployment-time choice under a timing constraint: depends on the open design-time question. |
| energy_evaluation | Unknown | No | Confirmed | §3.4 — Energy constraints are listed in general terms; nothing is measured. |
| thermal_evaluation | Unknown | No | Confirmed | full text — No thermal measurement. |
| multi_view | Unknown | No | Confirmed | §4 — Inputs are numeric SPI features, not images. |
| uncertainty | Unknown | No | Confirmed | full text — No uncertainty estimation. |
| confidence_gating | Unknown | Unknown | Ambiguous | §3.3 (p. 5), §4.2 (p. 6) — Predicted class (with conservativeness tuning to avoid false negatives) decides which fields of view skip X-ray. No confidence score is described; whether a class-triggered routing decision counts needs a decision. |
| anomaly_detection | Unknown | No | Confirmed | §3.2, §4.1 — Supervised classifiers trained on X-ray labels. |
| latency_evaluation | Unknown | Yes | Ambiguous | Table 3 (p. 7), §4.2 (p. 7) — Scoring times per 1,000 rows (Table 3, hardware not stated) and processing of current test sets in under one minute on the Intel Celeron N2930 edge PC. latency type: end-to-end latency (coarse bound on stated hardware). |
| accuracy_metrics | (blank) | Initial balanced sample (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9%. Conservative GBT on solder joints (Table 4): class recall 98.8% (defective) / 86.4% (defect-free). FOV level (Table 5): average X-ray inspection volume reduced by about 29% | Confirmed | Tables 3-5 (p. 7) —  |
| efficiency_metrics | (blank) | Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets processed in < 1 min. Edge-cloud link: 2-150 ms latency, about 1 Mbit/s per line | Confirmed | Table 3, §4.2 (p. 7) —  |

### Other evidence

- **paper type:** system/method (industrial case study) (§3-§5)
- **application/domain:** Quality prediction for PCB solder joints in SMT assembly from numeric solder-paste-inspection (SPI) measurements, to reduce X-ray inspection volume. The ML input is not images (§1, §4 (pp. 1, 5-6)). Key relevance finding: not image-based inspection. Relevance class decision is the researcher's.
- **dataset:** Five months of SPI and X-ray records from one product variant at the Siemens Amberg plant; about 1.46 billion data points, ~0.0008% not OK; seven numeric SPI features (height, 2D/3D shape, surface, volume, X/Y offset) (§4 Table 2 (p. 6))
- **hardware/device:** Inference: industrial PC with Intel Celeron N2930 at the line; Training: company Spark cluster (up to 24 workstations); Storage: AWS S3 (§4.2 (p. 7))
- **model(s):** Gradient Boosted Tree (selected); Decision Tree, Naive Bayes, Logistic Regression, SVM compared (§4.1 (p. 6))
- **inference location:** Edge industrial PC at the manufacturing line (receives SPI files over TCP/IP) (§4.2 (p. 7))
- **adaptation mechanism:** None (full text)
- **resource signals:** Takt time and model scoring time (model selection only) (§3.4, §4.1)
- **evaluation metrics:** Accuracy, recall, precision, TPR/FPR, training and scoring time, inspection-volume reduction (§3.2, Tables 3-5)
- **limitations:** Deployment limited to one product variant, one line and the SPI and X-ray data sources (§4.3 (p. 7)). Stated by the authors.
- **deployment setting:** Siemens electronics plant, Amberg (Germany), SMT line with SPI and X-ray stations (§4 (p. 5))
- **Observation:** **Not image-based:** the model input is seven numeric SPI measurements per solder joint; images are not processed by the ML model. The SPI station itself is an optical inspection machine.
- **Observation:** Relevance to visual inspection is indirect. The proposed class D is not changed here.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `edge_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `on_device`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `cloud`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `adaptive_inference`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `resource_awareness`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `energy_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `thermal_evaluation`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `multi_view`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `uncertainty`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `confidence_gating`: Unknown → Unknown (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `anomaly_detection`: Unknown → No (resolves Unknown; Confirmed; action: Change).
- `latency_evaluation`: Unknown → Yes (resolves Unknown; Ambiguous; action: Needs researcher decision).
- `accuracy_metrics`: (blank) → Initial balanced sample (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9%. Conservative GBT on solder joints (Table 4): class recall 98.8% (defective) / 86.4% (defect-free). FOV level (Table 5): average X-ray inspection volume reduced by about 29% (resolves Unknown; Confirmed; action: Change).
- `efficiency_metrics`: (blank) → Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets processed in < 1 min. Edge-cloud link: 2-150 ms latency, about 1 Mbit/s per line (resolves Unknown; Confirmed; action: Change).

### Recommended action

**Needs researcher decision.** Not image-based (numeric SPI process data). The researcher should decide the relevance class and the open edge/industrial-PC questions. Field-level candidate changes are listed in the conflicts file.

