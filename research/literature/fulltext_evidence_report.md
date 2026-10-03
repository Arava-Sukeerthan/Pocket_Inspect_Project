# Full-Text Evidence Report (Step 9.2)

_2026-10-03, Claude Code. Evidence collection only: **`papers.csv` was not modified**, relevance classes are unchanged, and no gap analysis was performed. Coding follows [`README.md` §7 v1.1](README.md#7-literature-coding-definitions). Field-by-field tables, including the contextual items, are in [`fulltext_verification_template.md`](fulltext_verification_template.md); every proposed change is listed in [`fulltext_conflicts.md`](fulltext_conflicts.md); access status is in [`fulltext_verification_status.md`](fulltext_verification_status.md)._

**Conventions**

- **Relevance classes** (A–E, from `audit_report.csv`) are *proposed auditor classifications*, not approved classes. The queue is the 17 proposed class-A papers plus P013 (proposed class D). No class was changed.
- **Quotations** are short and copied from the source text read in this session. Everything else is a paraphrase.
- **Page numbers** are given only where the source has printed page numbers and the page break was clear. PMC and HTML sources are cited by section heading.
- **`full text read; no occurrence`** means the whole text was read and the characteristic does not occur.
- **Confidence:** Confirmed / Not supported / Ambiguous.
- **Recommended action:** Keep current value / Candidate change / Needs researcher decision / Insufficient evidence. Candidate changes are **not applied**; they need researcher/ChatGPT approval and a separate recoding step (README §7.7).
- **Earlier attempt.** An earlier Claude Code session pushed a Step 9.2 attempt as commit `9643e43` on the unmerged branch `claude/pocketinspect-agent-sync-a33d88`. This report was produced independently from the sources read in this session. That commit was used only as a checklist of points to re-check. Where this session could not reach a source (P001, P007), none of the earlier evidence is adopted here. Differences from that attempt are listed in the status file.

**Access route used in this session.** Direct publisher access is blocked by this environment's network policy. Full texts were read through the PubMed Central full-text service (P002, P015), the alphaXiv full-text service for arXiv papers (P011, P029, P031, P033), and the alphaXiv document reader for open-access PDFs on publisher or institutional hosts (P013, P016, P020, P034). No pirated or unauthorised copies were used. Bot checks were not bypassed.

## P001 — Deep learning smartphone application for real‐time detection of defects in buildings

### Source

None obtained. **Status: Blocked (inaccessible from this environment).** Open access (Wiley, CC BY-NC; Semantic Scholar/OpenAlex list https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/stc.2751), but Wiley Online Library could not be fetched from this environment (egress policy and fetch failures).

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- The earlier attempt (commit `9643e43`) recorded publisher-HTML evidence for this paper. This session could not reach the source, so that evidence was **not re-verified and is not adopted**. A later session with access should re-check it.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P002 — A Road Defect Detection System Using Smartphones

### Source

- **Status:** Fully verified
- **Source used:** PubMed Central full text of the published article (PMC11014122), retrieved through the PubMed full-text service
- **URL / identifier:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11014122/ (DOI 10.3390/s24072099)
- **Accessed:** 2026-10-03
- **Parts read:** All running text read (Introduction to Conclusions). Tables and figures not available in the extraction.

### Version

- **Version:** Publisher version of record as deposited in PMC (Sensors 2024, 24(7), 2099; CC BY)
- **Version type:** publisher version
- **May differ materially from the published version:** No (version of record). The PMC text extraction omits table bodies, figure images and figure/table numbers, so evidence is cited by section heading; values that exist only inside tables or figures were not seen.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | Confirmed | §3.1.1; §4.1 | An Android app records 3-axis accelerometer data at 100 Hz on three phones (Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7). The phone is the sensing device; its camera is not used. | Keep current value |
| edge_device | Unknown | Unknown | Ambiguous | §3.2 (last paragraph); §4.1; §5 | The quantized RDD-CNN is converted with the TFLite Converter and is "designed for execution on smartphones"; the conclusions state the scope is real-time classification on local smartphones. No on-phone run or on-phone timing is described. | Needs researcher decision |
| on_device | Unknown | Unknown | Ambiguous | §3.2; §4.1; §5 | Same evidence as edge_device: on-phone execution is stated as intended and as the scope, but not described as executed or measured. | Needs researcher decision |
| cloud | Unknown | No | Confirmed | §5 | A cloud server for a live defect map is future work only; no cloud processing in the evaluated system. | Candidate change |
| adaptive_inference | Unknown | Unknown | Ambiguous | §3.2 (Algorithm 1); §4.3 | The RDD-CNN is fixed. A sliding window (3 s, 0.1 s stride) jumps ahead after a detection, so the number of tests per minute depends on the input. This changes how often the model is invoked, not the model's computation; whether such stream-level skipping counts is not covered by the §7.3 table. Leaning No. | Needs researcher decision |
| resource_awareness | Unknown | No | Confirmed | §3.2; §4.3 | 32-bit to 16-bit quantization lightens the model for phones (59.11% smaller). Design-time lightweighting with no stated device budget or runtime resource signal. | Candidate change |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No energy, power or battery result. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No temperature or throttling measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §3.2; §4.1 | The deployed input is a 300x1 accelerometer RMS series. Dashcam video (front/rear) is used only to label training data. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation or calibration. | Candidate change |
| confidence_gating | Unknown | Unknown | Ambiguous | §3.1.2; §4.2 | Label quality verifier: a sliced sample is kept only if at least 90% of its 30 YOLOv5m frame classifications agree; otherwise it is discarded. This is a vote-consistency gate during dataset construction, not a confidence score acting on the deployed classifier. | Needs researcher decision |
| anomaly_detection | Unknown | No | Confirmed | §3.2; §4.3 | Supervised classification of speed bumps, manholes and potholes from labelled data. | Candidate change |
| latency_evaluation | Unknown | Unknown | Ambiguous | §4.1; §4.3; §5 | Average time per model to evaluate 1 min of test data is reported (about 0.1 s per minute of driving for RDD-CNN), but the hardware used for the timing is not stated; preprocessing ran in a Linux/Python 3.8.10 environment. README §7.3 requires stated or identifiable hardware. | Needs researcher decision |
| accuracy_metrics | (blank) | RDD-CNN accuracy stated as "exceeding 86.77%" vs other models (§5); speed bump vs no-defect 99% (§4.3); YOLOv5m labeller 95.17% average per image (§4.2); automatic collection missed 15.21% of data with 100% label accuracy (§5) | Confirmed | §4.2; §4.3; §5 | Values as stated in the running text; per-model accuracies are in a figure not visible in the extraction. | Candidate change |
| efficiency_metrics | (blank) | Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB | Confirmed | §4.1; §4.3; §5 | Values as stated in the running text. | Candidate change |

### Other evidence

- **paper type:** system/method (§3-§5). Proposes an automatic data-collection system and the RDD-CNN classifier and evaluates both.
- **application/domain:** Road defect classification (speed bump, manhole, pothole) from smartphone accelerometer (vibration) signals in moving vehicles. Not image-based inspection. (§1 (last paragraph); §3). "a road defect detection system based on vibration sensors, specifically accelerometers" (§1).
- **dataset:** Self-collected: 20 h / 300 km training drive and 8 h / 120 km test drive (Cheongju, Korea); 576 speed bumps, 290 manholes, 271 potholes after automatic labelling; 696 training / 300 test samples; YOLOv5m labeller trained on 3,000/3,500/4,000 images plus open data (§4.1; §4.3). Counts as stated.
- **hardware/device:** Acquisition: Samsung Galaxy Note8, Xiaomi Redmi Note 10 Pro, LG Q7 (accelerometer, 100 Hz); INAVI QHD5000 dashcam (labelling only). Processing: Linux/Python environment (machine not stated). TFLite model designed for the three phones (§4.1). Device list and roles as stated.
- **model(s):** RDD-CNN (1D-CNN, Swish, softmax; TFLite, 16-bit quantization); YOLOv5m for automatic labelling; SVM, Random Forest, LSTM baselines (§3.1.2; §3.2; §4.3).
- **inference location:** Stated as local smartphones (scope); not described as executed or measured on a phone (§3.2; §5). See on_device.
- **adaptation mechanism:** None in the model; sliding-window stride policy only (§3.2). See adaptive_inference.
- **resource signals:** None (full text read; no occurrence). No runtime resource signal.
- **evaluation metrics:** Accuracy, confusion matrices, discarded-data ratio, processing time per minute of data, model size (§4.2; §4.3).
- **limitations:** Threshold segmentation misses mild defects (painted speed bumps, shallow manholes/potholes); accuracy drops when the phone is in unstable places (cup holder, door pocket, clothes pocket); raw data limited to daytime, good weather, front dashcam (§4.2; §4.3). Stated by the authors.
- **deployment setting:** Two vehicles (YF Sonata, Kia All New Sportage) on public roads around Cheongju, South Korea (§4.1).
- **Observation:** **Not image-based.** The deployed classifier takes smartphone accelerometer signals. Dashcam images are used only to label training data automatically (YOLOv5m). The phone is a vibration sensor, not a camera.
- **Observation:** Internal inconsistency: the acceleration threshold is 12 m/s² in §4.1 and 11 m/s² in §4.2.
- **Observation:** Internal inconsistency: the automatic-vs-manual accuracy gap is about 1% in §4.3 and 0.4% in §5.
- **Observation:** Relevance to smartphone *visual* inspection is low. The proposed class A is a researcher decision and is not changed here.

### Conflicts with abstract-level coding

- `edge_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `on_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `resource_awareness`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Needs researcher decision.** Not an image-based inspection paper (accelerometer input). Relevance class A needs researcher review; it is not changed here. Field-level candidate changes are listed in the conflicts file.

## P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

### Source

None obtained. **Status: Blocked (inaccessible from this environment).** Open access (CC BY; listed PDF https://downloads.hindawi.com/journals/ace/2022/9221211.pdf), but neither Hindawi nor Wiley could be fetched from this environment.

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- The earlier attempt (commit `9643e43`) recorded publisher-HTML evidence for this paper. This session could not reach the source, so that evidence was **not re-verified and is not adopted**. A later session with access should re-check it.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

### Source

- **Status:** Partially verified
- **Source used:** arXiv preprint 2407.11771v2 (25 Oct 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2407.11771v2 (version of record: Information Fusion 2025, DOI 10.1016/j.inffus.2024.102782)
- **Accessed:** 2026-10-03
- **Parts read:** Full preprint text read (pp. 1-26 plus references). Page numbers are the preprint's own.

### Version

- **Version:** Author preprint (arXiv v2)
- **Version type:** preprint
- **May differ materially from the published version:** Possibly. The Information Fusion version of record was not accessible (ScienceDirect blocked) and was not compared.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §5.5.1-5.5.2, pp. 13-14; Fig. 7, p. 15 | The mobile model is converted for "smartphone devices"; an app is built for Android and iOS; field engineers capture images with the device camera; the iOS interface is designed for an iPhone 11 Pro. No on-phone measurement is reported. | Candidate change |
| edge_device | Yes | Yes | Confirmed | §5.5, pp. 13-14 | Quantized and pruned model deployed in the mobile app. | Keep current value |
| on_device | Yes | Yes | Confirmed | §5.5.2, p. 14; §5.6 | The mobile model performs semantic segmentation on the uploaded image inside the app. | Keep current value |
| cloud | Unknown | Unknown | Ambiguous | §4 (module 6); §5.6, p. 14; Fig. 4 | Textual explanations are generated by calling the GPT-4 Vision API, and Fig. 4 places the domain-expert web app in a "Cloud Environment". The segmentation (the inspection inference) stays on the device. Whether remote explanation generation counts as "inference or decision processing" under README §7.3 is open. | Needs researcher decision |
| adaptive_inference | Unknown | No | Confirmed | §5.5 | Static quantized and pruned model. | Candidate change |
| resource_awareness | Unknown | No | Confirmed | §5.5.1, pp. 13-14 | Dynamic int8 quantization and 10% structured channel pruning are design-time lightweighting with no device budget. | Candidate change |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No energy or power result ("Energy-Based Pointing Game" is an XAI metric). | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §6.1; §7.1 | Aerial images (TTPLA) and substation images from handheld, AGV-mounted and fixed cameras, each segmented on its own. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | "Confidence" refers to user trust; no uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | full text read; no occurrence | No action triggered by a confidence score. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §5.1 | Supervised semantic segmentation trained with Dice loss. | Candidate change |
| latency_evaluation | Unknown | Unknown | Ambiguous | Table 4 caption; §8.3, p. 25 | No inference timing is reported. The Table 4 caption mentions running time in seconds, but the table has no time column in the text read. §8.3 says explanation generation on edge devices "may introduce latency" (limitation). Leaning No. | Needs researcher decision |
| accuracy_metrics | (blank) | TTPLA validation mIoU (Table 3, p. 17), base/enhanced/mobile: MobileNetV2 77.18/77.82/75.48%; ResNet50 83.20/83.90/81.53%; ResNet101 84.97/86.35/83.95%. Substation validation mIoU (Table 6, p. 23), ResNet101: 73.45/75.79/72.58% | Confirmed | Table 3, p. 17; Table 6, p. 23 | As stated. | Candidate change |
| efficiency_metrics | (blank) | Model size (Table 3), base vs mobile: MobileNetV2 4.37M / 16.71 MB vs 3.51M / 13.39 MB; ResNet50 26.67M / 101.76 MB vs 21.36M / 81.48 MB; ResNet101 45.66M / 174.21 MB vs 36.57M / 139.52 MB | Confirmed | Table 3, p. 17 | As stated. | Candidate change |

### Other evidence

- **paper type:** system/method (§4-§9). Proposes and evaluates the framework.
- **application/domain:** Visual inspection of power-grid assets (transmission towers, power lines, substation equipment) with explainable segmentation and LVLM text explanations (§6.1; §7.1). Not manufactured parts.
- **dataset:** TTPLA (1,242 aerial images, 4 classes); Substation Equipment dataset (1,660 images, 15 categories, 50,705 objects; handheld, AGV-mounted and fixed cameras) (§6.1, p. 15; §7.1).
- **hardware/device:** Inference: smartphones through an Android/iOS app (iOS UI designed for iPhone 11 Pro). Explanations: GPT-4 Vision API. Training hardware not stated (§5.5.2; §5.6; Fig. 7). Roles as stated.
- **model(s):** DeepLabv3+ (MobileNetV2, ResNet50, ResNet101 backbones); 10 XAI methods (RISE selected); GPT-4 Vision; PyTorch dynamic quantization, 10% structured pruning, TorchScript mobile optimisation (§4; §5).
- **inference location:** Segmentation on the phone; explanation text through a remote API (§5.5.2; §5.6). See on_device / cloud.
- **adaptation mechanism:** None at runtime (XAI-guided annotation augmentation is a training step) (§4; §6.4).
- **resource signals:** None (full text read; no occurrence).
- **evaluation metrics:** mIoU and per-class IoU; XAI plausibility (EBPG, IoU, BBox) and faithfulness (deletion, insertion); model size (§5.4; Tables 3-4).
- **limitations:** Annotation augmentation needs expert manual effort; explanation generation on edge devices may add latency and overhead; generalisation to other domains untested (§8.3, p. 25). Stated by the authors.
- **deployment setting:** Mobile app for field engineers (UI demonstrated); evaluation on public datasets (§5.5.2; §6). No field study timing.
- **Observation:** Verified against the arXiv v2 preprint only; the Information Fusion version was not compared.
- **Observation:** Where the mobile-model mIoU (Table 3) was computed (on a phone or off-device) is not stated.
- **Observation:** Possible inconsistency: TTPLA is described with 8,987 instances (§6.1), while Table 2 object counts sum to more.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `resource_awareness`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed, subject to a check against the version of record; resolve the Ambiguous cloud and latency rows first.

## P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

### Source

- **Status:** Fully verified
- **Source used:** PubMed Central full text of the published article (PMC9378646), retrieved through the PubMed full-text service
- **URL / identifier:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9378646/ (DOI 10.1038/s41467-022-31985-y)
- **Accessed:** 2026-10-03
- **Parts read:** All running text read (Introduction, Results, Discussion, Methods). Tables, figures and supplementary information not examined.

### Version

- **Version:** Publisher version of record as deposited in PMC (Nature Communications 13:4654, 2022; CC BY)
- **Version type:** publisher version
- **May differ materially from the published version:** No (version of record). The PMC text extraction omits table bodies, figure images and figure numbers; Table 1 baseline values and figure content were not seen. Evidence is cited by section heading.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | Methods - CAXTON system | Logitech C270 USB webcams on Raspberry Pi 4 gateways; a Raspberry Pi Camera v1 on the direct-ink-writing printer. No phone. | Candidate change |
| edge_device | Unknown | No | Confirmed | Online correction and parameter discovery pipeline; Computing and software requirements | Images are sent to a local server for inference. The final models were trained on a workstation with two Quadro RTX 5000 GPUs, and "this setup was also used for the online correction". The Raspberry Pi only relays G-code commands and acknowledgements. | Candidate change |
| on_device | Unknown | No | Confirmed | Same as edge_device | Inference runs on the local server, not on the capture device. | Candidate change |
| cloud | Unknown | No | Confirmed | Online correction pipeline; Computing and software requirements | Local server; an HPC cluster was used only for prototyping/training. No remote cloud processing. | Candidate change |
| adaptive_inference | Unknown | No | Confirmed | Online correction and parameter discovery pipeline | Fixed network. The feedback loop adjusts printing parameters, which README §7.3 treats as process adaptation, not inference adaptation. | Candidate change |
| resource_awareness | Unknown | No | Confirmed | full text read; no occurrence | No resource-driven decision. The crop size is tuned for accuracy versus response time at setup, not at runtime. | Candidate change |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No energy or power result. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | Hotend temperature is a corrected printing parameter, not a device thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | Methods - CAXTON system; Discussion | One nozzle-facing camera per printer. Different camera positions occur only across different setups (generalisation tests), not as joint views of one object. Adding a global camera is future work. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | Unknown | Ambiguous | Online correction and parameter discovery pipeline | Predictions per parameter are stored in lists of length L; a correction is made only if one class reaches the mode-threshold share of the list, and that share scales the update. A vote frequency over repeated predictions, not a model confidence score. | Needs researcher decision |
| anomaly_detection | Unknown | No | Confirmed | Results - Dataset generation; Model architecture | Supervised three-class labels (low/good/high) per parameter, derived automatically from known printer settings. | Candidate change |
| latency_evaluation | Unknown | Unknown | Ambiguous | Online correction pipeline; Methods; Discussion | Images are captured at 2.5 Hz and an order-of-magnitude faster correction is claimed, but no inference timing on stated hardware appears in the running text. Figures and supplementary material were not available. | Insufficient evidence |
| accuracy_metrics | (blank) | Test accuracy 84.3% overall; per parameter: flow rate 87.1%, lateral speed 86.4%, Z offset 85.5%, hotend temperature 78.3%; flow-rate accuracy 77.5% single-head vs 82.1% multi-head (ResNet18, 50 epochs) | Confirmed | Results - Model architecture, training and performance; Methods - Training procedure | Values as stated in the running text. Table 1 baselines not visible in the extraction. | Candidate change |
| efficiency_metrics | (blank) | (blank) | Confirmed | full text read; no occurrence | No efficiency value in the running text. | Keep current value |

### Other evidence

- **paper type:** system/method (full text). Proposes and evaluates the CAXTON network and multi-head detector/corrector.
- **application/domain:** Error detection and closed-loop correction in material-extrusion 3D printing from nozzle-camera images (Introduction (last paragraph)).
- **dataset:** CAXTON: 1,272,273 images from 192 prints on eight Creality CR-20 Pro printers (PLA); 1,166,552 after removing failed prints; 946,283 after cleaning (74.4%); 81 class combinations; 0.7/0.2/0.1 split (Results - Dataset generation, filtering and augmentation; Methods - Training procedure). Refines the current "1.2 million images" value.
- **hardware/device:** Inference and training: workstation with 2x NVIDIA Quadro RTX 5000, i9-9900K, 64 GB RAM. Acquisition: Logitech C270 webcam (1280x720, 2.5 Hz) per printer. Gateway: Raspberry Pi 4 Model B with OctoPrint. Other setups: Raspberry Pi Camera v1 (DIW printer), Lulzbot Taz 6 (Methods - CAXTON system; Computing and software requirements). Roles as stated.
- **model(s):** Multi-head residual attention network (Attention-56-based shared backbone, four heads x three classes) (Results - Model architecture).
- **inference location:** Local server (workstation) (Online correction pipeline; Computing requirements). See edge_device.
- **adaptation mechanism:** None in inference; proportional printer-parameter updates via mode thresholding (Online correction pipeline). Process control, not inference adaptation.
- **resource signals:** None (full text read; no occurrence).
- **evaluation metrics:** Classification accuracy per parameter; qualitative correction demonstrations (Results).
- **limitations:** Weakness on small Z-offset changes and dataset bias; correction oscillations possible; mechanical/electrical failures and large errors (cracking, warping, detachment) not solved; local view only (Discussion). Stated by the authors.
- **deployment setting:** Lab printers, including unseen Lulzbot Taz 6 and a modified Ender 3 Pro for direct ink writing (Results; Methods).

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `edge_device`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `on_device`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `resource_awareness`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Unknown (Insufficient evidence; Ambiguous; Insufficient evidence).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed; resolve the Ambiguous confidence_gating row and the latency row (figures/supplement not examined) first.

## P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

### Source

- **Status:** Fully verified
- **Source used:** MDPI publisher PDF, served from MDPI's content host
- **URL / identifier:** https://mdpi-res.com/d_attachment/processes/processes-08-01464/article_deploy/processes-08-01464.pdf (DOI 10.3390/pr8111464)
- **Accessed:** 2026-10-03
- **Parts read:** Pages 1-14 read (all sections; reference list partially).

### Version

- **Version:** Publisher version of record (Processes 2020, 8, 1464; CC BY; pages 1-15 printed)
- **Version type:** publisher version
- **May differ materially from the published version:** No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §3, p. 12 | Raspberry Pi 4 with a connected camera; no phone. | Candidate change |
| edge_device | Unknown | Yes | Confirmed | §3, p. 12 | The model was deployed by running it on a Raspberry Pi 4 "with a connected camera" in front of the print bed. | Candidate change |
| on_device | Unknown | Yes | Confirmed | §3, p. 12 | Inference runs on the Raspberry Pi 4 to which the camera is attached. | Candidate change |
| cloud | Unknown | No | Confirmed | §2.2, p. 8; §3, p. 12 | Training on an NVIDIA Tesla K80; live inference on the Pi. No cloud processing. | Candidate change |
| adaptive_inference | Unknown | No | Confirmed | full text read; no occurrence | Fixed SSD-300 model. | Candidate change |
| resource_awareness | Unknown | No | Confirmed | §2.2, p. 7 | SSD-300 chosen over SSD-512 for its published FPS and low input resolution: a design-time choice, not a resource-driven decision. | Candidate change |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No energy or power result. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §3, p. 12; §1.2, p. 3 | A single camera. Multiple camera angles appear only in related work, where the authors note they add complexity. | Candidate change |
| uncertainty | Unknown | No | Confirmed | §2.3, p. 10; §3 | Probability scores are used for precision-recall ranking and for gating; no uncertainty estimation or calibration. | Candidate change |
| confidence_gating | Unknown | Yes | Confirmed | §3, pp. 12-13; §4, p. 13 | A wrapper algorithm checks each frame: if a predicted defect's probability score is "greater than a predefined value", the user is notified whether to stop the print (human referral). | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §2.1-2.2, p. 7 | Supervised SSD trained on 500 manually annotated stringing images. | Candidate change |
| latency_evaluation | Unknown | Yes | Confirmed | §3, p. 12; §2.2, p. 7 | latency type: throughput/FPS. The setup ran at 14 FPS on live video, and the model ran at the same FPS on the Raspberry Pi 4. The 59 FPS in §4 is the published SSD-300 benchmark (§2.2), not the authors' measurement. | Candidate change |
| accuracy_metrics | (blank) | Test: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training data: precision 0.75, recall 0.92 (F1 0.82) | Confirmed | §3, pp. 11-12 | As stated. | Candidate change |
| efficiency_metrics | (blank) | 14 FPS on live video; same FPS on Raspberry Pi 4 | Confirmed | §3, p. 12 | As stated. | Candidate change |

### Other evidence

- **paper type:** system/method (full text). Develops and deploys a stringing detector.
- **application/domain:** Real-time stringing detection in FFF 3D printing with operator notification (Abstract; §3).
- **dataset:** 500 images of a stringing test object (Prusa i3 MK3S), augmented x5 to 2,500; PASCAL VOC annotations (LabelImg) (§2.1, p. 7).
- **hardware/device:** Inference: Raspberry Pi 4 with connected camera. Training: NVIDIA Tesla K80 (12 GB) (§2.2, p. 8; §3, p. 12). Roles as stated.
- **model(s):** SSD-300 with VGG16 base network (TensorFlow Object Detection API) (§2.2, pp. 7-8).
- **inference location:** Raspberry Pi 4 next to the printer (§3, p. 12). See on_device.
- **adaptation mechanism:** None (full text read; no occurrence).
- **resource signals:** None (full text read; no occurrence).
- **evaluation metrics:** Precision, recall, F1, average precision at IoU 0.4-0.6; FPS (§2.3; §3).
- **limitations:** Poor generalisation to external web images; case-specific training data (few shapes, one printer); 500 images considered insufficient (§3, pp. 11-12). Stated by the authors.
- **deployment setting:** Remote monitoring of long prints on one printer, shapes similar to the training data (§3, p. 13).
- **Observation:** The conclusions cite 59 FPS, which is the published SSD-300 benchmark (§2.2), not the measured 14 FPS (§3).

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `edge_device`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `on_device`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `resource_awareness`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed (no Ambiguous core rows).

## P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

### Source

None obtained. **Status: Blocked (inaccessible from this environment).** Gold open access per Semantic Scholar (https://www.sciencedirect.com/science/article/pii/S2351978918307820/pdf, CC BY-NC-ND), but ScienceDirect could not be fetched; bot checks were not bypassed.

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

### Source

None obtained. **Status: Blocked (abstract only).** Subscription article (Springer IJAMT); no legitimate open copy known (Step 9.1).

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P019 — Real-time defect detection in 3D printing using machine learning

### Source

None obtained. **Status: Blocked (abstract only).** Subscription article (Elsevier Materials Today: Proceedings); no legitimate open copy known (Step 9.1).

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

### Source

- **Status:** Fully verified
- **Source used:** MDPI publisher PDF, served from MDPI's content host
- **URL / identifier:** https://mdpi-res.com/d_attachment/asi/asi-04-00034/article_deploy/asi-04-00034.pdf (DOI 10.3390/asi4020034)
- **Accessed:** 2026-10-03
- **Parts read:** Pages 1-20 read.

### Version

- **Version:** Publisher version of record (Appl. Syst. Innov. 2021, 4, 34; CC BY; pages 1-20 printed)
- **Version type:** publisher version
- **May differ materially from the published version:** No (version of record).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §3, p. 5; §4.1, p. 13 | 8 MP Raspberry Pi camera; phones appear only in the literature review (p. 3). | Candidate change |
| edge_device | Unknown | Unknown | Ambiguous | §3, p. 5; §4.1, p. 13; §5.4, p. 17 | A Raspberry Pi 4B "is used for the processing" with a 7-inch display, but "all the programming, training, and testing are done in Matlab". Where the real-time classification runs is not stated. | Needs researcher decision |
| on_device | Unknown | Unknown | Ambiguous | §3, p. 5; §4.1, p. 13 | Same ambiguity as edge_device. | Needs researcher decision |
| cloud | Unknown | No | Confirmed | full text read; no occurrence | No cloud processing described. | Candidate change |
| adaptive_inference | Unknown | No | Confirmed | full text read; no occurrence | Fixed feature extractor plus classifier. | Candidate change |
| resource_awareness | Unknown | No | Confirmed | full text read; no occurrence | No resource-driven decision. | Candidate change |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No energy or power result. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | Table 3, p. 14 | Printing temperature is a process parameter, not a device thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §4.2, p. 13; §5.4, p. 17 | One camera mounted beside the nozzle; 4-5 images per layer captured on key press. The text does not say the viewpoints differ, and each image is classified on its own (no joint use). | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | §3.3, pp. 9-10 | The ensemble assigns Good if more than two of five classifiers vote Good. No downstream action is triggered by a confidence score. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §3.4, p. 10 | Despite the "anomaly detection" wording, layers are labelled good/bad manually by eye and classified with supervised models (README §7.3, CD-14). | Candidate change |
| latency_evaluation | Unknown | Unknown | Ambiguous | §5.4, p. 17; §6, p. 18 | AlexNet+SVM is chosen for "less computational time" with no timing value. README Decision 3 keeps qualitative claims Unknown, while §7.3 says No once the full text is read and no timing is reported. Which rule applies after full-text reading is a researcher decision. | Needs researcher decision |
| accuracy_metrics | (blank) | Feature+classifier (Table 5): AlexNet+SVM 99.70%, EfficientNet-B0+SVM 99.70%, EfficientNet-B0+KNN 99.70%, AlexNet+KNN 99.40%, ResNet50+SVM 99.40%; Naive Bayes lowest (85.90-91.10%). Ensemble (Table 6): AlexNet 100%, ResNet18 99.40%, EfficientNet-B0 99.10%, ResNet50 98.80%, GoogLeNet 97.80%. Density-wise (Table 7): ResNet50 100%, AlexNet and EfficientNet-B0 99.22% | Confirmed | Tables 5-7, pp. 15-17 | As stated. | Candidate change |
| efficiency_metrics | (blank) | (blank) | Confirmed | full text read; no occurrence | No timing, size or energy value reported. | Keep current value |

### Other evidence

- **paper type:** system/method (full text). Comparative study plus a real-time monitoring demonstration.
- **application/domain:** Layer-wise surface fault detection in FDM printing from camera images (§3, p. 5).
- **dataset:** 1,700 layer images (good/bad, labelled by eye) of a 25 x 25 x 5 mm PLA cube on a Dreamer FDM printer; 4-5 images per layer; parameter variants of density, temperature and printing speed (§3.4, p. 10; §4.2, pp. 13-14).
- **hardware/device:** Acquisition: 8 MP Raspberry Pi camera beside the nozzle. Processing: Raspberry Pi 4B with 7-inch display (role in inference unclear). Programming, training and testing in MATLAB (machine not stated) (§3, p. 5; §4.1, p. 13). Roles as stated.
- **model(s):** Pre-trained CNN features (AlexNet, GoogLeNet, ResNet18, ResNet50, EfficientNet-b0) with SVM, KNN, Random Forest, Decision Tree, Naive Bayes; majority-vote ensemble; AlexNet+SVM used for real-time monitoring (§3.2-3.3, pp. 6-10; §5.4, p. 17). Matches the essence of the current value.
- **inference location:** Not stated (§3; §4.1). See edge_device.
- **adaptation mechanism:** None (full text read; no occurrence).
- **resource signals:** None (full text read; no occurrence).
- **evaluation metrics:** Accuracy, loss (100 - accuracy), confusion matrices (§5).
- **limitations:** None explicitly stated; future work: real-time condition-monitoring data, explainable fault visualisation, reinforcement learning (§6, p. 18). Future work only.
- **deployment setting:** Lab FDM printer with mounted Raspberry Pi camera; layer-wise real-time demonstration (§4.1; §5.4).
- **Observation:** Internal inconsistency: the second-best ensemble result is ResNet18 99.40% in §5.2/Table 6 but EfficientNet-B0 99.10% in §6.
- **Observation:** Possible inconsistency: Table 3 lists 8 densities x 3 temperatures x 3 speeds, while the text reports 32 variants.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `edge_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `on_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `resource_awareness`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed; resolve the Ambiguous edge_device / on_device / latency rows first.

## P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

### Source

None obtained. **Status: Blocked (abstract only).** Subscription article (Emerald Rapid Prototyping Journal); no legitimate open copy known (Step 9.1).

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

### Source

None obtained. **Status: Blocked (abstract only).** Subscription article (Elsevier Manufacturing Letters); no legitimate open copy known (Step 9.1).

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

### Source

- **Status:** Partially verified
- **Source used:** arXiv preprint 1810.10090v1 (23 Oct 2018), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/1810.10090v1 (version of record: MobiCom 2018, DOI 10.1145/3241539.3241559)
- **Accessed:** 2026-10-03
- **Parts read:** Full preprint text read.

### Version

- **Version:** Author preprint carrying the MobiCom '18 ACM permission block
- **Version type:** preprint
- **May differ materially from the published version:** Possibly. The ACM version of record was not accessible and was not compared.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §4.3.1 | Implemented on three smartphones (Samsung Galaxy S8, Galaxy S7, LG Nexus 5; Android 7.0); results reported from the Galaxy S8. | Candidate change |
| edge_device | Yes | Yes | Confirmed | §4.3.1 | Runs on the smartphones. | Keep current value |
| on_device | Yes | Yes | Confirmed | §4.3.1; Fig. 8 | On-device inference and model switching measured on the Galaxy S8. | Keep current value |
| cloud | Unknown | No | Confirmed | §4.3.1; §6 | The authors state their on-device framework "does not rely on cloud connectivity"; no cloud processing in the evaluation. | Candidate change |
| adaptive_inference | Yes | Yes | Confirmed | §2-§3; §4.3 | Runtime selection among nested descendant models of a multi-capacity model. | Keep current value |
| resource_awareness | Yes | Yes | Confirmed | §3; §4.3.1 | Resource-aware scheduler allocates runtime resources (benchmark memory budget 400 MB) and picks resource-accuracy trade-offs. | Keep current value |
| energy_evaluation | Yes | Yes | Confirmed | §4.2 (model switching); §4.3.1; §4.3.3; Figs. 8 and 11 | Power measured with a Monsoon power monitor; switching energy and inference energy reported. | Keep current value |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §4.1 | Image classification benchmarks; no multi-view. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | full text read; no occurrence | No confidence-triggered action. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §4.1 | Supervised classification tasks. | Candidate change |
| latency_evaluation | Yes | Yes | Confirmed | §4.3.2; Fig. 10 | latency type: throughput/FPS (frame-rate speedup on the Galaxy S8). | Keep current value |
| accuracy_metrics | Up to +4.2% inference accuracy vs resource-agnostic baseline | Up to +4.2% inference accuracy vs resource-agnostic baseline | Confirmed | §4.3.2 | Supported: 4.1% (MinTotalCost) and 4.2% (MinMaxCost) at equal frame rate; 2.6% / 2.1% at the knee. | Keep current value |
| efficiency_metrics | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Confirmed | §4.3.2-4.3.3 | Supported: 2.0x / 1.9x frame rate at equal accuracy; 1.7x / 1.5x energy reduction. Model-switching energy reduction per 1,000 switches: 602.1 J (VC) and 4.0 J (VS) (§4.2). | Keep current value |

### Other evidence

- **paper type:** system/method (full text).
- **application/domain:** Resource-aware multi-tenant on-device inference for continuous mobile vision (not inspection) (§1; §4.1).
- **dataset:** CIFAR-10, ImageNet-50, ImageNet-100, GTSRB, Adience-Gender, Places-32 (§4.1, Table 2). Current value is "Unknown".
- **hardware/device:** Inference: Samsung Galaxy S8 (reported), Galaxy S7, LG Nexus 5 (Android 7.0); power: Monsoon power monitor (§4.3.1).
- **model(s):** NestDNN multi-capacity models built from VGG-16 and ResNet-50 (§4.1, Table 2). Refines the current value.
- **inference location:** On the smartphone (§4.3.1).
- **adaptation mechanism:** Runtime switching among nested descendant models (§2-§3).
- **resource signals:** Available memory and compute; number of concurrent applications (§3; §4.3.1).
- **evaluation metrics:** Accuracy gain, frame-rate speedup, energy, memory, model-switching cost (§4).
- **limitations:** Filter-importance (TRR) pruning costs much more than L1-norm pruning, raising the cost of generating multi-capacity models (§5). Stated by the authors.
- **deployment setting:** Benchmark emulating application launches and kills (2-6 concurrent apps; 60 s simulations, 100 repeats) (§4.3.1).
- **Observation:** Verified against the arXiv v1 preprint carrying the MobiCom 2018 permission block; the ACM version was not compared.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed, subject to a check against the version of record.

## P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

### Source

- **Status:** Partially verified
- **Source used:** arXiv preprint 2410.10847v1 (1 Oct 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2410.10847v1 (version of record: DAC 2024, DOI 10.1145/3649329.3657310)
- **Accessed:** 2026-10-03
- **Parts read:** Full preprint text read (6 pages plus references). The preprint has no printed page numbers; evidence is cited by section, table and figure.

### Version

- **Version:** Author preprint carrying the DAC '24 ACM copyright block
- **Version type:** preprint
- **May differ materially from the published version:** Possibly. The DAC version of record is closed access and was not compared.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Yes | Yes | Confirmed | §4.4; Table 2 caption | The text names the "Mi 11 Lite" with a Snapdragon 780G; the Table 2 caption names the "Mi 11 Lite 5G". The Step 8.3 external identification stands. | Keep current value |
| edge_device | Yes | Yes | Confirmed | §4.4; §5 | Jetson Orin Nano and Mi 11 Lite 5G. | Keep current value |
| on_device | Yes | Yes | Confirmed | §5.1.2; §5.2.1 | The two-stage detectors are "on-device" and run 3,000 iterations on the device. Note: the Lotus agent runs on a separate desktop (see cloud). | Keep current value |
| cloud | Unknown | No | Confirmed | §4.4 | The DRL agent runs on a desktop with an RTX 2080Ti and controls the device's frequencies over a socket. This is off-device control, but not a cloud/datacenter server. | Candidate change |
| adaptive_inference | Unknown | No | Confirmed | §4.1-4.4 | Lotus only scales CPU and GPU frequencies, twice per frame. The detector computation is unchanged; the varying proposal count is a property of the unmodified detectors; the two-width execution belongs to the agent's Q-network, not the detector. DVFS with unchanged model computation is No (Decision 4, README §7.4 #2). Requires researcher confirmation because of the Step 8.3 recode. | Candidate change |
| resource_awareness | Yes | Yes | Confirmed | §4.3.2 | Agent state includes CPU/GPU temperature, frequency level, remaining time to the latency constraint and the number of proposals. | Keep current value |
| energy_evaluation | Unknown | No | Confirmed | full text read; no occurrence | Power appears only as motivation; no energy or power result. | Candidate change |
| thermal_evaluation | Yes | Yes | Confirmed | §4.1; §5.2; Figs. 4-7 | Device temperatures measured and compared with baselines; throttling threshold in the reward. | Keep current value |
| multi_view | Unknown | No | Confirmed | §5.1.2 | KITTI and VisDrone2019 detection; no multi-view inspection. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | full text read; no occurrence | No confidence-triggered action. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §5.1.2 | Object-detection benchmarks. | Candidate change |
| latency_evaluation | Unknown | Yes | Confirmed | Tables 1-2; §5.2.1 | latency type: inference latency (mean and standard deviation per image on Jetson Orin Nano and Mi 11 Lite 5G). | Candidate change |
| accuracy_metrics | (blank) | (blank) | Confirmed | Fig. 1; §5 | No detection accuracy is reported for Lotus; the Fig. 1 mAP values are motivation for the baseline models. | Keep current value |
| efficiency_metrics | (blank) | Jetson Orin Nano, MaskRCNN on VisDrone2019 (Table 1): mean latency 768.4 / 584.3 / 531.4 ms and SD 260.4 / 114.2 / 70.7 ms (default / zTT / Lotus), i.e. latency -30.8% vs default and -9.1% vs zTT; SD -72.8% / -38.1%; constraint-satisfaction rate 39.0% / 50.1% / 74.9%. Mi 11 Lite 5G (Table 2): MaskRCNN on KITTI SD 781.8 / 610.5 / 552.3 ms (-29.4% / -9.5%); FasterRCNN on VisDrone2019 satisfaction 92.5%. Lotus overhead 8.52 ms per inference (Q-network 0.42 ms on the desktop GPU; socket 1.92 ms per message) | Confirmed | Tables 1-2; §4.4.2; §5.2.1 | The "+35.9% / +24.8%" satisfaction gains in §5.2.1 are percentage-point differences (74.9 - 39.0; 74.9 - 50.1). | Candidate change |

### Other evidence

- **paper type:** system/method (full text).
- **application/domain:** Thermal and latency-variation management for two-stage detectors on edge devices (autonomous-driving and drone datasets; not inspection) (§1; §5.1.2).
- **dataset:** KITTI; VisDrone2019 (§5.1.2). Current value is "Unknown".
- **hardware/device:** Inference: NVIDIA Jetson Orin Nano (6-core Cortex-A78AE, 1024-core Ampere GPU, 8 GB); Xiaomi Mi 11 Lite 5G (Snapdragon 780G, Kryo 670, Adreno 642). DRL agent: desktop with NVIDIA RTX 2080Ti, connected by socket (§4.4).
- **model(s):** Faster R-CNN and Mask R-CNN detectors; Lotus DQN agent (4-layer MLP executed at 0.75x and 1x width) (§4.3.4; §4.4.1; §5.1.2). Refines the current value.
- **inference location:** Detector on the device; frequency-control agent on a separate desktop (§4.4).
- **adaptation mechanism:** DRL-driven joint CPU/GPU DVFS, two decisions per frame (system-level) (§4.2-4.3).
- **resource signals:** CPU/GPU temperature, CPU/GPU frequency level, remaining time to the latency constraint, number of proposals (§4.3.2).
- **evaluation metrics:** Mean and standard deviation of latency, latency-constraint satisfaction rate, device temperature (§5; Tables 1-2).
- **limitations:** (blank) - none stated (§6).
- **deployment setting:** Lab: 25 °C indoor static environment; warm (25 °C) and cold (0 °C) zones; dataset switching (§5.2).
- **Observation:** Only the detector runs on the phone/Jetson. The Lotus agent runs off-device on a desktop RTX 2080Ti.
- **Observation:** Verified against the arXiv v1 preprint carrying the DAC 2024 copyright block; the publisher version is closed access.

### Conflicts with abstract-level coding

- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed, subject to a check against the version of record. adaptive_inference Unknown→No needs explicit researcher confirmation: Step 8.3 recoded it Yes→Unknown under Decision 4, and the full text now resolves it as DVFS-only (No).

## P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

### Source

None obtained. **Status: Blocked (inaccessible from this environment).** Publisher (ACM TECS) closed; the only open copy is a submitted version in the Uppsala DiVA repository (urn:nbn:se:uu:diva-587035, per OpenAlex and Semantic Scholar). The resolver returned an Anubis bot challenge, which was not bypassed.

### Version

- (no full text read)

### Evidence by characteristic

Not examined. The abstract-level coding in `papers.csv` stands unchanged.

### Other evidence

- None.

### Conflicts with abstract-level coding

Cannot be assessed.

### Recommended action

**Insufficient evidence.** Obtain the full text (normal browser access for open-access copies; institutional access, interlibrary loan or an author copy for subscription papers) before any recoding.

## P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

### Source

- **Status:** Partially verified
- **Source used:** arXiv copy 2409.01089v1 (2 Sep 2024), retrieved through the alphaXiv full-text service
- **URL / identifier:** https://arxiv.org/abs/2409.01089v1 (version of record: ACM TECS 23(4), Article 60, June 2024, DOI 10.1145/3665868)
- **Accessed:** 2026-10-03
- **Parts read:** Full text read. Page numbers 60:xx are given only where the page break was clear in the extracted text.

### Version

- **Version:** arXiv copy typeset in the ACM TECS journal layout (pages 60:1-60:31)
- **Version type:** preprint server copy in journal layout
- **May differ materially from the published version:** Unlikely (journal layout and pagination), but not confirmed against the ACM page, which was not accessible.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §6.3, p. 60:19 | Evaluated on three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71. | Candidate change |
| edge_device | Yes | Yes | Confirmed | §6.3 | The smartphones above. | Keep current value |
| on_device | Yes | Yes | Confirmed | §6.3-§7 | On-device execution with TFLite on CPU/GPU/NPU (DSP on A71). | Keep current value |
| cloud | Unknown | No | Confirmed | Fig. 2, p. 60:15 | A server is used only for offline model conversion and design generation; inference and the runtime manager run on the device. | Candidate change |
| adaptive_inference | Yes | Yes | Confirmed | §4.3; §7.2 | The runtime manager switches model, processor or both at runtime from a precomputed design set. | Keep current value |
| resource_awareness | Yes | Yes | Confirmed | §4.3; §7.2 | Switching is triggered by processor overload and memory pressure under user-defined SLOs. | Keep current value |
| energy_evaluation | Unknown | Unknown | Ambiguous | §4.1; §6.4, pp. 60:19-60:20; §7 | Energy is a listed objective and is profiled on the device (100 runs per configuration), but no energy value is reported in the results. Leaning No. | Needs researcher decision |
| thermal_evaluation | Unknown | No | Confirmed | §2.1.2; §4.3; §6.4 | Overheating is discussed as a cause of slowdowns, and 2-minute idle periods keep device temperature consistent during profiling, but temperature is not measured or reported. | Candidate change |
| multi_view | Unknown | No | Confirmed | full text read; no occurrence | No multi-view. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | full text read; no occurrence | No confidence-triggered action. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §6.2 | Supervised tasks. | Candidate change |
| latency_evaluation | Unknown | Yes | Confirmed | §7; Figs. 7-8 | latency type: inference latency (average and standard deviation in ms per design) and, separately, throughput/FPS (images per second). | Candidate change |
| accuracy_metrics | (blank) | UC1 initial design on S20 (EfficientNet Lite0 FFX8, CPU, 4 threads, XNNPACK): 75.11%; UC1 vs transferred baselines: +0.156 average accuracy; UC3 memory-efficient switch: 8.5% accuracy decrease | Confirmed | §7.1.2; §7.2.1; §7.2.2 | As stated. | Candidate change |
| efficiency_metrics | (blank) | vs transferred baselines: UC1 +32.7% throughput; UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory 16 MB; UC3 switch saved 92 MB RAM; storage vs OODIn e.g. UC1 on A71 13.83 MB vs 276.36 MB (Table 10). Optimality (a composite metric, not pure efficiency): UC3 1.47x average (up to 3.24x) over the multi-DNN-unaware baseline and 1.87x (up to 4.06x) over transferred baselines | Confirmed | §7.1.2-7.1.3; §7.2; Tables 9-10, p. 60:25 | The 4.06x figure is an optimality gain over transferred baselines, not a throughput value. | Candidate change |

### Other evidence

- **paper type:** system/method (full text).
- **application/domain:** Constraint-aware runtime adaptation of single- and multi-DNN workloads on smartphones (not inspection) (§1; §6.2).
- **dataset:** Use cases covering image classification (ImageNet ILSVRC 2012 evaluation), scene recognition, face analysis (gender, age, ethnicity), text classification and audio (YAMNet) (§6.2). Current value omits image classification and audio.
- **hardware/device:** Inference: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71 (CPU, GPU, NPU; DSP on A71); TFLite (§6.3).
- **model(s):** CARIn (MOO formulation, RASS solver, runtime manager); model suites including EfficientNet Lite variants, MobileViT and YAMNet (§4; §6.2). Refines the current value.
- **inference location:** On the smartphone (§6.3).
- **adaptation mechanism:** Model and/or processor switching from a precomputed design set (§4.3).
- **resource signals:** Processor workload (overload) and aggregate memory use (§4.3).
- **evaluation metrics:** Optimality, accuracy, latency (mean and SD), throughput, memory, model size, storage, solving time (§4.1; §7).
- **limitations:** Exhaustive on-device profiling is too costly for realistic deployment; generative models not evaluated (§8, p. 60:26). Stated by the authors.
- **deployment setting:** Lab evaluation on three phones with emulated runtime issues (§6-§7).
- **Observation:** The arXiv copy carries the ACM TECS journal pagination; it was not compared with the ACM page.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed, subject to a version check; resolve the Ambiguous energy_evaluation row first.

## P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

### Source

- **Status:** Fully verified
- **Source used:** FH JOANNEUM ePUB institutional repository PDF
- **URL / identifier:** https://epub.fh-joanneum.at/obvfhjoa/content/titleinfo/13393868/full.pdf (DOI 10.1109/TMC.2025.3594214)
- **Accessed:** 2026-10-03
- **Parts read:** Pages 451-464 read.

### Version

- **Version:** PDF in the IEEE Transactions on Mobile Computing final layout (vol. 25, no. 1, Jan 2026, pp. 451-464), bearing "© 2025 The Authors" and a CC BY 4.0 licence line
- **Version type:** publisher layout (repository copy)
- **May differ materially from the published version:** Unlikely. OpenAlex labels this repository copy "submittedVersion", which conflicts with the publisher layout and pagination; the label conflict is recorded, not resolved.

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | Yes | Confirmed | §VI, p. 461; Fig. 10, p. 462 | Evaluated on two phones (Xiaomi Redmi Note 9 Pro, Google Pixel 6) with the TFLite benchmarking tool on Android. | Candidate change |
| edge_device | Yes | Yes | Confirmed | §VI, p. 461 | Phones and IoT boards (Arduino Nano 33 BLE Sense, Infineon CY8CKIT-062S2). | Keep current value |
| on_device | Yes | Yes | Confirmed | §VI, p. 461 | On-device inference and submodel switching measured (TFLMicro extended for REDS). | Keep current value |
| cloud | Unknown | No | Confirmed | §IV-A, p. 458; Acknowledgment, p. 463 | Workstations and computing clusters used for training only; no cloud inference. | Candidate change |
| adaptive_inference | Yes | Yes | Confirmed | §II, p. 453; §VI, p. 462 | Nested subnetworks; switching changes the active layer widths at runtime (38 ± 1 µs adaptation). | Keep current value |
| resource_awareness | Yes | Yes | Confirmed | §I, p. 451; §III-D, pp. 455-457 | Subnetworks built under MAC and peak-memory constraints and switched in response to dynamic resource constraints. | Keep current value |
| energy_evaluation | Unknown | Yes | Confirmed | Table VI and text, p. 463 | Inference energy measured with a Power Profiler Kit (PPK2) on a Nordic nRF52840: 20-61 mJ for DS-CNN; switching < 0.01 mJ. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | full text read; no occurrence | No multi-view. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | No | Confirmed | §I, p. 452; Fig. 11, p. 462 | Early-exit methods appear only as related work and as a comparison baseline; REDS triggers no action from a confidence score. | Candidate change |
| anomaly_detection | Unknown | No | Confirmed | §IV | Supervised benchmark tasks. | Candidate change |
| latency_evaluation | Unknown | Yes | Confirmed | §VI, pp. 461-463; Fig. 10 | latency type: inference latency (TFLite benchmark on phones; on-device timing on IoT boards, e.g. 2-layer FC network on Arduino Nano 33 BLE Sense: 2,131 ± 27 µs at 25% MACs and 4,548 ± 13 µs at 50% MACs). | Candidate change |
| accuracy_metrics | (blank) | ViT-Base on ImageNet-1K (Table IV, p. 460), REDS full / medium / low subnetworks: 79.88% / 78.42% / 68.21% top-1; MobileNetV1 on VWW: 27% lower peak memory for 0.9% lower accuracy (§IV-B, p. 458; Table III, p. 460) | Confirmed | §IV-B, p. 458; Tables III-IV, p. 460 | Most other accuracies are in figures and were not extracted. | Candidate change |
| efficiency_metrics | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | Adaptation time 38 ± 1 µs (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 ± 27 µs (25% MACs) and 4,548 ± 13 µs (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2); cache-hit rate above 97% with the optimized matrix multiplication (RP2040, Table V) | Confirmed | §V-B, p. 461; §VI, pp. 462-463; Table VI | Extends the current single-value entry. | Candidate change |

### Other evidence

- **paper type:** system/method (full text).
- **application/domain:** Resource-adaptive nested subnetworks for mobile and IoT devices (keyword spotting, visual wake words, image classification; not inspection) (§I; §IV).
- **dataset:** Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K (Abstract; §IV-A). Matches the current value.
- **hardware/device:** Inference: Xiaomi Redmi Note 9 Pro, Google Pixel 6, Arduino Nano 33 BLE Sense (nRF52840), Infineon CY8CKIT-062S2. Cache benchmark: Raspberry Pi Pico (RP2040). Energy: PPK2 on nRF52840. Training: workstations with Tesla K80 / A100 GPUs (§IV-A, p. 458; §V-B, p. 461; §VI, pp. 461-463).
- **model(s):** REDS (iterative knapsack, bottom-up / top-down heuristics) applied to DNN, CNN, DS-CNN (S/L), MobileNetV1 (0.25x) and ViT-Base (§III; §IV-A). Refines the current value.
- **inference location:** On device (§VI).
- **adaptation mechanism:** Runtime switching among nested subnetworks by changing layer widths (§II; §VI).
- **resource signals:** MACs, peak memory, dynamic resource constraints (§III).
- **evaluation metrics:** Accuracy, parameters, MACs, peak memory, inference time, adaptation time, energy, cache-hit rate (§IV-§VI).
- **limitations:** Not tested as NAS for large language or multimodal models; cache optimisation for convolutions unexplored; energy as a solver constraint left for future work (§VII, p. 463). Stated as future directions.
- **deployment setting:** Lab benchmarks on phones and IoT boards (§VI).
- **Observation:** Repository copy carries the IEEE TMC journal pagination and CC BY line, although OpenAlex labels it "submittedVersion".
- **Observation:** Internal inconsistency: the abstract says eight benchmark architectures; the conclusion says seven.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `energy_evaluation`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Yes (Resolves Unknown; Confirmed; Candidate change).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Candidate change.** Candidate changes as listed.

## P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

### Source

- **Status:** Fully verified
- **Source used:** UTS institutional repository (OPUS) copy of the publisher PDF
- **URL / identifier:** https://opus.lib.uts.edu.au/bitstream/10453/147577/2/1-s2.0-S1474034620300707-main.pdf (hdl:10453/147577; DOI 10.1016/j.aei.2020.101101)
- **Accessed:** 2026-10-03
- **Parts read:** Pages 1-9 read (all sections; reference list partially).

### Version

- **Version:** Publisher PDF (Advanced Engineering Informatics 45 (2020) 101101; CC BY-NC-ND; pages 1-9 printed)
- **Version type:** publisher version
- **May differ materially from the published version:** No (publisher PDF).

### Evidence by characteristic

| Field | Current | Full text | Confidence | Location | Evidence | Recommended action |
|---|---|---|---|---|---|---|
| smartphone | Unknown | No | Confirmed | §4.2, p. 7 | The edge device is an industrial PC; no smartphone role. | Candidate change |
| edge_device | Unknown | Unknown | Ambiguous | §2.2, p. 2; §4.2, p. 7 | The GBT model runs on an edge device at the SMT line: an industrial PC with an Intel Celeron N2930. The paper defines an edge device as any computing or networking resource between data sources and the cloud. Whether a low-power industrial PC counts as resource-constrained hardware (README §7.3) or as plant IT is open. | Needs researcher decision |
| on_device | Unknown | Unknown | Ambiguous | §4.2, p. 7 | The edge PC receives and parses SPI result files (CAMX-XML) over TCP/IP; it is not the capturing device or hardware attached to it. Leaning No, but tied to the industrial-PC question. | Needs researcher decision |
| cloud | Unknown | No | Confirmed | §4.2, p. 7; §5, p. 8 | Training on a company-owned Spark cluster, storage in AWS S3; "trained ... in the cloud and deployed on local edge devices" (§5). Inference runs on the edge PC. Cloud used only for training and storage (does not qualify). | Candidate change |
| adaptive_inference | Unknown | No | Confirmed | §3.3, p. 5; §4.2, pp. 6-7 | Static GBT model. "Dynamic" inspection refers to routing panels around X-ray, not to inference. | Candidate change |
| resource_awareness | Unknown | Unknown | Ambiguous | §3.2, p. 4; §3.4, p. 5; §4.1, p. 6 | GBT chosen over SVM because its scoring time was eight times faster, "with future scaling" in mind; takt time sets the real-time constraint. A deployment-time choice informed by timing, without an explicit device budget. | Needs researcher decision |
| energy_evaluation | Unknown | No | Confirmed | §3.4, p. 5 | Energy constraints are listed as a general deployment challenge; nothing is measured. | Candidate change |
| thermal_evaluation | Unknown | No | Confirmed | full text read; no occurrence | No thermal measurement. | Candidate change |
| multi_view | Unknown | No | Confirmed | §4, Table 2, p. 6 | Inputs are seven numeric SPI features per solder joint, not images. | Candidate change |
| uncertainty | Unknown | No | Confirmed | full text read; no occurrence | No uncertainty estimation. | Candidate change |
| confidence_gating | Unknown | Unknown | Ambiguous | §3.3, p. 5; §4.1-4.2, pp. 6-7 | Fields of view predicted defect-free skip X-ray; the model is tuned to be conservative (penalising false negatives). The routing is triggered by the predicted class; no confidence score or threshold is described. | Needs researcher decision |
| anomaly_detection | Unknown | No | Confirmed | §3.2, p. 4; §4.1, p. 6 | Supervised classifiers trained on X-ray labels. | Candidate change |
| latency_evaluation | Unknown | Unknown | Ambiguous | §4.1, Table 3, pp. 6-7; §4.2, p. 7 | Table 3 gives scoring times per 1,000 rows, but "the description of hardware used is omitted". On the edge PC (Celeron N2930), current test sets are processed in under one minute: an upper bound, not a per-item timing. | Needs researcher decision |
| accuracy_metrics | (blank) | Initial balanced sample, 5-fold CV (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9% / 96.4% / 89.3%; DT 88.2%; NB 83.5%; LR 71.9%. Highly conservative GBT, solder-joint level (Table 4): class recall 98.8% / 86.4%. FOV level (Table 5): average X-ray volume reduced by about 29% | Confirmed | Tables 3-5, p. 7 | Table 3 values are clear. Some Table 4 and Table 5 cell values look inconsistent in the extracted text and should be checked visually before recoding. | Candidate change |
| efficiency_metrics | (blank) | Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets in under 1 min. Edge-cloud link: 2-150 ms latency, 10 MB per 14 s (about 1 Mbit/s per line) | Confirmed | Table 3, p. 7; §4.2, p. 7 | As stated. | Candidate change |

### Other evidence

- **paper type:** system/method (industrial case study) (§3-§4). Proposes a framework and evaluates it in a Siemens SMT line.
- **application/domain:** Predictive quality inspection of PCB solder joints in SMT assembly: predicting X-ray results from numeric solder-paste-inspection (SPI) measurements to reduce X-ray inspection volume. The ML model does not process images. (§1, p. 1; §4, pp. 5-6). SPI is described as a visual inspection station, but the model input is its numeric output.
- **dataset:** Five production months of SPI and X-ray records for one connector PCB variant (48-board panel), Siemens Amberg: 1,461,037,321 data points, ~0.0008% not OK; seven SPI features (height, shape 2D, shape 3D, surface, volume, offset X, offset Y) with binary X-ray label (§4, Table 2, p. 6).
- **hardware/device:** Inference: edge industrial PC with Intel Celeron N2930 at the SMT line. Training: company Spark cluster (up to 24 workstations, 16-core CPUs, 32-64 GB RAM). Storage: AWS S3 (§4.2, p. 7). Roles as stated.
- **model(s):** Gradient Boosted Tree (selected); Decision Tree, Naive Bayes, Logistic Regression, SVM compared (§4.1, p. 6).
- **inference location:** Edge industrial PC at the manufacturing line (§4.2, p. 7; §5, p. 8). See edge_device / on_device.
- **adaptation mechanism:** None (full text read; no occurrence). Static model; routing of panels is a process decision.
- **resource signals:** Takt time and model scoring time (model selection only) (§3.4, p. 5; §4.1, p. 6). See resource_awareness.
- **evaluation metrics:** Accuracy, standard deviation, recall, precision, training and scoring time, class recall, inspection-volume reduction (Tables 3-5, p. 7).
- **limitations:** Deployment limited to one product variant, one manufacturing line and the SPI and X-ray data sources (§4.3, p. 7). Stated by the authors.
- **deployment setting:** Siemens electronics plant, Amberg (Germany): SMT line with SPI station, edge PC and X-ray routing (§4, pp. 5-7).
- **Observation:** **Not image-based.** The ML input is seven numeric SPI measurements per solder joint. The task is predicting X-ray results so that defect-free fields of view can skip X-ray (about 29% average volume reduction at FOV level).
- **Observation:** The paper's own edge definition (§2.2) is broader than README §7.3 (it includes any computing resource between sources and cloud).
- **Observation:** Relevance to visual inspection is indirect: the data come from an optical SPI station, but the model never sees images. The proposed class D is not changed here.

### Conflicts with abstract-level coding

- `smartphone`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `edge_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `on_device`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `cloud`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `adaptive_inference`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `resource_awareness`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `energy_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `thermal_evaluation`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `multi_view`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `uncertainty`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `confidence_gating`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `anomaly_detection`: Unknown → No (Resolves Unknown; Confirmed; Candidate change).
- `latency_evaluation`: Unknown → Unknown (Ambiguous (current value kept); Needs researcher decision).
- `accuracy_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- `efficiency_metrics`: free-text fill/extension (Candidate change); see conflicts file.
- No current `Yes`/`No` value is contradicted.

### Recommended action

**Needs researcher decision.** Not image-based (numeric SPI process data). The relevance class and the industrial-PC edge questions are researcher decisions. Field-level candidate changes are listed in the conflicts file.
