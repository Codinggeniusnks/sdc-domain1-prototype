# M3 Explainability Architecture & Traceability Examples

**Version**: M3 v1.0.0  
**Interface**: `engine.explain_role_match(profile, masco_code, scenario_id)`  
**Audit Purpose**: Verifying that every recommendation output is mathematically auditable, evidence-grounded, and non-black-box.  
**Date**: 2026-10-23  

---

## 1. Explainability Contract & Decomposed Dimensions

In compliance with competition guidelines, M3 never outputs a single uninterpreted recommendation score. Every query to `explain_role_match` decomposes the outcome into six explicit dimensions:

1. **Role Match Index & Confidence Tier**: Numerical alignment ($0–100$) and categorical confidence.
2. **Skill Alignment Rationale**: Exact percentage of weighted skill overlap and core requirement coverage.
3. **Contributing Competencies**: Verified skills in the worker's profile that contributed positively.
4. **Skill Gap Diagnostics**: Missing core, important, and supporting competencies categorized by urgency.
5. **Labor & Scenario Influence Decomposition**: Explicit breakdown of how much M2 shortage and M6 AI foresight modified the score.
6. **Statutory & Research Citations**: Direct source citations (TalentCorp, MyCOL, ILO, ESCO, Bursa Malaysia).

---

## 2. Concrete Traceability Examples

### Example 1: High Confidence Match (Persona 2 $\rightarrow$ MASCO 2512 Software Developers)

```json
{
  "masco_code": "2512",
  "occupation_title": "Software Developers",
  "scenario_id": "REFERENCE_2026",
  "role_match_index": 85.3,
  "recommendation_confidence": "HIGH CONFIDENCE FIT",
  "rank": 1,
  "why_matched": "The worker demonstrates 81.6% weighted skill alignment with Software Developers, covering 2/2 core requirements (100.0%). Transition distance is classified as SHORT TRANSITION.",
  "contributing_skills": [
    "Python Scripting",
    "Api Integration",
    "Workflow Automation",
    "Rag Knowledge Systems"
  ],
  "missing_core_skills": ["None"],
  "transition_distance": "SHORT TRANSITION",
  "m2_labor_influence": "Empirical labour shortage is 89.6/100 (confidence: HIGH, damping: 1.0x) based on MyCOL and OpenDOSM evidence.",
  "m6_scenario_influence": "Under REFERENCE_2026, scenario outlook is 'STRONGLY RESILIENT' with reskilling urgency 'LOW', contributing 92.5/100.",
  "evidence_citations": {
    "source_ids": ["TALENTCORP_IMPACT_2024_CH4", "MYCOL_2024_2025_ICT", "ESCO_2512", "MASCO_2020_2512"],
    "evidence_quote": "TalentCorp Impact Study 2024 Chapter 4 (p. 58) highlights software developers transitioning into enterprise API integration and Python scripting, while MyCOL 2024/2025 classifies 2512 as critical shortage.",
    "source_dates": ["2024-11", "2024-05", "2020"]
  },
  "applied_guardrails": [],
  "disclaimer": "DISCLAIMER: ROLE MATCH INDEX IS AN EXPLAINABLE ALIGNMENT METRIC — NOT A HIRING DECISION OR PROBABILITY OF EMPLOYMENT"
}
```

---

### Example 2: Clerical-to-Analytical Transition (Persona 7 $\rightarrow$ MASCO 2511 Systems Analysts)

```json
{
  "masco_code": "2511",
  "occupation_title": "Systems Analysts",
  "scenario_id": "FAST_AGENTIC",
  "role_match_index": 69.9,
  "recommendation_confidence": "MODERATE FIT WITH GAP",
  "rank": 2,
  "why_matched": "The worker demonstrates 60.5% weighted skill alignment with Systems Analysts, covering 2/2 core requirements (100.0%). Transition distance is classified as MODERATE TRANSITION.",
  "contributing_skills": [
    "Process Mapping",
    "Workflow Automation",
    "Sql Data Analysis"
  ],
  "missing_core_skills": ["None"],
  "missing_important_skills": [
    "Api Integration",
    "Stakeholder Communication"
  ],
  "transition_distance": "MODERATE TRANSITION",
  "m2_labor_influence": "Empirical labour shortage is 89.6/100 (confidence: HIGH, damping: 1.0x) based on MyCOL and OpenDOSM evidence.",
  "m6_scenario_influence": "Under FAST_AGENTIC, scenario outlook is 'HIGH TRANSFORMATION ADVANTAGE' with reskilling urgency 'HIGH', contributing 88.4/100.",
  "evidence_citations": {
    "source_ids": ["TALENTCORP_IMPACT_2024_CH4", "MYCOL_2024_2025_ICT", "ESCO_2511", "MASCO_2020_2511"],
    "evidence_quote": "TalentCorp Impact Study 2024 Chapter 4 (p. 64) emphasizes Agentic Workflow Orchestration and process mapping for systems analysts.",
    "source_dates": ["2024-11", "2024-05", "2020"]
  },
  "applied_guardrails": [],
  "disclaimer": "DISCLAIMER: ROLE MATCH INDEX IS AN EXPLAINABLE ALIGNMENT METRIC — NOT A HIRING DECISION OR PROBABILITY OF EMPLOYMENT"
}
```

---

### Example 3: Zero-Overlap Guardrail Enforced (Persona 5 $\rightarrow$ MASCO 2512 Software Developers)

```json
{
  "masco_code": "2512",
  "occupation_title": "Software Developers",
  "scenario_id": "REFERENCE_2026",
  "role_match_index": 15.0,
  "recommendation_confidence": "DISTANT TRANSITION",
  "rank": 19,
  "why_matched": "The worker demonstrates 0.0% weighted skill alignment with Software Developers, covering 0/2 core requirements (0.0%). Transition distance is classified as LONG TRANSITION.",
  "contributing_skills": ["None"],
  "missing_core_skills": [
    "Python Scripting",
    "Api Integration"
  ],
  "transition_distance": "LONG TRANSITION",
  "m2_labor_influence": "Empirical labour shortage is 89.6/100 (confidence: HIGH, damping: 1.0x) based on MyCOL and OpenDOSM evidence.",
  "m6_scenario_influence": "Under REFERENCE_2026, scenario outlook is 'STRONGLY RESILIENT' with reskilling urgency 'LOW', contributing 92.5/100.",
  "evidence_citations": {
    "source_ids": ["TALENTCORP_IMPACT_2024_CH4", "MYCOL_2024_2025_ICT", "ESCO_2512", "MASCO_2020_2512"],
    "evidence_quote": "TalentCorp Impact Study 2024 Chapter 4 (p. 58) highlights software developers transitioning into enterprise API integration and Python scripting, while MyCOL 2024/2025 classifies 2512 as critical shortage.",
    "source_dates": ["2024-11", "2024-05", "2020"]
  },
  "applied_guardrails": [
    "ZERO_OVERLAP_CLAMPED_LE_15"
  ],
  "disclaimer": "DISCLAIMER: ROLE MATCH INDEX IS AN EXPLAINABLE ALIGNMENT METRIC — NOT A HIRING DECISION OR PROBABILITY OF EMPLOYMENT"
}
```

**Key Takeaway**: Despite Software Developers possessing the highest M2 shortage (89.6) and M6 scenario resilience (92.5) in the catalog, **the Zero-Overlap Guardrail clamps the final index strictly to 15.0**, preventing any spurious recommendation to a worker with zero software skills.
