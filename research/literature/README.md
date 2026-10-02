# Literature Management Subsystem (`research/literature/`)

This directory holds PocketInspect's verified literature records, search logs, human-readable summaries, and the generated literature matrix.

| File | Purpose |
| :--- | :--- |
| `papers.csv` | Main literature database (one row per verified paper, 29-column schema below) |
| `selected_papers.md` | Human-readable summary of every retained paper, with per-claim evidence records, plus rejected/deferred candidates |
| `search_log.md` | Every search batch: date, group, exact query, source, hits, screened count, retained IDs, rationale |
| `literature_matrix.csv` | Generated from `papers.csv` by `scripts/manage_literature.py matrix`. Do not edit by hand. |

> **Status:** Literature collection is ongoing. Nothing in this directory establishes a research gap or a novelty claim (see `RESEARCH_RULES.md`). Gap analysis in `research/gap_analysis/` is deferred until enough verified literature exists and a human researcher reviews it.

---

## 1. How papers are collected

Searches are organised into six groups:

| Group | Theme |
| :--- | :--- |
| G1 | Smartphone / mobile AI / on-device edge AI |
| G2 | Industrial visual inspection |
| G3 | 3D-printed part inspection |
| G4 | Adaptive / resource-aware inference (incl. energy, thermal, latency) |
| G5 | Multi-view / active inspection |
| G6 | Confidence / uncertainty / selective prediction |

For each group:

1. Run keyword queries against a scholarly index (batch 1 used the OpenAlex API). Broad queries are followed by narrower title/abstract queries when results are noisy. Known-item title lookups are allowed but must be labelled as such in `search_log.md`.
2. Screen the top-ranked results for relevance. Peer-reviewed venues and 2019–2026 publications are preferred. Foundational older works are kept only when later work builds on them. arXiv is used only when no peer-reviewed version is found.
3. Record every query, its hit count, how many results were screened and which paper IDs were retained in `search_log.md`.

## 2. How papers are verified

A paper is added only after all of the following succeed:

1. **Existence and metadata**: title, authors, year and venue are cross-checked between Crossref and OpenAlex. When the two disagree on year (online-first vs issue), the Crossref `issued` year is used and the difference is noted in `notes`.
2. **DOI resolution**: the DOI resolves via the doi.org handle API. Papers without a DOI (e.g., NeurIPS, PMLR) must have a verified proceedings landing page in `url`.
3. **Abstract retrieved**: from OpenAlex, Crossref, Semantic Scholar or the publisher landing page. If no abstract can be retrieved, the paper is **deferred**, not guessed.
4. **Evidence-backed fields**: every `Yes` in a characteristic field has a matching evidence item (claim → short paraphrase) in `evidence` and in `selected_papers.md`.

Rules that are never relaxed:
- Never infer `smartphone` from "edge" or "mobile device" wording.
- Never infer `on_device` unless the paper says inference runs on the device.
- Never infer `resource_awareness` just because a model is lightweight or runs on an edge device.
- Never infer `multi_view` unless multiple views or camera angles are actually captured.
- Set `uncertainty` only under the definition in §7 (an ordinary softmax confidence value is not enough on its own).

These rules are summaries. The binding definitions for every characteristic field are in **§7 Literature Coding Definitions**.

Rejected and deferred candidates are listed with reasons at the end of `selected_papers.md`.

## 3. `papers.csv` schema

29 columns in this exact order (enforced by `src/literature/schema.py`):

