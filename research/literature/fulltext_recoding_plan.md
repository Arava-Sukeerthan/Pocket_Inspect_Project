# Full-Text Recoding Plan (Step 9.3)

_2026-10-03, Claude Code, branch `claude/blissful-gauss-ub29pl`. A plan for a **future** controlled recoding task (README §7.7). **Nothing has been applied: `papers.csv` is unchanged.** Every row cites the evidence location recorded in the Step 9.2 evidence report (commit `86a087b`, [`fulltext_evidence_report.md`](fulltext_evidence_report.md)). Ambiguous rows are resolved in [`fulltext_decision_table.md`](fulltext_decision_table.md)._

## How to apply (future recoding task)

- Apply only the **Approved changes** below, one evidence item per changed field: `[<field>] <claim> -> <evidence> (<location>)` with the source prefix naming the full-text source and version (README §7.2).
- Append a dated note to `notes` for each change (README §7.7), set the extraction depth to `Full-text extraction (<date>)` for verified papers, and record the source version (e.g. `arXiv v1 preprint`).
- **Version-limited rows** (P011, P029, P031, P033) are marked ⚠. The researcher should decide whether to apply them now (with the version recorded in `notes`) or after a version-of-record check.
- Re-run `pytest` and `manage_literature.py validate`, and log the task in the CHANGELOG.

## Summary

| Section | Characteristic rows |
| :-- | --: |
| Approved changes | 94 (of which version-limited ⚠: 33) |
| Researcher decision required | 4 |
| Keep current value (ambiguous rows resolved as Unknown) | 9 |
| Insufficient evidence | 1 |

Approved changes = 90 Confirmed Unknown→value rows from Step 9.2 + 4 ambiguous rows approved in the decision table. Free-text metric and metadata rows are listed in the last section. Unchanged current `Yes`/`No` values that the full text confirmed are not listed. The 8 blocked papers (P001, P007, P017, P018, P019, P022, P023, P032) keep their abstract-level coding.

### Approved changes

