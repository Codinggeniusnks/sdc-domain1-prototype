# M2 AI Trend Intelligence Engine: Explainability & Citation Traceability Examples

**Author:** Senior Labour-Market Quantitative Researcher & Explainable-AI Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9B Explainable M2 Trend Scoring Engine  
**Implementation:** `src/trend_engine.py` (`explain_trend()` function)  

---

## 1. Overview of the Explainability Architecture

M2 produces human- and machine-readable explanations for every outlook classification. It strictly forbids ungrounded assertions. Every explanation is structured with:
- **Title & Code:** Canonical identifier and official name.
- **Overall Outlook & Confidence:** Classified trend state and confidence index.
- **Top Positive Drivers:** Specific empirical factors accelerating demand or productivity, each linked to exact source citations.
- **Top Negative Drivers:** Specific automation risks or contraction indicators with exact citations.
- **Uncertainties & Boundary Conditions:** Methodological caveats, data divergence, or measurement gaps.
- **Quality Flags:** Data density or latency alerts.

---

## 2. Example 1: Strongly Rising Role with High AI Exposure (Software Developers — MASCO 2512)

```json
{
  "entity_id": "2512",
  "title_or_name": "Software Developers",
  "overall_outlook": "STRONGLY RISING",
  "confidence": "HIGH (100.0/100)",
  "top_positive_drivers": [
    {
      "signal_id": "SIG-MYCOL-2512",
      "source_id": "SRC-MYCOL-2024",
      "publisher": "TalentCorp Malaysia & ILMIA",
      "source_date": "2024-11-01",
      "evidence_reference": "TalentCorp Critical Occupations List, MASCO 2512",
      "summary": "Identified as critical in 8/8 editions (Status: PERSISTENT_CRITICAL). Severe domestic talent deficit exacerbated by cross-border brain drain to Singapore and remote global employers."
    },
    {
      "signal_id": "SIG-ILO-AUG-2512",
      "source_id": "SRC-ILO-WP96",
      "publisher": "International Labour Organization",
      "source_date": "2023-08-01",
      "evidence_reference": "ILO Working Paper 96, ISCO 251",
      "summary": "High augmentation potential of 48.0% across software architecture, API design, and system debugging tasks, where Generative AI acts as a developer copilot."
    },
    {
      "signal_id": "SIG-POL-POL-MITI-NSS-2024-2512",
      "source_id": "POL-MITI-NSS-2024",
      "publisher": "Ministry of Investment, Trade and Industry (MITI)",
      "source_date": "2024-05-28",
      "evidence_reference": "MITI National Semiconductor Strategy (NSS), Pillar 2 (Talent Development)",
      "summary": "National policy mandate: National Semiconductor Strategy (NSS) targeting MASCO 2512 to supply 60,000 high-skilled engineers."
    }
  ],
  "top_negative_drivers": [
    {
      "signal_id": "SIG-ILO-AUTO-2512",
      "source_id": "SRC-ILO-WP96",
      "publisher": "International Labour Organization",
      "source_date": "2023-08-01",
      "evidence_reference": "ILO Working Paper 96, ISCO 251",
      "summary": "Automation potential of 6.0% affecting routine boilerplate code generation and standard template test writing."
    }
  ],
  "uncertainties": [
    "Direct academic research momentum not evaluated at occupational level (measured via underlying skills)."
  ],
  "quality_flags": [],
  "last_updated": "2026-10-23T07:00:17.123456+00:00"
}
```

### Explanatory Analysis:
Notice how the M2 engine resolves the "Exposure vs. Decline" paradox. Although Software Developers experience substantial AI exposure ($54.0/100$), its augmentation potential ($48.0/100$) dwarfs its automation vulnerability ($6.0/100$), and employer shortage remains persistent across all 8 MyCOL editions. The engine correctly classifies this occupation as **STRONGLY RISING**.

---

## 2. Example 2: Strongly Declining Role (General Office Clerks — MASCO 4110)

```json
{
  "entity_id": "4110",
  "title_or_name": "General Office Clerks",
  "overall_outlook": "STRONGLY DECLINING",
  "confidence": "HIGH (90.0/100)",
  "top_positive_drivers": [
    {
      "signal_id": "SIG-ILO-AUG-4110",
      "source_id": "SRC-ILO-WP96",
      "publisher": "International Labour Organization",
      "source_date": "2023-08-01",
      "evidence_reference": "ILO Working Paper 96, ISCO 411",
      "summary": "Low augmentation potential of 8.0% for basic scheduling and text synthesis assistance."
    }
  ],
  "top_negative_drivers": [
    {
      "signal_id": "SIG-ILO-AUTO-4110",
      "source_id": "SRC-ILO-WP96",
      "publisher": "International Labour Organization",
      "source_date": "2023-08-01",
      "evidence_reference": "ILO Working Paper 96, ISCO 411",
      "summary": "High automation potential of 28.0% affecting document filing, standardized data entry, and routine administrative transcription."
    },
    {
      "signal_id": "SIG-MYCOL-DROP-4110",
      "source_id": "SRC-MYCOL-2024",
      "publisher": "TalentCorp Malaysia & ILMIA",
      "source_date": "2024-11-01",
      "evidence_reference": "TalentCorp MyCOL 2024/2025 Edition Exclusions, MASCO 4110",
      "summary": "Dropped from latest national Critical Occupations List due to easing shortage and widespread enterprise software automation."
    }
  ],
  "uncertainties": [
    "Direct academic research momentum not evaluated at occupational level (measured via underlying skills)."
  ],
  "quality_flags": [],
  "last_updated": "2026-10-23T07:00:17.123456+00:00"
}
```

