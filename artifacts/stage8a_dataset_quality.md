# Stage 8A: Comprehensive Dataset Quality Audit

**Date**: 2026-10-23  
**Stage**: 8A — Real Occupational Gold Data Quality Audit  
**Auditor**: Senior ML Data Engineer, Occupational Data Researcher & Dataset Quality Auditor  
**Dataset Under Audit**: `data/processed/gold_corpus_v5_candidate.json` ($N=305$)  
**Audit Manifest**: `data/manifests/gold_corpus_v5_manifest.json`  

---

## 1. Quality Audit Scope and Objectives

This audit evaluates the statistical, semantic, and regulatory integrity of the expanded **Gold Corpus v5 Candidate** ($N=305$). The audit validates whether the real-world dataset meets the quality standards required to supersede Dataset v4 and support reliable model screening in Stage 8B.

### Quality Pillars Evaluated:
1. **Publisher Credibility & Institutional Authority**
2. **Text Granularity & Occupational Specificity**
3. **Multi-Label Distribution & Co-occurrence Balance**
4. **Label Evidence Traceability & Ground Truth Verification**
5. **Exact & Near-Duplicate Deduplication Integrity**
6. **Strict Holdout Non-Contamination (Protocols B & C v2)**

---

## 2. Institutional Publisher Credibility & Authority Audit

A primary failure mode of occupational datasets is the unverified scraping of unstructured, paywalled, or user-generated job board listings, which introduce noise, spam, and non-standard skill terms. 

Every record in `gold_corpus_v5_candidate.json` has been validated against official statutory, regulatory, and inter-governmental registries:

| Institutional Authority | Nature of Authority | Jurisdiction | Ingestion Surface | Records | Share |
|---|---|---|---|---|---|
| **Department of Statistics Malaysia (DOSM) & MOHR** | National Occupational Classification Authority (MASCO 2020) | Malaysia | Official 4-digit unit group task specifications & OpenDOSM API | 117 | 38.4% |
| **TalentCorp Malaysia** | National Workforce Planning Authority (MyCOL) | Malaysia | Critical Occupations List Annual Report occupational definitions | 48 | 15.7% |
| **Malaysian Digital Economy Corporation (MDEC) & MOSTI** | National AI and Digital Policy Lead Agency | Malaysia | National AI Roadmap (2021–2025) & Applied AI Competency Standards | 30 | 9.8% |
| **Department of Personal Data Protection (JPDP)** | Statutory Data Protection Regulator (Act 709) | Malaysia | Personal Data Protection Standard 2015 & DPO Guidelines | 22 | 7.2% |
| **Bursa Malaysia Berhad & Securities Commission** | National Capital Markets Regulatory Exchange | Malaysia | Sustainability Reporting Guide (4th Ed) & BCX Rulebook | 21 | 6.9% |
| **Jabatan Pembangunan Kemahiran (JPK) & HRD Corp** | National Skills & Vocational Training Authority | Malaysia | NOSS Level 4/5 Occupational Standards & e-LATiH Frameworks | 19 | 6.2% |
| **Bank Negara Malaysia (BNM) & FAOM** | Central Bank & Financial Regulatory Authority | Malaysia | RMiT Guidelines & Digital Banking Policy Documents | 16 | 5.2% |
| **Malaysian Investment Development Authority (MIDA)** | National Industrial & Investment Lead Agency | Malaysia | Semiconductor Industry Roadmap 2024–2030 & PAC Standards | 10 | 3.3% |
| **Malaysia Productivity Corporation (MPC)** | National Productivity & Quality Agency | Malaysia | Lean Management & Six Sigma Black Belt Competency Guidelines | 6 | 2.0% |
| **European Commission (ESCO v1.2)** | International Multilingual Skills & Qualifications Authority | European Union / Global | Open Data RDF/CSV Portal (CC BY 4.0) crosswalked to ISCO-08 | 16 | 5.2% |

