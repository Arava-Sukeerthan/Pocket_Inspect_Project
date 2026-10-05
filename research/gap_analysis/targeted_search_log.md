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
