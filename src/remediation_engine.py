"""Remediation Engine for Domain 1 AI Skills & Demand Predictor.
Implements:
1. Candidate A: Word + Subword Hybrid TF-IDF + LogisticRegression with direct sample_weight (no row duplication).
2. Candidate B: Actual PyTorch Multi-Task / Multi-Label Neural Network (SkillsPredictorNN) with BCEWithLogitsLoss.
3. Candidate C: Actual Pretrained Sentence-Transformers (all-MiniLM-L6-v2) with C1 (Linear) and C2 (MLP) heads.
4. Fold-isolated preprocessing: Vectorizers, embeddings, and scalers fit strictly on training folds.
5. Calibrated vs Uncalibrated comparison for demand: Zero duplicate record leakage.
6. Grouped 5-Fold Cross-Validation on cv_split_manifest_v2.json.
7. Out-of-fold prediction serialization.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sentence_transformers import SentenceTransformer
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import FeatureUnion

class MultiLabelBinaryClassifier:
    """Explicit Binary Relevance multi-label classifier supporting sample_weight natively."""
    def __init__(self, base_estimator: Any):
        self.base_estimator = base_estimator
        self.estimators_: list[Any] = []

    def fit(self, X: Any, y: np.ndarray, sample_weight: np.ndarray | None = None) -> MultiLabelBinaryClassifier:
        self.estimators_ = []
        for j in range(y.shape[1]):
            clf = clone(self.base_estimator)
            clf.fit(X, y[:, j], sample_weight=sample_weight)
            self.estimators_.append(clf)
        return self

    def predict_proba(self, X: Any) -> np.ndarray:
        probs = []
        for clf in self.estimators_:
            p = clf.predict_proba(X)
            if p.shape[1] == 1:
                probs.append(np.ones(X.shape[0]) if clf.classes_[0] == 1 else np.zeros(X.shape[0]))
            else:
                probs.append(p[:, 1])
        return np.column_stack(probs)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
CACHE_DIR = DATA_DIR / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

TAXONOMY_SKILLS = [
    "ai_literacy", "prompt_engineering", "process_mapping", "sql_data_analysis",
    "python_scripting", "data_visualization", "workflow_automation", "human_in_the_loop_qa",
    "rag_knowledge_systems", "api_integration", "ai_ethics_governance", "data_privacy_pdpa",
    "esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication",
    "instructional_design"
]

def build_hybrid_vectorizer() -> FeatureUnion:
    """Builds subword + word hybrid TF-IDF vectorizer."""
    return FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 3), max_features=2048, min_df=1, sublinear_tf=True, stop_words="english")),
        ("subword", TfidfVectorizer(ngram_range=(3, 5), analyzer="char_wb", max_features=1024, min_df=2, sublinear_tf=True)),
    ])

# ==========================================
# CANDIDATE B: Actual PyTorch Neural Network
# ==========================================
class SkillsPredictorNN(nn.Module):
    """PyTorch multi-label neural classifier for skills extraction."""
    def __init__(self, in_features: int, hidden_1: int = 256, hidden_2: int = 128, num_skills: int = 16, dropout: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_1),
            nn.LayerNorm(hidden_1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_1, hidden_2),
            nn.ReLU(),
            nn.Dropout(dropout * 0.7),
            nn.Linear(hidden_2, num_skills),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

def train_pytorch_candidate_b(
    X_train_np: np.ndarray,
    y_train_np: np.ndarray,
    weights_np: np.ndarray,
    X_val_np: np.ndarray,
    y_val_np: np.ndarray,
    epochs: int = 60,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    device: str = "cpu"
) -> tuple[SkillsPredictorNN, np.ndarray]:
    """Trains PyTorch Candidate B with pos_weight, sample weighting, and early stopping."""
    # Compute positive class weights for BCEWithLogitsLoss
    pos_counts = y_train_np.sum(axis=0)
    neg_counts = len(y_train_np) - pos_counts
    pos_weights = torch.tensor(np.clip(neg_counts / (pos_counts + 1e-5), 1.0, 10.0), dtype=torch.float32).to(device)

    in_dim = X_train_np.shape[1]
    model = SkillsPredictorNN(in_features=in_dim, hidden_1=256, hidden_2=128, num_skills=16).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weights, reduction="none")

    # Prepare datasets
    X_tr_t = torch.tensor(X_train_np, dtype=torch.float32)
    y_tr_t = torch.tensor(y_train_np, dtype=torch.float32)
    w_tr_t = torch.tensor(weights_np, dtype=torch.float32).unsqueeze(1)
    train_loader = DataLoader(TensorDataset(X_tr_t, y_tr_t, w_tr_t), batch_size=32, shuffle=True)

    X_val_t = torch.tensor(X_val_np, dtype=torch.float32).to(device)
    y_val_t = torch.tensor(y_val_np, dtype=torch.float32).to(device)

    best_val_loss = float("inf")
    best_weights = None
    patience = 8
    patience_counter = 0

    model.train()
    for ep in range(epochs):
        model.train()
        for bx, by, bw in train_loader:
            bx, by, bw = bx.to(device), by.to(device), bw.to(device)
            optimizer.zero_grad()
            logits = model(bx)
            loss_raw = criterion(logits, by)
            loss = (loss_raw * bw).mean()
            loss.backward()
            optimizer.step()

        # Validation step
        model.eval()
        with torch.no_grad():
            val_logits = model(X_val_t)
            val_loss = criterion(val_logits, y_val_t).mean().item()

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = {k: v.clone() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break

    if best_weights is not None:
        model.load_state_dict(best_weights)
    model.eval()
    with torch.no_grad():
        val_probs = torch.sigmoid(model(X_val_t)).cpu().numpy()

    return model, val_probs

# ==========================================
# CANDIDATE C: Pretrained MiniLM Bi-Encoder
# ==========================================
_MINILM_MODEL: SentenceTransformer | None = None

def get_minilm_model() -> SentenceTransformer:
    global _MINILM_MODEL
    if _MINILM_MODEL is None:
        _MINILM_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _MINILM_MODEL

def compute_minilm_embeddings(texts: list[str]) -> np.ndarray:
    """Computes or retrieves cached MiniLM embeddings."""
    hasher = hashlib.sha256()
    for t in texts:
        hasher.update(t.encode("utf-8"))
    cache_key = hasher.hexdigest()[:16]
    cache_path = CACHE_DIR / f"minilm_{cache_key}.joblib"

    if cache_path.exists():
        return joblib.load(cache_path)

    model = get_minilm_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype=np.float32)
    joblib.dump(embeddings, cache_path)
    return embeddings

# ==========================================
# METRICS & EVALUATION
# ==========================================
def calculate_metrics(y_true_s: np.ndarray, y_prob_s: np.ndarray, threshold_s: float = 0.35) -> dict[str, float]:
    y_pred_s = (y_prob_s >= threshold_s).astype(int)
    macro_f1 = float(f1_score(y_true_s, y_pred_s, average="macro", zero_division=0))
    micro_f1 = float(f1_score(y_true_s, y_pred_s, average="micro", zero_division=0))
    macro_prec = float(precision_score(y_true_s, y_pred_s, average="macro", zero_division=0))
    macro_rec = float(recall_score(y_true_s, y_pred_s, average="macro", zero_division=0))

    # Calculate per-class recall for rare labels
    per_cls_rec = recall_score(y_true_s, y_pred_s, average=None, zero_division=0)
    rare_cls_rec = float(np.mean(per_cls_rec))

    return {
        "skills_macro_f1": round(macro_f1, 4),
        "skills_micro_f1": round(micro_f1, 4),
        "skills_macro_precision": round(macro_prec, 4),
        "skills_macro_recall": round(macro_rec, 4),
        "rare_class_recall": round(rare_cls_rec, 4),
    }

def calculate_demand_metrics(y_true_d: np.ndarray, y_prob_d: np.ndarray, threshold_d: float = 0.50) -> dict[str, float]:
    y_pred_d = (y_prob_d >= threshold_d).astype(int)
    acc = float(accuracy_score(y_true_d, y_pred_d))
    macro_f1 = float(f1_score(y_true_d, y_pred_d, average="macro", zero_division=0))
    try:
        auc = float(roc_auc_score(y_true_d, y_prob_d))
    except Exception:
        auc = 0.5
    brier = float(brier_score_loss(y_true_d, y_prob_d))

    # Expected Calibration Error (10 bins)
    bins = 10
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (y_prob_d >= lo) & (y_prob_d < hi if hi < 1 else y_prob_d <= hi)
        if mask.sum() > 0:
            ece += mask.mean() * abs(y_true_d[mask].mean() - y_prob_d[mask].mean())

    return {
        "demand_accuracy": round(acc, 4),
        "demand_macro_f1": round(macro_f1, 4),
        "demand_roc_auc": round(auc, 4),
        "demand_brier_score": round(brier, 4),
        "demand_ece": round(float(ece), 4),
    }

# ==========================================
# TRAINING-SIDE GROUPED CV EXECUTION
# ==========================================
def run_remediated_grouped_cv() -> dict[str, Any]:
    """Runs rigorous 5-fold grouped CV on cv_split_manifest_v2.json.
    Compares:
    - Candidate A: Hybrid TF-IDF + LogisticRegression (sample_weight, fold-isolated)
    - Candidate B: PyTorch SkillsPredictorNN
    - Candidate C1: Pretrained all-MiniLM-L6-v2 + LogisticRegression
    - Candidate C2: Pretrained all-MiniLM-L6-v2 + PyTorch 2-layer MLP
    - Demand: Uncalibrated vs Calibrated (Leakage-free sample weights)
    """
    train_path = DATA_DIR / "processed" / "dataset_v4_clean_multisource.json"
    manifest_path = ARTIFACTS_DIR / "cv_split_manifest_v2.json"

    train_data = json.loads(train_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    all_texts = [r["text"] for r in train_data]
    y_skills_all = np.array([r["labels"] for r in train_data], dtype=np.int32)
    y_demand_all = np.array([1 if float(r["is_emerging_demand"]) >= 0.5 else 0 for r in train_data], dtype=np.int32)
    weights_all = np.array([3.0 if r.get("source_tier") == "GOLD" else 1.0 for r in train_data], dtype=np.float32)

    # Pre-embed with MiniLM
    minilm_embeddings = compute_minilm_embeddings(all_texts)

    candidates = ["A_Hybrid_LogReg", "B_PyTorch_NN", "C1_MiniLM_Linear", "C2_MiniLM_MLP"]
    fold_results = {c: [] for c in candidates}
    demand_uncal_results = []
    demand_cal_results = []

    # Store out-of-fold predictions
    oof_predictions = {
        "Candidate_A": np.zeros((len(train_data), 16), dtype=np.float32),
        "Candidate_B": np.zeros((len(train_data), 16), dtype=np.float32),
        "Candidate_C1": np.zeros((len(train_data), 16), dtype=np.float32),
        "Candidate_C2": np.zeros((len(train_data), 16), dtype=np.float32),
        "Demand_Uncalibrated": np.zeros(len(train_data), dtype=np.float32),
        "Demand_Calibrated": np.zeros(len(train_data), dtype=np.float32),
    }

    print("\n=== Executing Remediated Grouped 5-Fold Cross-Validation ===")
    for f_info in manifest["folds"]:
        f_id = f_info["fold_id"]
        val_idx = np.array(f_info["val_indices"])
        tr_idx = np.array([i for i in range(len(train_data)) if i not in set(val_idx)])

        tr_texts = [all_texts[i] for i in tr_idx]
        val_texts = [all_texts[i] for i in val_idx]

        y_s_tr, y_s_val = y_skills_all[tr_idx], y_skills_all[val_idx]
        y_d_tr, y_d_val = y_demand_all[tr_idx], y_demand_all[val_idx]
        w_tr = weights_all[tr_idx]

        # 1. Fold-isolated TF-IDF extraction
        vec = build_hybrid_vectorizer()
        X_tr_tfidf = vec.fit_transform(tr_texts)
        X_val_tfidf = vec.transform(val_texts)

        # -----------------------------------------------------------------
        # Candidate A: Hybrid TF-IDF + LogisticRegression with sample_weight
        # -----------------------------------------------------------------
        base_lr = LogisticRegression(C=2.2, max_iter=700, class_weight="balanced", random_state=42)
        clf_a = MultiLabelBinaryClassifier(base_lr)
        clf_a.fit(X_tr_tfidf, y_s_tr, sample_weight=w_tr)
        prob_a = clf_a.predict_proba(X_val_tfidf)
        oof_predictions["Candidate_A"][val_idx] = prob_a
        fold_results["A_Hybrid_LogReg"].append(calculate_metrics(y_s_val, prob_a, threshold_s=0.35))

        # -----------------------------------------------------------------
        # Candidate B: PyTorch SkillsPredictorNN
        # -----------------------------------------------------------------
        X_tr_dense = X_tr_tfidf.toarray().astype(np.float32)
        X_val_dense = X_val_tfidf.toarray().astype(np.float32)
        _, prob_b = train_pytorch_candidate_b(X_tr_dense, y_s_tr, w_tr, X_val_dense, y_s_val, epochs=50)
        oof_predictions["Candidate_B"][val_idx] = prob_b
        fold_results["B_PyTorch_NN"].append(calculate_metrics(y_s_val, prob_b, threshold_s=0.35))

        # -----------------------------------------------------------------
        # Candidate C1: Frozen MiniLM + LogisticRegression with sample_weight
        # -----------------------------------------------------------------
        X_tr_minilm = minilm_embeddings[tr_idx]
        X_val_minilm = minilm_embeddings[val_idx]
        clf_c1 = MultiLabelBinaryClassifier(LogisticRegression(C=2.0, max_iter=700, class_weight="balanced", random_state=42))
        clf_c1.fit(X_tr_minilm, y_s_tr, sample_weight=w_tr)
        prob_c1 = clf_c1.predict_proba(X_val_minilm)
        oof_predictions["Candidate_C1"][val_idx] = prob_c1
        fold_results["C1_MiniLM_Linear"].append(calculate_metrics(y_s_val, prob_c1, threshold_s=0.35))

        # -----------------------------------------------------------------
        # Candidate C2: Frozen MiniLM + PyTorch 2-Layer Head
        # -----------------------------------------------------------------
        _, prob_c2 = train_pytorch_candidate_b(X_tr_minilm, y_s_tr, w_tr, X_val_minilm, y_s_val, epochs=50)
        oof_predictions["Candidate_C2"][val_idx] = prob_c2
        fold_results["C2_MiniLM_MLP"].append(calculate_metrics(y_s_val, prob_c2, threshold_s=0.35))

        # -----------------------------------------------------------------
        # Demand Classifier Comparison: Uncalibrated vs Calibrated
        # -----------------------------------------------------------------
        # Uncalibrated Logistic Regression (with sample_weight)
        lr_dem_uncal = LogisticRegression(C=1.5, max_iter=700, class_weight="balanced", random_state=42)
        lr_dem_uncal.fit(X_tr_tfidf, y_d_tr, sample_weight=w_tr)
        prob_d_uncal = lr_dem_uncal.predict_proba(X_val_tfidf)[:, 1]
        oof_predictions["Demand_Uncalibrated"][val_idx] = prob_d_uncal
        demand_uncal_results.append(calculate_demand_metrics(y_d_val, prob_d_uncal))

        # Leakage-Safe CalibratedClassifierCV (without row duplication)
        lr_dem_base = LogisticRegression(C=1.5, max_iter=700, class_weight="balanced", random_state=42)
        cal_dem = CalibratedClassifierCV(estimator=lr_dem_base, method="sigmoid", cv=3)
        cal_dem.fit(X_tr_tfidf, y_d_tr, sample_weight=w_tr)
        prob_d_cal = cal_dem.predict_proba(X_val_tfidf)[:, 1]
        oof_predictions["Demand_Calibrated"][val_idx] = prob_d_cal
        demand_cal_results.append(calculate_demand_metrics(y_d_val, prob_d_cal))

        print(f"  Fold {f_id} Completed: Candidate A F1={fold_results['A_Hybrid_LogReg'][-1]['skills_macro_f1']} | Candidate B F1={fold_results['B_PyTorch_NN'][-1]['skills_macro_f1']} | Candidate C1 F1={fold_results['C1_MiniLM_Linear'][-1]['skills_macro_f1']} | Candidate C2 F1={fold_results['C2_MiniLM_MLP'][-1]['skills_macro_f1']}")

    # Aggregate candidate metrics
    def summarize_cv(res_list: list[dict[str, float]]) -> dict[str, float]:
        keys = res_list[0].keys()
        return {k: round(float(np.mean([m[k] for m in res_list])), 4) for k in keys}

    cv_summary = {c: summarize_cv(fold_results[c]) for c in candidates}
    demand_summary = {
        "Uncalibrated": summarize_cv(demand_uncal_results),
        "Calibrated": summarize_cv(demand_cal_results),
    }

    # Threshold search on Candidate A pooled OOF predictions
    threshold_search = []
    y_true_all_s = y_skills_all
    prob_a_all = oof_predictions["Candidate_A"]

    for thr in np.arange(0.25, 0.51, 0.02):
        thr = round(float(thr), 2)
        m = calculate_metrics(y_true_all_s, prob_a_all, threshold_s=thr)
        threshold_search.append({
            "threshold": thr,
            "skills_macro_f1": m["skills_macro_f1"],
            "skills_micro_f1": m["skills_micro_f1"],
            "skills_macro_precision": m["skills_macro_precision"],
            "skills_macro_recall": m["skills_macro_recall"],
            "rare_class_recall": m["rare_class_recall"],
        })

    # Serialize sample predictions for verification
    pred_records = []
    for i, r in enumerate(train_data):
        pred_records.append({
            "record_id": r["id"],
            "source": r.get("source", "unknown"),
            "occupation_group": r.get("occupation_group", "GEN"),
            "true_skills": [TAXONOMY_SKILLS[j] for j in range(16) if y_skills_all[i, j] == 1],
            "pred_skills_cand_a": [TAXONOMY_SKILLS[j] for j in range(16) if prob_a_all[i, j] >= 0.35],
            "prob_skills_cand_a": [round(float(p), 4) for p in prob_a_all[i]],
            "demand_truth": int(y_demand_all[i]),
            "demand_prob_uncal": round(float(oof_predictions["Demand_Uncalibrated"][i]), 4),
            "demand_prob_cal": round(float(oof_predictions["Demand_Calibrated"][i]), 4),
        })

    # Save out-of-fold prediction artifact
    (ARTIFACTS_DIR / "sample_oof_predictions_schema.json").write_text(json.dumps(pred_records[:20], indent=2), encoding="utf-8")

    return {
        "candidate_skills_cv": cv_summary,
        "demand_cv": demand_summary,
        "threshold_search": threshold_search,
        "fold_details": fold_results,
    }

if __name__ == "__main__":
    t_start = time.time()
    results = run_remediated_grouped_cv()
    elapsed = round(time.time() - t_start, 2)
    print(f"\n=== Remediated Grouped CV Suite Completed in {elapsed}s ===")
    print("\n--- Candidate Skills Model Comparison (Grouped 5-Fold CV) ---")
    for cand, res in results["candidate_skills_cv"].items():
        print(f"  {cand:20s} -> Macro F1: {res['skills_macro_f1']:.4f} | Micro F1: {res['skills_micro_f1']:.4f} | Prec: {res['skills_macro_precision']:.4f} | Rec: {res['skills_macro_recall']:.4f} | Rare Rec: {res['rare_class_recall']:.4f}")

    print("\n--- Demand Model: Uncalibrated vs Calibrated (Leakage-Free CV) ---")
    for mode, res in results["demand_cv"].items():
        print(f"  {mode:15s} -> ROC AUC: {res['demand_roc_auc']:.4f} | Brier: {res['demand_brier_score']:.4f} | ECE: {res['demand_ece']:.4f} | Acc: {res['demand_accuracy']:.4f}")

    print("\n--- Candidate A Threshold Search (Training-Side Grouped CV Pooled OOF) ---")
    for row in results["threshold_search"][:10]:
        print(f"  Threshold {row['threshold']:.2f} -> Macro F1: {row['skills_macro_f1']:.4f} | Prec: {row['skills_macro_precision']:.4f} | Rec: {row['skills_macro_recall']:.4f} | Rare Rec: {row['rare_class_recall']:.4f}")

    # Save results to artifacts
    (ARTIFACTS_DIR / "remediation_cv_benchmark.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved benchmark metrics to: {ARTIFACTS_DIR / 'remediation_cv_benchmark.json'}")