| Paper | Field | Current | New value | Evidence location (Step 9.2) | Basis |
|---|---|---|---|---|---|
| P002 | cloud | Unknown | No | §5 | Confirmed full-text evidence (Step 9.2) |
| P002 | adaptive_inference | Unknown | No | §3.2 (Algorithm 1); §4.3 | Rule 4C: the sliding window only changes where/how often the fixed RDD-CNN is invoked on the accelerometer stream; the model's computation per window never changes. README §7.3: static inference graph → No. The full text was read. |
| P002 | resource_awareness | Unknown | No | §3.2; §4.3 | Confirmed full-text evidence (Step 9.2) |
| P002 | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P002 | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P002 | multi_view | Unknown | No | §3.2; §4.1 | Confirmed full-text evidence (Step 9.2) |
| P002 | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P002 | anomaly_detection | Unknown | No | §3.2; §4.3 | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | smartphone | Unknown | Yes | §5.5.1-5.5.2, pp. 13-14; Fig. 7, p. 15 | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | adaptive_inference | Unknown | No | §5.5 | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | resource_awareness | Unknown | No | §5.5.1, pp. 13-14 | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | multi_view | Unknown | No | §6.1; §7.1 | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | confidence_gating | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P011 ⚠ | anomaly_detection | Unknown | No | §5.1 | Confirmed full-text evidence (Step 9.2) |
| P015 | smartphone | Unknown | No | Methods - CAXTON system | Confirmed full-text evidence (Step 9.2) |
| P015 | edge_device | Unknown | No | Online correction and parameter discovery pipeline; Computing and software requirements | Confirmed full-text evidence (Step 9.2) |
| P015 | on_device | Unknown | No | Same as edge_device | Confirmed full-text evidence (Step 9.2) |
| P015 | cloud | Unknown | No | Online correction pipeline; Computing and software requirements | Confirmed full-text evidence (Step 9.2) |
| P015 | adaptive_inference | Unknown | No | Online correction and parameter discovery pipeline | Confirmed full-text evidence (Step 9.2) |
| P015 | resource_awareness | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P015 | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P015 | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P015 | multi_view | Unknown | No | Methods - CAXTON system; Discussion | Confirmed full-text evidence (Step 9.2) |
| P015 | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P015 | anomaly_detection | Unknown | No | Results - Dataset generation; Model architecture | Confirmed full-text evidence (Step 9.2) |
| P016 | smartphone | Unknown | No | §3, p. 12 | Confirmed full-text evidence (Step 9.2) |
| P016 | edge_device | Unknown | Yes | §3, p. 12 | Confirmed full-text evidence (Step 9.2) |
| P016 | on_device | Unknown | Yes | §3, p. 12 | Confirmed full-text evidence (Step 9.2) |
| P016 | cloud | Unknown | No | §2.2, p. 8; §3, p. 12 | Confirmed full-text evidence (Step 9.2) |
| P016 | adaptive_inference | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P016 | resource_awareness | Unknown | No | §2.2, p. 7 | Confirmed full-text evidence (Step 9.2) |
| P016 | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P016 | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P016 | multi_view | Unknown | No | §3, p. 12; §1.2, p. 3 | Confirmed full-text evidence (Step 9.2) |
| P016 | uncertainty | Unknown | No | §2.3, p. 10; §3 | Confirmed full-text evidence (Step 9.2) |
| P016 | confidence_gating | Unknown | Yes | §3, pp. 12-13; §4, p. 13 | Confirmed full-text evidence (Step 9.2) |
| P016 | anomaly_detection | Unknown | No | §2.1-2.2, p. 7 | Confirmed full-text evidence (Step 9.2) |
| P016 | latency_evaluation | Unknown | Yes | §3, p. 12; §2.2, p. 7 | Confirmed full-text evidence (Step 9.2) |
| P020 | smartphone | Unknown | No | §3, p. 5; §4.1, p. 13 | Confirmed full-text evidence (Step 9.2) |
| P020 | cloud | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P020 | adaptive_inference | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P020 | resource_awareness | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P020 | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P020 | thermal_evaluation | Unknown | No | Table 3, p. 14 | Confirmed full-text evidence (Step 9.2) |
| P020 | multi_view | Unknown | No | §4.2, p. 13; §5.4, p. 17 | Confirmed full-text evidence (Step 9.2) |
| P020 | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P020 | confidence_gating | Unknown | No | §3.3, pp. 9-10 | Confirmed full-text evidence (Step 9.2) |
| P020 | anomaly_detection | Unknown | No | §3.4, p. 10 | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | smartphone | Unknown | Yes | §4.3.1 | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | cloud | Unknown | No | §4.3.1; §6 | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | multi_view | Unknown | No | §4.1 | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | confidence_gating | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P029 ⚠ | anomaly_detection | Unknown | No | §4.1 | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | cloud | Unknown | No | §4.4 | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | adaptive_inference | Unknown | No | §4.1-4.4 | Confirmed full-text evidence (Step 9.2); Decision B |
| P031 ⚠ | energy_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2); Decision B |
| P031 ⚠ | multi_view | Unknown | No | §5.1.2 | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | confidence_gating | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | anomaly_detection | Unknown | No | §5.1.2 | Confirmed full-text evidence (Step 9.2) |
| P031 ⚠ | latency_evaluation | Unknown | Yes | Tables 1-2; §5.2.1 | Confirmed full-text evidence (Step 9.2); Decision B |
| P033 ⚠ | smartphone | Unknown | Yes | §6.3, p. 60:19 | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | cloud | Unknown | No | Fig. 2, p. 60:15 | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | energy_evaluation | Unknown | No | §4.1; §6.4, pp. 60:19-60:20; §7 | Rule 4D: §6.4 describes profiling latency and energy (100 runs), but §7 reports no energy or power value. README §7.3: no energy results after reading the full text → No. Evidence is from an arXiv copy whose version is not confirmed; apply only with the P033 version check. |
| P033 ⚠ | thermal_evaluation | Unknown | No | §2.1.2; §4.3; §6.4 | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | multi_view | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | confidence_gating | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | anomaly_detection | Unknown | No | §6.2 | Confirmed full-text evidence (Step 9.2) |
| P033 ⚠ | latency_evaluation | Unknown | Yes | §7; Figs. 7-8 | Confirmed full-text evidence (Step 9.2) |
| P034 | smartphone | Unknown | Yes | §VI, p. 461; Fig. 10, p. 462 | Confirmed full-text evidence (Step 9.2) |
| P034 | cloud | Unknown | No | §IV-A, p. 458; Acknowledgment, p. 463 | Confirmed full-text evidence (Step 9.2) |
| P034 | energy_evaluation | Unknown | Yes | Table VI and text, p. 463 | Confirmed full-text evidence (Step 9.2) |
| P034 | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P034 | multi_view | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P034 | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P034 | confidence_gating | Unknown | No | §I, p. 452; Fig. 11, p. 462 | Confirmed full-text evidence (Step 9.2) |
| P034 | anomaly_detection | Unknown | No | §IV | Confirmed full-text evidence (Step 9.2) |
| P034 | latency_evaluation | Unknown | Yes | §VI, pp. 461-463; Fig. 10 | Confirmed full-text evidence (Step 9.2) |
| P013 | smartphone | Unknown | No | §4.2, p. 7 | Confirmed full-text evidence (Step 9.2); Decision A |
| P013 | edge_device | Unknown | Yes | §2.2, p. 2; §4.2, p. 7 | Decision A (approved): an industrial PC performing inference locally at the production line is an edge device. The GBT model runs on the Intel Celeron N2930 industrial PC at the SMT line (§4.2, p. 7). |
| P013 | on_device | Unknown | Yes | §4.2, p. 7 | Decision A (approved): inference runs locally on the industrial PC at the physical production site (§4.2, p. 7). Training/storage infrastructure (Spark cluster, AWS S3) is not the inference location. |
| P013 | cloud | Unknown | No | §4.2, p. 7; §5, p. 8 | Confirmed full-text evidence (Step 9.2); Decision A |
| P013 | adaptive_inference | Unknown | No | §3.3, p. 5; §4.2, pp. 6-7 | Confirmed full-text evidence (Step 9.2) |
| P013 | energy_evaluation | Unknown | No | §3.4, p. 5 | Confirmed full-text evidence (Step 9.2) |
| P013 | thermal_evaluation | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P013 | multi_view | Unknown | No | §4, Table 2, p. 6 | Confirmed full-text evidence (Step 9.2) |
| P013 | uncertainty | Unknown | No | full text read; no occurrence | Confirmed full-text evidence (Step 9.2) |
| P013 | anomaly_detection | Unknown | No | §3.2, p. 4; §4.1, p. 6 | Confirmed full-text evidence (Step 9.2) |

