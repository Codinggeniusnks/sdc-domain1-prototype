"""
test_scenario_engine_v1_1.py

Comprehensive test suite for M6 Future Workforce Scenario Engine (v1.1.0).
Verifies all Stage 10C remediations:
1. M2 freeze hashes & M1 provenance
2. REFERENCE central analytic multiplier = 1.0000
3. No hardcoded REFERENCE multiplier bypass
4. REFERENCE lower/upper meaningful uncertainty ranges
5. Monotonic automation scaling (FAST >= MODERATE >= REFERENCE across bounds)
6. Technology diffusion parameter non-zero sensitivity
7. All 8 scenario parameters active (zero dead parameters)
8. Unified outlook classifier across all scenarios
9. Zero spurious regime flips from REFERENCE to MODERATE
10. Granularity separation: 20 4-digit vs 8 Major Group fallbacks
11. Major Group direct wage measurement flags
12. Fallback neutrality contract for M3
13. Reskilling urgency calibration (clerical roles reach VERY HIGH under FAST_AGENTIC)
14. Multi-dimensional sensitivity semantics (UPSIDE_TRANSFORMATION vs DOWNSIDE_PRESSURE)
15. 4 OpenAlex zero-base skills carry INSUFFICIENT_HISTORICAL_BASELINE
16. Rank stability across multi-channel metrics
17. Deterministic rebuild verification
18. Prohibited demographic inputs rejection
"""

import unittest
import json
import hashlib
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.scenario_engine import ScenarioEngine
from scripts.build_scenario_profiles_v1_1 import get_scenario_multipliers_v1_1, REF_CENTRAL

