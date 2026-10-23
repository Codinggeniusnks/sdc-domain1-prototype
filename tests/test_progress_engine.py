"""
Unit Tests for O4 Learning Progress & Milestone Tracking Engine
Module: tests/test_progress_engine.py
"""

import unittest
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.progress_engine import ProgressEngine


class TestProgressEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ProgressEngine()
        self.sample_pathway = {
            "target_role": "2512",
            "milestones": [
                {"milestone_id": "M1", "title": "Programming Basics", "skills": ["python", "git"]},
                {"milestone_id": "M2", "title": "Data Structures", "skills": ["algorithms", "sql"]},
                {"milestone_id": "M3", "title": "Advanced Frameworks", "skills": ["fastapi", "docker"]}
            ]
        }

    def test_01_initialize_progress(self):
        """Verifies initial state is NOT_STARTED with 0% completion."""
        record = self.engine.initialize_progress("USER_001", self.sample_pathway)
        self.assertEqual(record["profile_id"], "USER_001")
        self.assertEqual(record["total_milestones"], 3)
        self.assertEqual(record["completed_milestones"], 0)
        self.assertEqual(record["overall_completion_pct"], 0.0)
        self.assertEqual(record["milestones_progress"]["M1"]["status"], "NOT_STARTED")
        self.assertIn("Official Notice", record["disclaimer"])

    def test_02_valid_state_transitions(self):
        """Verifies legal state transitions through the learning lifecycle."""
        record = self.engine.initialize_progress("USER_001", self.sample_pathway)
        
        # Step 1: Start M1
        rec1, ok1, _ = self.engine.update_milestone_progress(record, "M1", "IN_PROGRESS", 40.0)
        self.assertTrue(ok1)
        self.assertEqual(rec1["milestones_progress"]["M1"]["status"], "IN_PROGRESS")
        self.assertIn("FIRST_STEP_TAKEN", rec1["earned_badges"])

        # Step 2: Self-reported completion
        rec2, ok2, _ = self.engine.update_milestone_progress(rec1, "M1", "COMPLETED_SELF_REPORTED", 100.0)
        self.assertTrue(ok2)
        self.assertEqual(rec2["milestones_progress"]["M1"]["status"], "COMPLETED_SELF_REPORTED")

        # Step 3: Verified completion with credential
        evidence = {
            "credential_id": "MALAYSIA-MDEC-001",
            "issuer": "MDEC Digital Academy",
            "issue_date": "2026-05-10",
            "sha256": "a" * 64
        }
        rec3, ok3, _ = self.engine.update_milestone_progress(
            rec2, "M1", "COMPLETED_VERIFIED", 100.0, evidence=evidence, verified_skills=["python", "git"]
        )
        self.assertTrue(ok3)
        self.assertEqual(rec3["milestones_progress"]["M1"]["status"], "COMPLETED_VERIFIED")
        self.assertIn("VERIFIED_CREDENTIAL_EARNED", rec3["earned_badges"])
        self.assertIn("CORE_FOUNDATION_ACHIEVED", rec3["earned_badges"])

    def test_03_illegal_state_transition(self):
        """Rejects illegal jumps in state."""
        record = self.engine.initialize_progress("USER_001", self.sample_pathway)
        # Cannot jump from NOT_STARTED directly to COMPLETED_VERIFIED without starting or evidence
        rec, ok, msg = self.engine.update_milestone_progress(record, "M1", "COMPLETED_VERIFIED", 100.0)
        self.assertFalse(ok)
        self.assertIn("Illegal state transition", msg)

    def test_04_credential_verification_valid_and_invalid(self):
        """Verifies credential validation logic."""
        valid_ev = {
            "credential_id": "CERT-12345",
            "issuer": "HRD Corp Malaysia",
            "issue_date": "2026-01-15",
            "sha256": "1234567890abcdef" * 4
        }
        ok, _ = self.engine.verify_credential_evidence(valid_ev)
        self.assertTrue(ok)

        # Missing field
        bad_ev1 = {"credential_id": "CERT-12345"}
        ok1, msg1 = self.engine.verify_credential_evidence(bad_ev1)
        self.assertFalse(ok1)

        # Corrupt SHA-256 (not 64 hex chars)
        bad_ev2 = {"credential_id": "CERT-12345", "issuer": "HRD Corp", "issue_date": "2026-01-15", "sha256": "not-a-hash"}
        ok2, msg2 = self.engine.verify_credential_evidence(bad_ev2)
        self.assertFalse(ok2)

    def test_05_non_competitive_badges(self):
        """Verifies that earned badges contain zero peer ranking or competitive metrics."""
        record = self.engine.initialize_progress("USER_001", self.sample_pathway)
        badges = self.engine.evaluate_badges(record)
        self.assertIsInstance(badges, list)
        for b_name in badges:
            badge_def = self.engine.badge_registry.get(b_name, {})
            self.assertFalse(badge_def.get("is_competitive", False))
            self.assertNotIn("rank", str(badge_def).lower())
            self.assertNotIn("percentile", str(badge_def).lower())

    def test_06_verified_skills_delta_for_o2(self):
        """Verifies feedback loop payload structure for O2 replanning."""
        record = self.engine.initialize_progress("USER_001", self.sample_pathway)
        evidence = {
            "credential_id": "MALAYSIA-001",
            "issuer": "National Digital Academy",
            "issue_date": "2026-06-01",
            "sha256": "b" * 64
        }
        rec, _, _ = self.engine.update_milestone_progress(
            record, "M1", "IN_PROGRESS", 50.0
        )
        rec2, _, _ = self.engine.update_milestone_progress(
            rec, "M1", "COMPLETED_VERIFIED", 100.0, evidence=evidence, verified_skills=["python", "git"]
        )
        delta = self.engine.generate_verified_skills_delta(rec2)
        self.assertEqual(delta["profile_id"], "USER_001")
        self.assertEqual(delta["verified_skills_count"], 2)
        self.assertEqual(delta["verified_skills"], ["git", "python"])
        self.assertTrue(delta["trigger_replan_event"])

    def test_07_cohort_aggregation_privacy_k5(self):
        """Verifies small-cell masking in employer cohort progress view."""
        # 10 synthetic learners
        cohort = []
        for i in range(10):
            rec = self.engine.initialize_progress(f"USER_{i:03d}", self.sample_pathway)
            # 6 learners completed M1, only 3 learners completed M2
            if i < 6:
                rec["milestones_progress"]["M1"]["completion_pct"] = 100.0
            if i < 3:
                rec["milestones_progress"]["M2"]["completion_pct"] = 100.0
            cohort.append(rec)

        agg = self.engine.aggregate_cohort_progress(cohort, min_k=5)
        self.assertEqual(agg["cohort_size"], 10)
        self.assertEqual(agg["privacy_status"], "K_ANONYMITY_5_ACTIVE")

        # M1 has 6 completions (>= 5): reportable
        self.assertFalse(agg["milestone_completion_rates"]["M1"]["suppressed"])
        self.assertEqual(agg["milestone_completion_rates"]["M1"]["completed_count"], 6)

        # M2 has 3 completions (< 5): suppressed
        self.assertTrue(agg["milestone_completion_rates"]["M2"]["suppressed"])
        self.assertIsNone(agg["milestone_completion_rates"]["M2"]["completed_count"])
        self.assertEqual(agg["milestone_completion_rates"]["M2"]["completed_count_display"], "<5")

    def test_08_small_cohort_total_suppression(self):
        """Verifies entire cohort suppressed if total learners < 5."""
        cohort = [self.engine.initialize_progress(f"USER_{i:03d}", self.sample_pathway) for i in range(4)]
        agg = self.engine.aggregate_cohort_progress(cohort, min_k=5)
        self.assertEqual(agg["cohort_size_display"], "<5")
        self.assertEqual(agg["privacy_status"], "SUPPRESSED_SMALL_COHORT")
        self.assertIsNone(agg["cohort_size"])


if __name__ == "__main__":
    unittest.main()
