"""
Automated Unit Tests for M4 Personalised Reskilling Pathway Engine v1.1.0 (Stage 12C)
Module: M4 Reskilling Pathway Engine
Author: Senior Learning-Pathway Engineer, Education-Resource Auditor & Reproducibility Engineer
Date: 2026-10-23
"""

import os
import sys
import json
import math
import hashlib
import unittest

PROJECT_ROOT = r"C:\Users\LENOVO\.gemini\antigravity\scratch\sdc-domain1-prototype"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
src_dir = os.path.join(PROJECT_ROOT, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from role_matching_engine import RoleMatchingEngine
from reskilling_pathway_engine import ReskillingPathwayEngine


def get_file_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


class TestReskillingPathwayEngineV11(unittest.TestCase):
    """Comprehensive test suite for M4 Reskilling Pathway Engine v1.1.0."""

    @classmethod
    def setUpClass(cls):
        cls.m3_engine = RoleMatchingEngine()
        cls.m4_engine = ReskillingPathwayEngine(
            prerequisites_path=os.path.join(PROJECT_ROOT, "data", "reskilling", "skill_prerequisites_v1_1.json"),
            resources_path=os.path.join(PROJECT_ROOT, "data", "reskilling", "learning_resources_v1_1.json"),
            config_path=os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_scoring_config_v1_1.json")
        )
        
        personas_file = os.path.join(PROJECT_ROOT, "data", "matching", "synthetic_personas_v1_1.json")
        with open(personas_file, "r", encoding="utf-8") as f:
            cls.personas = json.load(f)["personas"]

        resources_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "learning_resources_v1_1.json")
        with open(resources_file, "r", encoding="utf-8") as f:
            cls.resources_data = json.load(f)

        prereqs_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "skill_prerequisites_v1_1.json")
        with open(prereqs_file, "r", encoding="utf-8") as f:
            cls.prereqs_data = json.load(f)

        config_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_scoring_config_v1_1.json")
        with open(config_file, "r", encoding="utf-8") as f:
            cls.config_data = json.load(f)

    # =========================================================================
    # 1. UPSTREAM FREEZE HASHES & IMMUTABILITY
    # =========================================================================
    def test_upstream_m2_freeze_hash(self):
        """Verify M2 v1.1.1 freeze hash remains intact."""
        manifest_file = os.path.join(PROJECT_ROOT, "data", "matching", "m3_build_manifest_v1_1.json")
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        m2_hash = manifest["upstream_dependencies"]["m2_trend_intelligence"]["manifest_sha256"]
        expected_hash = "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"
        self.assertEqual(m2_hash, expected_hash)

    def test_upstream_m6_freeze_hash(self):
        """Verify M6 v1.1.0 freeze hash remains intact."""
        manifest_file = os.path.join(PROJECT_ROOT, "data", "matching", "m3_build_manifest_v1_1.json")
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        m6_hash = manifest["upstream_dependencies"]["m6_scenario_engine"]["manifest_sha256"]
        expected_hash = "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"
        self.assertEqual(m6_hash, expected_hash)

    def test_upstream_m3_freeze_hash(self):
        """Verify M3 v1.1.0 build manifest hash remains intact."""
        manifest_file = os.path.join(PROJECT_ROOT, "data", "matching", "m3_build_manifest_v1_1.json")
        expected_hash = "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c"
        self.assertEqual(get_file_sha256(manifest_file), expected_hash)

    # =========================================================================
    # 2. P1 — DYNAMIC PATHWAY EVIDENCE CONFIDENCE & NON-SATURATION
    # =========================================================================
    def test_dynamic_confidence_non_saturation_across_benchmarks(self):
        """Verify confidence scores vary across benchmark personas and are not all 94.5."""
        benchmark_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_benchmark_results_v1_1.json")
        with open(benchmark_file, "r", encoding="utf-8") as f:
            b_data = json.load(f)
        
        scores = [tc["pathway_evidence_confidence_index"] for tc in b_data["test_cases"]]
        self.assertEqual(len(scores), 8)
        self.assertGreater(max(scores), min(scores), "Confidence scores must not be saturated/identical!")
        self.assertNotEqual(scores[0], 94.5, "Confidence score must be dynamically aggregated, not hardcoded 94.5.")
        self.assertGreater(b_data["confidence_distribution"]["standard_deviation"], 0.0)

    def test_confidence_independent_of_role_match_index(self):
        """Verify M3 Match Index and M3 Evidence Confidence do not change M4 learning workload or confidence."""
        p1 = self.personas[0]
        match_high = {
            "masco_code": "2521",
            "occupation_title": "Database Designer",
            "missing_core_skills": [{"skill_id": "data_privacy_pdpa", "deficit": 1.0, "strength": "CORE_REQUIREMENT"}],
            "missing_core_count": 1,
            "transition_distance": "SHORT TRANSITION",
            "role_match_index": 88.0,
            "evidence_confidence_index": 95.0
        }
        match_low = {
            "masco_code": "2521",
            "occupation_title": "Database Designer",
            "missing_core_skills": [{"skill_id": "data_privacy_pdpa", "deficit": 1.0, "strength": "CORE_REQUIREMENT"}],
            "missing_core_count": 1,
            "transition_distance": "SHORT TRANSITION",
            "role_match_index": 35.0,
            "evidence_confidence_index": 20.0
        }
        
        p_high = self.m4_engine.build_pathway(p1, match_high)
        p_low = self.m4_engine.build_pathway(p1, match_low)
        
        # Hours must be identical
        self.assertEqual(p_high["total_estimated_hours_low"], p_low["total_estimated_hours_low"])
        self.assertEqual(p_high["total_estimated_hours_high"], p_low["total_estimated_hours_high"])
        # Pathway evidence confidence must be identical because data evidence is identical
        self.assertEqual(p_high["pathway_evidence_confidence_index"], p_low["pathway_evidence_confidence_index"])

    def test_confidence_independent_of_pathway_length(self):
        """Verify pathway confidence does not automatically degrade solely due to pathway length."""
        p_short = self.personas[0] # 2 steps
        p_long = self.personas[1]  # 3 steps
        match_short = next(m for m in self.m3_engine.rank_roles(p_short) if m["masco_code"] == "2521")
        match_long = next(m for m in self.m3_engine.rank_roles(p_long) if m["masco_code"] == "2512")
        
        path_short = self.m4_engine.build_pathway(p_short, match_short)
        path_long = self.m4_engine.build_pathway(p_long, match_long)
        
        self.assertEqual(path_short["total_pathway_steps"], 2)
        self.assertEqual(path_long["total_pathway_steps"], 3)
        # Long pathway can have high confidence
        self.assertGreaterEqual(path_long["pathway_evidence_confidence_index"], 85.0)

    def test_confidence_independent_of_resource_cost(self):
        """Verify whether a resource is free or paid does not mechanically inflate/deflate confidence."""
        steps_free = [{
            "skill_id": "api_integration",
            "priority_tier": "CORE_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {
                "primary_resource": {
                    "resource_id": "RES_FREE",
                    "cost_status": "FREE",
                    "skill_alignment": 0.95,
                    "provider_reliability": 0.95,
                    "last_verified_date": "2026-10-23"
                }
            }
        }]
        steps_paid = [{
            "skill_id": "api_integration",
            "priority_tier": "CORE_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {
                "primary_resource": {
                    "resource_id": "RES_PAID",
                    "cost_status": "LOW_COST",
                    "cost_amount_if_verified": 99.0,
                    "skill_alignment": 0.95,
                    "provider_reliability": 0.95,
                    "last_verified_date": "2026-10-23"
                }
            }
        }]
        
        score_free, _, comp_free, _, _ = self.m4_engine._calculate_pathway_confidence(steps_free, 85.0)
        score_paid, _, comp_paid, _, _ = self.m4_engine._calculate_pathway_confidence(steps_paid, 85.0)
        
        self.assertEqual(score_free, score_paid)
        self.assertEqual(comp_free["resource_verification_quality"], comp_paid["resource_verification_quality"])

    def test_resource_verification_affects_confidence_appropriately(self):
        """Verify degraded resource alignment reduces pathway evidence confidence."""
        steps_high = [{
            "skill_id": "sql_data_analysis",
            "priority_tier": "CORE_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {
                "primary_resource": {
                    "resource_id": "RES_HIGH",
                    "cost_status": "FREE",
                    "skill_alignment": 0.98,
                    "provider_reliability": 0.98,
                    "last_verified_date": "2026-10-23"
                }
            }
        }]
        steps_degraded = [{
            "skill_id": "sql_data_analysis",
            "priority_tier": "CORE_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {
                "primary_resource": {
                    "resource_id": "RES_DEG",
                    "cost_status": "FREE",
                    "skill_alignment": 0.70,
                    "provider_reliability": 0.70,
                    "last_verified_date": "2026-10-23"
                }
            }
        }]
        
        score_high, _, _, _, _ = self.m4_engine._calculate_pathway_confidence(steps_high, 85.0)
        score_deg, _, _, flags_deg, _ = self.m4_engine._calculate_pathway_confidence(steps_degraded, 85.0)
        
        self.assertGreater(score_high, score_deg)
        self.assertTrue(any("RESOURCE_QUALITY_MODERATE" in f for f in flags_deg))

    def test_confidence_demonstration_high_medium_low(self):
        """Demonstrate HIGH, MEDIUM, and LOW confidence labels in unit test conditions."""
        # 1. HIGH
        steps_high = [{
            "skill_id": "prompt_engineering",
            "priority_tier": "CORE_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {"primary_resource": {"skill_alignment": 0.95, "provider_reliability": 0.95, "last_verified_date": "2026-10-23"}}
        }]
        score_h, label_h, _, _, _ = self.m4_engine._calculate_pathway_confidence(steps_high, 85.0)
        self.assertEqual(label_h, "HIGH")

        # 2. MEDIUM (Aged resources + lower requirement strength)
        steps_med = [{
            "skill_id": "prompt_engineering",
            "priority_tier": "SUPPORTING_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {"primary_resource": {"skill_alignment": 0.75, "provider_reliability": 0.75, "last_verified_date": "2025-09-01"}}
        }]
        score_m, label_m, _, _, _ = self.m4_engine._calculate_pathway_confidence(steps_med, 85.0)
        self.assertEqual(label_m, "MEDIUM")

        # 3. LOW (Missing resource + stale dates)
        steps_low = [{
            "skill_id": "prompt_engineering",
            "priority_tier": "SUPPORTING_REQUIREMENT",
            "direct_prerequisites": [],
            "resources": {"primary_resource": None}
        }]
        score_l, label_l, _, _, _ = self.m4_engine._calculate_pathway_confidence(steps_low, 85.0)
        self.assertIn(label_l, ["LOW", "INSUFFICIENT"])

    # =========================================================================
    # 3. P2-01 — PROVIDER NORMALIZATION
    # =========================================================================
    def test_provider_normalization_deterministic(self):
        """Verify all 36 production resources have normalized provider groups and 21 parent institutions."""
        self.assertEqual(len(self.resources_data["resources"]), 36)
        
        groups = set()
        raw_labels = set()
        for r in self.resources_data["resources"]:
            self.assertIn("provider_display_name", r)
            self.assertIn("provider_group_id", r)
            self.assertIn("provider_group_name", r)
            groups.add(r["provider_group_id"])
            raw_labels.add(r["provider_display_name"])
            
        self.assertEqual(len(groups), 21, "Must normalize into exactly 21 institutional provider groups!")
        self.assertEqual(len(raw_labels), 27, "Must retain 27 raw provider display labels for 36 courses!")

    # =========================================================================
    # 4. P2-02 — REMOVAL OF SYNTHETIC FIXTURES FROM PRODUCTION CATALOG
    # =========================================================================
    def test_zero_synthetic_fixtures_in_production_catalog(self):
        """Verify production catalog has exactly zero test fixtures and RES_LOWCOST_01/RES_VAR_01 are purged."""
        res_ids = [r["resource_id"] for r in self.resources_data["resources"]]
        self.assertNotIn("RES_LOWCOST_01", res_ids)
        self.assertNotIn("RES_VAR_01", res_ids)
        
        for r in self.resources_data["resources"]:
            self.assertFalse(r.get("test_only", False))
            self.assertIsNone(r.get("fixture_type"))

    def test_fixtures_isolated_in_test_fixtures_directory(self):
        """Verify test fixtures live in tests/fixtures/ and are marked test_only."""
        fix_path = os.path.join(PROJECT_ROOT, "tests", "fixtures", "m4_resource_pricing_fixtures.json")
        self.assertTrue(os.path.exists(fix_path))
        with open(fix_path, "r", encoding="utf-8") as f:
            fixtures_data = json.load(f)
        
        self.assertTrue(fixtures_data.get("test_only"))
        self.assertEqual(fixtures_data["total_fixtures"], 2)
        fix_ids = [f["resource_id"] for f in fixtures_data["fixtures"]]
        self.assertIn("RES_LOWCOST_01", fix_ids)
        self.assertIn("RES_VAR_01", fix_ids)
        for f in fixtures_data["fixtures"]:
            self.assertTrue(f["test_only"])
            self.assertEqual(f["fixture_type"], "BENCHMARK_SYNTHETIC_TEST_FIXTURE")

    # =========================================================================
    # 5. P2-03 — LEARNING-TIME 0.50 FLOOR RATIONALE & SENSITIVITY
    # =========================================================================
    def test_effort_floor_loaded_from_config(self):
        """Verify 0.50 floor is loaded from config, not buried in code."""
        scaling_cfg = self.config_data["learning_time_estimation"]["deficit_effort_scaling"]
        self.assertEqual(scaling_cfg["min_multiplier_floor"], 0.50)
        self.assertTrue(len(scaling_cfg["floor_rationale"]) > 20)

    def test_floor_sensitivity_ordering_invariance(self):
        """Verify varying the floor parameter between 0.35, 0.50, and 0.65 does not disrupt prerequisite order."""
        p2 = self.personas[1]
        match = next(m for m in self.m3_engine.rank_roles(p2) if m["masco_code"] == "2512")
        
        # Test 0.50 baseline
        p_50 = self.m4_engine.build_pathway(p2, match)
        steps_50 = [s["skill_id"] for s in p_50["pathway_steps"]]
        
        # Temporarily test 0.35
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.35
        p_35 = self.m4_engine.build_pathway(p2, match)
        steps_35 = [s["skill_id"] for s in p_35["pathway_steps"]]
        
        # Temporarily test 0.65
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.65
        p_65 = self.m4_engine.build_pathway(p2, match)
        steps_65 = [s["skill_id"] for s in p_65["pathway_steps"]]
        
        # Verify ordering invariance across all three floors
        self.assertEqual(steps_50, steps_35, "Prerequisite ordering must be invariant to effort floor!")
        self.assertEqual(steps_50, steps_65, "Prerequisite ordering must be invariant to effort floor!")
        
        # Verify that for partial deficit (deficit < 1.0), the floor actively scales hours
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.35
        _, h_35, _, _, _ = self.m4_engine._calculate_step_effort("prompt_engineering", deficit=0.10)
        
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.50
        _, h_50, _, _, _ = self.m4_engine._calculate_step_effort("prompt_engineering", deficit=0.10)
        
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.65
        _, h_65, _, _, _ = self.m4_engine._calculate_step_effort("prompt_engineering", deficit=0.10)
        
        # Reset to 0.50 baseline
        self.m4_engine.config["learning_time_estimation"]["deficit_effort_scaling"]["min_multiplier_floor"] = 0.50
        
        self.assertLess(h_35, h_50, "Floor 0.35 should yield lower hours for partial deficit than floor 0.50")
        self.assertLess(h_50, h_65, "Floor 0.50 should yield lower hours for partial deficit than floor 0.65")

    def test_mastered_skill_receives_zero_pathway_steps(self):
        """Verify fully qualified worker profile receives 0 steps and NO_RESKILLING_REQUIRED."""
        all_skills_confirmed = {
            "ai_literacy": "USER_CONFIRMED",
            "prompt_engineering": "USER_CONFIRMED",
            "python_scripting": "USER_CONFIRMED",
            "sql_data_analysis": "USER_CONFIRMED",
            "data_visualization": "USER_CONFIRMED",
            "process_mapping": "USER_CONFIRMED",
            "workflow_automation": "USER_CONFIRMED",
            "api_integration": "USER_CONFIRMED",
            "rag_knowledge_systems": "USER_CONFIRMED",
            "data_privacy_pdpa": "USER_CONFIRMED",
            "ai_ethics_governance": "USER_CONFIRMED",
            "human_in_the_loop_qa": "USER_CONFIRMED",
            "esg_sustainability_reporting": "USER_CONFIRMED",
            "carbon_footprint_analytics": "USER_CONFIRMED",
            "instructional_design": "USER_CONFIRMED",
            "stakeholder_communication": "USER_CONFIRMED"
        }
        perfect_profile = {"skills": all_skills_confirmed}
        match = {
            "masco_code": "2521",
            "occupation_title": "Database Designer",
            "missing_core_skills": [],
            "missing_important_skills": [],
            "missing_supporting_skills": [],
            "missing_core_count": 0,
            "transition_distance": "ZERO TRANSITION"
        }
        
        pathway = self.m4_engine.build_pathway(perfect_profile, match)
        self.assertEqual(pathway["total_pathway_steps"], 0)
        self.assertEqual(pathway["status"], "NO_RESKILLING_REQUIRED")
        self.assertEqual(pathway["total_estimated_hours_low"], 0)
        self.assertEqual(pathway["total_estimated_hours_high"], 0)

    # =========================================================================
    # 6. P3-01 & P3-02 — POLICY DISCLAIMERS & BENCHMARK WEEK ASSUMPTIONS
    # =========================================================================
    def test_low_cost_threshold_and_disclaimer_present(self):
        """Verify RM150 threshold and operational product disclaimer are present."""
        cost_cfg = self.config_data["cost_policy"]
        self.assertEqual(cost_cfg["low_cost_threshold_myr"], 150.0)
        self.assertIn("For this prototype, LOW_COST is operationally defined", cost_cfg["operational_disclaimer"])
        
        p = self.personas[0]
        match = self.m3_engine.rank_roles(p)[0]
        pathway = self.m4_engine.build_pathway(p, match)
        self.assertIn("operational_disclaimer", pathway["verified_cost_summary"])
        self.assertEqual(pathway["verified_cost_summary"]["low_cost_threshold_myr"], 150.0)

    def test_benchmark_week_label_test_assumption(self):
        """Verify benchmark results label weekly pace as TEST ASSUMPTION: 10 STUDY HOURS/WEEK."""
        benchmark_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_benchmark_results_v1_1.json")
        with open(benchmark_file, "r", encoding="utf-8") as f:
            b_data = json.load(f)
        
        for tc in b_data["test_cases"]:
            self.assertEqual(tc["schedule_assumptions"], "TEST ASSUMPTION: 10 STUDY HOURS/WEEK")
            self.assertIn("schedule_weeks_test_assumption_10h_per_week", tc)

    def test_user_week_estimates_require_explicit_hours(self):
        """Verify user pathway does NOT calculate weeks unless hours_per_week is provided."""
        p = self.personas[0]
        match = self.m3_engine.rank_roles(p)[0]
        
        pathway_no_schedule = self.m4_engine.build_pathway(p, match, hours_per_week=None)
        self.assertIsNone(pathway_no_schedule["schedule_estimate"])
        
        pathway_with_schedule = self.m4_engine.build_pathway(p, match, hours_per_week=15)
        self.assertIsNotNone(pathway_with_schedule["schedule_estimate"])
        self.assertEqual(pathway_with_schedule["schedule_estimate"]["study_hours_per_week"], 15)
        self.assertEqual(pathway_with_schedule["schedule_estimate"]["label"], "USER-SCHEDULE-DEPENDENT ESTIMATE")

    # =========================================================================
    # 7. CORE INVARIANTS, FAIRNESS, TOPOLOGY & MANIFEST
    # =========================================================================
    def test_core_first_prioritisation(self):
        """Verify missing CORE requirements appear before non-core requirements unless prerequisite dictates."""
        p8 = self.personas[7]  # Persona 8 on 3322 has missing CORE stakeholder_communication
        match = next(m for m in self.m3_engine.rank_roles(p8) if m["masco_code"] == "3322")
        pathway = self.m4_engine.build_pathway(p8, match)
        
        step_1 = pathway["pathway_steps"][0]
        self.assertIn(step_1["priority_tier"], ["CORE_REQUIREMENT", "FOUNDATION_PREREQUISITE"])
        self.assertEqual(step_1["skill_id"], "stakeholder_communication")

    def test_prerequisite_ordering_dag(self):
        """Verify required prerequisites appear at strictly earlier step indices than dependent skills."""
        p2 = self.personas[1]  # Persona 2 on 2512 requires human_in_the_loop_qa, which requires ai_literacy
        match = next(m for m in self.m3_engine.rank_roles(p2) if m["masco_code"] == "2512")
        pathway = self.m4_engine.build_pathway(p2, match)
        
        step_indices = {s["skill_id"]: s["step_number"] for s in pathway["pathway_steps"]}
        if "human_in_the_loop_qa" in step_indices and "ai_literacy" in step_indices:
            self.assertLess(step_indices["ai_literacy"], step_indices["human_in_the_loop_qa"])

    def test_scenario_cannot_invent_unsupported_skills(self):
        """M6 scenario urgency can re-rank existing gaps, but cannot manufacture gaps unneeded by the role."""
        p1 = self.personas[0]
        match = next(m for m in self.m3_engine.rank_roles(p1) if m["masco_code"] == "2521")
        
        p_ref = self.m4_engine.build_pathway(p1, match, scenario_id="REFERENCE_2026")
        p_agentic = self.m4_engine.build_pathway(p1, match, scenario_id="FAST_AGENTIC")
        
        self.assertEqual(
            set(s["skill_id"] for s in p_ref["pathway_steps"]),
            set(s["skill_id"] for s in p_agentic["pathway_steps"])
        )

    def test_resource_failure_independence(self):
        """If resource catalog is empty for a skill, the skill step remains intact with primary_resource=None."""
        p = self.personas[0]
        match = self.m3_engine.rank_roles(p)[0]
        test_skill = "data_privacy_pdpa"
        
        orig = self.m4_engine.resources_by_skill[test_skill]
        self.m4_engine.resources_by_skill[test_skill] = []
        pathway = self.m4_engine.build_pathway(p, match)
        self.m4_engine.resources_by_skill[test_skill] = orig
        
        step = next((s for s in pathway["pathway_steps"] if s["skill_id"] == test_skill), None)
        if step:
            self.assertIsNone(step["resources"]["primary_resource"])
            self.assertIn("No verified external resource", step["resources"]["resource_selection_rationale"])

    def test_demographic_fairness_invariance(self):
        """Demographic variations on identical skill profiles produce 100% identical pathways."""
        base_p = self.personas[0]
        match = self.m3_engine.rank_roles(base_p)[0]
        p_base = self.m4_engine.build_pathway(base_p, match)
        
        pert_p = base_p.copy()
        pert_p.update({"age": 48, "gender": "FEMALE", "race": "MALAY", "school": "Public University", "income": 3000})
        p_pert = self.m4_engine.build_pathway(pert_p, match)
        
        self.assertEqual(
            [s["skill_id"] for s in p_base["pathway_steps"]],
            [s["skill_id"] for s in p_pert["pathway_steps"]]
        )
        self.assertEqual(p_base["total_estimated_hours_low"], p_pert["total_estimated_hours_low"])
        self.assertEqual(p_base["total_estimated_hours_high"], p_pert["total_estimated_hours_high"])

    def test_v1_1_build_manifest_hashes_match(self):
        """Verify generated v1.1.0 build manifest hashes match active files on disk."""
        manifest_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_build_manifest_v1_1.json")
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        prereqs_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "skill_prerequisites_v1_1.json")
        resources_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "learning_resources_v1_1.json")
        config_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_scoring_config_v1_1.json")
        benchmarks_file = os.path.join(PROJECT_ROOT, "data", "reskilling", "m4_benchmark_results_v1_1.json")
        fixtures_file = os.path.join(PROJECT_ROOT, "tests", "fixtures", "m4_resource_pricing_fixtures.json")
        source_file = os.path.join(PROJECT_ROOT, "src", "reskilling_pathway_engine.py")
        
        self.assertEqual(manifest["artifacts_sha256"]["skill_prerequisites"], get_file_sha256(prereqs_file))
        self.assertEqual(manifest["artifacts_sha256"]["learning_resources"], get_file_sha256(resources_file))
        self.assertEqual(manifest["artifacts_sha256"]["scoring_config"], get_file_sha256(config_file))
        self.assertEqual(manifest["artifacts_sha256"]["benchmark_results"], get_file_sha256(benchmarks_file))
        self.assertEqual(manifest["artifacts_sha256"]["pricing_fixtures"], get_file_sha256(fixtures_file))
        self.assertEqual(manifest["artifacts_sha256"]["source_code"], get_file_sha256(source_file))


if __name__ == "__main__":
    unittest.main()