| Field | Type | Description |
| :--- | :--- | :--- |
| `paper_id` | String (required) | Sequential ID `P001`, `P002`, … Never reused. |
| `title` | String (required) | Verified full title |
| `authors` | String (required) | Full author list, `;`-separated, as registered in Crossref/OpenAlex |
| `year` | Integer (required) | Version-of-record year (Crossref `issued`) |
| `venue` | String | Journal or proceedings name |
| `doi` | String | Bare DOI (e.g. `10.1109/...`); blank if the paper has no DOI |
| `url` | String | `https://doi.org/<doi>` or the verified proceedings page |
| `domain` | String | Primary domain (e.g. "3D-Print Inspection") |
| `application` | String | Specific target application |
| `dataset` | String | Dataset(s) as stated by the source |
| `model` | String | Model or algorithm as stated by the source |
| `hardware` | String | Hardware platform as stated by the source |
| `smartphone` … `latency_evaluation` | `Yes` / `No` / `Unknown` | 12 characteristic fields: `smartphone`, `edge_device`, `on_device`, `cloud`, `adaptive_inference`, `resource_awareness`, `energy_evaluation`, `thermal_evaluation`, `multi_view`, `uncertainty`, `anomaly_detection`, `latency_evaluation` |
| `accuracy_metrics` | String | Metric values exactly as reported by the source |
| `limitations` | String | Limitations stated by the authors |
| `future_work` | String | Future work stated by the authors |
| `evidence` | String | `[Verified; source: …]` followed by `claim -> evidence` items separated by ` \| ` |
| `notes` | String | Search group, extraction depth/date, caveats |

## 4. What `Unknown`, `No` and blank mean

- **`Unknown`** means the examined source (currently the abstract) does not establish the characteristic. It is **not** evidence of absence and must never be converted to `No` without a full-text check.
- **`No`** is used only when the source explicitly describes a contrary setup (e.g., the hardware is stated to be a Raspberry Pi, so `smartphone = No`), when a full-text reading confirms the characteristic is absent, or when the paper is a survey/review (§7.1).
- **Blank free-text fields** (`limitations`, `future_work`, `accuracy_metrics`) mean nothing was extracted at the current extraction depth, not that none exists.
- The validator also accepts legacy `true`/`false`/empty values (see `src/literature/schema.py`). New records should use `Yes`/`No`/`Unknown`.

Operational definitions of `Yes` / `No` / `Unknown` for each field are in §7.

Batch 1 extraction is **abstract-level**. Full-text review will upgrade `Unknown` fields and fill limitations and future work; each upgrade needs a new evidence item.

## 5. Duplicate handling

Before a paper is added:
1. Compare its normalised DOI (lower-case, `https://doi.org/` stripped) with existing rows.
2. Compare its normalised title (lower-case alphanumerics only) with existing rows.
3. If the same work has several DOIs (e.g., an arXiv preprint and a peer-reviewed version, or ACM reprints in SIG newsletters), keep **one** row for the version of record and record the other identifiers in `notes`.

`python scripts/manage_literature.py validate` reports duplicate IDs, DOIs and titles. `tests/test_literature_data.py` fails if the committed `papers.csv` has any.

## 6. Running the literature tools

```bash
# Validate papers.csv schema and check for duplicates
python scripts/manage_literature.py validate

# Summary statistics over the characteristic fields
python scripts/manage_literature.py stats

# Regenerate literature_matrix.csv
python scripts/manage_literature.py matrix

# Export literature matrix to LaTeX or Markdown
python scripts/manage_literature.py export --format latex --out research/tables/literature_table.tex

# Run the test suite (schema, validator and committed-data integrity)
python -m pytest -q
```

`python scripts/manage_literature.py gap` (and `all`, which calls it) regenerates `research/gap_analysis/gap_matrix.csv` and `gap_candidates.md`. Do not run them as part of routine literature updates; gap analysis is deferred until a human researcher decides the literature base is sufficient.

---

## 7. Literature Coding Definitions

_Version 1.0, 2026-10-03. Drafted by Claude Code._

These definitions are meant to let two coders who read the same paper reach the same value. Items marked **⚑** are coding choices that **require researcher/ChatGPT approval**. Borderline cases and worked examples are in [`coding_decisions.md`](coding_decisions.md).

The definitions apply to new records and to any later correction of existing records. Records coded before 2026-10-03 have not yet been re-checked against them.

### 7.1 General rules

**What is coded.** Code only the paper's **own contribution**: the system, method, dataset, benchmark or measurement that the authors present and evaluate in that paper. Text that only appears in the following places never sets a field to `Yes`:
- motivation or introduction;
- related work;
- discussion of other systems;
- limitations or future work.

