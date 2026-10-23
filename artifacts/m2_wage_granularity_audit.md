# M2 Wage Granularity and Measurement Audit (v1.1.0)

## Executive Summary

During the Stage 9C Argon Forensic Audit, Defect **P1-3** identified that wage indicators in M2 v1.0.0 could be misconstrued as granular, 4-digit occupational salary surveys, despite national Malaysian wage statistics only being published at the 1-digit Major Group level by the Department of Statistics Malaysia (DOSM).

In M2 v1.1.0, a comprehensive structural schema update was implemented:
1. Every occupational profile explicitly tags wage metrics as **`MAJOR_GROUP_CONTEXT`**.
2. Context labels (`wage_context_code`, `wage_context_label`, `source_measurement_level`) are attached directly to each profile.
3. Automated quality flags (`MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA`) are systematically emitted.
4. Downstream safety contracts strictly prohibit M3 Role Matching or M6 Scenario modeling from interpreting these values as role-specific salary offers.

---

## National Data Reality: OpenDOSM Formal Sector Wage Survey

In Malaysia, the authoritative official source for formal sector wages is the **Department of Statistics Malaysia (DOSM)**, published semi-annually through the OpenDOSM data platform (`table_wage_sector_occupation`).

Key empirical constraints:
- **Available Granularity**: 1-Digit MASCO Major Groups (Groups 1 through 9).
- **Sub-group / Unit-group Granularity (3-digit or 4-digit)**: **Not published** in official public time-series datasets due to sample size restrictions and statistical confidentiality.
- **Survey Scope**: Formal private and public sector wage recipients with EPF contributions.
- **Reporting Period**: Historical baseline (2020–2022) to latest published time series (2023–2025).

Therefore, any claim that an ML model has access to official 4-digit MASCO wage time series across all occupations in Malaysia is empirically false. M2 v1.1.0 reflects the authentic statistical reality.

---

## Complete 20 MASCO 4-Digit Occupation Wage Mapping Inventory

| MASCO Code | Occupation Title | Major Group | Major Group Name | Wage Granularity Level | Context Code | Quality Flags Emitted |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- |
| `1219` | Business Services & Admin Managers NEC | 1 | Managers | `MAJOR_GROUP_CONTEXT` | `MAJOR_1` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `1221` | Sales & Marketing Managers | 1 | Managers | `MAJOR_GROUP_CONTEXT` | `MAJOR_1` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `1330` | ICT Services Managers | 1 | Managers | `MAJOR_GROUP_CONTEXT` | `MAJOR_1` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2121` | Civil Engineers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2141` | Industrial & Production Engineers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2166` | Graphic & Multimedia Designers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2411` | Accountants & Auditors | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2412` | Financial & Investment Advisers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2422` | Policy Administration Professionals | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2424` | Training & Staff Development Professionals | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2511` | Systems Analysts | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2512` | Software Developers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2514` | Applications Programmers | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `2529` | Database & Network Professionals NEC | 2 | Professionals | `MAJOR_GROUP_CONTEXT` | `MAJOR_2` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `3115` | Mechanical Engineering Technicians | 3 | Technicians & Assoc. Prof. | `MAJOR_GROUP_CONTEXT` | `MAJOR_3` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `3322` | Commercial Sales Representatives | 3 | Technicians & Assoc. Prof. | `MAJOR_GROUP_CONTEXT` | `MAJOR_3` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `3341` | Office Supervisors | 3 | Technicians & Assoc. Prof. | `MAJOR_GROUP_CONTEXT` | `MAJOR_3` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `3343` | Administrative Secretaries | 3 | Technicians & Assoc. Prof. | `MAJOR_GROUP_CONTEXT` | `MAJOR_3` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `4110` | General Office Clerks | 4 | Clerical Support Workers | `MAJOR_GROUP_CONTEXT` | `MAJOR_4` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |
| `4311` | Accounting & Bookkeeping Clerks | 4 | Clerical Support Workers | `MAJOR_GROUP_CONTEXT` | `MAJOR_4` | `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA` |

---

## Contractual Safety Rules for Downstream Modules

### Rules for M3 (Role Matching Engine)
1. **No Absolute Compensation Estimation**: M3 must NOT use the wage momentum index to predict individual salaries or compensation packages.
2. **Contextual Scaling Only**: Wage index may only be used as a macro economic health multiplier for career pathway viability ($w_{\text{macro}} \le 0.15$).
3. **Mandatory UI Disclaimer**: Any user interface displaying wage momentum must display the tag: *"Indicator reflects broader Major Group wage growth (DOSM), not role-specific salary data."*

### Rules for M6 (Scenario Engine)
1. **Macro Shock Propagation**: Wage adjustments during scenario stress testing (e.g., AI adoption surge) apply uniformly at the Major Group level, preventing ungrounded role-level salary variance.
2. **Uncertainty Bounds**: Role projections must carry a minimum $\pm 15\%$ confidence interval for any economic impact estimate derived from wage indices.
