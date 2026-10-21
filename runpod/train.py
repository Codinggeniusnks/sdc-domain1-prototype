"""Model Training Script for RunPod (AI Skills & Demand Predictor).

Trains a model on data/training_dataset.json to predict:
1. Multi-label skill proficiencies across the 16 taxonomy skills.
2. Binary classification of emerging demand vs. vulnerable/routine task profile.

Supports both PyTorch GPU acceleration on RunPod (CUDA) and CPU fallback.
Outputs:
- runpod/models/skills_predictor.pt (PyTorch) or skills_predictor.joblib
- runpod/training_metrics.json (eval metrics, F1, accuracy)
- runpod/training_loss.log (epoch loss history)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "training_dataset.json"
MODELS_DIR = Path(__file__).resolve().parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
METRICS_PATH = Path(__file__).resolve().parent / "training_metrics.json"
LOG_PATH = Path(__file__).resolve().parent / "training_loss.log"

sys.path.insert(0, str(BASE_DIR / "src"))
from taxonomy import SKILLS_CATALOG

SKILL_KEYS = list(SKILLS_CATALOG.keys())

def train_pytorch(device_name: str = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu", epochs: int = 25, lr: float = 1e-3):
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

    device = torch.device("cuda" if torch.cuda.is_available() and device_name == "cuda" else "cpu")
    print(f"[RunPod Train] Training via PyTorch on device: {device} ({torch.cuda.get_device_name(0) if device.type == 'cuda' else 'CPU'})")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    texts = [d["text"] for d in data]
    skill_labels = np.array([d["labels"] for d in data], dtype=np.float32)
    demand_labels = np.array([d["is_emerging_demand"] for d in data], dtype=np.float32).reshape(-1, 1)

    # Feature extraction (TF-IDF bag of subwords/words)
    vectorizer = TfidfVectorizer(max_features=1024, ngram_range=(1, 3))
    X = vectorizer.fit_transform(texts).toarray()

    split_idx = int(len(X) * 0.8)
    X_train, X_test = torch.tensor(X[:split_idx], dtype=torch.float32), torch.tensor(X[split_idx:], dtype=torch.float32)
    y_skills_train, y_skills_test = torch.tensor(skill_labels[:split_idx]), torch.tensor(skill_labels[split_idx:])
    y_demand_train, y_demand_test = torch.tensor(demand_labels[:split_idx]), torch.tensor(demand_labels[split_idx:])

    train_loader = DataLoader(TensorDataset(X_train, y_skills_train, y_demand_train), batch_size=32, shuffle=True)

    class SkillsPredictorNN(nn.Module):
        def __init__(self, in_features: int, num_skills: int):
            super().__init__()
            self.shared = nn.Sequential(
                nn.Linear(in_features, 256),
                nn.BatchNorm1d(256) if in_features > 1 else nn.Identity(),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.Linear(128, 64),
                nn.ReLU(),
            )
            self.skill_head = nn.Linear(64, num_skills)
            self.demand_head = nn.Linear(64, 1)

        def forward(self, x):
            feat = self.shared(x)
            return self.skill_head(feat), self.demand_head(feat)

    model = SkillsPredictorNN(X.shape[1], len(SKILL_KEYS)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion_skills = nn.BCEWithLogitsLoss()
    criterion_demand = nn.BCEWithLogitsLoss()

    logs = []
    start_time = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for bx, by_skills, by_demand in train_loader:
            bx, by_skills, by_demand = bx.to(device), by_skills.to(device), by_demand.to(device)
            optimizer.zero_grad()
            out_skills, out_demand = model(bx)
            loss = criterion_skills(out_skills, by_skills) + criterion_demand(out_demand, by_demand)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        logs.append(f"Epoch {ep:02d}/{epochs:02d} - Loss: {avg_loss:.4f}")
        if ep % 5 == 0 or ep == epochs:
            print(f"[RunPod Train] {logs[-1]}")

    elapsed = round(time.time() - start_time, 2)
    # Evaluate
    model.eval()
    with torch.no_grad():
        test_out_skills, test_out_demand = model(X_test.to(device))
        pred_skills = (torch.sigmoid(test_out_skills) > 0.5).cpu().numpy().astype(int)
        pred_demand = (torch.sigmoid(test_out_demand) > 0.5).cpu().numpy().astype(int)

    test_skills_true = y_skills_test.numpy().astype(int)
    test_demand_true = y_demand_test.numpy().astype(int)

    from sklearn.metrics import accuracy_score, f1_score
    skill_f1 = float(f1_score(test_skills_true, pred_skills, average="micro"))
    demand_acc = float(accuracy_score(test_demand_true, pred_demand))

    # Save weights & vocabulary
    torch.save({
        "state_dict": model.state_dict(),
        "vectorizer_vocab": vectorizer.vocabulary_,
        "in_features": X.shape[1],
        "skill_keys": SKILL_KEYS,
    }, MODELS_DIR / "skills_predictor.pt")

    metrics = {
        "framework": "PyTorch",
        "device": str(device),
        "epochs": epochs,
        "elapsed_seconds": elapsed,
        "skill_f1_score": round(skill_f1, 4),
        "demand_accuracy": round(demand_acc, 4),
        "dataset_size": len(data),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    LOG_PATH.write_text("\n".join(logs), encoding="utf-8")
    print(f"[RunPod Train] Training Complete in {elapsed}s! Saved PyTorch model to {MODELS_DIR / 'skills_predictor.pt'}")
    print(f"[RunPod Train] Skill F1: {skill_f1:.4f} | Emerging Demand Accuracy: {demand_acc:.4f}")
    return metrics

def train_sklearn():
    print("[RunPod Train Fallback] Training via Scikit-Learn MultiOutput Classifier + LogisticRegression...")
    warnings.filterwarnings("ignore")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.metrics import f1_score, accuracy_score
    import joblib
    import numpy as np

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    texts = [d["text"] for d in data]
    skill_labels = np.array([d["labels"] for d in data], dtype=int)
    demand_labels = np.array([d["is_emerging_demand"] for d in data], dtype=int)

    vectorizer = TfidfVectorizer(max_features=1024, ngram_range=(1, 3))
    X = vectorizer.fit_transform(texts)

    split = int(len(texts) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_skills_train, y_skills_test = skill_labels[:split], skill_labels[split:]
    y_dem_train, y_dem_test = demand_labels[:split], demand_labels[split:]

    start_time = time.time()
    # Train multi-output classifier for skills with LogisticRegression (high multi-label precision)
    clf_skills = MultiOutputClassifier(LogisticRegression(C=5.0, max_iter=200, random_state=42))
    clf_skills.fit(X_train, y_skills_train)

    # Train binary demand classifier
    clf_demand = LogisticRegression(C=2.0, max_iter=200, random_state=42)
    clf_demand.fit(X_train, y_dem_train)

    elapsed = round(time.time() - start_time, 2)

    pred_skills = clf_skills.predict(X_test)
    pred_dem = clf_demand.predict(X_test)

    skill_f1 = float(f1_score(y_skills_test, pred_skills, average="micro"))
    dem_acc = float(accuracy_score(y_dem_test, pred_dem))

    joblib.dump({
        "vectorizer": vectorizer,
        "clf_skills": clf_skills,
        "clf_demand": clf_demand,
        "skill_keys": SKILL_KEYS
    }, MODELS_DIR / "skills_predictor.joblib")

    metrics = {
        "framework": "Scikit-Learn (MultiOutputClassifier + LogisticRegression)",
        "device": "CPU",
        "epochs": 200,
        "elapsed_seconds": elapsed,
        "skill_f1_score": round(skill_f1, 4),
        "demand_accuracy": round(dem_acc, 4),
        "dataset_size": len(data),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    LOG_PATH.write_text(f"Scikit-Learn Model Training Finished in {elapsed}s\nSkill F1: {skill_f1:.4f}\nDemand Accuracy: {dem_acc:.4f}", encoding="utf-8")
    print(f"[RunPod Train] Training Complete in {elapsed}s! Saved model to {MODELS_DIR / 'skills_predictor.joblib'}")
    print(f"[RunPod Train] Skill F1: {skill_f1:.4f} | Demand Accuracy: {dem_acc:.4f}")
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Train RunPod Skills & Demand Predictor")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--epochs", type=int, default=25)
    args = parser.parse_args()

    try:
        import torch
        dev = "cuda" if (args.device in ("auto", "cuda") and torch.cuda.is_available()) else "cpu"
        train_pytorch(device_name=dev, epochs=args.epochs)
    except ImportError:
        train_sklearn()

if __name__ == "__main__":
    main()
