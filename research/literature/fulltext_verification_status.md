# Full-Text Verification Status

## Step 9.6 recovery (2026-10-03, Claude Code)

The follow-up work (`55873a3`) was recovered onto the new branch `claude/step-9-6-recovery` from `main` (`0a63176`). P029/P031/P033 statuses below are unchanged.

P002 and P013 relevance is **approved: peripheral/contextual, not core**; see `fulltext_version_verification.md` §13.

P013 Tables 4-5 remain unresolved because no PDF is available.

---

## Step 9.6 follow-up — evidence completion (2026-10-03, Claude Code)

| Paper | Status | Version used | Applied |
|---|---|---|---|
| P029 | **Verified (same-version copy)** | arXiv 1810.10090v1, author camera-ready with the MobiCom '18 ACM permission block | Yes: 7 characteristic + 4 free-text |
| P031 | **Verified (same-version copy)** | arXiv 2410.10847v1, author camera-ready with the DAC '24 ACM copyright block; consistent with the UMich Deep Blue copy | Yes: 8 characteristic + 4 free-text |
| P033 | **Verified (same-version copy)** | arXiv 2409.01089v1 in the final ACM TECS layout (Article 60, received/accepted dates) | Yes: 9 characteristic + 6 free-text |
| P013 Tables 4-5 | Still blocked: no rendered page obtainable | — | No; `accuracy_metrics` blank |
| P011 Fig. 4 | Unavailable (optional) | — | No change |

See `fulltext_version_verification.md` §8-12. The Step 9.6 rows below are history.

---

## Step 9.6 — version-of-record verification (2026-10-03, Claude Code)

_Details: [`fulltext_version_verification.md`](fulltext_version_verification.md). Earlier sections below are unchanged history._

