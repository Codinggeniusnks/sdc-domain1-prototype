# System Interface Specification: M2 (AI Trend Intelligence Engine) $\rightarrow$ M3 (Role Matching)

**Author:** Senior Labour-Market Data Engineer, AI Trend Research Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9A Data Foundation & Evidence Architecture  
**Interface Version:** 1.0.0  

---

## 1. Architectural Scope & Future Stage Boundaries

### Responsibility Split:
- **M2 (This Engine):** Responsible for multi-source evidence acquisition, normalization, freshness tracking, longitudinal shortage tracking, and decomposed signal delivery.
- **M3 (Future Role Matching Engine):** Responsible for matching user skill profiles to target occupations, calculating role suitability distances, and ranking career pathways.
- **Strict Boundary:** M3 logic (e.g. cosine similarity matching, vacancy distance ranking, recommendation engines) MUST NOT be implemented in Stage 9A.

---

## 2. Data Shape Contract (M2 $\rightarrow$ M3)

M2 provides M3 with pre-computed, decomposed occupational and skill vectors:

### 2.1. Occupational Profile Payload

```json
{
  "masco_code": "2512",
  "canonical_title": "Software Developers",
  "major_group": "2",
  "dosm_wage_category": "professionals",
  "median_monthly_wage_myr": 5400,
  "demand_signals": {
    "mycol_persistence_score": 1.0,
    "mycol_status": "PERSISTENT_CRITICAL",
    "editions_critical_count": 8,
    "is_critical_2024_2025": true,
    "direction": "STRONGLY RISING",
    "evidence_confidence": 0.95
  },
  "ai_disruption_profile": {
    "ilo_overall_exposure": 0.54,
    "ilo_augmentation_potential": 0.48,
    "ilo_automation_exposure": 0.06,
    "primary_mode": "AUGMENTATION_DOMINATED",
    "impact_classification": "HIGHLY_IMPACTED_ROLE",
    "time_horizon": "Immediate (0-12 months)"
  },
  "macroeconomic_context": {
    "national_unemployment_rate": 3.3,
    "national_employment_vitality_score": 0.90,
    "sectoral_employment_share_pct": 18.5
  },
  "policy_priority_weight": 0.90,
  "required_core_skills": [
    "python_scripting",
    "api_integration",
    "sql_data_analysis",
    "workflow_automation"
  ],
  "emerging_future_skills": [
    "prompt_engineering",
    "rag_knowledge_systems",
    "human_in_the_loop_qa"
  ],
  "provenance_citations": [
    "TalentCorp MyMahir MyCOL (2015-2025), MASCO 2512",
    "TalentCorp Impact Study 2024, Chapter 4, p. 72",
    "ILO Working Paper 96 (2023), ISCO 251",
    "OpenDOSM Salaries & Wages Survey (2023)"
  ]
}
```

---

## 3. Scenario Readiness & Hooks for M6 (Scenario Modelling)

M2 data structures are designed to allow future simulation models (M6) to inject exogenous technological assumptions **without altering underlying empirical baseline records**:

### Separation of Observed Evidence from Scenario Assumptions:
1. **Observed Baseline:** Real-world signals stored in `trend_signals_v1.json` remain immutable empirical records.
2. **Scenario Multiplier Hooks:** M3 receives parametric scaling coefficients from M6:
   - Scenario A: `MODERATE_AI_DISRUPTION`
     - $\text{EffectiveAutomation} = \text{ilo\_automation\_exposure} \times 1.0$
     - $\text{EffectiveAugmentation} = \text{ilo\_augmentation\_potential} \times 1.0$
   - Scenario B: `FAST_AGENTIC_AI_DISRUPTION`
     - $\text{EffectiveAutomation} = \min(1.0, \text{ilo\_automation\_exposure} \times 1.6)$
     - $\text{EffectiveAugmentation} = \min(1.0, \text{ilo\_augmentation\_potential} \times 1.3)$
     - Accelerated displacement multiplier applied specifically to routine clerical and bookkeeping occupations (`masco_code` in `["4110", "4311"]`).

By exposing clean, unweighted task parameters (`ilo_automation_exposure` and `ilo_augmentation_potential`), M2 enables M3 and M6 to model dynamic labor shifts without data fabrication.
