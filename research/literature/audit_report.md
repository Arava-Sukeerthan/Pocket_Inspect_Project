# Literature Audit Report: Batch 1

_Audit date: 2026-10-02. Auditor: Claude Code. Scope: `research/literature/papers.csv` (54 records, P001–P054). Per-paper results: [`audit_report.csv`](audit_report.csv)._

> **Status:** first-pass audit, findings only. `papers.csv` was **not** modified. The relevance classes are the auditor's **proposal** and need researcher/ChatGPT review. This report makes no novelty or research-gap claims.

---

## 1. Summary

| Measure | Result |
| :-- | --: |
| Records audited | 54 |
| Records that exist and whose metadata matches the registry | 54 / 54 |
| DOIs that resolve (doi.org handle API) | 52 / 52 with a DOI |
| Records without a DOI (proceedings page verified) | 2 (P045, P046) |
| Preprints (not peer-reviewed) | 1 (P054) |
| Duplicate records | 0 |
| Same work under several identifiers (single row kept, correct) | 2 (P028, P054) |
| Records with actionable metadata issues | 4 (P006, P007, P040, P054) |
| Records with actionable evidence issues | 13 |
| Retracted records (OpenAlex `is_retracted`) | 0 |

### Relevance classes

| Class | Meaning | Count | Paper IDs |
| :-- | :-- | --: | :-- |
| **A** | Directly relevant | 17 | P001, P002, P007, P011, P015, P016, P017, P018, P019, P020, P022, P023, P029, P031, P032, P033, P034 |
| **B** | Relevant supporting literature | 24 | P003, P004, P006, P008, P009, P012, P014, P021, P025, P027, P028, P030, P037, P038, P039, P041, P043, P045, P046, P047, P049, P050, P053, P054 |
| **C** | Peripheral / background | 12 | P005, P010, P024, P026, P035, P036, P040, P042, P044, P048, P051, P052 |
| **D** | Requires verification | 1 | P013 |
| **E** | Duplicate | 0 | — |

### Classes by search group (group as recorded in `notes`)

| Group | A | B | C | D | Total |
| :-- | --: | --: | --: | --: | --: |
| G1 Smartphone / mobile / on-device AI | 3 | 3 | 1 | 0 | 7 |
| G2 Industrial visual inspection | 1 | 4 | 1 | 1 | 7 |
| G3 3D-printed part inspection | 8 | 1 | 1 | 0 | 10 |
| G4 Adaptive / resource-aware inference | 5 | 4 | 3 | 0 | 12 |
| G5 Multi-view / active inspection | 0 | 5 | 3 | 0 | 8 |
| G6 Confidence / uncertainty | 0 | 7 | 3 | 0 | 10 |
| **Total** | **17** | **24** | **12** | **1** | **54** |

**Observation (fact):** no G5 or G6 record is class A. None of the multi-view or uncertainty papers involves smartphone, on-device or 3D-print inspection, at least at abstract level. This describes the current corpus only. It is **not** a research-gap finding, and it may change after full-text review or further searches.

---

## 2. Method

**Sources queried on 2026-10-02 (facts):**
- **doi.org handle API:** checked that each DOI resolves.
- **Crossref REST API:** title, authors (count and order), `issued` year and container title, compared with each row. Also checked for update and retraction notices.
- **DataCite API:** P054 (its arXiv DOI is registered with DataCite, not Crossref).
- **OpenAlex:** cross-check, retraction flag, and abstracts.
- **Semantic Scholar:** abstracts where OpenAlex or Crossref had none, or only a truncated one (P006, P008, P019, P023, P049).
- **Publisher and proceedings landing pages:** Springer (P018, P024), NeurIPS (P045), PMLR (P046).

**Checks per record.** These follow the 23 audit questions from the task.

