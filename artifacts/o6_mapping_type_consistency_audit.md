# Forensic Mapping Type Consistency Audit (Stage 14E)

**Audit Date:** 2026-10-24  
**Auditor Roles:** Senior Reproducibility Auditor, Aggregation-Mathematics Reviewer, Responsible-AI Safety Engineer  
**Audit Scope:** Issue A Forensic Verification — Mapping Types & Canonical Counting Units  
**Verdict:** `DOCUMENTATION-ONLY ERROR` (Production code verified complete for DIRECT, ENABLING, CONTEXTUAL)

---

## 1. Issue A Problem Statement

Stage 14D report erroneously declared:
$$\tau \in \{\text{DIRECT}, \text{ENABLING}\}, \quad \text{Share}_{\text{direct}} + \text{Share}_{\text{enabling}} = 1.0$$
omitting the CONTEXTUAL mapping type.

Frozen upstream M5 v1.1.0 contains verified CONTEXTUAL mappings, including clerical and beneficiary alignments (`CONTEXTUAL_BENEFICIARY_ALIGNMENT` on MASCO 4110, 4311, 3343).

---

## 2. Forensic Code & Configuration Inspection (Check A1)

Source code analysis of `src/sdg_aggregation_engine.py` (lines 610–685) reveals:
1. **Canonical Set Definition:**
   `cohort_relations: Set[Tuple[str, str, str]] = set()`
   Tuples are stored as `(profile_id, target_id, mapping_type)` where `mapping_type` is directly ingested from M5 without filtering or truncation.
2. **Tri-Partite Counting:**
   ```python
   total_direct = sum(1 for r in cohort_relations if r[2] == "DIRECT")
   total_enabling = sum(1 for r in cohort_relations if r[2] == "ENABLING")
   total_contextual = sum(1 for r in cohort_relations if r[2] == "CONTEXTUAL")

   direct_share = round(total_direct / total_relations, 4)
   enabling_share = round(total_enabling / total_relations, 4)
   contextual_share = round(total_contextual / total_relations, 4)
   ```
3. **Strict Sum Normalization:**
   ```python
   sum_shares = direct_share + enabling_share + contextual_share
   if sum_shares != 1.0 and total_contextual > 0:
       contextual_share = round(1.0 - direct_share - enabling_share, 4)
   elif sum_shares != 1.0 and total_enabling > 0:
       enabling_share = round(1.0 - direct_share - contextual_share, 4)
   ```
4. **Output Schema:** Emits `direct_count`, `enabling_count`, `contextual_count`, `direct_share`, `enabling_share`, `contextual_share`.

**Finding:** The engine implementation in `src/sdg_aggregation_engine.py` has always supported `CONTEXTUAL` mappings. The omission was solely in the Stage 14D narrative documentation text.

---

## 3. Canonical Relation Deduplication (Check A2)

$$R = \{(i, t, \tau) \mid i \in C_{\text{eligible}}, t \in \text{Target}(M5), \tau \in \{\text{DIRECT}, \text{ENABLING}, \text{CONTEXTUAL}\}\}$$

- **Entity Deduplication:** If an individual has multiple skills mapping to the same target with the same mapping type, exactly one $(i, t, \tau)$ is generated.
- **Type Separation:** If an individual has a DIRECT skill to target $t$ and a CONTEXTUAL skill to target $t$, both $(i, t, \text{DIRECT})$ and $(i, t, \text{CONTEXTUAL})$ are retained as distinct relations.

---

## 4. Mapping Shares Math (Check A3)

$$\text{Share}_{\text{direct}} = \frac{|R_{\text{DIRECT}}|}{|R|}, \quad \text{Share}_{\text{enabling}} = \frac{|R_{\text{ENABLING}}|}{|R|}, \quad \text{Share}_{\text{contextual}} = \frac{|R_{\text{CONTEXTUAL}}|}{|R|}$$
$$\text{Share}_{\text{direct}} + \text{Share}_{\text{enabling}} + \text{Share}_{\text{contextual}} \equiv 1.0000 \quad (\forall |R| > 0)$$

For zero-relation cohorts ($|R| = 0$), all shares evaluate to `0.0` with `status: "NO_ALIGNMENT_RELATIONS"`.

---

## 5. Contextual Fixture Execution (Check A4)

An explicit fixture containing 1 DIRECT, 1 ENABLING, and 1 CONTEXTUAL relation was evaluated:
- $|R| = 3$
- Direct Count = 1, Direct Share = 0.3333
- Enabling Count = 1, Enabling Share = 0.3333
- Contextual Count = 1, Contextual Share = 0.3334
- **Sum of Shares:** $0.3333 + 0.3333 + 0.3334 = 1.0000$ (PASS).

---

## 6. Beneficiary Alignment Preservation (Check A5)

Cohorts holding clerical roles (MASCO 4110, 4311, 3343) were evaluated:
- MASCO 4110 produces $(i, 8.5, \text{CONTEXTUAL})$.
- Mapping survived ingestion, deduplication, and aggregation.
- Output yielded:
  - Direct Share = 0.0
  - Enabling Share = 0.0
  - Contextual Share = 1.0000
- Quality flag `CONTEXTUAL_BENEFICIARY_ALIGNMENT_PRESENT` was successfully propagated to cohort output.
- Zero conversion to ENABLING or DIRECT.
