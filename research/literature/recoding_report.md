# Literature Recoding Report: Step 8.3

_Date: 2026-10-03. Coder: Claude Code. Rules: [`README.md` §7 v1.1](README.md#7-literature-coding-definitions); approval record in [`coding_decisions.md` §0](coding_decisions.md)._

> **Evidence level.** Every change below is **abstract-supported**. No full text was read in this step. P031's smartphone classification also uses the manufacturer's specification page, as Decision 6 requires. Where the abstract was not enough, the value was set or kept `Unknown`, and `notes` says `Requires full-text verification`. No records were added or deleted, and no new searches were run. Nothing here is a research-gap or novelty claim.

## 1. Summary

| Measure | Value |
| :-- | --: |
| Schema columns (before → after) | 29 → 31 |
| New fields | `confidence_gating` (after `uncertainty`), `efficiency_metrics` (after `accuracy_metrics`) |
| Records in `papers.csv` | 54 (unchanged) |
| Records with at least one recoded characteristic value (original 12 fields) | 20 |
| Characteristic values recoded (original 12 fields) | 95 |
| &nbsp;&nbsp;Unknown → No | 71 |
| &nbsp;&nbsp;Yes → Unknown | 14 |
| &nbsp;&nbsp;Unknown → Yes | 7 |
| &nbsp;&nbsp;Yes → No | 3 |
| `confidence_gating` values | Yes 1, No 6, Unknown 47 |
| `efficiency_metrics` populated | 6 (P007, P018, P028, P029, P034, P039) |
| `accuracy_metrics` values changed (efficiency figures moved out) | 5 |
| Records with appended evidence items | 24 |
| Records with notes updated (paper-type tag for all; recoding/metadata notes where applicable) | 54 |
| Records flagged `Requires full-text verification` | 14 |

## 2. Characteristic recodings (non-survey papers)

| Paper | Field | Old | New | Reason | Decision / rule | Evidence source | Support |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| P002 | `latency_evaluation` | Yes | Unknown | Abstract reports only a qualitative comparison ("outperforms conventional models in ... processing speed"); no measured timing value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P003 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: smartphone = Yes and on_device = Yes (smartphone SoC inference benchmarking) | README §7.5 consistency | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P003 | `latency_evaluation` | Yes | Unknown | Abstract states chipset "performance" was evaluated but names no timing quantity or value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P004 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: smartphone = Yes and on_device = Yes (inference deployed on Android/iOS smartphones) | README §7.5 consistency | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P004 | `resource_awareness` | Yes | Unknown | Abstract describes measuring CPU/GPU consumption (resource measurement), not a resource-driven decision | README §7.3 resource_awareness (measurement only) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P005 | `on_device` | Yes | Unknown | Static analysis of app packages; abstract does not state that inference was executed on the device | README §7.3 on_device (never inferred from static analysis) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P006 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: smartphone = Yes and on_device = Yes (DNNs measured on smartphones) | README §7.5 consistency | full abstract via Semantic Scholar (arXiv 2109.13963) | abstract-supported |
| P006 | `latency_evaluation` | Yes | Unknown | Full abstract mentions DNN "performance across devices" but names no timing quantity or value | Decision 3 (qualitative speed claims) | full abstract via Semantic Scholar (arXiv 2109.13963) | abstract-supported |
| P013 | `cloud` | Yes | Unknown | "Edge cloud" is ambiguous; abstract does not state that remote datacenter/cloud servers run the processing | README §7.3 cloud (ambiguous edge cloud) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P013 | `edge_device` | Yes | Unknown | "Edge Cloud Computing" is plant IT infrastructure, not an edge inference device | README §7.3 edge_device (edge infrastructure excluded) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P025 | `confidence_gating` | (new field) Unknown | Yes | Abstract states samples exit early via side branches when they can be inferred with high confidence | Decision 5 (confidence_gating) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P025 | `latency_evaluation` | Yes | Unknown | Abstract states inference time is "significantly" reduced but reports no measured value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P025 | `uncertainty` | Yes | Unknown | Confidence is used to trigger early exit (now coded as confidence_gating); abstract does not state that the score is estimated, calibrated or evaluated as uncertainty | Decision 5 (confidence gating is not uncertainty) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P027 | `latency_evaluation` | Yes | Unknown | Abstract states evaluations demonstrate "low-latency" edge intelligence but reports no measured value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P027 | `on_device` | Unknown | No | Abstract states computation is partitioned between device and edge (split inference) | Decision 7 (split inference) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P028 | `edge_device` | Unknown | Yes | Part of the model inference runs on the evaluated mobile development platform (edge_device covers full or partial inference on resource-constrained device hardware) | README §7.3 edge_device | abstract of ACM SIGPLAN Notices reprint via Crossref (10.1145/3093336.3037698) | abstract-supported |
| P028 | `on_device` | Unknown | No | Abstract states computation is partitioned between mobile device and datacenter (split inference) | Decision 7 (split inference) | abstract of ACM SIGPLAN Notices reprint via Crossref (10.1145/3093336.3037698) | abstract-supported |
| P029 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: on_device = Yes on mobile vision systems (resource-constrained mobile hardware) | README §7.5 consistency | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P031 | `adaptive_inference` | Yes | Unknown | Abstract describes only joint CPU/GPU frequency scaling (system-level DVFS); no change of model computation is stated. No requires full-text confirmation | Decision 4 (DVFS is not adaptive inference) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P031 | `latency_evaluation` | Yes | Unknown | Abstract states reduced latency variation and "faster inference" qualitatively; no measured value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P032 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: on_device = Yes on mobile devices with heterogeneous processors | README §7.5 consistency | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P032 | `latency_evaluation` | Yes | Unknown | Abstract states a required/consistent frame rate is maintained but reports no measured value | Decision 3 (qualitative speed claims) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P033 | `edge_device` | Unknown | Yes | Consistency rule README §7.5: on_device = Yes on heterogeneous mobile devices | README §7.5 consistency | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P034 | `latency_evaluation` | Yes | Unknown | Only adaptation time (<40 µs) is reported; adaptation time does not qualify as latency evaluation | README §7.3 latency_evaluation (adaptation time excluded) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |

## 3. Survey/review papers (Decision 1)

Reason for every row: the paper is a survey/review with no original evaluation, and discussing a capability is not evaluating it. Survey topics are recorded in `notes`. Evidence source: abstract. Support: abstract-supported.

| Paper | Fields Yes → No | Fields Unknown → No | `confidence_gating` (new) → No | Survey topics (recorded in `notes`) |
| :-- | :-- | :-- | :-- | :-- |
| P010 | none | 12 fields (all other original fields) | Yes | deep-learning-based automated visual inspection in manufacturing and maintenance (196 open-access papers) |
| P024 | none | 12 fields (all other original fields) | Yes | machine learning across additive manufacturing (design, material tuning, process optimisation, in-situ monitoring, cloud service, cybersecurity) |
| P026 | `adaptive_inference` | 11 fields (all other original fields) | Yes | dynamic neural networks (sample-wise, spatial-wise, temporal-wise adaptive computation) |
| P035 | `adaptive_inference` | 11 fields (all other original fields) | Yes | split computing and early exiting for mobile/edge DNN inference |
| P036 | none | 12 fields (all other original fields) | Yes | efficient DL inference on resource-constrained edge devices (architectures, optimisation, algorithm-hardware co-design, accelerators) |
| P052 | `uncertainty` | 11 fields (all other original fields) | Yes | uncertainty quantification methods in deep learning (Bayesian approximation, ensembles) and their applications |

## 4. Free-text field changes

| Paper | Field | Old | New | Reason | Evidence source | Support |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| P006 | `evidence` | prefix `[Verified; source: abstract via OpenAlex/Crossref abstract]` | prefix `[Verified; source: full abstract via Semantic Scholar (arXiv 2109.13963); OpenAlex abstract is truncated]` | Evidence source label corrected: claims (16k apps, energy footprint, gaugeNN) come from the full abstract, not the truncated OpenAlex abstract | Semantic Scholar record for DOI 10.1145/3487552.3487863 (retrieved 2026-10-02) | abstract-supported |
| P007 | `accuracy_metrics` | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy at 31.76 FPS on OAK-D | mAP: Tiny-YOLOv4 80.04%, YOLOv4 85.48%, YOLOv5 95% (image set); Tiny-YOLOv4 90% detection accuracy on OAK-D | Efficiency values moved out; accuracy_metrics keeps task-performance metrics only | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P007 | `efficiency_metrics` | (blank) | Tiny-YOLOv4 31.76 FPS on OAK-D | Efficiency values reported in the abstract (moved from accuracy_metrics) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P018 | `accuracy_metrics` | mAP50 97.5%; FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8 | mAP50 97.5% | Efficiency values moved out; accuracy_metrics keeps task-performance metrics only | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P018 | `efficiency_metrics` | (blank) | FPS +18.1%; GFLOPs -32.9% vs baseline YOLOv8 | Efficiency values reported in the abstract (moved from accuracy_metrics) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P028 | `accuracy_metrics` | End-to-end latency 3.1x avg (up to 40.7x) better; mobile energy -59.5% avg (up to -94.7%) | (blank) | Efficiency values moved out; accuracy_metrics keeps task-performance metrics only | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P028 | `efficiency_metrics` | (blank) | End-to-end latency 3.1x avg (up to 40.7x) better; mobile energy -59.5% avg (up to -94.7%); datacenter throughput 1.5x avg (up to 6.7x) | Efficiency values reported in the abstract (moved from accuracy_metrics; datacenter throughput added from the verified reprint abstract) | abstract of ACM SIGPLAN Notices reprint via Crossref (10.1145/3093336.3037698) | abstract-supported |
| P029 | `accuracy_metrics` | Up to +4.2% accuracy, 2.0x frame rate, 1.7x lower energy vs resource-agnostic baseline | Up to +4.2% inference accuracy vs resource-agnostic baseline | Efficiency values moved out; accuracy_metrics keeps task-performance metrics only | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P029 | `efficiency_metrics` | (blank) | Up to 2.0x video frame processing rate; up to 1.7x lower energy consumption vs resource-agnostic baseline | Efficiency values reported in the abstract (moved from accuracy_metrics) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P034 | `efficiency_metrics` | (blank) | Adaptation time < 40 µs (fully-connected network on Arduino Nano 33 BLE) | Reported adaptation-time measurement moved into the new efficiency field | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P039 | `accuracy_metrics` | Inspection speed > 400 pcs/min; accuracy > 95% | Inspection accuracy > 95% | Efficiency values moved out; accuracy_metrics keeps task-performance metrics only | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P039 | `efficiency_metrics` | (blank) | Inspection speed > 400 pcs/min | Efficiency values reported in the abstract (moved from accuracy_metrics) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |
| P042 | `limitations` | Abstract notes automated plans are hard to verify and compare with lab-developed plans. | (field-level) Abstract notes automated inspection plans are hard to verify and cannot be compared with laboratory-developed plans. | Marked as a field-level limitation, not the paper's own method limitation (README §7.6) | abstract (retrieved 2026-10-02 audit; OpenAlex/Crossref/Semantic Scholar/publisher page) | abstract-supported |

## 5. New field initialisation

- **`confidence_gating`:**
  - P025 = `Yes`: the abstract states that samples exit early when they can be inferred with high confidence.
  - The six surveys = `No` (Decision 1).
  - All other records = `Unknown`. The abstracts do not say whether a confidence score triggers an action.
  - P045 and P046 carry a note for researcher review: P045 rejects inputs to meet a risk level without naming the score, and P046 uses a learned selection head.
- **`efficiency_metrics`:** populated only where the abstract reports an efficiency figure (see §4). It is left blank elsewhere. P004 names throughput as a measured metric, but the abstract gives no value, so the field is blank and flagged for full text.

## 6. Metadata and notes corrections (from the 2026-10-02 audit)

| Paper | Correction | Source |
| :-- | :-- | :-- |
| P006 | Evidence source label corrected (§4). Alternative identifier arXiv 2109.13963 recorded in `notes` | Semantic Scholar record for DOI 10.1145/3487552.3487863 (audit 2026-10-02) |
| P007 | `notes` now record both the thematic group (G1) and the retrieval query (G4, "thermal-aware edge AI"). The group assignment itself is unchanged | `search_log.md` batch 1a |
| P054 | Alternative identifier SSRN 10.2139/ssrn.4042653 recorded in `notes`; no peer-reviewed version found as of 2026-10-02 | Crossref query (audit 2026-10-02) |
| P031 | External verification of the Mi 11 Lite as a cellular smartphone recorded in `notes` and evidence (Decision 6). The page does not use the word "smartphone" | https://www.mi.com/global/product/mi-11-lite/specs/ (accessed 2026-10-03) |
| P042 | `limitations` marked `(field-level)`; matching evidence item added | Abstract |
| P040 | Note added: multi_view stays Unknown (point-cloud representation); G5 fit awaits researcher decision | Abstract |
| P013 | `edge_device`/`cloud` recoded (§2). Relevance class D **not** resolved; full-text check still pending | Abstract |
| All 54 | `Paper type:` tag appended to `notes` (README §7.1): system/method 41, measurement study 4, dataset/benchmark 3, survey/review 6 | Abstract |

## 7. Records flagged `Requires full-text verification`

P002, P003, P004, P005, P006, P013, P025, P027, P031, P032, P034, P040, P045, P046

## 8. Values deliberately not changed

- **P027, P028 `adaptive_inference = Yes`:** both abstracts describe dynamic runtime partitioning (Decision 4).
- **P004 `latency_evaluation = Yes`:** throughput is named as a reported benchmark metric, so this is not a qualitative claim. Timing type: throughput/FPS.
- **P007, P018, P028, P029, P039 `latency_evaluation = Yes`:** measured values are reported. Timing type recorded.
- **P031:**
  - `smartphone = Yes`: externally verified (Decision 6);
  - `resource_awareness = Yes`: thermal-driven DVFS decision;
  - `thermal_evaluation = Yes`: lower CPU/GPU temperatures reported.
- **P045, P046, P048, P049, P051, P053, P054 `uncertainty = Yes`:** formal uncertainty methods: selective prediction, GP/OOD, MC dropout, ensembles.
- **P040 `anomaly_detection = Yes`:** unsupervised detection step.
- **P040 `multi_view = Unknown`:** not changed to `No` without full text.
- **P017 and P020:** left `Unknown` (see `coding_decisions.md` CD-09, CD-14).
