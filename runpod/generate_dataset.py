"""Synthetic + Open Public Data Training Dataset Generator for RunPod AI Skills Predictor.

Strictly adheres to Domain 1 Rule §6:
"Data: use public, open or synthetic data only. Do not use real personal data or real CVs."

Integrates:
1. Open-access academic literature from OpenAlex API (CC0) (data/signals_snapshot.json)
2. Public occupational task & competency descriptions from reviewed taxonomy (src/taxonomy.py)
3. Synthetic Malaysian worker career profiles & scenario tasks
Output: data/training_dataset.json
"""

import json
import random
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
from taxonomy import SKILLS_CATALOG, ROLES_CATALOG, SYNTHETIC_PROFILES

DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = DATA_DIR / "training_dataset.json"
SIGNALS_PATH = DATA_DIR / "signals_snapshot.json"

WORKPLACE_TEMPLATES = [
    ("Experienced practitioner specializing in {skill1} and {skill2} across enterprise operations. Currently upskilling in {skill3}.", 3),
    ("Responsible for production {skill1} pipelines, automated model evaluation, and implementing {skill2} best practices.", 2),
    ("Conducting comprehensive audits on {skill1} and ensuring full regulatory compliance with {skill2}.", 2),
    ("Specializing in {skill1}, telemetry logging, and {skill2} for sustainable cloud and enterprise architectures.", 2),
    ("Designed competency frameworks and training curricula covering practical {skill1} and vocational {skill2}.", 2),
    ("Analyzing relational databases and data marts with {skill1} and delivering stakeholder dashboards via {skill2}.", 2),
    ("Architecting autonomous agentic workflows utilizing {skill1} alongside production {skill2}.", 2),
    ("Operations lead responsible for standard operating procedures, {skill1}, and cross-functional {skill2}.", 2),
    ("Software quality engineer focusing on automated testing, {skill1}, and {skill2} regression suites.", 2),
    ("Sustainability analyst driving carbon telemetry using {skill1} and drafting {skill2} for Bursa disclosure.", 2),
    ("Deeply skilled in {skill1} with hands-on project experience in {skill2} and {skill3}.", 3),
    ("Proficient in {skill1} with focus on prompt optimization, validation benchmarking, and {skill2}.", 2),
    ("Data engineer handling vector stores, {skill1}, API gateways, and robust {skill2}.", 2),
    ("Conducting training on ethical AI, {skill1}, and compliance auditing for {skill2}.", 2),
    ("Routine manual filing, paper receipt sorting, and clerical copying without automated software tools.", 0),
    ("Repetitive manual data entry into spreadsheets, paper invoice filing, and physical mail handling.", 0),
    ("Basic mechanical document scanning and physical archive organization without software integrations.", 0),
]

EMERGING_SKILLS = {
    "workflow_automation", "human_in_the_loop_qa", "ai_ethics_governance", 
    "rag_knowledge_systems", "carbon_footprint_analytics", "prompt_engineering", 
    "python_scripting", "data_privacy_pdpa"
}

def generate_dataset(target_total: int = 1500) -> list[dict]:
    random.seed(42)
    skill_keys = list(SKILLS_CATALOG.keys())
    samples = []
    sample_id = 1

    # SOURCE 1: Real OpenAlex Open-Access Public Literature (CC0)
    if SIGNALS_PATH.exists():
        signals_data = json.loads(SIGNALS_PATH.read_text(encoding="utf-8"))
        for sig in signals_data.get("signals", []):
            extracted = [s for s in sig.get("extracted_skills", []) if s in skill_keys]
            if not extracted:
                continue
            one_hot = [1.0 if s in extracted else 0.0 for s in skill_keys]
            is_emerging = 1.0 if any(s in extracted for s in EMERGING_SKILLS) else 0.0
            
            # Combine title and abstract
            text = f"{sig['title']}. {sig.get('summary', '')}".strip()
            samples.append({
                "id": f"open-pub-{sample_id:04d}",
                "source": "OpenAlex CC0 Public Literature",
                "text": text,
                "skills": extracted,
                "labels": one_hot,
                "is_emerging_demand": is_emerging
            })
            sample_id += 1

    # SOURCE 2: Public Occupational Framework Competencies & Objectives (MOSTI / UNESCO / O*NET)
    for sk_id, sk_info in SKILLS_CATALOG.items():
        # Add primary definition
        one_hot = [1.0 if s == sk_id else 0.0 for s in skill_keys]
        is_emerging = 1.0 if sk_id in EMERGING_SKILLS else 0.0
        obj = sk_info.get("pathway_step", {}).get("objective", sk_info["name"])
        text = f"Competency in {sk_info['name']}: {obj}. Core keywords: {', '.join(sk_info['keywords'])}."
        samples.append({
            "id": f"open-comp-{sample_id:04d}",
            "source": "Public Competency Framework",
            "text": text,
            "skills": [sk_id],
            "labels": one_hot,
            "is_emerging_demand": is_emerging
        })
        sample_id += 1

    # SOURCE 3: Synthetic Malaysian Workplace Task Combinations
    remaining = target_total - len(samples)
    for _ in range(max(remaining, 500)):
        tmpl, num_skills = random.choice(WORKPLACE_TEMPLATES)
        chosen_skills = random.sample(skill_keys, k=max(num_skills, 1)) if num_skills > 0 else []
        
        skill_names = [random.choice(SKILLS_CATALOG[s]["keywords"]) for s in chosen_skills]
        if num_skills == 3:
            text = tmpl.format(skill1=skill_names[0], skill2=skill_names[1], skill3=skill_names[2])
        elif num_skills == 2:
            text = tmpl.format(skill1=skill_names[0], skill2=skill_names[1])
        elif num_skills == 1:
            text = tmpl.format(skill1=skill_names[0])
        else:
            text = tmpl
            chosen_skills = []

        one_hot = [1.0 if s in chosen_skills else 0.0 for s in skill_keys]
        is_emerging = 1.0 if any(s in chosen_skills for s in EMERGING_SKILLS) else 0.0

        samples.append({
            "id": f"synth-worker-{sample_id:04d}",
            "source": "Synthetic Malaysian Worker Task Profile",
            "text": text,
            "skills": chosen_skills,
            "labels": one_hot,
            "is_emerging_demand": is_emerging
        })
        sample_id += 1

    return samples

if __name__ == "__main__":
    dataset = generate_dataset(1500)
    OUTPUT_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    open_count = sum(1 for s in dataset if "Open" in s["source"])
    synth_count = sum(1 for s in dataset if "Synthetic" in s["source"])
    print(f"Generated {len(dataset)} records ({open_count} from Open Public Literature/Frameworks, {synth_count} Synthetic).")
    print(f"Saved to {OUTPUT_PATH}")
