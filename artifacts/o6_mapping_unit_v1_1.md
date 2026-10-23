# Canonical Mapping-Type Counting Unit Specification (v1.1.0)

**Defect Addressed:** DEF-P2-03  
**Status:** IMPLEMENTED & RECONCILED

---

## 1. Specification & Code Reconciliation

Stage 14B identified an ambiguity where `artifacts/o6_metric_definitions.md` described mapping shares over unique $(i, t, \tau)$ triples, whereas `src/sdg_aggregation_engine.py` summed all entity mapping instances.

In O6 v1.1.0, the implementation and documentation are fully reconciled to the canonical mathematical definition:

$$\text{Canonical Counting Unit} \equiv \text{UNIQUE PROFILE--TARGET--MAPPING\_TYPE RELATION } (i, t, \tau)$$

where:
- $i \in \mathcal{C}_{\text{elig}}$ is an eligible synthetic profile ID.
- $t \in \mathcal{T}$ is a canonical M5 SDG target ID (e.g. `"8.2"`).
- $\tau \in \{\text{"DIRECT"}, \text{"ENABLING"}, \text{"CONTEXTUAL"}\}$ is the evidence mapping tier.

---

## 2. Deduplication Rules

1. **Intra-Profile Entity Deduplication:**
   If profile $i$ holds multiple skills (e.g. Python and API Integration) or a role that all map to target $t$ with mapping type $\tau$, this contributes **exactly one** relation $(i, t, \tau)$.
2. **Multiple Legitimate Mapping Types:**
   If profile $i$ reaches target $t$ via DIRECT mapping (e.g. specialized clean tech skill) and target $t'$ via ENABLING mapping (e.g. software skill), or even reaches target $t$ via both DIRECT and ENABLING evidence, both distinct $(i, t, \tau)$ relations are preserved in the set $R$.

---

## 3. Formula for Mapping Shares

Let $R = \bigcup_{i \in \mathcal{C}_{\text{elig}}} R_i$. If $|R| > 0$:
$$\text{direct\_share} = \frac{|\{r \in R \mid \tau = \text{DIRECT}\}|}{|R|}$$
$$\text{enabling\_share} = \frac{|\{r \in R \mid \tau = \text{ENABLING}\}|}{|R|}$$
$$\text{contextual\_share} = \frac{|\{r \in R \mid \tau = \text{CONTEXTUAL}\}|}{|R|}$$

If $|R| == 0$, the engine safely returns `status: "NO_ALIGNMENT_RELATIONS"` without division-by-zero.
