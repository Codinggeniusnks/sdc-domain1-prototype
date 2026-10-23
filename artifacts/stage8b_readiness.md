# Stage 8B Readiness Assessment & Gate Verdict

**Date**: 2026-10-23  
**Stage Transition**: Stage 8A (Gold Data Expansion & Quality Audit) $\longrightarrow$ Stage 8B (Dataset v5 Construction & Synthetic Pruning)  
**Evaluator**: Senior ML Data Engineer, Occupational Data Researcher & Dataset Quality Auditor  
**Candidate Corpus**: `data/processed/gold_corpus_v5_candidate.json` ($N=305$)  
**Candidate Manifest**: `data/manifests/gold_corpus_v5_manifest.json`  

---

## 1. Executive Summary

Stage 8A was chartered by the Stage 7C Argon methodology review to eliminate the severe empirical data deficit capping model generalisation—specifically the reliance on only 98 real Gold records across 16 multi-label classes.

This readiness assessment evaluates whether the candidate Gold corpus fulfills all prerequisites to advance to **Stage 8B (Dataset v5 Construction & Synthetic Pruning)**.

---

## 2. Gate Verification Checklist

| Gate Criterion | Target Threshold | Achieved Metric | Status |
|---|---|---|---|
| **1. Gold Corpus Scale** | $\ge 300$ authoritative records | **305 records** ($+211.2\%$) | **MET** |
| **2. Synthetic Contamination in Gold** | Strictly $0.0\%$ | **0 synthetic records ($0.0\%$)** | **MET** |
| **3. Minimum Class Positive Support** | $\ge 20$ positives for all 16 skills | **16 of 16 skills meet $\ge 20$** | **MET** |
| **4. P0 Critical Data Gaps** | $+25$ target for P0 classes | `data_privacy_pdpa`: **44** ($+34$)<br>`process_mapping`: **99** ($+79$)<br>`esg_sustainability`: **43** ($+28$) | **MET** |
| **5. P1 Industrial Transition Gaps** | $+20$ target for P1 areas | `instructional_design`: **29**<br>`workflow_automation`: **67**<br>`human_in_the_loop_qa`: **59**<br>`sql_data_analysis`: **62** | **MET** |
| **6. P2 Advanced AI & Digital Skills** | $+15$ target for P2 areas | `rag_knowledge_systems`: **26**<br>`prompt_engineering`: **31**<br>`python_scripting`: **63** | **MET** |
| **7. Institutional Source Legitimacy** | Public/open regulatory bodies | **128 authoritative sources** | **MET** |
| **8. Native Malaysian Context** | Primary labour market grounding | **279 records ($91.5\%$)** | **MET** |
| **9. Occupational Diversity** | Broad MASCO unit group coverage | **61 4-digit unit groups** | **MET** |
| **10. Label Evidence Traceability** | Programmatic evidence verification | **100.0% verified (623/623 labels)** | **MET** |
| **11. Protocol B Protection** | Zero accesses / 100% sealed | **0 accesses** (Unopened) | **MET** |
| **12. Protocol C v2 Protection** | Zero accesses / 100% sealed | **0 accesses** (Unopened) | **MET** |
| **13. Quarantined Unit Group Isolation** | 0 overlaps with 25 test groups | **0 records overlap** (3 intercepted) | **MET** |
| **14. Deduplication Integrity** | Max cosine similarity $< 0.85$ | **Max observed: $0.412$** | **MET** |

---

## 3. Detailed Gap Status Summary

```
                      16-Skill Positive Support vs Floor
  Positives
   100 ───────────────────────────────────────── 99 (process_mapping)
    90 ───────────────────────────────────────── 98 (stakeholder_comm)
    80 ─────────────────────────────────────────
    70 ───────────────────────────────────────── 67 (workflow_auto)
    60 ───────────────────────────────────────── 63 (python), 62 (sql), 59 (hitl_qa)
    50 ─────────────────────────────────────────
    40 ───────────────────────────────────────── 44 (pdpa), 43 (esg), 41 (data_vis), 42 (api)
    30 ───────────────────────────────────────── 36 (ai_lit), 31 (prompt), 30 (ethics), 29 (carbon, inst)
    20 ═════════════════════════════════════════ 20 (MINIMUM HEURISTIC FLOOR)
    10 ───────────────────────────────────────── 26 (rag_knowledge)
     0 ─────────────────────────────────────────
```

- **P0 Gaps Remaining**: **0**
- **P1 Gaps Remaining**: **0**
- **P2 Gaps Remaining**: **0**
- **Skills Below 20 Real Positives**: **0**

---

## 4. Execution Blueprint for Stage 8B

Upon authorization to proceed to Stage 8B:

1. **Assemble Dataset v5**:
   - Merge `data/processed/gold_corpus_v5_candidate.json` ($N=305$) with class-conditionally pruned synthetic data.
2. **Apply Class-Conditional Synthetic Pruning Formula**:
   $$\text{Synthetic Count}(k) = \max\left(0, 30 - N_{\text{gold}}(k)\right)$$
   - Classes with $N_{\text{gold}} \ge 30$ (e.g., `process_mapping`, `workflow_automation`, `sql_data_analysis`, `python_scripting`, `stakeholder_communication`, `data_privacy_pdpa`, `esg_sustainability_reporting`, `ai_literacy`, `prompt_engineering`, `ai_ethics_governance`, `data_visualization`) will have their synthetic support reduced to 0, completely removing synthetic template bias from well-supported skills.
   - Classes with $20 \le N_{\text{gold}} < 30$ (e.g., `rag_knowledge_systems`, `carbon_footprint_analytics`, `instructional_design`) will retain minimal, targeted synthetic support (1–4 records) solely for rare edge-case balancing.
   - Expected synthetic footprint in Dataset v5: $\le 20$ records ($\approx 5\%$ of training data, down from $72\%$).
3. **Build Stage 8B CV Split Manifest**:
   - Partition Dataset v5 into 5-fold grouped cross-validation grouped strictly by MASCO 4-digit unit group.
4. **Decouple Candidate B & Candidate C**:
   - Re-screen the decoupled architectures on Dataset v5 to evaluate real generalisation gains.

---

## 5. Final Stage 8A Verdict

The evidence demonstrates that the Gold expansion has been completed legitimately, with authentic institutional backing, verified label evidence, zero synthetic contamination, and complete holdout isolation.

The formal verdict is:

$$\mathbf{READY\ TO\ BUILD\ DATASET\ V5}$$
