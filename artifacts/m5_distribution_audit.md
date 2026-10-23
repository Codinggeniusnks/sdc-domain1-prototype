# M5 SDG Distribution Audit

**System:** M5 SDG Impact Mapping Engine v1.0.0  
**Stage:** Stage 13A Architecture & Mapping  
**Date:** 2026-10-24  
**Auditor:** Senior Labour-Market Matching Methodologist, Quantitative Scenario Engineer  
**Artifact Referenced:** `data/sdg/skill_sdg_mappings_v1.json`, `data/sdg/role_sdg_mappings_v1.json`

---

## 1. Executive Summary & Macro Distribution

This audit examines the empirical distribution of SDG alignments across the 17 UN Sustainable Development Goals for the 16 canonical skills and 20 MASCO 4-digit occupations in the Prototype Domain 1 scope (ICT, Digital Economy, Engineering, Business Services, and Clerical Support).

The distribution reflects the **structural reality of Malaysia's knowledge-economy workforce**, rather than an artificial, forced uniform distribution across all 17 goals.

---

## 2. Global Distribution Across 17 Goals

The chart and table below show the total number of primary and secondary alignment links across the 17 SDGs:

```
SDG  1 (No Poverty)              | [0]
SDG  2 (Zero Hunger)             | [0]
SDG  3 (Good Health)             | [0]
SDG  4 (Quality Education)       | ===== [5]
SDG  5 (Gender Equality)         | [0]
SDG  6 (Clean Water)             | [0]
SDG  7 (Affordable Clean Energy) | ===== [5]
SDG  8 (Decent Work & Growth)    | ========================== [26]
SDG  9 (Industry, Innovation)    | ====================== [22]
SDG 10 (Reduced Inequalities)    | ==== [4]
SDG 11 (Sustainable Cities)      | = [1]
SDG 12 (Responsible Consumption) | ======== [8]
SDG 13 (Climate Action)          | ==== [4]
SDG 14 (Life Below Water)        | [0]
SDG 15 (Life on Land)            | [0]
SDG 16 (Peace, Justice, Inst)    | ============ [12]
SDG 17 (Partnerships)            | ====== [6]
```

### Tabular Distribution Breakdown:

| SDG # | SDG Official Name | Skill Primary | Skill Secondary | Role Primary | Role Secondary | Total Links | Share of Total | Primary Category in Scope |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **SDG 1** | No Poverty | 0 | 0 | 0 | 0 | 0 | 0.0% | Macro-social protection (out of immediate tech scope) |
| **SDG 2** | Zero Hunger | 0 | 0 | 0 | 0 | 0 | 0.0% | Agritech / Agriculture (Domain 2 future scope) |
| **SDG 3** | Good Health & Well-being | 0 | 0 | 0 | 0 | 0 | 0.0% | Healthcare / Clinical (Healthcare future scope) |
| **SDG 4** | Quality Education | 2 | 1 | 1 | 1 | 5 | 5.3% | Instructional design, workforce reskilling, training |
| **SDG 5** | Gender Equality | 0 | 0 | 0 | 0 | 0 | 0.0% | Institutional diversity (captured under DEI Target 10.2) |
| **SDG 6** | Clean Water & Sanitation | 0 | 0 | 0 | 0 | 0 | 0.0% | Municipal engineering (Environmental engineer secondary) |
| **SDG 7** | Affordable & Clean Energy | 0 | 0 | 4 | 1 | 5 | 5.3% | Electrical engineering, renewables, energy efficiency |
| **SDG 8** | Decent Work & Productivity | 3 | 4 | 12 | 7 | 26 | 27.7% | Economic productivity, technological upgrading, jobs |
| **SDG 9** | Industry, Innovation & Infra | 2 | 4 | 12 | 4 | 22 | 23.4% | Software R&D, ICT access, cloud computing, IC design |
| **SDG 10** | Reduced Inequalities | 0 | 1 | 1 | 2 | 4 | 4.3% | Accessibility, social inclusion, non-traditional reskilling |
| **SDG 11** | Sustainable Cities | 0 | 0 | 1 | 0 | 1 | 1.1% | Urban environmental engineering, municipal waste/air |
| **SDG 12** | Responsible Consumption | 1 | 2 | 4 | 1 | 8 | 8.5% | ESG reporting, corporate disclosures, life-cycle auditing |
| **SDG 13** | Climate Action | 1 | 2 | 1 | 0 | 4 | 4.3% | Carbon footprint analytics, GHG accounting, climate policy |
| **SDG 14** | Life Below Water | 0 | 0 | 0 | 0 | 0 | 0.0% | Marine / Fisheries (out of domain scope) |
| **SDG 15** | Life on Land | 0 | 0 | 0 | 0 | 0 | 0.0% | Forestry / Biodiversity (out of domain scope) |
| **SDG 16** | Peace, Justice & Institutions | 2 | 2 | 6 | 2 | 12 | 12.8% | Ethics, PDPA, fiduciary compliance, statutory audits |
| **SDG 17** | Partnerships for the Goals | 1 | 1 | 1 | 3 | 6 | 6.4% | High-quality open data, multi-stakeholder partnerships |
| **TOTAL** | | **12** | **17** | **42** | **22** | **93** | **100.0%** | |

---

## 3. Analysis of Domain Concentrations

### Why are SDGs 8 and 9 Predominant (51.1% Combined)?
The 20 MASCO occupations in Domain 1 represent Malaysia's digital transformation, software engineering, and business services sectors. In the UN 2030 indicator architecture:
- **Target 8.2** specifically measures *"economic productivity through diversification, technological upgrading and innovation, including through a focus on high-value added and labour-intensive sectors"*.
- **Target 9.5** measures *"upgrading technological capabilities of industrial sectors and encouraging innovation"*.
- **Target 9.c** measures *"access to information and communications technology"*.

These are the exact statutory and technical functions of software developers, systems analysts, database administrators, and ICT managers. Claiming these occupations align primarily to ocean conservation (SDG 14) or agriculture (SDG 2) would be dishonest.

### Why are SDGs 12 and 13 Focused on Specialized Roles?
SDG 12 (Target 12.6 - corporate sustainability reporting) and SDG 13 (Target 13.2 - climate measures) are concentrated specifically on accountants, auditors, environmental engineers, and sustainability reporting specialists. This concentration reflects the specialized technical nature of greenhouse gas accounting and ESG assurance.

### Why are SDGs 1, 2, 3, 5, 6, 14, 15 Zero in Scope?
Domain 1 is bounded to ICT, engineering, business services, and clerical work. Occupations in clinical healthcare (SDG 3), agricultural science (SDG 2), and marine biology (SDG 14) are scheduled for future sectoral expansions. Fabricating spurious links between office clerks and ocean conservation would violate the core anti-hallucination mandate.

---

## 4. Audit Verdict

- **Distribution Reality:** 100% justified by domain boundary.
- **Artificial Uniformity Imposed:** None.
- **Over-Claiming Detected:** None.
- **Outcome:** **PASS (VALID DISTRIBUTION)**.
