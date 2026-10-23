# M2 AI Trend Intelligence Engine: Signal Schema Specification

**Author:** Senior Labour-Market Data Engineer, AI Trend Research Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9A Data Foundation & Evidence Architecture  
**Schema Version:** 1.0.0  

---

## 1. Schema Design Principles

Every dynamic signal extracted for M2 must adhere strictly to the following architectural tenets:
1. **Explicit Provenance:** Every signal record directly links to an identifiable source, publisher, publication date, retrieval timestamp, and citation reference.
2. **Temporal Modeling:** Signals are time-aware, containing both effective observation dates (`source_date`), validity intervals (`valid_from`, `valid_to`), and computed freshness age (`freshness_days`).
3. **Decomposed Nature:** Signals represent single, unweighted dimensions of labour demand, skill demand, AI exposure, augmentation, or research momentum. Fused scores are prohibited at this stage.
4. **Idempotent Identification:** `signal_id` is generated deterministically from source, entity type, entity ID, and signal type to guarantee deduplication upon re-ingestion.

---

## 2. Field-by-Field Specification

| Field Name | Type | Constraints / Allowed Values | Description |
| :--- | :--- | :--- | :--- |
| `signal_id` | String | Format: `SIG-{ENTITY}-{ID}-{TYPE}-{HASH}` | Unique deterministic primary key. |
| `entity_type` | String | `skill` \| `occupation` \| `task` \| `sector` | Granularity level of the entity observed. |
| `entity_id` | String | Non-empty string | Canonical ID of the entity (e.g. `2512`, `ai_literacy`). |
| `signal_type` | String | Enum (see Section 3) | Decomposed signal dimension. |
| `signal_value_raw` | String | Non-empty text | Unaltered, human-readable observation or metric string. |
| `signal_value_normalized`| Float | Bounded range: `[0.0, 1.0]` | Statistically normalized, bounded score. |
| `direction` | String | Enum (see Section 4) | Directional momentum classification. |
| `source_id` | String | Valid foreign key to Manifest | Originating data source identifier. |
| `source_date` | String | ISO 8601: `YYYY-MM-DD` | Publication or survey date of the source data. |
| `retrieved_at` | String | ISO 8601 UTC timestamp | Exact timestamp when the record was ingested. |
| `valid_from` | String | ISO 8601: `YYYY-MM-DD` | Start of temporal validity. |
| `valid_to` | String | ISO 8601: `YYYY-MM-DD` | Expiration or expected review date. |
| `geography` | String | ISO 3166-1 alpha-3: `MYS` \| `GLO` | Geographic applicability scope. |
| `sector` | String | String or `null` | Economic sector or industry cluster. |
| `occupation_code` | String | String or `null` | 4-digit MASCO 2020 or major group code. |
| `evidence_text` | String | Minimum length: 15 characters | Verbatim evidence, survey summary, or rationale. |
| `evidence_reference` | String | Minimum length: 5 characters | Specific publication, report section, table, or API ID. |
| `confidence` | Float | Bounded range: `[0.0, 1.0]` | Objective evidence-quality score based on tier authority. |
| `quality_tier` | String | `TIER_A` \| `TIER_B` \| `TIER_C` \| `TIER_D` | Authority tier of the source. |
| `freshness_days` | Integer | $\ge 0$ | Age in days from `source_date` to `reference_date`. |
| `freshness_category` | String | `FRESH` \| `ACCEPTABLE` \| `ARCHIVAL_VALID` \| `STALE` | Staleness evaluation. |
| `evidence_family` | String | Upper snake_case string | Deduplication family for source independence checks. |
| `parent_source` | String | Non-empty string | Parent statutory body or publishing organization. |
| `publisher_family` | String | `GOVERNMENT_MALAYSIA` \| `UNITED_NATIONS` \| `OPEN_RESEARCH_INFRASTRUCTURE` | Top-level publisher authority grouping. |

---

## 3. Allowed `signal_type` Values

1. `DEMAND_SHORTAGE`: Empirical evidence of occupational or skill shortage from employer surveys (e.g., TalentCorp MyCOL).
2. `EMPLOYMENT_LEVEL`: Macroeconomic or sectoral employment magnitude and participation statistics (e.g., OpenDOSM).
3. `WAGE_LEVEL`: Median and mean wage levels by occupation, sector, or skill tier (e.g., OpenDOSM).
4. `WAGE_GROWTH`: Longitudinal wage momentum or CAGR.
5. `AI_EXPOSURE`: Task-level exposure to AI models without declaring displacement (e.g., ILO Working Paper 96).
6. `AUTOMATION_EXPOSURE`: Proportion of routine cognitive or manual tasks directly substitutable by AI automation.
7. `AUGMENTATION_POTENTIAL`: Proportion of tasks where AI complements, accelerates, or enhances human output.
8. `RESEARCH_ACTIVITY`: Cumulative peer-reviewed research publication volume (e.g., OpenAlex).
9. `RESEARCH_GROWTH`: Velocity ratio comparing recent publication activity (2024–2026) to historical baseline (2020–2023).
10. `EMERGING_ROLE`: Formal classification as a newly created occupational role in workforce impact studies.
11. `DECLINING_ROLE`: Formal classification as a structurally consolidating or declining occupational role.
12. `FUTURE_SKILL`: Technical or soft skill identified as an emerging prerequisite in workforce studies.
13. `POLICY_PRIORITY`: Statutory, regulatory, or strategic national priority (e.g., MOSTI AIGE, Bursa ESG, NSS).
14. `GREEN_TRANSITION`: Specific alignment with decarbonisation, renewable energy, and circular economy agendas.
15. `DIGITAL_TRANSITION`: Specific alignment with cloud modernization, enterprise automation, and AI integration.

