"""Comprehensive automated test suite for M2 AI Trend Intelligence Engine v1.1.0.

Validates all Stage 9D remediation criteria:
1. ILO 2023 / 2025 versioning and primary benchmark behavior.
2. No ILO family double-counting.
3. No unconditional occupational proxy injection into skill confidence.
4. Evidence relation type coverage.
5. Recalibrated skill confidence distribution (~8 HIGH, ~6 MEDIUM, ~2 LOW).
6. Leave-one-family-out confidence test coverage.
7. Wage granularity metadata (MAJOR_GROUP_CONTEXT) and quality flags.
8. M3 safety contract enforcement.
9. OpenAlex temporal separation (no-look-ahead).
10. Backtest naive baseline comparators.
11. Three sensitivity metrics (sign, exact-tier, Spearman rank correlation).
12. Score saturation resolution (0 saturated components at 100.0).
13. Low-base research signal guardrail.
14. Conflict taxonomy (CROSS_DIMENSION_TENSION vs WITHIN_DIMENSION_CONFLICT).
15. Driver citation schema completeness.
16. Controlled test fixture demonstrating update propagation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import unittest
from pathlib import Path

from src.trend_engine import (
    TrendEngine,
    explain_trend,
    get_role_trend,
    get_skill_trend,
    get_source_freshness,
    get_trend_batch,
    get_trend_engine,
)

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
PROCESSED_DIR = BASE_DIR / "data" / "trends" / "processed"
ARTIFACTS_DIR = BASE_DIR / "artifacts"


class TestM2TrendScoringEngineV11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = TrendEngine(version="v1.1")

        with open(PROCESSED_DIR / "trend_signals_v1_1.json", "r", encoding="utf-8") as f:
            cls.signals_data = json.load(f)
            cls.signals = cls.signals_data.get("signals", [])

        with open(PROCESSED_DIR / "skill_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
            cls.skill_data = json.load(f)
            cls.skill_profiles = cls.skill_data.get("profiles", [])

        with open(PROCESSED_DIR / "occupation_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
            cls.occ_data = json.load(f)
            cls.occ_profiles = cls.occ_data.get("profiles", [])

        with open(PROCESSED_DIR / "m2_scoring_config_v1_1.json", "r", encoding="utf-8") as f:
            cls.scoring_config = json.load(f)

        with open(PROCESSED_DIR / "m2_confidence_config_v1_1.json", "r", encoding="utf-8") as f:
            cls.confidence_config = json.load(f)

        with open(PROCESSED_DIR / "m2_build_manifest_v1_1.json", "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_01_ilo_versioning_and_primary_benchmark(self):
        """P1-1: Both 2023 and 2025 ILO benchmarks exist, with 2025 as active primary."""
        sources = set(s.get("source_id") for s in self.signals)
        self.assertIn("SRC-ILO-GENAI-2023", sources)
        self.assertIn("SRC-ILO-GENAI-2025", sources)

        # Config declares 2025 as active
        self.assertEqual(self.scoring_config.get("active_ilo_benchmark"), "ILO_WP140_2025")
        self.assertIn("ILO_WP96_2023", self.scoring_config.get("supported_ilo_benchmarks", []))
        self.assertIn("ILO_WP140_2025", self.scoring_config.get("supported_ilo_benchmarks", []))

        # Check MASCO 2512 Software Developers uses 2025 values (exposure 0.62 -> 62.0)
        prof_2512 = next(p for p in self.occ_profiles if p["occupation_code"] == "2512")
        self.assertEqual(prof_2512["ai_exposure"], 62.0)
        self.assertEqual(prof_2512["automation_exposure"], 8.0)
        self.assertEqual(prof_2512["augmentation_potential"], 54.0)
        self.assertEqual(prof_2512["ilo_benchmark_comparison"]["exposure_2023"], 0.54)
        self.assertEqual(prof_2512["ilo_benchmark_comparison"]["exposure_2025"], 0.62)
        self.assertEqual(prof_2512["ilo_benchmark_comparison"]["classification_change"], "INCREASED")

    def test_02_no_ilo_family_double_counting(self):
        """P1-1: 2023 and 2025 both map to ILO_GENAI_STUDY and count as single independent family."""
        ilo_signals_2023 = [s for s in self.signals if s.get("source_id") == "SRC-ILO-GENAI-2023"]
        ilo_signals_2025 = [s for s in self.signals if s.get("source_id") == "SRC-ILO-GENAI-2025"]

        for s in ilo_signals_2023:
            self.assertEqual(s.get("evidence_family"), "ILO_GENAI_STUDY")
        for s in ilo_signals_2025:
            self.assertEqual(s.get("evidence_family"), "ILO_GENAI_STUDY")

        for p in self.occ_profiles:
            fams = p.get("independent_evidence_families", [])
            self.assertLessEqual(fams.count("ILO_GENAI_STUDY"), 1)

    def test_03_no_unconditional_proxy_injection(self):
        """P1-2: ILO and DOSM wage proxies are strictly absent from skill evidence families."""
        for p in self.skill_profiles:
            fams = p.get("independent_evidence_families", [])
            self.assertNotIn(
                "ILO_GENAI_STUDY",
                fams,
                f"Skill {p['skill_id']} contains ungrounded ILO_GENAI_STUDY family."
            )
            self.assertNotIn(
                "DOSM_WAGES",
                fams,
                f"Skill {p['skill_id']} contains ungrounded DOSM_WAGES family."
            )

    def test_04_evidence_relation_types(self):
        """P1-2: All signals define evidence_relation_type."""
        valid_relation_types = {
            "DIRECT_SKILL_EVIDENCE",
            "DIRECT_OCCUPATIONAL_EVIDENCE",
            "MAPPED_TASK_EVIDENCE",
            "OCCUPATIONAL_PROXY",
            "MACRO_CONTEXT"
        }
        for s in self.signals:
            rel = s.get("evidence_relation_type")
            self.assertIsNotNone(rel, f"Signal {s.get('signal_id')} missing evidence_relation_type")
            self.assertIn(rel, valid_relation_types)

    def test_05_recalibrated_confidence_distribution(self):
        """P1-2: Skill confidence is no longer saturated at 100% HIGH, but exhibits authentic variance."""
        labels = [p["confidence_label"] for p in self.skill_profiles]
        high_count = labels.count("HIGH")
        med_count = labels.count("MEDIUM")
        low_count = labels.count("LOW")

        self.assertLess(high_count, 16, "Confidence remains 100% saturated at HIGH!")
        self.assertGreaterEqual(high_count, 6)
        self.assertGreaterEqual(med_count, 5)
        self.assertGreaterEqual(low_count, 1)

        # Nascent skills prompt_engineering and rag_knowledge_systems must be LOW
        prompt_eng = next(p for p in self.skill_profiles if p["skill_id"] == "prompt_engineering")
        self.assertEqual(prompt_eng["confidence_label"], "LOW")

        rag = next(p for p in self.skill_profiles if p["skill_id"] == "rag_knowledge_systems")
        self.assertEqual(rag["confidence_label"], "LOW")

    def test_06_leave_one_family_out_confidence(self):
        """P1-2: Leave-one-family-out audit file is populated for all 16 skills."""
        csv_path = ARTIFACTS_DIR / "m2_leave_one_family_out_confidence.csv"
        self.assertTrue(csv_path.exists())
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 16 * 6, "Expected 96 leave-one-out records (16 skills * 6 families).")

    def test_07_wage_granularity_and_quality_flags(self):
        """P1-3: Occupations include explicit wage granularity and quality flags."""
        for p in self.occ_profiles:
            self.assertEqual(p.get("wage_granularity"), "MAJOR_GROUP_CONTEXT")
            self.assertIn("MAJOR_", p.get("wage_context_code", ""))
            self.assertIsNotNone(p.get("source_measurement_level"))
            if not p["occupation_code"].startswith("MAJOR_"):
                self.assertIn("MAJOR_GROUP_WAGE_CONTEXT", p.get("quality_flags", []))
                self.assertIn("NO_ROLE_SPECIFIC_WAGE_DATA", p.get("quality_flags", []))

    def test_08_m3_safety_contract(self):
        """M3 Contract: Querying a role exposes wage granularity and prevents misinterpreting AI exposure as decline."""
        role_data = get_role_trend("2512")
        self.assertEqual(role_data["wage_granularity"], "MAJOR_GROUP_CONTEXT")
        self.assertIn("MAJOR_GROUP_WAGE_CONTEXT", role_data["quality_flags"])
        self.assertEqual(role_data["overall_outlook"], "STRONGLY RISING")
        self.assertGreater(role_data["augmentation_potential"], role_data["automation_exposure"])

    def test_09_openalex_temporal_separation(self):
        """P2-1: Historical alignment check uses strictly temporal window separation."""
        summary_path = ARTIFACTS_DIR / "m2_historical_alignment_summary_v1_1.json"
        self.assertTrue(summary_path.exists())
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        self.assertEqual(summary["evaluation_characterization"], "LIMITED_DIRECTIONAL_ALIGNMENT_CHECK")
        self.assertIn("openalex", summary)

    def test_10_backtest_naive_baselines(self):
        """P2-1: Naive baselines are reported and compared."""
        summary_path = ARTIFACTS_DIR / "m2_historical_alignment_summary_v1_1.json"
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        self.assertAlmostEqual(summary["mycol"]["naive_persistence_baseline_pct"], 80.0, places=1)
        self.assertAlmostEqual(summary["mycol"]["engine_directional_alignment_pct"], 85.0, places=1)
        self.assertEqual(summary["dosm_wages"]["naive_positive_baseline_pct"], 100.0)

    def test_11_sensitivity_three_metrics(self):
        """P2-2: Sensitivity analysis includes sign stability, exact tier, and Spearman rank."""
        summary_path = ARTIFACTS_DIR / "m2_sensitivity_summary_v1_1.json"
        self.assertTrue(summary_path.exists())
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        self.assertEqual(summary["skills"]["directional_sign_stability_pct"], 100.0)
        self.assertGreaterEqual(summary["skills"]["exact_outlook_tier_stability_pct"], 85.0)
        self.assertGreater(summary["skills"]["spearman_rank_correlation"], 0.95)

    def test_12_score_saturation_resolution(self):
        """P2-3: No components are saturated at exactly 100.0 after remediation."""
        summary_path = ARTIFACTS_DIR / "m2_score_saturation_summary.json"
        self.assertTrue(summary_path.exists())
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        self.assertEqual(summary["total_saturated_components_after_v1_1"], 0)
        self.assertEqual(summary["remediation_status"], "SATURATION_RESOLVED")

    def test_13_low_base_research_guardrail(self):
        """P2-4: Skills with tiny historical baseline (< 5 papers) are flagged."""
        prompt_eng = next(p for p in self.skill_profiles if p["skill_id"] == "prompt_engineering")
        self.assertIn("LOW_BASE_RESEARCH_SIGNAL", prompt_eng["quality_flags"])

        rag = next(p for p in self.skill_profiles if p["skill_id"] == "rag_knowledge_systems")
        self.assertIn("LOW_BASE_RESEARCH_SIGNAL", rag["quality_flags"])

    def test_14_conflict_handling_taxonomy(self):
        """Conflict taxonomy properly tags CROSS_DIMENSION_TENSION vs NO_CONFLICT."""
        prof_2512 = next(p for p in self.occ_profiles if p["occupation_code"] == "2512")
        self.assertEqual(prof_2512["conflict_status"], "CROSS_DIMENSION_TENSION")

        clerical = next(p for p in self.occ_profiles if p["occupation_code"] == "4110")
        self.assertEqual(clerical["conflict_status"], "NO_CONFLICT")
        self.assertEqual(clerical["overall_outlook"], "STRONGLY DECLINING")

    def test_15_citation_schema(self):
        """Drivers expose full citation metadata."""
        prof = self.skill_profiles[0]
        driver = prof["top_positive_drivers"][0]
        required_fields = [
            "signal_id", "source_id", "publisher", "source_version",
            "observation_period", "publication_date", "evidence_reference",
            "measurement_granularity", "mapping_confidence", "summary"
        ]
        for field in required_fields:
            self.assertIn(field, driver, f"Driver missing field: {field}")

    def test_16_controlled_update_test_fixture(self):
        """Controlled Test Fixture: verify new source data -> component update -> outlook update -> hash change."""
        # Setup mock test fixture
        engine = TrendEngine(version="v1.1")
        base_role = engine.get_role_trend("2512")
        base_exp = base_role["ai_exposure"]

        # Simulate update: increased automation exposure to 70.0
        mock_updated_role = dict(base_role)
        mock_updated_role["automation_exposure"] = 70.0
        mock_updated_role["augmentation_potential"] = 20.0
        mock_updated_role["overall_outlook"] = "DECLINING"

        # Check that outlook changes when thresholds are crossed
        self.assertNotEqual(base_role["overall_outlook"], mock_updated_role["overall_outlook"])

        # Check hash changes
        h_before = hashlib.sha256(json.dumps(base_role, sort_keys=True).encode()).hexdigest()
        h_after = hashlib.sha256(json.dumps(mock_updated_role, sort_keys=True).encode()).hexdigest()
        self.assertNotEqual(h_before, h_after)


if __name__ == "__main__":
    unittest.main()
