# M5 Comparative Evolution: v1.0.0 vs v1.1.0

**Document Reference**: M5-DIFF-001  
**Scope**: Full System Comparison (M5 SDG Impact Mapping Engine)  
**Status**: APPROVED  

---

## 1. High-Level Architecture Comparison

| System Dimension | M5 v1.0.0 (Candidate) | M5 v1.1.0 (Remediated) | Methodological Impact |
|---|---|---|---|
| **Engine Version** | 1.0.0 | **1.1.0** | Stage 13C remediation release |
| **UN Target Registry Scope** | 21 targets (unqualified) | **21 targets (Explicit `SELECTED_DOMAIN_RELEVANT_TARGETS`)** | P3-1 resolved: Anchored to 169-target official UN universe |
| **Target 9.c Mapping** | Widespread across software & digital skills | **100% Purged** (Reallocated to 9.5 & 8.2) | P1-1 resolved: Strict telecommunications physical boundary |
| **Data Privacy (PDPA 2010)** | Mapped to Target 16.10 (FOI) | **Mapped to Target 16.6 (DIRECT)** | P1-2 resolved: Realigned to institutional governance |
| **SQL Data Querying** | Mapped to Target 17.18 (Census ODA) | **Mapped to Target 9.5 & 8.2 (ENABLING)** | P1-3 resolved: Enterprise R&D / productivity realignment |
| **Corporate Carbon Accounting** | Target 13.2 DIRECT, Target 13.3 ENABLING | **Target 12.6 DIRECT, Target 13.2 ENABLING** | P2-1 resolved: Corporate disclosure vs macro policy split; 13.3 purged |
| **Engineering Roles (2151/2143/2152)**| Unqualified green DIRECT mappings | **`SECTOR_DEPENDENT_ALIGNMENT` flag + MEDIUM conf** | P2-2 resolved: Contextual deployment validity enforced |
| **Clerical Occupations (4110/4311/3343)**| Generic Target 8.5 alignment | **`CONTEXTUAL_BENEFICIARY_ALIGNMENT` flag** | P2-4 resolved: Worker beneficiary vs policy driver distinction |
| **Confidence Distribution** | 93.5% HIGH, 6.5% MEDIUM | **77.6% HIGH, 22.4% MEDIUM** | P2-3 resolved: Rating saturation eliminated |
| **Pathway Narrative Synthesis** | Undifferentiated roll-up | **Explicit separation of Skills vs Career Horizon** | Discloses competency acquisition vs occupational deployment |
| **$k$-Anonymity Regulatory Claim** | Statutory PDPA 2010 clause | **Engineering / Organizational Safeguard** | P3-2 resolved: Computer science privacy model precision |
| **Demographic Fairness Claim** | Substantive algorithmic fairness | **Structural Mathematical Invariance** | P3-3 resolved: Zero demographic input guarantees zero shift |
| **Benchmark Suite** | 8 benchmarks | **13 benchmarks (8 core + 5 remediation regressions)** | 100% pass rate across all suites |

---

## 2. Granular Skill Mapping Diff (Key Remediations)

```diff
  === carbon_footprint_analytics ===
- Target 13.2: DIRECT (HIGH)
- Target 13.3: ENABLING (HIGH)
- Target 12.6: ENABLING (HIGH)
+ Target 12.6: DIRECT (HIGH)
+ Target 13.2: ENABLING (HIGH)
+ Target 13.3: PURGED

  === data_privacy_pdpa ===
- Target 16.10: DIRECT (HIGH)
+ Target 16.6: DIRECT (HIGH)
+ Target 16.10: PURGED

  === sql_data_analysis ===
- Target 17.18: ENABLING (HIGH)
+ Target 9.5: ENABLING (HIGH)
+ Target 8.2: ENABLING (HIGH)
+ Target 17.18: PURGED

  === prompt_engineering ===
- Target 9.c: ENABLING (HIGH)
+ Target 8.2: ENABLING (MEDIUM)
+ Target 9.c: PURGED

  === api_integration ===
- Target 9.c: ENABLING (HIGH)
+ Target 9.5: ENABLING (HIGH)
+ Target 9.c: PURGED

  === rag_knowledge_systems ===
- Target 9.c: ENABLING (HIGH)
+ Target 9.5: ENABLING (HIGH)
+ Target 9.c: PURGED
```

---

## 3. Granular Occupational Mapping Diff (Key Remediations)

```diff
  === MASCO 2512 (Software Developers) ===
- Target 9.c: ENABLING (HIGH)
+ Target 9.5: ENABLING (HIGH)
+ Quality Flag: TARGET_SEMANTIC_REMEDIATED

  === MASCO 2151 (Electrical Engineers) ===
- Target 7.1: DIRECT (HIGH)
- Target 7.2: DIRECT (HIGH)
+ Target 7.1: DIRECT (MEDIUM)
+ Target 7.2: DIRECT (MEDIUM)
+ Quality Flag: SECTOR_DEPENDENT_ALIGNMENT

  === MASCO 2143 (Environmental Engineers) ===
- Target 13.2: DIRECT (HIGH)
+ Target 13.2: DIRECT (MEDIUM)
+ Quality Flag: SECTOR_DEPENDENT_ALIGNMENT

  === MASCO 2152 (Electronic Engineers) ===
- Target 12.5: ENABLING (HIGH)
+ Target 12.5: ENABLING (MEDIUM)
+ Quality Flag: SECTOR_DEPENDENT_ALIGNMENT

  === MASCO 4110 (General Office Clerks) ===
- Target 8.5: CONTEXTUAL (HIGH)
+ Target 8.5: CONTEXTUAL (MEDIUM)
+ Quality Flag: CONTEXTUAL_BENEFICIARY_ALIGNMENT
```

---

## 4. Stability of Core Architectural Invariants

M5 v1.1.0 strictly preserves all fundamental architectural invariants established in v1.0.0:
1. **Three Mapping Tiers**: `DIRECT`, `ENABLING`, and `CONTEXTUAL` preserved without dilution.
2. **General-Purpose Skill Rule (`RULE_GP_NON_DIRECT_STRICT`)**: 100% compliant across all 5 GP skills.
3. **Zero Fabricated Quantitative Metrics**: Zero synthetic kg CO2, jobs created, or percentage progress claims.
4. **Complete Module Isolation**: Zero feedback into M3 role recommendations or M4 course pathways.
