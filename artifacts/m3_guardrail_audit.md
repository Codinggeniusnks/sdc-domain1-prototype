# M3 Guardrails Continuity & Discontinuity Forensic Audit

**Audit Target**: Zero-Overlap Clamp, 20% Skill-Advantage Override, and Macro Dominance Protection  
**Date**: 2026-10-23  
**Auditor**: Senior Recommender-Systems Methodologist & Mathematical Auditor  
**Audit Finding**: **`P1 DEFECT (ZERO-CLAMP DISCONTINUITY) & P2 DEFECT (20% BUBBLE SWAP DISCONTINUITY)`**  

---

## 1. Zero-Overlap Clamp Continuity Audit (Audit 12 — P1-3)

The matching engine enforces a rule intended to prevent macro labor demand (M2) and AI resilience (M6) from elevating completely unrelated occupations:
$$\text{If } S_{\text{fit}}(U, r) == 0.0 \implies \text{Role Match Index} \le 15.0$$

### Forensic Empirical Test:
We evaluated candidate role `2512 Software Developers` (which has high M2 shortage of $89.6$ and high M6 resilience of $92.5$) across four progressive skill profiles:

| Profile Overlap Tier | User Competencies Present | Earned Skill Fit ($S_{\text{fit}}$) | Actual Composite Score | Clamped Score ($RMI$) | Delta vs Prior Tier |
|:---|:---|:---:|:---:|:---:|:---:|
| **Tier 0 (0% Overlap)** | `esg_sustainability_reporting` | **0.0%** | 34.5 | **15.0** | Baseline |
| **Tier 1 (7.9% Overlap)** | `rag_knowledge_systems` (Supporting) | **7.9%** | 36.2 | **36.2** | **+21.2 points** |
| **Tier 2 (15.8% Overlap)** | `sql_data_analysis` (Important) | **15.8%** | 39.2 | **39.2** | +3.0 points |
| **Tier 3 (26.3% Overlap)** | `python_scripting` (Core) | **26.3%** | 52.6 | **52.6** | +13.4 points |

### Defect Analysis (P1-3):
- Between Tier 0 ($0\%$ fit) and Tier 1 ($7.9\%$ fit), the score experiences an **artificial $21.2$-point step jump** ($15.0 \rightarrow 36.2$).
- The jump occurs because raw composite scoring at $0\%$ fit already calculates to $34.5$ (driven by $0.25 \times 89.6 + 0.15 \times 92.5 = 22.4 + 13.9 = 36.3$). The hard ceiling abruptly truncates this to $15.0$, but matching a single minor supporting skill completely removes the ceiling.
- **Methodological Verdict**: A hard mathematical clamp is an arbitrary "magic constant" that violates score continuity.

### Required Remediation (Continuous Skill-Fit Gating):
Instead of an arbitrary post-hoc clamp, external macro context ($M2$ and $M6$) should be continuously gated by the candidate's skill fit:
$$\text{Gated M2/M6 Multiplier } G(S_{\text{fit}}) = \min\left(1.0, \frac{S_{\text{fit}}}{20.0}\right)$$
Under this continuous formulation:
- At $S_{\text{fit}} = 0\%$, $G = 0.0 \implies$ external context is fully suppressed, naturally yielding a low baseline score without an artificial clamp.
- At $S_{\text{fit}} = 10\%$, $G = 0.50 \implies$ partial macro context is smoothly integrated.
- At $S_{\text{fit}} \ge 20\%$, $G = 1.00 \implies$ full macro context operates normally.
- This produces a strictly monotonic, continuous progression without step jumps.

---

## 2. 20% Skill-Advantage Guardrail Audit (Audit 14 — P2-1)

Stage 11A implemented a post-sorting bubble swap:
```python
# Lines 285-298 in src/role_matching_engine.py
if lower_role["components"]["current_skill_fit"] - higher_role["components"]["current_skill_fit"] > dom_threshold:
    if lower_role["role_match_index"] <= higher_role["role_match_index"]:
        lower_role["applied_guardrails"].append("SCENARIO_DOMINANCE_PROTECTED")
        scored_roles[i], scored_roles[j] = scored_roles[j], scored_roles[i]
```

### Forensic Critique:
1. **Discontinuous Step Inversion**:
   - If Role A has $S_{\text{fit}} = 45.0\%$ and Role B has $S_{\text{fit}} = 25.1\%$ ($\Delta = 19.9\%$), normal ranking applies.
   - If Role B has $S_{\text{fit}} = 24.9\%$ ($\Delta = 20.1\%$), a hard post-sort swap is triggered, forcibly swapping the positions.
   - A $0.2\%$ change in skill fit causes a hard discrete ranking inversion.
2. **Redundancy Analysis**:
   - Because $w_{\text{M1}} \ge 55\%$, a $20.0\%$ advantage in skill fit contributes at least $0.55 \times 20.0 = 11.0$ composite points.
   - For an inferior role to overcome an $11.0$-point deficit, it would require near-maximum disparity in M2 and M6 scores.
3. **Audit Verdict**: **`TOO HARD / DISCONTINUOUS (P2-1)`**.
   - Remediation: Replace the post-sort bubble swap with continuous soft penalty integration, or allow the mathematical primacy of $w_{\text{M1}} \ge 55\%$ and skill-fit gating to govern the ordering naturally.

---

## 3. Macro Dominance Verification (Audits 13, 15, 16)

We audited whether high labor shortage (M2) or high AI scenario resilience (M6) could ever elevate an unqualified candidate above fit occupations:

### Findings:
1. **Zero Dominance of M6**: Under M6 weights of $0\%, 5\%, 10\%, 15\%$, M6 adjusted ranks by at most $\pm 1$ position among closely matched roles. It never elevated an irrelevant role to the top tier.
2. **Zero Dominance of M2**: Across all 8 synthetic personas, the top 3 recommendations strictly matched the person's functional domain (Data analysts received database roles; developers received software roles; environmental analysts received sustainability roles).
3. **Conclusion**: The primary $w_{\text{M1}} \ge 55\%$ weight ceiling successfully guarantees skill-first primacy.
