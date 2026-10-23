"""Ablation experiments evaluating models trained on baseline vs new datasets against frozen test set."""

import json
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score, roc_auc_score, brier_score_loss

BASE_DIR = Path(__file__).resolve().parent.parent

def evaluate_corpus(train_data, test_data, name: str):
    X_tr_t = [d["text"] for d in train_data]
    y_s_tr = np.array([d["labels"] for d in train_data], dtype=np.int32)
    y_d_tr = np.array([d["is_emerging_demand"] for d in train_data], dtype=np.int32)

    X_te_t = [d["text"] for d in test_data]
    y_s_te = np.array([d["labels"] for d in test_data], dtype=np.int32)
    y_d_te = np.array([d["is_emerging_demand"] for d in test_data], dtype=np.int32)

    vec = TfidfVectorizer(max_features=1024, ngram_range=(1, 3))
    X_tr = vec.fit_transform(X_tr_t)
    X_te = vec.transform(X_te_t)

    # Train multi-label skills classifier
    clf_s = OneVsRestClassifier(LogisticRegression(max_iter=300, class_weight="balanced", random_state=42))
    clf_s.fit(X_tr, y_s_tr)
    preds_s = clf_s.predict(X_te)

    # Train demand classifier
    clf_d = LogisticRegression(max_iter=300, class_weight="balanced", random_state=42)
    clf_d.fit(X_tr, y_d_tr)
    preds_d = clf_d.predict(X_te)
    probs_d = clf_d.predict_proba(X_te)[:, 1]

    metrics = {
        "dataset_name": name,
        "train_size": len(train_data),
        "test_size": len(test_data),
        "skills_micro_f1": round(float(f1_score(y_s_te, preds_s, average="micro", zero_division=0)), 4),
        "skills_macro_f1": round(float(f1_score(y_s_te, preds_s, average="macro", zero_division=0)), 4),
        "skills_weighted_f1": round(float(f1_score(y_s_te, preds_s, average="weighted", zero_division=0)), 4),
        "skills_macro_recall": round(float(recall_score(y_s_te, preds_s, average="macro", zero_division=0)), 4),
        "skills_macro_precision": round(float(precision_score(y_s_te, preds_s, average="macro", zero_division=0)), 4),
        "demand_accuracy": round(float(accuracy_score(y_d_te, preds_d)), 4),
        "demand_macro_f1": round(float(f1_score(y_d_te, preds_d, average="macro")), 4),
        "demand_roc_auc": round(float(roc_auc_score(y_d_te, probs_d)), 4),
        "demand_brier_score": round(float(brier_score_loss(y_d_te, probs_d)), 4)
    }
    return metrics, (vec, clf_s, clf_d)

def main():
    test_data = json.loads((BASE_DIR / "data" / "splits" / "frozen_test_set.json").read_text(encoding="utf-8"))
    
    # 1. Baseline: original 1,200 training records
    orig_data = json.loads((BASE_DIR / "data" / "training_dataset.json").read_text(encoding="utf-8"))[:1200]
    m_base, _ = evaluate_corpus(orig_data, test_data, "Baseline (Original 1200 Synthetic-Dominant)")

    # 2. Real sources only (OpenAlex + ESCO + MASCO)
    v2_data = json.loads((BASE_DIR / "data" / "processed" / "dataset_v2_real_sources.json").read_text(encoding="utf-8"))
    m_v2, _ = evaluate_corpus(v2_data, test_data, "Dataset v2 (319 Real Sources Only)")

    # 3. Real + Balanced Synthetic (Dataset v3)
    v3_data = json.loads((BASE_DIR / "data" / "processed" / "dataset_v3_real_plus_synthetic.json").read_text(encoding="utf-8"))
    m_v3, models = evaluate_corpus(v3_data, test_data, "Dataset v3 (Multi-Source Real + Controlled Synthetic)")

    results = [m_base, m_v2, m_v3]
    out_path = BASE_DIR / "data" / "manifests" / "ablation_results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n================ ABLATION STUDY RESULTS ================")
    print(f"{'Metric':<25} | {'Baseline':<12} | {'v2 (Real Only)':<15} | {'v3 (Multi-Source Balanced)':<25}")
    print("-" * 85)
    for k in ["skills_macro_f1", "skills_micro_f1", "skills_weighted_f1", "skills_macro_precision", "demand_accuracy", "demand_macro_f1", "demand_roc_auc", "demand_brier_score"]:
        print(f"{k:<25} | {m_base[k]:<12} | {m_v2[k]:<15} | {m_v3[k]:<25}")
    print("-" * 85)

    # Save best model to runpod/models/skills_predictor_v3.joblib
    import joblib
    model_export_path = BASE_DIR / "runpod" / "models" / "skills_predictor_v3.joblib"
    joblib.dump({
        "vectorizer": models[0],
        "clf_skills": models[1],
        "clf_demand": models[2],
        "dataset_version": "v3_real_plus_synthetic",
        "training_size": len(v3_data)
    }, model_export_path)
    print(f"\nModel artifact serialized to: {model_export_path}")

if __name__ == "__main__":
    main()
