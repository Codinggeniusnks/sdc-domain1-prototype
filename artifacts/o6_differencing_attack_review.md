# Adversarial Review: Differencing Attack Vulnerabilities in O6 Engine

**Review Date:** 2026-10-24  
**Auditor:** Senior Privacy-Preserving Analytics Auditor & Security Methodologist  
**Status:** PARTIAL RESILIENCE — DEFECT DEF-P2-02 LOGGED

---

## 1. Adversarial Differencing Attack Threat Model

In statistical disclosure limitation (SDL), threshold suppression ($k=5$) prevents direct identification when an isolated query targets a cohort with $N < 5$. However, an adversary with query access can construct linear combinations of unsuppressed cohorts to reconstruct suppressed cohorts.

### Mathematical Formulation of Partition Differencing
Let cohort $\mathcal{C}$ be partitioned into disjoint subcohorts $\mathcal{C}_A$ and $\mathcal{C}_B$:
$$\mathcal{C} = \mathcal{C}_A \cup \mathcal{C}_B, \quad \mathcal{C}_A \cap \mathcal{C}_B = \emptyset$$

Suppose:
- $|\mathcal{C}| = 10 \ge 5$ (Unsuppressed)
- $|\mathcal{C}_A| = 6 \ge 5$ (Unsuppressed)
- $|\mathcal{C}_B| = 4 < 5$ (Suppressed by O6)

When an adversary queries $\mathcal{C}$ and $\mathcal{C}_A$:
1. $N_B = N_{\mathcal{C}} - N_{\mathcal{C}_A} = 10 - 6 = 4$.
2. For any additive aggregate metric $M$:
   $$M(\mathcal{C}_B) = M(\mathcal{C}) - M(\mathcal{C}_A)$$
3. The exact SDG alignment counts and mapping shares for the suppressed subcohort $\mathcal{C}_B$ are mathematically recovered.

---

## 2. Experimental Verification on O6 Synthetic Dataset

An adversarial script was executed against `SDGAggregationEngine` using the synthetic dataset:
1. **Parent Query:** Cohort `industrial_ops` ($N=12$). Result: Unsuppressed ($N=12$).
2. **Subcohort A:** Filter `region == 'Klang_Valley'` ($N=8$). Result: Unsuppressed ($N=8$).
3. **Subcohort B:** Filter `region == 'Penang'` ($N=4$). Result: `SUPPRESSED_SMALL_COHORT`.
4. **Reconstruction:**
   - Adversary computed $\text{SAP}(\text{Penang}) \times 4 = \text{SAP}(\text{Total}) \times 12 - \text{SAP}(\text{Klang_Valley}) \times 8$.
   - The exact count of workers contributing to SDG 9 in Penang was fully recovered.

---

## 3. Evaluation & Defect Classification

- **Current Rating:** `PARTIAL`.
- **Classification:** **P2** (Defect DEF-P2-02).
- **Reasoning:**
  O6 operates in a trusted enterprise/dashboard environment rather than an untrusted public API. However, declaring full privacy preservation without complementary suppression or differencing mitigation is methodologically misleading.

---

## 4. Stage 14C Remediation Strategy

To remediate DEF-P2-02 in Stage 14C:
1. **Explicit Differencing Warning:** Document differencing limitations in API metadata and engine specifications.
2. **Complementary Suppression Policy:** When reporting breakdowns of a cohort across dimensions (e.g. region, department), if exactly one cell is suppressed ($N < k$), suppress the second-smallest cell as well to prevent algebraic differencing.
3. **Long-Term Protection:** Add architectural support for differential privacy (DP Laplace/Gaussian noise) in enterprise deployment pipelines.
