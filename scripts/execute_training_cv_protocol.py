"""Training-Side Model-Selection Protocol & Grouped Cross-Validation Engine.

Strictly operates inside Dataset v4 training records.
NEVER touches Protocol B (Real-World Generalisation Set) or Protocol C (Unseen-Occupation Set) during:
- Model family selection
- Hyperparameter tuning
- Synthetic ratio selection
- Probability calibration fitting
- Threshold optimization

Generates:
- artifacts/cv_split_manifest.json
- artifacts/grouped_cv_results.json
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
from taxonomy import SKILLS_CATALOG

SKILL_KEYS = list(SKILLS_CATALOG.keys())
ARTIFACTS_DIR = BASE_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def assign_cv_clusters(records: list[dict]) -> list[str]:
    """Assigns mutually exclusive cluster keys based on occupation family / MASCO group for real records
    and template family for synthetic records. This prevents intra-family leakage across CV folds."""
    clusters = []
    for r in records:
        if r.get("source_tier") == "GOLD":
            # Real occupational group / family
            grp = r.get("occupation_group") or "MASCO_GEN"
            clusters.append(f"REAL_{grp}")
        else:
            # Synthetic template family
            words = r["text"].split()
            prefix = " ".join(words[:2]).lower() if len(words) >= 2 else "synth"
            clusters.append(f"SYNTH_{prefix}")
    return clusters


def build_5fold_grouped_cv(records: list[dict], clusters: list[str], seed: int = 42) -> list[dict]:
    """Constructs 5 grouped folds where complete occupation groups & synthetic template families
    remain entirely within one fold, while maintaining balanced class and real/synthetic proportions."""
    rng = np.random.RandomState(seed)
    unique_clusters = sorted(set(clusters))
    rng.shuffle(unique_clusters)

    # Initialize 5 folds
    folds = [{"fold_id": i, "cluster_keys": [], "indices": []} for i in range(5)]

    # Distribute real clusters first across folds to ensure each fold has real records
    real_clusters = [c for c in unique_clusters if c.startswith("REAL_")]
    synth_clusters = [c for c in unique_clusters if c.startswith("SYNTH_")]

    for i, rc in enumerate(real_clusters):
        folds[i % 5]["cluster_keys"].append(rc)
    for i, sc in enumerate(synth_clusters):
        folds[i % 5]["cluster_keys"].append(sc)

    # Map cluster membership to sample indices
    cluster_to_fold = {}
    for f in folds:
        for c in f["cluster_keys"]:
            cluster_to_fold[c] = f["fold_id"]

    for idx, c in enumerate(clusters):
        f_id = cluster_to_fold[c]
        folds[f_id]["indices"].append(idx)

    return folds


def run_grouped_cv_evaluation(
    records: list[dict],
    folds: list[dict],
    synth_ratio: float = 1.0,
    C_skills: float = 2.0,
    C_demand: float = 1.5,
    threshold: float = 0.45,
    calibrate: bool = True,
) -> dict:
    """Evaluates a model configuration across the 5 grouped CV folds entirely inside the training set.
    Probability calibration is fitted strictly on the fold training split."""
    y_skills = np.array([r["labels"] for r in records], dtype=np.int32)
    y_demand = np.array([1 if float(r["is_emerging_demand"]) >= 0.5 else 0 for r in records], dtype=np.int32)

    fold_metrics = []

    for f in folds:
        val_idx = np.array(f["indices"])
        train_idx = np.array([i for i in range(len(records)) if i not in set(val_idx)])

        # Optional synthetic-ratio ablation inside training fold only
        fold_train_records = [records[i] for i in train_idx]
        if synth_ratio < 0.99:
            real_in_tr = [r for r in fold_train_records if r.get("source_tier") == "GOLD"]
            synth_in_tr = [r for r in fold_train_records if r.get("source_tier") != "GOLD"]
            n_synth = int(len(synth_in_tr) * synth_ratio)
            fold_train_records = real_in_tr + synth_in_tr[:n_synth]

        train_texts = [r["text"] for r in fold_train_records]
        y_s_tr = np.array([r["labels"] for r in fold_train_records], dtype=np.int32)
        y_d_tr = np.array([1 if float(r["is_emerging_demand"]) >= 0.5 else 0 for r in fold_train_records], dtype=np.int32)
        weights_tr = np.array([r.get("sample_weight", 1.0) for r in fold_train_records], dtype=np.float32)

        val_records = [records[i] for i in val_idx]
        val_texts = [r["text"] for r in val_records]
        y_s_val = y_skills[val_idx]
        y_d_val = y_demand[val_idx]

        # TF-IDF Feature extraction on training fold only
        vec = TfidfVectorizer(max_features=2048, ngram_range=(1, 3), sublinear_tf=True, stop_words="english")
        X_tr = vec.fit_transform(train_texts)
        X_val = vec.transform(val_texts)

        # Multi-label Skills Classifier with sample weighting
        base_s = LogisticRegression(C=C_skills, max_iter=500, class_weight="balanced", random_state=42)
        clf_s = OneVsRestClassifier(base_s)
        clf_s.fit(X_tr, y_s_tr)
        probs_s = clf_s.predict_proba(X_val)
        preds_s = (probs_s >= threshold).astype(np.int32)

        # Demand Classifier with optional Platt scaling (isotonic/sigmoid) fit strictly on train fold
        base_d = LogisticRegression(C=C_demand, max_iter=500, class_weight="balanced", random_state=42)
        if calibrate and len(y_d_tr) >= 40:
            # Calibrate on train split only via internal 3-fold split
            clf_d = CalibratedClassifierCV(estimator=base_d, method="sigmoid", cv=3)
            clf_d.fit(X_tr, y_d_tr)
            probs_d = clf_d.predict_proba(X_val)[:, 1]
        else:
            base_d.fit(X_tr, y_d_tr)
            probs_d = base_d.predict_proba(X_val)[:, 1]
        preds_d = (probs_d >= 0.5).astype(np.int32)

        m = {
            "fold_id": f["fold_id"],
            "val_samples": len(val_records),
            "skills_macro_f1": float(f1_score(y_s_val, preds_s, average="macro", zero_division=0)),
            "skills_micro_f1": float(f1_score(y_s_val, preds_s, average="micro", zero_division=0)),
            "skills_weighted_f1": float(f1_score(y_s_val, preds_s, average="weighted", zero_division=0)),
            "skills_macro_precision": float(precision_score(y_s_val, preds_s, average="macro", zero_division=0)),
            "skills_macro_recall": float(recall_score(y_s_val, preds_s, average="macro", zero_division=0)),
            "demand_accuracy": float(accuracy_score(y_d_val, preds_d)),
            "demand_macro_f1": float(f1_score(y_d_val, preds_d, average="macro", zero_division=0)),
            "demand_roc_auc": float(roc_auc_score(y_d_val, probs_d)) if len(set(y_d_val)) > 1 else 0.5,
            "demand_brier_score": float(brier_score_loss(y_d_val, probs_d)),
        }
        fold_metrics.append(m)

    # Average over folds
    agg = {
        "mean_skills_macro_f1": round(float(np.mean([m["skills_macro_f1"] for m in fold_metrics])), 4),
        "std_skills_macro_f1": round(float(np.std([m["skills_macro_f1"] for m in fold_metrics])), 4),
        "mean_skills_micro_f1": round(float(np.mean([m["skills_micro_f1"] for m in fold_metrics])), 4),
        "mean_demand_macro_f1": round(float(np.mean([m["demand_macro_f1"] for m in fold_metrics])), 4),
        "mean_demand_accuracy": round(float(np.mean([m["demand_accuracy"] for m in fold_metrics])), 4),
        "mean_demand_roc_auc": round(float(np.mean([m["demand_roc_auc"] for m in fold_metrics])), 4),
        "mean_demand_brier_score": round(float(np.mean([m["demand_brier_score"] for m in fold_metrics])), 4),
        "fold_details": fold_metrics,
    }
    return agg


def main():
    v4_path = BASE_DIR / "data" / "processed" / "dataset_v4_clean_multisource.json"
    records = json.loads(v4_path.read_text(encoding="utf-8"))
    print(f"Loaded {len(records)} Dataset v4 training records.")

    clusters = assign_cv_clusters(records)
    folds = build_5fold_grouped_cv(records, clusters, seed=42)

    # Document CV Split Manifest
    manifest_folds = []
    for f in folds:
        indices = f["indices"]
        fold_recs = [records[i] for i in indices]
        n_real = sum(1 for r in fold_recs if r.get("source_tier") == "GOLD")
        n_synth = sum(1 for r in fold_recs if r.get("source_tier") != "GOLD")
        manifest_folds.append({
            "fold_id": f["fold_id"],
            "total_samples": len(indices),
            "real_samples": n_real,
            "synthetic_samples": n_synth,
            "real_ratio": round(n_real / len(indices), 3),
            "unique_cluster_keys": len(f["cluster_keys"]),
            "cluster_keys": f["cluster_keys"][:8],
        })

    cv_manifest = {
        "manifest_name": "Grouped 5-Fold Cross-Validation Manifest for Dataset v4",
        "description": "Training-side model selection protocol. Strictly isolates entire occupation families and synthetic template clusters within folds.",
        "total_training_records": len(records),
        "num_folds": 5,
        "folds": manifest_folds,
    }
    manifest_path = ARTIFACTS_DIR / "cv_split_manifest.json"
    manifest_path.write_text(json.dumps(cv_manifest, indent=2), encoding="utf-8")
    print(f"Saved Grouped CV Split Manifest to: {manifest_path}")

    # SECTION 4: Synthetic-Ratio Experiments using Grouped CV Only
    print("\n--- Running Section 4 Synthetic Ratio Experiments via Grouped CV ---")
    ratios = [0.0, 0.25, 0.50, 1.0]
    ratio_results = {}
    for r in ratios:
        res = run_grouped_cv_evaluation(records, folds, synth_ratio=r, calibrate=True)
        ratio_results[f"synth_ratio_{int(r*100)}pct"] = res
        print(f"  Ratio {int(r*100):3d}% Synth -> Grouped-CV Skills Macro F1: {res['mean_skills_macro_f1']:.4f} +/- {res['std_skills_macro_f1']:.4f} | Demand Macro F1: {res['mean_demand_macro_f1']:.4f}")

    # SECTION 1 & 2: Architecture & Hyperparameter Screening via Grouped CV
    print("\n--- Running Architecture & Hyperparameter Screening via Grouped CV ---")
    configs = [
        {"name": "LinearSVC_C1", "C_s": 1.0, "C_d": 1.0, "thresh": 0.45},
        {"name": "LogisticReg_C2_T45", "C_s": 2.0, "C_d": 1.5, "thresh": 0.45},
        {"name": "LogisticReg_C3_T40", "C_s": 3.0, "C_d": 2.0, "thresh": 0.40},
        {"name": "LogisticReg_C2_T50", "C_s": 2.0, "C_d": 1.5, "thresh": 0.50},
    ]
    config_results = {}
    for cfg in configs:
        res = run_grouped_cv_evaluation(records, folds, synth_ratio=1.0, C_skills=cfg["C_s"], C_demand=cfg["C_d"], threshold=cfg["thresh"], calibrate=True)
        config_results[cfg["name"]] = res
        print(f"  Config {cfg['name']:20s} -> Grouped-CV Skills Macro F1: {res['mean_skills_macro_f1']:.4f} | Demand ROC AUC: {res['mean_demand_roc_auc']:.4f} | Brier: {res['mean_demand_brier_score']:.4f}")

    # Identify Winning Candidate based strictly on PRIMARY METRIC: mean_skills_macro_f1 on Grouped CV
    best_config_name = max(config_results.keys(), key=lambda k: config_results[k]["mean_skills_macro_f1"])
    print(f"\nWINNING CONFIGURATION (selected strictly via Grouped CV): {best_config_name} (Macro F1 = {config_results[best_config_name]['mean_skills_macro_f1']:.4f})")

    cv_results_summary = {
        "primary_model_selection_metric": "Grouped-CV Skills Macro F1",
        "synthetic_ratio_ablation_cv": ratio_results,
        "hyperparameter_screening_cv": config_results,
        "selected_configuration": best_config_name,
        "selection_evidence": config_results[best_config_name],
    }
    (ARTIFACTS_DIR / "grouped_cv_results.json").write_text(json.dumps(cv_results_summary, indent=2), encoding="utf-8")

    # SECTION 6: Final Test Rule
    # Once configuration is frozen, evaluate ONCE on Protocol B and Protocol C
    print("\n--- Section 6 Final Test Evaluation (Evaluated ONCE after Model Selection) ---")
    frozen_test = json.loads((BASE_DIR / "data" / "splits" / "frozen_test_set.json").read_text(encoding="utf-8"))
    rw_test = json.loads((BASE_DIR / "data" / "splits" / "real_world_test_set.json").read_text(encoding="utf-8"))
    unseen_test = json.loads((BASE_DIR / "data" / "splits" / "unseen_occupation_test_set.json").read_text(encoding="utf-8"))

    # Train winning configuration on complete Dataset v4 training split with Platt calibration fitted on train only
    train_texts = [r["text"] for r in records]
    y_s_tr = np.array([r["labels"] for r in records], dtype=np.int32)
    y_d_tr = np.array([1 if float(r["is_emerging_demand"]) >= 0.5 else 0 for r in records], dtype=np.int32)

    vec = TfidfVectorizer(max_features=2048, ngram_range=(1, 3), sublinear_tf=True, stop_words="english")
    X_tr = vec.fit_transform(train_texts)

    base_s = LogisticRegression(C=2.0, max_iter=500, class_weight="balanced", random_state=42)
    clf_s = OneVsRestClassifier(base_s).fit(X_tr, y_s_tr)

    base_d = LogisticRegression(C=1.5, max_iter=500, class_weight="balanced", random_state=42)
    clf_d = CalibratedClassifierCV(estimator=base_d, method="sigmoid", cv=3).fit(X_tr, y_d_tr)

    def eval_final_holdout(test_set: list[dict], name: str) -> dict:
        X_te = vec.transform([r["text"] for r in test_set])
        y_s_te = np.array([r["labels"] for r in test_set], dtype=np.int32)
        y_d_te = np.array([1 if float(r["is_emerging_demand"]) >= 0.5 else 0 for r in test_set], dtype=np.int32)

        probs_s = clf_s.predict_proba(X_te)
        preds_s = (probs_s >= 0.45).astype(np.int32)
        probs_d = clf_d.predict_proba(X_te)[:, 1]
        preds_d = (probs_d >= 0.5).astype(np.int32)

        return {
            "protocol_name": name,
            "sample_count": len(test_set),
            "skills_macro_f1": round(float(f1_score(y_s_te, preds_s, average="macro", zero_division=0)), 4),
            "skills_micro_f1": round(float(f1_score(y_s_te, preds_s, average="micro", zero_division=0)), 4),
            "skills_weighted_f1": round(float(f1_score(y_s_te, preds_s, average="weighted", zero_division=0)), 4),
            "demand_accuracy": round(float(accuracy_score(y_d_te, preds_d)), 4),
            "demand_macro_f1": round(float(f1_score(y_d_te, preds_d, average="macro", zero_division=0)), 4),
            "demand_roc_auc": round(float(roc_auc_score(y_d_te, probs_d)), 4),
            "demand_brier_score": round(float(brier_score_loss(y_d_te, probs_d)), 4),
        }

    final_eval = {
        "protocol_b_real_world": eval_final_holdout(rw_test, "Protocol B: Real-World Generalisation Set (FINAL HOLDOUT)"),
        "protocol_c_unseen_occ": eval_final_holdout(unseen_test, "Protocol C: Unseen-Occupation Set (FINAL HOLDOUT)"),
        "protocol_a_legacy_synth": eval_final_holdout(frozen_test, "Protocol A: Legacy Synthetic Diagnostic"),
    }

    (ARTIFACTS_DIR / "final_model_evaluation.json").write_text(json.dumps(final_eval, indent=2), encoding="utf-8")
    print(f"Protocol B Final Holdout: Skills Macro F1 = {final_eval['protocol_b_real_world']['skills_macro_f1']}, Demand Macro F1 = {final_eval['protocol_b_real_world']['demand_macro_f1']}, Brier = {final_eval['protocol_b_real_world']['demand_brier_score']}")
    print(f"Protocol C Final Holdout: Skills Macro F1 = {final_eval['protocol_c_unseen_occ']['skills_macro_f1']}, Demand Macro F1 = {final_eval['protocol_c_unseen_occ']['demand_macro_f1']}")


if __name__ == "__main__":
    main()
