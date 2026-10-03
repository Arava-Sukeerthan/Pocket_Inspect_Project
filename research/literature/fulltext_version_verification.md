# Full-Text Version Verification (Step 9.6)

_2026-10-03, Claude Code, branch `claude/nice-babbage-51qfba` (from `main` at `d3f428e`)._

This step does four things:

1. checks the version-limited evidence for P011, P029, P031 and P033 against the strongest version that can be reached;
2. tries to verify P013 Tables 4-5 visually;
3. reassesses the relevance of P002 and P013;
4. applies changes to `papers.csv` only where the version of record was actually read.

No gap analysis was done. `research/gap_analysis/` was not touched.

**Definitions:** README §7 v1.1, `coding_decisions.md`, the approved Step 9.3/9.4 decisions, and the Step 9.6 operational definitions. These are unchanged.

**Evidence labels:**
- **Directly verified:** read in the source named.
- **Inferred:** follows from verified text by a stated rule.
- **Unresolved:** not settled by the source.

## 1. Summary

| Item | Result |
|---|---|
| P011 | **Version of record read** (Information Fusion 116 (2025) 102782, Elsevier-typeset PDF). All 11 deferred characteristic values and 6 deferred free-text values are confirmed and **applied** to `papers.csv`. No conflict with the arXiv v2 evidence. |
| P029 | **Stopped: version of record not reachable.** The strongest available copy is still arXiv 1810.10090v1, which carries the MobiCom '18 permission block. Nothing applied. |
| P031 | **Stopped: version of record not reachable** (DAC '24 is closed access, and ACM is blocked). A second copy was read (University of Michigan Deep Blue). It agrees with arXiv v1 on every deferred field. Nothing applied. |
| P033 | **Stopped: version of record not reachable** (ACM DL is blocked from this environment). arXiv v1 carries the final ACM TECS citation block. An earlier author manuscript (author's site) agrees on the fields checked. Nothing applied. |
| P013 Tables 4-5 | **Unresolved.** No visual inspection was possible, and the text layer is internally inconsistent. `accuracy_metrics` stays blank. |
| P002 relevance | **Peripheral/contextual (not core).** Proposed; needs researcher approval. |
| P013 relevance | **Peripheral/contextual (not core).** Proposed; needs researcher approval. |
| Corpus | 54 records; no paper added or removed; no bibliographic field changed; schema unchanged. |

## 2. Access route

- **Blocked hosts.** This environment's egress proxy blocks dl.acm.org, doi.org, sciencedirect.com, arxiv.org (direct), OpenAlex and Crossref. curl to all of them failed with CONNECT 403 on 2026-10-03.
- **Reader service.** Full texts were read through the alphaXiv document reader:
  - for open PDFs on author or institutional hosts;
  - for arXiv papers.
  The reader returns the PDF's text layer and does not render page images.
- **Copies found.** Web search (2026-10-03) was used only to locate legitimate copies of these four already-included papers. No new literature search was made and no paper was added.
- **No workarounds.** No bot check was bypassed and no unauthorised repository was used.

## 3. Version sources

| Paper | Strongest version read | Version type | Version of record reached? | Other versions compared |
|---|---|---|---|---|
| P011 | `https://www.cs.unb.ca/~hcao3/publications/2025-information-fusion/XEdgeAI.pdf` (host of the corresponding author, H. Cao). First page: "Information Fusion 116 (2025) 102782 … Available online 15 November 2024 … © 2024 The Author(s). Published by Elsevier B.V. … CC BY-NC". Elsevier running footers on every page. | Publisher-typeset version of record (open access) | **Yes** | arXiv 2407.11771v2 ("Preprint submitted to Information Fusion", Step 9.2 source) |
| P029 | arXiv 1810.10090v1. The Semantic Scholar PDF link resolves to the same copy. It carries the MobiCom '18 permission block, ACM ISBN 978-1-4503-5903-0/18/10 and DOI 10.1145/3241539.3241559. | Author copy with conference permission block | **No.** ACM DL is blocked. OpenAlex lists ACM as open access, so a normal browser should reach it. | None independent |
| P031 | University of Michigan Deep Blue repository PDF (`backend.production.deepblue-documents.lib.umich.edu/.../aa048de8-d9e0-4c5b-b343-6c187a37636f/content`). It carries the DAC '24 copyright block, ACM ISBN 979-8-4007-0601-1/24/06 and the DOI. The abstract still reads "Our code is available at [link]", which suggests an accepted-manuscript stage. | Institutional-repository author manuscript | **No.** Closed access; ACM blocked. | arXiv 2410.10847v1 (Step 9.2 source) |
| P033 | arXiv 2409.01089v1. It carries the final ACM reference: "ACM Trans. Embedd. Comput. Syst. 23, 4, Article 60 (June 2024), 31 pages. https://doi.org/10.1145/3665868". Running heads read "60:x". | arXiv copy in the final journal layout | **No.** ACM DL blocked. | Author-site copy `steliosven10.github.io/papers/[2024]_tecs_carin.pdf`: an earlier manuscript with placeholder citation data ("Vol. 37, No. 4, Article 111 … August 2024", DOI `XXXXXXX.XXXXXXX`) |

## 4. Per-paper verification

### 4.1 P011: version of record verified; changes applied

**Source:** Information Fusion 116 (2025) 102782 (Elsevier-typeset version of record). Page numbers below are the journal's.

**Comparison with arXiv v2:** the section text, Algorithm 1, Table 3, Table 4 and Table 6 values match the arXiv v2 evidence. The only differences found are pagination and one VoR sentence in §8.1, which states the framework's effectiveness "in both cloud and edge computing contexts".

#### Characteristic fields

| Field | Previous | New | Evidence (version of record) | Location | Evidence type |
|---|---|---|---|---|---|
| smartphone | Unknown | **Yes** | The mobile model is optimised "for deployment on smartphone devices". The Android/iOS smartphone app runs the mobile model θ on the captured or uploaded image. The iOS UI is "designed for iPhone 11 Pro". | §5.5.1-5.5.2, pp. 11-12; §5.6, Fig. 7, pp. 12-13 | Directly verified |
| cloud | Unknown | **Yes** (auxiliary component only) | GPT-4 Vision generates the textual explanations from a prompt carrying base64 image payloads (Template 1). §8.1 refers to "both cloud and edge computing contexts". The Fig. 4 labels "Call API", "Cloud Environment" and "Web App (Gradio)" were read in arXiv v2; the VoR Fig. 4 has the same caption but no text layer. The segmentation (the inspection inference) runs on the phone. | §4 module 6, p. 9; §5.6, p. 12; Template 1, p. 17; §8.1, p. 20; Fig. 4 | Directly verified (VoR text) + figure labels verified in arXiv v2 only. Applies the approved Step 9.4 decision D06. |
| adaptive_inference | Unknown | **No** | Design-time int8 dynamic quantisation, 10% structured pruning and TorchScript tracing. No runtime change of model computation. | §5.5.1, Algorithm 1, pp. 11-12 | Directly verified |
| resource_awareness | Unknown | **No** | Design-time lightweighting. No runtime decision driven by device resources. | §5.5.1, pp. 11-12 | Directly verified |
| energy_evaluation | Unknown | **No** | No energy, power or battery result. "Energy-Based Pointing Game" is an XAI metric. | Full text; no occurrence | Directly verified |
| thermal_evaluation | Unknown | **No** | No temperature or throttling measurement. | Full text; no occurrence | Directly verified |
| multi_view | Unknown | **No** | One uploaded image per inspection. Images from different cameras (handheld, AGV-mounted, fixed) are segmented independently. | §5.6, p. 12; §6.1, p. 12; §7.1, p. 17 | Directly verified |
| uncertainty | Unknown | **No** | No predictive uncertainty, calibration or OOD treatment. | Full text; no occurrence | Directly verified |
| confidence_gating | Unknown | **No** | Inspection is started by the user ("Inspect" button). No confidence score triggers an action. | §5.6, Fig. 7, pp. 12-13 | Directly verified |
| anomaly_detection | Unknown | **No** | Supervised semantic segmentation trained with Dice loss. | §5.1.2, p. 9 | Directly verified |
| latency_evaluation | Unknown | **No** | No inference latency, throughput or FPS appears anywhere. The Table 4 caption mentions "running time in seconds", but Table 4 contains only EPBG, BBox, IoU, Del and Ins. §8.3 names possible explanation latency only as a limitation. | Table 4, p. 15; §8.3, p. 20 | Directly verified. Applies the approved Step 9.4 decision D07. |

#### Retained values

| Field | Value | Reason |
|---|---|---|
| edge_device | Yes | Retained; the VoR is consistent with it. |
| on_device | Yes | Retained; the VoR is consistent with it. Segmentation runs on the phone (§5.5.2, §5.6). |

#### Free-text fields

Values are as recorded in `papers.csv`.

| Field | Source location |
|---|---|
| dataset | §6.1, p. 12; §7.1, p. 17 |
| model | §4-§5; Algorithm 1 |
| hardware | §5.5.2; §5.6; Fig. 7; Fig. 4 |
| accuracy_metrics | Table 3, p. 14; Table 6, p. 19 |
| efficiency_metrics | Table 3, p. 14 |
| limitations | §8.3, p. 20; §9, p. 21 |

The `hardware` text names GPT-4 Vision as remote using the Fig. 4 "Call API" label.

**Wording.** P011 is not a cloud-based inspection system. `cloud = Yes` records remote computation for the auxiliary explanation component only.

**Unresolved (P011):** where the Table 3 mobile-model mIoU was computed (on a phone or off-device) is not stated. This is recorded in `notes`, and no field depends on it.

### 4.2 P029: stopped

The version of record could not be verified.

**Strongest available version:** arXiv 1810.10090v1, the same copy as Step 9.2. No independent second copy was reachable. ResearchGate and ACM are blocked or not tried; no bot check was bypassed.

**Deferred values:** the Step 9.4 deferred values stay **not applied**:

| Field | Deferred value | Location (arXiv v1) |
|---|---|---|
| smartphone | Yes | §4.3.1: Samsung Galaxy S8, Samsung Galaxy S7, LG Nexus 5 (Android 7.0); results reported from the S8 |
| cloud | No | §4.3.1; §6 |
| thermal_evaluation | No | Full text; no occurrence |
| multi_view | No | §4.1 |
| uncertainty | No | Full text; no occurrence |
| confidence_gating | No | Full text; no occurrence |
| anomaly_detection | No | §4.1 |

The deferred free-text values (dataset, hardware, model, limitations) are also not applied.

**Re-read in Step 9.6:** the re-read of the arXiv copy found nothing that contradicts these values or the current `Yes` values (edge_device, on_device, adaptive_inference, resource_awareness, energy_evaluation, latency_evaluation).

**Energy evidence:** §4.3.1 states that a Monsoon power monitor was used. Fig. 8 reports model-switching energy on a Galaxy S8.

### 4.3 P031: stopped

The version of record could not be verified.

**Version check:** the Deep Blue copy and arXiv v1 agree on every deferred field:

| Field | Deferred value | Deep Blue copy evidence |
|---|---|---|
| smartphone | Yes (current) | §4.4: Mi 11 Lite with Snapdragon 780G. Table 2 caption: "Mi 11 Lite 5G". This settles the 4G/5G question noted in `papers.csv` without changing any value. |
| edge_device, on_device | Yes (current) | §5.2.1: the detector executes 3,000 iterations on the device. §4.4: the Lotus DQN agent runs on a separate desktop with an RTX 2080Ti and controls the device frequencies over a socket. |
| cloud | No | §4.4: the agent runs on a desktop, not a cloud server. Approved in Step 9.3. |
| adaptive_inference | No | §4.1-4.2: Lotus scales CPU/GPU frequency only, twice per frame. Detector computation is unchanged. The varying proposal count is a property of the unmodified detector. The 0.75x/1x widths belong to the agent's Q-network. This is DVFS only (Decision B). |
| resource_awareness | Yes (current) | §4.1-4.2: frequency decisions are driven by temperature and latency state. |
| energy_evaluation | No | No energy, power or battery value is reported. Power is mentioned only as motivation (§1-§2). |
| thermal_evaluation | Yes (current) | Figs. 4-7: CPU/GPU temperature traces and the throttling bound. |
| latency_evaluation | Yes | Tables 1-2: mean and SD of per-image detector latency (ms) and constraint-satisfaction rate on Jetson Orin Nano and Mi 11 Lite 5G. This is inference latency, not adaptation time. |
| multi_view, anomaly_detection | No | §5.1.2: single-image KITTI/VisDrone2019 object detection. |
| uncertainty, confidence_gating | No | No occurrence in the copy read. |

Both reachable copies are author or repository versions. The DAC version of record is closed access and was not compared. Under the Step 9.6 stop rule, nothing was applied.

### 4.4 P033: stopped

The version of record could not be verified.

**arXiv v1 (final citation block) and the earlier author manuscript agree on the pages read:**

| Topic | Evidence |
|---|---|
| Devices | Three smartphones: Google Pixel 7, Samsung Galaxy S20 FE, Samsung Galaxy A71 (§6.3; Table 6). |
| Energy | Latency and energy are profiled with 100 runs per configuration (§6.4). The §7 pages returned report optimality, throughput, latency speed-up and model switching, with no energy value. |
| Toolflow | Fig. 2: offline evaluation on a server (accuracy, size, workload) and on-device evaluation (latency, memory, energy). Inference runs on the device. |
| Runtime adaptation | The Runtime Manager switches among pre-computed designs (§4.3.4; §7.2; Table 7). This includes replacing the model with a lighter one and moving execution between processors. |

The current `adaptive_inference = Yes` and `resource_awareness = Yes` are consistent with this and were not reopened. The deferred values (smartphone Yes; cloud, energy_evaluation, thermal_evaluation, multi_view, uncertainty, confidence_gating and anomaly_detection No; latency_evaluation Yes) and the deferred free-text values stay **not applied**.

**Note:** the author-site copy is a pre-production manuscript ("Article 111", placeholder DOI) and is not a stronger source than arXiv v1.

## 5. P013 Tables 4-5: visual verification

**Result: UNRESOLVED.**

**Why no visual check was possible:**
- The UTS OPUS PDF (`opus.lib.uts.edu.au/bitstream/10453/147577/2/1-s2.0-S1474034620300707-main.pdf`) cannot be downloaded from this environment (curl: proxy CONNECT rejected).
- The reader service returns only the text layer, so the tables could not be rendered or seen.

**Text-layer values (version of record, p. 7), recorded as extracted. These are not verified values.**

Table 4, highly conservative GBT, solder-joint level, 5-fold CV:

| | True Defective | True Defect-free |
|---|---|---|
| Pred. Defective | 36 ± 14 | 91,608 ± 30,271 |
| Pred. Defect-free | 246 ± 110 | 7,570,753 ± 81,414 |
| Class recall | 98.8% ± 0.4% | 86.4% ± 4.5% |

Table 5, FOV level:

| | True Defective | True Defect-free | Average volume reduced |
|---|---|---|---|
| Pred. Defective | 41 ± 20 | 13,092 ± 1207 | ~29% |
| Pred. Defect-free | 4 ± 4 | 5463 ± 1370 | |
| Class recall | 29.4% ± 7.1% | 7.6% ± 5.2% | |

**Inconsistencies in the text layer:**
- **Table 4:** 36 / (36 + 246) ≈ 12.8%, not 98.8% or 86.4%. Also, §4.1 says the highly conservative model results "in zero false negatives", yet 246 appears in the false-negative position.
- **Table 5:** neither recall value follows from the cells as positioned.

Some cell or label positions may be transposed in extraction. Reconstructing them would be guesswork, so it was not done.

**Decision:** Tables 4-5 are not counted as verified accuracy metrics, and `accuracy_metrics` stays blank. Table 3 (initial balanced sample) is legible in the text layer, but it was held back together with Tables 4-5 in Step 9.4 and is outside this step's scope, so it is not applied either.

**Researcher action:** look at p. 7 of the PDF in a browser and confirm or correct the Table 4-5 cells.

## 6. P002 and P013 relevance reassessment

**Status of the classes:**
- The A-E classes in `audit_report.csv` are proposed auditor classes. No approved relevance field exists in the `papers.csv` schema, and Step 9.1 left that a researcher decision.
- This reassessment therefore changes neither the schema nor `audit_report.csv`. It is recorded here, with one dated sentence in each paper's `notes`.

**Decision categories:** core relevance / peripheral-contextual relevance / exclude from core corpus.

**Scope test:** [`PROJECT_SPEC.md`](../../PROJECT_SPEC.md) defines PocketInspect as smartphone-based visual inspection of physical objects or components, with resource-constrained, adaptive or resource-aware edge inference and accuracy-latency-energy trade-offs.

**Mapping to the auditor's criteria:**
- Class A ("directly relevant") requires smartphone or on-device edge **visual** defect inspection, camera-based 3D-print defect detection, or on-device inference with runtime resource or thermal adaptation.
- Class C includes "non-optical modalities".

| Paper | Decision | Evidence (full text, version of record) | Criteria met | Criteria not met |
|---|---|---|---|---|
| P002 | **Peripheral/contextual relevance (not core)** | The deployed input is a 300x1 smartphone accelerometer RMS series. Dashcam video and YOLOv5m only generate training labels (§3.1-3.2; §4.1). The task is road-condition classification (speed bumps, manholes, potholes). The TFLite model is "designed for execution on smartphones", but on-phone execution is not demonstrated or measured (§3.2; §5). | Smartphone as sensing hardware; lightweight TFLite model quantised for phones; defect detection | Not image-based visual inspection; not inspection of manufactured objects or components; on-device inference not demonstrated; no adaptive or resource-aware runtime behaviour |
| P013 | **Peripheral/contextual relevance (not core)** | Inputs are seven numeric SPI measurements per solder joint, used to predict X-ray results (§4, Table 2). A static GBT runs on an Intel Celeron N2930 industrial PC at the line (§4.2). Spark and AWS S3 serve only training and storage (§4.2; §5). Predictions route PCB fields of view around X-ray inspection (§3.3; §4.2). | Inspection of manufactured components (PCB solder joints); edge-deployed ML; reduces physical inspection volume | Not image-based (numeric process data); no smartphone; no adaptive or resource-aware inference; no latency or energy trade-off evaluation |

**Why not "Exclude from core corpus":**
- Both papers are verified, in-scope literature records that give context:
  - P002: smartphone-sensor defect detection with on-phone deployment intent;
  - P013: edge ML that decides when full physical inspection is needed.
- The corpus is kept at 54 records.
- If the researcher prefers exclusion, that is a corpus decision for a later step.

**Why not "Core":** both fail the visual-inspection criterion that defines PocketInspect's core.

**Proposed audit-class equivalent:** C (peripheral). This is not written to `audit_report.csv`.

**Status:** proposed; requires researcher approval.

## 7. Items that remain open

1. **P029, P031, P033 versions of record.** Researcher action: open the ACM DL versions in a normal browser and compare them, or explicitly accept the strongest available versions recorded in §3. For P031 the version of record is closed access. Once either is done, the deferred values in `fulltext_recoding_applied.md` can be applied without new evidence collection.
2. **P013 Tables 4-5.** Visual check of p. 7 of the version of record (see §5).
3. **P002 and P013 relevance decisions.** Researcher approval of §6.
4. **P011 Fig. 4.** The figure labels were read only in arXiv v2. A visual check of the version-of-record figure would turn the `cloud` evidence from "consistent" into "directly verified in the version of record".
