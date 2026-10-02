# Full-Text Verification Status

## Step 9.2 update (2026-10-04)

_Evidence collection only. `papers.csv` unchanged; relevance classes unchanged; no gap analysis._

| Measure | Value |
| :-- | :-- |
| Papers attempted | 18 (17 proposed class A + P013) |
| Fully verified (version of record or journal-formatted copy read) | 9: P001, P002, P007, P015, P016, P020, P033, P034, P013 |
| Partially verified (full text read, but only a preprint version was available) | 3: P011, P029, P031 |
| Abstract-only papers (blocked) | 4: P018, P019, P022, P023 |
| Inaccessible papers (blocked) | 2: P017, P032 |
| Total blocked | 6 |
| Conflict rows | 146 (see `fulltext_conflicts.md`) |

"Fully verified" means the full text was examined for all 15 coded fields and 11 contextual items. It does **not** mean every field was resolved: Ambiguous rows remain and need researcher decisions.

### Version differences

| Paper | Version used | Note |
| :-- | :-- | :-- |
| P001 | Publisher version of record (Struct. Control Health Monit. 28(7) e2751; HTML) | No (version of record) |
| P002 | Publisher version of record (Sensors 24(7):2099; HTML) | No (version of record) |
| P007 | Publisher version of record (Adv. Civil Eng. 2022, 9221211; HTML) | No (version of record) |
| P011 | Author preprint (arXiv v2); published version is Information Fusion 2025 (10.1016/j.inffus.2024.102782) | Possibly; preprint not compared with the version of record (ScienceDirect bot check) |
| P015 | Publisher version of record (Nat. Commun. 13:4654, 2022) | No (version of record) |
| P016 | Publisher version of record (Processes 8(11):1464; HTML) | No (version of record) |
| P020 | Publisher version of record (ASI 4(2):34; HTML) | No (version of record) |
| P029 | Author preprint carrying the MobiCom 2018 ACM copyright block; not confirmed identical to the ACM version of record | Possibly; not compared (ACM bot check) |
| P031 | Author preprint carrying the DAC 2024 ACM copyright block; publisher version is closed access | Possibly; not compared (closed access) |
| P033 | Copy formatted as the published article (ACM TECS 23(4), Article 60, June 2024; pages 60:1-60:xx) | Unlikely (journal layout), but not formally confirmed against the ACM page |
| P034 | Copy with IEEE TMC 25(1), Jan 2026 journal pagination (pp. 451-463); OpenAlex labels this repository copy "submittedVersion" | Unlikely (journal layout), label conflict noted |
| P013 | Publisher version of record PDF (Adv. Eng. Inform. 45 (2020) 101101; CC BY-NC-ND) | No (publisher PDF) |

### Remaining blockers

1. **Abstract only (subscription): P018, P019, P022, P023.** Full text needs institutional access, interlibrary loan or an author copy. This is a researcher action.
2. **P017:** gold open access per OpenAlex and Semantic Scholar, but ScienceDirect served a bot check. Not bypassed; a manual browser check is needed.
3. **P032:** the only open copy is in the Uppsala DiVA repository, which is unreachable from this environment (network connection failed; browser navigation refused). Needs a manual check or institutional access.
4. **Preprint-only verification (P011, P029, P031):** the publisher versions were not compared. A later check against the versions of record is recommended before recoding.
5. **Open definition questions**, now with full-text cases:
   - industrial PCs as `edge_device` (P013);
   - design-time selection under a timing constraint as `resource_awareness` (P013);
   - vote or consistency gates as `confidence_gating` (P002, P013, P015);
   - timing reported without stated hardware (P002, P011).
6. **Relevance:** P002 and P013 are not image-based. Their class decisions are the researcher's.

---

## Step 9.1 status (historical, 2026-10-04)

_Step 9.1, 2026-10-04. Preparation only: no full-text coding has started, and `papers.csv` is unchanged._

## Summary

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

## Accessibility by paper

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

## Immediate blockers

1. **Four papers are abstract-only:** P018, P019, P022 and P023, all class A (3D-print inspection). Full text needs institutional access, interlibrary loan or an author copy. These are researcher actions.
2. **Two papers are not confirmed:**
   - **P017:** gold open access per OpenAlex/Semantic Scholar, but ScienceDirect's bot check blocked confirmation. A manual browser check is probably enough.
   - **P032:** the only open copy is in the Uppsala DiVA repository, which did not respond from this environment. Needs a manual check or institutional access.
3. **Preprint versus version of record.** For P011, P029, P031 and P033 the confirmed copy is an arXiv preprint, and for P034 a submitted version. The verifier must record which version was used and flag differences that affect coding.
4. **Relevance class is not in `papers.csv`.** The queue uses the audit proposal in `audit_report.csv`. It is not known whether those A–E classes were formally approved. **Researcher decision:** approve the classes and decide whether they should become a schema column.
5. **P002 modality.** Publisher section headings (seen while checking access) mention vibration sensors and a 1D-CNN. If the system is not camera-based, its class-A status may need review. Only the researcher can change the class.