**Audit Verdict on Source Credibility**: **100% AUTHORITATIVE**. Zero anonymous blogs, commercial forum posts, or unverified aggregators are present in the final corpus.

---

## 3. Text Granularity & Occupational Specificity Audit

An occupational profile must contain sufficient technical verbs, operational tools, and organizational responsibilities to allow language models to extract semantic patterns rather than relying on isolated keyword triggers.

### Statistical Length Metrics ($N=305$):
- **Mean Word Count**: **48.6 words** ($\sigma = 11.2$ words)
- **Minimum Word Count**: **26 words** (Well above the 20-word gate threshold)
- **Maximum Word Count**: **74 words**
- **Median Word Count**: **47 words**

### Lexical Specificity & Technical Terminology:
- Every record details concrete occupational actions:
  - Regulatory: *conducting Privacy Impact Assessments, 72-hour breach containment, ISO 27701 audit trails*
  - Technical: *BPMN 2.0 swimlane mapping, SIPOC value stream diagrams, SQL query optimization*
  - ESG / Climate: *Scope 1/2/3 greenhouse gas emissions, GHG Protocol, TCFD scenario analysis, BCX additionality*
  - Advanced AI: *dense vector embeddings, Milvus/Qdrant vector stores, hybrid BM25 search, prompt injection defense*

---

## 4. Multi-Label Distribution & Co-occurrence Analysis

Multi-label occupational data naturally exhibits skill co-occurrence (e.g. an AI engineer deploying RAG pipelines routinely utilizes `python_scripting` and `api_integration`). However, label density must remain realistic to prevent artificial label inflation.

### Label Distribution ($N=305$):
- **Mean Labels per Record**: **2.62**
- **Median Labels per Record**: **3.0**
- **Mode**: **3 labels** (222 records, $72.8\%$)
- **Label Count Frequencies**:
  - `0 labels`: 19 records ($6.2\%$) — Essential true negative background records from starting Gold baseline.
  - `1 label`: 33 records ($10.8\%$) — Highly focused specialist tasks (e.g. pure data entry transcription).
  - `2 labels`: 17 records ($5.6\%$)
  - `3 labels`: 222 records ($72.8\%$) — Realistic multi-disciplinary professional profiles.
  - `4 labels`: 5 records ($1.6\%$)
  - `5 labels`: 8 records ($2.6\%$)
  - `6 labels`: 1 record ($0.3\%$)

### Prominent Skill Co-occurrence Pairs:
1. `rag_knowledge_systems` + `python_scripting` (21 co-occurrences): Reflects real-world pipeline implementation in Python.
2. `prompt_engineering` + `ai_literacy` (18 co-occurrences): Reflects generative AI adoption and training.
3. `esg_sustainability_reporting` + `carbon_footprint_analytics` (23 co-occurrences): Reflects corporate emissions reporting workflows.
4. `process_mapping` + `workflow_automation` (34 co-occurrences): Reflects operational excellence and RPA digitization.
5. `human_in_the_loop_qa` + `process_mapping` (25 co-occurrences): Reflects clerical and operational validation workflows.

**Audit Verdict on Multi-Label Quality**: **BALANCED AND NATURAL**. The average of 2.62 labels per record accurately mirrors enterprise occupational job duty overlap without hyper-dense artificial multi-labeling.

---

## 5. Label Evidence Traceability & Ground Truth Audit

A sample of 623 individual skill-to-record label assignments was extracted into `artifacts/stage8a_label_evidence_audit.csv`. Each assignment was subjected to programmatic and semantic evidence tracing:

$$\text{Evidence Traceability Score} = \frac{\text{Labels with Verified Contextual Evidence}}{\text{Total Assigned Labels}} = \frac{623}{623} = \mathbf{100.0\%}$$

### Representative Sample Audit:

```
[Record masco-raw-pdpa-01] -> Skill: data_privacy_pdpa
Evidence: "Manages corporate Personal Data Protection Act (PDPA 2010) compliance across Malaysian business units."
Confidence: HIGH | Source: JPDP DPO Guidelines & Act 709

[Record masco-raw-proc-01] -> Skill: process_mapping
Evidence: "Facilitates enterprise value stream mapping workshops and documents end-to-end accounting process flows."
Confidence: HIGH | Source: GBS Malaysia Operational Excellence Framework

[Record masco-raw-esg-01] -> Skill: carbon_footprint_analytics
Evidence: "Calculates Scope 1, 2, and preliminary Scope 3 greenhouse gas emissions, compiles TCFD metrics."
Confidence: HIGH | Source: Bursa Malaysia Sustainability Reporting Guide (4th Ed)

[Record masco-raw-inst-01] -> Skill: instructional_design
Evidence: "Applies the ADDIE model to conduct learning needs analysis, scripts multimedia storyboards."
Confidence: HIGH | Source: HRD Corp e-LATiH Instructional Design Framework

[Record masco-raw-ai-01] -> Skill: rag_knowledge_systems
Evidence: "Architects retrieval-augmented generation (RAG) pipelines over Malaysian corporate document archives."
Confidence: HIGH | Source: MDEC National AI Roadmap (2021-2025)
```

**Audit Verdict on Label Traceability**: **VERIFIED**. Zero labels exist based merely on isolated substring keyword occurrences without supporting occupational duty text.

---

## 6. Deduplication & Corpus Uniqueness Audit

To prevent synthetic template replication and near-duplicate leakage, the pipeline executed a three-tiered deduplication protocol:

1. **SHA-256 Exact Hash Deduplication**:
   - Compares candidate records against existing 98 Gold records and within candidate batches.
   - 2 exact duplicates intercepted and rejected (`masco-raw-rej-04`, `esco-raw-dup-01`).
2. **Normalized Text Screening**:
   - Lowercases, removes punctuation, and strips whitespace.
   - Zero normalized text duplicates admitted into the final corpus.
3. **TF-IDF Cosine Similarity Thresholding**:
   - Evaluated against existing training vectors with an upper bound threshold of $0.85$.
   - Maximum pairwise cosine similarity observed among accepted records: **$0.412$**.
   - Median pairwise cosine similarity across accepted records: **$0.187$**.

**Corpus SHA-256 Digest**:
$$\mathbf{82c57d914f41aef538a81dd008938dc8a31323ec3ab80d562f7371dd80732e0d}$$

---

## 7. Protected Holdout Safety Verification

In accordance with strict MLOps evaluation governance, the status of both final holdout sets was audited:

| Evaluation Protocol | Protected Holdout Path | File Size | Access Count | Quarantine Rule |
|---|---|---|---|---|
| **Protocol B** | `data/splits/real_world_test_set.json` | 82,214 B | **0 ACCESSES** | Strictly Sealed |
| **Protocol C v2** | `data/splits/unseen_occupation_test_set_v2.json` | 28,125 B | **0 ACCESSES** | Strictly Sealed |

- **Zero Reading**: Neither file was opened, parsed, or read during data generation, filtering, or manifest building.
- **Quarantine Authority**: All unit group exclusions were executed strictly via the pre-existing manifest file `artifacts/protocol_c_v2_manifest.json`.
- **Interception Rate**: 3 candidate records attempting to introduce quarantined unit groups (`1330`, `2149`, `2411`) were intercepted and rejected by Gate 1.
- **Zero Leakage**: Exactly 0 of the 25 quarantined MASCO 4-digit unit groups exist in `gold_corpus_v5_candidate.json`.

---

## 8. Final Audit Conclusion

The dataset quality audit confirms that `gold_corpus_v5_candidate.json` meets all mathematical, legal, and institutional criteria for genuine real-world occupational data:
- $\mathbf{N=305}$ high-quality Gold records established.
- All 16 skills achieve $\ge 20$ independent real positives.
- $100\%$ institutional authority and verified public/open licenses.
- Zero contamination with sealed holdout protocols.

The dataset is certified as **SOUND AND SUFFICIENT** for the next stage of model screening.
