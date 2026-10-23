# Forensic Review: "CORE-First" Claim vs. Mathematical Truth

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py`  
**Date:** 2026-10-24  
**Audit Finding:** DEFECT P2-01 (DOCUMENTATION OVERSTATEMENT)  

---

## 1. Background & The Stage 15A Claim

Stage 15A documentation (`artifacts/o1_workforce_gap_methodology.md`, Section 2) asserted:
> *"CORE gap prevalence is structurally prioritised with the highest weight (0.35), ensuring that structural job requirements dominate elective reskilling."*

In colloquial technical prose, engineers often describe a component with the largest single weight ($w_1 = 0.35$) as "dominating" or "guaranteeing" precedence. However, in rigorous mathematical auditing, a weighted sum **never** guarantees structural precedence unless lexicographic ordering or non-linear gating is enforced.

---

## 2. Mathematical Counterexample Proof

To verify whether O1 v1.0.0 is structurally CORE-first, we evaluated the prompt's canonical adversarial pair:

### Skill X (Niche Skill with Rare CORE Gap):
- $\text{CORE prevalence} = 0.02$ (1 worker out of 50)
- $\text{IMPORTANT prevalence} = 0.00$
- $\text{Average deficit} = 0.40$
- $\text{Cross-role transferability} = 0.10$
- $\text{Scenario urgency} = 0.00$
- $\text{Prerequisite centrality} = 0.00$

$$P(C, X) = (0.35 \times 0.02 + 0.20 \times 0.00 + 0.15 \times 0.40 + 0.15 \times 0.10 + 0.10 \times 0.00 + 0.05 \times 0.00) \times 100$$
$$P(C, X) = (0.007 + 0.060 + 0.015) \times 100 = 8.20$$

### Skill Y (Universal Skill with Widespread IMPORTANT Gap):
- $\text{CORE prevalence} = 0.00$ (0 workers have a CORE requirement)
- $\text{IMPORTANT prevalence} = 0.80$ (40 workers out of 50 require it as an IMPORTANT capability)
- $\text{Average deficit} = 1.00$
- $\text{Cross-role transferability} = 1.00$ (required across all roles)
- $\text{Scenario urgency} = 1.00$ (critical under active scenario)
- $\text{Prerequisite centrality} = 1.00$ (core foundation for other tools)

$$P(C, Y) = (0.35 \times 0.00 + 0.20 \times 0.80 + 0.15 \times 1.00 + 0.15 \times 1.00 + 0.10 \times 1.00 + 0.05 \times 1.00) \times 100$$
$$P(C, Y) = (0.160 + 0.150 + 0.150 + 0.100 + 0.050) \times 100 = 61.00$$

### Empirical Outcome:
$$P(C, Y) = 61.00 \gg P(C, X) = 8.20$$
Skill Y outranks Skill X by **52.80 points**, despite having **zero** CORE gaps.

---

## 3. Classification Determination

Under Audit 14, the reviewer must classify the engine's behavior as exactly one of:
1. `STRUCTURALLY GUARANTEED`
2. `WEIGHTED PREFERENCE ONLY`
3. `NOT CORE-FIRST`

### Official Finding:
**`WEIGHTED PREFERENCE ONLY`**

The claim in Stage 15A documentation that CORE gaps are "structurally prioritised" is **OVERSTATED** and constitutes **Defect P2-01**.

---

## 4. Enterprise Workforce Analytics Perspective

Is `WEIGHTED PREFERENCE ONLY` a bug in the code, or a flaw in documentation?

In enterprise workforce planning and budget allocation, **weighted preference is vastly superior to structural lexicographic ordering**:
- If an organization has 50 employees, and exactly 1 employee needs a niche CORE skill while 40 employees desperately lack an IMPORTANT cross-functional data skill needed for daily operations, a rational Chief Human Resources Officer (CHRO) must prioritize training the 40 employees over the 1 employee.
- Absolute lexicographic CORE precedence would force enterprise training budgets to sponsor 1-person courses for minor core gaps while ignoring widespread organizational competency deficits.

### Remediation Directive:
Do **not** alter the weighted sum to enforce rigid lexicographic filtering. Instead, remediate the documentation:
1. Formally strike all claims of "structural guarantee" or "structural dominance".
2. Truthfully state: *"CORE gaps receive the largest single weight (0.35), establishing a strong weighted preference; however, widespread IMPORTANT gaps with high transferability and scenario urgency can legitimately and transparently outrank rare CORE gaps in cohort-level resource allocation."*