**Evaluated configuration.** A field describes what the authors actually built, ran or measured. A capability that is claimed but not demonstrated (e.g. "can be deployed on mobile devices") is not enough for `Yes`.

**Values.** These apply to all 12 characteristic fields.

| Value | Use when |
| :-- | :-- |
| `Yes` | The examined source states, or directly reports, that the characteristic is part of the evaluated work, as defined for that field below. An evidence item is required (§7.2). |
| `No` | The examined source was read sufficiently and the characteristic is **explicitly absent or clearly not part of the work**. Two situations qualify: (a) the full text was read and the characteristic does not occur; (b) the examined source states a contrary setup. Example of (b): the abstract names a Raspberry Pi as the only hardware, so `smartphone = No`. |
| `Unknown` | The examined source does not establish either `Yes` or `No`. This is the default. Missing information is **never** coded `No`. |

**Abstract-level coding.** At abstract level:
- `Yes` requires an explicit statement in the abstract;
- `No` requires an explicitly contrary statement (case (b) above);
- everything else stays `Unknown`.

`notes` must state the extraction depth, either `Abstract-level extraction (date)` or `Full-text extraction (date)`.

**Paper type.** Record one paper-type tag in `notes`, as `Paper type: <type>.`, where `<type>` is one of:
- `system/method`: proposes and evaluates a method or system;
- `dataset/benchmark`: contributes data and evaluates existing methods on it;
- `measurement study`: measures existing systems, apps or hardware;
- `survey/review`: summarises other work and has no original evaluation of its own.

The CSV has no paper-type column, so `notes` is used.

**Survey and review papers.** ⚑
- A survey does not evaluate a system. All 12 characteristic fields are therefore coded **`No`** once the paper is confirmed to be a survey or review with no original experiments. The abstract states "survey" or "review" and reports no original experiments; full-text reading confirms it.
- If the survey also reports its own experiments, code only those experiments.
- Record the topics the survey covers in `notes` (`Survey topics: ...`) and in `domain`/`application`. Topics are **never** recorded in the characteristic fields.
- Benchmark and measurement studies (e.g. smartphone inference benchmarks) are **not** surveys. They are coded by what they measured.

### 7.2 Evidence requirements

Every `Yes` must have an evidence item in the `evidence` field. Every `No` that rests on case (b) should also have one.

**Acceptable evidence**, from the paper itself:
- an explicit statement in the methodology;
- an algorithm description;
- the experimental setup;
- a hardware or deployment description;
- evaluation results (text, tables, figures).

**Not acceptable on its own:**
- the title;
- motivation or related-work statements;
- future-work statements;
- the venue or the authors' affiliations;
- qualitative claims such as "real-time", "lightweight", "efficient" or "edge-friendly" without a reported measurement or a described mechanism;
- the coder's general knowledge of the method.

**External identification.** Identifying a named product is allowed and must be labelled as such in the evidence item. Example: a named phone model is a smartphone (`external identification: manufacturer product page`). ⚑

**Format.**
- The `evidence` field keeps its existing prefix, `[Verified; source: <source>]`. The prefix names where the text was read, e.g. `abstract via OpenAlex` or `full text`.
- The prefix is followed by items separated by ` | `.
- New or corrected items name the field they support and where the evidence is:

  `[<field>] <claim> -> <evidence paraphrase> (<location>)`

  where `<location>` is `abstract` or a full-text location such as `§4.2`, `Table 3` or `Fig. 5`.
- Evidence that comes only from the abstract must be identifiable as abstract evidence, through the source prefix or `(abstract)`.

### 7.3 Characteristic field definitions

#### `smartphone`
**Definition.** A smartphone is a functional part of the evaluated system, as the image-acquisition device, the inference/compute device, or both.
- **Yes:**
  - the paper states that a smartphone, or a named smartphone model, captures the inspection data in the proposed pipeline, or runs the processing;
  - an app running on a smartphone is part of the evaluated system;
  - the paper benchmarks smartphones as compute devices.
