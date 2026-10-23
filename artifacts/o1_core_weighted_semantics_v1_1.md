# O1 CORE-Weighted Preference Semantics v1.1.0

**Reference Date:** 2026-10-24  
**Defect Resolved:** DEF-P2-01 (CORE-First Documentation Overstatement)  

---

## 1. Empirical Counterexample & Proof

Stage 15B audited the claim that "CORE gaps are structurally prioritised."
The mathematical model evaluates priority as:
$$\text{Priority} = 100 \times [w_{\text{core}} x_{\text{core}} + w_{\text{imp}} x_{\text{imp}} + w_{\text{trans}} x_{\text{trans}} + w_{\text{scen}} x_{\text{scen}} + w_{\text{prereq}} x_{\text{prereq}}]$$

Consider the following adversarial fixture:
- **Skill A (Widespread IMPORTANT Gap):** $x_{\text{core}} = 0.0$, $x_{\text{imp}} = 0.80$, $x_{\text{trans}} = 0.50$, $x_{\text{prereq}} = 0.20$
  $$\text{Priority}_A = 100 \times [0.2353(0.80) + 0.1765(0.50) + 0.0588(0.20)] = \mathbf{28.82}$$
- **Skill B (Rare CORE Gap):** $x_{\text{core}} = 0.05$, all other components $= 0.0$
  $$\text{Priority}_B = 100 \times [0.4118(0.05)] = \mathbf{2.06}$$

**Outcome:** Skill A outranks Skill B by $26.76$ points ($28.82$ vs $2.06$).
This mathematically refutes any absolute structural precedence claim.

---

## 2. Strategic Enterprise Justification

For organizational reskilling investments, **weighted preference is the correct policy**:
- An employer cannot prioritize a rare competency needed by 1 employee over a critical digital skill needed by 80% of the entire department.
- Therefore, O1 assigns CORE gaps the single largest weight ($0.4118$), providing a strong advantage, but allows widespread prevalence and prerequisite leverage to govern institutional resource allocation.
- In contrast, **M4 individual learner pathways** strictly maintain `CORE_FIRST_ORDERING`.
