# M4 to M5 Reskilling Pathway Interface Contract: Final Ratification v1.1.0

**Contract Identifier**: CONTRACT-M4-M5-v1.1.0-FINAL  
**Upstream System**: M4 Personalised Reskilling Pathway Engine v1.1.0 (Frozen)  
**Downstream System**: M5 SDG Impact Mapping Engine v1.1.0 (Frozen)  
**Ratification Milestone**: Stage 13D Formal Freeze  
**Status**: RATIFIED & FROZEN  

---

## 1. Upstream Contract Guarantees (M4 $\to$ M5)

M4 emits reskilling pathways that adhere strictly to the following contract guarantees:
1. **Target Role Identification**: Every pathway specifies an unambiguous 4-digit MASCO code (`target_role_code`, e.g. `'2529'`, `'2512'`).
2. **Canonical Skill Set**: The pathway provides an explicit set of required competency tokens (`skills` or `modules[].skill_id`), all resolving to the 16 canonical skills.
3. **No Upstream SDG Influence**: M4 pathway construction, prerequisite topological sorting, and course selection are **100% blind to SDG alignments**. M4 never evaluates or filters courses based on SDG metadata.

---

## 2. Downstream Synthesis Guarantees (M5 $\to$ Consumers)

When M5 evaluates an M4 reskilling pathway via `SDGImpactEngine.map_pathway_to_sdgs(pathway)`, the engine enforces the following downstream safety guarantees:

### A. Separation of Competency Acquisition vs Occupational Deployment (Check 43)
M5 does not roll up skills and occupations into an undifferentiated SDG score. The synthesized narrative explicitly separates:
1. **Competency Acquisition Level**: Immediate capabilities gained through learning the specific pathway curriculum (e.g. acquiring `carbon_footprint_analytics` delivers direct corporate reporting capabilities under Target 12.6).
2. **Occupational Deployment Horizon**: Structural macro-level alignments associated with long-term employment in the target occupation (e.g. practicing as an Environmental Engineer under MASCO 2143), clearly noting any sector dependencies or beneficiary contexts.

### B. Course Completion Safety (Check 44)
Completing an online course or module is explicitly framed as **competency and capability acquisition**, never as direct creation of societal sustainability impact:
- Learning carbon accounting gives the learner the capability to ledger greenhouse gases. It does not reduce greenhouse gas emissions by itself.
- M5 output narratives and disclaimers strictly maintain this causal boundary.

### C. Resource Independence (Check 45)
M5 alignments are computed strictly over canonical competency IDs and MASCO codes:
- Changing course providers (e.g. Coursera vs edX vs FutureLearn).
- Changing course URLs.
- Changing pricing tiers (FREE vs FREE_TO_AUDIT vs PAID).
- Changing certificate status.
**Has exactly 0.0% effect on M5 SDG alignments.** M5 does not inspect resource commercial metadata.

### D. Upstream Score Isolation (Check 46)
The following M3 and M4 metrics have **zero weight, zero access, and zero influence** on M5 mappings:
- M3 Role Match Index (RMI)
- M3 Role Evidence Confidence
- M4 Dynamic Pathway Evidence Confidence
- M4 Total Estimated Learning Hours
- M4 Weekly Study Pace Assumptions

### E. Prohibition of Moral Ranking (Check 52)
A career pathway that aligns with 5 SDGs or has 2 DIRECT mappings **must never be ranked higher** in career guidance than a pathway that aligns with 1 SDG or has 0 DIRECT mappings. M5 operates purely as an explanatory and analytical lens; moral or ethical ranking of occupations is strictly prohibited.

---

## 3. Formal JSON Schema Contract

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "M4_M5_Pathway_Impact_Payload",
  "type": "object",
  "required": [
    "pathway_id",
    "engine_version",
    "target_role_code",
    "target_role_title",
    "skills_analyzed_count",
    "skills_analyzed",
    "total_sdgs_aligned",
    "direct_sdgs",
    "enabling_sdgs",
    "contextual_sdgs",
    "sector_dependent_sdgs",
    "beneficiary_aligned_sdgs",
    "pathway_quality_flags",
    "sdg_alignments",
    "pathway_impact_narrative",
    "methodology_disclaimer"
  ],
  "properties": {
    "engine_version": { "type": "string", "enum": ["1.1.0"] },
    "pathway_id": { "type": "string" },
    "target_role_code": { "type": "string", "pattern": "^[0-9]{4}$" },
    "target_role_title": { "type": "string" },
    "skills_analyzed_count": { "type": "integer", "minimum": 0 },
    "skills_analyzed": { "type": "array", "items": { "type": "string" } },
    "total_sdgs_aligned": { "type": "integer", "minimum": 0, "maximum": 17 },
    "direct_sdgs": { "type": "array", "items": { "type": "integer" } },
    "enabling_sdgs": { "type": "array", "items": { "type": "integer" } },
    "contextual_sdgs": { "type": "array", "items": { "type": "integer" } },
    "sector_dependent_sdgs": { "type": "array", "items": { "type": "integer" } },
    "beneficiary_aligned_sdgs": { "type": "array", "items": { "type": "integer" } },
    "pathway_quality_flags": { "type": "array", "items": { "type": "string" } },
    "pathway_impact_narrative": { "type": "string", "minLength": 50 },
    "methodology_disclaimer": { "type": "string", "minLength": 50 }
  }
}
```

---

## 4. Contract Freeze Status

CONTRACT-M4-M5-v1.1.0 is hereby certified as fully verified, safe, and **FORMALLY FROZEN**.