- **No:**
  - the evaluated hardware is explicitly a non-phone device (Raspberry Pi, Jetson, industrial camera + PC, MCU, tablet) with no smartphone role;
  - a smartphone appears **only** as the camera used to collect a dataset that is then processed offline, and the phone plays no part in the proposed system. Record "captured with smartphone" in `dataset` instead.
- **Unknown:** generic wording such as "mobile devices", "mobile platforms" or "edge devices" with no named phone.
- **Does not qualify:** a smartphone mentioned in motivation, as a possible future target, or as part of the environment.

#### `edge_device`
**Definition.** Model inference (the full model or a part of it) is executed and evaluated on resource-constrained hardware located at or near the data source. Examples: smartphone, single-board computer (Raspberry Pi), embedded GPU module (Jetson), USB/PCIe AI accelerator stick or kit attached to such a device (OAK-D, Coral), microcontroller, or embedded industrial controller.
- **Yes:** the paper runs inference on such hardware in at least one evaluated configuration.
- **No:**
  - inference runs only on workstation, desktop, server or cloud GPUs;
  - or the paper is a survey (§7.1).
- **Unknown:** the inference hardware is not stated, or the paper only says the model is "suitable for" edge deployment.
- **Does not qualify (edge infrastructure):** edge servers, multi-access edge computing (MEC) nodes, on-premise "edge cloud" platforms, gateways, or plant IT infrastructure that is not itself the resource-constrained device doing inference. Inference on a proximal **server** is recorded through `cloud`/`notes`, not as `edge_device`.

#### `on_device`
**Definition.** The **complete** inference of the evaluated model runs locally on the end device that captures the data (or on hardware physically attached to it, such as an AI kit on a single-board computer), in at least one evaluated configuration.
- **Yes:** the paper states the model is deployed and executed on the capturing/end device, e.g. "runs on the phone", "deployed on OAK-D for real-time detection", or on-device benchmark results.
- **No:**
  - all evaluated configurations send data off-device for inference (cloud-only or server-only);
  - or only part of the model ever runs locally (split computing). In that case record `partial on-device (split)` in `notes`. ⚑
- **Unknown:** the location of inference is not stated, e.g. "a smartphone app detects defects" without saying where inference runs.
- **Never inferred from:** a model being lightweight, the existence of an app, or models found inside app packages (static analysis) without execution.

#### `cloud`
**Definition.** Any part of the evaluated pipeline's inference or decision processing runs on remote datacenter/cloud servers.
- **Yes:** cloud-only processing **or** cloud-assisted processing (offloading, split/partitioned inference, hybrid fallback). Record the mode in `notes` as `cloud mode: cloud-only` or `cloud mode: cloud-assisted`.
- **No:** all evaluated inference runs locally or on a proximal edge server that the paper does not call cloud, and no cloud processing is described.
- **Unknown:** ambiguous terms such as "edge cloud" or "server" with no detail.
- **Does not qualify:** using the cloud only for training, data storage, dashboards or model distribution.

#### `adaptive_inference`
**Definition.** The **inference computation itself** changes at runtime, per input or per runtime condition. This means a change in which model, which layers or sub-network, or how much computation is executed, or how the model's computation is partitioned.

Qualifies:

| Mechanism | Qualifies? |
| :-- | :-- |
| Early exit / multi-exit networks | Yes |
| Dynamic model selection or model switching at runtime (e.g. choosing among model variants by input or condition) | Yes |
| Dynamic computation: layer/block skipping, dynamic width/depth, runtime sub-network selection, dynamic resolution | Yes |
| Input-dependent computation (spatial/temporal dynamic networks, cascades) | Yes |
| Runtime DNN partitioning/offloading decisions that change where model layers execute ⚑ | Yes |
| DVFS, CPU/GPU frequency scaling, core/processor allocation or task scheduling **with the model computation unchanged** | **No.** This is system-level adaptation; it is coded under `resource_awareness` if it is resource-driven |
| A model chosen once at design or deployment time and fixed afterwards | No |
| Changing physical process parameters (e.g. printer settings) based on predictions | No (adaptation of the process, not of inference) |

