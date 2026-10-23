# O1 Weight Sensitivity Analysis v1.1.0

**Reference Date:** 2026-10-24  
**Evaluation:** Local Perturbation Stability ($\pm 0.05$ on each active component)  

---

## 1. Sensitivity Test Results

| Perturbation Condition | Spearman Correlation | Skills Moving $\ge 3$ Positions | Status |
| :--- | :---: | :---: | :---: |
| core_gap_prevalence (-0.05) | 0.9816 | None | PASS |
| core_gap_prevalence (+0.05) | 0.9904 | None | PASS |
| important_gap_prevalence (-0.05) | 0.9934 | None | PASS |
| important_gap_prevalence (+0.05) | 0.9816 | None | PASS |
| cross_role_transferability (-0.05) | 0.9801 | None | PASS |
| cross_role_transferability (+0.05) | 0.9875 | None | PASS |
| scenario_urgency (-0.05) | 1.0000 | None | PASS |
| scenario_urgency (+0.05) | 1.0000 | None | PASS |
| prerequisite_centrality (-0.05) | 0.9823 | None | PASS |
| prerequisite_centrality (+0.05) | 0.9971 | None | PASS |

---

## 2. Classification & Conclusion

- **Minimum Spearman Correlation:** **0.9801** ($\ge 0.9765$)
- **Maximum Rank Shift:** $\pm 1$ position
- **Classification:** **ROBUST**
The priority weights exhibit high mathematical stability under local perturbations, confirming their fitness for enterprise policy planning.
