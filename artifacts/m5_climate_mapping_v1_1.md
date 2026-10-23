# M5 Climate Action & ESG Mapping Specification v1.1.0

**Defect Reference**: P2-1 (Stage 13B Independent Review)  
**Competencies In Question**: `carbon_footprint_analytics`, `esg_sustainability_reporting`  
**UN SDG Standard**: SDG 12 (Target 12.6) vs SDG 13 (Target 13.2 & 13.3)  
**Status**: APPROVED  

---

## 1. Analysis of Defect P2-1

In M5 v1.0.0, `carbon_footprint_analytics` was mapped as follows:
- **Target 13.2**: `DIRECT` ("Integrate climate change measures into national policies, strategies and planning")
- **Target 13.3**: `ENABLING` ("Improve education, awareness-raising and human and institutional capacity on climate change mitigation, adaptation, impact reduction and early warning")
- **Target 12.6**: `ENABLING` ("Encourage companies... to integrate sustainability information into their reporting cycle")

### Critical Misattributions Identified in Review:
1. **Target 13.2 is Macro-Policy, Not Corporate Carbon Accounting**:
   - Indicator 13.2.1 evaluates whether a country has communicated an integrated policy, strategy, or plan to increase its ability to adapt to climate change and lower emissions (e.g. Nationally Determined Contributions under the Paris Agreement).
   - Enterprise Scope 1, 2, and 3 GHG accounting measures corporate operational emissions (factories, company fleets, purchased electricity, value chain logistics). A corporate carbon accountant calculating emissions for a supply chain is NOT drafting national adaptation plans or passing parliamentary climate acts.
   - Corporate carbon accounting is an **ENABLING** data input to national climate strategies, providing empirical bottom-up emissions datasets that inform macro planning.
2. **Target 12.6 is the Exact Semantic Home for Corporate Carbon Reporting**:
   - Indicator 12.6.1 directly measures the "Number of companies publishing sustainability reports."
   - Carbon accounting according to the GHG Protocol Corporate Standard directly generates the quantitative carbon and emissions disclosures mandated by sustainability reporting standards (e.g. Bursa Malaysia Sustainability Reporting Guide, ISSB S2 Climate-related Disclosures, GRI 305).
   - Therefore, Target 12.6 is the **DIRECT** alignment for carbon footprint analytics.
3. **Target 13.3 (Awareness & Education) is a Weak Stretch**:
   - Target 13.3 focuses on public climate awareness, school curricula, and community disaster early-warning capacity. Professional carbon ledgering and lifecycle analysis in a corporation does not align to public awareness campaigns.

---

## 2. Remediated Climate Alignment Architecture v1.1.0

Under Stage 13C remediation, both sustainability competencies are harmonized into a coherent, evidence-grounded framework:

### A. `carbon_footprint_analytics`
- **Primary SDG**: SDG 12
  - **Target 12.6 (`DIRECT`, `HIGH` confidence)**: Directly measures Scope 1, 2, and 3 GHG emissions according to the GHG Protocol, producing verified corporate disclosures required under Bursa Malaysia ESG Guide and ISSB S2.
- **Primary SDG**: SDG 13
  - **Target 13.2 (`ENABLING`, `HIGH` confidence)**: Provides granular, facility-level empirical emissions baselines that feed into sectoral decarbonization roadmaps (e.g. Malaysia National Energy Transition Roadmap - NETR) and national mitigation planning.
- **Purged Target**: Target 13.3 has been completely eliminated.

### B. `esg_sustainability_reporting`
- **Primary SDG**: SDG 12
  - **Target 12.6 (`DIRECT`, `HIGH` confidence)**: Authoring corporate ESG disclosure reports, materiality matrices, and sustainability filings according to Bursa Malaysia and IFRS Sustainability Disclosure Standards.
- **Primary SDG**: SDG 16
  - **Target 16.6 (`DIRECT`, `HIGH` confidence)**: Establishing corporate accountability, stakeholder transparency, and ethical governance standards.

---

## 3. Automated Invariant Verification

Benchmark `BM12_CARBON_ACCOUNTING_PRECISION` and unit test `test_p2_1_carbon_accounting_precision` verify:
1. `carbon_footprint_analytics` maps to Target 12.6 as `DIRECT`.
2. `carbon_footprint_analytics` maps to Target 13.2 as `ENABLING`.
3. Target 13.3 is 100% purged.
4. All checks returned `PASS` with zero violations.