- **Yes:** the paper describes and evaluates one of the qualifying mechanisms.
- **No:**
  - the inference graph is static and any adaptation is system-level only;
  - or the paper is a survey (§7.1).
- **Unknown:** the abstract mentions "adaptation" without saying what adapts.

#### `resource_awareness`
**Definition.** The method makes a **decision that is driven by resources**. It takes explicit resource constraints or measured or predicted resource state as an input to a runtime or deployment-time decision. Resources include compute load, memory, battery or energy budget, temperature or thermal headroom, network bandwidth, and latency or service-level objectives.
- **Yes:** examples of qualifying decisions:
  - runtime adaptation to available resources;
  - scheduling or partitioning driven by bandwidth or load;
  - DVFS driven by thermal state;
  - selecting a configuration to meet an explicit device budget or service-level objective.
- **No:**
  - the method takes no resource-driven decision (the full text was read);
  - or the paper is a survey (§7.1).
- **Unknown:** the abstract-level case where resources are only measured or the model is only described as lightweight.
- **Does not qualify (resource measurement only):** reporting CPU/GPU utilisation, memory, model size, FLOPs, energy or latency, or designing a "lightweight" model, **without** using that information to make a decision. Measurements are captured by `energy_evaluation` and `latency_evaluation`, and by `notes` for memory and CPU.

#### `energy_evaluation`
**Definition.** The paper reports energy or power consumption of the evaluated inference system, either measured, or estimated with a stated energy or power model. Examples: J, Wh, W, mA, battery-drain %, battery life.
- **Yes:** energy or power results are reported for the paper's own system or measurements.
- **No:**
  - no energy or power results (the full text was read);
  - or the paper is a survey (§7.1).
- **Unknown:** energy is only mentioned as motivation at abstract level.
- **Does not qualify:** FLOPs, MACs, parameter count or model size used as proxies; statements that a method is "energy-efficient" without results.

#### `thermal_evaluation`
**Definition.** The paper measures, models or reports device temperature, thermal state, or thermal throttling of the evaluated system as part of its method or evaluation.
- **Yes:** temperature or throttling is measured or modelled, or used as an evaluation outcome. Examples: "maintains lower CPU/GPU temperature", "delays thermal throttling".
- **No:**
  - no thermal measurement or modelling (the full text was read);
  - or the paper is a survey (§7.1).
- **Unknown:** thermal issues are mentioned only as motivation.

#### `multi_view`
**Definition.** The inspected object or scene is imaged from **two or more distinct viewpoints**, meaning different camera poses relative to the object, and the views are used together in the inspection task (planning, fusion, or aggregated per-object decisions), or are released as a multi-view dataset.

| Situation | Qualifies? |
| :-- | :-- |
| Multiple camera angles / multiple images from different viewpoints of the same object | Yes |
| Multiple cameras at different poses | Yes |
| One camera moved (robot, hand-held) or object rotated/repositioned to obtain different viewpoints | Yes |
| Viewpoint/inspection planning that selects multiple camera poses | Yes |
| Repeated capture from the same viewpoint (re-shots, burst, different exposure or lighting at the same pose) | No |
| Temporal video frames from a fixed camera, or images at different print/process stages from the same pose | No |
| Video from a moving camera | Yes only if the paper treats distinct viewpoints as separate views; otherwise Unknown |
| Multi-modal capture from one pose (RGB + depth, RGB + thermal) | No (multi-modal, not multi-view) |
| "Multi-view" as a model-internal representation (projections of a point cloud, multi-view feature branches) without multiple physical camera views | No |

- **Unknown:** multiple images are mentioned without saying whether the viewpoints differ.

#### `uncertainty`
**Definition.** The paper **estimates, calibrates or evaluates predictive uncertainty**, or uses a **selective-prediction (reject-option) mechanism** that has a defined coverage/risk trade-off.

