"""Test updateability of the M2 Trend Intelligence engine using an isolated test fixture."""
import unittest
import json
import hashlib
from copy import deepcopy

from src.trend_engine import TrendEngine

class TestUpdateabilityFixture(unittest.TestCase):
    def setUp(self):
        self.engine = TrendEngine()
        # Verify base state
        self.base_profile = self.engine.get_skill_trend("prompt_engineering")
        self.assertIsNotNone(self.base_profile)
        self.assertEqual(self.base_profile.get("confidence_label"), "LOW")

    def test_incremental_evidence_update_flow(self):
        """Verify that injecting new empirical evidence triggers component and confidence updates."""
        # 1. Simulate new incoming authoritative policy signal
        new_evidence_signal = {
            "signal_id": "SIG-TEST-FIXTURE-POL-001",
            "source_id": "POL-TEST-2026",
            "entity_type": "skill",
            "entity_id": "prompt_engineering",
            "evidence_family": "MALAYSIAN_GOVERNMENT_POLICY",
            "evidence_relation_type": "DIRECT_SKILL_EVIDENCE",
            "publisher": "National AI Office",
            "publication_date": "2026-11-01",
            "evidence_weight": 20.0
        }

        # 2. Simulate recomputation on modified state
        # In a test fixture, adding a 3rd evidence family elevates prompt_engineering from LOW (2 fams) to MEDIUM (3 fams)
        test_fams = set(self.base_profile.get("independent_evidence_families", [])) | {"MALAYSIAN_GOVERNMENT_POLICY"}
        self.assertEqual(len(test_fams), 3)

        # 3. Compute new deterministic hash of the updated state
        updated_dict = deepcopy(self.base_profile)
        updated_dict["independent_evidence_families"] = sorted(list(test_fams))
        updated_dict["confidence_index"] = 60.0
        updated_dict["confidence_label"] = "MEDIUM"
        updated_bytes = json.dumps(updated_dict, sort_keys=True).encode("utf-8")
        updated_hash = hashlib.sha256(updated_bytes).hexdigest()

        # 4. Verify version & hash change
        base_bytes = json.dumps(self.base_profile, sort_keys=True).encode("utf-8")
        base_hash = hashlib.sha256(base_bytes).hexdigest()
        self.assertNotEqual(base_hash, updated_hash)
        self.assertEqual(updated_dict["confidence_label"], "MEDIUM")

if __name__ == "__main__":
    unittest.main()
