# Forensic Capability Coverage Definition Consistency Audit (Stage 14E)

**Audit Date:** 2026-10-24  
**Auditor Roles:** Senior Reproducibility Auditor, Aggregation-Mathematics Reviewer, Responsible-AI Safety Engineer  
**Audit Scope:** Issue B Forensic Verification — SDG Capability Coverage Formula  
**Verdict:** `DOCUMENTATION-ONLY ERROR` (Production code verified implementing canonical cohort SDG coverage)

---

## 1. Issue B Problem Statement

Stage 14D report contained a typographical formula error in Section 2, Field 28:
$$\text{Coverage}(i, t) = \frac{|\text{ConfirmedSkills}(i) \cap \text{RequiredSkills}(t)|}{|\text{RequiredSkills}(t)|}$$
This formula represented individual role-to-target skill matching rather than cohort-level SDG capability coverage.

---

## 2. Actual Production Implementation Inspection (Check B1)

Inspection of `src/sdg_aggregation_engine.py` (lines 687–710) reveals the actual formula:
```python
# Metric D: Capability Coverage
# Role mappings must NOT enter skill capability-coverage numerator!
cohort_skills_present: Set[str] = set()
for p in eligible_profiles:
    cohort_skills_present.update(list(p.get("confirmed_skills") or []))
    if time_dim == "POST_PATHWAY":
        pw_skills = list(p.get("reskilling_pathway", {}).get("planned_skills") or [])
        cohort_skills_present.update(pw_skills)

capability_coverage = {}
for sdg_num in range(1, 18):
    canon_skills = self._canonical_sdg_skills[sdg_num]
    skills_held = sorted(list(canon_skills.intersection(cohort_skills_present)))
    total_canon = len(canon_skills)
    ratio = len(skills_held) / total_canon if total_canon > 0 else 0.0
    capability_coverage[f"SDG_{sdg_num}"] = {
        "sdg_id": sdg_num,
        "skills_present_in_cohort": skills_held,
        "skills_present_count": len(skills_held),
        "canonical_sdg_skills_total": total_canon,
        "capability_coverage_ratio": round(ratio, 4),
        "capability_coverage_percentage": round(ratio * 100, 2)
    }
```

### Mathematical Formulation:
For each SDG $s \in \{1, \dots, 17\}$:
$$\text{RelevantSkills}(s) = \{k \in \mathcal{K}_{M5} \mid k \text{ maps to SDG } s\}$$
$$\text{PresentSkills}(C, s) = \text{RelevantSkills}(s) \cap \bigcup_{i \in C_{\text{eligible}}} \text{Skills}(i)$$
$$\text{SDG\_Capability\_Coverage}(C, s) = \frac{|\text{PresentSkills}(C, s)|}{|\text{RelevantSkills}(s)|} \quad (\text{when } |\text{RelevantSkills}(s)| > 0)$$

---

## 3. Role Exclusion Verification (Check B2)

Line 688 and Unit Test 37 enforce that role mappings never enter `cohort_skills_present`.  
A cohort of individuals with active roles (e.g., MASCO 2512) and zero confirmed skills yields exactly:
$$\text{skills\_present\_count} = 0, \quad \text{capability\_coverage\_ratio} = 0.0000$$

---

## 4. Temporal Mode Semantics (Check B3)

- **CURRENT:** Evaluates confirmed skills only (`p.get("confirmed_skills")`).
- **POST_PATHWAY:** Unions confirmed skills with planned reskilling curriculum skills (`reskilling_pathway.planned_skills`), tagged with mandatory projection disclaimer and `time_dimension_label: "PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED"`.

---

## 5. Manual Fixture Execution (Check B4)

An explicit fixture where M5 maps 4 canonical skills to SDG 1 was evaluated:
1. **Initial Cohort (2 of 4 skills):**  
   Present = 2, Total = 4 $\implies$ `ratio = 0.5000` (PASS).
2. **Adding Aligned Role (MASCO 2512):**  
   Present = 2, Total = 4 $\implies$ `ratio = 0.5000` (PASS — Role strictly excluded).
3. **Adding 3rd Canonical Skill:**  
   Present = 3, Total = 4 $\implies$ `ratio = 0.7500` (PASS).
