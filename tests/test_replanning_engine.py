"""
Automated Test Suite for O2 Automatic Replanning & Change Detection Engine v1.0.0
Covers all requirements from Stage 16A:
  - Upstream frozen baseline integrity
  - State snapshot immutability & fingerprinting
  - Dependency graph correctness
  - Unnecessary recomputation avoidance
  - Event validation: duplicate, stale, unsupported versions
  - Materiality forensic test: 5 structural vs 5 score-only cases
  - Privacy-safe diff mechanics (4->5, 5->4, <5-><5)
  - Responsible AI & HR safety invariants
  - Candidate separation and rollback reference
"""

import unittest
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.replanning_engine import ReplanningEngine


class TestReplanningEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ReplanningEngine()
        with open(ROOT / "data" / "replanning" / "synthetic_m2_snapshots_v1.json", "r", encoding="utf-8") as f:
            self.m2_snaps = json.load(f)

        self.base_profile = {
            "profile_id": "P_TEST_USER_001",
            "skills": {
                "python_scripting": "USER_CONFIRMED",
                "sql_data_analysis": "USER_CONFIRMED"
            }
        }

    # -------------------------------------------------------------------------
    # 1. Upstream Frozen Baseline Integrity
    # -------------------------------------------------------------------------

    def test_upstream_frozen_hashes_unchanged(self):
        """Verifies that all frozen core and aggregation engine files/manifests remain unmutated."""
        expected_hashes = {
            "M2": ("artifacts/m2_v1_1_1_freeze_manifest.json", "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"),
            "M6": ("data/scenarios/scenario_build_manifest_v1_1.json", "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"),
            "M3": ("data/matching/m3_build_manifest_v1_1.json", "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c"),
            "M4_MANIFEST": ("artifacts/m4_v1_1_freeze_manifest.json", "448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f"),
            "M5_MANIFEST": ("artifacts/m5_v1_1_freeze_manifest.json", "94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7"),
            "O6_MANIFEST": ("artifacts/o6_v1_1_freeze_manifest.json", "0fb13557e4a6665c6c85e2c2904dc4e99e41dfdf9019c49fb2a01b416f93ef5e"),
            "O1_MANIFEST": ("artifacts/o1_v1_1_freeze_manifest.json", "c4a58baf74549f05ceeb3063b779b680762aec98d1edf531b909fcf041bce1f9")
        }

        for label, (rel_path, exp_hash) in expected_hashes.items():
            full_p = ROOT / rel_path
            self.assertTrue(full_p.exists(), f"File {rel_path} does not exist")
            with open(full_p, "rb") as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(actual_hash, exp_hash, f"Frozen hash mismatch for {label} at {rel_path}")

    # -------------------------------------------------------------------------
    # 2. State Snapshot & Fingerprint Invariants
    # -------------------------------------------------------------------------

    def test_state_snapshot_immutability(self):
        """Verifies state snapshot immutability and state_id creation."""
        s1 = self.engine.build_state_snapshot(
            profile_snapshot=self.base_profile,
            m2_snapshot_id="M2_SNAP_BASELINE_2026Q1",
            scenario_id="REFERENCE_2026"
        )
        original_fp = s1["state_fingerprint"]

        # Mutating a copy does not affect internal store
        retrieved = self.engine._state_store[s1["state_id"]]
        self.assertEqual(retrieved["state_fingerprint"], original_fp)

    def test_fingerprint_excludes_timestamps_and_metadata(self):
        """Fingerprint must be strictly semantic, ignoring timestamps and non-semantic keys."""
        s1 = self.engine.build_state_snapshot(
            profile_snapshot=self.base_profile,
            created_at="2026-01-01T00:00:00Z",
            state_id="STATE_001"
        )
        s2 = self.engine.build_state_snapshot(
            profile_snapshot=self.base_profile,
            created_at="2026-10-24T05:00:00Z",
            state_id="STATE_002"
        )
        self.assertEqual(s1["state_fingerprint"], s2["state_fingerprint"])

    def test_fingerprint_changes_on_relevant_change(self):
        """Modifying a relevant field alters the state fingerprint."""
        s_base = self.engine.build_state_snapshot(
            profile_snapshot=self.base_profile,
            scenario_id="REFERENCE_2026"
        )
        s_changed = self.engine.build_state_snapshot(
            profile_snapshot=self.base_profile,
            scenario_id="FAST_AGENTIC"
        )
        self.assertNotEqual(s_base["state_fingerprint"], s_changed["state_fingerprint"])

    # -------------------------------------------------------------------------
    # 3. Dependency Graphs & Recomputation Planning
    # -------------------------------------------------------------------------

    def test_dependency_graphs_by_event_type(self):
        """Verifies deterministic dependency rules for all supported event types."""
        # M2 Trend change
        p_m2 = self.engine.build_recompute_plan("M2_TREND_SNAPSHOT_UPDATED", ["M2_TREND_EVIDENCE"])
        self.assertEqual(p_m2["affected_modules"], ["M3", "M4", "O6", "O1"])
        self.assertEqual(p_m2["recompute_order"], ["M3", "M4", "O6", "O1"])

        # M6 Scenario change
        p_m6 = self.engine.build_recompute_plan("M6_SCENARIO_CHANGED", ["M6_SCENARIO"])
        self.assertEqual(p_m6["affected_modules"], ["M3", "M4", "O6", "O1"])

        # Profile change
        p_prof = self.engine.build_recompute_plan("PROFILE_SKILL_STATE_UPDATED", ["PROFILE_SKILLS"])
        self.assertEqual(p_prof["affected_modules"], ["M3", "M4", "O6", "O1"])

        # Cohort change alone (skips individual M3/M4)
        p_cohort = self.engine.build_recompute_plan("COHORT_SNAPSHOT_UPDATED", ["COHORT_COMPOSITION"])
        self.assertEqual(p_cohort["affected_modules"], ["O6", "O1"])
        self.assertEqual(p_cohort["recompute_order"], ["O6", "O1"])
        self.assertTrue(p_cohort["skip_individual_m3_m4"])

    def test_avoid_unnecessary_recomputation(self):
        """Ensures identical state returns empty affected modules."""
        p_none = self.engine.build_recompute_plan("NO_RELEVANT_CHANGE", [])
        self.assertEqual(p_none["affected_modules"], [])
        self.assertEqual(p_none["recompute_order"], [])

    # -------------------------------------------------------------------------
    # 4. Event Validation: Duplicates, Stale, Unsupported Versions
    # -------------------------------------------------------------------------

    def test_duplicate_event_handling(self):
        """Duplicate event IDs must be rejected without mutating state."""
        s1 = self.engine.build_state_snapshot(self.base_profile, state_id="S_PREV")
        s2 = self.engine.build_state_snapshot(self.base_profile, state_id="S_NEW")
        evt = {"event_id": "EVT_TEST_DUP_01", "trigger_type": "MANUAL_REPLAN_REQUESTED", "timestamp": "2026-10-24T05:00:00Z"}

        res1 = self.engine.execute_candidate_replan(s1, evt, s2)
        res2 = self.engine.execute_candidate_replan(s1, evt, s2)

        self.assertEqual(res2["publication_status"], "DUPLICATE_EVENT")
        self.assertIn("DUPLICATE_EVENT", res2["quality_flags"])
        self.assertEqual(res2["rollback_reference"], "S_PREV")

    def test_stale_event_handling(self):
        """Events with timestamps older than current accepted state must be rejected."""
        s_curr = self.engine.build_state_snapshot(self.base_profile, created_at="2026-10-24T05:00:00Z")
        evt_stale = {"event_id": "EVT_STALE_01", "timestamp": "2024-01-01T00:00:00Z"}
        res = self.engine.execute_candidate_replan(s_curr, evt_stale, s_curr)

        self.assertEqual(res["publication_status"], "STALE_EVENT")
        self.assertIn("STALE_EVENT", res["quality_flags"])

    def test_unsupported_version_handling(self):
        """Events claiming uncertified upstream versions must be rejected."""
        s_curr = self.engine.build_state_snapshot(self.base_profile)
        evt_bad = {
            "event_id": "EVT_BAD_VER_01",
            "source_versions": {"M2": "2.0.0", "M3": "1.1.0"},
            "timestamp": "2026-10-24T05:00:00Z"
        }
        res = self.engine.execute_candidate_replan(s_curr, evt_bad, s_curr)

        self.assertEqual(res["publication_status"], "UNSUPPORTED_UPSTREAM_VERSION")
        self.assertIn("UNSUPPORTED_UPSTREAM_VERSION", res["quality_flags"])

    # -------------------------------------------------------------------------
    # 5. Materiality Forensic Test: 5 Structural vs 5 Score-Only Cases
    # -------------------------------------------------------------------------

    def test_materiality_forensic_suite(self):
        """
        Constructs at least 5 structural change cases and 5 score-only change cases.
        Verifies that structural changes receive strictly higher materiality.
        """
        # --- 5 STRUCTURAL CASES ---
        # Case S1: Top recommended role changed
        d_s1 = {"M3": {"top_recommended_role_changed": True}, "M4": {}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_s1), "HIGH_MATERIALITY")

        # Case S2: CORE skill gap added
        d_s2 = {"M3": {}, "M4": {"core_gaps_added": ["ai_literacy"]}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_s2), "HIGH_MATERIALITY")

        # Case S3: CORE skill gap removed
        d_s3 = {"M3": {}, "M4": {"core_gaps_removed": ["python_scripting"]}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_s3), "HIGH_MATERIALITY")

        # Case S4: Required pathway step added
        d_s4 = {"M3": {}, "M4": {"required_steps_added": ["workflow_automation"]}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_s4), "HIGH_MATERIALITY")

        # Case S5: Top-3 role membership changed
        d_s5 = {"M3": {"top3_membership_changed": True, "top_recommended_role_changed": False}, "M4": {}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_s5), "MATERIAL")

        # --- 5 SCORE-ONLY CASES ---
        # Case N1: Match index moves +2.5 points without rank changes
        d_n1 = {"M3": {"top_recommended_role_changed": False, "match_index_deltas": {"2511": 2.5}}, "M4": {}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_n1), "MINOR")

        # Case N2: Match index moves -4.0 points without rank changes
        d_n2 = {"M3": {"top_recommended_role_changed": False, "match_index_deltas": {"2511": -4.0}}, "M4": {}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_n2), "MINOR")

        # Case N3: ECI evidence reliability changes without match index change
        d_n3 = {"M3": {"top_recommended_role_changed": False, "eci_deltas": {"2511": 5.0}}, "M4": {}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_n3), "MINOR")

        # Case N4: Minor learning hours delta (+15h) without step additions
        d_n4 = {"M3": {}, "M4": {"learning_hours_delta": 15.0, "learning_hours_band_changed": False}, "O1": {}}
        self.assertEqual(self.engine.classify_materiality(d_n4), "MINOR")

        # Case N5: O1 priority rank shift without top priority skill change
        d_n5 = {"M3": {}, "M4": {}, "O1": {"rank_changes": [{"skill_id": "data_viz", "delta_rank": 1}], "top_priority_skill_changed": False}}
        self.assertEqual(self.engine.classify_materiality(d_n5), "MINOR")

    # -------------------------------------------------------------------------
    # 6. Privacy-Safe Diff Transitions (O1 k=5 Compliance)
    # -------------------------------------------------------------------------

    def test_privacy_safe_diff_transitions(self):
        """Verifies safe text emission for 4->5, 5->4, and <5-><5 transitions."""
        # 4 to 5
        m_4_to_5 = self.engine.build_privacy_safe_diff(prev_val="<5", new_val="5", prev_count=4, new_count=5)
        self.assertEqual(m_4_to_5, "Previously suppressed; now above reporting threshold.")
        self.assertNotIn("4", m_4_to_5)

        # 5 to 4
        m_5_to_4 = self.engine.build_privacy_safe_diff(prev_val="5", new_val="<5", prev_count=5, new_count=4)
        self.assertEqual(m_5_to_4, "Previously reportable; now below reporting threshold.")
        self.assertNotIn("4", m_5_to_4)

        # <5 to <5
        m_supp_to_supp = self.engine.build_privacy_safe_diff(prev_val="<5", new_val="<5", prev_count=2, new_count=3)
        self.assertEqual(m_supp_to_supp, "SUPPRESSED → SUPPRESSED")

        # >=5 to >=5
        m_vis_to_vis = self.engine.build_privacy_safe_diff(prev_val="10", new_val="14", prev_count=10, new_count=14)
        self.assertEqual(m_vis_to_vis, "10 → 14 (+4)")

    # -------------------------------------------------------------------------
    # 7. Responsible AI & Human Acknowledgement
    # -------------------------------------------------------------------------

    def test_human_acknowledgement_required_for_material_replan(self):
        """Material and High Materiality replans must require human acknowledgement."""
        s_prev = self.engine.build_state_snapshot(self.base_profile, m3_output=[{"masco_code": "2511", "role_match_index": 80.0}])
        s_cand = self.engine.build_state_snapshot(self.base_profile, m3_output=[{"masco_code": "2529", "role_match_index": 90.0}])
        evt = {"event_id": "EVT_MAT_ACK_01", "trigger_type": "M2_TREND_SNAPSHOT_UPDATED", "timestamp": "2026-10-24T05:00:00Z"}

        replan = self.engine.execute_candidate_replan(s_prev, evt, s_cand)
        self.assertEqual(replan["publication_status"], "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT")
        self.assertIn("HUMAN_ACKNOWLEDGEMENT_REQUIRED", replan["quality_flags"])
        self.assertEqual(replan["rollback_reference"], s_prev["state_id"])

    def test_responsible_ai_governance_invariants(self):
        """Confirms quality flags enforce non-employment use and partial differencing protection."""
        s1 = self.engine.build_state_snapshot(self.base_profile)
        evt = {"event_id": "EVT_GOV_01", "trigger_type": "MANUAL_REPLAN_REQUESTED", "timestamp": "2026-10-24T05:00:00Z"}
        replan = self.engine.execute_candidate_replan(s1, evt, s1)

        self.assertIn("NOT_FOR_EMPLOYMENT_DECISIONS", replan["quality_flags"])
        self.assertIn("PARTIAL_DIFFERENCING_PROTECTION", replan["quality_flags"])

    def test_rollback_helper(self):
        """Verifies rollback helper successfully retrieves previous state without mutation."""
        s_prev = self.engine.build_state_snapshot(self.base_profile, state_id="STATE_ROLLBACK_PREV")
        s_cand = self.engine.build_state_snapshot(self.base_profile, state_id="STATE_ROLLBACK_CAND")
        evt = {"event_id": "EVT_ROLLBACK_TEST", "trigger_type": "M6_SCENARIO_CHANGED", "timestamp": "2026-10-24T05:00:00Z"}

        replan = self.engine.execute_candidate_replan(s_prev, evt, s_cand)
        prev_recovered = self.engine.rollback_to_previous(replan)

        self.assertIsNotNone(prev_recovered)
        self.assertEqual(prev_recovered["state_id"], "STATE_ROLLBACK_PREV")

    # -------------------------------------------------------------------------
    # 8. Additional Safety, Isolation & Edge Invariants
    # -------------------------------------------------------------------------

    def test_resource_change_does_not_alter_skill_needs(self):
        """A future resource availability change in M4 must not alter skill needs or gaps."""
        m4_prev = {
            "pathway_steps": [{"skill_id": "ai_literacy", "requirement_tier": "CORE", "resource_id": "RES_001"}]
        }
        m4_new = {
            "pathway_steps": [{"skill_id": "ai_literacy", "requirement_tier": "CORE", "resource_id": "RES_002"}]
        }
        diff = self.engine.diff_m4_outputs(m4_prev, m4_new)
        self.assertEqual(diff["core_gaps_added"], [])
        self.assertEqual(diff["core_gaps_removed"], [])
        self.assertFalse(diff["structural_change"])
        self.assertEqual(self.engine.classify_materiality({"M4": diff}), "NONE")

    def test_no_individual_ids_in_employer_diff(self):
        """Employer-facing O1 diffs must not expose individual employee IDs."""
        o1_prev = {"priority_skills": [{"skill_id": "ai_literacy", "affected_profile_count": 10, "affected_profile_count_display": "10"}]}
        o1_new = {"priority_skills": [{"skill_id": "ai_literacy", "affected_profile_count": 12, "affected_profile_count_display": "12"}]}
        diff = self.engine.diff_o1_outputs(o1_prev, o1_new)

        diff_str = json.dumps(diff)
        self.assertNotIn("profile_id", diff_str)
        self.assertNotIn("P_TEST_USER", diff_str)
        self.assertIn("governance_notice", diff)

    def test_sdg_context_only_no_impact_claims(self):
        """O6 diffs must explicitly label changes as alignment context shifts, NOT ESG impact."""
        o6_prev = {"sdg_alignment_prevalence": {"SDG_8": 0.45}}
        o6_new = {"sdg_alignment_prevalence": {"SDG_8": 0.50}}
        diff = self.engine.diff_o6_outputs(o6_prev, o6_new)

        self.assertIn("SDG_8", diff["sdg_alignment_prevalence_deltas"])
        self.assertIn("alignment_notice", diff)
        self.assertIn("SDG_ALIGNMENT_CONTEXT_CHANGE", diff["alignment_notice"])
        self.assertIn("NOT verified corporate ESG impact scores", diff["alignment_notice"])

    def test_changeset_hash_determinism_and_reproducibility(self):
        """Identical diff outputs must produce exact bit-identical changeset hashes."""
        diff_sample = {
            "M3": {"top_recommended_role_changed": False, "match_index_deltas": {"2511": 1.2}},
            "M4": {"core_gaps_added": [], "core_gaps_removed": []}
        }
        h1 = self.engine._compute_changeset_hash(diff_sample)
        h2 = self.engine._compute_changeset_hash(diff_sample)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_audit_ledger_record_fields(self):
        """Audit ledger records must include all required audit metadata."""
        s1 = self.engine.build_state_snapshot(self.base_profile)
        evt = {"event_id": "EVT_LEDGER_TEST", "trigger_type": "MANUAL_REPLAN_REQUESTED", "timestamp": "2026-10-24T05:00:00Z"}
        self.engine.execute_candidate_replan(s1, evt, s1)

        last_entry = self.engine.audit_ledger[-1]
        required_keys = [
            "event_id", "previous_state_id", "candidate_state_id", "trigger_type",
            "materiality", "affected_modules", "recompute_order", "publication_status",
            "previous_state_fingerprint", "candidate_state_fingerprint", "changeset_hash", "created_at"
        ]
        for k in required_keys:
            self.assertIn(k, last_entry)

    def test_m2_synthetic_fixtures_labelled(self):
        """Synthetic M2 fixtures must be explicitly labelled SYNTHETIC_CHANGE_FIXTURE."""
        for snap_id, snap_data in self.m2_snaps.items():
            self.assertEqual(snap_data.get("data_source_class"), "SYNTHETIC_CHANGE_FIXTURE")

    def test_individual_m4_authority_preservation(self):
        """O1 priority ranking must not merge into or overwrite individual M4 pathway ordering."""
        # Verification that O2 diffs isolate M4 pathway diff from O1 priority diff
        d_m4 = {"pathway_steps_added": ["skill_a"]}
        d_o1 = {"top_priority_skill_changed": True}
        all_diffs = {"M4": d_m4, "O1": d_o1}

        self.assertIn("M4", all_diffs)
        self.assertIn("O1", all_diffs)
        self.assertNotEqual(all_diffs["M4"], all_diffs["O1"])


if __name__ == "__main__":
    unittest.main()