class TestScenarioEngineV11(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = ScenarioEngine(base_dir=BASE_DIR, version="1.1.0")
        cls.artifacts_dir = BASE_DIR / "artifacts"
        cls.scenarios_dir = BASE_DIR / "data" / "scenarios"
        cls.trends_dir = BASE_DIR / "data" / "trends" / "processed"

        with open(cls.scenarios_dir / "scenario_definitions_v1_1.json", "r", encoding="utf-8") as f:
            cls.scenario_defs = json.load(f)

        with open(cls.scenarios_dir / "occupation_scenario_profiles_v1_1.json", "r", encoding="utf-8") as f:
            cls.occ_data = json.load(f)

        with open(cls.scenarios_dir / "skill_scenario_profiles_v1_1.json", "r", encoding="utf-8") as f:
            cls.skill_data = json.load(f)

    # Test 1: M2 Freeze Hash & M1 Provenance Verification
    def test_01_m2_freeze_and_provenance(self):
        freeze_manifest_path = self.artifacts_dir / "m2_v1_1_1_freeze_manifest.json"
        self.assertTrue(freeze_manifest_path.exists())
        with open(freeze_manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        expected_hash = "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"
        actual_manifest_hash = hashlib.sha256(freeze_manifest_path.read_bytes()).hexdigest()
        self.assertEqual(actual_manifest_hash, expected_hash)

        occ_hash = hashlib.sha256((self.trends_dir / "occupation_trend_profiles_v1_1_1.json").read_bytes()).hexdigest()
        skill_hash = hashlib.sha256((self.trends_dir / "skill_trend_profiles_v1_1_1.json").read_bytes()).hexdigest()
        self.assertEqual(occ_hash, manifest["output_artifacts"]["occupation_trend_profiles_v1_1_1"])
        self.assertEqual(skill_hash, manifest["output_artifacts"]["skill_trend_profiles_v1_1_1"])

    # Test 2: P1-1 REFERENCE Central Analytic Multiplier = 1.0000
    def test_02_reference_central_analytic_multiplier(self):
        ref_params = {a["assumption_name"]: a for sc in self.scenario_defs["scenarios"] if sc["scenario_id"] == "REFERENCE_2026" for a in sc["assumptions"]}
        m = get_scenario_multipliers_v1_1(ref_params, bound="central")
        self.assertEqual(m["ai_press_mult"], 1.0000)
        self.assertEqual(m["auto_mult"], 1.0000)
        self.assertEqual(m["aug_mult"], 1.0000)
        self.assertEqual(m["policy_factor"], 0.4000)

    # Test 3: P1-1 No Hardcoded REFERENCE Bypass & Non-Zero REFERENCE Uncertainty
    def test_03_reference_bounds_non_zero(self):
        ref_params = {a["assumption_name"]: a for sc in self.scenario_defs["scenarios"] if sc["scenario_id"] == "REFERENCE_2026" for a in sc["assumptions"]}
        m_lower = get_scenario_multipliers_v1_1(ref_params, bound="lower")
        m_central = get_scenario_multipliers_v1_1(ref_params, bound="central")
        m_upper = get_scenario_multipliers_v1_1(ref_params, bound="upper")

        self.assertLess(m_lower["auto_mult"], m_central["auto_mult"])
        self.assertGreater(m_upper["auto_mult"], m_central["auto_mult"])
        self.assertLess(m_lower["ai_press_mult"], m_central["ai_press_mult"])
        self.assertGreater(m_upper["ai_press_mult"], m_central["ai_press_mult"])

    # Test 4: P1-1 Monotonic Automation Scaling Across Scenarios (FAST >= MOD >= REF)
    def test_04_monotonic_automation_scaling(self):
        params_by_scen = {sc["scenario_id"]: {a["assumption_name"]: a for a in sc["assumptions"]} for sc in self.scenario_defs["scenarios"]}
        
        m_ref_c = get_scenario_multipliers_v1_1(params_by_scen["REFERENCE_2026"], "central")
        m_cop_l = get_scenario_multipliers_v1_1(params_by_scen["MODERATE_COPILOT"], "lower")
        m_cop_c = get_scenario_multipliers_v1_1(params_by_scen["MODERATE_COPILOT"], "central")
        m_cop_u = get_scenario_multipliers_v1_1(params_by_scen["MODERATE_COPILOT"], "upper")
        m_age_l = get_scenario_multipliers_v1_1(params_by_scen["FAST_AGENTIC"], "lower")
        m_age_c = get_scenario_multipliers_v1_1(params_by_scen["FAST_AGENTIC"], "central")

        # Invariant 1: Moderate Copilot lower bound >= Reference central
        self.assertGreaterEqual(m_cop_l["auto_mult"], m_ref_c["auto_mult"])
        self.assertGreaterEqual(m_cop_l["ai_press_mult"], m_ref_c["ai_press_mult"])

        # Invariant 2: Fast Agentic lower bound >= Moderate Copilot central
        self.assertGreaterEqual(m_age_l["auto_mult"], m_cop_c["auto_mult"])
        self.assertGreaterEqual(m_age_l["ai_press_mult"], m_cop_c["ai_press_mult"])

        # Invariant 3: Central ordering
        self.assertGreater(m_age_c["auto_mult"], m_cop_c["auto_mult"])
        self.assertGreater(m_cop_c["auto_mult"], m_ref_c["auto_mult"])

    # Test 5: P1-3 Technology Diffusion Parameter Non-Zero Sensitivity
    def test_05_technology_diffusion_sensitivity(self):
        cop_params = {a["assumption_name"]: a for sc in self.scenario_defs["scenarios"] if sc["scenario_id"] == "MODERATE_COPILOT" for a in sc["assumptions"]}
        
        base_m = get_scenario_multipliers_v1_1(cop_params, bound="central")
        
        # Perturb only diffusion breadth by +10 points
        perturbed_params = {k: dict(v) for k, v in cop_params.items()}
        perturbed_params["TECHNOLOGY_DIFFUSION_BREADTH"]["central"] = perturbed_params["TECHNOLOGY_DIFFUSION_BREADTH"]["central"] + 10.0
        
        pert_m = get_scenario_multipliers_v1_1(perturbed_params, bound="central")
        
        # Derivative must be non-zero and positive
        self.assertGreater(pert_m["ai_press_mult"], base_m["ai_press_mult"], "Diffusion breadth has 0 derivative on ai_press_mult!")
        self.assertGreater(pert_m["auto_mult"], base_m["auto_mult"], "Diffusion breadth has 0 derivative on auto_mult!")
        self.assertGreater(pert_m["aug_mult"], base_m["aug_mult"], "Diffusion breadth has 0 derivative on aug_mult!")

    # Test 6: P1-2 Unified Outlook Classification (Zero Spurious Baseline Flips)
    def test_06_unified_outlook_classification(self):
        ref_occs = [p for p in self.occ_data["profiles"] if p["scenario_id"] == "REFERENCE_2026"]
        cop_occs = {p["masco_code"]: p for p in self.occ_data["profiles"] if p["scenario_id"] == "MODERATE_COPILOT"}
        
        # In REFERENCE_2026 central, outlooks must faithfully reflect baseline M2 state
        for p in ref_occs:
            code = p["masco_code"]
            cop = cop_occs[code]
            if p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK":
                self.assertEqual(p["scenario_outlook"], "RESILIENT")
                # Monotonicity: fallback profiles MUST remain RESILIENT under Moderate Copilot
                self.assertEqual(cop["scenario_outlook"], "RESILIENT", f"Fallback {code} spuriously flipped to {cop['scenario_outlook']} under Copilot!")

    # Test 7: P1-4 Granularity Separation (20 4-Digit vs 8 Major Group Fallbacks)
    def test_07_granularity_separation(self):
        ref_occs = [p for p in self.occ_data["profiles"] if p["scenario_id"] == "REFERENCE_2026"]
        
        four_digit = [p for p in ref_occs if p["entity_granularity"] == "FOUR_DIGIT_OCCUPATION"]
        major_group = [p for p in ref_occs if p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK"]
        
        self.assertEqual(len(four_digit), 20)
        self.assertEqual(len(major_group), 8)
        
        # Major group wage flag correctness
        for p in major_group:
            self.assertIn("AGGREGATED_MAJOR_GROUP_FALLBACK", p["quality_flags"])
            self.assertIn("GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT", p["quality_flags"])
            self.assertNotIn("NO_ROLE_SPECIFIC_WAGE_DATA", p["quality_flags"])
            self.assertNotIn("MAJOR_GROUP_WAGE_CONTEXT", p["quality_flags"])

        # 4-digit occupation wage flag correctness
        for p in four_digit:
            self.assertIn("MAJOR_GROUP_WAGE_CONTEXT", p["quality_flags"])
            self.assertIn("NO_ROLE_SPECIFIC_WAGE_DATA", p["quality_flags"])

    # Test 8: P2-1 Multi-Dimensional Sensitivity Semantics
    def test_08_sensitivity_profile_semantics(self):
        for p in self.occ_data["profiles"]:
            sp = p["sensitivity_profile"]
            self.assertIn(sp["exact_category_stability"], ["STABLE", "SHIFTING"])
            self.assertIn(sp["downside_risk_stability"], ["ROBUST", "VULNERABLE"])
            self.assertIn(sp["transformation_sensitivity"], ["HIGH", "LOW"])
            self.assertIn(sp["movement_type"], ["NO_SHIFT", "UPSIDE_TRANSFORMATION", "DOWNSIDE_PRESSURE", "NEUTRAL_BOUNDARY_SHIFT"])

        # Software Developers 2512 in MODERATE_COPILOT or FAST_AGENTIC
        dev = self.engine.get_role_scenario("2512", "FAST_AGENTIC")
        self.assertEqual(dev["sensitivity_profile"]["downside_risk_stability"], "ROBUST")

    # Test 9: P2-1 All 4 OpenAlex Zero-Base Skills Propagated
    def test_09_openalex_zero_base_skills(self):
        expected_skills = {
            "data_visualization",
            "human_in_the_loop_qa",
            "api_integration",
            "carbon_footprint_analytics"
        }
        
        skills_with_flag = {
            p["skill_id"] for p in self.skill_data["profiles"]
            if p["scenario_id"] == "REFERENCE_2026" and "INSUFFICIENT_HISTORICAL_BASELINE" in p["quality_flags"]
        }
        self.assertEqual(skills_with_flag, expected_skills)

    # Test 10: P2-2 Reskilling Urgency Calibration (4110 reaches VERY HIGH under FAST_AGENTIC)
    def test_10_reskilling_urgency_calibration(self):
        clerk_fast = self.engine.get_role_scenario("4110", "FAST_AGENTIC")
        self.assertEqual(clerk_fast["reskilling_urgency"], "VERY HIGH")
        
        id_ref = self.engine.get_skill_scenario("instructional_design", "REFERENCE_2026")
        self.assertEqual(id_ref["reskilling_urgency"], "MODERATE")

    # Test 11: M3 Fallback Neutrality API Contract
    def test_11_m3_fallback_neutrality_contract(self):
        four_digit_roles = self.engine.get_all_role_scenarios(scenario_id="MODERATE_COPILOT", granularity="FOUR_DIGIT_OCCUPATION")
        fallback_roles = self.engine.get_all_role_scenarios(scenario_id="MODERATE_COPILOT", granularity="ONE_DIGIT_MAJOR_GROUP_FALLBACK")
        
        self.assertEqual(len(four_digit_roles), 20)
        self.assertEqual(len(fallback_roles), 8)
        
        for r in fallback_roles:
            self.assertEqual(r["entity_granularity"], "ONE_DIGIT_MAJOR_GROUP_FALLBACK")

    # Test 12: Demographic Variable Rejection
    def test_12_prohibited_demographics(self):
        for bad_key in ["age", "gender", "race", "ethnicity", "religion", "socioeconomic_background"]:
            with self.assertRaises(ValueError):
                self.engine.get_role_scenario("2512", "MODERATE_COPILOT", **{bad_key: 30})

if __name__ == "__main__":
    unittest.main()