| Paper | Step 9.6 status | Strongest version read | Applied to `papers.csv` |
|---|---|---|---|
| P011 | **Fully verified (version of record)** | Information Fusion 116 (2025) 102782, Elsevier-typeset PDF on the corresponding author's UNB host | Yes: 11 characteristic + 6 free-text values |
| P029 | Partially verified (version of record not reachable) | arXiv 1810.10090v1 (MobiCom '18 permission block) | No: stopped |
| P031 | Partially verified (version of record closed and not reachable) | UMich Deep Blue repository copy + arXiv 2410.10847v1 (both DAC '24 copyright block; consistent) | No: stopped |
| P033 | Partially verified (version of record not reachable) | arXiv 2409.01089v1 with final ACM TECS citation (23(4), Article 60) + earlier author manuscript (consistent) | No: stopped |
| P013 Tables 4-5 | Unresolved: no visual inspection possible; text layer inconsistent | UTS OPUS publisher PDF (text layer only) | No: `accuracy_metrics` stays blank |

P002 and P013 relevance were reassessed as peripheral/contextual (not core). This is proposed and requires researcher approval; no schema or `audit_report.csv` change was made.

---

## Step 9.2 — full-text evidence collection (2026-10-03, Claude Code)

_Evidence collection only. `papers.csv` was not modified, no relevance class was changed, and no gap analysis was done. Evidence: [`fulltext_evidence_report.md`](fulltext_evidence_report.md); proposed changes: [`fulltext_conflicts.md`](fulltext_conflicts.md); field tables: [`fulltext_verification_template.md`](fulltext_verification_template.md)._

The relevance classes used to build the queue are **proposed auditor classifications** from `audit_report.csv`, not approved classes.

### Summary

| Measure | Value |
| :-- | :-- |
| Papers attempted | 18 (17 proposed class-A papers + P013, proposed class D) |
| Fully verified | 6: P002, P013, P015, P016, P020, P034 |
| Partially verified | 4: P011, P029, P031 (arXiv preprints), P033 (arXiv copy in journal layout, version not confirmed) |
| Abstract only (subscription; no legitimate open copy) | 4: P018, P019, P022, P023 |
| Inaccessible from this environment (open copy exists) | 4: P001, P007, P017, P032 |
| Blocked in total | 8 |
| Characteristic-field conflict rows | 108 (90 resolve `Unknown`; 17 ambiguous, current value kept; 1 insufficient evidence; **0 contradict a current Yes/No value**) |
| Free-text conflict rows | 15 metric rows; 37 metadata rows |
| Papers additionally queued | None. P045/P046 were not examined (no full text was opened for them in this step), so no confidence-gating observation is recorded. |

"Fully verified" means the whole text of the version of record (or a repository copy in the publisher's final layout) was read. "Partially verified" means the whole text was read, but only in a version that could not be confirmed as the version of record. A paper is never counted as verified from its abstract.

### Status by paper

| Paper | Step 9.2 status | Source used | Version | May differ from version of record |
| :-- | :-- | :-- | :-- | :-- |
| P001 | Blocked: inaccessible | none | - | - |
| P002 | Fully verified | PubMed Central PMC11014122 (full text) | Publisher version in PMC | No. Tables/figures not in the PMC text extraction |
| P007 | Blocked: inaccessible | none | - | - |
| P011 | Partially verified | arXiv 2407.11771v2 | Author preprint | Possibly; Information Fusion version not compared |
| P015 | Fully verified | PubMed Central PMC9378646 (full text) | Publisher version in PMC | No. Tables/figures/supplement not in the extraction |
| P016 | Fully verified | MDPI publisher PDF (mdpi-res.com) | Version of record | No |
| P017 | Blocked: inaccessible | none | - | - |
| P018 | Blocked: abstract only | none | - | - |
| P019 | Blocked: abstract only | none | - | - |
| P020 | Fully verified | MDPI publisher PDF (mdpi-res.com) | Version of record | No |
| P022 | Blocked: abstract only | none | - | - |
| P023 | Blocked: abstract only | none | - | - |
| P029 | Partially verified | arXiv 1810.10090v1 | Author preprint with MobiCom '18 permission block | Possibly; ACM version not compared |
| P031 | Partially verified | arXiv 2410.10847v1 | Author preprint with DAC '24 copyright block | Possibly; publisher version closed access |
| P032 | Blocked: inaccessible | none | - | - |
| P033 | Partially verified | arXiv 2409.01089v1 | arXiv copy in ACM TECS layout (60:1-60:31) | Unlikely, not confirmed |
| P034 | Fully verified | FH JOANNEUM ePUB repository PDF | IEEE TMC final layout, pp. 451-464, CC BY | Unlikely; OpenAlex labels the copy "submittedVersion" (label conflict noted) |
| P013 | Fully verified | UTS OPUS repository copy of the publisher PDF | Publisher PDF, pp. 1-9 | No |

### How the full texts were reached

- This environment's network policy blocks direct access to publisher sites (MDPI, Wiley, ScienceDirect, ACM, IEEE), arXiv, OpenAlex, Semantic Scholar and institutional repositories.
- Full texts were read through three services available in the session:
  - the PubMed Central full-text service (P002, P015);
  - the alphaXiv full-text service for arXiv papers (P011, P029, P031, P033);
  - the alphaXiv document reader for open-access PDFs on publisher or institutional hosts (P013, P016, P020, P034). It was also used for open-access location lookups.
- Bot checks (ScienceDirect, the KB/DiVA Anubis challenge) were not bypassed. No pirated or unauthorised repositories were used or searched.

### Version differences

- **Preprints only:** P011, P029 and P031 were read only as arXiv preprints. Compare them with the versions of record before any recoding.
- **P033:** the arXiv copy carries the ACM TECS journal layout and pagination. It was not compared with the ACM page.
- **P034:** the repository copy carries the IEEE TMC layout, pagination (pp. 451-464) and a CC BY licence line, but OpenAlex labels it "submittedVersion".
- **P002, P015:** PMC holds the version of record, but the text extraction used omits table bodies and figures. Evidence that exists only in tables or figures was not seen. For P015 this matters for `latency_evaluation` (Insufficient evidence).
- **P013:** some extracted cell values in Tables 4-5 look internally inconsistent. Check them visually in the PDF before recoding `accuracy_metrics`.

### Remaining blockers

1. **Inaccessible from this environment, open copy exists (4):**
   - **P001:** Wiley open access (CC BY-NC); `onlinelibrary.wiley.com/doi/pdfdirect/10.1002/stc.2751` could not be fetched;
   - **P007:** CC BY; `downloads.hindawi.com/journals/ace/2022/9221211.pdf` could not be fetched;
   - **P017:** gold open access; ScienceDirect PII S2351978918307820 could not be fetched;
   - **P032:** only open copy is the DiVA submitted version (urn:nbn:se:uu:diva-587035), behind an Anubis bot challenge.

   A normal browser session, or an environment whose network policy allows these hosts, should be enough. P032's DiVA copy is a submitted version.
2. **Abstract only (4):** P018, P019, P022, P023. These need institutional access, interlibrary loan or an author copy. This is a researcher action.
3. **Version-of-record checks:** P011, P029, P031 and P033 before their candidate changes are applied.
4. **Researcher decisions:** the 17 ambiguous characteristic rows in `fulltext_conflicts.md` §1, plus the P002 and P013 relevance observations (both not image-based). Themes:
   - stated-but-unmeasured on-device execution (P002);
   - industrial PCs as edge devices (P013);
   - vote/consistency gates as `confidence_gating` (P002, P013, P015);
   - timing without stated hardware (P002, P013);
   - remote LVLM explanations as `cloud` (P011);
   - energy profiled but not reported (P033);
   - whether Decision 3 or the §7.3 `No` rule applies once the full text shows no timing value (P011, P020);
   - stream-level window skipping as `adaptive_inference` (P002).
5. **Relevance classes** remain the auditor's proposal. Whether they become a schema column is still a researcher decision (Step 9.1).

### Relation to the earlier Step 9.2 attempt (commit `9643e43`)

An earlier Claude Code session pushed a Step 9.2 attempt as commit `9643e43` on the unmerged branch `claude/pocketinspect-agent-sync-a33d88`. That attempt read P001 and P007 from the Wiley HTML, and its CHANGELOG entry is dated 2026-10-04.

This step was redone independently on branch `claude/blissful-gauss-ub29pl`, starting from the Step 9.1 commit `b77072f`. The earlier attempt was used only as a checklist. Material differences:

- **P001, P007:** counted as blocked here, because the source could not be reached. The earlier evidence is not adopted.
- **P033:** counted as partially verified here (arXiv copy; version not confirmed), not fully verified.
- **P011 `cloud`:** Ambiguous here, not Confirmed Yes. GPT-4 Vision generates explanation text only; the inspection inference stays on the phone.
- **P011 `latency_evaluation`:** the Table 4 caption mentions running time, but no time values appear in the table read here.
- **P011 `accuracy_metrics`:** adds the Substation dataset mIoU (Table 6).
- **P002 `adaptive_inference`:** Ambiguous here, not Confirmed No (input-dependent sliding-window skipping). Also two new internal inconsistencies: threshold 12 vs 11 m/s², and accuracy gap 1% vs 0.4%.
- **P015 `latency_evaluation`:** marked Insufficient evidence, because figures and supplement were not visible.
- **P020 `latency_evaluation`:** flags the Decision 3 vs §7.3 `No`-rule question.
- **P033:** the 4.06x figure is an optimality gain, not an efficiency value.
- **P034:** adds ViT-Base and MobileNetV1 accuracy values; the page range is 451-464.
- **P031:** the satisfaction-rate gains are percentage points.
- **Dating:** this environment's date is 2026-10-03, earlier than the dates on the Step 9.1 and earlier Step 9.2 entries (2026-10-04).

---

## Step 9.1 — queue preparation (history, unchanged)

_Step 9.1, 2026-10-04. Preparation only: no full-text coding has started, and `papers.csv` is unchanged._

### Summary (Step 9.1)

| Measure | Value |
| :-- | :-- |
| Class-A papers | 17 (P001, P002, P007, P011, P015, P016, P017, P018, P019, P020, P022, P023, P029, P031, P032, P033, P034) |
| P013 | Queued, priority HIGH; audit class D (unchanged). Full text available via the UTS institutional repository |
| Papers in queue | 18 |
| Accessible full text (confirmed) | 12: 6 at the publisher (P001, P002, P007, P015, P016, P020) and 6 via an alternative legitimate source (P011, P029, P031, P033, P034, P013) |
| Requiring an alternative source | 6 (P011, P029, P031, P033, P034, P013) |
| Abstract only (subscription; no legitimate open copy found) | 4 (P018, P019, P022, P023) |
| Inaccessible from this environment (open copy listed but not confirmed) | 2 (P017, P032) |
| Full-text coding started | No |

### Accessibility by paper (Step 9.1)

| Paper | Status | Publisher / primary source | Alternative legitimate source |
| :-- | :-- | :-- | :-- |
| P001 | Full text available | Publisher (Wiley Online Library), open access CC BY-NC; full-text HTML confirmed in browser | — |
| P002 | Full text available | Publisher (MDPI Sensors), open access CC BY; full-text HTML confirmed in browser | PubMed Central PMC11014122 (page responded HTTP 200) |
| P007 | Full text available | Publisher (Wiley/Hindawi Advances in Civil Engineering), open access CC BY; full-text HTML confirmed in browser | — |
| P011 | Alternative legitimate source | Publisher (Elsevier Information Fusion) listed as open access CC BY-NC by OpenAlex, but ScienceDirect returned a bot check, so access was not confirmed | arXiv 2407.11771 (author preprint; same title and authors; PDF responded). May differ from the version of record |
| P015 | Full text available | Publisher (Nature Communications), open access CC BY; PDF responded | PubMed Central PMC9378646; Cambridge Apollo repository |
| P016 | Full text available | Publisher (MDPI Processes), open access CC BY; full-text HTML confirmed in browser | — |
| P017 | Inaccessible (from this environment) | Publisher (Elsevier Procedia Manufacturing) listed as gold open access CC BY-NC-ND by OpenAlex and Semantic Scholar; ScienceDirect bot check blocked confirmation. Likely readable in a normal browser | None found (arXiv exact-title search: no match) |
| P018 | Abstract only | Publisher (Springer IJAMT) subscription; abstract on landing page | None found (OpenAlex closed; arXiv exact-title search: no match; Semantic Scholar: no open PDF) |
| P019 | Abstract only | Publisher (Elsevier Materials Today: Proceedings) subscription | None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF) |
| P020 | Full text available | Publisher (MDPI Applied System Innovation), open access CC BY; full-text HTML confirmed in browser | — |
| P022 | Abstract only | Publisher (Emerald Rapid Prototyping Journal) subscription | None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF) |
| P023 | Abstract only | Publisher (Elsevier Manufacturing Letters) subscription | None found (OpenAlex closed; arXiv: no match; Semantic Scholar: no open PDF) |
| P029 | Alternative legitimate source | Publisher (ACM MobiCom) listed as open access by OpenAlex; ACM returned a bot check, not confirmed | arXiv 1810.10090 (same title; PDF responded). May differ from the version of record |
| P031 | Alternative legitimate source | Publisher (ACM/IEEE DAC 2024) closed per OpenAlex | arXiv 2410.10847 (same title and 8 authors; PDF responded). May differ from the version of record |
| P032 | Inaccessible (from this environment) | Publisher (ACM TECS) closed; OpenAlex lists a green copy in the Uppsala DiVA repository (urn:nbn:se:uu:diva-587035) | DiVA record did not respond from this environment (connection failed; browser navigation refused). Needs a manual check |
| P033 | Alternative legitimate source | Publisher (ACM TECS) listed as open access CC BY by OpenAlex; ACM returned a bot check, not confirmed | arXiv 2409.01089 (same title; PDF responded). May differ from the version of record |
| P034 | Alternative legitimate source | Publisher (IEEE TMC) listed as open access CC BY by OpenAlex; IEEE Xplore page not confirmed automatically | FH JOANNEUM ePUB repository (submitted version, CC BY; PDF responded) |
| P013 | Alternative legitimate source | Publisher (Elsevier Advanced Engineering Informatics) listed as open access CC BY-NC-ND by OpenAlex; ScienceDirect bot check, not confirmed | UTS institutional repository hdl:10453/147577 (hosts the publisher PDF of the article; PDF responded) |

**How accessibility was checked (2026-10-04).**
- Open-access status and locations came from OpenAlex; Semantic Scholar `openAccessPdf` was used for closed papers.
- Preprints were looked up only by exact title (or OpenAlex-linked ID) on arXiv. No new literature discovery was done.
- A source counts as "confirmed" when its PDF responded, or when the full-text HTML loaded in the browser with section headings beyond the abstract. Only the headings were read, not the article text.
- ScienceDirect, ACM and some MDPI/Wiley PDF links return bot checks to automated requests. Bot checks were not bypassed. Where a publisher page could not be confirmed, the paper is listed under its confirmed alternative or as not confirmed.
- No pirated sources were used or searched.

### Immediate blockers (Step 9.1)

1. **Four papers are abstract-only:** P018, P019, P022 and P023, all class A (3D-print inspection). Full text needs institutional access, interlibrary loan or an author copy. These are researcher actions.
2. **Two papers are not confirmed:**
   - **P017:** gold open access per OpenAlex/Semantic Scholar, but ScienceDirect's bot check blocked confirmation. A manual browser check is probably enough.
   - **P032:** the only open copy is in the Uppsala DiVA repository, which did not respond from this environment. Needs a manual check or institutional access.
3. **Preprint versus version of record.** For P011, P029, P031 and P033 the confirmed copy is an arXiv preprint, and for P034 a submitted version. The verifier must record which version was used and flag differences that affect coding.
4. **Relevance class is not in `papers.csv`.** The queue uses the audit proposal in `audit_report.csv`. It is not known whether those A–E classes were formally approved. **Researcher decision:** approve the classes and decide whether they should become a schema column.
5. **P002 modality.** Publisher section headings (seen while checking access) mention vibration sensors and a 1D-CNN. If the system is not camera-based, its class-A status may need review. Only the researcher can change the class.
