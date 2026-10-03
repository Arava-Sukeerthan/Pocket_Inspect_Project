# Full-Text Decision Table (Step 9.3)

_2026-10-03, Claude Code, branch `claude/blissful-gauss-ub29pl`. Built only from the Step 9.2 evidence in commit `86a087b` ([`fulltext_evidence_report.md`](fulltext_evidence_report.md), [`fulltext_conflicts.md`](fulltext_conflicts.md)). The earlier attempt `9643e43` is not an evidence source. **`papers.csv` was not modified**; nothing here is applied until a separate controlled recoding step (README §7.7). See [`fulltext_recoding_plan.md`](fulltext_recoding_plan.md)._

## Rules applied

- **Definitions:** README §7 v1.1 and `coding_decisions.md`, unchanged.
- **Approved researcher decisions (Step 9.3 instruction):**
  - **Decision A (industrial PC):** an industrial PC performing inference locally at the production line is an edge device. For P013: `smartphone = No`, `edge_device = Yes`, `on_device = Yes`, `cloud = No`. Training/storage infrastructure is not the inference location.
  - **Decision B (P031):** DVFS/frequency control with unchanged detector computation → `adaptive_inference = No`; measured latency in Tables 1-2 → `latency_evaluation = Yes`; keep `thermal_evaluation = Yes`, `energy_evaluation = No`.
  - **Decision C (relevance):** P002 and P013 keep their proposed classes (A and D) marked *requires reassessment*. No new class is assigned; `audit_report.csv` is unchanged.
- **Ambiguity rules (Step 9.3 §4):** 4A intended deployment ≠ demonstrated on-device execution; 4B only a confidence/probability (or explicitly equivalent predictive confidence/uncertainty) signal triggering an action is `confidence_gating`; 4C stream/window skipping counts as adaptive inference only if the model computation itself changes; 4D described energy profiling ≠ reported energy results; 4E only quantitative timing qualifies.
- **Status vocabulary:** APPROVED FOR RECODING / NEEDS RESEARCHER DECISION / KEEP CURRENT VALUE / INSUFFICIENT EVIDENCE. No ambiguity is converted to Yes or No without a stated rule or approved decision.

## Summary

| Status | Rows |
| :-- | --: |
| APPROVED FOR RECODING | 4 |
| NEEDS RESEARCHER DECISION | 4 |
| KEEP CURRENT VALUE | 9 |
| INSUFFICIENT EVIDENCE | 0 |
| **Total ambiguous rows (Step 9.2)** | **17** |

Values in the *Candidate value* column for KEEP CURRENT VALUE rows equal the current value. All current values are `Unknown`.

## Decision table: the 17 ambiguous characteristic rows

