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
    ("Experienced with {skill1} and {skill2} in day-to-day enterprise operations. Looking to master {skill3}.", 3),
    ("Responsible for {skill1} pipeline design, model evaluation, and {skill2} for production systems.", 2),
    ("Conducting audits on {skill1} and regulatory compliance including {skill2}.", 2),
    ("Specializing in {skill1}, telemetry logging, and {skill2} for sustainable cloud infrastructure.", 2),
    ("Designed curriculum and learning modules covering {skill1} and vocational {skill2}.", 2),
    ("Analyzing tabular datasets with {skill1} and creating dashboards using {skill2}.", 2),
    ("Building multi-agent autonomous workflows leveraging {skill1} and {skill2}.", 2),
    ("Routine manual data entry and repetitive clerical documentation without {skill1}.", 0),
]

def generate_dataset(num_samples: int = 500) -> list[dict]:
    random.seed(42)
    skill_keys = list(SKILLS_CATALOG.keys())
    samples = []

    # 1. Add canonical examples from profiles & signals
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
            text = "Routine manual data entry and repetitive clerical document filing without automated tools."
            chosen_skills = []

        # Target one-hot vector for 16 skills
        one_hot = [1.0 if s in chosen_skills else 0.0 for s in skill_keys]
        
        # Demand label: 1 if technical AI/governance/green skill, 0 if routine clerical
        is_emerging = 1.0 if any(s in chosen_skills for s in ["workflow_automation", "human_in_the_loop_qa", "ai_ethics_governance", "rag_knowledge_systems", "carbon_footprint_analytics"]) else 0.0

        samples.append({
            "id": f"sample-{idx+1:04d}",
            "text": text,
            "skills": chosen_skills,
            "labels": one_hot,
            "is_emerging_demand": is_emerging
        })

    return samples

if __name__ == "__main__":
    dataset = generate_dataset(600)
    OUTPUT_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    print(f"Generated {len(dataset)} synthetic training records at {OUTPUT_PATH}")