- **Checks 1–7:** metadata and existence. These were done automatically: stored values were compared with the normalised registry values.
- **Checks 8–9:** relevance and group fit. These were judged against [`PROJECT_SPEC.md`](../../PROJECT_SPEC.md). The search-group assignment was also compared with the IDs retained in [`search_log.md`](search_log.md).
- **Checks 10–20:** each `Yes`/`No` characteristic value was checked against the retrieved abstract text and against the rules in [`README.md`](README.md) §2 (e.g. "never infer `on_device`").
- **Checks 21–23:** the limitations, future_work and evidence fields were checked against the abstract.

**Relevance class criteria (auditor's proposal; requires researcher review):**
- **A, directly relevant:** the paper addresses at least one of PocketInspect's target combinations. These are:
  - smartphone or on-device edge visual defect inspection;
  - camera-based defect detection for 3D-printed parts;
  - on-device mobile/edge inference with runtime resource or thermal adaptation.
- **B, relevant supporting literature:** a method, dataset or benchmark that PocketInspect would build on or compare against, in one research dimension.
- **C, peripheral or background:** surveys and reviews, non-optical modalities (magnetic flux leakage, ultrasonic, tactile, point-cloud-only), or broad contextual studies.
- **D, requires verification:** relevance or the key coded claims cannot be confirmed from the available source.
- **E, duplicate:** the same work appears as more than one row.

**Limits of this audit (facts):**
- The audit is at abstract level only. No full texts were read, so `Unknown` values were not upgraded and missing limitations or future work could not be checked.
- Only 2 records have a `limitations` value (P024, P042) and only 1 has a `future_work` value (P024). For the other records, checks 21–22 have nothing to verify.
- The fetch and compare scripts were run from a temporary scratch directory and are not committed. The audit can be repeated from the method above, but not by running a script in this repo.

---

## 3. Duplicates

- `python scripts/manage_literature.py validate`: 0 duplicate IDs, 0 duplicate DOIs, 0 duplicate titles.
- Fuzzy title comparison (similarity > 0.6) flagged 9 pairs. All were checked by hand and are **distinct works** that share wording: P003/P004, P003/P005, P012/P018, P017/P019, P018/P019, P019/P021, P024/P052, P041/P042, P048/P054.
- Two works are registered under more than one identifier. In both cases the CSV correctly keeps one row:
  - **P028:** the ASPLOS 2017 paper is also reprinted in ACM SIGPLAN Notices (10.1145/3093336.3037698). This is already recorded in `notes`.
  - **P054:** the arXiv 2107.11643 preprint is also posted on SSRN (10.2139/ssrn.4042653, 2022). `notes` mentions SSRN but not this DOI.

## 4. Verification and metadata findings

**All 54 records pass the existence and metadata checks.** Title, author count and order, year (Crossref `issued`) and venue match the registry for every record with a DOI. The 3 automatic mismatches were only HTML encoding:
- P021 and P049: `&amp;` in the Crossref venue.
- P047: `<sup>` tags in the Crossref title.

**Verification caveats:**
- **P045, P046:** no DOI. Title, authors and year were confirmed on the NeurIPS and PMLR proceedings pages. An OpenAlex title search for P045 returned an unrelated work, so the proceedings page is the authoritative source for P045.
- **P054:** arXiv preprint, not peer-reviewed. The README allows this only when no peer-reviewed version exists. No peer-reviewed version was found in Crossref on 2026-10-02.

**Actionable metadata issues:**

| Paper | Issue | Recommended action |
| :-- | :-- | :-- |
| P006 | arXiv version (2109.13963) not recorded in `notes` | Record the alternative identifier |
| P007 | `search_log.md` retains P007 under a G4 query ("thermal-aware edge AI"), but `notes` assign G1 | Reconcile the group assignment with the search log |
| P040 | G5 fit is weak: "multi-view" refers to a point-cloud model representation, not camera views | Researcher to decide the group (or keep G5 with the existing caveat) |
| P054 | SSRN DOI not recorded in `notes` | Record 10.2139/ssrn.4042653 |

**Informational (not an error):** 11 records came from known-item lookups, not keyword queries: P005, P006, P009, P023, P025, P026, P028, P029, P030, P038, P054. Their group is a thematic assignment. This matches §1c of `search_log.md`.

## 5. Evidence findings

No coded `Yes` value contradicts the source abstract. All 54 evidence fields paraphrase their abstract accurately. The issues below are **weak or interpretive support** and **provenance labelling**. None of them is a fabrication.

| Paper | Field | Issue |
| :-- | :-- | :-- |
| P002 | latency_evaluation | Rests on a comparative "processing speed" claim; no figure in the abstract |
| P003 | latency_evaluation | The abstract says "evaluate the performance" only; no latency item in the evidence field |
| P004 | resource_awareness | Rests on CPU/GPU consumption benchmarking, not on resource-aware adaptation |
| P005 | on_device | Inferred from "models deployed on smartphones" in a static app analysis; the abstract does not say inference runs on the device (README rule) |
| P006 | evidence source, latency_evaluation | Labelled "OpenAlex/Crossref abstract", but the OpenAlex abstract is truncated; the claims match the full Semantic Scholar/arXiv abstract. Latency rests on "performance across devices" |
| P013 | edge_device, relevance | "Edge Cloud Computing" is plant IT infrastructure, not an edge inference device. The abstract does not say the method is image-based → class **D** |
| P026, P035 | adaptive_inference | `Yes` codes the survey's topic, not an evaluated system; this convention is undocumented |
| P027 | latency_evaluation | No explicit evidence item; the abstract claims "low-latency" without figures |
| P031 | adaptive_inference, smartphone | Adaptation is CPU/GPU frequency scaling (system-level). Smartphone = Yes relies on identifying "Mi 11 Lite" as a phone model |
| P034 | latency_evaluation | Rests on adaptation time (< 40 µs), not inference latency |
| P040 | anomaly_detection | Rests on "unsupervised method for defect detection" (interpretive) |
| P042 | limitations | Describes a field-wide limitation of automated planning, not the paper's own method; no matching evidence item |

Four further notes are recorded in the CSV and need no action:
- **P011:** on_device rests on deployment wording, which is acceptable.
- **P025:** the confidence-versus-calibrated-uncertainty caveat is already in `notes`.
- **P028:** the truncated OpenAlex abstract was resolved by the Crossref reprint abstract, which confirms the stored figures.
- **P039:** latency is measured as throughput, which is acceptable.

**Cross-cutting issue (requires researcher decision):** the schema ([`src/literature/schema.py`](../../src/literature/schema.py)) lists the 12 characteristic fields but does not define them. The README gives rules only for `smartphone`, `on_device`, `resource_awareness` (negative rule only), `multi_view` and `uncertainty`. Most of the evidence issues above come from these definitions being missing, especially:
- Does `latency_evaluation` include throughput, FPS or adaptation time?
- Does `adaptive_inference` include DVFS or system-level adaptation?
- Does `resource_awareness` include resource measurement without adaptation?
- Are surveys coded by their topic?

---

## 6. Recommended next steps

1. **Researcher/ChatGPT review** of the proposed A–D classes, especially the boundary cases P007, P013, P029 and P031–P034 (A vs B) and P040–P044 (B vs C).
2. **Write definitions** for all 12 characteristic fields in `research/literature/README.md`. Then re-check the 13 records with evidence issues against those definitions.
3. **After approval**, a separate correction task should edit `papers.csv`:
   - record the alternative identifiers for P006 and P054;
   - reconcile P007's group;
   - correct P006's evidence source label;
   - add missing evidence items (P003, P027, P042).
   Each change must be logged in `docs/agent_sync/CHANGELOG.md`.
4. **Full-text review**, prioritising class A and the D record (P013). This should resolve `Unknown` values and fill limitations and future work.
5. Re-check P054 for a peer-reviewed version before relying on it.
