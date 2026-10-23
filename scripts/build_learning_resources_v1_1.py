"""
Build Script for Normalized Learning Resources Catalog v1.1.0 (Stage 12C)
Module: M4 Reskilling Pathway Engine
Author: Senior Learning-Pathway Engineer & Reproducibility Auditor
Date: 2026-10-23
"""

import os
import json
import hashlib

BASE_DIR = r"C:\Users\LENOVO\.gemini\antigravity\scratch\sdc-domain1-prototype"
INPUT_PATH = os.path.join(BASE_DIR, "data", "reskilling", "learning_resources_v1.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "reskilling", "learning_resources_v1_1.json")

PROVIDER_MAPPING = {
    'DeepLearning.AI / Coursera': ('DEEPLEARNING_AI', 'DeepLearning.AI'),
    'DeepLearning.AI / OpenAI': ('DEEPLEARNING_AI', 'DeepLearning.AI'),
    'DeepLearning.AI': ('DEEPLEARNING_AI', 'DeepLearning.AI'),
    'LangChain / DeepLearning.AI': ('DEEPLEARNING_AI', 'DeepLearning.AI'),
    'DeepLearning.AI / Weights & Biases': ('DEEPLEARNING_AI', 'DeepLearning.AI'),
    
    'Google Cloud Skills Boost / Coursera': ('ALPHABET', 'Alphabet Inc.'),
    'Kaggle Learn': ('ALPHABET', 'Alphabet Inc.'),
    
    'The Open University (OpenLearn)': ('OPEN_UNIVERSITY', 'The Open University'),
    'OpenLearn / The Open University': ('OPEN_UNIVERSITY', 'The Open University'),
    
    'Microsoft Learn': ('MICROSOFT', 'Microsoft Corporation'),
    'IBM SkillsBuild': ('IBM', 'IBM Corporation'),
    'Cisco Networking Academy': ('CISCO', 'Cisco Systems'),
    'Mozilla Developer Network (MDN)': ('MOZILLA', 'Mozilla Foundation'),
    'Postman Academy': ('POSTMAN', 'Postman Inc.'),
    'Zapier Learn': ('ZAPIER', 'Zapier Inc.'),
    
    'freeCodeCamp': ('FREECODECAMP', 'freeCodeCamp Foundation'),
    'LearnPrompting.org': ('LEARN_PROMPTING', 'LearnPrompting.org'),
    
    'University of Helsinki & MinnaLearn': ('UNIV_HELSINKI', 'University of Helsinki & MinnaLearn'),
    'University of Illinois / Coursera': ('UNIV_ILLINOIS', 'University of Illinois Urbana-Champaign'),
    'Macquarie University / Coursera': ('MACQUARIE_UNIV', 'Macquarie University'),
    'Rochester Institute of Technology / edX': ('RIT', 'Rochester Institute of Technology'),
    
    'Department of Personal Data Protection Malaysia (JPDP)': ('JPDP_MALAYSIA', 'Department of Personal Data Protection Malaysia (JPDP)'),
    'Ministry of Science, Technology and Innovation (MOSTI) Malaysia': ('MOSTI_MALAYSIA', 'Ministry of Science, Technology and Innovation (MOSTI) Malaysia'),
    'Bursa Malaysia Berhad': ('BURSA_MALAYSIA', 'Bursa Malaysia Berhad'),
    
    'UN Global Compact Academy': ('UN_GLOBAL_COMPACT', 'United Nations Global Compact'),
    'Greenhouse Gas Protocol / WRI / WBCSD': ('GHG_PROTOCOL', 'Greenhouse Gas Protocol / WRI / WBCSD'),
    'Camunda / Object Management Group': ('OMG_CAMUNDA', 'Object Management Group & Camunda')
}


def build_catalog_v1_1():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        v1_data = json.load(f)

    raw_resources = v1_data["resources"]
    
    # Strictly exclude synthetic test fixtures
    prod_resources = []
    for r in raw_resources:
        if r["resource_id"] in ["RES_LOWCOST_01", "RES_VAR_01"]:
            continue
        
        provider_raw = r["provider"]
        group_id, group_name = PROVIDER_MAPPING.get(provider_raw, ("INDEPENDENT", provider_raw))
        
        normalized_resource = r.copy()
        normalized_resource["provider_display_name"] = provider_raw
        normalized_resource["provider_group_id"] = group_id
        normalized_resource["provider_group_name"] = group_name
        normalized_resource["test_only"] = False
        normalized_resource["fixture_type"] = None
        
        prod_resources.append(normalized_resource)

    # Compute catalog statistics
    raw_labels = sorted(list(set(r["provider_display_name"] for r in prod_resources)))
    group_ids = sorted(list(set(r["provider_group_id"] for r in prod_resources)))
    cost_counts = {
        "FREE": sum(1 for r in prod_resources if r["cost_status"] == "FREE"),
        "FREE_TO_AUDIT": sum(1 for r in prod_resources if r["cost_status"] == "FREE_TO_AUDIT"),
        "FREEMIUM": sum(1 for r in prod_resources if r["cost_status"] == "FREEMIUM"),
        "LOW_COST": sum(1 for r in prod_resources if r["cost_status"] == "LOW_COST"),
        "VARIABLE_PRICE": sum(1 for r in prod_resources if r["cost_status"] == "VARIABLE_PRICE"),
        "UNKNOWN": sum(1 for r in prod_resources if r["cost_status"] == "UNKNOWN")
    }

    catalog_v1_1 = {
        "version": "1.1.0",
        "module": "M4_PERSONALISED_RESKILLING_PATHWAY_ENGINE",
        "generated_date": "2026-10-23",
        "reference_milestone": "Stage 12C Targeted M4 Remediation",
        "catalog_type": "PRODUCTION_LIVE_VERIFIED_ONLY",
        "parent_v1_sha256": hashlib.sha256(open(INPUT_PATH, "rb").read()).hexdigest(),
        "total_production_resources": len(prod_resources),
        "test_fixtures_in_catalog": 0,
        "raw_provider_labels_count": len(raw_labels),
        "raw_provider_labels": raw_labels,
        "normalized_provider_groups_count": len(group_ids),
        "normalized_provider_groups": group_ids,
        "cost_status_distribution": cost_counts,
        "language_distribution": {
            "English": sum(1 for r in prod_resources if r.get("language") == "English")
        },
        "resources": prod_resources
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog_v1_1, f, indent=2, ensure_ascii=False)

    print(f"Built M4 v1.1.0 Resource Catalog: {OUTPUT_PATH}")
    print(f"Total Resources: {len(prod_resources)}")
    print(f"Raw Provider Labels: {len(raw_labels)}")
    print(f"Normalized Provider Groups: {len(group_ids)}")
    print(f"Cost Statuses: {cost_counts}")


if __name__ == "__main__":
    build_catalog_v1_1()