### Researcher decision required

| Paper | Field | Current | New value | Evidence location (Step 9.2) | Open question |
|---|---|---|---|---|---|
| P011 ⚠ | cloud | Unknown | Unknown | §4 (module 6); §5.6, p. 14; Fig. 4 | GPT-4 Vision is called remotely to generate explanation text; the inspection inference (segmentation) runs on the phone. README §7.3 `cloud` covers "inference or decision processing"; whether remote explanation generation counts is not decided by the definition. Evidence is from an arXiv preprint. |
| P011 ⚠ | latency_evaluation | Unknown | Unknown (candidate No) | Table 4 caption; §8.3, p. 25 | No timing value anywhere; the Table 4 caption mentions running time but the table has no time column; §8.3 mentions possible explanation latency only as a limitation. README §7.3 `No` (full text read, no timing) would apply, but the evidence is from an arXiv preprint and the version of record was not checked. |
| P013 | resource_awareness | Unknown | Unknown | §3.2, p. 4; §3.4, p. 5; §4.1, p. 6 | GBT was chosen over SVM because scoring was eight times faster "with future scaling" in mind, and takt time sets the real-time constraint; but the paper says the scoring-time constraint is mostly not delimiting and states no device budget. Whether this is a resource-driven deployment decision (README §7.3) is a judgement call. |
| P013 | latency_evaluation | Unknown | Unknown | §4.1, Table 3, pp. 6-7; §4.2, p. 7 | Table 3 scoring times give no hardware ("description of hardware used is omitted"). On the stated edge PC, test sets are processed in "less than one minute", an upper bound with no test-set size, so it is neither per-inference latency nor throughput. Whether such a coarse bound on stated hardware qualifies under Rule 4E is a researcher decision. |

