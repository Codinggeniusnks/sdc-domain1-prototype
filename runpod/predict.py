"""Inference Helper for RunPod Trained Model.

Loads either skills_predictor.pt (PyTorch) or skills_predictor.joblib (Scikit-Learn)
and predicts skills and emerging demand category for any input text.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = Path(__file__).resolve().parent / "models"
sys.path.insert(0, str(BASE_DIR / "src"))
from taxonomy import SKILLS_CATALOG

SKILL_KEYS = list(SKILLS_CATALOG.keys())

def predict_text(text: str) -> dict:
    if not text or not text.strip():
        return {"predicted_skills": [], "is_emerging_demand": False, "confidence": 0.0}

    # 1. Try PyTorch model first
    pt_path = MODELS_DIR / "skills_predictor.pt"
    if pt_path.exists():
        try:
            import torch
            import torch.nn as nn
            from sklearn.feature_extraction.text import TfidfVectorizer

            ckpt = torch.load(pt_path, map_location="cpu")
            vocab = ckpt["vectorizer_vocab"]
            vectorizer = TfidfVectorizer(vocabulary=vocab)
            X = torch.tensor(vectorizer.fit_transform([text]).toarray(), dtype=torch.float32)

            class SkillsPredictorNN(nn.Module):
                def __init__(self, in_features: int, num_skills: int):
                    super().__init__()
                    self.shared = nn.Sequential(
                        nn.Linear(in_features, 128),
                        nn.Identity(),
                        nn.ReLU(),
                        nn.Dropout(0.3),
                        nn.Linear(128, 64),
                        nn.ReLU(),
                    )
                    self.skill_head = nn.Linear(64, num_skills)
                    self.demand_head = nn.Linear(64, 1)

                def forward(self, x):
                    feat = self.shared(x)
                    return self.skill_head(feat), self.demand_head(feat)

            model = SkillsPredictorNN(ckpt["in_features"], len(SKILL_KEYS))
            model.load_state_dict(ckpt["state_dict"])
            model.eval()

            with torch.no_grad():
                s_logits, d_logits = model(X)
                s_probs = torch.sigmoid(s_logits)[0].numpy()
                d_prob = float(torch.sigmoid(d_logits)[0][0].item())

            detected = [SKILL_KEYS[i] for i, prob in enumerate(s_probs) if prob > 0.4]
            return {
                "framework": "PyTorch",
                "predicted_skills": detected,
                "is_emerging_demand": bool(d_prob > 0.5),
                "demand_score": round(d_prob * 100, 1),
            }
        except Exception:
            pass

    # 2. Try Scikit-Learn model
    jl_path = MODELS_DIR / "skills_predictor.joblib"
    if jl_path.exists():
        try:
            import joblib
            saved = joblib.load(jl_path)
            vec = saved["vectorizer"]
            clf_skills = saved["clf_skills"]
            clf_demand = saved["clf_demand"]

            X = vec.transform([text])
            preds = clf_skills.predict(X)[0]
            d_pred = int(clf_demand.predict(X)[0])
            try:
                d_prob = float(clf_demand.predict_proba(X)[0][1])
            except Exception:
                d_prob = float(d_pred)

            detected = [SKILL_KEYS[i] for i, val in enumerate(preds) if val == 1]
            return {
                "framework": "Scikit-Learn (Joblib)",
                "predicted_skills": detected,
                "is_emerging_demand": bool(d_pred == 1),
                "demand_score": round(d_prob * 100, 1),
            }
        except Exception:
            pass

    return {"predicted_skills": [], "is_emerging_demand": False, "confidence": 0.0}

if __name__ == "__main__":
    sample_text = "Operations analyst with experience in workflow automation, process mapping, and SQL data analysis."
    result = predict_text(sample_text)
    print(f"Sample Text: {sample_text}")
    print("Inference Result:", json.dumps(result, indent=2))
