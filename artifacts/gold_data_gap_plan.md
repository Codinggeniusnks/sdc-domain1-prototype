# Gold Data Gap Remediation & Scaling Plan

## Executive Summary
The independent forensic audit (`artifacts/opus_v4_independent_audit.md`) emphasized that the root bottleneck of the current model is **sample scarcity of genuine, high-quality, real-world data**.

Current training corpus (`data/processed/dataset_v4_clean_multisource.json`) composition:
- Total training records: **348**
- Gold (authoritative real sources): **98 (28.2%)**
- Synthetic (augmented templates): **250 (71.8%)**

While the remediated grouped 5-fold CV guarantees that every fold now contains 18 to 24 Gold validation records (eliminating the previous 0-Gold validation defect), expanding the absolute volume of Gold data is the single highest-ROI initiative for Domain 1.

---

## Target Data Acquisition Strategy

```
                          Target Gold Pipeline
                                   │
      ┌────────────────────────────┼───────────────────────────┐
      ▼                            ▼                           ▼
1. Academic / Scholarly    2. European Skills/Job     3. Malaysian National
   (OpenAlex Expansion)       (ESCO Mapping)             (MyCOL / MASCO / SOCSO)
   Target: +300 records       Target: +250 records       Target: +150 records
```

### 1. OpenAlex API Scholarly Extraction (+300 Records)
- **Scope**: AI/ML applications in traditional domains (agriculture, green economy, supply chain, legal tech, public health).
- **Target Concepts**:
  - `Process mining & workflow automation`
  - `Retrieval-Augmented Generation (RAG)`
  - `Algorithmic bias & AI governance`
  - `ESG carbon emissions accounting`
- **Quality Protocol**: Filter papers with $>10$ citations and verified abstract text. Programmatically tag skills via explicit phrase matching against the curated Domain 1 lexicon, followed by human-in-the-loop validation.

### 2. European Skills, Competences, Qualifications and Occupations (ESCO v1.2) (+250 Records)
- **Scope**: Extract granular occupational descriptions and associated essential skill relations.
- **Priority MASCO Alignments**:
  - MASCO Major Group 1: Managers (Operations, Supply Chain, IT Directors)
  - MASCO Major Group 2: Professionals (Software, Environmental, Legal, Financial)
  - MASCO Major Group 3: Technicians & Associate Professionals (Process Controllers, Data Clerks)
  - MASCO Major Group 4: Clerical Support Workers (Administrative & Back-Office)
- **Quality Protocol**: Direct extraction of ESCO `description` and `essential_skill` tags mapped to Domain 1 taxonomy.

### 3. Malaysian National Standards (+150 Records)
- **Scope**: Native Malaysian occupational frameworks:
  - **MyCOL** (Malaysian Skills Classification)
  - **MASCO 2020** unit group task descriptors
  - **HRD Corp** Critical Occupation List (MyCOL/HRDF)
  - **SOCSO** Employment Insurance System job vacancy descriptions
- **Quality Protocol**: Exact MASCO 4-digit code mapping, ensuring representation of Malaysia-specific workplace contexts (e.g., PDPA 2010 compliance, local industrial automation).

---

## Source Quality Tiering Framework

All prospective data must be ingested according to strict quality tiers:

| Tier | Definition | Allowed Weight ($w_i$) | Examples |
|---|---|---|---|
| **GOLD** | Authoritative standard, official regulatory profile, verified real vacancy | $3.0$ | MASCO 2020, ESCO, OpenAlex peer-reviewed abstracts |
| **SILVER** | Curated industry whitepapers, company tech blogs, conference talks | $2.0$ | Enterprise architecture case studies, vendor documentation |
| **BRONZE** | LLM-assisted synthetic generation with diversified structural framing | $1.0$ | Parameterized worker personas (strictly checked for template collision) |

---

## Leakage Prevention & Holdout Protection

To prevent repeating historical methodological invalidations:
1. **Deduplication Gate**: Every newly scraped record must undergo exact string deduplication, lowercased whitespace-normalized hashing, and TF-IDF cosine similarity screening against:
   - Protocol B (`data/splits/real_world_test_set.json`)
   - Protocol C v2 (`data/splits/unseen_occupation_test_set_v2.json`)
   - Existing training records
2. **Exclusion Rule**: Any candidate record exhibiting $> 0.60$ cosine similarity or matching the 4-digit MASCO unit groups of Protocol C v2 (e.g., 1330, 2149, 2151, 2166, 2411, 2413) is **automatically rejected** from the training pool.
