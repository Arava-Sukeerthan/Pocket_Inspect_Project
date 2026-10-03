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

---

# Step 9.6 follow-up: evidence completion (2026-10-03, Claude Code)

The researcher's follow-up instruction replaced the strict version-of-record requirement for P029, P031 and P033 with a narrower rule:

- Use the strongest accessible version.
- Apply a deferred value only if that copy is demonstrably the same paper and version and contains enough evidence for that field.

Sections 1-7 above are kept as the original Step 9.6 record. Where this follow-up differs from them, it supersedes them.

## 8. P029, P031, P033: strongest accessible versions

**Access.** The egress proxy still blocks:
- dl.acm.org, doi.org and arxiv.org (direct);
- core.ac.uk, web.archive.org, scholar.archive.org;
- Semantic Scholar, Unpaywall, ResearchGate;
- the UMich Deep Blue host and the CARIn author site.

All were checked with curl on 2026-10-03, and none of their PDFs can be downloaded here. The complete extracted text of each arXiv copy was retrieved through the alphaXiv full-text service and saved locally:

| Paper | Lines saved | Coverage |
|---|---|---|
| P029 | 1,632 | full text |
| P031 | 6 pages | full text |
| P033 | 2,129 | full text |

"No occurrence" below therefore means the whole text layer was searched. Text that exists only inside raster figures could not be searched.

### Version identity

