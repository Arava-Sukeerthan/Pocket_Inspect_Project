# Literature Search Log

> **Scope:** this file records literature-search activity only (queries, sources, hit counts, screening and retained IDs). Append a new batch section for each search round, attributed to the agent that ran it; do not rewrite earlier batches. General repository changes by agents are recorded in `docs/agent_sync/CHANGELOG.md`.

Each batch records the date, search group, exact query, source, number of candidates screened and number retained. Hit counts are the total matches reported by the source; only the top-ranked results were screened.

## Batch 1 — 2026-10-01

**Sources:** OpenAlex API (primary search), Crossref API (DOI and metadata verification), doi.org handle API (DOI resolution), Semantic Scholar API (missing abstracts only), Springer and NeurIPS/PMLR landing pages (abstract and venue confirmation). ScienceDirect and ACM pages returned bot checks and were not used.

### 1a. Broad keyword searches (OpenAlex `search=`, relevance-ranked, publication date ≥ 2016-01-01, top 15 screened per query)

| Group | Query | Total hits | Screened | Retained (IDs) |
| :-- | :-- | --: | --: | :-- |
| G1 | smartphone computer vision edge AI | 29,648 | 15 | 0  |
| G1 | mobile device deep learning inference | 114,887 | 15 | 0  |
| G1 | smartphone visual inspection | 30,187 | 15 | 1 (P010) |
| G1 | mobile AI industrial inspection | 29,439 | 15 | 0  |
| G1 | smartphone defect detection | 20,634 | 15 | 2 (P001, P002) |
| G1 | on-device computer vision inspection | 80,380 | 15 | 0  |
| G2 | industrial visual inspection deep learning | 61,267 | 15 | 1 (P010) |
| G2 | automated visual inspection defect detection | 33,096 | 15 | 1 (P008) |
| G2 | manufacturing defect detection computer vision | 33,428 | 15 | 1 (P014) |
| G2 | edge AI industrial inspection | 37,135 | 15 | 2 (P011, P013) |
| G2 | real-time industrial defect detection | 113,870 | 15 | 1 (P012) |
| G3 | 3D printed defect detection computer vision | 9,144 | 15 | 5 (P016, P019, P020, P021, P024) |
| G3 | 3D printing defect detection deep learning | 10,213 | 15 | 4 (P015, P016, P019, P024) |
| G3 | additive manufacturing visual inspection | 22,493 | 15 | 0  |
| G3 | 3D printed parts inspection | 25,677 | 15 | 1 (P024) |
| G3 | real-time 3D printing defect detection | 20,775 | 15 | 6 (P015, P016, P017, P018, P019, P024) |
| G4 | adaptive inference edge AI | 146,686 | 15 | 1 (P027) |
| G4 | resource-aware inference edge devices | 64,590 | 15 | 1 (P036) |
| G4 | resource adaptive deep learning | 906,691 | 15 | 1 (P052) |
| G4 | dynamic neural network edge computing | 389,141 | 15 | 1 (P027) |
| G4 | energy-aware deep learning inference | 140,491 | 15 | 1 (P052) |
| G4 | thermal-aware edge AI | 32,155 | 15 | 2 (P007, P036) |
| G4 | latency-aware inference | 237,554 | 15 | 0  |
| G5 | multi-view industrial defect detection | 60,246 | 15 | 1 (P037) |
| G5 | multi-view visual inspection | 171,863 | 15 | 0  |
| G5 | multi-angle defect detection | 94,006 | 15 | 1 (P039) |
| G5 | active vision industrial inspection | 56,648 | 15 | 0  |
| G5 | adaptive viewpoint inspection | 39,944 | 15 | 2 (P041, P042) |
| G5 | multi-view 3D printing inspection | 12,924 | 15 | 2 (P015, P024) |
| G6 | uncertainty-aware defect detection | 33,202 | 15 | 3 (P047, P048, P049) |
| G6 | confidence-aware visual inspection | 64,688 | 15 | 1 (P013) |
| G6 | uncertainty estimation industrial inspection | 47,690 | 15 | 0  |
| G6 | selective prediction computer vision | 122,627 | 15 | 0  |
| G6 | confidence-based inspection | 326,521 | 15 | 1 (P013) |
| G6 | uncertainty-aware anomaly detection | 59,509 | 15 | 2 (P050, P052) |

