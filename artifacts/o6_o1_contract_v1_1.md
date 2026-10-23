# Interface Contract Specification: O1 Ingestion -> O6 Aggregation (v1.1.0)

**Interface Direction:** Upstream (O1) to Downstream (O6)  
**Contract Version:** v1.1.0  
**Status:** READY FOR FUTURE O1 INTEGRATION

---

## 1. Input Profile Schema

O6 v1.1.0 accepts profiles structured as:
```json
{
  "cohort_id": "TECH_CORP_2026",
  "profiles": [
    {
      "profile_id": "SYN_PROF_001",
      "cohort_id": "TECH_CORP_2026",
      "region_id": "REGION_A",
      "current_role": {
        "masco_code": "2512",
        "role_title": "Software Developers"
      },
      "confirmed_skills": [
        "python_scripting",
        "api_integration"
      ],
      "target_role": {
        "masco_code": "2529",
        "role_title": "Database and Network Professionals NEC"
      },
      "reskilling_pathway": {
        "planned_skills": ["rag_knowledge_systems"],
        "core_gaps": ["rag_knowledge_systems"],
        "important_gaps": []
      }
    }
  ]
}
```

---

## 2. Validation & Quarantine Behavior

- If O1 passes records with `confirmed_skills: null`, O6 safely treats it as empty list.
- If O1 passes malformed records (e.g. non-dict, missing `profile_id`, empty `{}`), O6 quarantines them into `excluded_profiles_by_reason` and increments `excluded_profile_count`.
- Demographic variables remain strictly prohibited; any forbidden demographic key raises a runtime `ValueError`.
