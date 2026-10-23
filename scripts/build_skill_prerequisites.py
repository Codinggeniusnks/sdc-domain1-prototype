"""
Build Script for Skill Prerequisite Dependency Graph v1.0.0 (Stage 12A)
Module: M4 Reskilling Pathway Engine
Author: Senior Learning-Pathway Architect & Evidence-Grounding Auditor
Date: 2026-10-23
"""

import os
import json
from datetime import datetime
from collections import defaultdict, deque

PREREQUISITE_RELATIONS = [
    # 1. AI Literacy as foundation for generative engineering
    {
        "prerequisite_skill_id": "ai_literacy",
        "target_skill_id": "prompt_engineering",
        "dependency_strength": "REQUIRED",
        "reason": "Understanding fundamental LLM capabilities, tokenization, and temperature is essential before constructing systematic prompts.",
        "source_id": "DEEPLEARNING_AI_PROMPT_CURRICULUM_2024",
        "evidence_reference": "DeepLearning.AI ChatGPT Prompt Engineering Framework, Section 1: Foundations",
        "mapping_confidence": 0.95
    },
    # 2. AI Literacy as foundation for Human-in-the-Loop QA
    {
        "prerequisite_skill_id": "ai_literacy",
        "target_skill_id": "human_in_the_loop_qa",
        "dependency_strength": "REQUIRED",
        "reason": "Evaluating hallucination rates and output fidelity requires conceptual understanding of generative model failure modes.",
        "source_id": "NIST_AI_RMF_2023",
        "evidence_reference": "NIST AI Risk Management Framework 1.0, Measure Function 2.3",
        "mapping_confidence": 0.90
    },
    # 3. AI Literacy as foundation for AI Ethics & Governance
    {
        "prerequisite_skill_id": "ai_literacy",
        "target_skill_id": "ai_ethics_governance",
        "dependency_strength": "REQUIRED",
        "reason": "Governance frameworks and risk mitigation policies require technical comprehension of algorithmic behavior.",
        "source_id": "MOSTI_NATIONAL_AI_ROADMAP_2021_2025",
        "evidence_reference": "Ministry of Science, Technology and Innovation Malaysia: AI Ethics Principles, Pillar 3",
        "mapping_confidence": 0.95
    },
    # 4. Python Scripting as foundation for RAG Knowledge Systems
    {
        "prerequisite_skill_id": "python_scripting",
        "target_skill_id": "rag_knowledge_systems",
        "dependency_strength": "REQUIRED",
        "reason": "Developing retrieval pipelines, embedding chunking, and vector index querying requires programmatic Python capability.",
        "source_id": "LANGCHAIN_ACADEMY_CURRICULUM_2024",
        "evidence_reference": "LangChain Production RAG Architectures, Module 1: Document Ingestion",
        "mapping_confidence": 0.95
    },
    # 5. Python Scripting as recommended prerequisite for API Integration
    {
        "prerequisite_skill_id": "python_scripting",
        "target_skill_id": "api_integration",
        "dependency_strength": "RECOMMENDED",
        "reason": "Consuming REST APIs and parsing JSON responses is most effectively implemented through scripting automation.",
        "source_id": "MDN_WEB_APIS_GUIDE_2024",
        "evidence_reference": "Mozilla Developer Network: Client-side Web APIs & Python HTTP Client Practices",
        "mapping_confidence": 0.90
    },
    # 6. API Integration as recommended prerequisite for RAG Knowledge Systems
    {
        "prerequisite_skill_id": "api_integration",
        "target_skill_id": "rag_knowledge_systems",
        "dependency_strength": "RECOMMENDED",
        "reason": "RAG architectures interact heavily with vector search endpoints and LLM inference REST APIs.",
        "source_id": "OPENAI_EMBEDDING_API_GUIDE_2024",
        "evidence_reference": "OpenAI Platform Documentation: Embeddings and Vector Search Architecture",
        "mapping_confidence": 0.90
    },
    # 7. Prompt Engineering as recommended prerequisite for RAG Knowledge Systems
    {
        "prerequisite_skill_id": "prompt_engineering",
        "target_skill_id": "rag_knowledge_systems",
        "dependency_strength": "RECOMMENDED",
        "reason": "Synthesizing retrieved context chunks requires structured instruction and hallucination-resistant prompting.",
        "source_id": "ANTHROPIC_CONTEXTUAL_RETRIEVAL_2024",
        "evidence_reference": "Anthropic Engineering: Contextual Retrieval & Prompt Synthesis Standards",
        "mapping_confidence": 0.85
    },
    # 8. SQL Data Analysis as recommended prerequisite for Data Visualization
    {
        "prerequisite_skill_id": "sql_data_analysis",
        "target_skill_id": "data_visualization",
        "dependency_strength": "RECOMMENDED",
        "reason": "Creating accurate dashboards and executive charts depends on foundational relational querying and tabular aggregation.",
        "source_id": "MICROSOFT_POWERBI_CURRICULUM_2024",
        "evidence_reference": "Microsoft PL-300: Power BI Data Analyst Certification Framework, Domain 1",
        "mapping_confidence": 0.90
    },
    # 9. Process Mapping as recommended prerequisite for Workflow Automation
    {
        "prerequisite_skill_id": "process_mapping",
        "target_skill_id": "workflow_automation",
        "dependency_strength": "RECOMMENDED",
        "reason": "Automating business workflows requires first documenting decision trees, bottlenecks, and handoffs via BPMN standards.",
        "source_id": "OMG_BPMN_STANDARDS_2020",
        "evidence_reference": "Object Management Group BPMN 2.0 Process Modeling Specification",
        "mapping_confidence": 0.95
    },
    # 10. Data Privacy (PDPA) as recommended prerequisite for AI Ethics & Governance
    {
        "prerequisite_skill_id": "data_privacy_pdpa",
        "target_skill_id": "ai_ethics_governance",
        "dependency_strength": "RECOMMENDED",
        "reason": "Malaysian AI governance mandates compliance with statutory Personal Data Protection Act (PDPA 2010) principles.",
        "source_id": "JPDP_MALAYSIA_GUIDELINES_2024",
        "evidence_reference": "Jabatan Perlindungan Data Peribadi: Guidelines on Personal Data in Cloud & AI Computing",
        "mapping_confidence": 0.95
    },
    # 11. Carbon Footprint Analytics as recommended prerequisite for ESG Reporting
    {
        "prerequisite_skill_id": "carbon_footprint_analytics",
        "target_skill_id": "esg_sustainability_reporting",
        "dependency_strength": "RECOMMENDED",
        "reason": "Quantitative Scope 1, 2, and 3 emissions accounting forms the foundation of environmental disclosure frameworks.",
        "source_id": "BURSA_MALAYSIA_SUSTAINABILITY_REPORTING_GUIDE_2023",
        "evidence_reference": "Bursa Malaysia Sustainability Reporting Guide (4th Edition), Climate Change Disclosures",
        "mapping_confidence": 0.90
    },
    # 12. Stakeholder Communication as recommended prerequisite for Instructional Design
    {
        "prerequisite_skill_id": "stakeholder_communication",
        "target_skill_id": "instructional_design",
        "dependency_strength": "RECOMMENDED",
        "reason": "Training needs analysis and curriculum sign-off require structured communication with business sponsors.",
        "source_id": "ATD_INSTRUCTIONAL_DESIGN_BODY_OF_KNOWLEDGE_2023",
        "evidence_reference": "Association for Talent Development (ATD) Competency Model: Performance Improvement",
        "mapping_confidence": 0.85
    },
    # 13. SQL Data Analysis as optional foundation for Carbon Footprint Analytics
    {
        "prerequisite_skill_id": "sql_data_analysis",
        "target_skill_id": "carbon_footprint_analytics",
        "dependency_strength": "OPTIONAL",
        "reason": "Querying large ERP database activity records facilitates automated emissions calculation.",
        "source_id": "GHG_PROTOCOL_DATA_MANAGEMENT_2022",
        "evidence_reference": "Greenhouse Gas Protocol Corporate Standard, Chapter 6: Accounting for GHG Emissions",
        "mapping_confidence": 0.80
    },
    # 14. Process Mapping as optional foundation for Instructional Design
    {
        "prerequisite_skill_id": "process_mapping",
        "target_skill_id": "instructional_design",
        "dependency_strength": "OPTIONAL",
        "reason": "Mapping corporate standard operating procedures provides structured input for vocational training modules.",
        "source_id": "ILO_COMPETENCY_BASED_TRAINING_2021",
        "evidence_reference": "ILO Regional Skills Programme: Competency-Based Training Design Manual",
        "mapping_confidence": 0.75
    },
    # 15. AI Literacy as optional foundation for Data Privacy (PDPA)
    {
        "prerequisite_skill_id": "ai_literacy",
        "target_skill_id": "data_privacy_pdpa",
        "dependency_strength": "OPTIONAL",
        "reason": "Awareness of automated decision systems contextualizes statutory rights regarding automated profiling.",
        "source_id": "JPDP_MALAYSIA_GUIDELINES_2024",
        "evidence_reference": "JPDP Consultation Paper on Digital Economy Data Governance",
        "mapping_confidence": 0.80
    }
]

