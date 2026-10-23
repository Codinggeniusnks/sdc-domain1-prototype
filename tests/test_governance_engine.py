"""
Unit Tests for O5 Responsible-AI & Invariance Governance Audit Layer
Module: tests/test_governance_engine.py
"""

import unittest
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.governance_engine import GovernanceEngine


class TestGovernanceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = GovernanceEngine()

    def test_01_proxy_exclusion_clean(self):
        """Verifies clean skill/workforce data passes proxy scan."""
        clean_profile = {
            "profile_id": "SYNTH_001",
            "confirmed_skills": ["python", "sql", "git"],
            "target_role": "2512",
            "weekly_hours_available": 6
        }
        is_clean, violations = self.engine.audit_proxy_field_exclusion(clean_profile)
        self.assertTrue(is_clean)
        self.assertEqual(len(violations), 0)

    def test_02_proxy_exclusion_catches_demographics(self):
        """Detects illegal demographic proxy fields."""
        dirty_profile = {
            "profile_id": "SYNTH_002",
            "confirmed_skills": ["python"],
            "gender": "Female",
            "age": 32,
            "ethnicity": "Malay"
        }
        is_clean, violations = self.engine.audit_proxy_field_exclusion(dirty_profile)
        self.assertFalse(is_clean)
        self.assertEqual(len(violations), 3)

    def test_03_counterfactual_invariance_clean(self):
        """Verifies demographic perturbation produces 0.0 variance in sanitized pipeline."""
        base = {"skills": ["python", "sql"], "target": "2512"}
        perturbed = {"skills": ["python", "sql"], "target": "2512", "gender": "Male", "age": 45}

        # Simulated pipeline that only reads 'skills' and 'target'
        def mock_pipeline(p):
            return {
                "score": round(len(p.get("skills", [])) * 45.0, 2),
                "target": p.get("target")
            }

        passed, details = self.engine.run_counterfactual_invariance_test(base, perturbed, mock_pipeline)
        self.assertTrue(passed)
        self.assertEqual(details["violations_count"], 0)

    def test_04_counterfactual_invariance_detects_bias(self):
        """Catches biased pipeline that modifies scores based on demographics."""
        base = {"skills": ["python"], "target": "2512"}
        perturbed = {"skills": ["python"], "target": "2512", "age": 55}

        # Biased pipeline that penalizes age
        def biased_pipeline(p):
            penalty = 10.0 if p.get("age", 0) > 50 else 0.0
            return {"score": 80.0 - penalty}

        passed, details = self.engine.run_counterfactual_invariance_test(base, perturbed, biased_pipeline)
        self.assertFalse(passed)
        self.assertGreater(details["violations_count"], 0)

    def test_05_small_cell_privacy_clean(self):
        """Verifies properly suppressed small cells pass audit."""
        safe_payload = {
            "cell_a": {"profiles_count": 12, "suppressed": False},
            "cell_b": {"profiles_count": None, "display": "<5", "suppressed": True}
        }
        is_safe, violations = self.engine.verify_small_cell_privacy(safe_payload, min_k=5)
        self.assertTrue(is_safe)
        self.assertEqual(len(violations), 0)

    def test_06_small_cell_privacy_catches_leak(self):
        """Catches unsuppressed count < 5 in aggregate tables."""
        leaky_payload = {
            "cell_a": {"profiles_count": 12},
            "cell_b": {"profiles_count": 3}  # Leaked small cell!
        }
        is_safe, violations = self.engine.verify_small_cell_privacy(leaky_payload, min_k=5)
        self.assertFalse(is_safe)
        self.assertTrue(any("Small-cell count 3" in v for v in violations))

    def test_07_freeze_integrity_verification(self):
        """Verifies on-disk presence and cryptographic integrity of upstream manifests."""
        all_ok, report = self.engine.verify_freeze_integrity()
        self.assertTrue(all_ok, f"Freeze integrity failed: {report}")
        self.assertGreaterEqual(report["modules_checked"], 9)

    def test_08_audit_ledger_generation(self):
        """Verifies structure and completeness of comprehensive audit ledger."""
        ledger = self.engine.generate_comprehensive_audit_ledger()
        self.assertEqual(ledger["audit_ledger_version"], "v1.0.0")
        self.assertEqual(ledger["overall_governance_verdict"], "APPROVED_RESPONSIBLE_AI_COMPLIANT")
        self.assertIn("compliance_attestation", ledger)
        self.assertIn("freeze_integrity_verification", ledger)


if __name__ == "__main__":
    unittest.main()
