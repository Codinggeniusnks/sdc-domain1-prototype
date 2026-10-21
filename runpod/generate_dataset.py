"""Synthetic Training Dataset Generator for RunPod AI Skills Predictor.

Generates labeled pairs of text (worker bios, task summaries, and research abstracts)
mapped to the 16 canonical skills in src/taxonomy.py and emerging vs. routine demand labels.
Output: data/training_dataset.json
"""

import json
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from taxonomy import SKILLS_CATALOG, ROLES_CATALOG

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DATA_DIR / "training_dataset.json"

TEMPLATES = [
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
    ("Routine manual filing, paper receipt sorting, and clerical copying without automated tools.", 0),
    ("Repetitive manual data entry into spreadsheets, paper invoice filing, and physical mail handling.", 0),
    ("Basic mechanical document scanning and physical archive organization without software integrations.", 0),
]

def generate_dataset(num_samples: int = 1200) -> list[dict]:
    random.seed(42)
    skill_keys = list(SKILLS_CATALOG.keys())
    samples = []

    for idx in range(num_samples):
        tmpl, num_skills = random.choice(TEMPLATES)
        chosen_skills = random.sample(skill_keys, k=max(num_skills, 1)) if num_skills > 0 else []
        
        # Format text with skill names / keywords
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

        # Target one-hot vector for 16 skills
        one_hot = [1.0 if s in chosen_skills else 0.0 for s in skill_keys]
        
        # Demand label: 1 if high-growth technical/AI/governance/sustainability skill, 0 if routine clerical
        is_emerging = 1.0 if any(s in chosen_skills for s in [
            "workflow_automation", "human_in_the_loop_qa", "ai_ethics_governance", 
            "rag_knowledge_systems", "carbon_footprint_analytics", "prompt_engineering", "python_scripting"
        ]) else 0.0

        samples.append({
            "id": f"sample-{idx+1:04d}",
            "text": text,
            "skills": chosen_skills,
            "labels": one_hot,
            "is_emerging_demand": is_emerging
        })

    return samples

if __name__ == "__main__":
    dataset = generate_dataset(1200)
    OUTPUT_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    print(f"Generated {len(dataset)} synthetic training records at {OUTPUT_PATH}")
