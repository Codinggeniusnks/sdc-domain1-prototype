# System Interface Specification: M1 (Skills Extraction) $\rightarrow$ M2 (AI Trend Intelligence Engine)

**Author:** Senior Labour-Market Data Engineer, AI Trend Research Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9A Data Foundation & Evidence Architecture  
**Interface Version:** 1.0.0  

---

## 1. Architectural Boundary & Governance

### Status of M1:
- M1 Skills Extraction is **FORMALLY CONCLUDED** (`PROMOTE WITH LIMITATIONS`).
- Frozen model: `H_blend_0.70A_0.30C1_W1.0` (Stored in `runpod/models/skills_predictor_v5_final/`).
- M1 thresholds: Core threshold $\tau_{\text{core}} = 0.50$, Suggested range $\tau_{\text{sugg}} \in [0.25, 0.50)$.
- **Strict Prohibition:** M2 MUST NOT retrain M1, alter M1 decision thresholds, reopen Protocol B or Protocol C v2, or alter Dataset v5.

### Decoupling Principle:
M1 and M2 communicate strictly through a **stateless, schema-validated API payload**. M2 does not inspect M1 feature vectors, model weights, or TF-IDF pipelines; it receives extracted canonical skill identifiers and returns dated, attributed trend intelligence.

---

## 2. Interface Contract

### 2.1. Request Payload (M1 $\rightarrow$ M2)

M1 supplies extracted and confirmed skills along with extraction confidence and tier classification:

```json
{
  "request_id": "REQ-M1-M2-20261023-001",
  "timestamp": "2026-10-23T14:30:00Z",
  "user_context": {
    "profile_id": "USER-MY-0421",
    "declared_occupation_masco": "2512",
    "years_experience": 4
  },
  "extracted_skills": [
    {
      "skill_id": "python_scripting",
      "canonical_name": "Python Scripting & Data Automation",
      "m1_confidence": 0.88,
      "tier": "CORE"
    },
    {
      "skill_id": "api_integration",
      "canonical_name": "REST API Integration & Resilient Fallbacks",
      "m1_confidence": 0.74,
      "tier": "CORE"
    },
    {
      "skill_id": "sql_data_analysis",
      "canonical_name": "SQL & Structured Data Analysis",
      "m1_confidence": 0.65,
      "tier": "CORE"
    },
    {
      "skill_id": "prompt_engineering",
      "canonical_name": "Structured Prompting & Context Engineering",
      "m1_confidence": 0.42,
      "tier": "SUGGESTED"
    }
  ]
}
```

---

### 2.2. Response Payload (M2 $\rightarrow$ M1 / Product UI)

For every skill provided, M2 returns decomposed trend evidence, directional momentum, exposure indicators, and provenance citations:

```json
{
  "response_id": "RESP-M2-20261023-001",
  "request_id": "REQ-M1-M2-20261023-001",
  "reference_date": "2026-10-23",
  "skill_trend_intelligence": [
    {
      "skill_id": "python_scripting",
      "canonical_name": "Python Scripting & Data Automation",
      "overall_direction": "RISING",
      "momentum_tier": "HIGH_MOMENTUM",
      "evidence_confidence": 0.94,
      "decomposed_signals": {
        "demand_shortage": {
          "status": "CRITICAL_SHORTAGE",
          "persistence_score": 1.0,
          "source": "TalentCorp MyCOL (2015-2025)",
          "freshness_days": 722
        },
        "ai_impact": {
          "mode": "AUGMENTATION_DOMINATED",
          "augmentation_potential": 0.48,
          "automation_exposure": 0.06,
          "source": "ILO Working Paper 96",
          "freshness_days": 1159
        },
        "research_momentum": {
          "velocity_ratio": 1.45,
          "recent_publication_share": 0.48,
          "source": "OpenAlex Scholarly Corpus",
          "freshness_days": 2
        },
        "policy_priority": {
          "status": "NATIONAL_PRIORITY",
          "mandate": "National Semiconductor Strategy (NSS) & MyDIGITAL",
          "source": "MITI / MDEC",
          "freshness_days": 764
        }
      },
      "explanation_text": "Python scripting demand is sustained by persistent shortages across Malaysian software development and semiconductor testing (MyCOL 8/8 editions), complemented by high AI code-generation augmentation (ILO) and national semiconductor reskilling priority (MITI NSS).",
      "primary_sources": [
        "TalentCorp MyCOL 2024/2025",
        "ILO Working Paper 96 (2023)",
        "MITI National Semiconductor Strategy (2024)"
      ],
      "last_updated": "2026-10-23T06:31:02Z"
    }
  ]
}
```

---

## 3. Data Integrity & Backward Compatibility

1. **Non-Breaking Schema:** If M1 extracts a skill that has zero research papers in OpenAlex, M2 returns the Malaysian authoritative and policy signals gracefully, marking research momentum as `INSUFFICIENT_EVIDENCE` rather than failing.
2. **Unmapped Skill Fallback:** If M1 passes a Level 2 expanded skill (e.g. `BPMN Modeling`), M2 uses `skill_source_crosswalk.json` to resolve it to `process_mapping` while preserving the specific domain context.
3. **Audit Trail:** Every response contains an immutable `response_id` referencing the exact `retrieved_at` timestamp of the underlying `trend_signals_v1.json` artifact.
