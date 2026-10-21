"""Reviewed skill taxonomy, future role catalog, SDG mappings, scenarios, and synthetic profiles.

All AI/market signal extraction is strictly constrained to the skills and roles defined in this
reviewed catalog so the system never invents jobs, courses, statistics, or unsupported claims.
"""

from __future__ import annotations

SKILLS_CATALOG: dict[str, dict] = {
    "ai_literacy": {
        "id": "ai_literacy",
        "name": "Foundational AI Literacy & LLM Capabilities",
        "category": "AI Core",
        "keywords": ["artificial intelligence", "large language model", "llm", "generative ai", "ai literacy", "foundation model"],
        "sdg_tags": ["SDG 4.4", "SDG 8.2"],
        "pathway_step": {
            "stage": 1,
            "objective": "Understand generative AI capabilities, hallucination limits, and safe workplace usage.",
            "resource_title": "AI Untuk Rakyat (MyDIGITAL & MDEC National Self-Paced Programme) / Elements of AI",
            "resource_url": "https://www.ai.gov.my/",
            "cost_tier": "Free (Verified Public National Initiative)",
            "estimated_hours": 6,
            "estimated_weeks": 1,
            "verification_status": "Verified public Malaysian government initiative (AI Untuk Rakyat).",
        },
    },
    "prompt_engineering": {
        "id": "prompt_engineering",
        "name": "Structured Prompting & Context Engineering",
        "category": "AI Core",
        "keywords": ["prompt", "in-context learning", "context engineering", "instruction tuning", "few-shot", "chain-of-thought"],
        "sdg_tags": ["SDG 4.4", "SDG 8.2"],
        "pathway_step": {
            "stage": 1,
            "objective": "Design reproducible, schema-constrained prompts with explicit verification rubrics.",
            "resource_title": "Skill Objective: Structured Prompt & Rubric Design (HRD Corp e-LATiH / Open Documentation)",
            "resource_url": "https://elatih.hrdcorp.gov.my/",
            "cost_tier": "Free (HRD Corp e-LATiH Public Portal)",
            "estimated_hours": 10,
            "estimated_weeks": 1,
            "verification_status": "Verified platform (HRD Corp e-LATiH); specific module taken as skill objective.",
        },
    },
    "process_mapping": {
        "id": "process_mapping",
        "name": "Business Process Mapping & SOP Design",
        "category": "Operations",
        "keywords": ["business process", "workflow", "process mining", "sop", "task decomposition", "enterprise operations"],
        "sdg_tags": ["SDG 8.2", "SDG 9.4"],
        "pathway_step": {
            "stage": 1,
            "objective": "Deconstruct manual workplace workflows into auditable human vs. AI-assisted steps.",
            "resource_title": "Skill Objective: Operational Workflow Mapping & Bottleneck Analysis (e-LATiH)",
            "resource_url": "https://elatih.hrdcorp.gov.my/",
            "cost_tier": "Free / Low-Cost Skill Objective",
            "estimated_hours": 8,
            "estimated_weeks": 1,
            "verification_status": "Skill objective (no commercial course price invented).",
        },
    },
    "sql_data_analysis": {
        "id": "sql_data_analysis",
        "name": "SQL & Structured Data Analysis",
        "category": "Data & Engineering",
        "keywords": ["sql", "database", "tabular data", "text-to-sql", "data analysis", "data analytics"],
        "sdg_tags": ["SDG 4.4", "SDG 8.2", "SDG 9.5"],
        "pathway_step": {
            "stage": 2,
            "objective": "Query relational datasets, audit missing values, and validate KPI baselines reproducibly.",
            "resource_title": "PostgreSQL / SQLite Official Documentation & Interactive SQL Exercises",
            "resource_url": "https://www.postgresql.org/docs/current/tutorial.html",
            "cost_tier": "Free (Open-Source Official Documentation)",
            "estimated_hours": 16,
            "estimated_weeks": 2,
            "verification_status": "Verified open-source documentation.",
        },
    },
    "python_scripting": {
        "id": "python_scripting",
        "name": "Python Scripting & Data Automation",
        "category": "Data & Engineering",
        "keywords": ["python", "scripting", "code generation", "software engineering"],
        "sdg_tags": ["SDG 4.4", "SDG 8.2", "SDG 9.5"],
        "pathway_step": {
            "stage": 2,
            "objective": "Write modular Python scripts for data validation, API requests, and automated testing.",
            "resource_title": "Official Python 3 Tutorial & Standard Library Reference",
            "resource_url": "https://docs.python.org/3/tutorial/",
            "cost_tier": "Free (Official Open Documentation)",
            "estimated_hours": 24,
            "estimated_weeks": 3,
            "verification_status": "Verified official Python documentation.",
        },
    },
    "data_visualization": {
        "id": "data_visualization",
        "name": "Data Visualization & KPI Storytelling",
        "category": "Operations",
        "keywords": ["data visualization", "visualization", "dashboard", "dashboards", "chart", "charts"],
        "sdg_tags": ["SDG 4.4", "SDG 8.2"],
        "pathway_step": {
            "stage": 2,
            "objective": "Communicate uncertainty intervals, baselines, and operational KPIs clearly to stakeholders.",
            "resource_title": "Skill Objective: Evidence-Based Dashboard & Uncertainty Reporting",
            "resource_url": "https://elatih.hrdcorp.gov.my/",
            "cost_tier": "Free / Low-Cost Skill Objective",
            "estimated_hours": 12,
            "estimated_weeks": 2,
            "verification_status": "Skill objective aligned with HRD Corp e-LATiH data literacy tracks.",
        },
    },
    "workflow_automation": {
        "id": "workflow_automation",
        "name": "Agentic Workflow Orchestration & Tool Integration",
        "category": "AI Core",
        "keywords": ["agentic", "ai agent", "ai agents", "llm agent", "llm agents", "multi-agent", "agent orchestration", "tool use", "workflow automation"],
        "sdg_tags": ["SDG 8.2", "SDG 9.5"],
        "pathway_step": {
            "stage": 3,
            "objective": "Chain bounded AI tool calls with deterministic fallback and human approval checkpoints.",
            "resource_title": "Skill Objective: Human-in-the-Loop AI Workflow Orchestration & Fallback Design",
            "resource_url": "https://www.nist.gov/itl/ai-risk-management-framework",
            "cost_tier": "Free (Open Technical Guidelines & Hands-on Lab Objective)",
            "estimated_hours": 18,
            "estimated_weeks": 2,
            "verification_status": "Skill objective grounded in open engineering standards.",
        },
    },
    "human_in_the_loop_qa": {
        "id": "human_in_the_loop_qa",
        "name": "Human-in-the-Loop Evaluation & AI Testing",
        "category": "Governance & QA",
        "keywords": ["llm evaluation", "model evaluation", "hallucination", "hallucinations", "red teaming", "red-teaming", "human-in-the-loop", "human oversight"],
        "sdg_tags": ["SDG 8.5", "SDG 9.5", "SDG 16.6"],
        "pathway_step": {
            "stage": 3,
            "objective": "Build gold-standard evaluation sets, detect AI hallucinations, and enforce guardrails.",
            "resource_title": "NIST AI Risk Management Framework (AI RMF 1.0) â€” Measure & Verify Playbook",
            "resource_url": "https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook",
            "cost_tier": "Free (Public Standard Playbook)",
            "estimated_hours": 14,
            "estimated_weeks": 2,
            "verification_status": "Verified public standard documentation.",
        },
    },
    "rag_knowledge_systems": {
        "id": "rag_knowledge_systems",
        "name": "Retrieval-Augmented Generation (RAG) & Citation Grounding",
        "category": "Data & Engineering",
        "keywords": ["retrieval-augmented", "retrieval augmented", "rag", "vector database", "knowledge graph", "information retrieval"],
        "sdg_tags": ["SDG 4.4", "SDG 9.5"],
        "pathway_step": {
            "stage": 3,
            "objective": "Index dated organizational documents and enforce strict source-citation grounding.",
            "resource_title": "Skill Objective: Source-Grounded Retrieval & Citation Verification Pipeline",
            "resource_url": "https://docs.python.org/3/",
            "cost_tier": "Free (Open-Source Implementation Objective)",
            "estimated_hours": 20,
            "estimated_weeks": 3,
            "verification_status": "Skill objective (hands-on project build).",
        },
    },
    "api_integration": {
        "id": "api_integration",
        "name": "REST API Integration & Resilient Fallbacks",
        "category": "Data & Engineering",
        "keywords": ["api", "apis", "rest api", "endpoint", "microservice", "microservices"],
        "sdg_tags": ["SDG 9.5"],
        "pathway_step": {
            "stage": 2,
            "objective": "Integrate external JSON/XML data feeds with schema validation, timeouts, and snapshot fallbacks.",
            "resource_title": "MDN Web Docs â€” HTTP & REST API Architecture Guides",
            "resource_url": "https://developer.mozilla.org/en-US/docs/Web/HTTP",
            "cost_tier": "Free (Verified Open Web Documentation)",
            "estimated_hours": 12,
            "estimated_weeks": 2,
            "verification_status": "Verified open documentation.",
        },
    },
    "ai_ethics_governance": {
        "id": "ai_ethics_governance",
        "name": "AI Ethics, Fairness Auditing & Governance",
        "category": "Governance & QA",
        "keywords": ["ai ethics", "ethics", "fairness", "algorithmic bias", "ai governance", "governance", "accountability", "explainability", "ai safety"],
        "sdg_tags": ["SDG 5.5", "SDG 8.5", "SDG 10.3", "SDG 16.6"],
        "pathway_step": {
            "stage": 3,
            "objective": "Audit AI systems for demographic fairness, transparency, and compliance with Malaysia's National Guidelines on AI Governance & Ethics (AIGE).",
            "resource_title": "Malaysia National Guidelines on AI Governance & Ethics (MOSTI) & UNESCO AI Ethics",
            "resource_url": "https://www.mosti.gov.my/",
            "cost_tier": "Free (Public Policy & Governance Framework)",
            "estimated_hours": 10,
            "estimated_weeks": 1,
            "verification_status": "Verified Malaysian MOSTI policy framework reference.",
        },
    },
    "data_privacy_pdpa": {
        "id": "data_privacy_pdpa",
        "name": "Data Privacy & Malaysian PDPA Compliance",
        "category": "Governance & QA",
        "keywords": ["privacy", "pdpa", "personal data", "anonymization", "synthetic data", "data protection"],
        "sdg_tags": ["SDG 8.8", "SDG 16.6"],
        "pathway_step": {
            "stage": 2,
            "objective": "Apply data minimization, synthetic test profiling, and Personal Data Protection Act (PDPA) controls.",
            "resource_title": "OWASP Top 10 for Large Language Model Applications & PDPA Compliance Objective",
            "resource_url": "https://genai.owasp.org/",
            "cost_tier": "Free (Open Security Standard)",
            "estimated_hours": 10,
            "estimated_weeks": 1,
            "verification_status": "Verified OWASP open-source security guidance.",
        },
    },
    "esg_sustainability_reporting": {
        "id": "esg_sustainability_reporting",
        "name": "ESG Frameworks & UN SDG Impact Mapping",
        "category": "Sustainability",
        "keywords": ["sustainability", "sdg", "sdgs", "climate", "esg", "renewable", "emissions"],
        "sdg_tags": ["SDG 7.3", "SDG 12.6", "SDG 13.2"],
        "pathway_step": {
            "stage": 2,
            "objective": "Map operational and digital initiatives to UN SDG targets and quantifiable sustainability KPIs.",
            "resource_title": "UN CC:e-Learn (United Nations Climate Change Learning Partnership) Free Courses",
            "resource_url": "https://www.uncclearn.org/",
            "cost_tier": "Free (Official UN Learning Platform)",
            "estimated_hours": 12,
            "estimated_weeks": 2,
            "verification_status": "Verified United Nations public learning platform.",
        },
    },
    "carbon_footprint_analytics": {
        "id": "carbon_footprint_analytics",
        "name": "Carbon-Aware Compute & Resource Telemetry",
        "category": "Sustainability",
        "keywords": ["carbon", "carbon footprint", "energy consumption", "energy efficiency", "green ai", "green computing"],
        "sdg_tags": ["SDG 7.3", "SDG 9.4", "SDG 13.2"],
        "pathway_step": {
            "stage": 3,
            "objective": "Measure compute energy efficiency and right-size AI workloads (CPU vs. GPU).",
            "resource_title": "Green Software Foundation â€” Green Software Practitioner (Free Linux Foundation Course)",
            "resource_url": "https://learn.greensoftware.foundation/",
            "cost_tier": "Free (Verified Open Industry Curriculum)",
            "estimated_hours": 8,
            "estimated_weeks": 1,
            "verification_status": "Verified free practitioner curriculum by Green Software Foundation.",
        },
    },
    "stakeholder_communication": {
        "id": "stakeholder_communication",
        "name": "Human-Centred Change & Stakeholder Communication",
        "category": "Operations",
        "keywords": ["stakeholder", "stakeholders", "human-centered", "human-centred", "decision support", "science communication"],
        "sdg_tags": ["SDG 4.3", "SDG 8.5"],
        "pathway_step": {
            "stage": 1,
            "objective": "Facilitate human-in-charge career and operational decisions alongside AI recommendations.",
            "resource_title": "Skill Objective: Human-Centred AI Change Management & Advisory Communication",
            "resource_url": "https://elatih.hrdcorp.gov.my/",
            "cost_tier": "Free / Low-Cost Skill Objective",
            "estimated_hours": 8,
            "estimated_weeks": 1,
            "verification_status": "Skill objective.",
        },
    },
    "instructional_design": {
        "id": "instructional_design",
        "name": "Competency Matrix & Reskilling Curriculum Design",
        "category": "Operations",
        "keywords": ["curriculum", "reskilling", "upskilling", "workforce training", "vocational", "education", "competency", "lifelong learning"],
        "sdg_tags": ["SDG 4.3", "SDG 4.4", "SDG 8.5"],
        "pathway_step": {
            "stage": 3,
            "objective": "Structure modular adult reskilling pathways mapped to Malaysia's TVET and HRD Corp frameworks.",
            "resource_title": "UNESCO-UNEVOC TVET & Digital Competency Frameworks (Open Resource)",
            "resource_url": "https://unevoc.unesco.org/",
            "cost_tier": "Free (Official UNESCO Open Resource)",
            "estimated_hours": 12,
            "estimated_weeks": 2,
            "verification_status": "Verified UNESCO-UNEVOC public framework.",
        },
    },
}


