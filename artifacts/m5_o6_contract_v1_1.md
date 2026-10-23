# M5 to O6 Interface Contract Specification v1.1.0

**Contract Reference**: CONTRACT-M5-O6-v1.1.0  
**Upstream Engine**: M5 SDG Impact Mapping Engine v1.1.0  
**Downstream Consumer**: Output 6 (O6 Sustainability & ESG Analytics / Reporting Interface)  
**Status**: APPROVED & LOCKED  

---

## 1. System Boundary & Communication Topology

```
+-----------------------------------+
|  M4 Reskilling Pathway Engine     |
|  (Personalized Learning Pathways) |
+-----------------+-----------------+
                  |
                  | (Consumes pathway payload)
                  v
+-----------------------------------+
|  M5 SDG Impact Mapping Engine     |
|  (Evaluates targets & qualities)  |
+-----------------+-----------------+
                  |
                  | (Emits pure explanatory SDG annotations)
                  v
+-----------------------------------+
|  O6 Sustainability Reporting      |
|  (Downstream UI / Executive View) |
+-----------------------------------+
```

### Critical Operational Invariants:
1. **One-Way Unidirectional Flow**: Data flows strictly $M4 \to M5 \to O6$. O6 cannot alter M5 mappings, and M5 cannot alter M4 pathways or M3 role matches.
2. **Zero Feedback Loop**: M5 outputs MUST NEVER be used to re-rank, filter, or penalize career matches in M3 or courses in M4.
3. **No Synthetic Metric Inflation**: O6 is strictly prohibited from converting qualitative M5 alignments into fabricated quantitative claims (e.g. converting Target 13.2 alignment into "12.4 metric tons CO2 saved" or Target 8.5 into "3 jobs generated").

---

## 2. Input Specification (Payload Consumed by M5)

M5 accepts standard reskilling pathway objects from M4:

```json
{
  "pathway_id": "string (required, e.g. 'PATH_2529_001')",
  "target_role_code": "string (required, 4-digit MASCO code, e.g. '2529')",
  "target_role_title": "string (optional, e.g. 'Database and Network Professionals NEC')",
  "skills": ["string (canonical skill_id list, e.g. ['python_scripting', 'sql_data_analysis'])"],
  "modules": [
    {
      "module_id": "string",
      "skill_id": "string",
      "title": "string"
    }
  ]
}
```

---

## 3. Output Specification (Payload Emitted by M5 to O6)

`SDGImpactEngine.map_pathway_to_sdgs()` returns a standardized, target-traceable JSON payload:

```json
{
  "pathway_id": "PATH_2529_001",
  "engine_version": "1.1.0",
  "target_role_code": "2529",
  "target_role_title": "Database and Network Professionals NEC",
  "skills_analyzed_count": 4,
  "skills_analyzed": [
    "ai_ethics_governance",
    "carbon_footprint_analytics",
    "python_scripting",
    "sql_data_analysis"
  ],
  "total_sdgs_aligned": 4,
  "direct_sdgs": [12],
  "enabling_sdgs": [8, 9, 13, 16],
  "contextual_sdgs": [],
  "sector_dependent_sdgs": [],
  "beneficiary_aligned_sdgs": [],
  "pathway_quality_flags": [
    "DIRECT_SUSTAINABILITY_ROLE",
    "GENERAL_PURPOSE_SAFE",
    "OFFICIAL_TARGET_TRACEABLE",
    "TARGET_SEMANTIC_REMEDIATED"
  ],
  "sdg_alignments": [
    {
      "sdg_id": 12,
      "sdg_name": "Responsible Consumption and Production",
      "overall_mapping_type": "DIRECT",
      "targets_addressed": ["12.6"],
      "contributing_skills": ["carbon_footprint_analytics"],
      "role_aligned": false,
      "skill_aligned": true,
      "quality_flags": ["DIRECT_SUSTAINABILITY_ROLE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
      "direct_contributions_count": 1,
      "enabling_contributions_count": 0,
      "contextual_contributions_count": 0,
      "contributions": [
        {
          "source_type": "SKILL",
          "source_id": "carbon_footprint_analytics",
          "source_title": "Carbon Footprint Analytics & Accounting",
          "target_id": "12.6",
          "target_description": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
          "mapping_type": "DIRECT",
          "alignment_strength": "STRONG",
          "contribution_pathway": "Calculates organizational greenhouse gas balances and product lifecycle footprints for corporate sustainability reporting.",
          "evidence_references": "WRI/WBCSD GHG Protocol Corporate Standard; Bursa Malaysia Sustainability Reporting Guide; UN SDG Target 12.6.",
          "confidence": "HIGH",
          "quality_flags": ["DIRECT_SUSTAINABILITY_ROLE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"]
        }
      ]
    }
  ],
  "pathway_impact_narrative": "Pathway 'PATH_2529_001' prepares learners for 'Database and Network Professionals NEC' through 4 competencies. At the competency acquisition level, the curriculum delivers DIRECT capabilities advancing: SDG 12 (Responsible Consumption and Production). Acquired skills provide essential ENABLING tools supporting: SDG 8 (Decent Work and Economic Growth); SDG 9 (Industry, Innovation and Infrastructure); SDG 13 (Climate Action); SDG 16 (Peace, Justice and Strong Institutions). In the target occupational deployment horizon as 'Database and Network Professionals NEC', the role structurally anchors SDG 9 (Industry, Innovation and Infrastructure).",
  "methodology_disclaimer": "M5 SDG impact mapping represents qualitative and structural policy alignment grounded in the official UN 2030 indicator framework (anchored to 169 official UN targets). M5 does NOT produce synthetic quantitative measurements (such as metric tons of CO2 avoided or direct jobs generated). M5 operates as a downstream analytical lens and does not alter, bias, or restrict M3 role matching or M4 course recommendations."
}
```

---

## 4. O6 UI Presentation Guidelines

When O6 visualizes this data, the following UI presentation standards are mandatory:
1. **Tier Badge Visuals**:
   - `DIRECT`: Solid Green Badge ("Direct Core Contribution")
   - `ENABLING`: Blue Badge ("Enabling Technical Capability")
   - `CONTEXTUAL`: Gray Badge ("Contextual / Operational Support")
2. **Special Quality Indicators**:
   - `SECTOR_DEPENDENT_ALIGNMENT`: Yellow Amber Flag with tooltip ("Alignment depends on employment in clean energy or green environmental sectors").
   - `CONTEXTUAL_BENEFICIARY_ALIGNMENT`: Purple Informational Flag with tooltip ("Role represents employment participation under decent work standards rather than policy administration").
3. **Traceability Modals**:
   - Clicking any target badge must open the official UN target metadata, displaying official text, indicator ID, and source URL linking to `https://sdgs.un.org/goals`.
4. **Prominent Methodology Disclaimer**:
   - The disclaimer text provided in `methodology_disclaimer` must be displayed at the base of the sustainability dashboard card.