| ID | Paper | Field | Current value | Full-text evidence | Candidate value | Decision status | Reason |
|---|---|---|---|---|---|---|---|
| D01 | P002 | edge_device | Unknown | The quantized RDD-CNN is converted with the TFLite Converter and is "designed for execution on smartphones"; the conclusions state the scope is real-time classification on local smartphones. No on-phone run or on-phone timing is described. (§3.2 (last paragraph); §4.1; §5) | Unknown | KEEP CURRENT VALUE | Rule 4A: the TFLite model is "designed for execution on smartphones" and on-phone classification is stated as the scope, but local execution is never demonstrated or measured. README §7.3: intended deployment is not enough for Yes. |
| D02 | P002 | on_device | Unknown | Same evidence as edge_device: on-phone execution is stated as intended and as the scope, but not described as executed or measured. (§3.2; §4.1; §5) | Unknown | KEEP CURRENT VALUE | Rule 4A, same evidence as edge_device. Intended on-phone deployment, not demonstrated execution. |
| D03 | P002 | adaptive_inference | Unknown | The RDD-CNN is fixed. A sliding window (3 s, 0.1 s stride) jumps ahead after a detection, so the number of tests per minute depends on the input. This changes how often the model is invoked, not the model's computation; whether such stream-level skipping counts is not covered by the §7.3 table. Leaning No. (§3.2 (Algorithm 1); §4.3) | No | APPROVED FOR RECODING | Rule 4C: the sliding window only changes where/how often the fixed RDD-CNN is invoked on the accelerometer stream; the model's computation per window never changes. README §7.3: static inference graph → No. The full text was read. |
| D04 | P002 | confidence_gating | Unknown | Label quality verifier: a sliced sample is kept only if at least 90% of its 30 YOLOv5m frame classifications agree; otherwise it is discarded. This is a vote-consistency gate during dataset construction, not a confidence score acting on the deployed classifier. (§3.1.2; §4.2) | Unknown | KEEP CURRENT VALUE | Rule 4B: the only gate is the label-quality verifier (≥90% agreement among 30 YOLOv5m frame labels) used to build the training set. It is a vote-agreement check during data generation, not a confidence/probability score triggering an action in the deployed system. Not Yes; documented as Unknown rather than forced to No. |
| D05 | P002 | latency_evaluation | Unknown | Average time per model to evaluate 1 min of test data is reported (about 0.1 s per minute of driving for RDD-CNN), but the hardware used for the timing is not stated; preprocessing ran in a Linux/Python 3.8.10 environment. README §7.3 requires stated or identifiable hardware. (§4.1; §4.3; §5) | Unknown | KEEP CURRENT VALUE | Rule 4E is met for quantity (processing time per minute of data), but README §7.3 also requires stated or identifiable hardware, and none is given for the timing. Not Yes. |
| D06 | P011 | cloud | Unknown | Textual explanations are generated by calling the GPT-4 Vision API, and Fig. 4 places the domain-expert web app in a "Cloud Environment". The segmentation (the inspection inference) stays on the device. Whether remote explanation generation counts as "inference or decision processing" under README §7.3 is open. (§4 (module 6); §5.6, p. 14; Fig. 4) | Unknown | NEEDS RESEARCHER DECISION | GPT-4 Vision is called remotely to generate explanation text; the inspection inference (segmentation) runs on the phone. README §7.3 `cloud` covers "inference or decision processing"; whether remote explanation generation counts is not decided by the definition. Evidence is from an arXiv preprint. **Version-limited evidence (arXiv preprint v2).** |
| D07 | P011 | latency_evaluation | Unknown | No inference timing is reported. The Table 4 caption mentions running time in seconds, but the table has no time column in the text read. §8.3 says explanation generation on edge devices "may introduce latency" (limitation). Leaning No. (Table 4 caption; §8.3, p. 25) | Unknown (candidate No) | NEEDS RESEARCHER DECISION | No timing value anywhere; the Table 4 caption mentions running time but the table has no time column; §8.3 mentions possible explanation latency only as a limitation. README §7.3 `No` (full text read, no timing) would apply, but the evidence is from an arXiv preprint and the version of record was not checked. **Version-limited evidence (arXiv preprint v2).** |
| D08 | P013 | edge_device | Unknown | The GBT model runs on an edge device at the SMT line: an industrial PC with an Intel Celeron N2930. The paper defines an edge device as any computing or networking resource between data sources and the cloud. Whether a low-power industrial PC counts as resource-constrained hardware (README §7.3) or as plant IT is open. (§2.2, p. 2; §4.2, p. 7) | Yes | APPROVED FOR RECODING | Decision A (approved): an industrial PC performing inference locally at the production line is an edge device. The GBT model runs on the Intel Celeron N2930 industrial PC at the SMT line (§4.2, p. 7). |
| D09 | P013 | on_device | Unknown | The edge PC receives and parses SPI result files (CAMX-XML) over TCP/IP; it is not the capturing device or hardware attached to it. Leaning No, but tied to the industrial-PC question. (§4.2, p. 7) | Yes | APPROVED FOR RECODING | Decision A (approved): inference runs locally on the industrial PC at the physical production site (§4.2, p. 7). Training/storage infrastructure (Spark cluster, AWS S3) is not the inference location. |
| D10 | P013 | resource_awareness | Unknown | GBT chosen over SVM because its scoring time was eight times faster, "with future scaling" in mind; takt time sets the real-time constraint. A deployment-time choice informed by timing, without an explicit device budget. (§3.2, p. 4; §3.4, p. 5; §4.1, p. 6) | Unknown | NEEDS RESEARCHER DECISION | GBT was chosen over SVM because scoring was eight times faster "with future scaling" in mind, and takt time sets the real-time constraint; but the paper says the scoring-time constraint is mostly not delimiting and states no device budget. Whether this is a resource-driven deployment decision (README §7.3) is a judgement call. |
| D11 | P013 | confidence_gating | Unknown | Fields of view predicted defect-free skip X-ray; the model is tuned to be conservative (penalising false negatives). The routing is triggered by the predicted class; no confidence score or threshold is described. (§3.3, p. 5; §4.1-4.2, pp. 6-7) | Unknown | KEEP CURRENT VALUE | Rule 4B: fields of view predicted defect-free skip X-ray, and the model is tuned to be conservative, but the action is triggered by the predicted class; no confidence/probability score or threshold is described. Not Yes; Unknown rather than No because the conservativeness tuning mechanism is not described. |
| D12 | P013 | latency_evaluation | Unknown | Table 3 gives scoring times per 1,000 rows, but "the description of hardware used is omitted". On the edge PC (Celeron N2930), current test sets are processed in under one minute: an upper bound, not a per-item timing. (§4.1, Table 3, pp. 6-7; §4.2, p. 7) | Unknown | NEEDS RESEARCHER DECISION | Table 3 scoring times give no hardware ("description of hardware used is omitted"). On the stated edge PC, test sets are processed in "less than one minute", an upper bound with no test-set size, so it is neither per-inference latency nor throughput. Whether such a coarse bound on stated hardware qualifies under Rule 4E is a researcher decision. |
| D13 | P015 | confidence_gating | Unknown | Predictions per parameter are stored in lists of length L; a correction is made only if one class reaches the mode-threshold share of the list, and that share scales the update. A vote frequency over repeated predictions, not a model confidence score. (Online correction and parameter discovery pipeline) | Unknown | KEEP CURRENT VALUE | Rule 4B: a correction fires when one predicted class reaches the mode-threshold share of the last L predictions. This is a vote frequency over repeated predictions, not a confidence/probability score. Not Yes. |
| D14 | P020 | edge_device | Unknown | A Raspberry Pi 4B "is used for the processing" with a 7-inch display, but "all the programming, training, and testing are done in Matlab". Where the real-time classification runs is not stated. (§3, p. 5; §4.1, p. 13; §5.4, p. 17) | Unknown | KEEP CURRENT VALUE | Rule 4A: a Raspberry Pi 4B is "used for the processing", but programming, training and testing were done in MATLAB and the location of real-time classification is never stated. |
| D15 | P020 | on_device | Unknown | Same ambiguity as edge_device. (§3, p. 5; §4.1, p. 13) | Unknown | KEEP CURRENT VALUE | Rule 4A, same evidence as edge_device. |
| D16 | P020 | latency_evaluation | Unknown | AlexNet+SVM is chosen for "less computational time" with no timing value. README Decision 3 keeps qualitative claims Unknown, while §7.3 says No once the full text is read and no timing is reported. Which rule applies after full-text reading is a researcher decision. (§5.4, p. 17; §6, p. 18) | Unknown | KEEP CURRENT VALUE | Rule 4E: "less computational time" is a qualitative claim with no timing value, so not Yes. README Decision 3 keeps qualitative speed claims Unknown. |
| D17 | P033 | energy_evaluation | Unknown | Energy is a listed objective and is profiled on the device (100 runs per configuration), but no energy value is reported in the results. Leaning No. (§4.1; §6.4, pp. 60:19-60:20; §7) | No | APPROVED FOR RECODING | Rule 4D: §6.4 describes profiling latency and energy (100 runs), but §7 reports no energy or power value. README §7.3: no energy results after reading the full text → No. Evidence is from an arXiv copy whose version is not confirmed; apply only with the P033 version check. **Version-limited evidence (arXiv copy in journal layout, version not confirmed).** |

