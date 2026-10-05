# Step 9.8 Targeted Counterexample Search Log

**Purpose.** Each search below was designed to **disprove** one of the Step 9.7 candidate gaps (GC-01, GC-02 and GC-03). It looks for published work that would make the candidate wrong or narrower. A search that finds nothing is not evidence that nothing exists.

**Boundary.** None of the papers found here was added to [`research/literature/papers.csv`](../literature/papers.csv). That file is frozen at 54 records, SHA-256 `c8fac51d5d80abd25f09816eace1ab840c498af76ade913ce7f7f1ecdc7da521`. Every paper assessed is recorded in [`counterexample_candidates.csv`](counterexample_candidates.csv).

## Note on the Step 9.8 methodology correction

These searches were designed and run against the **Step 9.7 wording** of GC-01, GC-02 and GC-03. The researcher-approved correction then narrowed the wording, confirmed four partial counterexamples, and formalised Decisions A–C (see [`candidate_gap_evaluation.md`](candidate_gap_evaluation.md) §3.4). No new search was run for the correction, and none of the entries below has been altered. Classifications given in the entries refer to the coding at search time, with one exception: `resource_awareness` for 2608.14727, TinyGLASS, 2309.00022 and 2505.07119 was later recoded under Decision A in `counterexample_candidates.csv`.

## Conventions

- **Date.** All searches ran on 2026-10-05.
- **Results returned.** The exact number of result links that the tool returned for the query. These counts were taken from the raw tool output.
- **Relevant results inspected.** How many of those results were plausibly relevant to the candidate and were examined beyond the title (snippet, abstract or full text). Off-topic results are not counted, e.g.:
  - consumer how-to pages;
  - product listings;
  - patents;
  - medical or activity-recognition papers.
- **Search engine.**
  - "WebSearch" is the web search tool available in this environment. It is US-only and returns about 10 links per query, with no pagination.
  - "alphaXiv discover" is the alphaXiv paper-discovery tool, which covers arXiv only.
- **Verification channels.**
  - Full text was read through the alphaXiv PDF/page reader (arXiv papers and some web pages) and the PubMed full-text tool (PMC articles).
  - Direct page fetches (WebFetch) were blocked by the network egress proxy for:
    - ombrulla.com;
    - ncbi.nlm.nih.gov;
    - frontiersin.org;
    - dl.acm.org;
    - doi.org.
  - The MDPI page for Electronics 15(17):3915 returned only an interstitial.
- **Self-reference.** Two queries returned this project's own GitHub repository. It was excluded.

## Limitations common to every search

- **Retrieval.**
  - One results page per query (about 10 links). Ranking is engine-specific and not reproducible.
  - No Scopus, Web of Science, IEEE Xplore or ACM Digital Library search was possible.
  - Publisher pages were mostly unreachable, so many hits could be judged only by title or snippet.
- **Search-engine summaries.** These were **not** used as evidence. One summary attributed a latency figure ("1.33×–3.93×") that appears in none of the papers that were checked.
- **Systematic false positives.** These were recorded but not treated as counterexamples:
  - "smartphone defect detection" papers where the phone is the inspected product;
  - thermography, where thermal imaging is the inspection modality, not a device thermal evaluation;
  - "energy-based" detection methods;
  - grey literature (vendor pages, blogs).
- **Coverage gaps.** Queries were English-only. Non-English and very recent (unindexed) work may be missed.

---

## GC-01: runtime resource-aware/adaptive inference in smartphone visual inspection

### S01

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `smartphone visual inspection adaptive inference` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 4: MSAdaNet (snippet); Smartphone screen surface defect detection, Sci. Rep. (snippet); PMC12074420 (full text); arXiv 2608.30997 (abstract) |
| Strongest relevant papers | PMC12074420 (smartphone-cluster inference with energy measurements; not inspection) |
| Potential counterexamples | None |
| Unresolved items | "Adaptive explainable artificial intelligence for visual defect inspection" (ScienceDirect S1877050924002977): title only; "adaptive" appears to refer to the explanations, not the inference computation; not verified |
| Search limitations | Two results were smartphone-as-product screen inspection; the medical and odometry hits were off-topic |

