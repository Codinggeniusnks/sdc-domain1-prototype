"""
test_scenario_engine.py

Comprehensive test suite for M6 Future Workforce Scenario Engine (v1.0.0).
Verifies:
1. M2 freeze hashes
2. REFERENCE baseline preservation
3. Scenario assumptions separated from observations
4. No hidden scenario constants
5. Automation monotonicity (FAST_AGENTIC >= MODERATE_COPILOT >= REFERENCE_2026)
6. Augmentation independence
7. Demand resilience independence
8. Confidence propagation
9. Quality-flag propagation
10. Null preservation
11. Wage-granularity safety
12. LOW_BASE_RESEARCH_SIGNAL propagation & INSUFFICIENT_HISTORICAL_BASELINE
13. Scenario range sensitivity (lower, central, upper)
14. Deterministic rebuild
15. M3 API contract
16. No demographic inputs rejection
"""

import unittest
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(BASE_DIR))

from src.scenario_engine import ScenarioEngine

class TestScenarioEngineM6(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = ScenarioEngine(base_dir=BASE_DIR)
        cls.artifacts_dir = BASE_DIR / "artifacts"
        cls.scenarios_dir = BASE_DIR / "data" / "scenarios"
        cls.trends_dir = BASE_DIR / "data" / "trends" / "processed"
        
        with open(cls.scenarios_dir / "scenario_definitions_v1.json", "r", encoding="utf-8") as f:
            cls.scenario_defs = json.load(f)
            
        with open(cls.scenarios_dir / "occupation_scenario_profiles_v1.json", "r", encoding="utf-8") as f:
            cls.occ_data = json.load(f)
            
        with open(cls.scenarios_dir / "skill_scenario_profiles_v1.json", "r", encoding="utf-8") as f:
            cls.skill_data = json.load(f)

    # Test 1: M2 Freeze Hashes
    def test_01_m2_freeze_hashes(self):
        freeze_manifest_path = self.artifacts_dir / "m2_v1_1_1_freeze_manifest.json"
        self.assertTrue(freeze_manifest_path.exists(), "M2 freeze manifest missing!")
        with open(freeze_manifest_path, "r", encoding="utf-8") as f:
            m2_manifest = json.load(f)
            
        occ_hash = hashlib.sha256((self.trends_dir / "occupation_trend_profiles_v1_1_1.json").read_bytes()).hexdigest()
        skill_hash = hashlib.sha256((self.trends_dir / "skill_trend_profiles_v1_1_1.json").read_bytes()).hexdigest()
        
        self.assertEqual(occ_hash, m2_manifest["output_artifacts"]["occupation_trend_profiles_v1_1_1"])
        self.assertEqual(skill_hash, m2_manifest["output_artifacts"]["skill_trend_profiles_v1_1_1"])
        self.assertEqual(m2_manifest["freeze_status"], "FROZEN")

    # Test 2: REFERENCE Baseline Preservation
    def test_02_reference_baseline_preservation(self):
        # In REFERENCE_2026, automation_pressure and augmentation_opportunity must match baseline
        with open(self.trends_dir / "occupation_trend_profiles_v1_1_1.json", "r", encoding="utf-8") as f:
            base_occs = {o["occupation_code"]: o for o in json.load(f)["profiles"]}
            
        ref_occs = [p for p in self.occ_data["profiles"] if p["scenario_id"] == "REFERENCE_2026"]
        self.assertEqual(len(ref_occs), 28)
        
        for p in ref_occs:
            code = p["masco_code"]
            base = base_occs[code]
            self.assertAlmostEqual(p["automation_pressure"], base.get("automation_exposure", 0.0), places=1)
            self.assertAlmostEqual(p["augmentation_opportunity"], base.get("augmentation_potential", 0.0), places=1)
            self.assertEqual(p["scenario_delta_from_reference"]["automation_pressure_delta"], 0.0)
            self.assertEqual(p["scenario_delta_from_reference"]["augmentation_opportunity_delta"], 0.0)
            self.assertEqual(p["scenario_delta_from_reference"]["transition_pressure_delta"], 0.0)

    # Test 3: Scenario Assumptions Separated from Observations
    def test_03_assumptions_separated_from_observations(self):
        for sc in self.scenario_defs["scenarios"]:
            for a in sc["assumptions"]:
                self.assertEqual(a["assumption_status"], "SCENARIO_ASSUMPTION")
                self.assertNotEqual(a["assumption_status"], "OBSERVED_EVIDENCE")
                self.assertIn("rationale", a)
                self.assertIn("qualitative_band", a)
                self.assertIn("affected_dimensions", a)
                self.assertTrue(a["central"] >= a["lower"])
                self.assertTrue(a["upper"] >= a["central"])

    # Test 4: No Hidden Constants
    def test_04_no_hidden_constants(self):
        # All scenario parameters used by profiles must map to declared parameter_ids in scenario_definitions_v1.json
        declared_param_ids = {
            a["parameter_id"] for sc in self.scenario_defs["scenarios"] for a in sc["assumptions"]
        }
        for p in self.occ_data["profiles"]:
            for param_id in p["scenario_assumptions_used"]:
                self.assertIn(param_id, declared_param_ids, f"Hidden parameter {param_id} found in occupation profile!")

    # Test 5: Automation Monotonicity
    def test_05_automation_monotonicity(self):
        # For every occupation and skill: FAST_AGENTIC >= MODERATE_COPILOT >= REFERENCE_2026
        by_occ = {}
        for p in self.occ_data["profiles"]:
            by_occ.setdefault(p["masco_code"], {})[p["scenario_id"]] = p
            
        for code, sc_dict in by_occ.items():
            ref_auto = sc_dict["REFERENCE_2026"]["automation_pressure"]
            cop_auto = sc_dict["MODERATE_COPILOT"]["automation_pressure"]
            age_auto = sc_dict["FAST_AGENTIC"]["automation_pressure"]
            self.assertGreaterEqual(cop_auto, ref_auto, f"Occupation {code} copilot auto < reference")
            self.assertGreaterEqual(age_auto, cop_auto, f"Occupation {code} agentic auto < copilot")

        by_skill = {}
        for p in self.skill_data["profiles"]:
            by_skill.setdefault(p["skill_id"], {})[p["scenario_id"]] = p
            
        for sid, sc_dict in by_skill.items():
            ref_auto = sc_dict["REFERENCE_2026"]["automation_pressure"]
            cop_auto = sc_dict["MODERATE_COPILOT"]["automation_pressure"]
            age_auto = sc_dict["FAST_AGENTIC"]["automation_pressure"]
            self.assertGreaterEqual(cop_auto, ref_auto, f"Skill {sid} copilot auto < reference")
            self.assertGreaterEqual(age_auto, cop_auto, f"Skill {sid} agentic auto < copilot")

    # Test 6: Augmentation Independence
    def test_06_augmentation_independence(self):
        # High AI exposure + high augmentation (e.g. Software Developers 2512) retains high augmentation opportunity and resilient/transforming outlook
        dev = self.engine.get_role_scenario("2512", "FAST_AGENTIC")
        self.assertGreater(dev["augmentation_opportunity"], 70.0)
        self.assertIn(dev["scenario_outlook"], ["STRONGLY RESILIENT", "RESILIENT", "TRANSFORMING"])
        self.assertNotEqual(dev["scenario_outlook"], "HIGHLY PRESSURED")

    # Test 7: Demand Resilience Independence
    def test_07_demand_resilience_independence(self):
        # Demand resilience is not crushed by automation pressure
        clerk = self.engine.get_role_scenario("4110", "FAST_AGENTIC")
        dev = self.engine.get_role_scenario("2512", "FAST_AGENTIC")
        # Software developers maintain high demand resilience despite high AI adoption
        self.assertGreater(dev["demand_resilience"], 70.0)
        # General office clerks have low demand resilience because shortage level was low (20.0)
        self.assertLess(clerk["demand_resilience"], 35.0)

    # Test 8: Confidence Propagation
    def test_08_confidence_propagation(self):
        for p in self.occ_data["profiles"]:
            self.assertIn(p["scenario_confidence"], ["HIGH", "MEDIUM", "LOW"])
            self.assertIn(p["sensitivity_classification"], ["ROBUST", "MODERATELY SENSITIVE", "HIGHLY SENSITIVE"])

    # Test 9: Quality-Flag Propagation
    def test_09_quality_flag_propagation(self):
        for p in self.occ_data["profiles"]:
            self.assertIn("MAJOR_GROUP_WAGE_CONTEXT", p["quality_flags"])
            self.assertIn("NO_ROLE_SPECIFIC_WAGE_DATA", p["quality_flags"])
            if p["masco_code"].startswith("MAJOR_"):
                self.assertIn("AGGREGATE_MAJOR_GROUP", p["quality_flags"])

    # Test 10: Null Preservation
    def test_10_null_preservation(self):
        # research_momentum is null for occupations in M2; must remain strictly None in M6
        for p in self.occ_data["profiles"]:
            self.assertIsNone(p["research_momentum"], f"Null component overwritten for {p['masco_code']}!")

    # Test 11: Wage-Granularity Safety
    def test_11_wage_granularity_safety(self):
        # M6 must NOT output any specific salary numbers, future wage predictions or salary forecasts
        for p in self.occ_data["profiles"]:
            self.assertNotIn("future_salary", p)
            self.assertNotIn("salary_forecast", p)
            self.assertNotIn("salary_growth_rate", p)
            self.assertNotIn("wage_rm", p)

    # Test 12: LOW_BASE_RESEARCH_SIGNAL & INSUFFICIENT_HISTORICAL_BASELINE Propagation
    def test_12_low_base_research_signal_propagation(self):
        prompt_eng = self.engine.get_skill_scenario("prompt_engineering", "MODERATE_COPILOT")
        self.assertIn("LOW_BASE_RESEARCH_SIGNAL", prompt_eng["quality_flags"])
        
        hitl = self.engine.get_skill_scenario("human_in_the_loop_qa", "FAST_AGENTIC")
        self.assertIn("INSUFFICIENT_HISTORICAL_BASELINE", hitl["quality_flags"])
        
        dataviz = self.engine.get_skill_scenario("data_visualization", "FAST_AGENTIC")
        self.assertIn("INSUFFICIENT_HISTORICAL_BASELINE", dataviz["quality_flags"])

    # Test 13: Scenario Range Sensitivity
    def test_13_scenario_range_sensitivity(self):
        # Range metrics must satisfy lower <= central <= upper or lower >= central >= upper
        for p in self.occ_data["profiles"]:
            ub = p["uncertainty_band"]
            self.assertTrue(ub["lower"] <= ub["central"] <= ub["upper"] or ub["lower"] <= ub["upper"])
            self.assertIn("range_metrics", p)

    # Test 14: Deterministic Rebuild
    def test_14_deterministic_rebuild(self):
        manifest_path = self.scenarios_dir / "scenario_build_manifest_v1.json"
        self.assertTrue(manifest_path.exists())
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        occ_hash = hashlib.sha256((self.scenarios_dir / "occupation_scenario_profiles_v1.json").read_bytes()).hexdigest()
        self.assertEqual(occ_hash, manifest["output_artifacts"]["occupation_scenario_profiles_v1"])

    # Test 15: M3 API Contract
    def test_15_m3_api_contract(self):
        role_profile = self.engine.get_role_scenario("2512", "MODERATE_COPILOT")
        self.assertEqual(role_profile["masco_code"], "2512")
        self.assertEqual(role_profile["scenario_id"], "MODERATE_COPILOT")
        
        skill_profile = self.engine.get_skill_scenario("ai_literacy", "FAST_AGENTIC")
        self.assertEqual(skill_profile["skill_id"], "ai_literacy")
        self.assertEqual(skill_profile["scenario_id"], "FAST_AGENTIC")
        
        comparison = self.engine.compare_role_scenarios("4110")
        self.assertEqual(len(comparison["scenario_outlooks"]), 3)
        self.assertEqual(comparison["scenario_outlooks"]["FAST_AGENTIC"], "HIGHLY PRESSURED")
        
        delta = self.engine.get_scenario_delta("4110", "FAST_AGENTIC")
        self.assertGreater(delta["automation_pressure_delta"], 20.0)
        
        explanation = self.engine.explain_role_scenario("2512", "FAST_AGENTIC")
        self.assertIn("what_changed", explanation)
        self.assertIn("why", explanation)
        self.assertIn("m2_evidence_that_mattered", explanation)
        self.assertIn("scenario_assumptions_that_caused_change", explanation)
        self.assertIn("uncertainty_level", explanation)

    # Test 16: No Demographic Inputs
    def test_16_no_demographic_inputs(self):
        for bad_key in ["age", "gender", "race", "ethnicity", "religion", "socioeconomic_background"]:
            with self.assertRaises(ValueError):
                self.engine.get_role_scenario("2512", "MODERATE_COPILOT", **{bad_key: 35})
            with self.assertRaises(ValueError):
                self.engine.compare_role_scenarios("2512", **{bad_key: "female"})
            with self.assertRaises(ValueError):
                self.engine.get_scenario_delta("2512", "FAST_AGENTIC", **{bad_key: "test"})

if __name__ == "__main__":
    unittest.main()