**Related row outside the 17.** P015 `latency_evaluation` was marked *Insufficient evidence* in Step 9.2 (not Ambiguous): no inference timing appears in the running text, and the figures/supplement were not visible in the PMC extraction. Status: **INSUFFICIENT EVIDENCE**; current `Unknown` kept.

## P002 — modality/relevance

| Item | Finding | Evidence (Step 9.2) |
|---|---|---|
| Deployed input | Smartphone accelerometer signals (3-axis, 100 Hz; RMS series, 300 x 1 per 3-s window) | §3.1.1; §3.2; §4.1 |
| Dashcam / YOLOv5m | Used only to label training data automatically (label quality verifier); not part of the deployed classifier | §3.1.2; §4.2 |
| Deployed task | Classifying speed bumps, manholes and potholes from vehicle vibration: **not image-based visual inspection** | §1; §3 |
| Smartphone role | Sensing hardware (Galaxy Note8, Redmi Note 10 Pro, LG Q7); `smartphone = Yes` stays | §3.1.1; §4.1 |
| On-phone execution | Intended (TFLite, "designed for execution on smartphones"), not demonstrated → `edge_device`/`on_device` stay Unknown (D01, D02) | §3.2; §4.1; §5 |
| Relevance status | **Proposed Class A — requires reassessment.** No new class assigned; `audit_report.csv` unchanged; paper stays in the database | Decision C |