| Concept | Qualifies? |
| :-- | :-- |
| Raw softmax score, class probability or "confidence" reported or thresholded, without being estimated or evaluated as uncertainty | **No** on its own ⚑ |
| Confidence or entropy thresholds used for control decisions (early exit, recapture, human referral) without evaluating that score as uncertainty | **No** on its own ⚑; record `confidence-gated decision` in `notes` |
| Calibrated confidence (temperature scaling, calibration evaluated with ECE or reliability diagrams) | Yes |
| Predictive uncertainty from Bayesian methods (MC dropout, variational, Bayesian NNs), deep ensembles, Gaussian processes, evidential learning, conformal prediction | Yes |
| Epistemic and/or aleatoric uncertainty explicitly modelled | Yes |
| Predictive entropy or mutual information presented **and evaluated** as an uncertainty measure | Yes |
| Selective prediction / reject option with risk-coverage evaluation | Yes |
| Out-of-distribution detection used to flag unreliable predictions | Yes |

- **No:**
  - the full text was read and none of the qualifying items occur;
  - or the paper is a survey (§7.1).
- **Unknown:** the abstract mentions confidence or reliability without detail.

#### `anomaly_detection`
**Definition.** The inspection task is formulated as detecting deviations from normality. The model is trained or fitted mainly on normal (defect-free) data, or is unsupervised or self-supervised with respect to real defect labels. Examples: one-class, reconstruction-based, density- or feature-distance-based, or memory-bank methods. Methods trained on normal data with **synthetic** anomalies count, as do datasets built for this setting.
- **Yes:** the paper uses or evaluates such a formulation, or contributes a dataset or benchmark for it.
- **No:**
  - ordinary supervised defect classification, detection or segmentation trained on labelled defect classes, **even if the paper calls it "anomaly detection"**;
  - or the paper is a survey (§7.1).
- **Unknown:** the training regime is not stated.
- **Does not qualify:** OOD detection used for prediction reliability (coded under `uncertainty`); detecting anomalies in non-visual process signals is recorded in `domain`.

#### `latency_evaluation`
The schema has a single latency field. **No schema change is made.** The field is defined as follows, and the type of timing must be recorded in the evidence item as `latency type: inference | end-to-end | throughput`.

**Definition.** The paper reports a **measured timing result** of the evaluated inference pipeline on stated or identifiable hardware.

| Timing quantity | Qualifies? |
| :-- | :-- |
| Inference latency (time per forward pass / per input) | Yes (`inference`) |
| End-to-end latency (capture or request to result, including pre/post-processing or network transfer) | Yes (`end-to-end`) |
| Throughput: FPS, images/s, parts/min, or a measured relative FPS/speed change | Yes (`throughput`) ⚑ |
| Adaptation, reconfiguration or switching time **only** | **No**; record it in `notes` |
| Training time only | No |
| FLOPs, MACs, parameter count, model size | No (not timing) |
| "Real-time" or "fast" claimed without a reported measurement or comparison | Unknown (not Yes) |
| A comparative result ("faster than X") stated as an experimental finding, with no figures | Yes, flagged in evidence as `comparative, no figure` ⚑ |

- **No:**
  - the full text was read and no timing is reported;
  - or the paper is a survey (§7.1).

### 7.4 Key distinctions (summary)

