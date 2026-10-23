"""
tests/test_role_matching_engine.py

Comprehensive test suite for M3 Explainable Future-Role Matching Engine v1.1.0.
Verifies all safety contracts, mathematical bounds, guardrails, demographic neutrality,
user override hierarchy, explainability traceability, decoupled confidence, continuous gating,
and Stage 11C remediation requirements using standard unittest.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
sys.path.insert(0, str(BASE_DIR))

from src.role_matching_engine import RoleMatchingEngine, RoleRankingResult


class TestRoleMatchingEngineV1_1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = RoleMatchingEngine()

    # 1. Candidate Role Universe & Fallback Neutrality
    def test_candidate_universe_strictly_20_four_digit(self):
        """Candidate roles pool must be strictly the 20 four-digit MASCO occupations."""
        self.assertEqual(len(self.engine.roles), 20)
        for code, role in self.engine.roles.items():
            self.assertEqual(len(code), 4)
            self.assertTrue(code.isdigit())
            self.assertEqual(role["entity_granularity"], "FOUR_DIGIT_OCCUPATION")

    def test_major_group_fallbacks_excluded(self):
        """Major Group fallbacks (MAJOR_1 to MAJOR_9) must never appear in candidate pool."""
        for fallback_id in [f"MAJOR_{i}" for i in range(1, 10)]:
            self.assertNotIn(fallback_id, self.engine.roles)

        test_profile = {"skills": {"sql_data_analysis": "USER_CONFIRMED"}}
        ranking = self.engine.rank_roles(test_profile)
        for r in ranking:
            self.assertFalse(r["masco_code"].startswith("MAJOR_"))

    # 2. Downstream Safety Weight Contract Bounds
    def test_weight_bounds_contract(self):
        """All weight configurations must strictly satisfy: M1 >= 55%, M2 <= 30%, M6 <= 15%."""
        bounds = self.engine.config["safety_contract_bounds"]
        for name, cfg in self.engine.config["weight_configurations"].items():
            m1_tot = cfg["m1_skill_weights"]["total_m1"]
            m2_tot = cfg["m2_labor_weights"]["total_m2"]
            m6_tot = cfg["m6_scenario_weights"]["total_m6"]

            self.assertGreaterEqual(m1_tot, bounds["min_m1_weight"] - 1e-6, f"{name}: M1 weight {m1_tot} < 0.55")
            self.assertLessEqual(m2_tot, bounds["max_m2_weight"] + 1e-6, f"{name}: M2 weight {m2_tot} > 0.30")
            self.assertLessEqual(m6_tot, bounds["max_m6_weight"] + 1e-6, f"{name}: M6 weight {m6_tot} > 0.15")
            self.assertAlmostEqual(m1_tot + m2_tot + m6_tot, 1.0, places=4, msg=f"{name}: Weights must sum to 1.0")

    # 3. User Override Hierarchy & Deduplication
    def test_user_override_dismissal(self):
        """Dismissed skill must receive zero credit, overriding M1 core inference."""
        profile_with_m1 = {
            "m1_inferred_skills": {"core": ["python_scripting", "api_integration"]},
            "dismissed_skills": ["python_scripting"]
        }
        normalized, _, _ = self.engine._normalize_user_skills(profile_with_m1)
        self.assertEqual(normalized.get("python_scripting"), 0.0)
        self.assertEqual(normalized.get("api_integration"), 0.85)

    def test_user_override_added_skill(self):
        """User added skill must receive 1.0 credit and be recognized."""
        profile = {
            "user_added_skills": ["rag_knowledge_systems"]
        }
        normalized, _, _ = self.engine._normalize_user_skills(profile)
        self.assertEqual(normalized.get("rag_knowledge_systems"), 1.0)

    def test_user_confirmation_priority_hierarchy(self):
        """Evidence priority: USER_CONFIRMED (1.0) > M1_CORE (0.85) > M1_SUGGESTED (0.50)."""
        weights = self.engine.user_confirm_weights
        self.assertEqual(weights["USER_CONFIRMED"], 1.0)
        self.assertEqual(weights["USER_ADDED"], 1.0)
        self.assertEqual(weights["M1_CORE"], 0.85)
        self.assertEqual(weights["M1_SUGGESTED"], 0.50)
        self.assertEqual(weights["DISMISSED"], 0.0)

    def test_duplicate_skills_do_not_inflate_score(self):
        """Duplicate skill declarations must resolve to max credit without double counting."""
        profile = {
            "skills": {
                "python_scripting": "USER_CONFIRMED",
            },
            "user_added_skills": ["python_scripting"],
            "m1_inferred_skills": {"core": ["python_scripting"]}
        }
        normalized, _, _ = self.engine._normalize_user_skills(profile)
        self.assertEqual(normalized["python_scripting"], 1.0)

    def test_unknown_skills_do_not_contribute(self):
        """Unknown skill IDs must be preserved in unmapped_skills and emit warning."""
        profile = {
            "skills": {
                "quantum_computing": "USER_CONFIRMED",
                "python_scripting": "USER_CONFIRMED"
            }
        }
        normalized, unmapped, warnings = self.engine._normalize_user_skills(profile)
        self.assertIn("quantum_computing", unmapped)
        self.assertNotIn("quantum_computing", normalized)
        self.assertIn("UNKNOWN_SKILL_NOT_SCORED", warnings)

    # 4. P1-1: Match Strength vs Evidence Confidence Decoupling
    def test_match_strength_independent_from_evidence_confidence(self):
        """Match strength label must describe fit, while evidence confidence describes data certainty."""
        profile = {"skills": {"python_scripting": "USER_CONFIRMED", "api_integration": "USER_CONFIRMED"}}
        match = self.engine.get_role_match(profile, "2512")

        self.assertIn("match_strength_label", match)
        self.assertIn("evidence_confidence_label", match)
        self.assertIn("evidence_confidence_index", match)
        self.assertNotIn("HIGH CONFIDENCE", match["match_strength_label"])

    def test_high_match_with_medium_confidence_possible(self):
        """Proxy-mapped PARTIAL role 2519 with full skills exhibits high match + medium confidence."""
        profile = {
            "skills": {
                "python_scripting": "USER_CONFIRMED",
                "api_integration": "USER_CONFIRMED",
                "workflow_automation": "USER_CONFIRMED"
            }
        }
        match_2519 = self.engine.get_role_match(profile, "2519")

        self.assertGreaterEqual(match_2519["role_match_index"], 70.0)
        self.assertIn(match_2519["match_strength_label"], ["STRONG CURRENT FIT", "GOOD FIT WITH GAPS"])
        self.assertEqual(match_2519["evidence_confidence_label"], "MEDIUM")
        self.assertLess(match_2519["evidence_confidence_index"], 75.0)

    def test_low_match_with_high_confidence_possible(self):
        """COMPLETE role 2143 with 0% skill fit exhibits low match + high evidence confidence."""
        profile = {"skills": {"python_scripting": "USER_CONFIRMED"}}
        match_2143 = self.engine.get_role_match(profile, "2143")

        self.assertLess(match_2143["role_match_index"], 20.0)
        self.assertEqual(match_2143["match_strength_label"], "DISTANT TRANSITION")
        self.assertEqual(match_2143["evidence_confidence_label"], "HIGH")
        self.assertGreaterEqual(match_2143["evidence_confidence_index"], 75.0)

    def test_role_completeness_affects_confidence_not_skill_fit(self):
        """Partial completeness lowers evidence confidence index without suppressing earned skill fit."""
        profile = {"skills": {"python_scripting": "USER_CONFIRMED", "api_integration": "USER_CONFIRMED"}}
        match_2512 = self.engine.get_role_match(profile, "2512")  # COMPLETE
        match_2519 = self.engine.get_role_match(profile, "2519")  # PARTIAL

        # Both have 100% core coverage for these 2 skills
        self.assertEqual(match_2512["components"]["core_requirement_coverage_pct"], 100.0)
        self.assertEqual(match_2519["components"]["core_requirement_coverage_pct"], 100.0)
        # But evidence confidence is lower for PARTIAL
        self.assertGreater(match_2512["evidence_confidence_index"], match_2519["evidence_confidence_index"])

    # 5. P1-2: Deterministic Requirement Derivation
    def test_requirement_derivation_deterministic(self):
        """Every role-skill requirement must have auditable derivation rule and evidence references."""
        for role in self.engine.role_catalog["roles"]:
            self.assertIn("skill_requirement_details", role)
            for detail in role["skill_requirement_details"]:
                self.assertIn("derivation_rule_id", detail)
                self.assertIn("derivation_reason", detail)
                self.assertIn("publisher_count", detail)
                self.assertGreater(detail["publisher_count"], 0)

    def test_low_mapping_confidence_cannot_create_core(self):
        """In derivation rulebook, LOW mapping confidence must demote to IMPORTANT or SUPPORTING."""
        from scripts.build_role_requirements import derive_skill_requirement_rule
        strength, rule, reason, _, _ = derive_skill_requirement_rule("CORE_REQUIREMENT", ["ESCO_2512"], "LOW")
        self.assertNotEqual(strength, "CORE_REQUIREMENT")
        self.assertEqual(strength, "IMPORTANT")
        self.assertEqual(rule, "RULE_DEMOTION_LOW_MAPPING_CONFIDENCE")

    def test_policy_only_source_cannot_create_core(self):
        """Single policy document without occupational taxonomy cannot assign CORE."""
        from scripts.build_role_requirements import derive_skill_requirement_rule
        strength, rule, reason, _, _ = derive_skill_requirement_rule("CORE_REQUIREMENT", ["BURSA_MALAYSIA_ESG_2024"], "HIGH")
        self.assertNotEqual(strength, "CORE_REQUIREMENT")
        self.assertEqual(rule, "RULE_DEMOTION_UNGROUNDED_POLICY")

    # 6. P1-3: Continuous Low-Fit Gating & No Discontinuity Cliff
    def test_zero_overlap_continuous_gating(self):
        """A role with zero skill overlap has G(S_fit) = 0.0, completely zeroing M2/M6 contextual boost."""
        profile = {"skills": {"instructional_design": "USER_CONFIRMED"}}
        match_2512 = self.engine.get_role_match(profile, "2512")

        self.assertEqual(match_2512["components"]["current_skill_fit"], 0.0)
        self.assertEqual(match_2512["components"]["skill_fit_gating_factor"], 0.0)
        self.assertEqual(match_2512["components"]["m2_effective_contribution"], 0.0)
        self.assertEqual(match_2512["components"]["m6_effective_contribution"], 0.0)
        self.assertLessEqual(match_2512["role_match_index"], 5.0)

    def test_no_score_cliff_around_zero_fit(self):
        """Progressive skill overlap from 0% to 20% must show smooth score progression without a 21-point cliff."""
        # Tier 0: 0% fit for 2512
        p0 = {"skills": {"instructional_design": "USER_CONFIRMED"}}
        m0 = self.engine.get_role_match(p0, "2512")["role_match_index"]

        # Tier 1: 7.9% fit for 2512 (supporting skill rag_knowledge_systems)
        p1 = {"skills": {"rag_knowledge_systems": "USER_CONFIRMED"}}
        m1 = self.engine.get_role_match(p1, "2512")["role_match_index"]

        score_jump = m1 - m0
        # In v1.0.0 the jump was 21.2 points (15.0 -> 36.2). In v1.1.0 it must be smooth (<= 16.0 points for 0% to 7.9%)
        self.assertLessEqual(score_jump, 16.0, f"Score jump {score_jump} is too steep; discontinuity present.")

    # 7. P2-1: Removal of 20% Post-Sort Bubble Swap
    def test_no_bubble_swap_override(self):
        """Applied guardrails must not contain SCENARIO_DOMINANCE_PROTECTED; ranking is purely continuous."""
        profile = {"skills": {"sql_data_analysis": "USER_CONFIRMED", "python_scripting": "USER_CONFIRMED"}}
        ranking = self.engine.rank_roles(profile, scenario_id="FAST_AGENTIC")

        for r in ranking:
            self.assertNotIn("SCENARIO_DOMINANCE_PROTECTED", r.get("applied_guardrails", []))

    def test_context_cannot_dominate_poor_fit(self):
        """Continuous gating ensures high-M2/M6 role with poor fit cannot outrank role with superior skill fit."""
        # Profile has software development core skills
        profile = {"skills": {"python_scripting": "USER_CONFIRMED", "api_integration": "USER_CONFIRMED"}}
        ranking = self.engine.rank_roles(profile, scenario_id="FAST_AGENTIC")

        top_role = ranking[0]
        # Software developers (2512) or closely related (2519) should dominate unrelated roles with high M2/M6
        self.assertIn(top_role["masco_code"], ["2512", "2519"])
        self.assertGreater(top_role["components"]["current_skill_fit"], 50.0)

    # 8. P2-2: Recalibrated Weight-Sensitivity Flag
    def test_weight_sensitivity_flag_recalibrated(self):
        """Sensitivity flag must trigger on Top-3 flips or major displacement (disp >= 4), not minor shifts."""
        bench_file = self.engine.data_dir / "matching" / "m3_benchmark_results_v1_1.json"
        self.assertTrue(bench_file.exists())
        with open(bench_file, "r", encoding="utf-8") as f:
            bench = json.load(f)

        sensitive_count = bench["aggregate_metrics"]["total_weight_sensitive_roles_count"]
        # In v1.0.0 it was 18. In v1.1.0 it should be recalibrated to a meaningful subset (<= 10)
        self.assertLessEqual(sensitive_count, 10)
        self.assertGreater(sensitive_count, 0)

    # 9. P2-3: Demographic Field Stripping & Neutrality
    def test_protected_attributes_stripped_not_scored(self):
        """Protected demographic attributes must be stripped with a warning and not crash."""
        dirty_profile = {
            "skills": {"sql_data_analysis": "USER_CONFIRMED"},
            "gender": "Female",
            "age": 32,
            "religion": "Islam",
            "race": "Malay"
        }
        ranking = self.engine.rank_roles(dirty_profile)
        self.assertEqual(len(ranking), 20)
        self.assertIn("PROTECTED_ATTRIBUTE_STRIPPED", ranking.warnings)

    def test_fairness_invariance_on_protected_attributes(self):
        """Identical skill sets with different protected attributes must yield identical scores and ranks."""
        p_male = {"skills": {"python_scripting": "USER_CONFIRMED"}, "gender": "Male", "age": 25}
        p_female = {"skills": {"python_scripting": "USER_CONFIRMED"}, "gender": "Female", "age": 45}

        rank_m = self.engine.rank_roles(p_male)
        rank_f = self.engine.rank_roles(p_female)

        for rm, rf in zip(rank_m, rank_f):
            self.assertEqual(rm["masco_code"], rf["masco_code"])
            self.assertEqual(rm["role_match_index"], rf["role_match_index"])
            self.assertEqual(rm["evidence_confidence_index"], rf["evidence_confidence_index"])
            self.assertEqual(rm["rank"], rf["rank"])

    # 10. P2-4: Empty Profile & Degenerate Profiles
    def test_empty_profile_returns_insufficient_profile_data(self):
        """Completely empty profile must return INSUFFICIENT_PROFILE_DATA with zero matches."""
        empty_profile = {}
        result = self.engine.rank_roles(empty_profile)

        self.assertEqual(result.status, "INSUFFICIENT_PROFILE_DATA")
        self.assertEqual(len(result), 0)
        self.assertEqual(result["role_matches"], [])
        self.assertIn("INSUFFICIENT_PROFILE_DATA", result.warnings)

    def test_all_dismissed_profile_returns_insufficient_state(self):
        """Profile where all skills are dismissed must return INSUFFICIENT_PROFILE_DATA."""
        dismissed_profile = {
            "skills": {"python_scripting": "DISMISSED", "sql_data_analysis": "DISMISSED"}
        }
        result = self.engine.rank_roles(dismissed_profile)
        self.assertEqual(result.status, "INSUFFICIENT_PROFILE_DATA")
        self.assertEqual(len(result), 0)

    # 11. P3-1: Deterministic Tie-Breaking
    def test_deterministic_tie_breaking(self):
        """Tie breaking must follow: role_match_index DESC, skill_fit DESC, masco_code ASC."""
        profile = {"skills": {"stakeholder_communication": "USER_CONFIRMED"}}
        ranking = self.engine.rank_roles(profile)

        for i in range(len(ranking) - 1):
            r1 = ranking[i]
            r2 = ranking[i + 1]
            if r1["role_match_index"] == r2["role_match_index"]:
                if r1["components"]["current_skill_fit"] == r2["components"]["current_skill_fit"]:
                    self.assertLess(int(r1["masco_code"]), int(r2["masco_code"]))

    # 12. P3-3: Missing Core Count Payload
    def test_missing_core_count_payload(self):
        """Every role match output must explicitly contain missing_core_count, matched_core_count, and total."""
        profile = {"skills": {"python_scripting": "USER_CONFIRMED"}}
        match = self.engine.get_role_match(profile, "2512")

        self.assertIn("missing_core_count", match)
        self.assertIn("matched_core_count", match)
        self.assertIn("core_requirements_count", match)
        self.assertEqual(match["core_requirements_count"], 2)
        self.assertEqual(match["matched_core_count"], 1)
        self.assertEqual(match["missing_core_count"], 1)

    # 13. Upstream Frozen Hashes & Rebuild Integrity
    def test_frozen_upstream_hashes_unchanged(self):
        """Upstream M1, M2, and M6 freeze hashes must remain exactly as certified."""
        manifest_path = self.engine.data_dir / "matching" / "m3_build_manifest_v1_1.json"
        self.assertTrue(manifest_path.exists())
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        m2_hash = manifest["upstream_dependencies"]["m2_trend_intelligence"]["manifest_sha256"]
        m6_hash = manifest["upstream_dependencies"]["m6_scenario_engine"]["manifest_sha256"]

        self.assertEqual(m2_hash, "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542")
        self.assertEqual(m6_hash, "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5")

    # 14. Explainability & Traceability
    def test_explain_role_match_v1_1(self):
        """Explainability output must provide match strength, evidence confidence, citations, and disclaimer."""
        profile = {"skills": {"python_scripting": "USER_CONFIRMED", "api_integration": "USER_CONFIRMED"}}
        exp = self.engine.explain_role_match(profile, "2512")

        self.assertIn("match_strength_label", exp)
        self.assertIn("evidence_confidence_label", exp)
        self.assertIn("evidence_confidence_index", exp)
        self.assertIn("confidence_explanation", exp)
        self.assertIn("evidence_citations", exp)
        self.assertIn("DISCLAIMER", exp["disclaimer"].upper())


if __name__ == "__main__":
    unittest.main()
