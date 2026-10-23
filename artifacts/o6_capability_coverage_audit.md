# Forensic Capability Coverage Audit: O6 Engine v1.0.0

**Review Date:** 2026-10-24  
**Auditor:** Senior Sustainability Aggregation Methodologist  
**Status:** FULL AUDIT PASS — NO INVERSION DETECTED

---

## 1. Objective of Capability Coverage

Capability Coverage measures the breadth of sustainability-relevant competencies present within a workforce cohort relative to the total known universe of skills mapped to a specific Sustainable Development Goal (SDG).

Unlike prevalence (which measures worker headcount participation), coverage measures organizational capability diversity.

---

## 2. Mathematical Definition & Inversion Check

### Formula Audit
$$CC(s) = \frac{|\mathcal{K}_{\mathcal{C}}(s)|}{|\mathcal{K}_{\text{total}}(s)|}$$

- **Numerator $|\mathcal{K}_{\mathcal{C}}(s)|$:** The count of unique skills present in the cohort's confirmed skill profiles that map to SDG $s$ under M5 v1.1.0.
- **Denominator $|\mathcal{K}_{\text{total}}(s)|$:** The total count of canonical skills in the frozen M5 taxonomy mapped to SDG $s$.

### Audit Questions:
1. **Is the metric inverted?**
   - Inverted definition would compute $\frac{\text{canonical total}}{\text{cohort unique}}$, leading to values $\ge 1.0$ or division-by-zero.
   - Code verification: Line 238 computes `len(cohort_skills_for_sdg) / len(total_m5_skills_for_sdg)`.
   - **Verdict:** `NOT INVERTED` (Correct).
2. **Is the metric strictly bounded?**
   - Since $\mathcal{K}_{\mathcal{C}}(s) \subseteq \mathcal{K}_{\text{total}}(s)$, $0 \le |\mathcal{K}_{\mathcal{C}}(s)| \le |\mathcal{K}_{\text{total}}(s)|$.
   - Thus, $0.0 \le CC(s) \le 1.0$.
   - **Verdict:** `BOUNDED` (Correct).

---

## 3. Role vs. Skill Isolation

A critical integrity requirement is that roles mapped to SDGs must NOT be counted as skills in the capability coverage numerator.
- Code verification (lines 142–165): The engine parses profile skills and current roles into distinct data structures: `profile_skills` and `profile_roles`.
- Capability coverage exclusively queries `profile_skills`.
- **Verdict:** `STRICTLY ISOLATED` (No role contamination).