| # | Distinction | Rule |
| :-- | :-- | :-- |
| 1 | Resource measurement vs resource-aware adaptation | Only a resource-driven **decision** sets `resource_awareness = Yes`. Measurement goes to `energy_evaluation`, `latency_evaluation` or `notes`. |
| 2 | Adaptive inference vs system-level adaptation (DVFS) | `adaptive_inference` requires the model computation to change. DVFS or scheduling with an unchanged model is `adaptive_inference = No`, and is `resource_awareness = Yes` if resource-driven. |
| 3 | Inference latency vs throughput/FPS vs adaptation time | Inference latency, end-to-end latency and throughput all qualify (record the type). Adaptation time alone does not. |
| 4 | Confidence score vs uncertainty estimation/calibration | A softmax confidence alone, used or thresholded, is not `uncertainty`. Calibration, a UQ method, an evaluated uncertainty measure, or selective prediction is. |
| 5 | Multiple images vs true multi-view | Only distinct camera poses of the same object, used jointly, count. Repeated shots, time series and multi-modal capture from one pose do not. |
| 6 | Smartphone as inspection device vs smartphone mentioned | The phone must capture or compute in the evaluated system. A phone used only to collect a dataset processed offline is `smartphone = No` (note it in `dataset`). |
| 7 | Edge infrastructure vs edge inference on a device | `edge_device` requires inference on resource-constrained device hardware. Edge servers, MEC and "edge cloud" do not count. |
| 8 | Cloud-assisted vs cloud-only | Both are `cloud = Yes`. Record the mode in `notes`. Cloud-only implies `on_device = No`. |
| 9 | Anomaly detection vs supervised defect detection | Training on normal data (± synthetic anomalies) or unsupervised with respect to defect labels counts. Supervised defect classes do not, whatever the paper's wording. |
| 10 | Survey/review vs evaluated system | Surveys are coded `No` for all 12 fields. Their topics go in `notes`/`domain`/`application`. |

### 7.5 Consistency rules

- `smartphone = Yes` and `on_device = Yes` ⇒ `edge_device = Yes`.
- `on_device = Yes` ⇒ `edge_device = Yes`, except when the end device is not resource-constrained (e.g. a workstation directly attached to the camera). In that case explain it in `notes`.
- Cloud-only processing (`cloud mode: cloud-only`) ⇒ `on_device = No`.
- `adaptive_inference = Yes` does not imply `resource_awareness = Yes`: input-dependent early exit can be resource-agnostic. Code each field separately.
- A `survey/review` paper type ⇒ all 12 characteristic fields are `No`.

### 7.6 Free-text fields

| Field | How to record |
| :-- | :-- |
| `dataset` | Dataset names exactly as the source states them, separated by `; `. For custom data, give a short description (object, defect types, size if stated, acquisition device), illustrative example: `Custom: <N> images of FDM parts, <k> defect classes (captured with smartphone)`. If the abstract does not state it, write `Not stated in abstract`. `Unknown` is reserved for characteristic fields. |
| `model` | The model or algorithm as named by the source (e.g. `Improved YOLOv8 (group-convolution head)`), separated by `; ` if several. Do not name a backbone the paper does not state. |
| `hardware` | Prefix each component with its role, using only the roles the source states: `Inference: ...; Acquisition: ...; Training: ...`. Illustrative example: `Inference: OAK-D on Raspberry Pi; Acquisition: camera on a moving vehicle`. Use device model names as stated. If no hardware is stated, write `Not stated in abstract` (or `Not stated` after full-text reading). |
| `accuracy_metrics` | Quantitative **task-performance** results exactly as reported: metric name, value with the source's units and precision, and the dataset or condition, separated by `; `. Never recompute, round or convert values. Efficiency results (latency, FPS, energy, GFLOPs, model size) may also be recorded here **only** with the prefix `Efficiency:` (e.g. `Efficiency: 31.76 FPS on OAK-D`), because the schema has no separate efficiency column ⚑. Relative results must stay relative (`+18.1% FPS vs YOLOv8`). Leave the field blank if no figures were extracted. |
| `limitations` | Limitations of **this paper's own** method or study, stated by the authors. A limitation of the field in general must be marked `(field-level)`. Each entry needs an evidence item. |
| `future_work` | Future work stated by the authors, with an evidence item. Do not record the coder's suggestions. |

### 7.7 Changing an existing coding

- A coding change in `papers.csv` must:
  - cite the definition subsection that applies (e.g. `§7.3 latency_evaluation`);
  - update the evidence item;
  - append a dated note to `notes`, such as `Recoded latency_evaluation Yes→Unknown under README §7 v1.0 (2026-10-xx)`.
- Upgrading `Unknown` to `Yes` or `No` after full-text reading needs a full-text evidence item.
- Recoding is done as a separate, logged task (`docs/agent_sync/CHANGELOG.md`), never silently.