---

## 4. Allowed `direction` Values

- `STRONGLY RISING`: Longitudinal momentum $\ge +25\%$ or persistent statutory critical status across $\ge 75\%$ of evaluated periods.
- `RISING`: Longitudinal momentum between $+10\%$ and $+25\%$, newly critical status, or steady research growth.
- `STABLE`: Balanced indicators ($\Delta \in [-10\%, +10\%]$) or steady baseline demand.
- `MIXED / UNCERTAIN`: Conflicting cross-source signals (e.g. high exposure but simultaneous talent shortage).
- `DECLINING`: Structural task contraction or displacement by automated systems ($-10\%$ to $-25\%$).
- `STRONGLY DECLINING`: Severe task obsolescence or formal phase-out classification ($< -25\%$).

---

## 5. Sample Signal Records

### 5.1. Occupational Demand Shortage Signal (TalentCorp MyCOL)
```json
{
  "signal_id": "SIG-OCC-2512-DEMAND-7a2e5d99b1a0",
  "entity_type": "occupation",
  "entity_id": "2512",
  "signal_type": "DEMAND_SHORTAGE",
  "signal_value_raw": "Critical in 8/8 editions (Status: PERSISTENT_CRITICAL)",
  "signal_value_normalized": 1.0,
  "direction": "STRONGLY RISING",
  "source_id": "SRC-MYCOL-2024",
  "source_date": "2024-11-01",
  "retrieved_at": "2026-10-23T06:31:02.123456Z",
  "valid_from": "2024-11-01",
  "valid_to": "2025-12-31",
  "geography": "MYS",
  "sector": "Information and Communication Technology (ICT)",
  "occupation_code": "2512",
  "evidence_text": "Intense shortage of experienced developers skilled in cloud microservices, REST APIs, and automated CI/CD pipelines; severe cross-border brain drain to Singapore and remote overseas employers.",
  "evidence_reference": "TalentCorp MyMahir Critical Occupations List (2015-2025), MASCO 2512: Software Developers",
  "confidence": 0.95,
  "quality_tier": "TIER_A",
  "freshness_days": 722,
  "freshness_category": "FRESH",
  "evidence_family": "TALENTCORP_MYCOL",
  "parent_source": "TalentCorp Malaysia & ILMIA",
  "publisher_family": "GOVERNMENT_MALAYSIA"
}
```

### 5.2. AI Augmentation Potential Signal (ILO Working Paper 96)
```json
{
  "signal_id": "SIG-OCC-2512-AUGMEN-4c81f3d2e091",
  "entity_type": "occupation",
  "entity_id": "2512",
  "signal_type": "AUGMENTATION_POTENTIAL",
  "signal_value_raw": "Augmentation Potential: 0.48",
  "signal_value_normalized": 0.48,
  "direction": "STRONGLY RISING",
  "source_id": "SRC-ILO-GENAI-2023",
  "source_date": "2023-08-21",
  "retrieved_at": "2026-10-23T06:31:02.123456Z",
  "valid_from": "2023-08-21",
  "valid_to": "2027-12-31",
  "geography": "GLO",
  "sector": "Cross-Industry",
  "occupation_code": "2512",
  "evidence_text": "Key augmented tasks: Code generation and auto-completion, Unit test scaffolding, API documentation generation, Bug diagnostics.",
  "evidence_reference": "ILO Working Paper 96, ISCO 251 -> MASCO 2512",
  "confidence": 0.88,
  "quality_tier": "TIER_B",
  "freshness_days": 1159,
  "freshness_category": "ARCHIVAL_VALID",
  "evidence_family": "ILO_GENAI_STUDY",
  "parent_source": "International Labour Organization",
  "publisher_family": "UNITED_NATIONS"
}
```

### 5.3. Research Growth Momentum Signal (OpenAlex)
```json
{
  "signal_id": "SIG-SKI-rag_knowledg-RESEAR-9f123a48e7bc",
  "entity_type": "skill",
  "entity_id": "rag_knowledge_systems",
  "signal_type": "RESEARCH_GROWTH",
  "signal_value_raw": "Growth Velocity Ratio: 1.85x (Recent Share: 58.2%)",
  "signal_value_normalized": 0.925,
  "direction": "STRONGLY RISING",
  "source_id": "SRC-OPENALEX-TEMPORAL",
  "source_date": "2026-10-21",
  "retrieved_at": "2026-10-23T06:31:02.123456Z",
  "valid_from": "2024-01-01",
  "valid_to": "2026-12-31",
  "geography": "GLO",
  "sector": "Academic & Industrial R&D",
  "occupation_code": null,
  "evidence_text": "58.2% of all publications for rag_knowledge_systems appeared in the 2024-2026 window, demonstrating SURGING_MOMENTUM.",
  "evidence_reference": "OpenAlex Temporal Momentum Series, Topic: rag_knowledge_systems",
  "confidence": 0.85,
  "quality_tier": "TIER_C",
  "freshness_days": 2,
  "freshness_category": "FRESH",
  "evidence_family": "OPENALEX_SCHOLARLY",
  "parent_source": "OurResearch OpenAlex API",
  "publisher_family": "OPEN_RESEARCH_INFRASTRUCTURE"
}
```