ROLES_CATALOG: dict[str, dict] = {
    "ai_workflow_specialist": {
        "id": "ai_workflow_specialist",
        "title": "AI Workflow & Operations Specialist",
        "category": "Operations & Productivity",
        "summary": "Redesigns routine administrative, reporting, and customer operations into audited human-in-the-loop AI workflows.",
        "required_skills": [
            "ai_literacy",
            "prompt_engineering",
            "process_mapping",
            "workflow_automation",
            "human_in_the_loop_qa",
        ],
        "supporting_skills": [
            "sql_data_analysis",
            "data_visualization",
            "stakeholder_communication",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 8 â€” Decent Work and Economic Growth",
                "target": "Target 8.2",
                "explanation": "Achieves higher economic productivity through technological upgrading and human-centred workflow innovation rather than worker replacement.",
            },
            {
                "sdg": "SDG 4 â€” Quality Education",
                "target": "Target 4.4",
                "explanation": "Equips administrative and operational workers with relevant digital and AI orchestration skills for decent jobs.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 1.00,
            "fast_agentic": 1.15,
            "sdg_green_push": 0.95,
        },
        "uncertainty_note": "No hiring-demand data is used; tool interfaces evolve rapidly; durable value lies in process mapping and QA rather than vendor-specific prompts.",
    },
    "llm_quality_evaluator": {
        "id": "llm_quality_evaluator",
        "title": "AI Evaluation & Quality Assurance Specialist",
        "category": "Engineering & QA",
        "summary": "Designs test suites, hallucination audits, and citation-grounding benchmarks for enterprise AI applications.",
        "required_skills": [
            "ai_literacy",
            "human_in_the_loop_qa",
            "prompt_engineering",
            "sql_data_analysis",
            "python_scripting",
        ],
        "supporting_skills": [
            "ai_ethics_governance",
            "rag_knowledge_systems",
            "api_integration",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 9 â€” Industry, Innovation and Infrastructure",
                "target": "Target 9.5",
                "explanation": "Strengthens technological reliability and scientific validation of deployed AI systems.",
            },
            {
                "sdg": "SDG 8 â€” Decent Work and Economic Growth",
                "target": "Target 8.5",
                "explanation": "Transitions traditional manual QA and support testers into higher-value AI verification roles.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 1.00,
            "fast_agentic": 1.20,
            "sdg_green_push": 1.00,
        },
        "uncertainty_note": "As automated code and text generation rises, verification bottlenecks grow; requires continuous upskilling in statistical evaluation.",
    },
    "ai_governance_auditor": {
        "id": "ai_governance_auditor",
        "title": "AI Governance, Privacy & Fairness Analyst",
        "category": "Governance, Risk & Compliance",
        "summary": "Audits AI deployments for Malaysian PDPA privacy compliance, demographic fairness, source traceability, and MOSTI AI ethics alignment.",
        "required_skills": [
            "ai_literacy",
            "ai_ethics_governance",
            "data_privacy_pdpa",
            "human_in_the_loop_qa",
            "stakeholder_communication",
        ],
        "supporting_skills": [
            "process_mapping",
            "sql_data_analysis",
            "esg_sustainability_reporting",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 16 â€” Peace, Justice and Strong Institutions",
                "target": "Target 16.6",
                "explanation": "Develops effective, accountable, and transparent institutional guardrails for automated decision-support systems.",
            },
            {
                "sdg": "SDG 10 â€” Reduced Inequalities",
                "target": "Target 10.3",
                "explanation": "Audits recruitment and workforce algorithms to prevent discriminatory outcomes across age, gender, or background.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 0.95,
            "fast_agentic": 1.15,
            "sdg_green_push": 1.15,
        },
        "uncertainty_note": "Regulatory timelines vary across ASEAN jurisdictions; this prototype has no vacancy data on which sectors hire for this role.",
    },
    "rag_knowledge_engineer": {
        "id": "rag_knowledge_engineer",
        "title": "Knowledge Systems & RAG Pipeline Engineer",
        "category": "Data & Engineering",
        "summary": "Builds source-grounded retrieval pipelines that connect verified organizational data to AI assistants without hallucination.",
        "required_skills": [
            "python_scripting",
            "sql_data_analysis",
            "rag_knowledge_systems",
            "api_integration",
            "human_in_the_loop_qa",
        ],
        "supporting_skills": [
            "ai_literacy",
            "prompt_engineering",
            "data_privacy_pdpa",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 9 â€” Industry, Innovation and Infrastructure",
                "target": "Target 9.5",
                "explanation": "Upgrades digital knowledge infrastructure and technical capabilities across industrial sectors.",
            },
            {
                "sdg": "SDG 4 â€” Quality Education",
                "target": "Target 4.3",
                "explanation": "Enables accessible, citation-backed technical knowledge retrieval for lifelong learners.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 1.05,
            "fast_agentic": 1.10,
            "sdg_green_push": 0.95,
        },
        "uncertainty_note": "Requires stronger programming fundamentals (Python, SQL, APIs); commodity vector search is maturing into broader data-quality engineering.",
    },
    "sustainable_ai_analyst": {
        "id": "sustainable_ai_analyst",
        "title": "Sustainable AI & ESG Telemetry Analyst",
        "category": "Sustainability & Green Tech",
        "summary": "Tracks compute energy efficiency, carbon footprints, and SDG/ESG data pipelines for green digital transformation.",
        "required_skills": [
            "esg_sustainability_reporting",
            "carbon_footprint_analytics",
            "sql_data_analysis",
            "data_visualization",
            "ai_literacy",
        ],
        "supporting_skills": [
            "python_scripting",
            "ai_ethics_governance",
            "stakeholder_communication",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 13 â€” Climate Action",
                "target": "Target 13.2",
                "explanation": "Integrates climate-change and carbon-intensity metrics directly into corporate IT and AI operations.",
            },
            {
                "sdg": "SDG 7 â€” Affordable and Clean Energy",
                "target": "Target 7.3",
                "explanation": "Improves computational energy efficiency by right-sizing models and avoiding unnecessary GPU workloads.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 0.95,
            "fast_agentic": 0.95,
            "sdg_green_push": 1.30,
        },
        "uncertainty_note": "Team assumption (not measured): relevance depends on Bursa Malaysia / ASEAN ESG reporting timelines; no vacancy data is used.",
    },
    "workforce_reskilling_strategist": {
        "id": "workforce_reskilling_strategist",
        "title": "Workforce AI Reskilling & L&D Strategist",
        "category": "Human Capital & TVET",
        "summary": "Maps team-wide skill gaps and designs inclusive, HRD Corp-aligned reskilling pathways for displaced or transitioning workers.",
        "required_skills": [
            "ai_literacy",
            "instructional_design",
            "stakeholder_communication",
            "process_mapping",
            "ai_ethics_governance",
        ],
        "supporting_skills": [
            "data_visualization",
            "prompt_engineering",
            "data_privacy_pdpa",
        ],
        "sdg_links": [
            {
                "sdg": "SDG 4 â€” Quality Education",
                "target": "Target 4.3 & Target 4.4",
                "explanation": "Expands lifelong technical and vocational reskilling pathways for working adults and graduates.",
            },
            {
                "sdg": "SDG 8 â€” Decent Work and Economic Growth",
                "target": "Target 8.5",
                "explanation": "Supports full and productive employment during technological transitions by keeping humans in charge of career paths.",
            },
        ],
        "scenario_weights": {
            "moderate_copilot": 1.00,
            "fast_agentic": 1.10,
            "sdg_green_push": 1.10,
        },
        "uncertainty_note": "Directly addresses Malaysia's gap where 56% use AI at work but only 26% have formal training (Hays 2025, as quoted in the Domain 1 brief); impact depends on employer training budgets.",
    },
}