## P013 — industrial edge inference / relevance

| Item | Finding | Evidence (Step 9.2) |
|---|---|---|
| Model input | Seven numeric SPI measurements per solder joint (height, shape 2D, shape 3D, surface, volume, offset X, offset Y) | §4, Table 2, p. 6 |
| Task | Predicting X-ray inspection results so that defect-free fields of view skip X-ray (~29% average volume reduction) | §4.1-4.2, pp. 6-7; Table 5 |
| Inference hardware | Local inference on an industrial PC with Intel Celeron N2930 at the SMT line | §4.2, p. 7 |
| Training / storage | Company Spark cluster (training), AWS S3 (storage) | §4.2, p. 7; §5, p. 8 |
| Cloud | Inference is **not** cloud-based; cloud used only for training/storage → `cloud = No` | §4.2; §5 |
| Candidate coding (Decision A) | `smartphone = No`, `edge_device = Yes` (D08), `on_device = Yes` (D09), `cloud = No` | Decision A |
| Modality | **Not image-based visual inspection**: the SPI station is optical, but the model sees only its numeric output | §1; §4 |
| Relevance status | **Proposed Class D — requires reassessment.** No new class assigned; `audit_report.csv` unchanged; paper stays in the database | Decision C |

## P031 — final candidate coding (Decision B)

| Field | Current | Candidate | Evidence (Step 9.2) | Status |
|---|---|---|---|---|
| smartphone | Yes | Yes | §4.4; Table 2 caption | KEEP CURRENT VALUE |
| edge_device | Yes | Yes | §4.4; §5 | KEEP CURRENT VALUE |
| on_device | Yes | Yes | §5.1.2; §5.2.1 | KEEP CURRENT VALUE |
| cloud | Unknown | No | §4.4 | APPROVED FOR RECODING |
| adaptive_inference | Unknown | No | §4.1-4.4 | APPROVED FOR RECODING |
| resource_awareness | Yes | Yes | §4.3.2 | KEEP CURRENT VALUE |
| energy_evaluation | Unknown | No | full text read; no occurrence | APPROVED FOR RECODING |
| thermal_evaluation | Yes | Yes | §4.1; §5.2; Figs. 4-7 | KEEP CURRENT VALUE |
| multi_view | Unknown | No | §5.1.2 | APPROVED FOR RECODING |
| uncertainty | Unknown | No | full text read; no occurrence | APPROVED FOR RECODING |
| confidence_gating | Unknown | No | full text read; no occurrence | APPROVED FOR RECODING |
| anomaly_detection | Unknown | No | §5.1.2 | APPROVED FOR RECODING |
| latency_evaluation | Unknown | Yes | Tables 1-2; §5.2.1 | APPROVED FOR RECODING |

No full-text evidence contradicts Decision B. P031 evidence is from the arXiv v1 preprint (DAC '24 copyright block); the version of record is closed access. Decision B is approved by the researcher, so its rows are approved for recoding with that version limitation recorded.

## Version limitations

| Paper | Evidence version | Status |
|---|---|---|
| P011 | arXiv preprint 2407.11771v2; Information Fusion version of record not compared | Partially verified (preprint) |
| P029 | arXiv preprint 1810.10090v1 (MobiCom '18 permission block); ACM version not compared | Partially verified (preprint) |
| P031 | arXiv preprint 2410.10847v1 (DAC '24 copyright block); version of record closed access | Partially verified (preprint) |
| P033 | arXiv copy 2409.01089v1 in ACM TECS layout; ACM page not compared | Partially verified (version not confirmed) |
| P034 | FH JOANNEUM repository copy in IEEE TMC final layout (pp. 451-464, CC BY); OpenAlex labels it "submittedVersion" | Fully verified, label conflict recorded (unchanged) |

None of P011, P029, P031 or P033 is treated as publisher-version verified.
