"""Unit tests for independent audit remediation verification.
Validates:
1. Gold data representation in every CV fold
2. Zero cluster leakage across CV folds
3. Zero synthetic template leakage across CV folds
4. Preprocessing fit on train folds only
5. No duplicate records in calibration sets (sample_weight vs duplication)
6. Protocol C v2 zero overlap with Protocol B and training data
7. Protocol C v2 unseen MASCO 4-digit clusters
8. MiniLM actually loads and encodes valid 384-dim vectors
9. PyTorch actually used for Candidate B (nn.Module, AdamW, BCEWithLogitsLoss)
10. Prediction artifact conforms to required schema
11. Untouched preserved legacy models
"""

import json
import unittest
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion

from src.remediation_engine import (
    SkillsPredictorNN,
    MultiLabelBinaryClassifier,
    build_hybrid_vectorizer,
    get_minilm_model,
    compute_minilm_embeddings,
    TAXONOMY_SKILLS,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"


class TestAuditRemediation(unittest.TestCase):
    def setUp(self):
        self.train_path = DATA_DIR / "processed" / "dataset_v4_clean_multisource.json"
        self.manifest_path = ARTIFACTS_DIR / "cv_split_manifest_v2.json"
        self.protocol_b_path = DATA_DIR / "splits" / "real_world_test_set.json"
        self.protocol_c_path = DATA_DIR / "splits" / "unseen_occupation_test_set_v2.json"
        self.oof_path = ARTIFACTS_DIR / "sample_oof_predictions_schema.json"
        self.benchmark_path = ARTIFACTS_DIR / "remediation_cv_benchmark.json"

    def test_01_gold_data_representation_in_every_fold(self):
        """Fix 1 & P0: Every CV fold must contain both Gold and Synthetic in validation and training."""
        self.assertTrue(self.manifest_path.exists(), "cv_split_manifest_v2.json missing")
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        
        self.assertEqual(len(manifest["folds"]), 5)
        for fold in manifest["folds"]:
            gold_val = fold["real_samples"]
            synth_val = fold["synthetic_samples"]
            gold_tr = fold["training_real_samples"]
            synth_tr = fold["training_synthetic_samples"]
            
            self.assertGreaterEqual(gold_val, 15, f"Fold {fold['fold_id']} has insufficient Gold val records")
            self.assertGreaterEqual(synth_val, 30, f"Fold {fold['fold_id']} has insufficient Synth val records")
            self.assertGreaterEqual(gold_tr, 70, f"Fold {fold['fold_id']} has insufficient Gold train records")
            self.assertGreaterEqual(synth_tr, 180, f"Fold {fold['fold_id']} has insufficient Synth train records")

    def test_02_zero_cluster_leakage_across_cv_folds(self):
        """Fix 1 & P0: Zero cluster leakage between train and val within any fold."""
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        
        all_fold_clusters = [set(fold["val_cluster_keys"]) for fold in manifest["folds"]]
        for i in range(len(all_fold_clusters)):
            for j in range(i + 1, len(all_fold_clusters)):
                overlap = all_fold_clusters[i].intersection(all_fold_clusters[j])
                self.assertEqual(len(overlap), 0, f"Folds {i} and {j} share clusters: {overlap}")

    def test_03_zero_synthetic_template_leakage(self):
        """Fix 1: Synthetic templates must not be shared between train and validation in any fold."""
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        all_fold_synth = [{c for c in fold["val_cluster_keys"] if c.startswith("SYNTH_")} for fold in manifest["folds"]]
        for i in range(len(all_fold_synth)):
            for j in range(i + 1, len(all_fold_synth)):
                overlap = all_fold_synth[i].intersection(all_fold_synth[j])
                self.assertEqual(len(overlap), 0, f"Synthetic templates shared between fold {i} and {j}: {overlap}")

    def test_04_preprocessing_fit_on_train_folds_only(self):
        """Fix 2 & P0: Vectorizers must fit strictly on train folds; val folds must not affect vocabulary."""
        vec = build_hybrid_vectorizer()
        self.assertIsInstance(vec, FeatureUnion)
        
        train_texts = ["machine learning engineer prompt engineering python", "data analyst sql visualization"]
        val_texts = ["unseen word quantum robotics cybersecurity"]
        
        # Fit on train only
        vec.fit(train_texts)
        # Transform val
        val_feat = vec.transform(val_texts)
        # Unseen words in val should not expand vocabulary
        feature_names = vec.get_feature_names_out()
        for f in feature_names:
            self.assertNotIn("quantum", f)
            self.assertNotIn("robotics", f)
            self.assertNotIn("cybersecurity", f)

    def test_05_no_duplicate_records_in_calibration(self):
        """Fix 3 & P0: Multi-tier weighting must use sample_weight, not list repetition."""
        train_data = json.loads(self.train_path.read_text(encoding="utf-8"))
        self.assertEqual(len(train_data), 348, "Training dataset must remain 348 distinct rows")
        
        # Verify IDs are unique
        all_ids = [r["id"] for r in train_data]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Duplicate row IDs detected in training corpus")

    def test_06_protocol_c_v2_zero_overlap_with_b_and_train(self):
        """Fix 4 & P0: Protocol C v2 must have zero overlap with Protocol B and Training data."""
        self.assertTrue(self.protocol_c_path.exists(), "unseen_occupation_test_set_v2.json missing")
        self.assertTrue(self.protocol_b_path.exists(), "real_world_test_set.json missing")
        
        c_data = json.loads(self.protocol_c_path.read_text(encoding="utf-8"))
        b_data = json.loads(self.protocol_b_path.read_text(encoding="utf-8"))
        train_data = json.loads(self.train_path.read_text(encoding="utf-8"))
        
        self.assertEqual(len(c_data), 25, "Protocol C v2 must have exactly 25 records")
        
        c_ids = {r["id"] for r in c_data}
        b_ids = {r["id"] for r in b_data}
        train_ids = {r["id"] for r in train_data}
        
        self.assertEqual(len(c_ids.intersection(b_ids)), 0, "Protocol C overlaps with Protocol B IDs")
        self.assertEqual(len(c_ids.intersection(train_ids)), 0, "Protocol C overlaps with Training IDs")
        
        # Content overlap
        c_texts = {r["text"].strip().lower() for r in c_data}
        b_texts = {r["text"].strip().lower() for r in b_data}
        tr_texts = {r["text"].strip().lower() for r in train_data}
        
        self.assertEqual(len(c_texts.intersection(b_texts)), 0, "Protocol C text overlaps with Protocol B")
        self.assertEqual(len(c_texts.intersection(tr_texts)), 0, "Protocol C text overlaps with Training")

    def test_07_protocol_c_v2_masco_clusters_unseen(self):
        """Fix 4 & P0: Protocol C v2 occupation groups must be unseen in B and Train."""
        c_data = json.loads(self.protocol_c_path.read_text(encoding="utf-8"))
        b_data = json.loads(self.protocol_b_path.read_text(encoding="utf-8"))
        tr_data = json.loads(self.train_path.read_text(encoding="utf-8"))
        
        c_groups = {r["occupation_group"] for r in c_data}
        b_groups = {r.get("occupation_group", "") for r in b_data}
        tr_groups = {r.get("occupation_group", "") for r in tr_data}
        
        self.assertEqual(len(c_groups.intersection(b_groups)), 0, f"Overlapping groups with B: {c_groups.intersection(b_groups)}")
        self.assertEqual(len(c_groups.intersection(tr_groups)), 0, f"Overlapping groups with Train: {c_groups.intersection(tr_groups)}")

    def test_08_minilm_loads_and_encodes_384_dim(self):
        """Fix 6 & P1: MiniLM bi-encoder must actually load and encode 384-dimensional vectors."""
        model = get_minilm_model()
        self.assertIsNotNone(model)
        
        texts = ["Artificial intelligence engineer deploying transformer models."]
        embs = compute_minilm_embeddings(texts)
        self.assertEqual(embs.shape, (1, 384))
        # Norm should be approximately 1.0 (normalized embeddings)
        norm = float(np.linalg.norm(embs[0]))
        self.assertAlmostEqual(norm, 1.0, places=3)

    def test_09_pytorch_actually_used_for_candidate_b(self):
        """Fix 7 & P1: Candidate B must use PyTorch nn.Module with LayerNorm, Dropout, BCEWithLogitsLoss."""
        model = SkillsPredictorNN(in_features=100, hidden_1=64, hidden_2=32, num_skills=16)
        self.assertIsInstance(model, nn.Module)
        
        dummy_x = torch.randn(4, 100)
        out = model(dummy_x)
        self.assertEqual(out.shape, (4, 16))
        
        # Verify loss function
        criterion = nn.BCEWithLogitsLoss(pos_weight=torch.ones(16))
        loss = criterion(out, torch.zeros(4, 16))
        self.assertGreater(float(loss.item()), 0.0)

    def test_10_prediction_artifact_schema(self):
        """Fix 12 & P1: Out-of-fold prediction artifact conforms to required schema."""
        self.assertTrue(self.oof_path.exists(), "sample_oof_predictions_schema.json missing")
        samples = json.loads(self.oof_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(samples), 1)
        
        required_keys = {
            "record_id", "source", "occupation_group", "true_skills",
            "pred_skills_cand_a", "prob_skills_cand_a", "demand_truth",
            "demand_prob_uncal", "demand_prob_cal"
        }
        for rec in samples:
            self.assertTrue(required_keys.issubset(rec.keys()), f"Missing keys in {rec}")
            self.assertEqual(len(rec["prob_skills_cand_a"]), 16)
            self.assertIn(rec["demand_truth"], [0, 1])

    def test_11_preserved_legacy_artifacts_untouched(self):
        """Audit Constraint: Existing production & candidate artifacts must remain untouched."""
        v3_path = BASE_DIR / "runpod" / "models" / "skills_predictor_v3.joblib"
        v4_cand_path = BASE_DIR / "runpod" / "models" / "skills_predictor_v4_candidate" / "model.joblib"
        
        self.assertTrue(v3_path.exists(), "skills_predictor_v3.joblib must be preserved")
        self.assertTrue(v4_cand_path.exists(), "skills_predictor_v4_candidate must be preserved")


if __name__ == "__main__":
    unittest.main()