Also open (not CSV characteristic changes):

- **P002 relevance:** proposed Class A — requires reassessment (not image-based; accelerometer input).
- **P013 relevance:** proposed Class D — requires reassessment (not image-based; numeric SPI input).
- **Version-limited rows** (⚠ above): apply now with the version noted, or after a version-of-record check.
- **P013 `accuracy_metrics`:** Table 4-5 cell values looked inconsistent in the extracted text; check the PDF visually before recording Table 4-5 values (Table 3 values are clear).

### Keep current value

| Paper | Field | Current | New value | Evidence location (Step 9.2) | Reason |
|---|---|---|---|---|---|
| P002 | edge_device | Unknown | Unknown | §3.2 (last paragraph); §4.1; §5 | Rule 4A: the TFLite model is "designed for execution on smartphones" and on-phone classification is stated as the scope, but local execution is never demonstrated or measured. README §7.3: intended deployment is not enough for Yes. |
| P002 | on_device | Unknown | Unknown | §3.2; §4.1; §5 | Rule 4A, same evidence as edge_device. Intended on-phone deployment, not demonstrated execution. |
| P002 | confidence_gating | Unknown | Unknown | §3.1.2; §4.2 | Rule 4B: the only gate is the label-quality verifier (≥90% agreement among 30 YOLOv5m frame labels) used to build the training set. It is a vote-agreement check during data generation, not a confidence/probability score triggering an action in the deployed system. Not Yes; documented as Unknown rather than forced to No. |
| P002 | latency_evaluation | Unknown | Unknown | §4.1; §4.3; §5 | Rule 4E is met for quantity (processing time per minute of data), but README §7.3 also requires stated or identifiable hardware, and none is given for the timing. Not Yes. |
| P015 | confidence_gating | Unknown | Unknown | Online correction and parameter discovery pipeline | Rule 4B: a correction fires when one predicted class reaches the mode-threshold share of the last L predictions. This is a vote frequency over repeated predictions, not a confidence/probability score. Not Yes. |
| P020 | edge_device | Unknown | Unknown | §3, p. 5; §4.1, p. 13; §5.4, p. 17 | Rule 4A: a Raspberry Pi 4B is "used for the processing", but programming, training and testing were done in MATLAB and the location of real-time classification is never stated. |
| P020 | on_device | Unknown | Unknown | §3, p. 5; §4.1, p. 13 | Rule 4A, same evidence as edge_device. |
| P020 | latency_evaluation | Unknown | Unknown | §5.4, p. 17; §6, p. 18 | Rule 4E: "less computational time" is a qualitative claim with no timing value, so not Yes. README Decision 3 keeps qualitative speed claims Unknown. |
| P013 | confidence_gating | Unknown | Unknown | §3.3, p. 5; §4.1-4.2, pp. 6-7 | Rule 4B: fields of view predicted defect-free skip X-ray, and the model is tuned to be conservative, but the action is triggered by the predicted class; no confidence/probability score or threshold is described. Not Yes; Unknown rather than No because the conservativeness tuning mechanism is not described. |