SCENARIOS: dict[str, dict] = {
    "moderate_copilot": {
        "id": "moderate_copilot",
        "name": "Scenario A: Moderate Co-Pilot Adoption (Baseline 2026â€“2028)",
        "badge": "Baseline Estimate",
        "assumptions": (
            "Assumes gradual enterprise adoption where AI acts as an assistive co-pilot inside existing roles. "
            "Employers prioritize foundational AI literacy, SQL/data analysis, and structured prompting while keeping "
            "existing job structures largely intact."
        ),
        "uncertainty_level": "Moderate (Â±10% score sensitivity)",
        "skill_boosts": {
            "ai_literacy": 1.15,
            "prompt_engineering": 1.15,
            "sql_data_analysis": 1.10,
            "process_mapping": 1.10,
        },
    },
    "fast_agentic": {
        "id": "fast_agentic",
        "name": "Scenario B: Fast Agentic Disruption (Rapid Task Automation)",
        "badge": "High Disruption Stress-Test",
        "assumptions": (
            "Assumes multi-step AI agents automate routine reporting, basic coding, and tier-1 support within 18â€“36 months "
            "(aligning with MOSTI's 600,000 reskilling warning). Demand shifts sharply toward human-in-the-loop QA, "
            "agentic workflow orchestration, RAG citation grounding, and AI governance."
        ),
        "uncertainty_level": "High (Â±20% score sensitivity â€” regulatory & reliability bottlenecks may slow deployment)",
        "skill_boosts": {
            "workflow_automation": 1.35,
            "human_in_the_loop_qa": 1.35,
            "rag_knowledge_systems": 1.25,
            "ai_ethics_governance": 1.25,
        },
    },
    "sdg_green_push": {
        "id": "sdg_green_push",
        "name": "Scenario C: Accelerated SDG & Green-Tech Transition",
        "badge": "Sustainability & Policy Push",
        "assumptions": (
            "Assumes stricter ASEAN ESG disclosure mandates, green cloud/compute efficiency targets, and Malaysia National "
            "AI Governance & Ethics (AIGE) enforcement. Roles combining AI literacy with ESG telemetry, carbon analytics, "
            "and inclusive workforce reskilling rise to the top."
        ),
        "uncertainty_level": "Moderate-High (Â±15% score sensitivity â€” depends on policy enforcement timelines)",
        "skill_boosts": {
            "esg_sustainability_reporting": 1.40,
            "carbon_footprint_analytics": 1.40,
            "ai_ethics_governance": 1.25,
            "instructional_design": 1.20,
        },
    },
}


