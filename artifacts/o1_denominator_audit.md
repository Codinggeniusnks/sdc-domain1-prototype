# O1 Denominator & Profile Ingestion Audit (v1.0.0)

**Audit Scope:** Mathematical Denominator Hygiene & Sanitization Layers  
**Status:** PASS — MATHEMATICAL DENOMINATOR INTEGRITY VERIFIED

---

## 1. Denominator Specifications

| Metric | Formally Specified Formula | Denominator Definition |
|---|---|---|
| **Cohort Profile Eligibility** | $N_{\text{eligible}} = |\mathcal{C}_{\text{eligible}}|$ | Count of validated dictionary profiles with verified ID and role/skill content. |
| **Skill Gap Prevalence** | $\text{GapPrevalence}(s) = \frac{|\text{GappedProfiles}(s)|}{N_{\text{eligible}}}$ | Strictly $N_{\text{eligible}}$. Malformed, duplicate, or excluded records are omitted. |
| **CORE Gap Prevalence** | $\text{CoreGapPrevalence}(s) = \frac{|\text{CoreGappedProfiles}(s)|}{N_{\text{eligible}}}$ | Strictly $N_{\text{eligible}}$. |
| **IMPORTANT Gap Prevalence** | $\text{ImportantGapPrevalence}(s) = \frac{|\text{ImpGappedProfiles}(s)|}{N_{\text{eligible}}}$ | Strictly $N_{\text{eligible}}$. |
| **Mean Deficit Among Gapped** | $\text{MeanDeficit}(s) = \frac{\sum_{i \in \text{Gapped}} \text{Deficit}(i, s)}{|\text{GappedProfiles}(s)|}$ | Strictly $|\text{GappedProfiles}(s)|$. Deficits of ungapped workers (0.0) are NOT averaged in. |
| **Role Transition Share** | $\text{TransitionShare}(r_1 \to r_2) = \frac{\text{Count}(r_1 \to r_2)}{N_{\text{eligible}}}$ | Strictly $N_{\text{eligible}}$. |

---

## 2. Ingestion Classification Matrix

Candidate profile records are categorized into 6 mutually exclusive states:
1. `ELIGIBLE`: Valid operational dictionary with verified string ID, containing roles or skills.
2. `EXCLUDED_INVALID_TYPE`: Non-dictionary records (`None`, strings, integers, arrays).
3. `EXCLUDED_MISSING_ID`: Missing, empty, or whitespace-only `profile_id`.
4. `EXCLUDED_PROHIBITED_DEMOGRAPHIC`: Contains prohibited demographic attributes.
5. `EXCLUDED_RAW_CV`: Contains raw CV text (`raw_cv`, `resume_text`).
6. `EXCLUDED_INCOMPLETE`: Dictionaries missing both roles and confirmed skills.
7. `EXCLUDED_DUPLICATE_ID`: Repeated instances of previously ingested profile IDs (first instance retained).

---

## 3. Boundary & Error Conditions

- **All-Invalid Input:** Returns `status: "INSUFFICIENT_ELIGIBLE_COHORT_DATA"` with $N_{\text{eligible}} = 0$ and zero divide-by-zero crashes.
- **Empty Cohort:** Returns `suppressed: True` and zero distributions.
- **Small Cohort ($0 < N_{\text{eligible}} < 5$):** Returns `status: "SUPPRESSED_SMALL_COHORT"`, masking statistical distributions to prevent identity disclosure.
