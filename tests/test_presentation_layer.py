"""
Unit Tests for O3 Multilingual & Low-Bandwidth Presentation Layer
Module: tests/test_presentation_layer.py
"""

import unittest
import os
import sys

# Ensure UTF-8 output encoding for Windows compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.presentation_layer import PresentationLayer


class TestPresentationLayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = PresentationLayer()

    def test_01_locales_initialization(self):
        """Verifies that all 3 supported locales are registered."""
        self.assertEqual(self.engine.supported_locales, ["en", "ms", "zh-CN"])
        self.assertEqual(self.engine.default_locale, "en")
        self.assertEqual(self.engine.fallback_locale, "en")
        self.assertIn("en", self.engine.catalogs)
        self.assertIn("ms", self.engine.catalogs)
        self.assertIn("zh-CN", self.engine.catalogs)

    def test_02_100_percent_key_parity(self):
        """Forensic check: EN, MS, and ZH-CN must have 100% key parity with zero missing keys."""
        report = self.engine.validate_key_parity()
        self.assertTrue(report["is_clean"], f"Key parity failed: {report['discrepancies']}")
        self.assertEqual(report["status"], "PASS")
        self.assertGreater(report["total_canonical_keys"], 100)
        self.assertEqual(
            report["locale_key_counts"]["en"],
            report["locale_key_counts"]["ms"]
        )
        self.assertEqual(
            report["locale_key_counts"]["en"],
            report["locale_key_counts"]["zh-CN"]
        )

    def test_03_translation_resolution_en(self):
        """Verifies English translations resolve accurately."""
        self.engine.set_locale("en")
        self.assertEqual(self.engine.t("nav.overview"), "System Overview")
        self.assertEqual(self.engine.t("nav.matching"), "Career Matching")
        self.assertEqual(self.engine.t("common.tiers.core"), "Core Requirement")

    def test_04_translation_resolution_ms(self):
        """Verifies Bahasa Melayu translations resolve accurately."""
        self.engine.set_locale("ms")
        self.assertEqual(self.engine.t("nav.overview"), "Gambaran Keseluruhan")
        self.assertEqual(self.engine.t("nav.matching"), "Padanan Kerjaya")
        self.assertEqual(self.engine.t("common.tiers.core"), "Keperluan Teras")

    def test_05_translation_resolution_zh(self):
        """Verifies Simplified Chinese translations resolve accurately."""
        self.engine.set_locale("zh-CN")
        self.assertEqual(self.engine.t("nav.overview"), "系统总览")
        self.assertEqual(self.engine.t("nav.matching"), "职业匹配")
        self.assertEqual(self.engine.t("common.tiers.core"), "核心必修能力")

    def test_06_fallback_behavior(self):
        """Verifies safe fallback to English or default string on missing keys."""
        self.engine.set_locale("ms")
        # Non-existent key should return fallback default
        result = self.engine.t("non.existent.key", default="Custom Fallback")
        self.assertEqual(result, "Custom Fallback")
        # Invalid locale code falls back to default
        active = self.engine.set_locale("invalid-locale")
        self.assertEqual(active, "en")

    def test_07_formatting_utilities(self):
        """Verifies number and Malaysian currency formatting."""
        self.assertEqual(self.engine.format_number(123.456, 2), "123.46")
        self.assertEqual(self.engine.format_currency(5200.5), "RM 5,200.50")
        self.assertEqual(self.engine.format_currency(1000000), "RM 1,000,000.00")

    def test_08_mathematical_invariance_clean(self):
        """Verifies that cross-language rendering preserves bit-exact mathematical equality."""
        payload_en = {
            "target_role": "Software Developers",
            "masco_code": "2512",
            "fit_score": 87.45,
            "gap_priority_index": 72.10,
            "core_gaps": ["ai_literacy", "cloud_architecture"],
            "reskilling_hours": 120.0
        }
        # In Malay, only human label might differ, numbers and codes MUST be identical
        payload_ms = {
            "target_role": "Pembangun Perisian",
            "masco_code": "2512",
            "fit_score": 87.45,
            "gap_priority_index": 72.10,
            "core_gaps": ["ai_literacy", "cloud_architecture"],
            "reskilling_hours": 120.0
        }
        is_invariant, violations = self.engine.verify_mathematical_invariance(payload_en, payload_ms)
        self.assertTrue(is_invariant, f"Invariance violations: {violations}")
        self.assertEqual(len(violations), 0)

    def test_09_mathematical_invariance_violation_catch(self):
        """Verifies that mathematical mutations across language versions are caught immediately."""
        payload_en = {
            "masco_code": "2512",
            "fit_score": 87.45,
            "gap_priority_index": 72.10
        }
        # Mutate score by 0.01
        payload_mutated = {
            "masco_code": "2512",
            "fit_score": 87.46,
            "gap_priority_index": 72.10
        }
        is_invariant, violations = self.engine.verify_mathematical_invariance(payload_en, payload_mutated)
        self.assertFalse(is_invariant)
        self.assertTrue(any("Numeric variance" in v for v in violations))

    def test_10_masco_code_mutation_catch(self):
        """Verifies that accidental translation or mutation of MASCO code is caught."""
        payload_en = {"masco_code": "2512", "fit_score": 90.0}
        payload_translated_code = {"masco_code": "2512-BM", "fit_score": 90.0}
        is_invariant, violations = self.engine.verify_mathematical_invariance(payload_en, payload_translated_code)
        self.assertFalse(is_invariant)
        self.assertTrue(any("Code string mutation" in v for v in violations))

    def test_11_low_bandwidth_payload_pruning(self):
        """Verifies that low-bandwidth pruning strips vectors/narratives and rounds floats."""
        rich_payload = {
            "role_title": "Data Scientist",
            "masco_code": "2511",
            "fit_score": 92.345678,
            "svg": "<svg width='500' height='500'>...</svg>",
            "icon_vector": "M10 20 L30 40 Z",
            "full_methodology_text": "Extensive 50-page theoretical framework...",
            "milestones": [
                {"name": "Python Mastery", "duration_hours": 45.1234}
            ]
        }
        pruned = self.engine.render_low_bandwidth_payload(rich_payload)
        self.assertEqual(pruned["_mode"], "LOW_BANDWIDTH")
        self.assertNotIn("svg", pruned)
        self.assertNotIn("icon_vector", pruned)
        self.assertNotIn("full_methodology_text", pruned)
        self.assertEqual(pruned["fit_score"], 92.35)
        self.assertEqual(pruned["milestones"][0]["duration_hours"], 45.12)
        self.assertEqual(pruned["masco_code"], "2511")

    def test_12_payload_compression_ratio(self):
        """Verifies that compression reduces payload by >= 60% and stays under ceiling."""
        large_payload = {
            "cohort_data": [
                {
                    "profile_id": f"SYNTH_USER_{i:04d}",
                    "current_role": "Administrative Assistant",
                    "target_role": "Data Analyst",
                    "masco_code": "2511",
                    "gap_score": 65.43,
                    "skills": ["data_entry", "spreadsheets", "sql_basics", "reporting"]
                }
                for i in range(100)
            ]
        }
        metrics = self.engine.compress_payload(large_payload)
        self.assertTrue(metrics["within_bandwidth_ceiling"])
        self.assertGreaterEqual(metrics["reduction_ratio"], 0.60)
        self.assertLess(metrics["compressed_bytes"], 15000)


if __name__ == "__main__":
    unittest.main()