SYNTHETIC_PROFILES: list[dict] = [
    {
        "id": "aisyah_ops",
        "name": "Aisyah Rahman (Synthetic Profile)",
        "current_role": "Junior Operations & Reporting Executive (3 yrs experience, Selangor)",
        "persona_type": "Working Adult at Risk of Routine Task Displacement",
        "background_summary": (
            "Synthetic persona: Prepares weekly spreadsheet and SQL operations reports, documents SOPs, and coordinates "
            "cross-team handoffs. Uses chat AI informally at work (part of the 56% in Hays 2025) but has no formal AI training."
        ),
        "skills": [
            "process_mapping",
            "sql_data_analysis",
            "data_visualization",
            "stakeholder_communication",
            "ai_literacy",
        ],
        "interests": ["Operations & Productivity", "Human Capital & TVET", "Governance, Risk & Compliance"],
    },
    {
        "id": "weijie_qa",
        "name": "Tan Wei Jie (Synthetic Profile)",
        "current_role": "Entry-Level Software QA & Support Analyst (1 yr experience, Penang)",
        "persona_type": "Fresh Graduate / Early-Career Tech Switcher",
        "background_summary": (
            "Synthetic persona: Writes Python test scripts, validates REST APIs, and triages customer bug reports. "
            "Wants to transition from manual regression testing into AI quality evaluation or RAG engineering."
        ),
        "skills": [
            "python_scripting",
            "api_integration",
            "sql_data_analysis",
            "human_in_the_loop_qa",
        ],
        "interests": ["Engineering & QA", "Data & Engineering"],
    },
    {
        "id": "priya_esg",
        "name": "Priya Nair (Synthetic Profile)",
        "current_role": "Environmental & Sustainability Coordinator (Fresh Graduate, Kuala Lumpur)",
        "persona_type": "Sustainability & Policy Career Switcher",
        "background_summary": (
            "Synthetic persona: Tracks corporate energy metrics and UN SDG alignment reports. Wants to combine ESG domain "
            "knowledge with AI data analytics and governance."
        ),
        "skills": [
            "esg_sustainability_reporting",
            "data_visualization",
            "stakeholder_communication",
            "data_privacy_pdpa",
        ],
        "interests": ["Sustainability & Green Tech", "Governance, Risk & Compliance"],
    },
    {
        "id": "sparse_edge_case",
        "name": "Sparse / Unverified Profile (Guardrail Demo)",
        "current_role": "Incomplete Intake (Edge-Case Verification)",
        "persona_type": "Guardrail Verification Persona",
        "background_summary": (
            "Synthetic test case with only 1 generic skill entered. Demonstrates that AI Skills Compass refuses to "
            "fabricate a high-confidence career prediction when profile evidence is insufficient."
        ),
        "skills": ["ai_literacy"],
        "interests": [],
    },
]
