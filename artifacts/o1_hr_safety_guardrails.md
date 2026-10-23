# O1 Responsible AI, Ethics & HR Decision Guardrails (v1.0.0)

**Policy Scope:** Anti-Surveillance, Decision Guardrails & Demographic Fairness  
**Status:** STRICT ETHICAL GUARDRAILS ENFORCED

---

## 1. Prohibited Uses & Automated Employment Decisions

O1 is engineered solely as a workforce capability planning instrument. The software payload explicitly embeds machine-readable prohibitions against using its outputs for:
1. `HIRING_DECISIONS`: Evaluating candidate resumes or suitability.
2. `TERMINATION_DECISIONS`: Identifying workers for retrenchment, redundancy, or layoff.
3. `PROMOTION_DECISIONS`: Ranking individuals for promotion eligibility.
4. `COMPENSATION_DECISIONS`: Setting wages, bonuses, or salary increases.
5. `DISCIPLINARY_DECISIONS`: Formal corrective action or punitive HR evaluation.
6. `INDIVIDUAL_PERFORMANCE_SCORING`: Evaluating past worker productivity.
7. `WORKER_SURVEILLANCE`: Tracking keystrokes, activity, or individual learning pace.

---

## 2. Anti-Ranking & Cohort-First Invariants

- **No Individual Ranking:** O1 never ranks employees against one another ("top employee", "lowest-value worker").
- **No Individual Deficit Tables in Employer Payloads:** Individual M4 reskilling pathways remain strictly learner-facing. Employer analytics receive aggregated cohort statistics only.
- **No Raw CV Exposure:** Unstructured CV and resume text is permanently excluded from ingestion and outputs.

---

## 3. Structural Non-Use & Fairness Transparency

- **Demographic Attributes Prohibited:** Demographic attributes (gender, age, ethnicity, religion, disability) are strictly banned from profile schemas.
- **Truthful Fairness Claims:**
  - `protected_attributes_used = False`
  - `demographic_fairness_evaluated = False`
  - O1 does NOT output Disparate Impact Ratios (DIR) or claim mathematical demographic parity, truthfully recognizing that blindness does not equate to empirical equity testing.