### Insufficient evidence

| Paper | Field | Current | New value | Evidence location (Step 9.2) | Reason |
|---|---|---|---|---|---|
| P015 | latency_evaluation | Unknown | Unknown | Online correction pipeline; Methods; Discussion | Step 9.2: deciding content (figures/supplement) not visible. |

Also insufficient evidence (whole paper, no full text): P001, P007, P017, P018, P019, P022, P023, P032. Their abstract-level coding stays.

## Free-text fields (supported; apply with the characteristic changes)

Values are in [`fulltext_conflicts.md`](fulltext_conflicts.md) §2 (metrics) and §3 (metadata), with locations. They fill blank fields or replace generic abstract-level text and do not change any characteristic value.

| Paper | Fields | Evidence locations (Step 9.2) | Note |
|---|---|---|---|
| P002 | accuracy_metrics, efficiency_metrics, dataset, hardware, model, limitations | §4.2; §4.3; §5; §4.1; §4.3; §5; §4.1; §4.3; §4.1; §3.1.2; §3.2; §4.3; §4.2; §4.3 | per-model accuracies are in a figure not visible in the PMC extraction |
| P011 | accuracy_metrics, efficiency_metrics, dataset, hardware, model, limitations | Table 3, p. 17; Table 6, p. 23; Table 3, p. 17; §6.1, p. 15; §7.1; §5.5.2; §5.6; Fig. 7; §4; §5; §8.3, p. 25 | ⚠ version-limited |
| P015 | accuracy_metrics, dataset, hardware, model, limitations | Results - Model architecture, training and performance; Methods - Training procedure; Results - Dataset generation, filtering and augmentation; Methods - Training procedure; Methods - CAXTON system; Computing and software requirements; Results - Model architecture; Discussion |  |
| P016 | accuracy_metrics, efficiency_metrics, dataset, hardware, model, limitations | §3, pp. 11-12; §3, p. 12; §2.1, p. 7; §2.2, p. 8; §3, p. 12; §2.2, pp. 7-8 |  |
| P020 | accuracy_metrics, dataset, hardware, model | Tables 5-7, pp. 15-17; §3.4, p. 10; §4.2, pp. 13-14; §3, p. 5; §4.1, p. 13; §3.2-3.3, pp. 6-10; §5.4, p. 17 |  |
| P029 | dataset, hardware, model, limitations | §4.1, Table 2; §4.3.1; §5 | ⚠ version-limited |
| P031 | efficiency_metrics, dataset, hardware, model | Tables 1-2; §4.4.2; §5.2.1; §5.1.2; §4.4; §4.3.4; §4.4.1; §5.1.2 | ⚠ version-limited |
| P033 | accuracy_metrics, efficiency_metrics, dataset, hardware, model, limitations | §7.1.2; §7.2.1; §7.2.2; §7.1.2-7.1.3; §7.2; Tables 9-10, p. 60:25; §6.2; §6.3; §4; §6.2; §8, p. 60:26 | ⚠ version-limited |
| P034 | accuracy_metrics, efficiency_metrics, hardware, model, limitations | §IV-B, p. 458; Tables III-IV, p. 460; §V-B, p. 461; §VI, pp. 462-463; Table VI; §IV-A, p. 458; §V-B, p. 461; §VI, pp. 461-463; §III; §IV-A; §VII, p. 463 |  |
| P013 | accuracy_metrics, efficiency_metrics, dataset, hardware, model, limitations | Tables 3-5, p. 7; Table 3, p. 7; §4.2, p. 7; §4, Table 2, p. 6; §4.2, p. 7; §4.1, p. 6; §4.3, p. 7 | accuracy_metrics: use Table 3 values; Tables 4-5 need a visual check (researcher decision) |
