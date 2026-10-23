# O1 Responsible AI & HR Decision Guardrails v1.1.0

**Reference Date:** 2026-10-24  
**Compliance Standard:** Enterprise Ethical AI, PDPA Malaysia 2010, EU AI Act High-Risk Employment Guardrails  

---

## 1. Prohibited Operational Uses

O1 v1.1.0 strictly prohibits and enforces runtime architectural blocks against using workforce gap outputs for:
1. Individual hiring or talent acquisition screening.
2. Worker termination, redundancy, or layoff selections.
3. Employee promotion, demotion, or career gatekeeping.
4. Individual performance appraisals or compensation adjustments.
5. Worker risk scoring, stack-ranking, or disciplinary proceedings.

---

## 2. Demographic Attribute Safeguards

- `protected_attributes_used: false`
- `demographic_fairness_evaluated: false`
- Profiles containing demographic attributes (`gender`, `age`, `race`, `religion`, `salary`, `marital_status`) are rejected at ingestion with `PROHIBITED_DEMOGRAPHIC_ATTRIBUTE`.
- Profiles containing unstructured CV narratives (`raw_cv`, `resume_text`) are excluded to prevent demographic proxy leakage.

---

## 3. Disclaimers & Non-Use Limitations

> **Mandatory Disclaimer:** The architectural exclusion of demographic attributes does **NOT** prove empirical demographic parity, nor does it guarantee the absence of historical societal proxies. O1 outputs are strictly limited to aggregate curriculum planning.
