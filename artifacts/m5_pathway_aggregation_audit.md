# M5 Pathway SDG Aggregation Forensic Audit

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior Recommender-Systems Methodologist, Workforce-Impact Researcher  
**Code Evaluated:** `src/sdg_impact_engine.py` (`map_pathway_to_sdgs` method)

---

## 1. Audit Scope & Functional Invariants

The `map_pathway_to_sdgs()` function in `SDGImpactEngine` is responsible for ingesting an M4 reskilling pathway and synthesizing an integrated SDG profile. This audit tests the implementation against five critical functional invariants:

1. **Goal Deduplication:** Multiple skills mapping to the same goal (e.g. Python $\to$ 9.5 and SQL $\to$ 9.5) must not double-count the goal.
2. **Provenance & Source Attribution:** Every aggregated goal must preserve its exact contributing skills and target citations.
3. **Typology Hierarchy Preservation:** A goal with at least one `DIRECT` contribution must be classified as `DIRECT`, while goals with only enabling contributions remain `ENABLING`.
4. **Role vs. Skill Distinction:** Target role structural contributions must be explicitly distinguished from skill-level learning contributions.
5. **Zero Quantitative Metric Synthesis:** The engine must produce zero synthetic scores, carbon savings numbers, or job-creation counts.

---

## 2. Code Forensic Inspection

Inspection of `src/sdg_impact_engine.py` (lines 186–340):

```python
# Invariant 1 & 2: Goal Deduplication and Attribution
all_sdg_buckets = {}  # sdg_id -> dict
# Bucket tracks targets_addressed (set) and contributing_skills (set)
# Result: Deduplication is strictly enforced; sets prevent duplicate counting.

# Invariant 3: Typology Hierarchy
if len(b["direct_contributions"]) > 0:
    primary_type = "DIRECT"
    direct_sdg_ids.append(sdg_num)
elif len(b["enabling_contributions"]) > 0:
    primary_type = "ENABLING"
    enabling_sdg_ids.append(sdg_num)
else:
    primary_type = "CONTEXTUAL"
    contextual_sdg_ids.append(sdg_num)
# Result: Deterministic hierarchical resolution.

# Invariant 4: Role vs. Skill Distinction
entry = {
    "source_type": "ROLE" if is_role else "SKILL",
    "source_id": id,
    "source_title": title,
    ...
}
# Result: Role and skill contributions are tagged with source_type.

# Invariant 5: Zero Synthetic Metrics
# Result: Verified. Zero arithmetic operations on carbon, jobs, or percentages.
```

---

## 3. Dynamic Pathway Execution Trace

To verify runtime behavior, a diagnostic test was executed with a pathway targeting MASCO `2512` (Software Developer) with skills `[python_scripting, carbon_footprint_analytics, ai_ethics_governance]`:

| Evaluation Metric | Observed Result | Pass Criteria | Status |
| :--- | :---: | :---: | :---: |
| **Total SDGs Aligned** | 7 | Deduplicated list | **PASS** |
| **Direct SDGs Identified** | [12, 13, 16] | Correctly extracted from skills & role | **PASS** |
| **Enabling SDGs Identified** | [8, 9, 10, 17] | Correctly separated from direct | **PASS** |
| **Source Type Traceability** | 100% of contributions tagged | `source_type` $\in$ {SKILL, ROLE} | **PASS** |
| **Methodology Disclaimer** | Present and unaltered | $>50$ characters | **PASS** |
| **Synthetic Metric Check** | Keys `kg_co2`, `jobs_created`, `impact_score` = None | Zero synthetic metrics | **PASS** |

---

## 4. Nuance Identified: Role-to-Learner Equivalence Hazard

### Finding (P2 Calibration Observation):
When `map_pathway_to_sdgs` evaluates a pathway, it incorporates the **target role's primary SDGs** into the pathway's profile.
- *The Hazard:* A learner who takes a single introductory course on Python for an Environmental Engineering role could be presented with an output stating that the "pathway directly mitigates climate change (SDG 13)", even though the learner has only acquired basic coding.
- *Remediation Requirement:* The output JSON and narrative text must explicitly separate:
  1. **"Competencies Developed in this Pathway"** (Skill contributions).
  2. **"Target Career Horizon Alignment"** (Occupational structural contributions).
  This ensures learners understand that acquiring the skills prepares them for a role that has these contributions, rather than implying that completing an online course instantly captures carbon.

---

## 5. Audit Verdict

- **Core Aggregation Logic:** **VALID**.
- **Isolation & Anti-Hallucination:** **VERIFIED**.
- **Required Polish:** Clarify role horizon vs. current competency attribution in narrative synthesis.
