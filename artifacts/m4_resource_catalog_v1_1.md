# M4 Production Resource Catalog & Pricing Integrity v1.1.0

**Reference Milestone**: Stage 12C Remediation (Audit Finding M4-P2-02)  
**Target Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Status**: COMPLETE, AUDITED & ISOLATED

---

## 1. Audit Context & Fixture Purging

In M4 v1.0.0, the production catalog file `data/reskilling/learning_resources_v1.json` contained 38 resource entries, two of which were synthetic testing artifacts:
- `RES_LOWCOST_01` ("Practical Python for Automating Daily Tasks", RM99)
- `RES_VAR_01` ("Enterprise AI Strategy Masterclass", UNKNOWN pricing)

These items had been introduced during early bench-testing to exercise the `LOW_COST` and `UNKNOWN` cost aggregation logic. However, their inclusion in the production catalog violated production data hygiene and caused audit confusion regarding catalog truthfulness.

In Stage 12C, the production catalog has been completely purged of synthetic test fixtures. All test fixtures now reside exclusively in `tests/fixtures/m4_resource_pricing_fixtures.json` with an explicit `test_only = true` guard.

---

## 2. Production Catalog Overview (`learning_resources_v1_1.json`)

The production catalog contains exactly **36 verified, real-world learning resources** mapped across all 13 target domain skills.

### Cost Status Distribution

| Cost Classification | Count | Percentage | Description |
|:---|:---:|:---:|:---|
| **`FREE`** | **31** | 86.1% | Completely free access to full course materials, videos, and built-in exercises. |
| **`FREE_TO_AUDIT`** | **5** | 13.9% | Free access to all lectures and reading materials via Coursera / edX audit modes (optional paid certificate available). |
| **`LOW_COST`** | **0** | 0.0% | Zero synthetic low-cost entries in production; real courses are free or audit-free. |
| **`VARIABLE_PRICE`** | **0** | 0.0% | Zero variable price courses in production catalog. |
| **`UNKNOWN`** | **0** | 0.0% | 100% of production resources have verified pricing status. |
| **Total Production Resources** | **36** | **100.0%** | All 36 are live, verified courses with real institutional backing. |

---

## 3. Skill Coverage & Resource Allocation

| Skill ID | Skill Name | Live Resources | Primary Resource | Primary Provider | Cost Status |
|:---|:---|:---:|:---|:---|:---:|
| `prompt_engineering` | Prompt Engineering | 3 | ChatGPT Prompt Engineering for Developers | DeepLearning.AI | FREE |
| `ai_literacy` | AI Literacy & Principles | 4 | Elements of AI: Introduction to AI | University of Helsinki | FREE |
| `python_scripting` | Python Scripting | 3 | Python for Everybody | freeCodeCamp | FREE |
| `sql_data_analysis` | SQL Data Analysis | 3 | Google Data Analytics - SQL for Data Analysis | Alphabet (Google) | FREE_TO_AUDIT |
| `data_visualization` | Data Visualization | 3 | Data Analysis and Visualization with Power BI | Microsoft Learn | FREE |
| `process_mapping` | Process Mapping & BPMN | 2 | BPMN 2.0 Process Modeling Masterclass | Camunda Academy / OMG | FREE |
| `workflow_automation` | Workflow Automation | 2 | Zapier Getting Started with Automation | Zapier Inc. | FREE |
| `ai_agent_orchestration`| AI Agent Orchestration | 3 | Functions, Tools and Agents with LangChain | DeepLearning.AI | FREE |
| `cloud_infrastructure` | Cloud Infrastructure | 3 | Microsoft Azure Fundamentals (AZ-900) | Microsoft Learn | FREE |
| `data_governance_privacy`| Data Governance & Privacy | 3 | Panduan Asas Akta Perlindungan Data Peribadi 2010 | JPDP Malaysia | FREE |
| `esg_reporting` | ESG Carbon Accounting | 3 | Bursa Malaysia ESG Reporting Guide & Toolkit | Bursa Malaysia Berhad | FREE |
| `api_integration` | API Integration & Webhooks | 2 | Postman API Fundamentals Student Expert | Postman Academy | FREE |
| `critical_thinking_ai` | Critical Thinking in AI Era | 2 | Critical Thinking & Problem Solving | RIT via edX | FREE_TO_AUDIT |
| **Total** | **13 Skills Covered** | **36** | — | — | — |

Every skill possesses at least 2 verified resources, ensuring full redundancy for primary, alternative, and practice recommendations.

---

## 4. Isolated Test Fixture Manifest (`tests/fixtures/m4_resource_pricing_fixtures.json`)

To enable automated testing of paid and uncertain cost branches without compromising the production catalog, synthetic fixtures are isolated in the test directory:

```json
{
  "test_only": true,
  "description": "Synthetic testing fixtures for M4 cost aggregation logic (LOW_COST, UNKNOWN)",
  "total_fixtures": 2,
  "fixtures": [
    {
      "resource_id": "RES_LOWCOST_01",
      "title": "Practical Python for Automating Daily Tasks",
      "cost_status": "LOW_COST",
      "cost_amount_if_verified": 99.0,
      "currency": "MYR",
      "test_only": true,
      "fixture_type": "BENCHMARK_SYNTHETIC_TEST_FIXTURE"
    },
    {
      "resource_id": "RES_VAR_01",
      "title": "Enterprise AI Strategy Masterclass",
      "cost_status": "VARIABLE_PRICE",
      "cost_amount_if_verified": null,
      "currency": "MYR",
      "test_only": true,
      "fixture_type": "BENCHMARK_SYNTHETIC_TEST_FIXTURE"
    }
  ]
}
```

The unit test suite explicitly checks that `RES_LOWCOST_01` and `RES_VAR_01` do not appear anywhere in `learning_resources_v1_1.json`, guaranteeing strict separation of concerns.
