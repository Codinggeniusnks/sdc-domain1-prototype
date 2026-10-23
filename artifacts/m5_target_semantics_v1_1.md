# M5 Target Semantics Specification v1.1.0

**Document Reference**: M5-SEM-001  
**Standard**: UN 2030 Agenda for Sustainable Development (A/RES/71/313)  
**Scope**: Domain 1 Selected Relevant Targets (21 Targets Indexed from 169 Official Target Universe)  
**Status**: APPROVED  

---

## 1. UN Target Boundary Principles

M5 v1.1.0 establishes strict semantic boundary conditions for every SDG target referenced in skills, occupations, and learning pathways. To maintain rigorous evidence grounding, mappings must strictly conform to official UN indicator metadata rather than metaphorical or loose thematic associations.

### Core Boundary Rules:
1. **Target 9.c (Telecommunications Access)**: Strict physical connectivity mandate. Strictly restricted to terrestrial cellular base stations, submarine cables, satellite constellations, and broadband spectrum infrastructure. Prohibited from application to application software, cloud services, relational databases, REST APIs, and UI/UX design.
2. **Target 16.6 vs Target 16.10 (Governance vs Public Information)**:
   - Target 16.6 ("Develop effective, accountable and transparent institutions at all levels"): Governs internal institutional integrity, statutory compliance (e.g. PDPA 2010), audit mechanisms, and corporate governance.
   - Target 16.10 ("Ensure public access to information and protect fundamental freedoms"): Governs constitutional freedom of speech, journalist safety, and statutory Freedom of Information (FOI) laws providing public inspection of state archives. Commercial data privacy compliance under PDPA 2010 belongs to Target 16.6, not Target 16.10.
3. **Target 9.5 vs Target 17.18 (Domestic R&D vs International Statistical Capacity)**:
   - Target 9.5 ("Enhance scientific research, upgrade technological capabilities of industrial sectors"): Governs domestic industrial innovation, enterprise analytics, computational modeling, and technological upgrading.
   - Target 17.18 ("Enhance capacity-building support to developing countries... to increase significantly the availability of high-quality, timely and reliable data disaggregated by income, gender, age..."): Specifically denotes official development assistance (ODA) and multilateral capacity building for National Statistical Offices (NSOs, e.g. DOSM) conducting decennial population censuses and national accounts. Enterprise commercial SQL data querying belongs to Target 9.5 and Target 8.2, not Target 17.18.
4. **Target 12.6 vs Target 13.2 (Corporate Sustainability Reporting vs National Climate Policy)**:
   - Target 12.6 ("Encourage companies... to adopt sustainable practices and to integrate sustainability information into their reporting cycle"): Direct mandate for corporate ESG reporting, Scope 1/2/3 greenhouse gas accounting, and corporate sustainability disclosures.
   - Target 13.2 ("Integrate climate change measures into national policies, strategies and planning"): Governs macro-level state policies, Nationally Determined Contributions (NDCs), and national mitigation strategies. Enterprise carbon analytics provides an ENABLING evidentiary input to this target, not direct execution.

---

## 2. Complete Index of Domain-Relevant Targets in M5 v1.1.0

The 21 domain-relevant targets indexed in `data/sdg/sdg_targets_v1_1.json` are organized below with their official indicator anchors and permissible mapping types:

| Target ID | Official Target Summary | Primary Indicators | Permissible Mapping Types |
|---|---|---|---|
| **4.4** | Relevant technical/vocational skills for employment | 4.4.1 (ICT skills proportion) | DIRECT, ENABLING |
| **4.7** | Knowledge & skills for sustainable development | 4.7.1 (Mainstreaming sustainability education) | DIRECT, ENABLING |
| **7.1** | Universal access to affordable, modern energy | 7.1.1 (Electricity access), 7.1.2 (Clean fuels) | DIRECT (Clean Energy only), ENABLING |
| **7.2** | Substantially increase share of renewable energy | 7.2.1 (Renewable energy share in TFEC) | DIRECT (Clean Energy only), ENABLING |
| **8.2** | Economic productivity through diversification & tech upgrading | 8.2.1 (Real GDP per employed person growth) | DIRECT, ENABLING |
| **8.5** | Full, productive employment and decent work for all | 8.5.1 (Average hourly earnings), 8.5.2 (Unemployment) | DIRECT (Labor Policy only), CONTEXTUAL (Beneficiary) |
| **8.8** | Protect labor rights and safe working environments | 8.8.1 (Occupational injuries), 8.8.2 (Labor rights compliance) | DIRECT, ENABLING |
| **9.1** | Develop quality, reliable, resilient infrastructure | 9.1.1 (Rural population access), 9.1.2 (Passenger/freight volumes) | DIRECT, ENABLING |
| **9.2** | Promote inclusive and sustainable industrialization | 9.2.1 (Manufacturing value added), 9.2.2 (Manufacturing employment) | DIRECT, ENABLING |
| **9.4** | Upgrade infrastructure & retrofit industries for sustainability | 9.4.1 (CO2 emission per unit of value added) | DIRECT, ENABLING |
| **9.5** | Enhance scientific research & technological capabilities | 9.5.1 (R&D expenditure % GDP), 9.5.2 (Researchers per million) | DIRECT, ENABLING |
| **10.2** | Empower and promote social, economic and political inclusion | 10.2.1 (Proportion living below 50% median income) | ENABLING, CONTEXTUAL |
| **11.2** | Safe, affordable, accessible and sustainable transport systems | 11.2.1 (Public transport access) | DIRECT, ENABLING |
| **11.6** | Reduce adverse per capita environmental impact of cities | 11.6.1 (Municipal solid waste), 11.6.2 (Urban fine particulate matter) | DIRECT, ENABLING |
| **12.2** | Sustainable management and efficient use of natural resources | 12.2.1 (Material footprint), 12.2.2 (Domestic material consumption) | DIRECT, ENABLING |
| **12.5** | Substantially reduce waste generation through circularity | 12.5.1 (National recycling rate) | DIRECT, ENABLING |
| **12.6** | Encourage companies to adopt sustainable practices & ESG reporting | 12.6.1 (Number of companies publishing sustainability reports) | DIRECT, ENABLING |
| **13.1** | Strengthen resilience to climate-related hazards | 13.1.1 (Deaths/missing from disasters) | DIRECT, ENABLING |
| **13.2** | Integrate climate change measures into national policies | 13.2.1 (National adaptation plans & NDCs) | DIRECT (Policy Roles), ENABLING |
| **16.6** | Develop effective, accountable and transparent institutions | 16.6.1 (Government expenditure vs budget), 16.6.2 (Satisfaction with public services) | DIRECT, ENABLING |
| **16.7** | Ensure responsive, inclusive, participatory decision-making | 16.7.1 (Proportions in public institutions), 16.7.2 (Population feeling decision-making inclusive) | DIRECT, ENABLING |

---

## 3. General-Purpose Skill Non-DIRECT Invariant (`RULE_GP_NON_DIRECT_STRICT`)

A cornerstone principle of M5 v1.1.0 is that general-purpose, horizontal computational skills:
- `python_scripting`
- `sql_data_analysis`
- `api_integration`
- `prompt_engineering`
- `workflow_automation`

cannot be assigned a `DIRECT` mapping to any SDG target. Because these computational skills are inherently dual-use—deployable in fossil-fuel extraction, high-frequency speculative trading, carbon-intensive manufacturing, or neutral administration just as easily as green tech—they are strictly classified as `ENABLING` or `CONTEXTUAL`.