| Paper | Accessible copy | Category | Bibliographic comparison with `papers.csv` | Same paper and version? |
|---|---|---|---|---|
| P029 | arXiv 1810.10090v1 (23 Oct 2018) | arXiv copy of the author camera-ready | Title, authors, year, venue (MobiCom '18, 24th Annual International Conference on Mobile Computing and Networking) and DOI all match. The first page carries the ACM permission block, the conference date and place, ACM ISBN 978-1-4503-5903-0/18/10 and the DOI. The ACM reference format states 13 pages. | **Yes.** It is the camera-ready layout with ACM's permission block. ACM's own PDF was not compared. |
| P031 | arXiv 2410.10847v1 (1 Oct 2024); the UMich Deep Blue repository copy was read earlier | arXiv copy of the author camera-ready; the repository copy is an earlier author manuscript | Title, 8 authors, year, venue (DAC '24, 61st ACM/IEEE DAC) and DOI all match. Both copies carry the DAC '24 ACM copyright block, ISBN 979-8-4007-0601-1/24/06 and the DOI. arXiv v1 gives the code URL where Deep Blue still has "[link]". | **Yes.** It is the camera-ready layout. Tables 1-2, §4.4 and §5 are identical in both copies. The closed-access ACM PDF was not compared. |
| P033 | arXiv 2409.01089v1 (2 Sep 2024) | arXiv copy of the final ACM-typeset article | Title, authors, year, venue (ACM TECS) and DOI all match. Every page footer reads "ACM Trans. Embedd. Comput. Syst., Vol. 23, No. 4, Article 60. Publication date: June 2024". The ACM reference format reads 31 pages, the running heads 60:x, and the history line "Received 14 November 2023; revised 9 April 2024; accepted 7 May 2024". | **Yes.** It is the production layout with final volume, issue, article number and DOI. |

**Judgement.** Each copy carries the publisher's own citation data for the exact DOI in `papers.csv`, and the full text is present (all sections, tables and figure captions). They are treated as sufficient for the deferred fields under the follow-up rule. The residual risk is a post-camera-ready edit in the ACM PDF that the copy does not show. This is recorded here and in each paper's `notes`.

### Field decisions applied to `papers.csv`

All previous values below were `Unknown`.

**P029** (arXiv 1810.10090v1):

| Field | New | Evidence | Location | Evidence type |
|---|---|---|---|---|
| smartphone | Yes | Evaluated on Galaxy S8, Galaxy S7 and Nexus 5 (Android 7.0); results reported from the S8 | §4.3.1 | Directly verified |
| cloud | No | On-device evaluation; §6 states the framework "does not rely on cloud connectivity" | §4.3.1; §6 | Directly verified |
| thermal_evaluation | No | No thermal, temperature or throttling term | full text searched | Directly verified |
| multi_view | No | Single-image datasets; frames from one camera are temporal, not multiple views | §4.1, Table 2 | Directly verified |
| uncertainty | No | No occurrence | full text searched | Directly verified |
| confidence_gating | No | No confidence score triggers an action; the scheduler responds to resources and app queries | full text searched; §3.3 | Directly verified |
| anomaly_detection | No | Supervised recognition | §4.1, Table 2 | Directly verified |

P029 free text was filled or refined from the same copy: dataset, hardware and model (§4.1, Table 2; §4.3.1) and limitations (§5).

**P031** (arXiv 2410.10847v1):

| Field | New | Evidence | Location | Evidence type |
|---|---|---|---|---|
| cloud | No | Detectors run on the device. The DQN frequency controller runs on a proximal desktop RTX 2080Ti over a socket, which the paper does not call cloud. Under README §7.3, a proximal server that the paper does not call cloud is `No`. | §4.4 | Directly verified + README rule |
| adaptive_inference | No | Only CPU/GPU frequency changes, twice per frame. The detector computation path is unchanged; the varying proposal count is a property of the standard two-stage detector; the 0.75x/1x widths belong to the controller's Q-network. Rule: DVFS alone is not adaptive inference. | §4.1-4.4 | Directly verified + rule (Decision B) |
| energy_evaluation | No | No energy, power or battery value. Power appears only as motivation. | full text read | Directly verified |
| multi_view | No | Single-image detection on KITTI and VisDrone2019 | §5.1.2 | Directly verified |
| uncertainty | No | No predictive uncertainty. "Uncertainty" in §3 means variable computation counts. | full text read | Directly verified |
| confidence_gating | No | No occurrence | full text read | Directly verified |
| anomaly_detection | No | Supervised Faster/Mask R-CNN detection | §5.1.2 | Directly verified |
| latency_evaluation | Yes | Measured per-image detector inference latency (mean and SD in ms over 3,000 on-device iterations) plus satisfaction rate, on Jetson Orin Nano and Mi 11 Lite 5G. This is inference latency, not adaptation time. | Tables 1-2; §5.2.1 | Directly verified |

P031 free text was filled or refined: dataset, hardware, model and efficiency_metrics. All efficiency figures were re-checked against Tables 1-2. The quoted percentage reductions follow arithmetically from the table values; for example, (768.4 − 531.4) / 768.4 = 30.8%.

**P033** (arXiv 2409.01089v1):

| Field | New | Evidence | Location | Evidence type |
|---|---|---|---|---|
| smartphone | Yes | Pixel 7, Galaxy S20 FE, Galaxy A71 | §6.3, Table 6 | Directly verified |
| cloud | No | The server does only offline conversion, accuracy evaluation and design generation; inference and the Runtime Manager run on the device. Offline use does not qualify (README §7.3). | Fig. 2, p. 60:15 | Directly verified + README rule |
| energy_evaluation | No | Energy is defined as a possible objective and profiled (100 runs), but no energy or power value appears in §7 or any table | §4.1; §6.4; §7 | Directly verified (rule 4D) |
| thermal_evaluation | No | Temperature appears only as motivation and as a 2-minute idle period to keep device temperature consistent; no temperature is measured or reported | §2.1.2; §4.3.2; §6.4 | Directly verified |
| multi_view | No | Single-input image, text and audio tasks; the UC4 face-attribute models share one image | §6.2 | Directly verified |
| uncertainty | No | No occurrence | full text searched | Directly verified |
| confidence_gating | No | Switching is triggered by processor and memory issue flags, not by confidence | §4.3.3-4.3.4; full text searched | Directly verified |
| anomaly_detection | No | Supervised classification | §6.2 | Directly verified |
| latency_evaluation | Yes | Measured on-device throughput (images/s, S20, Fig. 7), average latency and latency SD (A71, Fig. 8), and a 19.9% latency speed-up (UC2), all from on-device profiling | §6.4; §7.1.2; §7.2; Figs. 7-8 | Directly verified |

P033 free text was filled or refined: dataset, hardware, model, accuracy_metrics, efficiency_metrics and limitations (§6.2-6.3; §7; Tables 9-10; §8).

**Retained values (not reopened):** the current `Yes` values for these papers:
- P029: edge_device, on_device, adaptive_inference, resource_awareness, energy_evaluation, latency_evaluation;
- P031: smartphone, edge_device, on_device, resource_awareness, thermal_evaluation;
- P033: edge_device, on_device, adaptive_inference, resource_awareness.

Nothing in the full texts contradicts them. P031's Table 2 caption names the "Mi 11 Lite 5G"; this was noted, and no field changed.

## 9. P013 Tables 4-5: still blocked

**Attempts made:**
- direct download of the UTS OPUS PDF (proxy CONNECT 403);
- the reader service (text layer only, no rendering);
- aggregators and archives (CORE, Internet Archive, Semantic Scholar, Unpaywall): all blocked.

**Result:** no rendered page could be obtained, so the tables could not be inspected visually.

**Recorded statement (also in P013 `notes`):** "Unable to visually verify Tables 4–5; extracted text is internally inconsistent; no metrics reconstructed."

`accuracy_metrics` stays blank. The approved P013 characteristic values are unchanged.

## 10. P011 Figure 4: unavailable

The version-of-record PDF on the UNB host cannot be downloaded or rendered here; the reader returns text only, and the figure has no text layer. Per the instruction, nothing was changed. P011 keeps its Step 9.6 coding and its recorded evidence (VoR text plus arXiv v2 figure labels).

## 11. Relevance: unchanged

P002 and P013 stay **peripheral/contextual (not core)**, as proposed in §6:
- no `relevance_class` column was added;
- `audit_report.csv` was not modified.

## 12. Remaining blockers after the follow-up

1. **P013 Tables 4-5.** Visual inspection of p. 7 of the version of record. This needs a browser, a local copy of the PDF, or network access to `opus.lib.uts.edu.au`.
2. **P011 Fig. 4 (optional).** Visual check of the version-of-record figure. This needs access to `www.cs.unb.ca` or the publisher.
3. **Optional confirmation for P029/P031/P033.** Comparing the ACM PDFs in a browser would remove the residual camera-ready versus ACM-PDF risk noted in §8.

---

# Step 9.6 recovery and relevance approval (2026-10-03, Claude Code)

**Branch history.**
- PR #7 merged only the first Step 9.6 commit (`29aaf78`) into `main` (`0a63176`).
- The follow-up commit `55873a3` (§8-12) was cherry-picked unchanged onto the new branch `claude/step-9-6-recovery`, created from `origin/main`.
- No evidence, decision or methodology in §8-12 was redone or altered.

## 13. Researcher-approved relevance decisions

These decisions replace the *proposed* status recorded in §6 and §11.

| Paper | Approved decision | Reason (researcher) |
|---|---|---|
| P002 | **Peripheral/contextual, not core** | Accelerometer-based road-condition classification rather than image-based inspection |
| P013 | **Peripheral/contextual, not core** | Numeric solder-paste measurements predicting X-ray results rather than smartphone visual inspection |

**Not changed:**
- No `relevance_class` column was added to `papers.csv`.
- No A-E class was assigned.
- `audit_report.csv` is unchanged.
- Both papers stay in the 54-record corpus.

A dated sentence was appended to each paper's `notes`.

## 14. P013 Tables 4-5: still unresolved

No copy of the P013 PDF or a page image is available in this environment, and `opus.lib.uts.edu.au` is still blocked by the egress proxy.

The §9 statement stands: "Unable to visually verify Tables 4–5; extracted text is internally inconsistent; no metrics reconstructed."

- `accuracy_metrics` stays blank.
- All approved P013 characteristic values are unchanged.

A later, separate commit can resolve only this item once the PDF or a page image is supplied.