### Explanatory Analysis:
In direct contrast to software engineering, General Office Clerks exhibit an automation potential ($28.0\%$) that is $3.5\times$ higher than its augmentation potential ($8.0\%$). Coupled with its exclusion from MyCOL and below-average wage growth ($2.2\%$ CAGR in OpenDOSM), the engine deterministically assigns **STRONGLY DECLINING**.

---

## 3. Example 3: Newly Critical Role with Surging Momentum (Environmental Engineers — MASCO 2143)

```json
{
  "entity_id": "2143",
  "title_or_name": "Environmental Engineers",
  "overall_outlook": "STRONGLY RISING",
  "confidence": "HIGH (90.0/100)",
  "top_positive_drivers": [
    {
      "signal_id": "SIG-MYCOL-2143",
      "source_id": "SRC-MYCOL-2024",
      "publisher": "TalentCorp Malaysia & ILMIA",
      "source_date": "2024-11-01",
      "evidence_reference": "TalentCorp Critical Occupations List, MASCO 2143",
      "summary": "Identified as newly critical in 2022/2023 and 2024/2025 editions (Status: NEWLY_CRITICAL). Surge driven by corporate carbon accounting and ESG disclosures."
    },
    {
      "signal_id": "SIG-POL-POL-BURSA-ESG-2024-2143",
      "source_id": "POL-BURSA-ESG-2024",
      "publisher": "Bursa Malaysia & Securities Commission",
      "source_date": "2024-03-01",
      "evidence_reference": "Bursa Malaysia Enhanced Sustainability Reporting Framework, Chapter 9",
      "summary": "National policy mandate: Mandatory ESG Scope 1, 2, and 3 disclosures for all Main Market public listed companies."
    }
  ],
  "top_negative_drivers": [],
  "uncertainties": [
    "Historical shortage persistence is low (2/8 editions) due to recent emergence; momentum is surging rather than long-term steady state."
  ],
  "quality_flags": [],
  "last_updated": "2026-10-23T07:00:17.123456+00:00"
}
```

### Explanatory Analysis:
This case demonstrates the "Level vs. Momentum" separation. Because Environmental Engineers only emerged in the 2022/23 and 2024/25 editions, their cumulative persistence score is moderate ($2/8 = 25.0\%$, index: $60.0$). However, their demand momentum index is surging at $88.0/100$. The engine captures both dimensions honestly without averaging them away.

---

## 4. Example 4: Statutory Mandate Skill (Data Privacy & Malaysian PDPA Compliance — `data_privacy_pdpa`)

```json
{
  "entity_id": "data_privacy_pdpa",
  "title_or_name": "Data Privacy & Malaysian PDPA Compliance",
  "overall_outlook": "STRONGLY RISING",
  "confidence": "HIGH (100.0/100)",
  "top_positive_drivers": [
    {
      "signal_id": "SIG-POL-POL-JPDP-PDPA-2024-data_privacy_pdpa",
      "source_id": "POL-JPDP-PDPA-2024",
      "publisher": "Department of Personal Data Protection (JPDP) & Parliament of Malaysia",
      "source_date": "2024-07-31",
      "evidence_reference": "Personal Data Protection (Amendment) Act 2024 (Act A1720), Gazetted August 2024",
      "summary": "National policy mandate (ENACTED_LEGISLATION): Mandatory Data Protection Officer (DPO) appointments, statutory 72-hour breach notification, and increased penalties up to RM1 million."
    },
    {
      "signal_id": "SIG-OALEX-data_privacy_pdpa",
      "source_id": "SRC-OPENALEX-2026",
      "publisher": "OurResearch (OpenAlex)",
      "source_date": "2026-10-23",
      "evidence_reference": "OpenAlex Works API, Concept: data_privacy_pdpa",
      "summary": "Publication velocity ratio of 5.8x across AI data sovereignty and cross-border transfer compliance."
    }
  ],
  "top_negative_drivers": [],
  "uncertainties": [],
  "quality_flags": [],
  "last_updated": "2026-10-23T07:00:17.123456+00:00"
}
```

### Explanatory Analysis:
The skill profile reflects enacted Malaysian legislation (`PDPA Amendment Act 2024`), giving it a `policy_priority_index` of $100.0$. The citation explicitly references the parliamentary act, gazette date, and regulatory provisions, demonstrating full provenance.
