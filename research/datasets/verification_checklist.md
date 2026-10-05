# Pre-Implementation Verification Checklist — GC-03

_Step 10B, 2026-10-05, Claude Code._

Every item must be completed, with evidence recorded, before implementation or data collection begins. **No item is complete.** Acceptance criteria that need numbers are **TO BE PRE-REGISTERED**. An item becomes VERIFIED only when the stated evidence is stored in the repository (or referenced) and reviewed by the researcher.

| ID | Area | Check | Evidence required | Blocks | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| V-01 | Dataset access verification | Real-IAD can be obtained by the project (host, request or agreement process completed). | Record of the access route and date; no data committed to git. | Stage 1 | REQUIRES_VERIFICATION |
| V-02 | Dataset access verification | Fallback (MANTA) and sanity set (VisA) access routes. | As V-01. | Fallbacks | REQUIRES_VERIFICATION |
| V-03 | Dataset license verification | Real-IAD **data** terms read in full and compatible with research use and publication of derived results. | Copy or link of the terms; researcher sign-off. The code-repository `LICENSE` is not sufficient. | Stage 1 | REQUIRES_VERIFICATION |
| V-04 | Dataset license verification | Terms for any other dataset used (VisA CC BY 4.0 as stated; MVTec AD and KolektorSDD2 non-commercial as stated). | As V-03. | Any use | REQUIRES_VERIFICATION |
| V-05 | Dataset content | Per-sample linkage of the five Real-IAD views, image-level labels and annotation format. | Inspection report on a sample after access is granted. | A2 proxy, item-level labels | REQUIRES_VERIFICATION |
| V-06 | Smartphone availability | Which physical device(s) the researcher has; model, SoC, RAM, battery health. | Device inventory entry. | Everything on-device | REQUIRES_VERIFICATION |
| V-07 | Android version | API level ≥ 29 (thermal status); ≥ 30 preferred (thermal headroom). | `Build.VERSION.SDK_INT` recorded. | R-state inputs | REQUIRES_VERIFICATION |
| V-08 | Telemetry API verification | Battery level, voltage, current (`CURRENT_NOW` sign/units/refresh), charge and energy counters; RAM; process CPU time; power-save mode. | Short log from a probe build, with update intervals observed. | Telemetry layer A | REQUIRES_VERIFICATION |
| V-09 | Telemetry API verification | Device-wide CPU utilisation and frequency, GPU counters via ADB/Perfetto. | Perfetto trace showing each counter, or a recorded "unavailable". | Manipulation checks | REQUIRES_VERIFICATION |
| V-10 | Thermal API verification | `getCurrentThermalStatus`, `getThermalHeadroom`, battery temperature, accessible thermal zones and their mapping. | Probe log plus thermal-zone map for the device. | Thermal DV, R-state | REQUIRES_VERIFICATION |
| V-11 | Energy measurement verification | External reference: power analyzer with battery bypass, or a validated pass-through. Agreement with software counters. | Validation report (bias, limits of agreement, usable interval). Criteria TO BE PRE-REGISTERED. | Energy DV (H3, H5) | REQUIRES_VERIFICATION (EXTERNAL-METER VALIDATION REQUIRED) |
| V-12 | Energy measurement verification | External surface probe and ambient thermometer available and synchronised. | Instrument list; synchronisation test. | Thermal DV | REQUIRES_VERIFICATION |
| V-13 | Accelerator verification | GPU (and NPU, if used) backend executes each configuration; delegation coverage and fallback detectable. | Per-configuration delegation report. | S4, configuration identity | REQUIRES_VERIFICATION |
| V-14 | Model deployment verification | All C1–C4 convert to the single chosen runtime and run offline on the device. | Conversion log; on-device smoke run (no benchmark claims). | Ladder | REQUIRES_VERIFICATION |
| V-15 | Model deployment verification | Cost ordering of C1–C4 at R0 (S3) and accuracy ordering on validation (S6). | E1 pilot results, stored as results only after the protocol is registered. | Ladder | REQUIRES EMPIRICAL BENCHMARKING |
| V-16 | Confidence-output verification | Each exported model outputs class probabilities; temperature scaling can be applied on device; calibration split defined by item. | Output-signature check; calibration-split manifest. | Gating (A0–A4) | REQUIRES_VERIFICATION |
| V-17 | Multi-view/recapture verification | Real-IAD views usable as the A2 proxy (V-05). | As V-05. | A2 (Stage 1) | REQUIRES_VERIFICATION |
| V-18 | Multi-view/recapture verification | Custom capture rig (jig/turntable, lighting, item IDs) and Camera2 manual control on the device. | Rig description; Camera2 capability dump. | A1, A2 (Stage 2) | REQUIRES_VERIFICATION |
| V-19 | Pressure protocol | R0–R3 can be induced reproducibly (load, thermal soak, battery/power-saver state) and confirmed by telemetry. | Pilot telemetry traces. Thresholds TO BE CALIBRATED DURING EXPERIMENT DESIGN. | All E1/E2 | REQUIRES_VERIFICATION |
| V-20 | Timestamp synchronisation | Shared sync events align phone, host and external-meter streams. | Sync test with residual offset reported. | Energy per item | REQUIRES_VERIFICATION |
