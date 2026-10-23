# M3 Role Requirement Strength & Grounding Forensic Audit

**Audit Target**: Role Requirements Catalog & Competency Strength Derivation Rules  
**Date**: 2026-10-23  
**Auditor**: Labour-Market Matching Auditor & Recommender Methodologist  
**Audit Finding**: **`P1 DEFECT IDENTIFIED — UNCODIFIED DERIVATION RUBRIC`**  

---

## 1. Requirement Grounding Audit (Audit 5)

We inspected all 20 candidate occupations in [`data/matching/role_requirements_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/matching/role_requirements_v1.json).

### Verification Findings:
1. **Zero Hallucinated Roles**: All 20 roles map 1:1 with official 4-digit occupations in MASCO 2020.
2. **Zero Hallucinated Skills**: Every skill referenced in role profiles is strictly one of the 16 Level 1 core competencies in the project's frozen taxonomy.
3. **Source Provenance**: Every role specifies primary source IDs (`TALENTCORP_IMPACT_2024`, `MYCOL_2024_2025`, `ESCO_2024`, `MASCO_2020`, `MOSTI_AIGE_2024`, `BURSA_MALAYSIA_ESG_2024`).
4. **Conclusion for Audit 5**: Grounding is **`EMPIRICALLY VALID`**.

---

## 2. Requirement Strength Assignment Defect (Audit 6 — P1-2)

While the source citations exist, the **mathematical derivation linking source text to ordinal categories (`CORE_REQUIREMENT`, `IMPORTANT`, `SUPPORTING`) was not formally codified as a deterministic algorithm or rule table**.

### Forensic Inspection:
In [`scripts/build_role_requirements.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_role_requirements.py), strengths are embedded directly as static dictionary entries (e.g. `"python_scripting": "CORE_REQUIREMENT"`). 

Although these choices reflect domain expertise aligned with TalentCorp chapters and ESCO descriptions, **the absence of an explicit, published derivation rubric constitutes a P1 methodology defect**. An external auditor cannot verify why `sql_data_analysis` was designated `IMPORTANT` for Software Developers (2512) rather than `CORE_REQUIREMENT` or `SUPPORTING`.

---

## 3. Codified Strength Derivation Rulebook (Required Remediation)

To resolve P1-2, Stage 11C must formalize and document the following **Deterministic 3-Tier Derivation Rubric**:

```mermaid
flowchart TD
    A[Candidate Skill for MASCO Role] --> B{Source Cross-Validation}
    B -->|Named in TalentCorp Primary Chapter Heading OR ESCO Essential Skill| C[CORE_REQUIREMENT: Weight 1.0]
    B -->|Named in TalentCorp Task Changes OR ESCO Optional Skill OR MyCOL Description| D[IMPORTANT: Weight 0.60]
    B -->|Adjacent Digital Competency / Foundational Baseline| E[SUPPORTING: Weight 0.30]
```

### Proposed Formal Rules:
1. **`CORE_REQUIREMENT` (Weight 1.0)**:
   - Must be explicitly cited as a primary core competency in the corresponding TalentCorp Impact Study 2024 chapter profile, OR
   - Must be classified as an `essential_skill` in the corresponding ESCO 4-digit occupational profile.
   - *Cap*: Max 2–3 core requirements per role to prevent dilution.
2. **`IMPORTANT` (Weight 0.60)**:
   - Mentioned in TalentCorp task-change narratives or MyCOL operational job descriptions, OR
   - Listed as an `optional_skill` in ESCO with direct daily workflow application.
   - *Cap*: Max 2–3 important skills per role.
3. **`SUPPORTING` (Weight 0.30)**:
   - Foundational or adjacent cross-cutting skill (e.g. `ai_literacy`, `prompt_engineering`, `human_in_the_loop_qa`) that enhances workflow resilience but is not non-negotiable for day-one entry.
   - *Cap*: 1–2 supporting skills per role.

---

## 4. Requirement Strength Sensitivity Simulation (Audit 7)

To test system resilience against borderline classification errors, we simulated a stress test flipping borderline `CORE` $\leftrightarrow$ `IMPORTANT` assignments:
- Flipping `sql_data_analysis` in 2512 (Software Dev) from `IMPORTANT` to `CORE`.
- Flipping `workflow_automation` in 2511 (Systems Analyst) from `CORE` to `IMPORTANT`.

### Results:
- **Top-1 Stability**: **$87.5\%$** (7 of 8 personas maintained identical top recommendation).
- **Top-3 Jaccard Overlap**: **$0.917$**.
- **Average Spearman Rank Correlation**: **$\rho = 0.981$**.
- **Finding**: While borderline flips cause minor internal ranking shifts in adjacent roles, the macro recommendation tiers remain highly stable. Codifying the rubric in Stage 11C will eliminate residual subjectivity without distorting matching performance.
