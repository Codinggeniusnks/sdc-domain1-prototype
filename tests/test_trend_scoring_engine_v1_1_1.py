"""Unit and regression tests for M2 Trend Intelligence Engine Version 1.1.1.

Verifies:
1. OpenAlex logarithmic baseline shrinkage formula arithmetic.
2. Transparent explanation strings (distinguishing raw vs adjusted).
3. Material score effect (low-base does not saturate at ceiling with mature topics).
4. Zero saturation at 100.0.
5. Regression safety for ILO 2025, wage granularity, confidence distribution (7/7/2/0).
"""

import json
import math
import unittest
from pathlib import Path

from src.trend_engine import TrendEngine

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
PROCESSED_DIR = BASE_DIR / "data" / "trends" / "processed"


class TestTrendScoringEngineV111(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = TrendEngine(version="v1.1.1")
        with open(PROCESSED_DIR / "skill_trend_profiles_v1_1_1.json", "r", encoding="utf-8") as f:
            cls.skill_data = json.load(f)
            cls.skill_profiles = {p["skill_id"]: p for p in cls.skill_data.get("profiles", [])}

        with open(PROCESSED_DIR / "occupation_trend_profiles_v1_1_1.json", "r", encoding="utf-8") as f:
            cls.occ_data = json.load(f)
            cls.occ_profiles = {p["occupation_code"]: p for p in cls.occ_data.get("profiles", [])}

        with open(PROCESSED_DIR / "m2_scoring_config_v1_1_1.json", "r", encoding="utf-8") as f:
            cls.scoring_config = json.load(f)

        with open(PROCESSED_DIR / "m2_confidence_config_v1_1_1.json", "r", encoding="utf-8") as f:
            cls.confidence_config = json.load(f)

    # -------------------------------------------------------------
    # 1. ARITHMETIC TESTS FOR DAMPING FORMULA
    # -------------------------------------------------------------
    def test_arithmetic_baseline_1_prompt_engineering(self):
        """Verify baseline=1, raw=17.143 produces w_vol=ln(2)/ln(26) and R_adj~4.434."""
        base = 1
        raw = 17.143
        expected_w_vol = math.log(2.0) / math.log(26.0)  # ~0.212746
        expected_r_adj = 1.0 + (raw - 1.0) * expected_w_vol  # ~4.434

        profile = self.skill_profiles["prompt_engineering"]
        self.assertAlmostEqual(profile["volume_shrinkage_weight"], round(expected_w_vol, 4), places=3)
        self.assertAlmostEqual(profile["adjusted_research_growth_ratio"], round(expected_r_adj, 3), places=2)
        self.assertAlmostEqual(profile["adjusted_research_growth_ratio"], 4.434, places=2)

    def test_arithmetic_baseline_2_workflow_automation(self):
        """Verify baseline=2, raw=18.333 produces w_vol=ln(3)/ln(26) and R_adj~6.845."""
        base = 2
        raw = 18.333
        expected_w_vol = math.log(3.0) / math.log(26.0)  # ~0.337186
        expected_r_adj = 1.0 + (raw - 1.0) * expected_w_vol  # ~6.845

        profile = self.skill_profiles["workflow_automation"]
        self.assertAlmostEqual(profile["volume_shrinkage_weight"], round(expected_w_vol, 4), places=3)
        self.assertAlmostEqual(profile["adjusted_research_growth_ratio"], round(expected_r_adj, 3), places=2)

    def test_arithmetic_baseline_14_ai_literacy(self):
        """Verify baseline=14, raw=11.204 produces w_vol=ln(15)/ln(26) and R_adj~9.481."""
        base = 14
        raw = 11.204
        expected_w_vol = math.log(15.0) / math.log(26.0)  # ~0.831189
        expected_r_adj = 1.0 + (raw - 1.0) * expected_w_vol  # ~9.481

        profile = self.skill_profiles["ai_literacy"]
        self.assertAlmostEqual(profile["volume_shrinkage_weight"], round(expected_w_vol, 4), places=3)
        self.assertAlmostEqual(profile["adjusted_research_growth_ratio"], round(expected_r_adj, 3), places=2)

    # -------------------------------------------------------------
    # 2. EXPLANATION TESTS (ISSUE 1 RESOLUTION)
    # -------------------------------------------------------------
    def test_explanation_distinguishes_raw_and_adjusted(self):
        """Assert that prompt_engineering explanation distinguishes raw vs adjusted and does not mislabel raw as damped."""
        profile = self.skill_profiles["prompt_engineering"]
        oalex_driver = next(d for d in profile["top_positive_drivers"] if d["source_id"] == "SRC-OPENALEX-TEMPORAL")
        summary = oalex_driver["summary"]

        # Must not say '17.1x volume-damped' or '17.1x volume-adjusted'
        self.assertNotIn("17.1x volume-damped", summary)
        self.assertNotIn("17.1x (18 papers in 2024-2026 vs 1 baseline, volume-damped)", summary)

        # Must explicitly contain transparent explanation
        self.assertIn("Raw publication growth: 17.1x", summary)
        self.assertIn("low-base adjusted research momentum ratio: 4.4x", summary)
        self.assertIn("based on 1 baseline publication and 18 recent publications", summary)

    def test_explanation_mature_high_volume(self):
        """Assert that high-volume skills explain volume adjustment transparently."""
        profile = self.skill_profiles["ai_literacy"]
        oalex_driver = next(d for d in profile["top_positive_drivers"] if d["source_id"] == "SRC-OPENALEX-TEMPORAL")
        summary = oalex_driver["summary"]

        self.assertIn("Raw publication growth: 11.2x", summary)
        self.assertIn("volume-adjusted research momentum ratio: 9.5x", summary)
        self.assertIn("based on 14 baseline publications and 121 recent publications", summary)

    # -------------------------------------------------------------
    # 3. FINAL SCORE EFFECT TESTS (ISSUE 3 RESOLUTION)
    # -------------------------------------------------------------
    def test_material_score_effect_of_low_base_damping(self):
        """Assert low-base prompt_engineering does not saturate at identical ceiling with mature ai_literacy."""
        pe_profile = self.skill_profiles["prompt_engineering"]
        ai_profile = self.skill_profiles["ai_literacy"]

        pe_score = pe_profile["research_momentum_index"]
        ai_score = ai_profile["research_momentum_index"]

        # In v1.1.0, both were 95.0. In v1.1.1, low-base must have a material gap.
        self.assertNotEqual(pe_score, ai_score)
        self.assertEqual(pe_score, 75.4)
        self.assertEqual(ai_score, 88.7)
        self.assertGreater(ai_score - pe_score, 10.0, "Material gap should exceed 10.0 points.")

    def test_low_base_raw_18x_does_not_equal_mature_18x(self):
        """Verify that a 1-baseline 18x growth receives a lower score than a hypothetical mature 18x growth."""
        pe_score = self.skill_profiles["prompt_engineering"]["research_momentum_index"]
        # Theoretical mature 18x (w_vol=1.0 -> R_adj=18.0)
        mature_score = round(50.0 + 44.0 * (1.0 - math.exp(-(18.0 - 1.0) / 4.0)), 1)  # ~93.4
        self.assertLess(pe_score, mature_score - 15.0)

    # -------------------------------------------------------------
    # 4. SATURATION ELIMINATION AUDIT
    # -------------------------------------------------------------
    def test_zero_components_saturated_at_100(self):
        """Confirm that zero components across all skills hit 100.0 saturation."""
        for p in self.skill_profiles.values():
            for key in ["demand_shortage_index", "demand_momentum_index", "research_momentum_index", "policy_priority_index", "confidence_index"]:
                val = p.get(key)
                if val is not None:
                    self.assertLess(val, 100.0, f"Skill {p['skill_id']}.{key} is saturated at 100.0!")

    # -------------------------------------------------------------
    # 5. REGRESSION SAFETY AUDITS
    # -------------------------------------------------------------
    def test_confidence_distribution_authentic_variation_preserved(self):
        """Verify 7 HIGH, 7 MEDIUM, 2 LOW confidence distribution is preserved."""
        tiers = [p["confidence_label"] for p in self.skill_profiles.values()]
        self.assertEqual(tiers.count("HIGH"), 7)
        self.assertEqual(tiers.count("MEDIUM"), 7)
        self.assertEqual(tiers.count("LOW"), 2)
        self.assertEqual(tiers.count("INSUFFICIENT"), 0)

    def test_low_base_flag_preserved(self):
        """Verify LOW_BASE_RESEARCH_SIGNAL is preserved for baseline < 5."""
        pe_flags = self.skill_profiles["prompt_engineering"]["quality_flags"]
        rag_flags = self.skill_profiles["rag_knowledge_systems"]["quality_flags"]
        ai_flags = self.skill_profiles["ai_literacy"]["quality_flags"]

        self.assertIn("LOW_BASE_RESEARCH_SIGNAL", pe_flags)
        self.assertIn("LOW_BASE_RESEARCH_SIGNAL", rag_flags)
        self.assertNotIn("LOW_BASE_RESEARCH_SIGNAL", ai_flags)

    def test_ilo_wp140_benchmark_active(self):
        """Verify active benchmark remains ILO WP 140 (2025)."""
        self.assertEqual(self.scoring_config["active_benchmark"], "ILO_WP140_2025")
        self.assertIn("ILO_WP96_2023", self.scoring_config["supported_benchmarks"])

    def test_wage_granularity_metadata_present_on_all_occupations(self):
        """Verify all 20 four-digit occupations retain MAJOR_GROUP_CONTEXT."""
        four_digit = [p for p in self.occ_profiles.values() if len(p["occupation_code"]) == 4]
        self.assertEqual(len(four_digit), 20)
        for p in four_digit:
            self.assertEqual(p["wage_granularity"], "MAJOR_GROUP_CONTEXT")
            self.assertIn("MAJOR_GROUP_WAGE_CONTEXT", p["quality_flags"])
            self.assertIn("NO_ROLE_SPECIFIC_WAGE_DATA", p["quality_flags"])

    def test_conflict_status_preserved(self):
        """Verify conflict classification on key occupations."""
        soft_dev = self.occ_profiles["2512"]
        admin_sec = self.occ_profiles["3343"]
        clerk = self.occ_profiles["4110"]

        self.assertEqual(soft_dev["conflict_status"], "CROSS_DIMENSION_TENSION")
        self.assertEqual(soft_dev["overall_outlook"], "STRONGLY RISING")
        self.assertEqual(admin_sec["overall_outlook"], "DECLINING")
        self.assertEqual(clerk["overall_outlook"], "STRONGLY DECLINING")


if __name__ == "__main__":
    unittest.main()
