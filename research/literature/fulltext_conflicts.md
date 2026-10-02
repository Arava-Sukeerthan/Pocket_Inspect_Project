# Full-Text Conflicts with Abstract-Level Coding (Step 9.2)

_2026-10-04, Claude Code. Lists only cases where full-text evidence differs from, or could contradict, the current `papers.csv` value. **Nothing has been applied**: every row needs researcher/ChatGPT review before a separate, logged recoding step (README §7.7)._

**Row types:**
- **Resolves Unknown:** the current value is `Unknown` and the full text supports `Yes` or `No`.
- **Contradicts:** the full text does not support the current `Yes`/`No`.
- **Ambiguous (leaning change):** the evidence points to a different value but is not conclusive.
- **Ambiguous (no change):** the evidence is unclear and does not point to a different value.
- **Free-text:** a metric field would gain or change content.
- **Relevance:** the finding bears on the relevance class, which is not changed in this step.

`Ambiguous` rows keep the current value until the researcher decides.

| Paper | Field | Current | Full-text evidence | Proposed value | Reason | Decision required |
|---|---|---|---|---|---|---|
| P001 | `edge_device` | Unknown | §6.3, §7; README §7.5: Inference runs on the Android phone (resource-constrained mobile hardware). | Yes | Resolves Unknown | Yes: approve before recoding |
| P001 | `on_device` | Unknown | §6.3, §7, §8: Trained model converted to TFLite and run on the phone; real-time detection on the phone camera video stream; conclusion says detection uses only smartphones. | Yes | Resolves Unknown | Yes: approve before recoding |
| P001 | `cloud` | Unknown | §4, §6: Training on a desktop GPU workstation; inference on the phone; no cloud or server processing described. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `adaptive_inference` | Unknown | §4.2, §6: Single fixed SSD MobileNet model; no runtime adaptation. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `resource_awareness` | Unknown | §3, §4.2: Model chosen for its published speed/accuracy trade-off: a design-time lightweight-model choice, not a resource-driven decision (README §7.3). | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No temperature or throttling measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `multi_view` | Unknown | §5, §7: Single images and a single phone-camera video stream. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `uncertainty` | Unknown | §6.2, §7: Prediction percentage displayed as confidence; no uncertainty estimation or calibration. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `confidence_gating` | Unknown | §6.2-§7: Confidence is displayed in the app; no action is triggered by it. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `anomaly_detection` | Unknown | §5.3, §6: Supervised detector trained on four labelled defect classes. | No | Resolves Unknown | Yes: approve before recoding |
| P001 | `latency_evaluation` | Unknown | §4.2, §7, Fig. 7: App GUI shows inference time and Fig. 7 screenshots include it, but no values are given in the text. The 56 ms in §4.2 is the pre-trained model's published COCO benchmark, not the authors' measurement. Values may be readable in Fig. 7. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P001 | `accuracy_metrics` | (blank) | Table 1, §7: Per class at IoU 0.6 (Table 1), recall/precision/accuracy: crack 0.4/0.53/0.61; deterioration 0.68/0.68/0.83; mould 0.85/0.66/0.81; stain 0.71/0.85/0.95 | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P002 | `edge_device` | Unknown | §4.3, §5: Conclusions state classification runs in real time on local smartphones, and models were quantized to reduce load on phones. The text does not describe running or timing the CNN on a named phone. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P002 | `on_device` | Unknown | §4.3, §5: Same as edge_device: real-time on-phone classification is stated as the scope, but no on-device execution or benchmark is described. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P002 | `cloud` | Unknown | §5: A cloud server for a live defect map is future work only. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `adaptive_inference` | Unknown | keyword search of full text + methods/results read: Fixed models; the sliding window changes how often tests run, not the model computation. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `resource_awareness` | Unknown | §4.3: Quantization to lighten models for phones is design-time lightweighting, not a resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `multi_view` | Unknown | §3.1, §3.2: Input modality is a 1-D accelerometer time series, not imaging. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `confidence_gating` | Unknown | §3.1.2: In the automatic labelling pipeline, a dashcam sample is kept only if at least 90% of 30 YOLOv5m frame classifications agree. This is a consistency vote used to build the dataset, not a confidence score acting on the deployed classifier. Whether this counts needs a decision. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P002 | `anomaly_detection` | Unknown | §3.2, §4.3: Supervised classification of speed bumps, manholes and potholes. | No | Resolves Unknown | Yes: approve before recoding |
| P002 | `latency_evaluation` | Unknown | §4.3 Fig. 9, §5: Average processing time per minute of test data is reported (about 0.1 s per minute of driving), but the hardware on which it was measured is not stated (README §7.3 requires stated or identifiable hardware). | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P002 | `accuracy_metrics` | (blank) | §4.3, §5: RDD-CNN accuracy reported as exceeding 86.77% (Conclusions); speed bump vs no-defect discrimination 99% (Fig. 7); automatic data collection missed 15.21% of data with 100% label accuracy (Conclusions) | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P002 | `efficiency_metrics` | (blank) | §4.1, §4.3, §5: Quantization reduced model size by 59.11% on average; about 0.1 s processing per minute of driving data (hardware not stated); 533.75 sliding-window tests per minute on average; YOLOv5m labelling model 882 MB | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P002 | `application/domain` | Smartphone / Mobile AI / Road defect classification (speed bumps, manholes, potholes) | §3.1, §3.2: Input modality is vibration. Relevance to smartphone visual inspection is a researcher decision. | No CSV change proposed; relevance class review | Relevance | Yes: researcher decision on relevance class (not changed in this step) |
| P007 | `cloud` | Unknown | §2, §3: No cloud processing; training on a local workstation. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `adaptive_inference` | Unknown | keyword search of full text + methods/results read: Fixed detectors. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `resource_awareness` | Unknown | keyword search of full text + methods/results read: No resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `multi_view` | Unknown | §2.2.4: OAK-D has stereo cameras, but detection uses the single RGB camera; no multi-view inspection. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `confidence_gating` | Unknown | §3.4, §3.7: Confidence thresholds only filter detections; no downstream action (recapture, referral, fallback) is triggered. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `anomaly_detection` | Unknown | §3.2: Supervised single-class pothole detection. | No | Resolves Unknown | Yes: approve before recoding |
| P007 | `efficiency_metrics` | Tiny-YOLOv4 31.76 FPS on OAK-D | Table 1, Table 3: On OAK-D (Table 3): Tiny-YOLOv4 31.76 FPS, SSD-MobileNetv2 26.65 FPS, YOLOv5 18.25 FPS, YOLOv2 3.20 FPS, YOLOv3 2.39 FPS, YOLOv4 1.98 FPS. Inference time per image (Table 1, hardware not stated): Tiny-YOLOv4 4.86 ms, SSD-MobileNetv2 7 ms, YOLOv5 10 ms, YOLOv2 33.7 ms, YOLOv4 52.51 ms, YOLOv3 70.57 ms, YOLOv1 340 ms | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P011 | `smartphone` | Unknown | §5.5.1, §5.5.2, Fig. 7 (pp. 13-15): Mobile model optimised for smartphones; app built for Android and iOS; iOS interface designed for an iPhone 11 Pro. | Yes | Resolves Unknown | Yes: approve before recoding |
| P011 | `cloud` | Unknown | §4 module 6, §5.6, Fig. 4 (pp. 9-14): Textual explanations are generated by calling the GPT-4 Vision API (a remote large vision-language model). Cloud mode: cloud-assisted (explanation step only); segmentation stays on the device. | Yes | Resolves Unknown | Yes: approve before recoding |
| P011 | `adaptive_inference` | Unknown | §5.5: Static quantized/pruned model; no runtime adaptation. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `resource_awareness` | Unknown | §5.5.1: Quantization and pruning are design-time lightweighting with no explicit device budget or resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `multi_view` | Unknown | §6.1, §7.1: Single images from aerial and handheld/AGV cameras; no joint use of multiple views. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation ("confidence" appears only as user trust). | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `confidence_gating` | Unknown | keyword search of full text + methods/results read: No action triggered by a confidence score. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `anomaly_detection` | Unknown | §5: Supervised semantic segmentation. | No | Resolves Unknown | Yes: approve before recoding |
| P011 | `latency_evaluation` | Unknown | Table 4, §8.3: No segmentation inference timing reported. Table 4 gives XAI-method running times in seconds without stated hardware; the authors list explanation latency on edge devices as a limitation. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P011 | `accuracy_metrics` | (blank) | Table 3 (p. 17), §6.5: TTPLA mIoU (Table 3): DLv3P-MobileNetv2 mobile 75.48%; DLv3P-ResNet101 enhanced 86.35%, mobile 83.95% | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P011 | `efficiency_metrics` | (blank) | Table 3 (p. 17): Model size (Table 3): DLv3P-MobileNetv2 mobile 3.51M parameters / 13.39 MB; DLv3P-ResNet101 mobile 36.57M / 139.52 MB vs base 45.66M / 174.21 MB | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P015 | `smartphone` | Unknown | Methods (p. 10): Logitech C270 webcams and Raspberry Pi cameras; no smartphone. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `edge_device` | Unknown | Online correction (p. 6); Computing requirements (p. 11): Images are sent to a local server for inference; the final models ran on a workstation with two NVIDIA Quadro RTX 5000 GPUs, which was also used for online correction. The Raspberry Pi is only a networked gateway. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `on_device` | Unknown | p. 6, p. 11: Inference runs on the local server, not on the capture device. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `cloud` | Unknown | p. 6, p. 11: Local server; no remote cloud processing described. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `adaptive_inference` | Unknown | Online correction pipeline (p. 6): Fixed network; the control loop adapts printer parameters, not inference (README §7.3). | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `resource_awareness` | Unknown | full text: No resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `energy_evaluation` | Unknown | full text: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `thermal_evaluation` | Unknown | full text: Hotend temperature is a printing parameter being corrected, not a device thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `multi_view` | Unknown | Methods (p. 10), Discussion (p. 10): A single nozzle-facing camera; combining with a global camera is suggested as future work. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `uncertainty` | Unknown | full text: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `confidence_gating` | Unknown | Fig. 3, Online correction pipeline (p. 6): Predictions are stored in lists of length L; a correction is made only if one prediction reaches the mode-threshold share of the list, and that share scales the adjustment. This is a vote frequency over repeated predictions rather than a model confidence score; whether it counts needs a decision. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P015 | `anomaly_detection` | Unknown | Network architecture section, Fig. 2: Supervised multi-head classification of parameter deviation (too low/good/too high). | No | Resolves Unknown | Yes: approve before recoding |
| P015 | `latency_evaluation` | Unknown | p. 6, Methods (p. 10): Images are captured at 2.5 Hz and correction speed is discussed, but no inference timing on stated hardware was found in the sections read. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P015 | `accuracy_metrics` | (blank) | Table 1 and Methods (p. 11): Test accuracy across four parameters 84.3% (attention multi-head network; Table 1); single-stage ResNet18-101 baselines 80.4-82.5%; flow-rate accuracy 82.1% multi-head vs 77.5% single-head | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P016 | `smartphone` | Unknown | §3: Raspberry Pi 4 with a camera; no smartphone. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `edge_device` | Unknown | §3: The trained SSD model runs on a Raspberry Pi 4 with a connected camera, at the same frame rate as the earlier setup. | Yes | Resolves Unknown | Yes: approve before recoding |
| P016 | `on_device` | Unknown | §3: Inference runs on the Raspberry Pi 4 with its attached camera placed in front of the print bed. | Yes | Resolves Unknown | Yes: approve before recoding |
| P016 | `cloud` | Unknown | §2.2, §3: Training on a Tesla K80 GPU; live inference on the Raspberry Pi; no cloud processing. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `adaptive_inference` | Unknown | keyword search of full text + methods/results read: Fixed SSD-300 model. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `resource_awareness` | Unknown | §2.2: SSD-300 chosen over SSD-512 for its published FPS: design-time choice, not a resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `multi_view` | Unknown | §1.2, §3: A single camera; the authors note that multiple angles add complexity. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `uncertainty` | Unknown | keyword search of full text + methods/results read: Probability scores are used for ranking and gating, but uncertainty is not estimated or calibrated. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `confidence_gating` | Unknown | §3: A wrapper algorithm checks each frame; if the probability score of a predicted defect exceeds a predefined value, it notifies the user whether to stop the print. | Yes | Resolves Unknown | Yes: approve before recoding |
| P016 | `anomaly_detection` | Unknown | §2.1, §2.2: Supervised SSD detector trained on annotated stringing images. | No | Resolves Unknown | Yes: approve before recoding |
| P016 | `latency_evaluation` | Unknown | §3: latency type: throughput/FPS. The setup ran at 14 FPS on live video, and at the same rate on the Raspberry Pi 4. The 59 FPS in the conclusions is the published SSD-300 benchmark, not the authors' measurement. | Yes | Resolves Unknown | Yes: approve before recoding |
| P016 | `accuracy_metrics` | (blank) | §3: Test set: precision 0.44 / recall 0.69 at IoU 0.4 (F1 0.55); 0.41 / 0.63 at IoU 0.5; 0.40 / 0.62 at IoU 0.6. Average precision 0.52 / 0.44 / 0.40 at IoU 0.4 / 0.5 / 0.6. Training set: precision 0.75, recall 0.92 | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P016 | `efficiency_metrics` | (blank) | §3: 14 FPS on live video, same rate reported on Raspberry Pi 4 | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P020 | `smartphone` | Unknown | §3, §4.1: Raspberry Pi camera; no smartphone. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `edge_device` | Unknown | §3, §4.1, §5.4: A Raspberry Pi 4B is described as "used for the processing" with a Pi camera and display, but all programming, training and testing were done in MATLAB. Where real-time classification runs is not stated. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P020 | `on_device` | Unknown | §3, §4.1, §5.4: Same ambiguity as edge_device. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P020 | `cloud` | Unknown | keyword search of full text + methods/results read: No cloud processing described. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `adaptive_inference` | Unknown | keyword search of full text + methods/results read: Fixed feature extractor + classifier. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `resource_awareness` | Unknown | keyword search of full text + methods/results read: No resource-driven decision. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `energy_evaluation` | Unknown | keyword search of full text + methods/results read: No energy or power measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: Printing temperature is a process parameter, not a device thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `multi_view` | Unknown | §4.2, §5.4: Four to five images per layer from one mounted camera are each classified individually; views are not used jointly. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `confidence_gating` | Unknown | §3.3: The ensemble uses a vote count to assign the final label; no downstream action is triggered by a confidence score. | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `anomaly_detection` | Unknown | §3.4, §5: Despite the "anomaly detection" wording, models are trained on manually labelled good and bad layer images (supervised; README §7.3, CD-14). | No | Resolves Unknown | Yes: approve before recoding |
| P020 | `accuracy_metrics` | (blank) | §5.1-§5.3, §6: AlexNet+SVM and EfficientNet-B0+SVM 99.70% (§5.1); ensemble with AlexNet features 100% (§5.2); density-wise classification ResNet50 100% (§5.3) | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P029 | `smartphone` | Unknown | §4.3.1: Implemented on three smartphones (Samsung Galaxy S8, Galaxy S7, LG Nexus 5; Android 7.0); results reported for the Galaxy S8. | Yes | Resolves Unknown | Yes: approve before recoding |
| P029 | `cloud` | Unknown | §6 (Related Work): The authors state the framework does not rely on cloud connectivity. | No | Resolves Unknown | Yes: approve before recoding |
| P029 | `thermal_evaluation` | Unknown | keyword search of full text: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P029 | `multi_view` | Unknown | keyword search of full text + methods/results read: Image classification benchmarks; no multi-view. | No | Resolves Unknown | Yes: approve before recoding |
| P029 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P029 | `confidence_gating` | Unknown | keyword search of full text + methods/results read: No confidence-triggered action. | No | Resolves Unknown | Yes: approve before recoding |
| P029 | `anomaly_detection` | Unknown | keyword search of full text + methods/results read: Supervised classification tasks. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `cloud` | Unknown | §4.4 (p. 4): The off-device agent runs on a desktop machine over a socket, not on a cloud datacenter. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `adaptive_inference` | Unknown | §4.2-§4.4 (pp. 3-4): Lotus scales CPU and GPU frequencies twice per frame via DRL; the detector models are unchanged. The two-width network belongs to the agent's Q-network, not the detector. The variable proposal count is an inherent property of the unmodified detectors. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `energy_evaluation` | Unknown | full text: Power is mentioned only as motivation; no energy or power results. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `multi_view` | Unknown | full text: KITTI and VisDrone2019 detection; no multi-view inspection. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `uncertainty` | Unknown | full text: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `confidence_gating` | Unknown | full text: No confidence-triggered action. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `anomaly_detection` | Unknown | full text: Object detection benchmarks. | No | Resolves Unknown | Yes: approve before recoding |
| P031 | `latency_evaluation` | Unknown | Tables 1-2 (pp. 4-5), §5.2.1: latency type: inference latency (mean and standard deviation per image on Jetson Orin Nano and Mi 11 Lite 5G). | Yes | Resolves Unknown | Yes: approve before recoding |
| P031 | `efficiency_metrics` | (blank) | §4.4.2, §5.2.1 (pp. 4-5): Jetson Orin Nano, MaskRCNN on VisDrone2019: latency -30.8% vs default governor and -9.1% vs zTT; latency standard deviation -72.8% / -38.1%; latency-constraint satisfaction +35.9% / +24.8% (§5.2.1). Mi 11 Lite 5G: latency variation -29.4% / -9.5% for MaskRCNN on KITTI; satisfaction rate 92.5% for FasterRCNN on VisDrone2019. Lotus overhead 8.52 ms per inference | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P033 | `smartphone` | Unknown | §6.3 (p. 60:19): Evaluated on three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71. | Yes | Resolves Unknown | Yes: approve before recoding |
| P033 | `cloud` | Unknown | Fig. 2 (p. 60:15): A server is used only for offline model conversion and evaluation; runtime inference is on the device. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `energy_evaluation` | Unknown | §4.1, §6.4 (p. 60:20), Fig. 2: Energy is an objective and is profiled on the device, but no energy results were found in §7. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P033 | `thermal_evaluation` | Unknown | §4.3.2, §6.4, §7 (keyword search): Overheating is discussed as a cause of processor issues and idle periods are used to keep temperatures consistent, but temperature is not measured or reported. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `multi_view` | Unknown | keyword search of full text + methods/results read: No multi-view. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `confidence_gating` | Unknown | keyword search of full text + methods/results read: No confidence-triggered action. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `anomaly_detection` | Unknown | keyword search of full text + methods/results read: Supervised tasks. | No | Resolves Unknown | Yes: approve before recoding |
| P033 | `latency_evaluation` | Unknown | §6.4, §7.1-§7.2, Fig. 8 (pp. 60:20-60:24): latency type: inference latency (average latency in ms per design) and throughput/FPS (images per second). | Yes | Resolves Unknown | Yes: approve before recoding |
| P033 | `accuracy_metrics` | (blank) | §7.1.2, §7.2.1: UC1 initial design on S20 (EfficientNet Lite0, FFX8, CPU): 75.11% accuracy; UC1 vs transferred baselines: +0.156 average accuracy | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P033 | `efficiency_metrics` | (blank) | §7.1.2, §7.2.1: Up to 4.06x over hardware-unaware multi-DNN designs; vs transferred baselines: UC1 +32.7% throughput, UC2 -2.8 MB model size and 19.9% latency speedup at equal accuracy; UC1 initial design memory footprint 16 MB | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P034 | `smartphone` | Unknown | §VI (p. 461): Evaluated on two mobile phones: Xiaomi Redmi Note 9 Pro and Google Pixel 6, using the TFLite benchmark tool on Android. | Yes | Resolves Unknown | Yes: approve before recoding |
| P034 | `cloud` | Unknown | §VI, Acknowledgment: Computing clusters used only for training; no cloud inference. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `energy_evaluation` | Unknown | §VI, Table VI (p. 463): Inference energy measured with a Power Profiler Kit (PPK2) on the Nordic nRF52840: 20-61 mJ for DS-CNN; switching < 0.01 mJ. | Yes | Resolves Unknown | Yes: approve before recoding |
| P034 | `thermal_evaluation` | Unknown | keyword search of full text + methods/results read: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `multi_view` | Unknown | keyword search of full text + methods/results read: No multi-view. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `uncertainty` | Unknown | keyword search of full text + methods/results read: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `confidence_gating` | Unknown | §VI, Fig. 11: Early-exit linear classifiers appear only as a comparison baseline; no confidence-triggered action in REDS. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `anomaly_detection` | Unknown | keyword search of full text + methods/results read: Supervised benchmark tasks. | No | Resolves Unknown | Yes: approve before recoding |
| P034 | `latency_evaluation` | Unknown | §VI, Fig. 10 (p. 462): latency type: inference latency (inference time on phones via TFLite benchmark and on IoT boards; e.g. 2-layer FC network on Arduino Nano 33 BLE Sense: 2,131 +/- 27 us at 25% MACs and 4,548 +/- 13 us at 50% MACs). | Yes | Resolves Unknown | Yes: approve before recoding |
| P034 | `efficiency_metrics` | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | §VI, Table VI (pp. 462-463): Adaptation time 38 +/- 1 us (2-layer FC network, Arduino Nano 33 BLE Sense); inference 2,131 +/- 27 us (25% MACs) and 4,548 +/- 13 us (50% MACs) on the same board; DS-CNN inference energy 20-61 mJ, switching < 0.01 mJ (nRF52840, PPK2) | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P013 | `smartphone` | Unknown | §4.2 (p. 7): Edge hardware is an industrial PC; no smartphone. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `edge_device` | Unknown | §4.2 (p. 7): Inference ("deployment") runs on an edge industrial PC with an Intel Celeron N2930 at the manufacturing line. Whether a low-power industrial PC counts as a resource-constrained edge device is the open industrial-PC question. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P013 | `on_device` | Unknown | §4.2 (p. 7): The edge PC receives SPI data files over TCP/IP; it is not the capturing device or physically attached to it. Leaning No, but the case depends on the same open question. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P013 | `cloud` | Unknown | §4.2 (p. 7), §5 (p. 8): Models are trained in a company-owned Spark cluster and data stored in AWS S3; inference runs on the edge device. Cloud used only for training and storage (README §7.3). | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `adaptive_inference` | Unknown | §3, §4: Static GBT model; "dynamic inspection" refers to routing parts, not to inference. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `resource_awareness` | Unknown | §3.4 (p. 5), §4.1 (p. 6): GBT chosen over SVM because its scoring time was eight times faster with future scaling in mind; real-time constraint set by takt time. A deployment-time choice under a timing constraint: depends on the open design-time question. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P013 | `energy_evaluation` | Unknown | §3.4: Energy constraints are listed in general terms; nothing is measured. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `thermal_evaluation` | Unknown | full text: No thermal measurement. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `multi_view` | Unknown | §4: Inputs are numeric SPI features, not images. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `uncertainty` | Unknown | full text: No uncertainty estimation. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `confidence_gating` | Unknown | §3.3 (p. 5), §4.2 (p. 6): Predicted class (with conservativeness tuning to avoid false negatives) decides which fields of view skip X-ray. No confidence score is described; whether a class-triggered routing decision counts needs a decision. | Keep Unknown (Ambiguous) | Ambiguous (no change) | Yes: researcher decision on the ambiguity |
| P013 | `anomaly_detection` | Unknown | §3.2, §4.1: Supervised classifiers trained on X-ray labels. | No | Resolves Unknown | Yes: approve before recoding |
| P013 | `latency_evaluation` | Unknown | Table 3 (p. 7), §4.2 (p. 7): Scoring times per 1,000 rows (Table 3, hardware not stated) and processing of current test sets in under one minute on the Intel Celeron N2930 edge PC. latency type: end-to-end latency (coarse bound on stated hardware). | Keep Unknown (Ambiguous; leaning Yes) | Ambiguous (leaning change) | Yes: researcher decision on the ambiguity |
| P013 | `accuracy_metrics` | (blank) | Tables 3-5 (p. 7): Initial balanced sample (Table 3): GBT accuracy 92.6%, recall 89.9%, precision 93.1%; SVM 92.9%. Conservative GBT on solder joints (Table 4): class recall 98.8% (defective) / 86.4% (defect-free). FOV level (Table 5): average X-ray inspection volume reduced by about 29% | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P013 | `efficiency_metrics` | (blank) | Table 3, §4.2 (p. 7): Scoring time per 1,000 rows (Table 3, hardware not stated): DT 6 ms, NB 9 ms, LR 27 ms, GBT 40 ms, SVM 360 ms. Edge PC (Intel Celeron N2930): current test sets processed in < 1 min. Edge-cloud link: 2-150 ms latency, about 1 Mbit/s per line | Replace/extend with full-text values (see report) | Free-text | Yes: approve before recoding |
| P013 | `application/domain` | Industrial Quality Inspection / Edge-Cloud / Predictive model-based quality inspection in SMT manufacturing | §1, §4 (pp. 1, 5-6): Key relevance finding: not image-based inspection. Relevance class decision is the researcher's. | No CSV change proposed; relevance class review | Relevance | Yes: researcher decision on relevance class (not changed in this step) |

## Counts

| Type | Rows |
| :-- | --: |
| Contradicts | 0 |
| Resolves Unknown | 112 |
| Ambiguous (leaning change) | 1 |
| Ambiguous (no change) | 15 |
| Free-text | 16 |
| Relevance | 2 |
| **Total** | **146** |

16 characteristic or metric rows are Ambiguous. They propose keeping the current value until the researcher decides.

## Contradictions of current Yes/No values

None.

## Relevance findings (no class changed)

- **P002 (proposed class A):** not image-based. The deployed classifier uses smartphone accelerometer signals; images are used only to auto-label the training data.
- **P013 (proposed class D):** not image-based. The ML input is numeric SPI measurements; inference runs on an edge industrial PC.

## Free-text refinements not listed above

Dataset, hardware, model and limitations refinements (Action = Change in the template's "Other evidence" rows) are recorded in [`fulltext_verification_template.md`](fulltext_verification_template.md). They enrich `Unknown` or abstract-level free text rather than contradict a coded value.
