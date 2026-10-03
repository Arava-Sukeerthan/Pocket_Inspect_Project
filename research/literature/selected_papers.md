# Selected Papers — Literature Batch 1

_Last updated: 2026-10-01. Records: 54 retained (P001–P054)._

_2026-10-03 (Step 8.3): the "Characteristics marked Yes" lines were regenerated from `papers.csv` after recoding under README §7 v1.1. `papers.csv` is the authoritative record; see `recoding_report.md` for every changed value. Other text in this file is unchanged from 2026-10-01 and may describe the earlier coding._

_2026-10-03 (Step 9.4): the "Characteristics marked Yes" lines for P002, P013, P015, P016, P020 and P034 were regenerated from `papers.csv` after the controlled full-text recoding; see `fulltext_recoding_applied.md`. Other text for these papers (e.g. Dataset / Model / Hardware lines) still reflects the abstract-level extraction._

**Epistemic status.** Every entry is a real publication. Its metadata was verified against Crossref and/or OpenAlex, and every DOI resolves through the doi.org handle registry. Characteristic fields were extracted from the **abstract only** (Fact = stated in the abstract). Anything the abstract does not state is recorded as `Unknown`, and full-text review is pending. Nothing in this file is a research-gap or novelty claim.

## Papers by search group

| Group | Theme | Papers |
| :-- | :-- | :-- |
| G1 | Smartphone / Mobile AI / On-device Edge AI | 7 (P001–P007) |
| G2 | Industrial Visual Inspection | 7 (P008–P014) |
| G3 | 3D-Printed Part Inspection | 10 (P015–P024) |
| G4 | Adaptive / Resource-Aware Inference | 12 (P025–P036) |
| G5 | Multi-view / Active Inspection | 8 (P037–P044) |
| G6 | Confidence / Uncertainty / Selective Prediction | 10 (P045–P054) |


## G1 — Smartphone / Mobile AI / On-device Edge AI

### P001 — Deep learning smartphone application for real‐time detection of defects in buildings

