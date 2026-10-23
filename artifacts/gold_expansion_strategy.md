# Strategic Gold Data Expansion Plan: Scaling Real Occupational Ground Truth

## Executive Summary
Stage 7B screening definitively established that data scarcity—specifically the reliance on only **98 Gold records** across 16 multi-label classes—is the primary bottleneck capping predictive generalisation.

This strategy outlines the systematic expansion of the real-world training corpus from **98 to $\ge 300$ authoritative Gold records**, targeting high-priority weak classes identified during forensic screening, with primary emphasis on native Malaysian labour market sources.

---

## 1. Class-Targeted Acquisition Priorities

```
                        Gold Data Acquisition Hierarchy
                                       │
      ┌────────────────────────────────┼───────────────────────────────┐
      ▼                                ▼                               ▼
  P0 Gaps (Critical)            P1 Gaps (Moderate)              P2 Gaps (Scaling)
  - data_privacy_pdpa           - instructional_design          - rag_knowledge_systems
  - process_mapping             - semiconductor automation      - prompt_engineering
  - esg_sustainability          - clerical/BPO digitization     - python_scripting
  Target: +75 positives         - finance / FinTech             - ai_literacy
                                Target: +80 positives           Target: +60 positives
```

### 1.1 Priority P0 Data Gaps (Severe Screening Bottlenecks)

1. **`data_privacy_pdpa`** (Current Support: 35 | Standalone Candidate A Recall: 48.6%)
   - **Target Positives**: $+25$ authoritative examples.
   - **Preferred Sources**: Malaysian Department of Personal Data Protection (JPDP) official compliance handbooks, enterprise Data Protection Officer (DPO) job specs, ISO/IEC 27701 privacy information management standards.
   - **Malaysia Relevance**: Malaysian Personal Data Protection Act (PDPA 2010), 2024 PDPA amendments (mandatory data breach notifications, data protection officers).
   - **Expected Impact**: Eliminates false negatives on privacy compliance tasks; grounds the model in Malaysian legal standards.

2. **`process_mapping`** (Current Support: 50 | Standalone Candidate A Precision: 38.8%)
   - **Target Positives**: $+25$ authoritative examples.
   - **Preferred Sources**: Lean Six Sigma project charters, Business Process Model and Notation (BPMN) documentation, Malaysian shared services SOPs.
   - **Malaysia Relevance**: Operational excellence frameworks across multinational Global Business Services (GBS) hubs in Cyberjaya, Bangsar South, and Penang.
   - **Expected Impact**: Teaches the classifier to distinguish rigorous workflow mapping from generic casual mentions of "business process".

3. **`esg_sustainability_reporting`** (Current Support: 48 | Standalone Candidate A Recall: 56.3%)
   - **Target Positives**: $+25$ authoritative examples.
   - **Preferred Sources**: Bursa Malaysia Sustainability Reporting Guidelines (4th Edition), FTSE4Good Bursa Malaysia disclosures, GHG Protocol corporate standards.
   - **Malaysia Relevance**: Mandatory ESG reporting for Main and ACE Market listed issuers; National Energy Transition Roadmap (NETR) green jobs.
   - **Expected Impact**: Elevates F1 from 0.4615 to $>0.65$; captures carbon accounting and sustainability disclosure phrasings.

---

### 1.2 Priority P1 Data Gaps (Moderate Weaknesses & Industrial Transitions)

4. **`instructional_design`** (Current Support: 44 | Precision: 46.2%)
   - **Target Positives**: $+20$ examples.
   - **Sources**: HRD Corp e-LATiH syllabus frameworks, National Occupational Skills Standards (NOSS) under Jabatan Pembangunan Kemahiran (JPK).
   - **Impact**: Grounds adult learning design and digital curriculum development.

5. **`workflow_automation` (Semiconductor / E&E Focus)** (Current Support: 36)
   - **Target Positives**: $+20$ examples.
   - **Sources**: Malaysian Investment Development Authority (MIDA) E&E workforce reports, factory automation task sheets from Penang / Kulim Hi-Tech Park manufacturers.
   - **Impact**: Enhances recognition of SCADA/PLC to modern RPA/AI pipeline automation.

6. **`human_in_the_loop_qa` & `sql_data_analysis` (Clerical / BPO Modernization)**
   - **Target Positives**: $+20$ examples.
   - **Sources**: Digital Global Business Services Council Malaysia (GBS Malaysia) competency frameworks, data mart operational manuals.
   - **Impact**: Provides training signal for clerical workers transitioning to AI validation roles.