**Observation:** broad relevance-ranked queries returned many off-topic, highly cited works (medical imaging, NLP, generic surveys). The narrower title/abstract queries in 1b were added for that reason.

### 1b. Targeted title/abstract searches (OpenAlex `title_and_abstract.search`, sorted by citations, ≥ 2016-01-01, top 12 screened)

| Group | Query | Total hits | Screened | Retained (IDs) |
| :-- | :-- | --: | --: | :-- |
| G1 | `smartphone "on-device" defect detection` | 84 | 12 | 0  |
| G1 | `smartphone deep learning crack detection real-time application` | 6 | 6 | 1 (P001) |
| G1 | `smartphone "TensorFlow Lite" detection inspection` | 1 | 1 | 0  |
| G1 | `"mobile phone" "industrial inspection" deep learning` | 2 | 2 | 0  |
| G1 | `deep learning android smartphones benchmark inference` | 4 | 4 | 2 (P003, P004) |
| G1 | `"mobile deep learning" measurement smartphones apps` | 0 | 0 | 0  |
| G2 | `edge device "Jetson" surface defect detection real-time` | 20 | 12 | 0  |
| G2 | `anomaly detection dataset industrial inspection unsupervised benchmark` | 67 | 12 | 0  |
| G3 | `fused deposition modeling defect detection camera deep learning` | 3 | 3 | 0  |
| G3 | `FDM 3D printing camera "convolutional neural network" monitoring` | 2 | 2 | 0  |
| G3 | `3D printing defect detection "Raspberry Pi"` | 20 | 12 | 1 (P022) |
| G4 | `thermal throttling deep learning inference mobile` | 6 | 6 | 2 (P031, P032) |
| G4 | `early exit neural network inference edge` | 205 | 12 | 2 (P027, P035) |
| G4 | `on-device deep learning resource constraints runtime adaptation mobile` | 7 | 7 | 2 (P033, P034) |
| G4 | `energy consumption deep learning inference smartphones measurement` | 2 | 2 | 0  |
| G5 | `multi-view anomaly detection industrial` | 130 | 12 | 3 (P037, P043, P044) |
| G5 | `multi-view convolutional neural network surface defect` | 13 | 12 | 1 (P040) |
| G5 | `"next best view" inspection defect` | 1 | 1 | 0  |
| G6 | `uncertainty quantification surface defect detection deep learning` | 11 | 11 | 1 (P051) |
| G6 | `"Monte Carlo dropout" defect detection` | 17 | 12 | 3 (P049, P051, P053) |
| G6 | `"selective classification" deep neural networks reject option` | 7 | 7 | 2 (P045, P046) |
| G6 | `image quality assessment defect inspection blur recapture` | 0 | 0 | 0  |

### 1c. Known-item lookups

Some candidates were well-known papers in these areas. Each was located by an exact-title search in OpenAlex or Crossref and then verified like every other candidate (metadata cross-check, DOI resolution, abstract). They did not come from the keyword queries above, and the selection may reflect prior familiarity with the field.

Retained from known-item lookup: P005, P006, P009, P023, P025, P026, P028, P029, P030, P038, P054

### Batch 1 totals

- Unique candidates screened in depth (metadata + abstract): 59
- Retained: 54
- Rejected: 2; Deferred: 3 (see `selected_papers.md`)
- Selection rationale: direct relevance to PocketInspect themes, peer-reviewed venue preferred, 2019–2026 preferred. Foundational pre-2019 works (BranchyNet, MCDNN, Neurosurgeon, Selective Classification) were kept where they define a technique used by later papers.
- Abstract-level extraction only; full-text review of each retained paper is pending.

