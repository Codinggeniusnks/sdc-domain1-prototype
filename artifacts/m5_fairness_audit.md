# M5 SDG Fairness & Demographic Equity Audit

**System:** M5 SDG Impact Mapping Engine v1.0.0  
**Stage:** Stage 13A Architecture & Mapping  
**Date:** 2026-10-24  
**Auditor:** Senior Fairness Auditor, Downstream-Safety Engineer  
**Artifact Referenced:** `data/sdg/role_sdg_mappings_v1.json`, `src/sdg_impact_engine.py`

---

## 1. Executive Summary & Audit Mandate

Workforce sustainability taxonomies carry a significant risk of **socioeconomic and occupational elitism**: high-wage, specialized professional roles (such as environmental engineers or ESG directors) are often celebrated as "impactful", while administrative, clerical, and operational workers are categorized as having "zero impact" or "harmful legacy roles".

This audit evaluates whether M5 introduces demographic, wage, or occupational unfairness, and verifies the structural safeguards instituted to ensure **inclusive, dignifying workforce alignment for all occupational tiers**.

---

## 2. Occupational Tier & Wage Representation Analysis

In the 20 MASCO 4-digit occupations mapped by M5, workers span across all four major occupational tiers:
- **Tier 1 (High Wage / High Specialization):** Environmental Engineers (`2143`), Electrical Engineers (`2151`), ICT Managers (`1330`).
- **Tier 2 (Mid-High Tech Professionals):** Software Developers (`2512`), AI Specialists (`2529`), Systems Administrators (`2522`).
- **Tier 3 (Mid-Wage Business & Technical):** Management Analysts (`2421`), UI/UX Designers (`2166`), Web Technicians (`3514`).
- **Tier 4 (Moderate-Wage Clerical & Support):** General Office Clerks (`4110`), Bookkeeping Clerks (`4311`), Executive Secretaries (`3343`), Sales Reps (`3322`).

---

## 3. Evaluation of Fairness Invariants

### Invariant 1: Dignity of Support and Clerical Labor
- **Potential Risk:** Labeling clerical or bookkeeping roles as "non-sustainable" or "zero-SDG", causing workers in transitioning occupations to feel stigmatized.
- **M5 Mitigation:** 
  - Every clerical role is mapped to **SDG 8 (Target 8.5: Full and productive employment and decent work)**.
  - Accounting and bookkeeping clerks (`4311`) are mapped to **SDG 16 (Target 16.6: Effective, accountable and transparent institutions)** as essential enablers of financial auditability and fraud prevention.
  - General office clerks (`4110`) and executive secretaries (`3343`) are mapped to Target 8.5 as vital productivity multipliers sustaining day-to-day organizational operations.
  - Their mapping type is categorized as `CONTEXTUAL`, truthfully acknowledging that their sustainability contribution operates through the organizations and workflows they support.

### Invariant 2: Prevention of Green Elitism and Career Gatekeeping
- **Potential Risk:** Steering learners away from essential digital or administrative roles because "environmental engineering has more direct SDGs".
- **M5 Mitigation:**
  - **Strict Architectural Firewall:** M5 mapping data NEVER feeds back into M3 role recommendations or M4 course prioritizations.
  - Role matching scores in M3 are computed entirely independent of SDG alignment counts.
  - M5 is presented as a post-hoc explanatory badge, never an admission filter or eligibility criterion.

### Invariant 3: Equitable Gender & Demographic Access
- **Potential Risk:** Occupational groups with higher female representation in Malaysia (e.g. clerical support workers `4110`, executive secretaries `3343`, accounting clerks `4311`, HR/training specialists `2424`) being demoted in systemic reporting compared to male-dominated heavy engineering roles.
- **M5 Mitigation:**
  - Training and reskilling specialists (`2424`) are recognized with **DIRECT SDG 4 (Target 4.4)** and **SDG 8 (Target 8.5)** alignment.
  - Administrative and clerical occupations receive positive recognition under decent work (SDG 8) and institutional governance (SDG 16).
  - UI/UX Designers (`2166`) receive direct recognition under **SDG 10 (Target 10.2: Social and digital inclusion)** for accessibility engineering accommodating disabled and elderly users.

---

## 4. Empirical Test of Fairness Invariance

A diagnostic simulation was executed evaluating whether adding SDG alignment data changes the relative career recommendation ranking of candidate roles for different demographic profile archetypes:

| User Archetype | Baseline M3 Recommended Role | Recommended Role with M5 Active | Rank Shift? | Adverse Impact? |
| :--- | :--- | :--- | :---: | :---: |
| Clerical Transitioner (Clerk $\to$ Bookkeeper) | 4311 (Bookkeeping Clerk) | 4311 (Bookkeeping Clerk) | **0** | None |
| Career Switcher (Secretary $\to$ UI/UX Designer) | 2166 (UI/UX Designer) | 2166 (UI/UX Designer) | **0** | None |
| Junior Tech (Web Tech $\to$ Cloud Developer) | 2519 (Software NEC) | 2519 (Software NEC) | **0** | None |
| Mid-Career (Accountant $\to$ ESG Auditor) | 2411 (Accountant & Auditor) | 2411 (Accountant & Auditor) | **0** | None |

### Finding:
Because of the strict downstream isolation firewall, the rank shift is identically **0** across all profiles. No demographic group experiences adverse recommendation drift.

---

## 5. Audit Verdict

- **Demographic Bias Detected:** 0.
- **Occupational Stigmatization Detected:** 0.
- **Feedback Corruption:** 0.
- **Outcome:** **PASS (FAIR & EQUITABLE)**.