7. **`finance / FinTech` (Digital Banking & Algorithmic Finance)**
   - **Target Positives**: $+20$ examples.
   - **Sources**: Bank Negara Malaysia (BNM) Digital Banking Framework competencies, FinTech Association of Malaysia reports.
   - **Impact**: Captures automated fraud detection, algorithmic risk, and digital KYC tasks.

---

### 1.3 Priority P2 Data Gaps (Scaling Established Domains)

8. **`rag_knowledge_systems`, `prompt_engineering`, `python_scripting`, `ai_literacy`**
   - **Target Positives**: $+15$ examples each.
   - **Sources**: OpenAlex peer-reviewed abstracts (2024–2026), arXiv applied ML papers.
   - **Impact**: Maintains cutting-edge technical vocabulary coverage.

---

## 2. Malaysian Authoritative Ingestion Channels

To maintain high data integrity, ingestion must prioritize official public databases and structured open government datasets over uncontrolled scraping:

| Source Category | Organization / Entity | Ingestion Mechanism | Target Volume | Legal / Technical Status |
|---|---|---|---|---|
| **MASCO 2020** | MOHR / DOSM | OpenDOSM API & Official 4-Digit PDF Catalogs | 60 unit groups | Public domain open data |
| **TalentCorp MyCOL** | Ministry of Human Resources | Critical Occupations List Annual Reports (PDF) | 50 profiles | Official public government report |
| **Bursa Malaysia** | Bursa Malaysia Berhad | Public Listed Company ESG Disclosures & Guides | 40 extracts | Public regulatory guidelines |
| **HRD Corp** | Pembangunan Sumber Manusia | Public e-LATiH Course Metadata & Curricula | 30 profiles | Public educational standards |
| **ESCO v1.2** | European Commission | ESCO API / Downloadable RDF/CSV Data | 70 profiles | Open access CC BY 4.0 |
| **OpenAlex** | OurResearch | OpenAlex Scholarly REST API | 50 abstracts | CC0 Public Domain API |

**Security Gate**: Web scraping of protected, authenticated, or paywalled job boards is **strictly forbidden**. Only open government data, open-access APIs, and official public publications may be ingested.

---

## 3. Class Balance Target: The Rule of $\ge 20$

In multi-label classification evaluated via 5-fold grouped cross-validation, a class must have sufficient positive representation across folds to prevent fold starvation:

- **Mathematical Requirement**:
  To guarantee that every validation fold receives at least $3$ to $5$ genuine Gold positive instances (allowing stable F1 and recall computation without zero-division anomalies), every skill class must achieve:
  $$\mathbf{N_{\text{gold}}(k) \ge 20 \text{ independent authoritative records}}$$
- **Current Deficit**:
  Currently, several classes rely on as few as 8–12 real Gold instances in training, with the remainder filled by synthetic templates. The expansion must satisfy the $\ge 20$ Gold floor for all 16 skills.

---

## 4. Future Synthetic Data Policy: Class-Conditional Pruning

Synthetic data provided indispensable structural support during early stages (doubling Macro F1 from 0.2898 to 0.6530). However, as Gold data scales, synthetic data must be phased down to prevent synthetic template bias.

### 4.1 The Class-Conditional Augmentation Formula
$$\text{Synthetic Records for Skill } k = \max\left(0, 30 - N_{\text{gold}}(k)\right)$$

### 4.2 Phased Transition Milestones
1. **Current Phase ($N=348$)**: 98 Gold (28%) + 250 Synthetic (72%). Necessary to prevent class starvation.
2. **Intermediate Phase ($N \approx 320$)**: 220 Gold (69%) + 100 Synthetic (31%). Synthetic support pruned from well-represented classes (e.g. `prompt_engineering`, `python_scripting`).
3. **Mature Phase ($N \ge 350$)**: $\ge 300$ Gold ($\ge 85\%$) + $\le 50$ Synthetic ($\le 15\%$). Synthetic data retained solely for rare edge-case stress testing and minority class balancing.

---

## 5. Leakage Prevention Protocol

Before any new Gold or Silver record is accepted into the training corpus:
1. **Deduplication Check**: Must have 0 exact string match and 0 normalized token overlap with:
   - Protocol B (`data/splits/real_world_test_set.json`)
   - Protocol C v2 (`data/splits/unseen_occupation_test_set_v2.json`)
2. **Cosine Similarity Screening**: TF-IDF cosine similarity against any Protocol B/C v2 sample must be strictly $< 0.50$.
3. **Occupation Group Exclusion**: Any record belonging to the 25 MASCO unit groups quarantined in Protocol C v2 (e.g., 1330, 2149, 2151, 2166, 2411, 2413) is **automatically rejected**.
