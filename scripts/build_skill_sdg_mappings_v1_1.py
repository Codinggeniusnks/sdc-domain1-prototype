"""
Build Canonical Skill SDG Mappings v1.1.0 (Stage 13C Remediation)
Resolves:
- P1-1: Target 9.c overstretch (RAG, API integration reallocated to 9.5)
- P1-2: Target 16.10 PDPA mischaracterization (PDPA reallocated to Target 16.6)
- P1-3: Target 17.18 SQL mismatch (SQL reallocated to Target 9.5)
- P2-1: Target 13.2 corporate carbon directness (Carbon accounting primary -> 12.6 DIRECT, 13.2 ENABLING; purge 13.3)
- P2-3: Confidence recalibration (contextual/sector-dependent alignments -> MEDIUM)
"""

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
TARGETS_FILE = ROOT / "data" / "sdg" / "sdg_targets_v1_1.json"
OUTPUT_FILE = ROOT / "data" / "sdg" / "skill_sdg_mappings_v1_1.json"

def main():
    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets_data = json.load(f)
    valid_targets = {t["target_id"]: t for t in targets_data["targets"]}

    mappings = [
        {
            "entity_id": "ai_literacy",
            "entity_name": "AI Literacy & Principles",
            "entity_type": "SKILL",
            "primary_sdgs": [4],
            "secondary_sdgs": [8],
            "sdg_mappings": [
                {
                    "sdg_number": 4,
                    "target_ids": ["4.4"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "AI literacy provides foundational digital understanding necessary for workers to acquire relevant technical competencies and maintain decent employment.",
                    "contribution_pathway": "Enables learners to acquire essential technical capabilities that promote workforce employability in a digitized economy.",
                    "evidence_source_ids": ["UNESCO_AI_COMPETENCY_2024", "UN_SDG_TARGET_4_4"],
                    "evidence_references": "UNESCO AI Competency Framework for Teachers and Citizens (2024); UN SDG Target 4.4.",
                    "independent_source_families": ["UNESCO", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["FOUNDATIONAL_CAPABILITY", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Understanding artificial intelligence tools enables employees to adapt to technological changes, supporting productivity improvements.",
                    "contribution_pathway": "Supports enterprise operational transition toward diversified and technologically upgraded workflows.",
                    "evidence_source_ids": ["ILO_GENAI_WORKFORCE_2023", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "ILO Generative AI and Jobs Report (2023); UN SDG Target 8.2.",
                    "independent_source_families": ["ILO", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["INDIRECT_PRODUCTIVITY_EFFECT", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "prompt_engineering",
            "entity_name": "Prompt Engineering & Synthesis",
            "entity_type": "SKILL",
            "primary_sdgs": [8],
            "secondary_sdgs": [9],
            "sdg_mappings": [
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Prompt engineering enhances human-AI collaboration efficiency, accelerating knowledge synthesis and lifting white-collar labor productivity.",
                    "contribution_pathway": "Enables workers to utilize foundation models to automate cognitive tasks, supporting high-value service productivity.",
                    "evidence_source_ids": ["STANFORD_AI_INDEX_2024", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "Stanford AI Index Report 2024 Chapter on Labor Productivity; UN SDG Target 8.2.",
                    "independent_source_families": ["STANFORD_HAI", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Prompt synthesis assists researchers and developers in code generation, rapid prototyping, and literature synthesis.",
                    "contribution_pathway": "Augments technical capabilities in industrial R&D environments.",
                    "evidence_source_ids": ["OECD_AI_POLICY_2023", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "OECD Principles for Digital Innovation (2023); UN SDG Target 9.5.",
                    "independent_source_families": ["OECD", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "process_mapping",
            "entity_name": "Business Process Mapping",
            "entity_type": "SKILL",
            "primary_sdgs": [8],
            "secondary_sdgs": [12],
            "sdg_mappings": [
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Process mapping identifies workflow bottlenecks, eliminates operational waste, and streamlines business procedures.",
                    "contribution_pathway": "Drives higher productivity and efficiency through systematic organizational re-engineering.",
                    "evidence_source_ids": ["MALAYSIA_PRODUCTIVITY_REPORT_2023", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "Malaysia Productivity Corporation (MPC) Annual Report 2023; UN SDG Target 8.2.",
                    "independent_source_families": ["MPC_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["OPERATIONAL_OPTIMIZATION", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 12,
                    "target_ids": ["12.6"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Mapping material and resource flows enables organizations to identify carbon hotspots and adopt sustainable operational practices.",
                    "contribution_pathway": "Provides structural transparency required for corporate sustainability and circular economy reporting.",
                    "evidence_source_ids": ["WBCSD_CIRCULAR_TRANSITION_2023", "UN_SDG_TARGET_12_6"],
                    "evidence_references": "WBCSD Circular Transition Indicators v3.0; UN SDG Target 12.6.",
                    "independent_source_families": ["WBCSD", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["CIRCULAR_ECONOMY_LINK", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "sql_data_analysis",
            "entity_name": "SQL Data Extraction & Analysis",
            "entity_type": "SKILL",
            "primary_sdgs": [9],
            "secondary_sdgs": [8],
            "sdg_mappings": [
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "SQL extraction and structured relational querying provide essential data retrieval capabilities supporting scientific, industrial, and engineering technological analysis.",
                    "contribution_pathway": "Equips technical analysts and developers with database query tools necessary for empirical industrial research and data modeling.",
                    "evidence_source_ids": ["IEEE_DATA_ENGINEERING_2023", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "IEEE Computer Society Technical Brief on Database Query Languages; UN SDG Target 9.5.",
                    "independent_source_families": ["IEEE", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Automating business query pipelines and operational reporting lifts managerial decision velocity and enterprise productivity.",
                    "contribution_pathway": "Replaces manual spreadsheet processing with automated database queries, improving organizational productivity.",
                    "evidence_source_ids": ["WORLD_BANK_DIGITAL_SERVICES_2023", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "World Bank Digital Economy Diagnostics 2023; UN SDG Target 8.2.",
                    "independent_source_families": ["WORLD_BANK", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "python_scripting",
            "entity_name": "Python Scripting & Automation",
            "entity_type": "SKILL",
            "primary_sdgs": [9],
            "secondary_sdgs": [8],
            "sdg_mappings": [
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Python is the primary language of scientific computing, machine learning, and computational engineering, upgrading technological R&D capabilities.",
                    "contribution_pathway": "Empowers research and engineering teams to model complex systems, build automated pipelines, and conduct data-driven technical research.",
                    "evidence_source_ids": ["ACM_COMPUTING_SURVEY_2023", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "ACM Computing Surveys on Scientific Python Ecosystem; UN SDG Target 9.5.",
                    "independent_source_families": ["ACM", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Scripting repetitive computational and back-office tasks eliminates manual processing delays and accelerates technical productivity.",
                    "contribution_pathway": "Enables enterprise automation across high-value added sectors.",
                    "evidence_source_ids": ["TALENTCORP_IMPACT_2024", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4; UN SDG Target 8.2.",
                    "independent_source_families": ["TALENTCORP_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "data_visualization",
            "entity_name": "Data Visualization & Dashboarding",
            "entity_type": "SKILL",
            "primary_sdgs": [8],
            "secondary_sdgs": [16],
            "sdg_mappings": [
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Interactive dashboards and visual business analytics accelerate operational decision-making, elevating enterprise productivity.",
                    "contribution_pathway": "Transforms raw multi-source business data into actionable visual insights for high-value operational upgrading.",
                    "evidence_source_ids": ["GARTNER_BI_ANALYTICS_2024", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "Gartner Magic Quadrant for Analytics and Business Intelligence Platforms 2024; UN SDG Target 8.2.",
                    "independent_source_families": ["GARTNER", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["OPERATIONAL_DECISION_SUPPORT", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Visual reporting dashboards assist organizational stakeholders in auditing compliance and maintaining operational transparency.",
                    "contribution_pathway": "Supports internal institutional oversight and transparent governance.",
                    "evidence_source_ids": ["OECD_PUBLIC_GOVERNANCE_2023", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "OECD Guidelines on Digital Government and Transparent Metrics; UN SDG Target 16.6.",
                    "independent_source_families": ["OECD", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "MEDIUM",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["CONTEXT_DEPENDENT_ALIGNMENT", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "workflow_automation",
            "entity_name": "Workflow & Integration Automation",
            "entity_type": "SKILL",
            "primary_sdgs": [8],
            "secondary_sdgs": [9],
            "sdg_mappings": [
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Automating enterprise workflows directly drives productivity upgrading and error reduction across administrative and technical sectors.",
                    "contribution_pathway": "Connects disaggregated systems into unified automated execution flows, maximizing labor output value.",
                    "evidence_source_ids": ["FORRESTER_AUTOMATION_2023", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "Forrester Wave on Digital Process Automation Software 2023; UN SDG Target 8.2.",
                    "independent_source_families": ["FORRESTER", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "CI/CD automated testing and DevOps pipelines upgrade technological execution capabilities in digital engineering.",
                    "contribution_pathway": "Supports technological infrastructure modernization in technical teams.",
                    "evidence_source_ids": ["DORA_STATE_OF_DEVOPS_2023", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "DORA State of DevOps Report 2023; UN SDG Target 9.5.",
                    "independent_source_families": ["DORA_GOOGLE", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "human_in_the_loop_qa",
            "entity_name": "Human-in-the-Loop Quality Assurance",
            "entity_type": "SKILL",
            "primary_sdgs": [8],
            "secondary_sdgs": [16],
            "sdg_mappings": [
                {
                    "sdg_number": 8,
                    "target_ids": ["8.8"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Enforcing human verification on automated and AI-generated outputs protects workplace safety, preventing critical operational errors.",
                    "contribution_pathway": "Guarantees safe and secure working environments where algorithmic systems operate alongside human workers.",
                    "evidence_source_ids": ["EU_AI_ACT_HUMAN_OVERSIGHT_2024", "UN_SDG_TARGET_8_8"],
                    "evidence_references": "European Union Artificial Intelligence Act Article 14 (Human Oversight); UN SDG Target 8.8.",
                    "independent_source_families": ["EUROPEAN_UNION", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["WORKPLACE_SAFETY_OVERSIGHT", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Human verification mechanisms prevent silent erroneous decisions, maintaining institutional procedural integrity.",
                    "contribution_pathway": "Supports institutional accountability in automated administrative decisions.",
                    "evidence_source_ids": ["IEEE_ETHICALLY_ALIGNED_DESIGN_2022", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "IEEE Ethically Aligned Design (1st Edition); UN SDG Target 16.6.",
                    "independent_source_families": ["IEEE", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["INSTITUTIONAL_ACCOUNTABILITY", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "rag_knowledge_systems",
            "entity_name": "Retrieval-Augmented Generation (RAG) Architecture",
            "entity_type": "SKILL",
            "primary_sdgs": [9],
            "secondary_sdgs": [16],
            "sdg_mappings": [
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "RAG knowledge systems ground generative models in authoritative enterprise repositories, upgrading technological capabilities for industrial knowledge work.",
                    "contribution_pathway": "Upgrades domestic industrial research, documentation retrieval, and engineering problem-solving through grounded neural search.",
                    "evidence_source_ids": ["NEURIPS_RAG_FOUNDATION_2020", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (NeurIPS 2020); UN SDG Target 9.5.",
                    "independent_source_families": ["ACADEMIC_PEER_REVIEW", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["KNOWLEDGE_INFRASTRUCTURE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Grounding AI outputs in verifiable organizational source documents ensures verifiable auditability and institutional integrity.",
                    "contribution_pathway": "Reinforces institutional transparency by attaching verifiable document provenance to synthesized knowledge.",
                    "evidence_source_ids": ["NIST_AI_RMF_2023", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0); UN SDG Target 16.6.",
                    "independent_source_families": ["NIST_USA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "MEDIUM",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["CONTEXT_DEPENDENT_ALIGNMENT", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "api_integration",
            "entity_name": "API Integration & Orchestration",
            "entity_type": "SKILL",
            "primary_sdgs": [9],
            "secondary_sdgs": [8],
            "sdg_mappings": [
                {
                    "sdg_number": 9,
                    "target_ids": ["9.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "API orchestration enables distributed digital architecture integration, upgrading the technological capabilities of industrial software systems.",
                    "contribution_pathway": "Enables modular software interoperability and enterprise digital infrastructure modernization.",
                    "evidence_source_ids": ["IEEE_CLOUD_STANDARDS_2023", "UN_SDG_TARGET_9_5"],
                    "evidence_references": "IEEE Guide for Cloud Interoperability; UN SDG Target 9.5.",
                    "independent_source_families": ["IEEE", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 8,
                    "target_ids": ["8.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Integrating programmatic APIs eliminates manual data transfer across enterprise applications, driving labor productivity.",
                    "contribution_pathway": "Automates programmatic communication across financial, logistics, and customer service platforms.",
                    "evidence_source_ids": ["TALENTCORP_IMPACT_2024", "UN_SDG_TARGET_8_2"],
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4; UN SDG Target 8.2.",
                    "independent_source_families": ["TALENTCORP_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["GENERAL_PURPOSE_SKILL", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "ai_ethics_governance",
            "entity_name": "AI Ethics & Algorithmic Governance",
            "entity_type": "SKILL",
            "primary_sdgs": [16],
            "secondary_sdgs": [10],
            "sdg_mappings": [
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Auditing algorithms for demographic bias, ensuring explainability, and enforcing fairness directly builds effective, accountable, and transparent institutions.",
                    "contribution_pathway": "Establishes ethical oversight and procedural accountability in AI-driven decision-making systems.",
                    "evidence_source_ids": ["UNESCO_AI_ETHICS_2021", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "UNESCO Recommendation on the Ethics of Artificial Intelligence (2021); UN SDG Target 16.6.",
                    "independent_source_families": ["UNESCO", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_DIRECT_GOVERNANCE",
                    "quality_flags": ["DIRECT_GOVERNANCE_ROLE", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 10,
                    "target_ids": ["10.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Mitigating algorithmic bias prevents discriminatory outcomes against marginalized demographic groups in credit, hiring, and public service allocation.",
                    "contribution_pathway": "Promotes social and economic inclusion by ensuring algorithmic fairness across demographic cohorts.",
                    "evidence_source_ids": ["UN_HUMAN_RIGHTS_AI_2022", "UN_SDG_TARGET_10_2"],
                    "evidence_references": "UN High Commissioner for Human Rights Report on AI and Right to Privacy; UN SDG Target 10.2.",
                    "independent_source_families": ["OHCHR_UN", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["NON_DISCRIMINATION_OVERLAY", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "data_privacy_pdpa",
            "entity_name": "Data Privacy & PDPA Compliance",
            "entity_type": "SKILL",
            "primary_sdgs": [16],
            "secondary_sdgs": [10],
            "sdg_mappings": [
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Enforcing statutory personal data compliance under Malaysia's Personal Data Protection Act 2010 (Act 709) directly upholds institutional accountability, lawful processing, and regulatory rule of law.",
                    "contribution_pathway": "Guarantees that public and commercial institutions handle data in strict adherence to statutory privacy standards, preventing unlawful disclosure and abuse of authority.",
                    "evidence_source_ids": ["MALAYSIA_PDPA_ACT_709", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "Personal Data Protection Act 2010 (Act 709, Malaysia); UN SDG Target 16.6 on effective and accountable institutions.",
                    "independent_source_families": ["PARLIAMENT_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_DIRECT_GOVERNANCE",
                    "quality_flags": ["STATUTORY_COMPLIANCE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 10,
                    "target_ids": ["10.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Protecting personal identifiable information protects individuals from predatory profiling and unauthorized commercial surveillance.",
                    "contribution_pathway": "Empowers citizens by safeguarding personal data autonomy in digital service interactions.",
                    "evidence_source_ids": ["PDP_MALAYSIA_GUIDELINES_2023", "UN_SDG_TARGET_10_2"],
                    "evidence_references": "Department of Personal Data Protection (JPDP) Malaysia Annual Guidelines 2023; UN SDG Target 10.2.",
                    "independent_source_families": ["JPDP_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "MEDIUM",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["CITIZEN_PROTECTION", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "esg_sustainability_reporting",
            "entity_name": "ESG & Corporate Sustainability Reporting",
            "entity_type": "SKILL",
            "primary_sdgs": [12],
            "secondary_sdgs": [13],
            "sdg_mappings": [
                {
                    "sdg_number": 12,
                    "target_ids": ["12.6"],
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "ESG reporting directly operationalizes Target 12.6 by preparing verified corporate sustainability disclosures and integrating ESG metrics into corporate reporting cycles.",
                    "contribution_pathway": "Produces standardized sustainability statements under Bursa Malaysia, IFRS S1/S2, and GRI disclosure standards.",
                    "evidence_source_ids": ["BURSA_MALAYSIA_ESG_GUIDE_2024", "UN_SDG_TARGET_12_6"],
                    "evidence_references": "Bursa Malaysia Sustainability Reporting Guide (3rd Edition); IFRS S1/S2 Standards; UN SDG Target 12.6.",
                    "independent_source_families": ["BURSA_MALAYSIA", "ISSB_IFRS", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_DIRECT_SUSTAINABILITY",
                    "quality_flags": ["DIRECT_SUSTAINABILITY_ROLE", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 13,
                    "target_ids": ["13.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Corporate sustainability disclosures provide verified private sector emissions data that enables sovereign climate planning and NDC tracking.",
                    "contribution_pathway": "Informs national greenhouse gas inventories and national decarbonization strategies under Malaysia's Climate Policy.",
                    "evidence_source_ids": ["MALAYSIA_CLIMATE_POLICY_2023", "UN_SDG_TARGET_13_2"],
                    "evidence_references": "Malaysia National Climate Change Policy 2.0; UN SDG Target 13.2.",
                    "independent_source_families": ["NRECC_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["POLICY_FEED_CAPABILITY", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "carbon_footprint_analytics",
            "entity_name": "Carbon Footprint Analytics & Accounting",
            "entity_type": "SKILL",
            "primary_sdgs": [12, 13],
            "secondary_sdgs": [],
            "sdg_mappings": [
                {
                    "sdg_number": 12,
                    "target_ids": ["12.6"],
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Carbon accounting directly measures Scope 1, 2, and 3 GHG emissions according to the GHG Protocol, generating mandatory quantitative disclosures under Target 12.6.",
                    "contribution_pathway": "Calculates organizational greenhouse gas balances and product lifecycle footprints for corporate sustainability reporting.",
                    "evidence_source_ids": ["GHG_PROTOCOL_CORPORATE_STANDARD", "BURSA_MALAYSIA_ESG_GUIDE_2024", "UN_SDG_TARGET_12_6"],
                    "evidence_references": "WRI/WBCSD GHG Protocol Corporate Standard; Bursa Malaysia Sustainability Reporting Guide; UN SDG Target 12.6.",
                    "independent_source_families": ["WRI_WBCSD", "BURSA_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_DIRECT_SUSTAINABILITY",
                    "quality_flags": ["DIRECT_SUSTAINABILITY_ROLE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 13,
                    "target_ids": ["13.2"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Quantified corporate carbon accounting provides granular emissions baselines that enable facility and national decarbonization roadmap integration.",
                    "contribution_pathway": "Feeds empirical baseline emissions data into national and sectoral climate action planning.",
                    "evidence_source_ids": ["IPCC_WGIII_MITIGATION_2022", "UN_SDG_TARGET_13_2"],
                    "evidence_references": "IPCC 6th Assessment Report (WGIII Mitigation Chapter 5); UN SDG Target 13.2.",
                    "independent_source_families": ["IPCC", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["POLICY_FEED_CAPABILITY", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "stakeholder_communication",
            "entity_name": "Cross-Functional Stakeholder Communication",
            "entity_type": "SKILL",
            "primary_sdgs": [17],
            "secondary_sdgs": [16],
            "sdg_mappings": [
                {
                    "sdg_number": 17,
                    "target_ids": ["17.16"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Cross-functional communication facilitates collaborative alignment across disparate teams, enabling multi-stakeholder partnerships when deployed in sustainability initiatives.",
                    "contribution_pathway": "Bridges technical, executive, and community boundaries to enable multi-stakeholder project coordination.",
                    "evidence_source_ids": ["UN_PARTNERSHIPS_GUIDE_2023", "UN_SDG_TARGET_17_16"],
                    "evidence_references": "UN Department of Economic and Social Affairs Multi-Stakeholder Partnership Guide 2023; UN SDG Target 17.16.",
                    "independent_source_families": ["UNDESA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "MEDIUM",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["CONTEXT_DEPENDENT_ALIGNMENT", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 16,
                    "target_ids": ["16.6"],
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "LIMITED",
                    "alignment_explanation": "Transparent and accurate communication of operational updates supports internal organizational accountability.",
                    "contribution_pathway": "Supports institutional transparency through accurate dissemination of organizational information.",
                    "evidence_source_ids": ["OECD_PUBLIC_GOVERNANCE_2023", "UN_SDG_TARGET_16_6"],
                    "evidence_references": "OECD Principles of Corporate Governance 2023; UN SDG Target 16.6.",
                    "independent_source_families": ["OECD", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "MEDIUM",
                    "derivation_rule_id": "RULE_SKILL_CONTEXTUAL_SUPPORT",
                    "quality_flags": ["CONTEXT_DEPENDENT_ALIGNMENT", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        },
        {
            "entity_id": "instructional_design",
            "entity_name": "Instructional Design & Workforce Reskilling",
            "entity_type": "SKILL",
            "primary_sdgs": [4],
            "secondary_sdgs": [8],
            "sdg_mappings": [
                {
                    "sdg_number": 4,
                    "target_ids": ["4.4"],
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "alignment_explanation": "Instructional design directly operationalizes Target 4.4 by formulating adult learning curricula that substantially increase technical and vocational competencies for employment.",
                    "contribution_pathway": "Creates modular, skill-aligned vocational learning interventions that equip youth and adults for decent employment.",
                    "evidence_source_ids": ["UNESCO_UNEVOC_TVET_2023", "HRD_CORP_MALAYSIA_INDEX_2024", "UN_SDG_TARGET_4_4"],
                    "evidence_references": "UNESCO-UNEVOC Technical and Vocational Education Guidelines; HRD Corp National Training Index 2024; UN SDG Target 4.4.",
                    "independent_source_families": ["UNESCO", "HRD_CORP_MALAYSIA", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_DIRECT_EDUCATION",
                    "quality_flags": ["DIRECT_EDUCATION_RESKILLING_ROLE", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                },
                {
                    "sdg_number": 8,
                    "target_ids": ["8.5"],
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "alignment_explanation": "Delivering effective upskilling programs prevents worker displacement and protects full and productive employment.",
                    "contribution_pathway": "Enables workers to transition into modern digital and green roles, preserving productive employment.",
                    "evidence_source_ids": ["ILO_RESKILLING_REPORT_2023", "UN_SDG_TARGET_8_5"],
                    "evidence_references": "ILO World Employment and Social Outlook 2023; UN SDG Target 8.5.",
                    "independent_source_families": ["ILO", "UN_SDG_FRAMEWORK"],
                    "mapping_confidence": "HIGH",
                    "derivation_rule_id": "RULE_SKILL_ENABLING_CAPABILITY",
                    "quality_flags": ["EMPLOYABILITY_PRESERVATION", "OFFICIAL_TARGET_TRACEABLE"],
                    "last_verified_date": "2026-10-24"
                }
            ]
        }
    ]

    # Validation audits
    assert len(mappings) == 16, f"Expected 16 skills, got {len(mappings)}"
    gp_skills = ["python_scripting", "sql_data_analysis", "api_integration", "prompt_engineering", "workflow_automation"]
    for m in mappings:
        s_id = m["entity_id"]
        assert 1 <= len(m["primary_sdgs"]) <= 3, f"Skill {s_id} primary SDGs out of bounds"
        for sm in m["sdg_mappings"]:
            for tid in sm["target_ids"]:
                assert tid in valid_targets, f"Skill {s_id} references invalid target {tid}"
            if s_id in gp_skills:
                assert sm["mapping_type"] != "DIRECT", f"Violation: GP skill {s_id} has DIRECT mapping!"

    manifest = {
        "version": "1.1.0",
        "module": "M5_SKILL_SDG_MAPPINGS",
        "total_skills_mapped": len(mappings),
        "generated_date": "2026-10-24",
        "remediation_stage": "Stage 13C",
        "canonical_skills_coverage": "16/16",
        "mappings": mappings
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Saved 16 remediated skill SDG mappings v1.1.0 to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