- **Authors:** Husein Perez; Joseph H. M. Tah
- **Year / Venue:** 2021 — Structural Control and Health Monitoring
- **DOI / URL:** [10.1002/stc.2751](https://doi.org/10.1002/stc.2751)
- **Application:** Real-time detection of building defects (cracks, mould, stain, paint deterioration)
- **Dataset / Model / Hardware:** Unknown / Deep learning model (architecture not stated in abstract) / Smartphone (model not stated in abstract)
- **Characteristics marked Yes:** smartphone
- **Why relevant:** Closest application-level analogue in this batch: a smartphone camera app used for visual defect inspection (civil domain, not manufactured parts).
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Closest application-level analogue in this batch: a smartphone camera app used for visual defect inspection (civil domain, not manufactured parts).
- **Notes:** Real-time claim stated without a reported latency figure in the abstract; full text needed for hardware and on-device confirmation.

**Evidence records**

> **Paper ID:** P001  
> **Claim:** The work develops a smartphone application for defect detection.  
> **Evidence:** Abstract describes a deep learning-based smartphone app for real-time detection of four building defect types.  
> **Source:** https://doi.org/10.1002/stc.2751 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P001  
> **Claim:** Inference location (on-device vs server).  
> **Evidence:** Abstract does not state where inference executes; on_device left Unknown.  
> **Source:** https://doi.org/10.1002/stc.2751 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P002 — A Road Defect Detection System Using Smartphones

- **Authors:** Gyulim Kim; Seungku Kim
- **Year / Venue:** 2024 — Sensors
- **DOI / URL:** [10.3390/s24072099](https://doi.org/10.3390/s24072099)
- **Application:** Road defect classification (speed bumps, manholes, potholes)
- **Dataset / Model / Hardware:** Automatically collected and labelled smartphone data / CNN-based classifier / Commercial smartphones
- **Characteristics marked Yes:** smartphone
- **Why relevant:** Shows smartphone-collected data and a smartphone-oriented CNN for defect classification; road domain.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Shows smartphone-collected data and a smartphone-oriented CNN for defect classification
- **Notes:** Abstract wording ('on smartphones') suggests but does not explicitly confirm on-device inference; on_device left Unknown pending full text.

**Evidence records**

> **Paper ID:** P002  
> **Claim:** Smartphone-based system.  
> **Evidence:** Abstract presents automatic data collection and a deep learning model for road defect detection on smartphones.  
> **Source:** https://doi.org/10.3390/s24072099 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P002  
> **Claim:** Speed evaluated.  
> **Evidence:** Abstract reports the CNN outperforms conventional models in accuracy and processing speed.  
> **Source:** https://doi.org/10.3390/s24072099 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P003 — AI Benchmark: All About Deep Learning on Smartphones in 2019

- **Authors:** Andrey Ignatov; Radu Timofte; Andrei Kulik; Seungsoo Yang; Ke Wang; Felix Baum; Max Wu; Lirong Xu; Luc Van Gool
- **Year / Venue:** 2019 — 2019 IEEE/CVF International Conference on Computer Vision Workshop (ICCVW)
- **DOI / URL:** [10.1109/iccvw.2019.00447](https://doi.org/10.1109/iccvw.2019.00447)
- **Application:** Benchmarking AI inference acceleration on smartphone SoCs
- **Dataset / Model / Hardware:** AI Benchmark tasks / Multiple DNNs / Mobile chipsets from Qualcomm, HiSilicon, Samsung, MediaTek, Unisoc
- **Characteristics marked Yes:** smartphone, edge_device, on_device
- **Why relevant:** Reference for how heterogeneous smartphone accelerators differ, relevant to running inspection models on older or low-resource phones.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Reference for how heterogeneous smartphone accelerators differ, relevant to running inspection models on older or low-resource phones.
- **Notes:** Performance benchmarking; latency_evaluation=Yes refers to accelerator performance benchmarking.

**Evidence records**

> **Paper ID:** P003  
> **Claim:** On-device smartphone inference is evaluated.  
> **Evidence:** Abstract evaluates performance of all chipsets from five vendors that provide hardware acceleration for AI inference on mobile devices.  
> **Source:** https://doi.org/10.1109/iccvw.2019.00447 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P003  
> **Claim:** Android ML pipeline discussed.  
> **Evidence:** Abstract discusses recent changes in the Android ML pipeline and deployment of DL models on mobile devices.  
> **Source:** https://doi.org/10.1109/iccvw.2019.00447 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P004 — Guidelines and Benchmarks for Deployment of Deep Learning Models on Smartphones as Real-Time Apps

- **Authors:** Abhishek Sehgal; Nasser Kehtarnavaz
- **Year / Venue:** 2019 — Machine Learning and Knowledge Extraction
- **DOI / URL:** [10.3390/make1010027](https://doi.org/10.3390/make1010027)
- **Application:** Real-time deployment of DL inference networks as smartphone apps
- **Dataset / Model / Hardware:** Unknown / Six CNN models / Android and iOS smartphones
- **Characteristics marked Yes:** smartphone, edge_device, on_device, latency_evaluation
- **Why relevant:** Practical deployment and benchmarking methodology (accuracy, CPU/GPU use, throughput) relevant to PocketInspect's evaluation protocol.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Practical deployment and benchmarking methodology (accuracy, CPU/GPU use, throughput) relevant to PocketInspect's evaluation protocol.

**Evidence records**

> **Paper ID:** P004  
> **Claim:** On-device smartphone deployment.  
> **Evidence:** Abstract devises a uniform implementation flow for real-time deployment of DL inference networks on Android and iOS smartphones.  
> **Source:** https://doi.org/10.3390/make1010027 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P004  
> **Claim:** Resource and throughput benchmarking.  
> **Evidence:** Benchmarking framework covers accuracy, CPU/GPU consumption and real-time throughput; multi-threading used to improve throughput.  
> **Source:** https://doi.org/10.3390/make1010027 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P005 — A First Look at Deep Learning Apps on Smartphones

- **Authors:** Mengwei Xu; Jiawei Liu; Yuanqiang Liu; Felix Xiaozhu Lin; Yunxin Liu; Xuanzhe Liu
- **Year / Venue:** 2019 — The World Wide Web Conference
- **DOI / URL:** [10.1145/3308558.3313591](https://doi.org/10.1145/3308558.3313591)
- **Application:** Empirical study of deep learning usage in Android apps
- **Dataset / Model / Hardware:** 16,500 popular Android apps / DL models extracted from apps / Android smartphones
- **Characteristics marked Yes:** smartphone
- **Why relevant:** Context on how DL is actually deployed on smartphones; not an inspection paper.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Context on how DL is actually deployed on smartphones
- **Notes:** Any priority wording in the title is the authors' own and is not adopted by PocketInspect.

**Evidence records**

> **Paper ID:** P005  
> **Claim:** Studies DL models deployed in smartphone apps.  
> **Evidence:** Abstract reports an empirical study of 16,500 popular Android apps using a static tool to analyse their deep learning functions and models.  
> **Source:** https://doi.org/10.1145/3308558.3313591 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P006 — Smart at what cost?: Characterising Mobile Deep Neural Networks in the Wild

- **Authors:** Mario Almeida; Stefanos Laskaridis; Abhinav Mehrotra; Lukasz Dudziak; Ilias Leontiadis; Nicholas D. Lane
- **Year / Venue:** 2021 — Proceedings of the 21st ACM Internet Measurement Conference
- **DOI / URL:** [10.1145/3487552.3487863](https://doi.org/10.1145/3487552.3487863)
- **Application:** Measurement of DNN deployment and performance across smartphones
- **Dataset / Model / Hardware:** Over 16k popular Google Play apps / DNNs extracted from apps / Smartphones across tiers and generations
- **Characteristics marked Yes:** smartphone, edge_device, on_device, energy_evaluation
- **Why relevant:** Directly relevant to device heterogeneity (older vs newer phones) and energy cost of on-device inference.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Directly relevant to device heterogeneity (older vs newer phones) and energy cost of on-device inference.
- **Notes:** Title on Crossref: 'Smart at what cost?'; full title includes 'Characterising Mobile Deep Neural Networks in the wild'.

**Evidence records**

> **Paper ID:** P006  
> **Claim:** On-device DNN performance measured across device tiers.  
> **Evidence:** Abstract analyses over 16k apps and measures how their DNNs run on devices of different capabilities across tiers and generations.  
> **Source:** https://doi.org/10.1145/3487552.3487863 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P006  
> **Claim:** Energy measured.  
> **Evidence:** Abstract states the models' energy footprint is measured; the gaugeNN tool automates deployment and measurement.  
> **Source:** https://doi.org/10.1145/3487552.3487863 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P007 — Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective

- **Authors:** Muhammad Haroon Asad; Saran Khaliq; Muhammad Haroon Yousaf; Muhammad Obaid Ullah; Afaq Ahmad
- **Year / Venue:** 2022 — Advances in Civil Engineering
- **DOI / URL:** [10.1155/2022/9221211](https://doi.org/10.1155/2022/9221211)
- **Application:** Real-time pothole detection on an edge AI device
- **Dataset / Model / Hardware:** Pothole image dataset (diverse road and illumination conditions) plus real-time vehicle video / YOLOv1-v5, Tiny-YOLOv4, SSD-MobileNetV2 / OAK-D AI kit on Raspberry Pi
- **Characteristics marked Yes:** edge_device, on_device, latency_evaluation
- **Why relevant:** Comparator for low-cost non-smartphone edge hardware running lightweight detectors in real time.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Comparator for low-cost non-smartphone edge hardware running lightweight detectors in real time.
- **Reported metrics (abstract):** mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy at 31.76 FPS on OAK-D
- **Notes:** smartphone=No because the abstract explicitly specifies OAK-D + Raspberry Pi hardware.

**Evidence records**

> **Paper ID:** P007  
> **Claim:** Edge deployment on low-cost hardware.  
> **Evidence:** Abstract deploys detectors on OAK-D attached to a Raspberry Pi as the edge platform.  
> **Source:** https://doi.org/10.1155/2022/9221211 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P007  
> **Claim:** Latency/FPS reported.  
> **Evidence:** Abstract reports Tiny-YOLOv4 at 90% detection accuracy and 31.76 FPS.  
> **Source:** https://doi.org/10.1155/2022/9221211 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)


## G2 — Industrial Visual Inspection

### P008 — Segmentation-based deep-learning approach for surface-defect detection

- **Authors:** Domen Tabernik; Samo Šela; Jure Skvarč; Danijel Skočaj
- **Year / Venue:** 2019 — Journal of Intelligent Manufacturing
- **DOI / URL:** [10.1007/s10845-019-01476-x](https://doi.org/10.1007/s10845-019-01476-x)
- **Application:** Surface-crack detection and segmentation for quality control
- **Dataset / Model / Hardware:** Newly created real-world quality-control dataset (publicly released) / Segmentation-based deep learning architecture / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Small-data supervised surface-defect segmentation, relevant because PocketInspect will likely have few defective 3D-printed samples.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Small-data supervised surface-defect segmentation, relevant because PocketInspect will likely have few defective 3D-printed samples.
- **Notes:** Abstract mentions experiments on required computational cost but gives no device or latency figures.

**Evidence records**

> **Paper ID:** P008  
> **Claim:** Learns from few defective samples.  
> **Evidence:** Abstract reports learning from roughly 25-30 defective training samples.  
> **Source:** https://doi.org/10.1007/s10845-019-01476-x (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P008  
> **Claim:** Dataset released.  
> **Evidence:** Abstract states the dataset is based on a real quality-control case and made publicly available.  
> **Source:** https://doi.org/10.1007/s10845-019-01476-x (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

### P009 — MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection

- **Authors:** Paul Bergmann; Michael Fauser; David Sattlegger; Carsten Steger
- **Year / Venue:** 2019 — 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
- **DOI / URL:** [10.1109/cvpr.2019.00982](https://doi.org/10.1109/cvpr.2019.00982)
- **Application:** Unsupervised anomaly detection benchmark dataset
- **Dataset / Model / Hardware:** MVTec AD (5,354 high-resolution images; >70 defect types; pixel-level ground truth) / Benchmarked: convolutional autoencoders, GANs, pretrained-CNN feature descriptors, classical methods / Unknown
- **Characteristics marked Yes:** anomaly_detection
- **Why relevant:** Standard benchmark for industrial anomaly detection; candidate evaluation reference.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Standard benchmark for industrial anomaly detection

**Evidence records**

> **Paper ID:** P009  
> **Claim:** Unsupervised anomaly detection dataset.  
> **Evidence:** Abstract introduces MVTec AD with defect-free training images and anomalous test images with pixel-precise ground truth.  
> **Source:** https://doi.org/10.1109/cvpr.2019.00982 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P009  
> **Claim:** Benchmark of methods.  
> **Evidence:** Abstract evaluates deep and classical unsupervised anomaly detection methods.  
> **Source:** https://doi.org/10.1109/cvpr.2019.00982 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P010 — Deep Learning for Automated Visual Inspection in Manufacturing and Maintenance: A Survey of Open- Access Papers

- **Authors:** Nils Hütten; Miguel Alves Gomes; Florian Hölken; Karlo Andricevic; Richard Meyes; Tobias Meisen
- **Year / Venue:** 2024 — Applied System Innovation
- **DOI / URL:** [10.3390/asi7010011](https://doi.org/10.3390/asi7010011)
- **Application:** Survey of deep learning for automated visual inspection in manufacturing and maintenance
- **Dataset / Model / Hardware:** 196 open-access publications / Survey (CNNs dominant; vision transformers emerging) / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Survey baseline for industrial AVI; its findings on dataset sizes and supervision are useful context.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Survey baseline for industrial AVI
- **Notes:** Survey; device-related fields not applicable at abstract level.

**Evidence records**

> **Paper ID:** P010  
> **Claim:** Survey scope.  
> **Evidence:** Abstract surveys 196 open-access publications (31.7% manufacturing, 68.3% maintenance use cases).  
> **Source:** https://doi.org/10.3390/asi7010011 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P010  
> **Claim:** Reported findings.  
> **Evidence:** Abstract reports 97% use supervised learning, median dataset size 2,500 samples, and an approximately three-year lag between CV research and industrial inspection uptake.  
> **Source:** https://doi.org/10.3390/asi7010011 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P011 — XEdgeAI: A human-centered industrial inspection framework with data-centric Explainable Edge AI approach

- **Authors:** Hung Truong Thanh Nguyen; Loc Phuc Truong Nguyen; Hung Cao
- **Year / Venue:** 2025 — Information Fusion
- **DOI / URL:** [10.1016/j.inffus.2024.102782](https://doi.org/10.1016/j.inffus.2024.102782)
- **Application:** Explainable visual quality inspection with semantic segmentation on low-resource edge devices
- **Dataset / Model / Hardware:** Unknown / Semantic segmentation model + XAI + Large Vision Language Model explanations / Low-resource edge / mobile devices (models not stated in abstract)
- **Characteristics marked Yes:** edge_device, on_device
- **Why relevant:** Industrial inspection framework explicitly targeting low-resource mobile/edge deployment.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Industrial inspection framework explicitly targeting low-resource mobile/edge deployment.
- **Notes:** 'Mobile devices' in abstract; smartphone use not explicitly confirmed, so smartphone=Unknown. Crossref issued year 2025; OpenAlex lists 2024 (online ahead of print).

**Evidence records**

> **Paper ID:** P011  
> **Claim:** Edge deployment.  
> **Evidence:** Abstract targets deployment of semantic segmentation models on low-resource edge devices.  
> **Source:** https://doi.org/10.1016/j.inffus.2024.102782 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P011  
> **Claim:** Mobile deployment reported.  
> **Evidence:** Abstract states the enhanced model is deployed on mobile devices, with competitive accuracy and significantly reduced model size.  
> **Source:** https://doi.org/10.1016/j.inffus.2024.102782 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P012 — Real-Time Defect Detection Model in Industrial Environment Based on Lightweight Deep Learning Network

- **Authors:** Jiaqi Lu; Soo-Hong Lee
- **Year / Venue:** 2023 — Electronics
- **DOI / URL:** [10.3390/electronics12214388](https://doi.org/10.3390/electronics12214388)
- **Application:** Lightweight real-time industrial surface defect detection
- **Dataset / Model / Hardware:** Four public datasets (names not in abstract) / Lightweight detector: attention backbone, multiscale aggregation, residual and attention enhancement networks / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Lightweight detector design for industrial defects; candidate baseline family.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Lightweight detector design for industrial defects
- **Reported metrics (abstract):** Outperforms YOLOv5n and YOLOv8n on P, R, F1, mAP@.5 and GFLOPS (values not in abstract)
- **Notes:** Edge/mobile deployment is a motivation; no on-device evaluation is stated in the abstract, so edge_device and on_device stay Unknown.

**Evidence records**

> **Paper ID:** P012  
> **Claim:** Lightweight design motivated by GPU-less/edge deployment.  
> **Evidence:** Abstract motivates a lightweight network because general detectors are hard to deploy on devices without GPUs or on edge and mobile devices.  
> **Source:** https://doi.org/10.3390/electronics12214388 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P012  
> **Claim:** Compared with YOLO nano models.  
> **Evidence:** Abstract reports better P, R, F1, mAP@.5 and GFLOPS than YOLOv5n and YOLOv8n on four public datasets.  
> **Source:** https://doi.org/10.3390/electronics12214388 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P013 — Predictive model-based quality inspection using Machine Learning and Edge Cloud Computing

- **Authors:** Jacqueline Schmitt; Jochen Bönig; Thorbjörn Borggräfe; Gunter Beitinger; Jochen Deuse
- **Year / Venue:** 2020 — Advanced Engineering Informatics
- **DOI / URL:** [10.1016/j.aei.2020.101101](https://doi.org/10.1016/j.aei.2020.101101)
- **Application:** Predictive model-based quality inspection in SMT manufacturing
- **Dataset / Model / Hardware:** Real industrial SMT use case / Machine learning (models not stated in abstract) / Edge Cloud Computing infrastructure
- **Characteristics marked Yes:** edge_device, on_device
- **Why relevant:** Shows edge-cloud deployment for reducing inspection load; relevant to deciding when full inspection is needed.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Shows edge-cloud deployment for reducing inspection load
- **Notes:** Abstract does not state that the approach is image-based; it may rely on process data. Treat as system-level context, not a CV baseline.

**Evidence records**

> **Paper ID:** P013  
> **Claim:** Edge cloud computing used.  
> **Evidence:** Abstract investigates predictive model-based quality inspection using ML and Edge Cloud Computing in the existing plant IT infrastructure.  
> **Source:** https://doi.org/10.1016/j.aei.2020.101101 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P013  
> **Claim:** Outcome.  
> **Evidence:** Abstract reports inspection volumes can be reduced significantly.  
> **Source:** https://doi.org/10.1016/j.aei.2020.101101 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P014 — A Real-Time Automated Defect Detection System for Ceramic Pieces Manufacturing Process Based on Computer Vision with Deep Learning

- **Authors:** Esteban Cumbajin; Nuno Rodrigues; Paulo Costa; Rolando Miragaia; Luís Frazão; Nuno Costa; Antonio Fernández-Caballero; Jorge Carneiro; Leire H. Buruberri; António Pereira
- **Year / Venue:** 2023 — Sensors
- **DOI / URL:** [10.3390/s24010232](https://doi.org/10.3390/s24010232)
- **Application:** Real-time defect detection on ceramic pieces in production
- **Dataset / Model / Hardware:** Images from in-house acquisition and labelling platform / CNN-based classifier / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** End-to-end industrial pipeline (acquisition, labelling, preprocessing, CNN) for small manufactured items.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** End-to-end industrial pipeline (acquisition, labelling, preprocessing, CNN) for small manufactured items.
- **Reported metrics (abstract):** Accuracy 98.00%, F1 97.29%
- **Notes:** Real-time claim without latency figure in abstract.

**Evidence records**

> **Paper ID:** P014  
> **Claim:** Industrial deployment.  
> **Evidence:** Abstract describes a CNN-based system that runs in real time and was implemented and evaluated at a Portuguese tableware manufacturer.  
> **Source:** https://doi.org/10.3390/s24010232 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P014  
> **Claim:** Metrics.  
> **Evidence:** Abstract reports 98.00% accuracy and 97.29% F1-score.  
> **Source:** https://doi.org/10.3390/s24010232 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)


## G3 — 3D-Printed Part Inspection

### P015 — Generalisable 3D printing error detection and correction via multi-head neural networks

- **Authors:** Douglas A. J. Brion; Sebastian W. Pattinson
- **Year / Venue:** 2022 — Nature Communications
- **DOI / URL:** [10.1038/s41467-022-31985-y](https://doi.org/10.1038/s41467-022-31985-y)
- **Application:** Real-time error detection and correction in material extrusion 3D printing
- **Dataset / Model / Hardware:** 1.2 million images from 192 parts labelled with printing parameters / Multi-head neural network with control loop / Unknown
- **Characteristics marked Yes:** none (full-text extraction)
- **Why relevant:** Key 3D-printing monitoring reference; in-process (during printing) rather than post-print part inspection.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Key 3D-printing monitoring reference

**Evidence records**

> **Paper ID:** P015  
> **Claim:** Large automatically labelled dataset.  
> **Evidence:** Abstract reports 1.2 million images from 192 parts labelled by deviation from optimal printing parameters.  
> **Source:** https://doi.org/10.1038/s41467-022-31985-y (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P015  
> **Claim:** Real-time detection and correction.  
> **Evidence:** Abstract states the network plus control loop enables real-time detection and rapid correction across geometries, materials, printers and toolpaths.  
> **Source:** https://doi.org/10.1038/s41467-022-31985-y (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P016 — Real-Time 3D Printing Remote Defect Detection (Stringing) with Computer Vision and Artificial Intelligence

- **Authors:** Konstantinos Paraskevoudis; Panagiotis Karayannis; Elias P. Koumoulos
- **Year / Venue:** 2020 — Processes
- **DOI / URL:** [10.3390/pr8111464](https://doi.org/10.3390/pr8111464)
- **Application:** Real-time stringing defect detection during FFF printing from camera video
- **Dataset / Model / Hardware:** Images showing stringing defects / Deep CNN / Microprocessor plus camera (not specified in abstract)
- **Characteristics marked Yes:** edge_device, on_device, confidence_gating, latency_evaluation
- **Why relevant:** In-process camera-based 3D-printing defect detection with live deployment.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** In-process camera-based 3D-printing defect detection with live deployment.
- **Notes:** Hardware described only generically; edge_device left Unknown.

**Evidence records**

> **Paper ID:** P016  
> **Claim:** Video-based in-process detection.  
> **Evidence:** Abstract trains a deep CNN on stringing images and deploys it on a live video camera feed during printing.  
> **Source:** https://doi.org/10.3390/pr8111464 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P017 — Automated Process Monitoring in 3D Printing Using Supervised Machine Learning

- **Authors:** Ugandhar Delli; Shing Chang
- **Year / Venue:** 2018 — Procedia Manufacturing
- **DOI / URL:** [10.1016/j.promfg.2018.07.111](https://doi.org/10.1016/j.promfg.2018.07.111)
- **Application:** Good/defective classification of semi-finished 3D printed parts
- **Dataset / Model / Hardware:** ABS and PLA printed parts imaged at critical print stages / Support vector machine / Camera integrated with printer
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Early camera-plus-ML 3D-print quality check; shows staged image capture.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Early camera-plus-ML 3D-print quality check
- **Notes:** Images are taken at different print stages (temporal), not from multiple viewpoints; multi_view left Unknown.

**Evidence records**

> **Paper ID:** P017  
> **Claim:** Camera images at multiple print stages.  
> **Evidence:** Abstract takes images of semi-finished parts at several critical stages and classifies them with an SVM as good or defective.  
> **Source:** https://doi.org/10.1016/j.promfg.2018.07.111 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P018 — Real-time defect detection for FFF 3D printing using lightweight model deployment

- **Authors:** WenJing Hu; Chang Chen; Shaohui Su; Jian Zhang; An Zhu
- **Year / Venue:** 2024 — The International Journal of Advanced Manufacturing Technology
- **DOI / URL:** [10.1007/s00170-024-14452-4](https://doi.org/10.1007/s00170-024-14452-4)
- **Application:** Real-time detection of five common FFF printing defects
- **Dataset / Model / Hardware:** Deliberately designed defect dataset (five defect types) / Improved YOLOv8 with lightweight group-convolution detection head / Unknown
- **Characteristics marked Yes:** latency_evaluation
- **Why relevant:** Lightweight detector for FFF defects; closest in task to PocketInspect's 3D-print defect classes.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Lightweight detector for FFF defects
- **Reported metrics (abstract):** mAP50 97.5%; FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8
- **Notes:** Abstract retrieved from the Springer landing page.

**Evidence records**

> **Paper ID:** P018  
> **Claim:** Lightweight detector for FFF defects.  
> **Evidence:** Abstract reports an improved YOLOv8 head using group convolution, reaching 97.5% mAP50 with 18.1% higher FPS and 32.9% fewer GFLOPs.  
> **Source:** https://doi.org/10.1007/s00170-024-14452-4 (abstract via Springer landing page)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P018  
> **Claim:** Real-time system.  
> **Evidence:** Abstract states the model is integrated into a real-time detection system that alerts on defects.  
> **Source:** https://doi.org/10.1007/s00170-024-14452-4 (abstract via Springer landing page)  
> **Evidence status:** Verified (abstract-level)

### P019 — Real-time defect detection in 3D printing using machine learning

- **Authors:** Mohammad Farhan Khan; Aftaab Alam; Mohammad Ateeb Siddiqui; Mohammad Saad Alam; Yasser Rafat; Nehal Salik; Ibrahim Al-Saidan
- **Year / Venue:** 2021 — Materials Today: Proceedings
- **DOI / URL:** [10.1016/j.matpr.2020.10.482](https://doi.org/10.1016/j.matpr.2020.10.482)
- **Application:** Real-time detection of infill defects in 3D printing
- **Dataset / Model / Hardware:** Unknown / CNN image classifier / Camera integrated with 3D printer
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Simple camera-plus-CNN in-process monitoring baseline.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Simple camera-plus-CNN in-process monitoring baseline.
- **Notes:** Crossref issued year 2021; OpenAlex lists 2020.

**Evidence records**

> **Paper ID:** P019  
> **Claim:** Camera images classified by CNN.  
> **Evidence:** Abstract captures images at regular intervals with a printer-integrated camera and classifies infill anomalies with a CNN.  
> **Source:** https://doi.org/10.1016/j.matpr.2020.10.482 (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

### P020 — Enhancing Surface Fault Detection Using Machine Learning for 3D Printed Products

- **Authors:** Vaibhav Kadam; Satish Kumar; Arunkumar Bongale; Seema Wazarkar; Pooja Kamat; Shruti Patil
- **Year / Venue:** 2021 — Applied System Innovation
- **DOI / URL:** [10.3390/asi4020034](https://doi.org/10.3390/asi4020034)
- **Application:** Layer-wise fault detection in FDM printing
- **Dataset / Model / Hardware:** Unknown / Pretrained CNN features + ML classifiers (AlexNet + SVM best) / Unknown
- **Characteristics marked Yes:** none (full-text extraction)
- **Why relevant:** Low-compute-cost FDM fault detection.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Low-compute-cost FDM fault detection.
- **Notes:** Abstract uses the term 'anomaly detection' but describes supervised classifiers; anomaly_detection left Unknown.

**Evidence records**

> **Paper ID:** P020  
> **Claim:** Layer-wise detection.  
> **Evidence:** Abstract performs layer-wise anomaly detection in FDM using pre-trained models combined with ML algorithms; AlexNet+SVM gave the highest accuracy.  
> **Source:** https://doi.org/10.3390/asi4020034 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P021 — Geometrical defect detection for additive manufacturing with machine learning models

- **Authors:** Rui Li; Mingzhou Jin; Vincent C. Paquit
- **Year / Venue:** 2021 — Materials & Design
- **DOI / URL:** [10.1016/j.matdes.2021.109726](https://doi.org/10.1016/j.matdes.2021.109726)
- **Application:** Geometric defect detection of additively manufactured objects from 3D point clouds
- **Dataset / Model / Hardware:** Synthetic 3D point clouds with defects; experimental prints / Bagging, Gradient Boosting, Random Forest, KNN, Linear SVM / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Geometry-based (3D) rather than camera-image inspection; useful contrast to 2D smartphone imaging.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Geometry-based (3D) rather than camera-image inspection
- **Notes:** Uses 3D point clouds, not RGB images.

**Evidence records**

> **Paper ID:** P021  
> **Claim:** Point-cloud based detection.  
> **Evidence:** Abstract trains ML models on synthetic defective point clouds and applies them to real prints; Bagging and Random Forest performed best.  
> **Source:** https://doi.org/10.1016/j.matdes.2021.109726 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P022 — Defect detection in 3D-printed polymer parts using deep learning models: a comparative investigation

- **Authors:** Vivek V. Bhandarkar; Mohan Karnati; Puneet Tandon
- **Year / Venue:** 2025 — Rapid Prototyping Journal
- **DOI / URL:** [10.1108/rpj-09-2024-0395](https://doi.org/10.1108/rpj-09-2024-0395)
- **Application:** Warping, stringing and cracking detection in 3D-printed PLA/ABS parts
- **Dataset / Model / Hardware:** Defect images from Taguchi L9 design (extruder temp, bed temp, print speed) on a Delta printer / DenseNet121, MobileNetV2, ResNet50, VGG16, XceptionNet (transfer learning) / Raspberry Pi-based data acquisition
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Directly matches PocketInspect's 3D-printed part defect types; MobileNetV2 result is relevant to mobile-friendly models.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Directly matches PocketInspect's 3D-printed part defect types
- **Reported metrics (abstract):** Warping 98.59% (DenseNet121); stringing 99.38% (MobileNetV2); cracking 99.32% (XceptionNet); multi-class 98.90% (MobileNetV2)
- **Notes:** Raspberry Pi is used for data acquisition; abstract does not say inference runs on it, so edge_device/on_device stay Unknown.

**Evidence records**

> **Paper ID:** P022  
> **Claim:** Defect types and models.  
> **Evidence:** Abstract compares five transfer-learned CNNs for warping, stringing and cracking, individually and multi-class.  
> **Source:** https://doi.org/10.1108/rpj-09-2024-0395 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P022  
> **Claim:** MobileNetV2 strongest for multi-class.  
> **Evidence:** Abstract reports MobileNetV2 achieved 98.90% accuracy for multiple-defect detection.  
> **Source:** https://doi.org/10.1108/rpj-09-2024-0395 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P023 — Autonomous in-situ correction of fused deposition modeling printers using computer vision and deep learning

- **Authors:** Zeqing Jin; Zhizhou Zhang; Grace X. Gu
- **Year / Venue:** 2019 — Manufacturing Letters
- **DOI / URL:** [10.1016/j.mfglet.2019.09.005](https://doi.org/10.1016/j.mfglet.2019.09.005)
- **Application:** Real-time monitoring and autonomous correction of FDM extrusion errors
- **Dataset / Model / Hardware:** Unknown / Deep learning model with feedback loop / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Closed-loop vision for FDM; shows acting on predictions rather than only flagging.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Closed-loop vision for FDM
- **Notes:** Adaptation here is of printer parameters, not of the inference pipeline; adaptive_inference left Unknown.

**Evidence records**

> **Paper ID:** P023  
> **Claim:** Closed-loop correction.  
> **Evidence:** Abstract describes a real-time monitoring and autonomous correction system that uses a deep learning model and feedback loop to adjust printing parameters.  
> **Source:** https://doi.org/10.1016/j.mfglet.2019.09.005 (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

### P024 — A review on machine learning in 3D printing: applications, potential, and challenges

- **Authors:** G. D. Goh; S. L. Sing; W. Y. Yeong
- **Year / Venue:** 2020 — Artificial Intelligence Review
- **DOI / URL:** [10.1007/s10462-020-09876-9](https://doi.org/10.1007/s10462-020-09876-9)
- **Application:** Review of machine learning across the additive manufacturing workflow
- **Dataset / Model / Hardware:** Review / Review / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Review baseline for ML in 3D printing.
- **Limitations (author-stated):** Authors list computational cost, qualification standards and data acquisition techniques as open challenges (abstract).
- **PocketInspect relevance:** Review baseline for ML in 3D printing.
- **Notes:** Abstract retrieved from the Springer landing page.

**Evidence records**

> **Paper ID:** P024  
> **Claim:** Review scope.  
> **Evidence:** Abstract reviews ML for design, material tuning, process optimisation, in-situ monitoring, cloud service and cybersecurity in AM.  
> **Source:** https://doi.org/10.1007/s10462-020-09876-9 (abstract via Springer landing page)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P024  
> **Claim:** Stated challenges.  
> **Evidence:** Abstract names computational cost, qualification standards and data acquisition as challenges and calls for data sharing standards.  
> **Source:** https://doi.org/10.1007/s10462-020-09876-9 (abstract via Springer landing page)  
> **Evidence status:** Verified (abstract-level)


## G4 — Adaptive / Resource-Aware Inference

### P025 — BranchyNet: Fast inference via early exiting from deep neural networks

- **Authors:** Surat Teerapittayanon; Bradley McDanel; H.T. Kung
- **Year / Venue:** 2016 — 2016 23rd International Conference on Pattern Recognition (ICPR)
- **DOI / URL:** [10.1109/icpr.2016.7900006](https://doi.org/10.1109/icpr.2016.7900006)
- **Application:** Early-exit deep networks for faster inference
- **Dataset / Model / Hardware:** MNIST, CIFAR10 / BranchyNet applied to LeNet, AlexNet, ResNet / Unknown
- **Characteristics marked Yes:** adaptive_inference, confidence_gating
- **Why relevant:** Foundational confidence-gated adaptive inference; directly related to confidence-triggered extra computation or recapture.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Foundational confidence-gated adaptive inference
- **Notes:** uncertainty=Yes because prediction confidence is explicitly used for the exit decision; this is not a calibrated uncertainty estimate. Pre-2019 foundational paper.

**Evidence records**

> **Paper ID:** P025  
> **Claim:** Confidence-based early exit.  
> **Evidence:** Abstract adds side-branch classifiers so samples exit early when they can be inferred with high confidence.  
> **Source:** https://doi.org/10.1109/icpr.2016.7900006 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P025  
> **Claim:** Inference time reduced.  
> **Evidence:** Abstract reports improved accuracy and significantly reduced inference time.  
> **Source:** https://doi.org/10.1109/icpr.2016.7900006 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P026 — Dynamic Neural Networks: A Survey

- **Authors:** Yizeng Han; Gao Huang; Shiji Song; Le Yang; Honghui Wang; Yulin Wang
- **Year / Venue:** 2022 — IEEE Transactions on Pattern Analysis and Machine Intelligence
- **DOI / URL:** [10.1109/tpami.2021.3117837](https://doi.org/10.1109/tpami.2021.3117837)
- **Application:** Survey of dynamic neural networks
- **Dataset / Model / Hardware:** Survey / Sample-wise, spatial-wise and temporal-wise dynamic networks / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Taxonomy reference for adaptive inference design options.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Taxonomy reference for adaptive inference design options.
- **Notes:** Survey. Crossref issued year 2022; OpenAlex lists 2021 (early access).

**Evidence records**

> **Paper ID:** P026  
> **Claim:** Survey taxonomy.  
> **Evidence:** Abstract categorises dynamic networks into sample-wise, spatial-wise and temporal-wise models and reviews design, decision schemes and optimisation.  
> **Source:** https://doi.org/10.1109/tpami.2021.3117837 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P027 — Edge AI: On-Demand Accelerating Deep Neural Network Inference via Edge Computing

- **Authors:** En Li; Liekang Zeng; Zhi Zhou; Xu Chen
- **Year / Venue:** 2020 — IEEE Transactions on Wireless Communications
- **DOI / URL:** [10.1109/twc.2019.2946140](https://doi.org/10.1109/twc.2019.2946140)
- **Application:** Device-edge collaborative DNN inference with partitioning and early exit
- **Dataset / Model / Hardware:** Unknown / Edgent (DNN partitioning + right-sizing via early exit) / Raspberry Pi and desktop PC prototype
- **Characteristics marked Yes:** edge_device, adaptive_inference, resource_awareness
- **Why relevant:** Accuracy-latency trade-off under changing conditions; offloading is an alternative PocketInspect may compare against.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Accuracy-latency trade-off under changing conditions
- **Notes:** Offloads to a proximal edge server, not explicitly a cloud datacenter; cloud left Unknown. Crossref issued year 2020; OpenAlex lists 2019.

**Evidence records**

> **Paper ID:** P027  
> **Claim:** Adaptive partitioning and early exit.  
> **Evidence:** Abstract describes adaptive DNN partitioning between device and edge plus early-exit right-sizing.  
> **Source:** https://doi.org/10.1109/twc.2019.2946140 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P027  
> **Claim:** Bandwidth-aware runtime adaptation.  
> **Evidence:** Abstract uses regression models in static and online change-point detection in dynamic bandwidth environments.  
> **Source:** https://doi.org/10.1109/twc.2019.2946140 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P027  
> **Claim:** Prototype hardware.  
> **Evidence:** Abstract implements a Raspberry Pi and desktop PC prototype.  
> **Source:** https://doi.org/10.1109/twc.2019.2946140 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P028 — Neurosurgeon: Collaborative Intelligence Between the Cloud and Mobile Edge

- **Authors:** Yiping Kang; Johann Hauswald; Cao Gao; Austin Rovinski; Trevor Mudge; Jason Mars; Lingjia Tang
- **Year / Venue:** 2017 — Proceedings of the Twenty-Second International Conference on Architectural Support for Programming Languages and Operating Systems
- **DOI / URL:** [10.1145/3037697.3037698](https://doi.org/10.1145/3037697.3037698)
- **Application:** Layer-level DNN partitioning between mobile device and datacenter
- **Dataset / Model / Hardware:** 8 intelligent applications (vision, speech, NLP) / Neurosurgeon scheduler / Mobile development platform (model not stated in abstract)
- **Characteristics marked Yes:** edge_device, cloud, adaptive_inference, resource_awareness, energy_evaluation, latency_evaluation
- **Why relevant:** Foundational mobile/cloud split reference for energy-latency trade-offs.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Foundational mobile/cloud split reference for energy-latency trade-offs.
- **Reported metrics (abstract):** End-to-end latency 3.1x avg (up to 40.7x) better; mobile energy -59.5% avg (up to -94.7%)
- **Notes:** Full abstract taken from the ACM SIGPLAN Notices reprint (10.1145/3093336.3037698) of the same paper. Pre-2019 foundational paper.

**Evidence records**

> **Paper ID:** P028  
> **Claim:** Adaptive partitioning.  
> **Evidence:** Abstract describes a scheduler that partitions DNN computation between mobile and datacenter, adapting to hardware, wireless network and server load.  
> **Source:** https://doi.org/10.1145/3037697.3037698 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P028  
> **Claim:** Latency and energy evaluated.  
> **Evidence:** Abstract reports 3.1x average latency improvement and 59.5% average mobile energy reduction.  
> **Source:** https://doi.org/10.1145/3037697.3037698 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P029 — NestDNN: Resource-Aware Multi-Tenant On-Device Deep Learning for Continuous Mobile Vision

- **Authors:** Biyi Fang; Xiao Zeng; Mi Zhang
- **Year / Venue:** 2018 — Proceedings of the 24th Annual International Conference on Mobile Computing and Networking
- **DOI / URL:** [10.1145/3241539.3241559](https://doi.org/10.1145/3241539.3241559)
- **Application:** Resource-aware multi-tenant on-device deep learning for continuous mobile vision
- **Dataset / Model / Hardware:** Unknown / NestDNN / Mobile vision systems (platform not stated in abstract)
- **Characteristics marked Yes:** edge_device, on_device, adaptive_inference, resource_awareness, energy_evaluation, latency_evaluation
- **Why relevant:** Runtime resource-accuracy trade-off on mobile vision; close to PocketInspect's adaptive-inference direction.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Runtime resource-accuracy trade-off on mobile vision
- **Reported metrics (abstract):** Up to +4.2% accuracy, 2.0x frame rate, 1.7x lower energy vs resource-agnostic baseline
- **Notes:** Abstract lists smartphones among example mobile vision systems but does not state the evaluation device; smartphone=Unknown.

**Evidence records**

> **Paper ID:** P029  
> **Claim:** Runtime resource adaptation.  
> **Evidence:** Abstract selects resource-accuracy trade-offs per model at runtime to fit available resources.  
> **Source:** https://doi.org/10.1145/3241539.3241559 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P029  
> **Claim:** Energy and frame rate.  
> **Evidence:** Abstract reports up to 4.2% higher accuracy, 2.0x frame processing rate and 1.7x energy reduction.  
> **Source:** https://doi.org/10.1145/3241539.3241559 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P030 — MCDNN: An Approximation-Based Execution Framework for Deep Stream Processing Under Resource Constraints

- **Authors:** Seungyeop Han; Haichen Shen; Matthai Philipose; Sharad Agarwal; Alec Wolman; Arvind Krishnamurthy
- **Year / Venue:** 2016 — Proceedings of the 14th Annual International Conference on Mobile Systems, Applications, and Services
- **DOI / URL:** [10.1145/2906388.2906396](https://doi.org/10.1145/2906388.2906396)
- **Application:** Approximate model scheduling for mobile video DNNs under resource constraints
- **Dataset / Model / Hardware:** Unknown / MCDNN compiler and runtime scheduler / Cloud-backed mobile devices
- **Characteristics marked Yes:** cloud, adaptive_inference, resource_awareness, energy_evaluation
- **Why relevant:** Early formulation of accuracy-vs-resource scheduling for continuous mobile vision.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Early formulation of accuracy-vs-resource scheduling for continuous mobile vision.
- **Notes:** Pre-2019 foundational paper.

**Evidence records**

> **Paper ID:** P030  
> **Claim:** Resource-constrained scheduling.  
> **Evidence:** Abstract trades DNN accuracy for resource use and reasons about on-device vs cloud execution under battery, data and cloud-cost budgets.  
> **Source:** https://doi.org/10.1145/2906388.2906396 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P030  
> **Claim:** Energy characterised.  
> **Evidence:** Abstract characterises accuracy trade-offs against memory, computation and energy.  
> **Source:** https://doi.org/10.1145/2906388.2906396 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P031 — LOTUS: learning-based online thermal and latency variation management for two-stage detectors on edge devices

- **Authors:** Yifan Gong; Yushu Wu; Zheng Zhan; Pu Zhao; Liangkai Liu; Chao Wu; Xulong Tang; Yanzhi Wang
- **Year / Venue:** 2024 — Proceedings of the 61st ACM/IEEE Design Automation Conference
- **DOI / URL:** [10.1145/3649329.3657310](https://doi.org/10.1145/3649329.3657310)
- **Application:** Thermal and latency-variation management for two-stage detectors
- **Dataset / Model / Hardware:** Unknown / LOTUS (DRL-based joint CPU/GPU frequency scaling) / NVIDIA Jetson Orin Nano; Mi 11 Lite mobile platform
- **Characteristics marked Yes:** smartphone, edge_device, on_device, resource_awareness, thermal_evaluation
- **Why relevant:** Directly relevant: thermal-aware on-device detection on a smartphone-class platform.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Directly relevant: thermal-aware on-device detection on a smartphone-class platform.
- **Notes:** smartphone=Yes because the abstract names the Mi 11 Lite mobile platform (a smartphone model).

**Evidence records**

> **Paper ID:** P031  
> **Claim:** Thermal throttling addressed.  
> **Evidence:** Abstract scales CPU and GPU frequencies online with deep RL to avoid thermal throttling and stabilise inference speed.  
> **Source:** https://doi.org/10.1145/3649329.3657310 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P031  
> **Claim:** Evaluated platforms.  
> **Evidence:** Abstract implements LOTUS on NVIDIA Jetson Orin Nano and Mi 11 Lite mobile platforms and reports lower CPU/GPU temperatures.  
> **Source:** https://doi.org/10.1145/3649329.3657310 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P032 — Phoenix: Thermal-Aware On-Device Inference of Multi-Instance DNNs for Mobile Video Applications

- **Authors:** Seunghyeok Jeon; Jiwon Kim; Jeho Lee; Hojung Cha
- **Year / Venue:** 2026 — ACM Transactions on Embedded Computing Systems
- **DOI / URL:** [10.1145/3793860](https://doi.org/10.1145/3793860)
- **Application:** Thermal-aware multi-DNN on-device inference for mobile video
- **Dataset / Model / Hardware:** Two benchmarks + Virtual YouTuber streaming app / Phoenix (RL task allocation + multi-exit networks) / Mobile devices with heterogeneous processors
- **Characteristics marked Yes:** edge_device, on_device, adaptive_inference, resource_awareness, thermal_evaluation
- **Why relevant:** Combines thermal awareness with early-exit adaptation on mobile devices, a combination PocketInspect is exploring.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Combines thermal awareness with early-exit adaptation on mobile devices, a combination PocketInspect is exploring.
- **Notes:** 'Mobile devices' in abstract; smartphone model not stated, so smartphone=Unknown.

**Evidence records**

> **Paper ID:** P032  
> **Claim:** Thermal-aware allocation.  
> **Evidence:** Abstract allocates DNN tasks across heterogeneous processors using RL to model thermal dynamics and delay throttling.  
> **Source:** https://doi.org/10.1145/3793860 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P032  
> **Claim:** Multi-exit adaptation.  
> **Evidence:** Abstract uses multi-exit networks to keep frame rates consistent once throttling occurs.  
> **Source:** https://doi.org/10.1145/3793860 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P033 — CARIn: Constraint-Aware and Responsive Inference on Heterogeneous Devices for Single- and Multi-DNN Workloads

- **Authors:** Ioannis Panopoulos; Stylianos Venieris; Iakovos Venieris
- **Year / Venue:** 2024 — ACM Transactions on Embedded Computing Systems
- **DOI / URL:** [10.1145/3665868](https://doi.org/10.1145/3665868)
- **Application:** Constraint-aware runtime adaptation for single- and multi-DNN workloads on heterogeneous mobile devices
- **Dataset / Model / Hardware:** Text classification, scene recognition, face analysis tasks / CARIn (multi-objective optimisation + RASS solver) / Heterogeneous mobile devices
- **Characteristics marked Yes:** edge_device, on_device, adaptive_inference, resource_awareness
- **Why relevant:** Runtime configuration switching on heterogeneous mobile hardware.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Runtime configuration switching on heterogeneous mobile hardware.
- **Notes:** smartphone=Unknown (abstract says mobile devices).

**Evidence records**

> **Paper ID:** P033  
> **Claim:** Runtime adaptation under SLOs.  
> **Evidence:** Abstract optimises on-device DNN execution under user-defined service-level objectives with low-overhead runtime adaptation.  
> **Source:** https://doi.org/10.1145/3665868 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P033  
> **Claim:** Resource contention and heterogeneity.  
> **Evidence:** Abstract addresses device heterogeneity and multi-DNN resource contention, reporting up to 4.06x gain over hardware-unaware designs.  
> **Source:** https://doi.org/10.1145/3665868 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P034 — REDS: Resource-Efficient Deep Subnetworks for Dynamic Resource Constraints

- **Authors:** Francesco Corti; Balz Maag; Joachim Schauer; Ulrich Pferschy; Olga Saukh
- **Year / Venue:** 2026 — IEEE Transactions on Mobile Computing
- **DOI / URL:** [10.1109/tmc.2025.3594214](https://doi.org/10.1109/tmc.2025.3594214)
- **Application:** Deep subnetworks that adapt to dynamic resource constraints on edge devices
- **Dataset / Model / Hardware:** Visual Wake Words, Google Speech Commands, Fashion-MNIST, CIFAR-10, ImageNet-1K / REDS / Four mobile and embedded platforms incl. Arduino Nano 33 BLE
- **Characteristics marked Yes:** smartphone, edge_device, on_device, adaptive_inference, resource_awareness, energy_evaluation, latency_evaluation
- **Why relevant:** Runtime model downsizing driven by resource state.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Runtime model downsizing driven by resource state.
- **Notes:** Crossref issued year 2026; OpenAlex lists 2025 (early access).

**Evidence records**

> **Paper ID:** P034  
> **Claim:** Adapts to variable resources.  
> **Evidence:** Abstract introduces subnetworks that adapt at runtime to resource variability from energy levels, timing constraints or task priorities.  
> **Source:** https://doi.org/10.1109/tmc.2025.3594214 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P034  
> **Claim:** Hardware and adaptation time.  
> **Evidence:** Abstract tests on four off-the-shelf mobile and embedded platforms with adaptation time under 40 microseconds on Arduino Nano 33 BLE.  
> **Source:** https://doi.org/10.1109/tmc.2025.3594214 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P035 — Split Computing and Early Exiting for Deep Learning Applications: Survey and Research Challenges

- **Authors:** Yoshitomo Matsubara; Marco Levorato; Francesco Restuccia
- **Year / Venue:** 2022 — ACM Computing Surveys
- **DOI / URL:** [10.1145/3527155](https://doi.org/10.1145/3527155)
- **Application:** Survey of split computing and early exiting
- **Dataset / Model / Hardware:** Survey / Split computing and early-exit methods / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Survey of the two main runtime adaptation families for mobile inference.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Survey of the two main runtime adaptation families for mobile inference.
- **Notes:** Survey.

**Evidence records**

> **Paper ID:** P035  
> **Claim:** Survey scope.  
> **Evidence:** Abstract surveys split computing (head on device, tail on edge) and early exiting, where the accuracy-delay trade-off is tuned to current conditions.  
> **Source:** https://doi.org/10.1145/3527155 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P036 — Efficient Acceleration of Deep Learning Inference on Resource-Constrained Edge Devices: A Review

- **Authors:** Md. Maruf Hossain Shuvo; Syed Kamrul Islam; Jianlin Cheng; Bashir I. Morshed
- **Year / Venue:** 2023 — Proceedings of the IEEE
- **DOI / URL:** [10.1109/jproc.2022.3226481](https://doi.org/10.1109/jproc.2022.3226481)
- **Application:** Review of efficient DL inference on resource-constrained edge devices
- **Dataset / Model / Hardware:** Review / Review (architectures, model optimisation, HW/SW co-design, accelerators) / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Background on compression and acceleration options for on-device inspection models.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Background on compression and acceleration options for on-device inspection models.
- **Notes:** Review. Crossref issued year 2023; OpenAlex lists 2022.

**Evidence records**

> **Paper ID:** P036  
> **Claim:** Review scope.  
> **Evidence:** Abstract reviews four directions: efficient architectures, optimisation of existing methods, algorithm-hardware co-design and accelerator design.  
> **Source:** https://doi.org/10.1109/jproc.2022.3226481 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)


## G5 — Multi-view / Active Inspection

### P037 — Real-IAD: A Real-World Multi-View Dataset for Benchmarking Versatile Industrial Anomaly Detection

- **Authors:** Chengjie Wang; Wenbing Zhu; Bin-Bin Gao; Zhenye Gan; Jiangning Zhang; Zhihao Gu; Shuguang Qian; Mingang Chen; Lizhuang Ma
- **Year / Venue:** 2024 — 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
- **DOI / URL:** [10.1109/cvpr52733.2024.02159](https://doi.org/10.1109/cvpr52733.2024.02159)
- **Application:** Multi-view industrial anomaly detection benchmark
- **Dataset / Model / Hardware:** Real-IAD (150K high-resolution images, 30 objects) / Benchmarked popular IAD methods / Unknown
- **Characteristics marked Yes:** multi_view, anomaly_detection
- **Why relevant:** Multi-view IAD dataset with sample-level metrics; relevant to multi-view verification of a part.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Multi-view IAD dataset with sample-level metrics

**Evidence records**

> **Paper ID:** P037  
> **Claim:** Multi-view capture.  
> **Evidence:** Abstract states a multi-view shooting method was adopted and sample-level metrics proposed.  
> **Source:** https://doi.org/10.1109/cvpr52733.2024.02159 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P037  
> **Claim:** Scale and setting.  
> **Evidence:** Abstract reports 150K images of 30 objects and a fully unsupervised IAD setting.  
> **Source:** https://doi.org/10.1109/cvpr52733.2024.02159 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P038 — MANTA: A Large-Scale Multi-View and Visual-Text Anomaly Detection Dataset for Tiny Objects

- **Authors:** Lei Fan; Dongdong Fan; Zhiguang Hu; Yiwen Ding; Donglin Di; Kai Yi; Maurice Pagnucco; Yang Song
- **Year / Venue:** 2025 — 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
- **DOI / URL:** [10.1109/cvpr52734.2025.02376](https://doi.org/10.1109/cvpr52734.2025.02376)
- **Application:** Multi-view visual-text anomaly detection dataset for tiny objects
- **Dataset / Model / Hardware:** MANTA (137.3K images, 38 categories, 8.6K anomalous; 5 viewpoints per object) / Baseline for visual-text tasks / Unknown
- **Characteristics marked Yes:** multi_view, anomaly_detection
- **Why relevant:** Multi-view anomaly data for small objects, close to PocketInspect's small-component scope.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Multi-view anomaly data for small objects, close to PocketInspect's small-component scope.

**Evidence records**

> **Paper ID:** P038  
> **Claim:** Five viewpoints per image set.  
> **Evidence:** Abstract states each image is captured from five distinct viewpoints for comprehensive object coverage.  
> **Source:** https://doi.org/10.1109/cvpr52734.2025.02376 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P038  
> **Claim:** Small objects.  
> **Evidence:** Abstract targets tiny objects across five domains with pixel-level anomaly labels.  
> **Source:** https://doi.org/10.1109/cvpr52734.2025.02376 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P039 — Research on Defect Detection of the Outer Side of Bottle Cap Based on High Angle and Multi-View Vision System

- **Authors:** Chenghu He; Chen Li; Bowen Chen; Bin Yuan; Yongjing Yin
- **Year / Venue:** 2023 — IEEE Access
- **DOI / URL:** [10.1109/access.2023.3290616](https://doi.org/10.1109/access.2023.3290616)
- **Application:** Defect detection on outer side of bottle caps
- **Dataset / Model / Hardware:** Unknown / Background reconstruction of line structure element (BRLSE), classical image processing / High-angle annular illumination, four-view imaging system
- **Characteristics marked Yes:** multi_view, latency_evaluation
- **Why relevant:** Multi-view plus illumination design for curved small parts.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Multi-view plus illumination design for curved small parts.
- **Reported metrics (abstract):** Inspection speed > 400 pcs/min; accuracy > 95%
- **Notes:** Classical (non-deep-learning) method.

**Evidence records**

> **Paper ID:** P039  
> **Claim:** Four imaging views.  
> **Evidence:** Abstract completes imaging of the cap's outer side in four views under high-angle annular illumination.  
> **Source:** https://doi.org/10.1109/access.2023.3290616 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P039  
> **Claim:** Throughput and accuracy.  
> **Evidence:** Abstract reports speed better than 400 pcs/min and accuracy better than 95%.  
> **Source:** https://doi.org/10.1109/access.2023.3290616 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P040 — MVGCN: Multi-View Graph Convolutional Neural Network for Surface Defect Identification Using Three-Dimensional Point Cloud

- **Authors:** Yinan Wang; Wenbo Sun; Jionghua (Judy) Jin; Zhenyu (James) Kong; Xiaowei Yue
- **Year / Venue:** 2022 — Journal of Manufacturing Science and Engineering
- **DOI / URL:** [10.1115/1.4056005](https://doi.org/10.1115/1.4056005)
- **Application:** Surface defect identification from 3D point clouds
- **Dataset / Model / Hardware:** Synthetic aircraft fuselage surface; real precast concrete specimen / Unsupervised detection + multi-view graph CNN (MVGCN) classifier / Unknown
- **Characteristics marked Yes:** anomaly_detection
- **Why relevant:** Highlights viewpoint and lighting sensitivity of 2D images.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Highlights viewpoint and lighting sensitivity of 2D images.
- **Notes:** 'Multi-view' refers to the model's representation of point-cloud data; multiple physical camera views are not stated, so multi_view=Unknown.

**Evidence records**

> **Paper ID:** P040  
> **Claim:** Two-step approach.  
> **Evidence:** Abstract combines unsupervised defect detection with a multi-view deep learning model for defect classification on 3D point clouds.  
> **Source:** https://doi.org/10.1115/1.4056005 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P040  
> **Claim:** Image limitations noted.  
> **Evidence:** Abstract argues image-based methods lose depth information and are sensitive to inspection angle and lighting.  
> **Source:** https://doi.org/10.1115/1.4056005 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P041 — Feature-Driven Viewpoint Placement for Model-Based Surface Inspection

- **Authors:** Dennis Mosbach; Petra Gospodnetić; Markus Rauhut; Bernd Hamann; Hans Hagen
- **Year / Venue:** 2020 — Machine Vision and Applications
- **DOI / URL:** [10.1007/s00138-020-01116-y](https://doi.org/10.1007/s00138-020-01116-y)
- **Application:** Camera viewpoint placement for model-based optical surface inspection
- **Dataset / Model / Hardware:** 3D surface models (triangular meshes) / B-spline approximation with feature-driven adaptive surface sampling / Robot-mounted cameras (context)
- **Characteristics marked Yes:** multi_view
- **Why relevant:** Viewpoint selection methodology relevant to guiding a user to recapture from additional angles.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Viewpoint selection methodology relevant to guiding a user to recapture from additional angles.
- **Notes:** Offline planning from CAD models; no learned defect detector.

**Evidence records**

> **Paper ID:** P041  
> **Claim:** Viewpoint planning.  
> **Evidence:** Abstract determines a small number of well-placed camera viewpoints for inspection from 3D models using adaptive non-uniform surface sampling.  
> **Source:** https://doi.org/10.1007/s00138-020-01116-y (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P042 — Viewpoint placement for inspection planning

- **Authors:** Petra Gospodnetić; Dennis Mosbach; Markus Rauhut; Hans Hagen
- **Year / Venue:** 2021 — Machine Vision and Applications
- **DOI / URL:** [10.1007/s00138-021-01252-z](https://doi.org/10.1007/s00138-021-01252-z)
- **Application:** Evaluation of automated inspection viewpoint planning vs expert plans
- **Dataset / Model / Hardware:** Various objects / Generate-and-test viewpoint planning approaches / Unknown
- **Characteristics marked Yes:** multi_view
- **Why relevant:** Practical limits of automatic viewpoint planning.
- **Limitations (author-stated):** Abstract notes automated plans are hard to verify and compare with lab-developed plans.
- **PocketInspect relevance:** Practical limits of automatic viewpoint planning.

**Evidence records**

> **Paper ID:** P042  
> **Claim:** Comparison with experts.  
> **Evidence:** Abstract reviews generate-and-test viewpoint planning, evaluates them on several objects and compares with expert-created plans.  
> **Source:** https://doi.org/10.1007/s00138-021-01252-z (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P043 — 2M3DF: Advancing 3D Industrial Defect Detection With Multi-Perspective Multimodal Fusion Network

- **Authors:** Mujtaba Asad; Waqar Azeem; He Jiang; Hafiz Tayyab Mustafa; Jie Yang; Wei Liu
- **Year / Venue:** 2025 — IEEE Transactions on Circuits and Systems for Video Technology
- **DOI / URL:** [10.1109/tcsvt.2025.3536475](https://doi.org/10.1109/tcsvt.2025.3536475)
- **Application:** 3D industrial anomaly detection fusing multi-view RGB and point clouds
- **Dataset / Model / Hardware:** MVTec3D-AD, Eyecandies / 2M3DF (pretrained extractors, inter-modality fusion, multivariate Gaussian) / Unknown
- **Characteristics marked Yes:** multi_view, anomaly_detection
- **Why relevant:** Multi-view fusion for anomaly detection.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Multi-view fusion for anomaly detection.
- **Reported metrics (abstract):** Mean I-AUROC 96.6%
- **Notes:** Real-time claim without latency figure in abstract.

**Evidence records**

> **Paper ID:** P043  
> **Claim:** Multi-view RGB fusion.  
> **Evidence:** Abstract uses features from multi-view RGB images and corresponding point clouds, fused pixel-to-point.  
> **Source:** https://doi.org/10.1109/tcsvt.2025.3536475 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P043  
> **Claim:** Result.  
> **Evidence:** Abstract reports 96.6% mean I-AUROC and real-time results.  
> **Source:** https://doi.org/10.1109/tcsvt.2025.3536475 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P044 — Robotic Defect Inspection with Visual and Tactile Perception for Large-Scale Components

- **Authors:** Arpit Agarwal; Abhiroop Ajith; Chengtao Wen; Veniamin Stryzheus; Brian Miller; Matthew Chen; Micah K. Johnson; Jose Luis Susa Rincon; Justinian Rosca; Wenzhen Yuan
- **Year / Venue:** 2023 — 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)
- **DOI / URL:** [10.1109/iros55552.2023.10341590](https://doi.org/10.1109/iros55552.2023.10341590)
- **Application:** Two-stage visual-then-tactile defect inspection of large aerospace components
- **Dataset / Model / Hardware:** New real-world dataset of metallic defects on aerospace parts / Two-stage multimodal pipeline (vision then tactile) / Robot with visual and tactile sensors
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Example of escalating to a second sensing stage when the first is insufficient (analogous to recapture).
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Example of escalating to a second sensing stage when the first is insufficient (analogous to recapture).
- **Notes:** Second stage is tactile, not a second camera view; multi_view left Unknown.

**Evidence records**

> **Paper ID:** P044  
> **Claim:** Staged inspection.  
> **Evidence:** Abstract localises defects with a global visual view, then uses tactile scanning of localised areas for remaining defects.  
> **Source:** https://doi.org/10.1109/iros55552.2023.10341590 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P044  
> **Claim:** Result.  
> **Evidence:** Abstract reports 85% of defects found in Stage I and 100% after Stage II.  
> **Source:** https://doi.org/10.1109/iros55552.2023.10341590 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)


## G6 — Confidence / Uncertainty / Selective Prediction

### P045 — Selective Classification for Deep Neural Networks

- **Authors:** Yonatan Geifman; Ran El-Yaniv
- **Year / Venue:** 2017 — Advances in Neural Information Processing Systems 30 (NeurIPS 2017)
- **DOI / URL:** [proceedings page](https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html)
- **Application:** Selective classification (reject option) with guaranteed risk
- **Dataset / Model / Hardware:** CIFAR, ImageNet / Selective classifier built on trained DNNs / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Formal basis for abstaining (e.g., requesting recapture) when confidence is insufficient.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Formal basis for abstaining (e.g., requesting recapture) when confidence is insufficient.
- **Reported metrics (abstract):** 2% top-5 ImageNet error guaranteed with probability 99.9% at almost 60% coverage
- **Notes:** Peer-reviewed NeurIPS 2017 paper (no DOI). arXiv preprint DOI: 10.48550/arXiv.1705.08500. Venue verified via OpenAlex and the NeurIPS proceedings page.

**Evidence records**

> **Paper ID:** P045  
> **Claim:** Reject option with risk control.  
> **Evidence:** Abstract constructs a selective classifier that rejects instances at test time to guarantee a user-set risk level.  
> **Source:** https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html (abstract via OpenAlex (arXiv record) and proceedings page)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P045  
> **Claim:** Result.  
> **Evidence:** Abstract reports 2% top-5 ImageNet error with 99.9% probability at almost 60% coverage.  
> **Source:** https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html (abstract via OpenAlex (arXiv record) and proceedings page)  
> **Evidence status:** Verified (abstract-level)

### P046 — SelectiveNet: A Deep Neural Network with an Integrated Reject Option

- **Authors:** Yonatan Geifman; Ran El-Yaniv
- **Year / Venue:** 2019 — Proceedings of the 36th International Conference on Machine Learning (ICML 2019), PMLR 97
- **DOI / URL:** [proceedings page](https://proceedings.mlr.press/v97/geifman19a.html)
- **Application:** End-to-end training of classification with integrated rejection
- **Dataset / Model / Hardware:** Several classification and regression datasets (names not in abstract) / SelectiveNet / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Learned abstention mechanism; alternative to fixed confidence thresholds for recapture triggers.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Learned abstention mechanism
- **Notes:** Peer-reviewed ICML 2019 paper (no DOI). arXiv preprint DOI: 10.48550/arXiv.1901.09192. Venue verified via the PMLR proceedings page.

**Evidence records**

> **Paper ID:** P046  
> **Claim:** Integrated reject option.  
> **Evidence:** Abstract trains classification and rejection jointly end-to-end, in contrast to thresholding a pretrained network's confidence.  
> **Source:** https://proceedings.mlr.press/v97/geifman19a.html (abstract via OpenAlex (arXiv record) and proceedings page)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P046  
> **Claim:** Risk-coverage.  
> **Evidence:** Abstract reports improved risk-coverage trade-off over several datasets.  
> **Source:** https://proceedings.mlr.press/v97/geifman19a.html (abstract via OpenAlex (arXiv record) and proceedings page)  
> **Evidence status:** Verified (abstract-level)

### P047 — U2D2PCB: Uncertainty-Aware Unsupervised Defect Detection on PCB Images Using Reconstructive and Discriminative Models

- **Authors:** Changlin Chen; Qiman Wu; Jin Zhang; Haojie Xia; Pengrong Lin; Yong Wang; Mengke Tian; Rencheng Song
- **Year / Venue:** 2024 — IEEE Transactions on Instrumentation and Measurement
- **DOI / URL:** [10.1109/tim.2024.3386210](https://doi.org/10.1109/tim.2024.3386210)
- **Application:** Unsupervised PCB defect detection with uncertainty estimation
- **Dataset / Model / Hardware:** Public PCB defect dataset; DeepPCB / U2D2PCB (reconstructive + discriminative U-Nets) / Unknown
- **Characteristics marked Yes:** uncertainty, anomaly_detection
- **Why relevant:** Uncertainty-aware unsupervised defect segmentation for small manufactured components.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Uncertainty-aware unsupervised defect segmentation for small manufactured components.
- **Reported metrics (abstract):** mAP 99.29% (PCB defect dataset); 95.78% (DeepPCB)

**Evidence records**

> **Paper ID:** P047  
> **Claim:** Uncertainty evaluated.  
> **Evidence:** Abstract's discriminative sub-network segments defects and evaluates defect uncertainty.  
> **Source:** https://doi.org/10.1109/tim.2024.3386210 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P047  
> **Claim:** Unsupervised training.  
> **Evidence:** Abstract trains only on defect-free images with synthetic multi-scale defects.  
> **Source:** https://doi.org/10.1109/tim.2024.3386210 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P048 — An Uncertainty-Aware Deep Learning Model for Reliable Detection of Steel Wire Rope Defects

- **Authors:** Wenting Yi; Wai Kit Chan; Hiu Hung Lee; Steven T. Boles; Xiaoge Zhang
- **Year / Venue:** 2024 — IEEE Transactions on Reliability
- **DOI / URL:** [10.1109/tr.2023.3335958](https://doi.org/10.1109/tr.2023.3335958)
- **Application:** Steel wire rope defect classification with uncertainty and OOD detection
- **Dataset / Model / Hardware:** Magnetic flux leakage signals from dedicated experimental setup / GoogLeNet with SNGP (spectral normalisation + Gaussian process) / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Distance-aware uncertainty and OOD flagging for inspection decisions.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Distance-aware uncertainty and OOD flagging for inspection decisions.
- **Notes:** Sensing modality is magnetic flux leakage converted to images (Gramian angular field), not camera images. Crossref issued year 2024; OpenAlex lists 2023.

**Evidence records**

> **Paper ID:** P048  
> **Claim:** Uncertainty module.  
> **Evidence:** Abstract integrates spectral-normalised neural Gaussian process into GoogLeNet for distance-aware uncertainty.  
> **Source:** https://doi.org/10.1109/tr.2023.3335958 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P048  
> **Claim:** OOD identification.  
> **Evidence:** Abstract evaluates identification of out-of-distribution wire-rope instances.  
> **Source:** https://doi.org/10.1109/tr.2023.3335958 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P049 — Epistemic and aleatoric uncertainty quantification for crack detection using a Bayesian Boundary Aware Convolutional Network

- **Authors:** Rahul Rathnakumar; Yutian Pang; Yongming Liu
- **Year / Venue:** 2023 — Reliability Engineering & System Safety
- **DOI / URL:** [10.1016/j.ress.2023.109547](https://doi.org/10.1016/j.ress.2023.109547)
- **Application:** Crack boundary detection with epistemic and aleatoric uncertainty
- **Dataset / Model / Hardware:** Benchmark crack datasets (names not in abstract) / Bayesian Boundary-Aware Convolutional Network (B-BACN) / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Separating model vs data (image) uncertainty, relevant to deciding whether to recapture or escalate.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Separating model vs data (image) uncertainty, relevant to deciding whether to recapture or escalate.

**Evidence records**

> **Paper ID:** P049  
> **Claim:** Epistemic and aleatoric UQ.  
> **Evidence:** Abstract uses Monte Carlo dropout for epistemic and Gaussian sampling for aleatoric uncertainty.  
> **Source:** https://doi.org/10.1016/j.ress.2023.109547 (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P049  
> **Claim:** Calibration.  
> **Evidence:** Abstract reports reduced misclassification and improved calibration.  
> **Source:** https://doi.org/10.1016/j.ress.2023.109547 (abstract via Semantic Scholar)  
> **Evidence status:** Verified (abstract-level)

### P050 — Pixel-Level Anomaly Detection via Uncertainty-aware Prototypical Transformer

- **Authors:** Chao Huang; Chengliang Liu; Zheng Zhang; Zhihao Wu; Jie Wen; Qiuping Jiang; Yong Xu
- **Year / Venue:** 2022 — Proceedings of the 30th ACM International Conference on Multimedia
- **DOI / URL:** [10.1145/3503161.3548082](https://doi.org/10.1145/3503161.3548082)
- **Application:** Pixel-level visual anomaly detection
- **Dataset / Model / Hardware:** Five datasets (names not in abstract) / Uncertainty-aware prototypical transformer (UPformer) / Unknown
- **Characteristics marked Yes:** uncertainty, anomaly_detection
- **Why relevant:** Uncertainty used inside the detector rather than only post hoc.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Uncertainty used inside the detector rather than only post hoc.

**Evidence records**

> **Paper ID:** P050  
> **Claim:** Uncertainty guides decoding.  
> **Evidence:** Abstract learns detection uncertainty distributions and uses them to guide the decoder toward uncertain areas.  
> **Source:** https://doi.org/10.1145/3503161.3548082 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P051 — Uncertainty Quantification for Deep Learning in Ultrasonic Crack Characterization

- **Authors:** Richard J. Pyle; Robert R. Hughes; Amine Ait Si Ali; Paul D. Wilcox
- **Year / Venue:** 2022 — IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control
- **DOI / URL:** [10.1109/tuffc.2022.3176926](https://doi.org/10.1109/tuffc.2022.3176926)
- **Application:** Crack sizing from ultrasonic plane-wave images with UQ
- **Dataset / Model / Hardware:** Simulated (hybrid FE/ray model) and experimental ultrasonic images / CNN with deep ensembles and Monte Carlo dropout / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Comparative evidence on which UQ method is calibrated for inspection.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Comparative evidence on which UQ method is calibrated for inspection.
- **Reported metrics (abstract):** Calibration fit R: MC dropout 0.84; deep ensembles 0.95; ensembles + spectral norm + residual 0.98
- **Notes:** Ultrasonic imaging modality, not optical camera.

**Evidence records**

> **Paper ID:** P051  
> **Claim:** UQ methods compared.  
> **Evidence:** Abstract compares deep ensembles and Monte Carlo dropout and judges UQ by calibration and OOD detection.  
> **Source:** https://doi.org/10.1109/tuffc.2022.3176926 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P051  
> **Claim:** Finding.  
> **Evidence:** Abstract reports MC dropout performs poorly and deep ensembles improve calibration and anomaly detection.  
> **Source:** https://doi.org/10.1109/tuffc.2022.3176926 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P052 — A review of uncertainty quantification in deep learning: Techniques, applications and challenges

- **Authors:** Moloud Abdar; Farhad Pourpanah; Sadiq Hussain; Dana Rezazadegan; Li Liu; Mohammad Ghavamzadeh; Paul Fieguth; Xiaochun Cao; Abbas Khosravi; U. Rajendra Acharya; Vladimir Makarenkov; Saeid Nahavandi
- **Year / Venue:** 2021 — Information Fusion
- **DOI / URL:** [10.1016/j.inffus.2021.05.008](https://doi.org/10.1016/j.inffus.2021.05.008)
- **Application:** Review of uncertainty quantification in deep learning
- **Dataset / Model / Hardware:** Review / Bayesian approximation, ensemble methods and others / Unknown
- **Characteristics marked Yes:** none (all Unknown/No at abstract level)
- **Why relevant:** Background reference for UQ method selection.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Background reference for UQ method selection.
- **Notes:** Review.

**Evidence records**

> **Paper ID:** P052  
> **Claim:** Review scope.  
> **Evidence:** Abstract reviews UQ methods in deep learning, with Bayesian approximation and ensembles as the two main families.  
> **Source:** https://doi.org/10.1016/j.inffus.2021.05.008 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P053 — Contact Wire Support Defect Detection Using Deep Bayesian Segmentation Neural Networks and Prior Geometric Knowledge

- **Authors:** Gaoqiang Kang; Shibin Gao; Long Yu; Dongkai Zhang; Xiaoguang Wei; Dong Zhan
- **Year / Venue:** 2019 — IEEE Access
- **DOI / URL:** [10.1109/access.2019.2955753](https://doi.org/10.1109/access.2019.2955753)
- **Application:** Railway catenary contact wire support defect detection
- **Dataset / Model / Hardware:** Images from Hefei-Fuzhou high-speed railway line / Faster R-CNN + Bayesian FCN segmentation (CCSN) + geometric criteria / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Multi-stage inspection pipeline with Bayesian uncertainty.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Multi-stage inspection pipeline with Bayesian uncertainty.

**Evidence records**

> **Paper ID:** P053  
> **Claim:** MC dropout uncertainty.  
> **Evidence:** Abstract states the segmentation network evaluates model uncertainty via Monte Carlo dropout.  
> **Source:** https://doi.org/10.1109/access.2019.2955753 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

### P054 — An Uncertainty-Aware Deep Learning Framework for Defect Detection in Casting Products

- **Authors:** Maryam Habibpour; Hassan Gharoun; AmirReza Tajally; Afshar Shamsi; Hamzeh Asgharnezhad; Abbas Khosravi; Saeid Nahavandi
- **Year / Venue:** 2021 — arXiv preprint
- **DOI / URL:** [10.48550/arxiv.2107.11643](https://doi.org/10.48550/arxiv.2107.11643)
- **Application:** Casting product defect classification with epistemic uncertainty
- **Dataset / Model / Hardware:** Small casting image dataset (name not in abstract) / Pretrained CNN features (VGG16, ResNet50, DenseNet121, InceptionResNetV2) + ML classifiers; ensemble of MLPs for UQ / Unknown
- **Characteristics marked Yes:** uncertainty
- **Why relevant:** Lightweight ensemble UQ for manufactured-part classification.
- **Limitations (author-stated):** Not stated in abstract — full-text review pending.
- **PocketInspect relevance:** Lightweight ensemble UQ for manufactured-part classification.
- **Notes:** Preprint (arXiv; also posted on SSRN). No peer-reviewed version found in OpenAlex as of 2026-10-01.

**Evidence records**

> **Paper ID:** P054  
> **Claim:** Ensemble UQ.  
> **Evidence:** Abstract measures epistemic uncertainty with an ensemble of MLPs on features from four pretrained CNNs.  
> **Source:** https://doi.org/10.48550/arxiv.2107.11643 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)

> **Paper ID:** P054  
> **Claim:** UQ evaluation.  
> **Evidence:** Abstract uses a UQ confusion matrix and uncertainty accuracy metric; VGG16-based UQ performed best.  
> **Source:** https://doi.org/10.48550/arxiv.2107.11643 (abstract via OpenAlex/Crossref abstract)  
> **Evidence status:** Verified (abstract-level)


## Rejected or deferred candidates

| DOI | Title | Year | Group | Decision and reason |
| :-- | :-- | :-- | :-- | :-- |
| [10.1061/(asce)is.1943-555x.0000489](https://doi.org/10.1061/(asce)is.1943-555x.0000489) | Smartphone-Based Pothole Detection Utilizing Artificial Neural Networks | 2019 | G1 | Rejected: uses smartphone inertial sensors and OBD-II signals, not camera images; out of scope for visual inspection. |
| [10.1016/j.neucom.2018.03.013](https://doi.org/10.1016/j.neucom.2018.03.013) | Scale insensitive and focus driven mobile screen defect detection in industry | 2018 | G1 | Rejected for G1: keyword false positive. The phone screen is the inspected product, not the inspection device. Could be reconsidered for G2 (it includes weight quantization). |
| [10.56042/jsir.v82i04.72390](https://doi.org/10.56042/jsir.v82i04.72390) | Lightweight CNN Models for Product Defect Detection with Edge Computing in Manufacturing Industries | 2023 | G2 | Deferred: author list missing in both Crossref and OpenAlex, so the required authors field cannot be verified. Relevant (Jetson Nano deployment); revisit with publisher page. |
| [10.1016/j.compind.2023.103911](https://doi.org/10.1016/j.compind.2023.103911) | Deep CNN-based visual defect detection: Survey of current literature | 2023 | G2 | Deferred: abstract not available from OpenAlex/Semantic Scholar and ScienceDirect presented a bot check; fields could not be evidenced. |
| [10.1016/j.measurement.2025.117362](https://doi.org/10.1016/j.measurement.2025.117362) | Real-time remote monitoring and defect detection in smart additive manufacturing for reduced material wastage | 2025 | G3 | Deferred: abstract not retrievable (ScienceDirect bot check). Potentially highly relevant (low-cost 3D-print monitoring); revisit manually. |
