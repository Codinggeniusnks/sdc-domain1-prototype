# O1 Unified Small-Cell Privacy Policy v1.1.0

**Reference Date:** 2026-10-24  
**Specification:** Unified Privacy Floor & Mathematical Suppression Layer  

---

## 1. Canonical Policy Definition

O1 v1.1.0 implements a unified, reusable privacy safeguarding layer governing all employer-facing outputs.

### Mathematical Parameters:
- **Minimum Cohort Size ($k$):** $5$ (Enterprise policy floor; not statutory PDPA).
- **Sensitive Small Cell:** Any subgroup count $N$ where $0 < N < 5$.
- **Zero Values:** Legitimate zeros ($N = 0$) remain unmasked as `"0"`, reflecting complete absence of capability deficit.
- **Masking Format:** 
  - Underlying integer: `null`
  - Display string: `"<5"`
  - Status flags: `"suppressed": true`, `"suppression_reason": "SMALL_CELL_PRIVACY"`

---

## 2. Reusable Suppression Primitives

The engine centralizes all privacy enforcement through three core primitives:

1. `mask_small_cell_count(count: Optional[int]) -> (Optional[int], str, bool)`
2. `mask_small_cell_prevalence(count: Optional[int], total: int) -> (Optional[float], str, bool)`
3. `apply_partition_suppression(category_counts: Dict[str, int], parent_total: Optional[int]) -> Dict[str, Dict[str, Any]]`

---

## 3. Priority Reconstruction Protection

Because the Reskilling Priority Index is a linear combination of six explainable components:
$$\text{Priority} = 100 \times \sum_{i=1}^{6} w_i x_i$$
Publishing the final index alongside unmasked sibling components would allow an adversary to solve for an underlying small-cell numerator:
$$x_{\text{core}} = \frac{\text{Priority} - \sum_{j \neq \text{core}} w_j x_j}{w_{\text{core}}}$$
To defeat this algebraic re-identification vector, O1 v1.1.0 enforces:
> **Reconstruction Safety Invariant:** If ANY active ranking component depends on an underlying $0 < N < 5$ subgroup, the employer-facing `priority_index`, `components`, and `weighted_contributions` are suppressed to `null`.

---

## 4. Truthful Privacy Limitations

- **Cross-Query Differencing:** Truthfully rated **PARTIAL**. Standard small-cell suppression mitigates isolated queries but does not provide Differential Privacy guarantees.
- **Differential Privacy:** `differential_privacy_claimed: false`. Zero Laplace or Gaussian noise is injected into deterministic operational outputs.
