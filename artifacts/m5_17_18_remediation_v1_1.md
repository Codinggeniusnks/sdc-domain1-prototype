# M5 Target 17.18 vs 9.5 Enterprise SQL Remediation Report v1.1.0

**Defect Reference**: P1-3 (Stage 13B Independent Review)  
**Competency In Question**: `sql_data_analysis` (SQL Data Querying & Relational Analysis)  
**UN SDG Standard**: Target 17.18 vs Target 9.5 & Target 8.2  
**Status**: APPROVED  

---

## 1. Taxonomic Misalignment in v1.0.0

In M5 v1.0.0, the general-purpose competency `sql_data_analysis` was mapped to:
- **Target 17.18**: "By 2020, enhance capacity-building support to developing countries, including for least developed countries and small island developing States, to increase significantly the availability of high-quality, timely and reliable data disaggregated by income, gender, age, race, ethnicity, migratory status, disability, geographic location and other characteristics relevant in national contexts."

### Critical Methodology Flaws in v1.0.0:
1. **International Development & Official Statistics Focus**:
   - Target 17.18 is situated under Goal 17 ("Partnerships for the Goals") and focuses exclusively on **Official Development Assistance (ODA)** and bilateral/multilateral statistical capacity-building.
   - Indicator 17.18.1 measures the proportion of sustainable development indicators produced at the national level with full disaggregation.
   - Indicator 17.18.2 measures whether a country has national statistical legislation that complies with the Fundamental Principles of Official Statistics.
   - Indicator 17.18.3 measures whether a country has a funded National Statistical Plan.
   - The target is designed to assist **National Statistical Offices (NSOs)**, such as the Department of Statistics Malaysia (DOSM), in conducting national censuses and macroeconomic accounts.
2. **Commercial Enterprise Reality**:
   - `sql_data_analysis` in the workforce involves querying relational tables (PostgreSQL, MySQL, SQL Server, BigQuery) for corporate KPI reporting, supply chain tracking, marketing funnel analysis, and financial reporting.
   - A business analyst writing `SELECT ... WHERE order_status = 'shipped'` in a private firm has zero causal link to international statistical capacity-building in LDCs or national census disaggregation.

---

## 2. Remediated Alignment to Targets 9.5 and 8.2

Under Stage 13C remediation, `sql_data_analysis` is correctly realigned to its true economic and technological functions:

### 1. Primary Alignment: Target 9.5 (`ENABLING`)
- **Target 9.5**: "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries..."
- **Evidentiary Basis**: Relational database querying is a foundational computational capability for empirical industrial R&D, data-driven product optimization, and technological modernization across industrial and service sectors.
- **Mapping Classification**:
  - `mapping_type`: `ENABLING` (General-Purpose Rule strictly enforced)
  - `alignment_strength`: `STRONG`
  - `confidence`: `HIGH`
  - `quality_flags`: `["GENERAL_PURPOSE_SAFE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"]`

### 2. Secondary Alignment: Target 8.2 (`ENABLING`)
- **Target 8.2**: "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation..."
- **Evidentiary Basis**: Structured SQL data analytics enables data-driven decision-making, operational process optimization, and labor productivity gains across commercial enterprises.
- **Mapping Classification**:
  - `mapping_type`: `ENABLING`
  - `alignment_strength`: `MODERATE`
  - `confidence`: `HIGH`
  - `quality_flags`: `["GENERAL_PURPOSE_SAFE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"]`

---

## 3. Automated Verification

Benchmark `BM11_TARGET_17_18_SQL_BOUNDARY` and unit test `test_p1_3_sql_target_9_5_reallocation` confirm:
1. Target 17.18 is 100% purged from `sql_data_analysis` and all other Domain 1 skills.
2. `sql_data_analysis` aligns to Target 9.5 and 8.2 as `ENABLING`, strictly complying with `RULE_GP_NON_DIRECT_STRICT`.
3. Automated verification returned `PASS` with zero regression findings.
