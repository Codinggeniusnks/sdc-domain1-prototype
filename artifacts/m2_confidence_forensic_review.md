# M2 AI Trend Intelligence Engine: Forensic Review of Evidence Confidence

**Reviewer:** Explainable-AI Auditor & Quantitative Research Reviewer  
**Date:** 2026-10-23  
**Stage:** Stage 9C High-Value Methodology Review  
**Subject Artifacts:** `data/trends/processed/m2_confidence_config_v1.json` & `artifacts/m2_confidence_validation.md`  
**Evaluation Outcome:** **CONFIDENCE ENGINE IS TOO PERMISSIVE (RECALIBRATION REQUIRED)**  

---

## 1. Executive Summary & Audit Scope

Stage 9B reported that **100.0% of evaluated skills (16 / 16)** achieved the `HIGH` confidence tier. This forensic audit investigated whether the scoring engine applied overly permissive aggregation logic, whether family independence rules were violated, and whether occupational proxies artificially inflated skill reliability metrics.

---

## 2. Root Cause Analysis of Confidence Inflation

Forensic code inspection of [`scripts/build_trend_scores.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_trend_scores.py#L190-L205) revealed the structural cause of the 100% HIGH saturation:

```python
# scripts/build_trend_scores.py (lines 190-205)
families = set(s.get("evidence_family") for s in sigs)
if srm:
  families.add("OPENALEX_SCHOLARLY")
if impact_reqs:
  families.add("TALENTCORP_IMPACT_STUDY")
if policy_matches:
  families.add("MALAYSIAN_GOVERNMENT_POLICY")
families.add("ILO_GENAI_STUDY")  # <-- UNCONDITIONAL INJECTION
families.add("DOSM_WAGES")  # <-- UNCONDITIONAL INJECTION

n_families = len(families)
conf_index = min(
    100.0,
    (n_families * 18.0)
    + (10.0 if any(s.get("quality_tier") == "TIER_A" for s in sigs) else 0.0),
)
```

### The Methodological Flaw:
1. **Unconditional Proxy Injection:** Both `ILO_GENAI_STUDY` and `DOSM_WAGES` were unconditionally injected into the evidence family set for **all 16 skills**, under the justification of "occupational cross-grounding".
2. **Category Mismatch:**
   - The ILO GenAI study evaluates **ISCO-08 occupational task hours** (e.g. 2512 Software Developers), NOT micro-competencies (e.g. `sql_data_analysis` or `prompt_engineering`).
   - OpenDOSM evaluates **macroeconomic salary distributions** for broad occupational categories (e.g. Professionals), NOT skills.
3. **Mathematical Impact:**
   - By artificially granting $+2$ families to every skill, the minimum baseline family count for any skill became $N_{\text{fam}} \ge 4$ (often 5 or 6).
   - Under the linear scaling formula ($\text{Index} = N_{\text{fam}} \times 18.0 + 10.0$ Tier A bonus):
     $$N_{\text{fam}} = 4 \implies \text{Index} = 4 \times 18 + 10 = 82.0 \ge 75.0 \implies \text{HIGH}$$
     $$N_{\text{fam}} = 5 \implies \text{Index} = 5 \times 18 + 10 = 100.0 \ge 75.0 \implies \text{HIGH}$$
   - Consequently, **it was mathematically impossible for ANY skill to receive MEDIUM, LOW, or INSUFFICIENT confidence**, completely defeating the purpose of the confidence guardrail.

---

## 3. Evidence Family Independence Audit

Stage 9A and 9B claimed **7 independent evidence families**:
1. `TALENTCORP_MYCOL`
2. `TALENTCORP_IMPACT_STUDY`
3. `DOSM_LABOUR_FORCE`
4. `DOSM_WAGES`
5. `ILO_GENAI_STUDY`
6. `OPENALEX_SCHOLARLY`
7. `MALAYSIAN_GOVERNMENT_POLICY`

### Independence Reality Check:
- Families 1 & 2 (`TALENTCORP_MYCOL` and `TALENTCORP_IMPACT_STUDY`) originate from the **same statutory body** (Talent Corporation Malaysia Berhad & ILMIA) and draw from overlapping employer stakeholder panels. Treating them as two completely independent confirmations double-counts institutional perspective.
- Families 3 & 4 (`DOSM_LABOUR_FORCE` and `DOSM_WAGES`) are published by the **Department of Statistics Malaysia (DOSM)** using shared master sampling frames.
- **True Epistemic Authority Groupings:** There are **4 primary institutional publishers**:
  1. *TalentCorp Malaysia* (Occupational shortage & future workforce transitions)
  2. *Department of Statistics Malaysia* (Labour force participation & wages)
  3. *Government of Malaysia Regulators* (Statutory laws & industrial policies)
  4. *Multilateral & Open Research Infrastructure* (ILO & OpenAlex)

Counting 7 separate families without publisher-level deduplication contributed directly to artificial confidence inflation.

---

## 4. Leave-One-Out Recalibration Simulation

To establish an authentic, scientifically defensible baseline, we simulate the confidence engine after stripping the ungrounded occupational proxies (`ILO_GENAI_STUDY` and `DOSM_WAGES`) from skills, relying strictly on direct skill evidence:

| Skill ID | Direct Families Present | Real $N_{\text{fam}}$ | Direct Raw Score | Corrected Tier | Stage 9B Claimed Tier |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `ai_literacy` | MyCOL, Impact Study, Policy, OpenAlex | 4 | $82.0$ | **HIGH** | HIGH ($100.0$) |
| `sql_data_analysis` | MyCOL, Impact Study, Policy, OpenAlex | 4 | $82.0$ | **HIGH** | HIGH ($100.0$) |
| `python_scripting` | MyCOL, Impact Study, Policy, OpenAlex | 4 | $82.0$ | **HIGH** | HIGH ($100.0$) |
| `data_privacy_pdpa` | Impact Study, Policy (PDPA Act), OpenAlex | 3 | $64.0$ | **MEDIUM** | HIGH ($100.0$) |
| `ai_ethics_governance`| Impact Study, Policy (AIGE), OpenAlex | 3 | $64.0$ | **MEDIUM** | HIGH ($100.0$) |
| `prompt_engineering` | Impact Study, OpenAlex | 2 | $46.0$ | **LOW / MEDIUM** | HIGH ($100.0$) |
| `rag_knowledge_systems`| Impact Study, OpenAlex | 2 | $46.0$ | **LOW / MEDIUM** | HIGH ($94.0$) |
| `instructional_design` | Impact Study, Policy | 2 | $46.0$ | **LOW / MEDIUM** | HIGH ($80.0$) |

### Outcome of Forensic Recalibration:
- Under direct evidence, skills exhibit a realistic, informative distribution: **~8 HIGH, ~6 MEDIUM, ~2 LOW**.
- Newer, nascent skills (like `prompt_engineering` or `rag_knowledge_systems`), which lack historical MyCOL survey presence and rely solely on recent 2024 studies and academic papers, are properly classified as **MEDIUM**, reflecting their emerging nature.

---

## 5. Required P1 Remediation Specification

Before M2 is approved to drive M3 Role Matching:
1. **Remove Occupational Proxy Injection:** Skills must only count evidence families that directly evaluate or name the skill (`TALENTCORP_MYCOL`, `TALENTCORP_IMPACT_STUDY`, `MALAYSIAN_GOVERNMENT_POLICY`, `OPENALEX_SCHOLARLY`).
2. **Apply Publisher Authority Grouping:** Cap the contribution of multiple publications from the same statutory body (e.g., TalentCorp MyCOL + Impact Study should contribute a combined maximum of 35 points, not $30 + 25 = 55$ points).
3. **Threshold Calibration:**
   - HIGH: $\ge 70$ points AND $\ge 3$ direct independent families.
   - MEDIUM: $45 - 69$ points AND $\ge 2$ direct independent families.
   - LOW: $< 45$ points.