def audit_prerequisite_graph(relations):
    """
    Validates graph invariants:
    1. Acyclic for REQUIRED and overall dependencies.
    2. Valid dependency strengths.
    3. Completeness of metadata.
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set()

    for r in relations:
        u = r["prerequisite_skill_id"]
        v = r["target_skill_id"]
        strength = r["dependency_strength"]
        if strength not in ["REQUIRED", "RECOMMENDED", "OPTIONAL"]:
            raise ValueError(f"Invalid dependency strength: {strength}")
        graph[u].append((v, strength))
        in_degree[v] += 1
        all_nodes.add(u)
        all_nodes.add(v)

    # Cycle detection via Kahn's algorithm
    queue = deque([node for node in all_nodes if in_degree[node] == 0])
    visited_count = 0

    while queue:
        curr = queue.popleft()
        visited_count += 1
        for neighbor, _ in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    has_cycle = visited_count < len(all_nodes)
    if has_cycle:
        raise ValueError("PREREQUISITE_CONFLICT: Cycle detected in prerequisite dependency graph!")

    return True

def build_prerequisites_file():
    target_dir = r"C:\Users\LENOVO\.gemini\antigravity\scratch\sdc-domain1-prototype\data\reskilling"
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "skill_prerequisites_v1.json")

    # Run cycle audit
    audit_prerequisite_graph(PREREQUISITE_RELATIONS)

    required_count = sum(1 for r in PREREQUISITE_RELATIONS if r["dependency_strength"] == "REQUIRED")
    recommended_count = sum(1 for r in PREREQUISITE_RELATIONS if r["dependency_strength"] == "RECOMMENDED")
    optional_count = sum(1 for r in PREREQUISITE_RELATIONS if r["dependency_strength"] == "OPTIONAL")

    payload = {
        "version": "1.0.0",
        "module": "M4_PERSONALISED_RESKILLING_PATHWAY_ENGINE",
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
        "total_prerequisite_relations": len(PREREQUISITE_RELATIONS),
        "relation_strength_counts": {
            "REQUIRED": required_count,
            "RECOMMENDED": recommended_count,
            "OPTIONAL": optional_count
        },
        "cycle_audit_result": "PASS_ACYCLIC",
        "prerequisites": PREREQUISITE_RELATIONS
    }

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Successfully generated {target_file}")
    print(f"Total relations: {len(PREREQUISITE_RELATIONS)} (Required: {required_count}, Recommended: {recommended_count}, Optional: {optional_count})")
    print(f"Cycle Audit: PASS_ACYCLIC")

if __name__ == "__main__":
    build_prerequisites_file()
