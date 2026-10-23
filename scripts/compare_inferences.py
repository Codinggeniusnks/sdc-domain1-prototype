"""Evaluate real-world resume inferences between baseline and v3 models."""

import json
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
model_orig = joblib.load(BASE_DIR / "runpod" / "models" / "skills_predictor.joblib")
model_v3 = joblib.load(BASE_DIR / "runpod" / "models" / "skills_predictor_v3.joblib")

real_cvs = [
    "Experienced operations executive with 4 years managing workflow mapping, SOP documentation, and automating reporting pipelines in logistics.",
    "Software engineer in Penang specializing in Python scripting, REST APIs, automated testing, and relational database queries using PostgreSQL and SQL.",
    "Environmental coordinator responsible for ESG compliance, carbon footprint accounting, Scope 1 and Scope 2 emission monitoring under Bursa Malaysia guidelines.",
    "Senior compliance lead auditing algorithmic fairness, AI governance, and personal data protection under PDPA 2010."
]

print("=== REAL-WORLD PROMPTS EVALUATION ===")
for i, cv in enumerate(real_cvs):
    print(f"\nSample {i+1}: '{cv[:65]}...'")
    # Baseline model
    x_orig = model_orig["vectorizer"].transform([cv])
    preds_orig = [k for k, p in zip(model_orig["clf_skills"].classes_, model_orig["clf_skills"].predict(x_orig)[0]) if p == 1]
    d_orig = model_orig["clf_demand"].predict(x_orig)[0]

    # v3 model
    x_v3 = model_v3["vectorizer"].transform([cv])
    preds_v3 = [k for k, p in zip(model_v3["clf_skills"].classes_, model_v3["clf_skills"].predict(x_v3)[0]) if p == 1]
    d_v3 = model_v3["clf_demand"].predict(x_v3)[0]

    print("  Baseline Model Skills:", preds_orig, "| Demand:", d_orig)
    print("  V3 Multi-Source Skills:", preds_v3, "| Demand:", d_v3)