### S02

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `mobile visual inspection resource-aware inference` |
| Database / engine | WebSearch |
| Results returned | 9 (one was this project's GitHub repository; excluded) |
| Relevant results inspected | 4: NestDNN (= P029, already in the corpus); CARIn (= P033, already in the corpus); Ombrulla article (full page); Corun, PMC11487435 (full text) |
| Strongest relevant papers | P029 and P033: runtime resource-aware adaptation on smartphones, but outside visual inspection (already known from Step 9.7) |
| Potential counterexamples | None new |
| Unresolved items | "Automated Surface Quality Control via Deep Visual …" (iieta.org PDF): title only, not opened |
| Search limitations | The Ombrulla page needed the alphaXiv reader because direct access was blocked; CloudEye (mobile video analytics) was judged off-topic from its title |

### S03

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `smartphone manufacturing defect detection adaptive inference` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 4 distinct papers at snippet level: Sci. Rep. screen-defect paper; MSAdaNet; CE-SGNet (PMC11175082); "Combining AI and deep learning to develop a mobile phone screen defect detection system" (ScienceDirect/SSRN) |
| Strongest relevant papers | None relevant: all are inspections *of* phones |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | The query wording attracts phone-as-product papers. "Adaptive" in these titles means multi-scale feature design, not runtime adaptation. |

### S04

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `mobile edge inspection dynamic model selection` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: Ombrulla article; "Towards Autonomous Mobile Inspection Robots Using Edge AI" (ResearchGate, title and snippet only) |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | The mobile-inspection-robot paper (robot platform, not smartphone; runtime model selection not indicated; not opened) |
| Search limitations | MODI, SneakPeek, conformal edge model selection and service-migration papers address dynamic model selection without an inspection task. They were judged off-task from title and snippet. |

### S05

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `smartphone industrial inspection energy-aware inference` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 1: Ombrulla article |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | "Sustainability Is Not Linear: Quantifying Performance, Energy, and Privacy Trade-offs in On-Device I…" (arXiv 2603.26603): title only; no inspection task indicated |
| Search limitations | Results were dominated by on-device LLM inference, activity recognition and mobile-inference surveys |

### S06

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `resource-aware mobile defect detection` |
| Database / engine | WebSearch |
| Results returned | 9 (one was this project's GitHub repository; excluded) |
| Relevant results inspected | 4: Sci. Rep. screen paper; CE-SGNet; Electronics 15(17):3915 (snippet); Cloud-Edge Collaborative Defect Detection, PMC11435656 (full text, keyword scan) |
| Strongest relevant papers | PMC11435656: edge (Raspberry Pi 4) PCB inspection with per-sample confidence-triggered escalation to a cloud model |
| Potential counterexamples | PMC11435656 is a **partial** counterexample: runtime adaptation in edge visual inspection, but not on a smartphone and not resource-driven. Electronics 15(17):3915 is **potential** (snippet only). |
| Unresolved items | Electronics 15(17):3915: the MDPI page returned an interstitial |
| Search limitations | "Resource-efficient" in titles describes model design, not runtime decisions |

### S07

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `adaptive inference smartphone industrial vision` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 2: Frontiers 10.3389/fcomp.2025.1535775 (full text via alphaXiv reader); Ombrulla article |
| Strongest relevant papers | None: the Frontiers paper detects phone *usage* in restricted zones |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Vendor pages (Latent AI, AMD, Tipteh) and an O-RAN paper were off-task |

### S08

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 |
| Exact query | `runtime model selection mobile visual inspection` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: Ombrulla article |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | US patents 12480890 ("Deep learning based mode selection for inspection"), 10733723 and 10706525: patents are outside the scholarly corpus and were not assessed |
| Search limitations | Patents and a Unity runtime inspector tool dominated the results |

---

## GC-02: energy/thermal evaluation in smartphone or edge visual inspection

### S09

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `smartphone visual inspection energy consumption` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: all results were generic smartphone power-measurement papers (e.g. Carroll and Heiser, USENIX ATC 2010) |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Smartphone energy measurement methodology papers are useful for experimental design, but they are not inspection papers |

### S10

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `mobile defect detection thermal evaluation` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Every result used thermography as the inspection modality, which is a known false positive |

### S11

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `smartphone industrial inspection power consumption` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Results were generic smartphone power analyses, a measurement application note and a pill-recognition patent |

### S12

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `edge visual inspection thermal evaluation` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 1: arXiv 2603.20288 (full text) |
| Strongest relevant papers | arXiv 2603.20288: edge-oriented visual anomaly detection. It measures time and memory on a desktop CPU used to simulate edge conditions; no energy or thermal results |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Thermography and thermal-odometry results are false positives |

### S13

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `mobile manufacturing inspection energy efficiency` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Results were plant energy management and vendor blogs |

### S14

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `smartphone inspection battery consumption` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None. "Smartphone Sensor Battery Consumption: A Standardized and Reproducible Test Protocol" (Sensors, doi 10.3390/s26102923) is a measurement-protocol paper, not inspection. It was noted for experimental design only. |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Results were consumer battery-health how-to pages |

### S15

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `mobile visual inspection temperature` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Results were thermal-camera products and high-temperature inspection services |

### S16

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 |
| Exact query | `edge defect detection energy evaluation` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 3: EEDD (snippet); Electronics 15(17):3915 (snippet); "Solar Panel Defect Detection using FOMO on Edge Impulse" (title) |
| Strongest relevant papers | None verified |
| Potential counterexamples | Electronics 15(17):3915 (potential; snippet only); FOMO solar-panel paper (potential; unresolved) |
| Unresolved items | FOMO/Edge Impulse paper (ebpj.e-iph.co.uk 6822): not opened. Electronics 15(17):3915: interstitial page only. |
| Search limitations | EEDD's "energy-based" names the detection method. In the FOMO paper, "energy" may refer to the solar domain. |

### S17 (supplementary)

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (and GC-01) |
| Exact query | question: `visual inspection or defect detection deployed on smartphone or edge device with measured energy consumption, power, battery or temperature`; keywords: `defect detection`, `energy consumption`, `edge device`, `smartphone` |
| Database / engine | alphaXiv discover (arXiv only) |
| Results returned | 12 |
| Relevant results inspected | 6, all full text: 2608.14727, 2606.07659, 2603.16451, 2603.20288 (already read), 2309.00022, 2505.07119. PaSTe (2410.11591) was also read; it is cited by 2603.20288 and 2505.07119. |
| Strongest relevant papers | **TinyGLASS (2603.16451)**: in-sensor industrial visual anomaly detection (Sony IMX500 with Raspberry Pi 5) reporting 4.0 mJ per inference and 470 GMAC/J |
| Potential counterexamples | TinyGLASS is a **partial** GC-02 counterexample (energy reported on an edge visual-inspection platform; no thermal results; not a smartphone). 2309.00022 measures energy with a power meter, but its task is pedestrian detection (not a counterexample). |
| Unresolved items | How TinyGLASS obtained its energy figure (instrumented measurement vs. a power model) is not described in detail |
| Search limitations | arXiv-only; ranking is relevance-based and not reproducible; papers on optoelectronic hardware, SOT-MTJ and medical routing were off-task |

---

## GC-03: smartphone visual inspection with runtime adaptation and confidence-aware downstream decisions

### S18

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `smartphone visual inspection confidence-aware` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 2: arXiv 2608.21967 (full text); Ombrulla mobile inspection app page (title and snippet; vendor) |
| Strongest relevant papers | arXiv 2608.21967: production-line inspection that defers uncertain units to human review. The online deferral is not yet evaluated (work in progress), and the platform is not stated. |
| Potential counterexamples | 2608.21967 (potential, for the confidence component only) |
| Unresolved items | None |
| Search limitations | Results included phone-as-product vendor pages (FIH Mobile, SwitchOn), medical smartphone screening and an explanation-auditing paper |

### S19

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `mobile inspection confidence gating` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | "Mobile inspection" matched mobile car-inspection services and patents. The MobileNetV2 confidence-aware detector (PMC8037591) targets autonomous driving, not inspection. |

### S20

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `smartphone defect detection recapture` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 4: road-defect smartphone system (PMC11014122 = P002, already in the corpus, peripheral); CE-SGNet; phone-surface RK3568 paper (PMC12716720, snippet); building-defect smartphone app (Wiley stc.2751 = P001, already in the corpus) |
| Strongest relevant papers | P001 and P002 (both already in the corpus) |
| Potential counterexamples | P001 remains **potential** (abstract-level Unknowns; full text not accessible) |
| Unresolved items | None new |
| Search limitations | No result described confidence-triggered recapture. "Recapture" did not retrieve recapture-on-low-confidence work. |

### S21

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `mobile visual inspection additional view` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Results were vendor products (Visometry Twyn, IBM Maximo, Screening Eagle) and generic guides with no evaluated method |

### S22

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `smartphone inspection adaptive inference confidence` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: Springer "Deep learning enabled computer vision in remanufacturing and refurbishment applications: defect detection and grading for smart phones" (snippet) |
| Strongest relevant papers | None: phones are the graded product, and the confidence threshold is a reporting setting |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Other results were activity recognition, cognitive screening and patents |

### S23

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `edge inspection confidence-triggered recapture` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 2: a dev.to blog on falling back from edge detection to a cloud VLM when confidence drops (snippet); an iFactory vendor blog on flagging uncertain scores for review (snippet) |
| Strongest relevant papers | None scholarly. Both items are grey literature describing confidence-triggered fallback as a pattern, without an evaluated inspection system. |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | "Recapture" matched image-recapture forensics and capture–recapture statistics |

### S24

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `mobile visual inspection uncertainty decision` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: "Visual inspection via anomaly detection by automated uncertainty propagation" (SPIE, title only); MDPI Electronics 15(12):2727 review of AI visual inspection (snippet) |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | SPIE 12136-1213611 (uncertainty propagation in visual inspection): title only; platform and downstream action unknown |
| Search limitations | "Uncertainty in visual inspection data" results concern human inspector disagreement (Bristol) |

### S25

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | `smartphone industrial inspection multi-view confidence` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 3: arXiv 2608.30997 (abstract); ActiveInspect (PMC13468834, full text, keyword scan); multiview AI framework (PMC11945225, title only) |
| Strongest relevant papers | ActiveInspect (Sensors 26(15):4932): learned, sample-adaptive selection of further views or modalities when the initial view is ambiguous. It runs a 7B VLM on A100 GPUs over a pre-acquired observation pool. |
| Potential counterexamples | ActiveInspect is a **partial** counterexample: additional-view decision and sample-adaptive computation, but not a smartphone, and the trigger is a learned policy rather than a confidence threshold |
| Unresolved items | PMC11945225 (multiview early-fusion framework): title only; no indication of a confidence-triggered action |
| Search limitations | 2608.30997 inspects smartphone cover glass (phone as product) |

### S26 (supplementary)

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 |
| Exact query | question: `on-device smartphone visual inspection where low confidence or uncertainty triggers recapture, additional view, or human review, with adaptive inference`; keywords: `smartphone`, `inspection`, `uncertainty`, `recapture` |
| Database / engine | alphaXiv discover (arXiv only) |
| Results returned | 12 |
| Relevant results inspected | 3: 2608.21967 (full text, also found by S18); 2512.13497 (full text); 2608.30997 (abstract) |
| Strongest relevant papers | 2608.21967 (see S18) |
| Potential counterexamples | No new ones |
| Unresolved items | 2609.02212 (FuDU, uncertainty for streaming active learning) and 2609.14219 (active metrological inspection with evidence gating): titles and abstracts only. Neither indicates a smartphone platform. |
| Search limitations | arXiv-only |

### S27 (verification lookup)

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (verification) |
| Exact query | `Perez 2021 "Deep learning smartphone application for real-time detection of defects in buildings" Structural Control and Health Monitoring` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: Wiley landing record of P001 |
| Strongest relevant papers | P001 (already in the corpus) |
| Potential counterexamples | P001 (potential; unchanged) |
| Unresolved items | P001 full text: Wiley and ResearchGate were not reachable from this environment |
| Search limitations | A bibliographic lookup, not a discovery search |

---

## Summary of what the searches found

| Candidate | Searches | Full counterexamples | Partial counterexamples found in Step 9.8 | Potential (unresolved) |
| :-- | :-- | :-- | :-- | :-- |
| GC-01 | S01–S08, S17 | None | arXiv 2608.14727 (edge cascade); PMC11435656 (edge confidence-triggered offloading) | Electronics 15(17):3915 |
| GC-02 | S09–S17 | None | arXiv 2603.16451 TinyGLASS (energy reported; no thermal; not a smartphone) | Electronics 15(17):3915; FOMO/Edge Impulse paper; P007 (from Step 9.7) |
| GC-03 | S18–S27 | None | ActiveInspect (Sensors 26(15):4932); PMC11435656; arXiv 2608.14727 | arXiv 2608.21967; P001 |

The four partial counterexamples above were confirmed by the researcher in the Step 9.8 methodology correction and remain partial.

"None" for full counterexamples describes these searches only. It is not a claim about the literature as a whole.

---

## Narrowed-claim falsification check (S28–S45)

**Purpose.** After the methodology correction, 18 further searches (6 per candidate) were run against the **exact narrowed wording**, to look for a full counterexample. The earlier 27 searches were not repeated. Full-text verification of hits used the alphaXiv reader. These reads are verification of returned hits, not additional searches.

**Full-counterexample criteria.**
- **GC-01:** smartphone + optical visual inspection + resource/device-state-driven runtime adaptation.
- **GC-02:** resource-constrained smartphone + optical visual inspection + resource-adaptive inference + direct energy evaluation + direct thermal evaluation.
- **GC-03:** resource awareness + smartphone + visual inspection + runtime adaptation + confidence-aware downstream verification. Learned view selection alone does not count (Decision B).

### S28

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `resource-aware adaptive inference smartphone visual inspection` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 3: Mobiprox (title); ApproxDet (title); Ombrulla article (already read in S02) |
| Strongest relevant papers | None meeting all three GC-01 criteria. ApproxDet and Mobiprox describe resource/contention-aware adaptive inference on mobiles for generic vision, not inspection |
| Potential counterexamples | None (ApproxDet, Mobiprox: not_counterexample at title level) |
| Unresolved items | "A Unified and Resource-Aware Framework for Adaptive Inference Acceleration on Edge and Embedded Platforms" (Electronics 14(11):2188): title only; no indication of smartphone or inspection |
| Search limitations | This project's GitHub repository was returned and excluded. Vendor text in the Ombrulla article describes battery/temperature-based model selection as a possibility, not an evaluated system |

### S29

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `resource-driven runtime adaptation smartphone inspection` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: results are self-adaptive software-engineering papers and OODIn (mobile inference optimisation), none on inspection |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | "Inspection" did not retrieve visual-inspection work; results were runtime-verification and Android analysis papers |

### S30

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `resource-aware smartphone defect detection adaptive inference` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: arXiv 2606.24173 (full text); smartphone-screen defect papers (already classified, phone as product) |
| Strongest relevant papers | arXiv 2606.24173 has a confidence-gated adaptive cascade, but on tabular sensor data |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Phone-as-product false positives dominated (CE-SGNet, MSAdaNet, DY-YOLO) |

### S31

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `dynamic resource-aware inference mobile visual inspection` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: DMS: Dynamic Model Scaling for Quality-Aware Deep Learning Inference in Mobile and Embedded Devices (title only) |
| Strongest relevant papers | None meeting all criteria; DMS and the dynamic-DNN runtime-management papers address generic mobile inference |
| Potential counterexamples | None |
| Unresolved items | DMS (ResearchGate): title only; no indication of an inspection task |
| Search limitations | This project's GitHub repository was returned and excluded. PMC13363810 concerns chemical-plant risk inference from scene graphs, not mobile |

### S32

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `smartphone industrial inspection resource-aware model selection` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 3: SAEC, arXiv 2509.17136 (full text); Smart-Inspect, arXiv 2010.00741 (title); RK3568 phone-surface paper (already classified) |
| Strongest relevant papers | SAEC: industrial visual inspection with runtime edge/cloud routing driven by scene complexity and confidence; Xeon CPU + A100, not a smartphone |
| Potential counterexamples | SAEC (partial) |
| Unresolved items | None |
| Search limitations | Smart-Inspect inspects smartphone glass (phone as product). Patents were not assessed |

### S33

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-01 (narrowed wording) |
| Exact query | `smartphone visual inspection battery temperature adaptive inference` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: arXiv 2603.26603 (full text; previously unresolved) |
| Strongest relevant papers | arXiv 2603.26603: smartphone energy and temperature measurement during on-device LLM inference; no inspection, no runtime adaptation |
| Potential counterexamples | None for GC-01 |
| Unresolved items | None |
| Search limitations | Results were battery-temperature prediction and smartphone thermal-behaviour papers without an inspection task |

### S34

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `smartphone visual inspection energy thermal adaptive inference` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: arXiv 2010.06291 (full text); arXiv 2603.26603 (full text) |
| Strongest relevant papers | arXiv 2603.26603 (smartphone, energy + temperature, LLM workload); arXiv 2010.06291 (Raspberry Pi 4B thermal throttling, ImageNet classification) |
| Potential counterexamples | arXiv 2603.26603 (partial, outside visual-inspection scope) |
| Unresolved items | "LLM Inference at the Edge: Mobile, NPU, and GPU Performance Efficiency Trade-offs Under Sustained Load" (arXiv 2603.23640) and EnerInfer (arXiv 2606.23001): titles/snippets only; both concern LLM workloads, not inspection |
| Search limitations | Smartphone thermal-imaging pages are false positives (thermal camera as inspection modality) |

### S35

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `smartphone defect inspection energy thermal evaluation` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: smartphone-based fluorescence thermography and thermal-camera accessories (thermography as inspection modality) |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | All results are thermography false positives or battery-safety inspection |

### S36

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `mobile visual inspection energy thermal resource adaptive` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: infrared inspection services, patents and mobile-robot thermal analytics |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Thermography false positives; patents not assessed |

### S37

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `smartphone industrial inspection power temperature adaptive` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: "Power and Thermal Analysis of Commercial Mobile Platforms: Experiments and Case Studies" (arXiv 1904.09814, title only) |
| Strongest relevant papers | None: arXiv 1904.09814 characterises mobile platforms in general, not an inspection system |
| Potential counterexamples | None |
| Unresolved items | arXiv 1904.09814: title only |
| Search limitations | Remaining results were smartphone thermal-camera products |

### S38

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `resource adaptive smartphone inspection energy temperature` |
| Database / engine | WebSearch |
| Results returned | 10 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: generic smartphone power/thermal management (eTEC, iOS thermal states) and temperature-sensing papers |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | No inspection task appeared in the results |

### S39

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-02 (narrowed wording) |
| Exact query | `mobile defect detection joint energy thermal evaluation` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: "joint" retrieved solder/polymer joint thermography |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Query wording attracted welded/solder-joint inspection by thermography |

### S40

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `resource-aware smartphone visual inspection confidence adaptive` |
| Database / engine | WebSearch |
| Results returned | 8 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: driver-behaviour super-resolution, medical smartphone screening and audio-visual QA papers |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | This project's GitHub repository was returned and excluded |

### S41

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `smartphone visual inspection resource adaptive confidence gating` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None: phone-as-product screen inspection, medical screening, generic confidence-gating topic page |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | "Adaptive confidence gating" topic aggregator (emergentmind) is grey literature |

### S42

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `smartphone defect inspection confidence-triggered recapture` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: RK3568 phone-surface paper (already classified) |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | "Automated Evaluation of Smartphone Screen Damage" (bonviewpress): title only; phone as product |
| Search limitations | "Recapture" again matched capture-recapture statistics and image-recapture forensics |

### S43

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `smartphone industrial inspection adaptive inference confidence` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: RobustDefect-LLM, arXiv 2608.08589 (full text); "Adaptive visual detection of industrial product defects" (PMC10280690, title only) |
| Strongest relevant papers | RobustDefect-LLM: confidence/margin-triggered HUMAN REVIEW with a mobile client; inference in a backend, no runtime adaptation |
| Potential counterexamples | RobustDefect-LLM (partial) |
| Unresolved items | PMC10280690: title only; platform and confidence use unknown |
| Search limitations | Smartphone-grading and orthopedic-tray papers do not run inference on a phone |

### S44

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `mobile visual inspection resource-aware confidence verification` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 2: arXiv 2608.21967 (already read in S18); isaacyanney/confidence-aware-visual-inspection (GitHub, snippet) |
| Strongest relevant papers | arXiv 2608.21967 (unchanged: potential) |
| Potential counterexamples | None new |
| Unresolved items | None |
| Search limitations | The GitHub portfolio project is grey literature (FastAPI service), not a smartphone system. This project's GitHub repository was returned and excluded |

### S45

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording) |
| Exact query | `smartphone inspection low confidence additional view adaptive` |
| Database / engine | WebSearch |
| Results returned | 9 |
| Relevant results inspected | 1: arXiv 2608.30997 (already classified, phone as product) |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | "Adaptive texture and low-light feature learning in enhanced MobileNetV4 for industrial packaging quality inspection" (PMC13458609): title only; "adaptive" appears to describe feature learning |
| Search limitations | Medical smartphone screening and low-vision aids were off-task |

### Outcome of S28–S45

| Candidate | Full counterexamples | Partial (verified) | Potential / unresolved | Not counterexamples (verified or title-level) |
| :-- | :-- | :-- | :-- | :-- |
| GC-01 | None | SAEC (arXiv 2509.17136): visual inspection + content/confidence-driven adaptation; not resource-driven; not a smartphone | Electronics 14(11):2188 (title only); DMS (title only) | ApproxDet, Mobiprox (generic mobile vision, title level) |
| GC-02 | None | SAEC (visual inspection + adaptation + energy; no thermal; not a smartphone); arXiv 2603.26603 (smartphone + energy + temperature; LLM workload, not inspection; no adaptation) | arXiv 1904.09814 (title only) | arXiv 2010.06291 (thermal only; RPi4; not inspection) |
| GC-03 | None | SAEC (visual inspection + adaptation + confidence-triggered escalation; no resource awareness; not a smartphone); RobustDefect-LLM (visual inspection + confidence-triggered human review; inference not on the phone; no adaptation) | PMC10280690 (title only) | arXiv 2606.24173 (confidence-gated cascade on tabular sensor data) |

No full counterexample was identified in this targeted falsification search.

This describes 18 bounded web searches (one results page each) and the hits verified from them. It is not a statement about the literature as a whole.


## Step 9.9B GC-03 evidence closure (S46–S57)

_2026-10-05, Claude Code, branch `claude/step-9-9b-gc03-evidence-closure`. Twelve searches against GC-03 only, intended to falsify it. Report: [`gc03_evidence_closure.md`](gc03_evidence_closure.md)._

**Database access.** IEEE Xplore, ACM Digital Library, Scopus and Web of Science were all blocked by this environment's egress proxy (HTTP CONNECT 403 or `EGRESS_BLOCKED` on 2026-10-05). No results were fabricated. Each planned database search was run through a legitimate substitute, named in the "Database / engine" row:
- IEEE Xplore: 3 WebSearch queries restricted to the IEEE domain;
- ACM DL: 3 WebSearch queries restricted to the ACM domain;
- Scopus: 3 Consensus queries;
- Web of Science: 3 PubMed queries.

**Verification lookups (not counted among the 12 searches).** Full texts read:
- PMC11435656, PMC13468834 (ActiveInspect) and PMC10280690, through the PubMed Central full-text service.

Repository-copy searches:
- P001: two WebSearch queries; the hits were a different paper;
- P007: one WebSearch query.

Citation follow-up and snippet lookup:
- One WebSearch query followed the 'resource awareness module' citation in PMC11435656 and found AIVD, arXiv 2601.04734.
- One WebSearch query looked up AIVD snippet detail.

Blocked fetches: onlinelibrary.wiley.com (P001, P007), downloads.hindawi.com, structurae.de, www.mdpi.com and arxiv.org.

### S46

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `smartphone visual inspection resource-aware adaptive inference confidence` |
| Database / engine | WebSearch restricted to ieeexplore.ieee.org (IEEE Xplore itself blocked by the egress proxy; not the Xplore search interface) |
| Results returned | 10 |
| Relevant results inspected | 3: RobustDefect-LLM (already classified); CE-SGNet (already classified); ApproxDet (already classified, generic mobile vision) |
| Strongest relevant papers | None meeting all five criteria; medical smartphone screening papers off-task |
| Potential counterexamples | None new |
| Unresolved items | None |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page |

### S47

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `smartphone defect detection resource-aware adaptive confidence on-device` |
| Database / engine | WebSearch restricted to ieeexplore.ieee.org (IEEE Xplore itself blocked by the egress proxy; not the Xplore search interface) |
| Results returned | 9 |
| Relevant results inspected | 3: PMC12716720 (already classified); SSGD dataset (phone as inspected product); arXiv 2509.20946 (on-device laser power-meter defect detection, title/snippet) |
| Strongest relevant papers | None: phone-as-product inspection and a non-smartphone edge-AI core |
| Potential counterexamples | None new |
| Unresolved items | arXiv 2509.20946: snippet only; platform is an edge-AI core, not a smartphone |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page |

### S48

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `mobile industrial inspection resource-aware inference confidence escalation` |
| Database / engine | WebSearch restricted to ieeexplore.ieee.org (IEEE Xplore itself blocked by the egress proxy; not the Xplore search interface) |
| Results returned | 10 |
| Relevant results inspected | 2: HAPI, arXiv 2008.03997 (new, snippet); RobustDefect-LLM (already classified) |
| Strongest relevant papers | HAPI: confidence-based progressive inference on generic workloads (partial; not inspection) |
| Potential counterexamples | None |
| Unresolved items | HAPI: snippet only |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page; patents returned |

### S49

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `smartphone visual inspection resource-aware adaptive inference confidence` |
| Database / engine | WebSearch restricted to dl.acm.org (ACM DL itself blocked by the egress proxy; not the ACM DL search interface) |
| Results returned | 9 |
| Relevant results inspected | 2: ApproxDet (already classified; ACM DL PDF link); Corun (mobile image sensing, not inspection) |
| Strongest relevant papers | None meeting all five criteria |
| Potential counterexamples | None new |
| Unresolved items | None |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page |

### S50

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `smartphone manufacturing inspection dynamic inference confidence` |
| Database / engine | WebSearch restricted to dl.acm.org (ACM DL itself blocked by the egress proxy; not the ACM DL search interface) |
| Results returned | 9 |
| Relevant results inspected | 2: Multi-View Reflective Surface Inspection (already classified); Mobiprox (already classified) |
| Strongest relevant papers | None meeting all five criteria |
| Potential counterexamples | None new |
| Unresolved items | A snippet describing edge systems delegating low-confidence inspections to a higher instance could not be attributed to a source |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page |

### S51

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `mobile defect detection resource-aware adaptive model selection confidence threshold recapture` |
| Database / engine | WebSearch restricted to dl.acm.org (ACM DL itself blocked by the egress proxy; not the ACM DL search interface) |
| Results returned | 9 |
| Relevant results inspected | 3: RAMS, arXiv 2606.14716 (new, snippet); ModiPick (generic SLA-aware mobile inference); arXiv 2509.20946 |
| Strongest relevant papers | RAMS: resource-adaptive, detection-conditioned model switching for road-user perception (partial; not inspection) |
| Potential counterexamples | None |
| Unresolved items | RAMS: snippet only |
| Search limitations | The domain filter leaked: most results came from PMC, arXiv and USPTO rather than the restricted domain; one results page |

### S52

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `smartphone visual inspection resource-aware adaptive inference confidence-based verification defect detection` |
| Database / engine | Consensus (substitute for Scopus, which is blocked; Consensus states coverage of Semantic Scholar, PubMed, Scopus and arXiv) |
| Results returned | 10 |
| Relevant results inspected | 4: Zakaria et al. 2022 (new, abstract); P001 (corpus, abstract re-read); Multi-View Reflective (already classified); CE-SGNet (already classified) |
| Strongest relevant papers | Zakaria et al. 2022: bridge visual inspection on edge devices including smartphones, with human-verified results (potential, abstract only) |
| Potential counterexamples | Zakaria et al. 2022 (potential) |
| Unresolved items | Zakaria et al. 2022: runtime adaptation and confidence-triggered verification not stated in the abstract |
| Search limitations | One results page (10 results, free tier); phone-as-product glass inspection papers off-task |

### S53

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `on-device defect detection mobile phone dynamic model switching battery thermal confidence recapture` |
| Database / engine | Consensus (substitute for Scopus, which is blocked; Consensus states coverage of Semantic Scholar, PubMed, Scopus and arXiv) |
| Results returned | 10 |
| Relevant results inspected | 0: results drifted to lithium-ion battery fault detection; DGNet (static detector on Jetson Nano) not relevant |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Query terms 'battery thermal' were matched as the inspected object; one results page |

### S54

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `mobile industrial inspection resource-aware inference low-confidence escalation human review` |
| Database / engine | Consensus (substitute for Scopus, which is blocked; Consensus states coverage of Semantic Scholar, PubMed, Scopus and arXiv) |
| Results returned | 10 |
| Relevant results inspected | 5: Yan et al. 2025 (new, abstract); Choi et al. 2026 (new, abstract); RobustDefect-LLM (already classified); arXiv 2608.21967 (already classified); P011 (corpus) |
| Strongest relevant papers | Yan et al. 2025: visual defect inspection with confidence-based early exit (partial; not on a smartphone). Choi et al. 2026: confidence-threshold cooperative edge inference with joint radio-resource optimisation (potential; task and device not stated) |
| Potential counterexamples | Choi et al. 2026 (potential) |
| Unresolved items | Choi et al. 2026: device type, image task and runtime role of resource state not stated in the abstract |
| Search limitations | One results page; first attempt hit the Consensus rate limit and was retried |

### S55

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `(smartphone OR "mobile phone") AND ("defect detection" OR "visual inspection") AND (adaptive OR "resource-aware" OR "dynamic inference") AND confidence` |
| Database / engine | PubMed (substitute for Web of Science, which is blocked; indexes Sensors, PeerJ CS and other engineering journals in PMC) |
| Results returned | 3 |
| Relevant results inspected | 0: all three records are smartphone cervical-cancer screening (medical, not inspection of physical items) |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | PubMed covers engineering only through journals it indexes |

### S56

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `(smartphone OR mobile) AND "industrial inspection" AND (resource OR battery OR thermal) AND (confidence OR uncertainty)` |
| Database / engine | PubMed (substitute for Web of Science, which is blocked; indexes Sensors, PeerJ CS and other engineering journals in PMC) |
| Results returned | 0 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Zero records; PubMed engineering coverage is partial |

### S57

| Field | Value |
| :-- | :-- |
| Date | 2026-10-05 |
| Candidate | GC-03 (narrowed wording; Step 9.9B evidence closure) |
| Exact query | `(smartphone OR "edge device") AND (manufacturing OR "surface defect") AND ("model switching" OR "early exit" OR "dynamic inference" OR cascade) AND (confidence OR uncertainty)` |
| Database / engine | PubMed (substitute for Web of Science, which is blocked; indexes Sensors, PeerJ CS and other engineering journals in PMC) |
| Results returned | 0 |
| Relevant results inspected | 0 |
| Strongest relevant papers | None |
| Potential counterexamples | None |
| Unresolved items | None |
| Search limitations | Zero records; PubMed engineering coverage is partial |

### Outcome of S46–S57

| Candidate | Full counterexamples | Partial | Potential / unresolved | Not counterexamples |
| :-- | :-- | :-- | :-- | :-- |
| GC-03 | None | Yan et al. 2025 (abstract; visual inspection + early exit + confidence; not a smartphone); RAMS (snippet; not inspection); HAPI (snippet; not inspection); P007 (corpus; not a smartphone) | AIVD (snippet; resource-aware scheduling claimed; platform and confidence role unknown); Choi et al. 2026 (abstract); Zakaria et al. 2022 (abstract); P001 (corpus, abstract only); Electronics 15(17):3915 (snippet) | PMC10280690 (full text: training-time meta-learning) |

No full counterexample to GC-03 was identified in these twelve searches and the verification lookups. This describes bounded, one-page searches through substitute engines. It is not a statement about the literature as a whole.
