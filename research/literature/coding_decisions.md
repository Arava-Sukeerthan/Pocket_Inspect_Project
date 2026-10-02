# Literature Coding Decisions

_Version 1.1, 2026-10-03. v1.0 was drafted by Claude Code (Step 8.1). v1.1 adds the approval record (Step 8.3). Companion to [`README.md` §7 Literature Coding Definitions](README.md#7-literature-coding-definitions)._

This file records the borderline coding decisions behind the definitions and shows how they apply to papers already in the corpus.

> **Status (v1.1).**
> - The eight ⚑ questions from v1.0 were **decided by the researcher/ChatGPT on 2026-10-03** (§0).
> - The approved rules were applied to `papers.csv` in Step 8.3. The changes actually made are in [`recoding_report.md`](recoding_report.md), which **supersedes** the provisional table in §2.
> - The v1.0 text of each decision below is kept unchanged for traceability. An **Approval outcome** line is added under each ⚑ decision.
> - All effects are judged at **abstract level**, using the abstracts retrieved during the 2026-10-02 audit ([`audit_report.md`](audit_report.md)).
> - Nothing here is a research-gap or novelty claim.

---

## 0. Approval record (2026-10-03)

| Decision | v1.0 question | Approved outcome | Changed from v1.0 proposal? |
| :-- | :-- | :-- | :-- |
| 1 | CD-01 surveys | All characteristic fields `No`; topics in `notes`/`domain`/`application` | No |
| 2 | CD-02 throughput | Throughput/FPS qualifies; evidence must name the timing type (inference latency / end-to-end latency / throughput/FPS) | No |
| 3 | CD-04 comparative speed claims | Qualitative claims without a measured timing value are **`Unknown`** | **Yes**: v1.0 proposed `Yes` |
| 4 | CD-06 partitioning | Only **dynamic** runtime partitioning is `adaptive_inference = Yes`; static partitioning is `No`; DVFS/scheduling is `No` (`resource_awareness = Yes` if resource-driven) | Refined: static case added |
| 5 | CD-08 confidence gating | New categorical field **`confidence_gating`**; `uncertainty` reserved for formal uncertainty | **Yes**: schema change instead of a `notes` tag |
| 6 | CD-10 named phone models | Allowed when the paper names the model **and** an authoritative external source confirms it; the source is recorded in `notes`/evidence | Refined: authoritative source required |
| 7 | CD-13 split inference | Split device/edge/cloud inference gives `on_device = No`, with the split recorded in `notes` | No |
| 8 | CD-16 efficiency figures | New free-text field **`efficiency_metrics`**; `accuracy_metrics` keeps task metrics only | **Yes**: schema change instead of a prefix |

The schema grew from 29 to 31 columns (`confidence_gating` after `uncertainty`; `efficiency_metrics` after `accuracy_metrics`).

**Application notes (Claude Code, Step 8.3).** These are choices made while applying the decisions:
- **Surveys and `confidence_gating`.** Decision 1 named "the 12 characteristic fields" because there were 12 at the time. Surveys are also coded `No` for the new 13th field, `confidence_gating`, under the same reasoning.
- **Measured relative timing values count as measured** under Decision 3. Examples: "+18.1% FPS" (P018), "3.1x lower end-to-end latency" (P028), "2.0x frame processing rate" (P029).
- **A named timing metric without a value in the abstract** stays `Yes`. P004 names "real-time throughput" as a reported benchmark metric. Its `efficiency_metrics` field is left blank, and `notes` flags the values for full-text verification.
- **`adaptive_inference` is not set to `No` for DVFS-only papers at abstract level.** P031's `adaptive_inference` is `Unknown` rather than `No`, because the abstract alone cannot establish that the model computation never changes.

---

## 1. Decisions

Each decision gives the question, the decision taken, the reason, the alternatives considered, and the papers it affects.

### CD-01 Survey and review papers ⚑
- **Question:** how should a survey that *discusses* adaptive inference, uncertainty and so on be coded?
- **Decision:** all 12 characteristic fields are `No`. Topics go in `notes` (`Survey topics: ...`) and in `domain`/`application`. The `Paper type: survey/review` tag goes in `notes`.
- **Rationale:** the characteristic fields describe an evaluated system, and a survey evaluates none. Coding by topic would let a survey count as evidence that a system was evaluated, which is exactly what the audit flagged.
- **Alternatives considered:**
  - `Unknown`: rejected, because the absence is not uncertain. The paper type rules out an evaluated system.
  - Keep topic coding: rejected for the reason above.
  - Add a `paper_type` column: this is a schema change. It is reported in §3 and not implemented.
- **Corpus:** P010, P024, P026, P035, P036, P052.
- **Approval outcome (Decision 1):** approved as proposed. Applied to all 13 characteristic fields, including the new `confidence_gating`.

### CD-02 Throughput counts as latency evaluation ⚑
- **Question:** should FPS or throughput count toward `latency_evaluation`?
- **Decision:** yes. Inference latency, end-to-end latency and throughput all qualify. The evidence item must record `latency type: inference | end-to-end | throughput`.
- **Rationale:**
  - The schema has one timing field.
  - Throughput on stated hardware is a measured timing result of the inference pipeline.
  - Recording the type keeps the three quantities separable without a schema change.
- **Alternative considered:** inference and end-to-end latency only. Rejected because papers that report only FPS would then have no timing field. Separate columns would be a schema change (§3).
- **Corpus:** P007 (31.76 FPS), P018 (+18.1% FPS), P039 (> 400 pcs/min): all stay `Yes`, with type `throughput`.
- **Approval outcome (Decision 2):** approved. The evidence labels are `latency type: inference latency`, `latency type: end-to-end latency` and `latency type: throughput/FPS`; a test checks that every `latency_evaluation = Yes` row has one.

### CD-03 Adaptation time is not latency evaluation
- **Decision:** adaptation, reconfiguration or switching time **alone** does not set `latency_evaluation = Yes`. It is recorded in `notes`.
- **Rationale:** it measures how fast the system changes configuration, not how fast it infers.
- **Corpus:** P034. The abstract reports only adaptation time (< 40 µs), so the provisional effect is `Yes → Unknown` until the full text is checked for inference timing.

### CD-04 Comparative speed claims without figures ⚑
- **Decision:** an experimental finding such as "faster than X", or "evaluations demonstrate low latency", is enough for `Yes`. The evidence item is flagged `comparative, no figure`. A design claim with no reported result ("real-time capable") stays `Unknown`.
- **Corpus:**
  - P002 ("outperforms ... in processing speed") stays `Yes`.
  - P027 ("experimental evaluations demonstrate ... low-latency") stays `Yes`.
  - P003 ("evaluate the performance") and P006 ("performance across devices") give no timing wording, so the provisional effect is `Yes → Unknown`.
- **Approval outcome (Decision 3): not approved as proposed.** Qualitative claims without a measured timing value are coded `Unknown` with `Requires full-text verification`. Applied: P002, P025, P027, P031 and P032 move `Yes → Unknown`, in addition to P003 and P006.

### CD-05 DVFS is not adaptive inference
- **Decision:** CPU/GPU frequency scaling, processor allocation or task scheduling that leaves the model computation unchanged is **system-level adaptation**:
  - `adaptive_inference = No`;
  - `resource_awareness = Yes` if the adaptation is driven by resources.
- **Rationale:** the prompt asked that DVFS not be counted automatically. Keeping it separate lets the corpus distinguish model-level from system-level adaptation.
- **Corpus:**
  - P031 (LOTUS): the abstract describes only joint CPU/GPU frequency scaling. Provisional `adaptive_inference Yes → Unknown`, and `No` once the full text confirms no model-level adaptation. `resource_awareness` and `thermal_evaluation` stay `Yes`.
  - P032 (Phoenix): processor allocation (system-level) **and** multi-exit networks (model-level), so `adaptive_inference` stays `Yes` through the multi-exit mechanism.

### CD-06 Runtime partitioning counts as adaptive inference ⚑
- **Decision:** a runtime decision that changes where a model's layers execute (device, edge or cloud partitioning) counts as `adaptive_inference`.
- **Rationale:** the model's execution plan changes per runtime condition, unlike DVFS, where the same computation runs faster or slower.
- **Alternative considered:** count only changes to model structure (early exit, sub-network selection). Under that alternative P028 would become `Unknown`/`No`. P027 would stay `Yes` because it also uses early exit.
- **Corpus:** P027 and P028 stay `Yes`.
- **Approval outcome (Decision 4):** approved for **dynamic** partitioning only. Static partitioning is `No`. Both P027 (bandwidth-driven change-point detection) and P028 (adapts to network and server load) describe dynamic partitioning in their abstracts, so both stay `Yes`. DVFS-only (P031) is handled under CD-05.

### CD-07 Resource measurement is not resource awareness
- **Decision:** `resource_awareness = Yes` requires a decision driven by resources. Measuring CPU, GPU, memory, energy or latency only, or designing a "lightweight" model, does not qualify.
- **Corpus:**
  - P004 benchmarks CPU/GPU consumption, and the abstract describes no resource-driven decision. Provisional effect: `Yes → Unknown`.
  - P027 (bandwidth-driven), P029, P030, P031, P032, P033 and P034 stay `Yes`.

### CD-08 Confidence-gated decisions are not uncertainty ⚑
- **Decision:** thresholding a softmax confidence or entropy for a control decision (early exit, recapture, human referral) does **not** set `uncertainty = Yes` unless the paper estimates, calibrates or evaluates that score as uncertainty. Such papers get `confidence-gated decision` in `notes`.
- **Rationale:** the prompt asked that ordinary softmax confidence not be equated with formal uncertainty.
- **Caveat for the researcher:** confidence-gated recapture or referral is directly relevant to PocketInspect's acquisition loop. Under this decision it is visible only through `notes`. A dedicated field would be a schema change (§3).
- **Corpus:**
  - P025 (BranchyNet) exits on high confidence; the abstract does not say the score is evaluated as uncertainty. Provisional effect: `Yes → Unknown`, then `No` if the full text confirms.
  - P045 and P046 (selective prediction with risk-coverage evaluation) stay `Yes`.
  - P048 and P051 (OOD detection or ensembles) stay `Yes`.
  - P049, P053 and P054 (MC dropout or ensembles) stay `Yes`.
- **Approval outcome (Decision 5): superseded by a new field.** `confidence_gating` (Yes/No/Unknown) records confidence-triggered actions; `uncertainty` stays formal.
  - Applied: P025 `uncertainty Yes → Unknown`, `confidence_gating = Yes`.
  - P045 and P046: `confidence_gating = Unknown`. The P045 abstract does not name the score that drives rejection. P046 uses a learned selection head, which the paper contrasts with confidence thresholds. Researcher review is noted in `notes`.

### CD-09 True multi-view
- **Decision:** two or more distinct camera poses of the same object, used together, count as `multi_view`. These do not count:
  - repeated shots from one pose;
  - temporal frames or process stages from a fixed camera;
  - multi-modal capture from one pose;
  - "multi-view" used as a model-internal representation.
- **Corpus:**
  - P037, P038 (multi-view datasets), P039 (four imaging views), P041, P042 (viewpoint planning) and P043 (multi-view RGB) stay `Yes`.
  - P017 (images at several print stages) stays `Unknown`. The abstract does not say whether the pose changes; if it is the same pose, `No`.
  - P040 ("multi-view" is a point-cloud model representation) stays `Unknown` at abstract level; `No` if the full text shows no multiple physical views.
  - P044 (one global visual view plus tactile) stays `Unknown`.

### CD-10 Named phone models and generic "mobile devices" ⚑
- **Decision:**
  - A named product that is a smartphone (identified externally, e.g. from the manufacturer's product page) gives `smartphone = Yes`. The evidence item must be labelled `external identification`.
  - Generic "mobile devices" or "mobile platforms" give `smartphone = Unknown`.
- **Corpus:**
  - P031 ("Mi 11 Lite mobile platform") stays `Yes`, but its evidence needs the `external identification` label.
  - P011, P029, P032 and P033 stay `Unknown`.
- **Approval outcome (Decision 6):** approved, with an authoritative external source required.
  - Applied to P031. Xiaomi's official specifications page for the Mi 11 Lite lists dual nano-SIM, 4G/3G/2G cellular support and Android 11. The URL and access date are recorded in `notes`.
  - The page does not use the word "smartphone". The classification rests on the cellular phone specifications.

### CD-11 Smartphone used only for dataset collection
- **Decision:** if a phone only captures a dataset that is processed offline and has no role in the proposed system, `smartphone = No`, and "captured with smartphone" goes in `dataset`.
- **Corpus:** no current record is affected. The rule is set in advance for future searches.

### CD-12 Edge infrastructure vs edge device
- **Decision:** `edge_device` requires inference on resource-constrained device hardware. Edge servers, MEC, "edge cloud" platforms and plant IT do not count. "Edge cloud" is also too ambiguous to set `cloud = Yes` without detail.
- **Corpus:** P013 ("Edge Cloud Computing" in plant IT). Provisional effect: `edge_device Yes → Unknown` and `cloud Yes → Unknown`, pending the full-text check already recommended by the audit (class D).

### CD-13 What counts as on-device ⚑
- **Decision:**
  - `on_device = Yes` requires the **complete** model inference to run on the end device in at least one evaluated configuration.
  - Configurations that only ever run part of the model locally (split computing) get `No`, plus `partial on-device (split)` in `notes`.
  - Models found by static analysis of app packages, never executed, do not establish on-device inference.
- **Alternative considered:** count partial execution as `Yes`. Rejected because it would hide the difference between local and offloaded inference, which matters for PocketInspect's deployment.
- **Corpus:**
  - P005 (static analysis of app packages). Provisional effect: `Yes → Unknown`.
  - P027 and P028 stay `Unknown`, because the abstracts do not say whether an all-local configuration was evaluated.
- **Approval outcome (Decision 7):** approved. Split inference gives `on_device = No`.
  - Applied: P027 `on_device Unknown → No` (device + edge) and P028 `on_device Unknown → No` (device + cloud). `notes` records the split.
  - P028 also gets `edge_device Unknown → Yes`, because the device part runs on a mobile development platform.

### CD-14 Anomaly detection is decided by training regime, not wording
- **Decision:** `anomaly_detection = Yes` requires training on normal data (synthetic anomalies are allowed), or being unsupervised with respect to defect labels. Supervised defect classification is `No`, even when the paper calls it anomaly detection.
- **Corpus:**
  - P009, P037, P038, P043, P047 (synthetic defects on defect-free images), P050 and P040 (unsupervised detection step) stay `Yes`.
  - P020 uses the phrase "anomaly detection" but describes supervised classifiers; it stays `Unknown` until the training regime is confirmed.

### CD-15 Consistency: on-device inference on a phone or edge hardware implies edge_device
- **Decision:** README §7.5 makes `edge_device = Yes` follow from `on_device = Yes` on resource-constrained hardware.
- **Corpus:** P003, P004, P006, P029, P032 and P033 have `on_device = Yes` on smartphones or mobile devices but `edge_device = Unknown`. Provisional effect: `edge_device Unknown → Yes`.

### CD-16 Efficiency figures in `accuracy_metrics` ⚑
- **Decision:** `accuracy_metrics` holds task-performance metrics. Efficiency figures may stay in the field only with an `Efficiency:` prefix.
- **Alternative considered:** a separate `efficiency_metrics` column, which is a schema change (§3).
- **Corpus:** P007, P018, P028, P029 and P039 contain FPS, GFLOPs, latency, energy or throughput values without the prefix. Provisional effect: add the prefix and leave the values unchanged.
- **Approval outcome (Decision 8): superseded by a new field.** Efficiency values for P007, P018, P028, P029 and P039 were moved into `efficiency_metrics`, wording unchanged. P028's datacenter throughput figure was added from the verified reprint abstract. P034's adaptation time was recorded there too. The `Efficiency:` prefix is not used.

### CD-17 Hardware role prefixes
- **Decision:** the `hardware` field uses role prefixes (`Inference:`, `Acquisition:`, `Training:`).
- **Corpus:** P022 ("Raspberry Pi-based data acquisition") would become `Acquisition: Raspberry Pi-based system; Inference: Not stated in abstract`. The other rows would be reformatted in the same correction task.

---

## 2. Provisional effect on current records (v1.0; superseded)

> **Superseded by [`recoding_report.md`](recoding_report.md)** (Step 8.3). The table is kept as the v1.0 record. The applied changes differ where Decisions 3, 4, 5 and 7 changed or refined the proposal:
> - more `latency_evaluation` values became `Unknown`;
> - P025 got `confidence_gating = Yes`;
> - P027 and P028 got `on_device = No`;
> - P028 got `edge_device = Yes`;
> - surveys are coded across 13 fields.

These are abstract-level changes that a correction task would make **after** the definitions are approved.

| Paper | Field | Current | Provisional | Decision |
| :-- | :-- | :-- | :-- | :-- |
| P003 | latency_evaluation | Yes | Unknown | CD-04 |
| P003 | edge_device | Unknown | Yes | CD-15 |
| P004 | resource_awareness | Yes | Unknown | CD-07 |
| P004 | edge_device | Unknown | Yes | CD-15 |
| P005 | on_device | Yes | Unknown | CD-13 |
| P006 | latency_evaluation | Yes | Unknown | CD-04 |
| P006 | edge_device | Unknown | Yes | CD-15 |
| P013 | edge_device | Yes | Unknown | CD-12 |
| P013 | cloud | Yes | Unknown | CD-12 |
| P025 | uncertainty | Yes | Unknown | CD-08 |
| P029 | edge_device | Unknown | Yes | CD-15 |
| P031 | adaptive_inference | Yes | Unknown | CD-05 |
| P032 | edge_device | Unknown | Yes | CD-15 |
| P033 | edge_device | Unknown | Yes | CD-15 |
| P034 | latency_evaluation | Yes | Unknown | CD-03 |
| P026, P035 | adaptive_inference | Yes | No | CD-01 |
| P052 | uncertainty | Yes | No | CD-01 |
| P010, P024, P026, P035, P036, P052 | all other characteristic fields | Unknown | No | CD-01 |

**Totals** (values, not papers):
- 9 values go from `Yes` to `Unknown`;
- 6 values go from `Unknown` to `Yes`;
- 3 values go from `Yes` to `No` (surveys);
- 69 values go from `Unknown` to `No` (6 surveys × 12 fields, minus the 3 above).

Formatting-only changes (CD-10 evidence label, CD-16, CD-17) are not counted.

---

## 3. Schema changes considered

> **Update (v1.1):** `confidence_gating` and `efficiency_metrics` **were implemented** in Step 8.3 (Decisions 5 and 8). The other rows remain unimplemented.

The definitions work with the current 29-column schema. No schema change is required. The following optional extensions would make some distinctions machine-readable. Each one needs a researcher decision and a change to `src/literature/schema.py`, the validator and the tests.

| Possible column | Would replace | Benefit |
| :-- | :-- | :-- |
| `paper_type` | `Paper type:` tag in `notes` | Filter surveys out without parsing `notes` |
| `latency_type` (or separate `inference_latency`, `throughput` columns) | `latency type:` tag in evidence | Separate timing quantities directly |
| `efficiency_metrics` | `Efficiency:` prefix in `accuracy_metrics` | Keep task metrics and efficiency metrics apart |
| `confidence_gating` | `confidence-gated decision` in `notes` | Track confidence-driven recapture or referral, which is relevant to PocketInspect |
| `system_adaptation` | Notes on DVFS / scheduling | Count system-level adaptation separately from `adaptive_inference` |

---

## 4. Questions for researcher/ChatGPT approval

> **Answered 2026-10-03.** See §0. Two questions raised in Antigravity's Step 8.2 review remain open:
> - Does design-time, constraint-aware optimisation (e.g. NAS or compression under an explicit device budget) set `resource_awareness = Yes`?
> - Where do tablets and industrial PCs with desktop-grade GPUs fall for `smartphone` and `edge_device`?
>
> No current record depends on either answer.

1. **CD-01:** code surveys `No` across all characteristic fields (vs `Unknown`, or a `paper_type` column)?
2. **CD-02:** count throughput/FPS toward `latency_evaluation`?
3. **CD-04:** accept comparative speed findings without figures as `Yes`?
4. **CD-06:** count runtime device/edge/cloud partitioning as `adaptive_inference`?
5. **CD-08:** exclude confidence-gated decisions from `uncertainty`, and should a `confidence_gating` field be added?
6. **CD-10:** allow external identification of named phone models?
7. **CD-13:** code split-only execution as `on_device = No`?
8. **CD-16:** keep efficiency figures in `accuracy_metrics` with a prefix, or add an `efficiency_metrics` column?
9. Approve applying the provisional changes in §2 as a separate, logged correction task.
