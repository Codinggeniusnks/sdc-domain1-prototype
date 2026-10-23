# Fairness Claims & Demographic Omission Review: O6 Engine

**Review Date:** 2026-10-24  
**Auditor:** Senior Responsible-AI & Fairness Auditor  
**Status:** MISLEADING CLAIM IDENTIFIED — DEFECT DEF-P2-01 LOGGED

---

## 1. Demographic Omission Audit

A forensic scan of `data/synthetic_workforce.json` and internal profile schemas in `src/sdg_aggregation_engine.py` was conducted to verify the absence of protected personal attributes.

### Verified Absence:
- `gender` / `sex`: **ABSENT**
- `race` / `ethnicity`: **ABSENT**
- `religion`: **ABSENT**
- `age` / `date_of_birth`: **ABSENT**
- `marital_status` / `dependents`: **ABSENT**
- `disability`: **ABSENT**

All synthetic records are defined purely by operational characteristics: `profile_id`, `cohort_id`, `region`, `current_role_id`, and `confirmed_skills`.

---

## 2. Review of Stage 14A Fairness Claims

In Stage 14A, the report asserted:
> *"Disparate Impact Ratio (DIR) ≡ 1.000 across all demographic categories because protected attributes are excluded."*

### Methodological Critique (Defect DEF-P2-01):
1. **Definition of Disparate Impact:**
   Disparate Impact Ratio (DIR) is defined under the EEOC Uniform Guidelines on Employee Selection Procedures as:
   $$DIR = \frac{\Pr(\hat{Y} = 1 \mid A = 0)}{\Pr(\hat{Y} = 1 \mid A = 1)}$$
   where $A \in \{0, 1\}$ represents membership in a protected demographic class.
2. **Mathematical Inapplicability:**
   When protected attribute $A$ is uncollected and absent, the probabilities $\Pr(\hat{Y} = 1 \mid A = a)$ cannot be estimated. Asserting that $DIR = 1.000$ implies empirical parity has been measured and verified, which is untrue.
3. **Correct Conceptual Classification:**
   The design implements **Fairness through Unawareness** (structural non-use). It does not guarantee demographic parity in practice because proxy variables (such as region or historical role) could theoretically correlate with demographics.
4. **Remediation:**
   Revoke the empirical claim `DIR ≡ 1.000`. Replace with explicit statement of structural demographic omission.
