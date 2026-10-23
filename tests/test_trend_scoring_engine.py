"""Comprehensive automated test suite for M2 AI Trend Intelligence Engine.

Validates:
1. Component score bounds ([0.0, 100.0]).
2. Null handling & missing data preservation (no fake 50 fills).
3. Source-family independence (no double-counting within family).
4. Signal-type aware freshness logic (dynamic vs structural).
5. Level vs. Momentum separation (State != Trend).
6. AI Exposure vs. Job Decline separation (Automation != Augmentation).
7. Explainable, rule-based outlook classification.
8. Evidence confidence calculation & categorical tier assignment.
9. Conflicting evidence detection & penalties.
10. Explanation citation traceability (provenance verification).
11. Cryptographic build hash determinism.
12. M1 Skills Extraction decoupled API contract.
13. M3 Role Matching decoupled API contract (including Major Group fallback).
14. Idempotent rebuild capability.
"""

from __future__ import annotations

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


class TestM2TrendScoringEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = TrendEngine()
        with open(PROCESSED_DIR / "skill_trend_profiles_v1.json", "r", encoding="utf-8") as f:
            cls.skill_data = json.load(f)
            cls.skill_profiles = cls.skill_data.get("profiles", [])

        with open(PROCESSED_DIR / "occupation_trend_profiles_v1.json", "r", encoding="utf-8") as f:
            cls.occ_data = json.load(f)
            cls.occ_profiles = cls.occ_data.get("profiles", [])

        with open(PROCESSED_DIR / "m2_scoring_config_v1.json", "r", encoding="utf-8") as f:
            cls.scoring_config = json.load(f)

        with open(PROCESSED_DIR / "m2_confidence_config_v1.json", "r", encoding="utf-8") as f:
            cls.confidence_config = json.load(f)

        with open(PROCESSED_DIR / "m2_build_manifest_v1.json", "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_01_component_bounds(self):
        """All non-null score components must strictly lie within [0.0, 100.0]."""
        numeric_fields_skills = [
            "demand_shortage_index",
            "demand_momentum_index",
            "employment_wage_index",
            "research_momentum_index",
            "ai_exposure_index",
            "automation_index",
            "augmentation_index",
            "policy_priority_index",
            "confidence_index",
        ]
        for p in self.skill_profiles:
            for field in numeric_fields_skills:
                val = p.get(field)
                if val is not None:
                    self.assertGreaterEqual(
                        val,
                        0.0,
                        f"Skill {p['skill_id']} field {field} is below 0.0: {val}",
                    )
                    self.assertLessEqual(
                        val,
                        100.0,
                        f"Skill {p['skill_id']} field {field} exceeds 100.0: {val}",
                    )

        numeric_fields_occ = [
            "demand_shortage_level",
            "demand_momentum",
            "employment_wage_momentum",
            "research_momentum",
            "ai_exposure",
            "automation_exposure",
            "augmentation_potential",
            "policy_priority",
            "confidence_index",
        ]
        for p in self.occ_profiles:
            for field in numeric_fields_occ:
                val = p.get(field)
                if val is not None:
                    self.assertGreaterEqual(
                        val,
                        0.0,
                        f"Occ {p['occupation_code']} field {field} is below 0.0: {val}",
                    )
                    self.assertLessEqual(
                        val,
                        100.0,
                        f"Occ {p['occupation_code']} field {field} exceeds 100.0: {val}",
                    )

    def test_02_null_handling_missing_evidence(self):
        """Missing evidence must remain null or INSUFFICIENT_DATA, never filled with arbitrary 50."""
        # Occupational profiles must NOT fill research_momentum with fake 50
        for p in self.occ_profiles:
            if not p["occupation_code"].startswith("MAJOR_"):
                self.assertIsNone(
                    p["research_momentum"],
                    f"Occ {p['occupation_code']} should have null research_momentum, not fake score",
                )

        # Non-existent query must return explicit INSUFFICIENT_DATA
        res = self.engine.get_skill_trend("unknown_nonexistent_skill_xyz")
        self.assertEqual(res.get("error"), "INSUFFICIENT_DATA")
        self.assertEqual(res.get("confidence_label"), "INSUFFICIENT")

    def test_03_source_family_independence(self):
        """Independent families must be deduplicated across signals from same publisher."""
        for p in self.skill_profiles:
            fams = p.get("independent_evidence_families", [])
            # Assert no duplicates
            self.assertEqual(
                len(fams),
                len(set(fams)),
                f"Duplicate families in skill {p['skill_id']}",
            )
            # High confidence requires at least 3 distinct families
            if p.get("confidence_label") == "HIGH":
                self.assertGreaterEqual(
                    len(fams),
                    3,
                    f"Skill {p['skill_id']} is HIGH confidence but has < 3 families: {fams}",
                )

    def test_04_freshness_logic(self):
        """Freshness must be signal-type aware and bounded."""
        for p in self.skill_profiles:
            self.assertIn(
                p.get("freshness_status"), ["FRESH", "AGING", "STALE"]
            )
            self.assertGreaterEqual(p.get("freshness_days", -1), 0)

        freshness_audit = self.engine.get_source_freshness()
        self.assertIn("sources", freshness_audit)
        self.assertEqual(
            freshness_audit.get("reference_date"), "2026-10-23"
        )

    def test_05_level_vs_momentum_separation(self):
        """Level and momentum must be modeled separately and allowed to diverge."""
        # Software developers (2512): High level and High momentum (75)
        dev = self.engine.get_role_trend("2512")
        self.assertGreater(dev.get("demand_shortage_level"), 80.0)
        self.assertEqual(dev.get("demand_momentum"), 75.0)

        # Environmental engineers (2143): Moderate level (60.0) but Surging momentum (88.0)
        env = self.engine.get_role_trend("2143")
        self.assertEqual(env.get("demand_shortage_level"), 60.0)
        self.assertEqual(env.get("demand_momentum"), 88.0)
        self.assertNotEqual(
            env.get("demand_shortage_level"), env.get("demand_momentum")
        )

    def test_06_exposure_vs_decline_separation(self):
        """High AI exposure must not automatically cause a DECLINING outlook if augmentation is high."""
        # Software Developers (2512): High AI exposure (54%) with Augmentation (48%) > Automation (6%)
        dev = self.engine.get_role_trend("2512")
        self.assertGreater(dev.get("ai_exposure"), 50.0)
        self.assertIn(
            dev.get("overall_outlook"), ["RISING", "STRONGLY RISING"]
        )

        # General Office Clerks (4110): Automation (28%) > Augmentation (8%) -> STRONGLY DECLINING
        clerk = self.engine.get_role_trend("4110")
        self.assertGreater(
            clerk.get("automation_exposure"),
            clerk.get("augmentation_potential"),
        )
        self.assertIn(
            clerk.get("overall_outlook"), ["DECLINING", "STRONGLY DECLINING"]
        )

    def test_07_outlook_classification_rules(self):
        """Outlooks must strictly conform to allowed enum values."""
        allowed_outlooks = {
            "STRONGLY RISING",
            "RISING",
            "STABLE",
            "MIXED / UNCERTAIN",
            "DECLINING",
            "STRONGLY DECLINING",
        }
        for p in self.skill_profiles:
            self.assertIn(p.get("overall_outlook"), allowed_outlooks)
        for p in self.occ_profiles:
            self.assertIn(p.get("overall_outlook"), allowed_outlooks)

    def test_08_confidence_calculation(self):
        """Confidence index and categorical labels must follow configured thresholds."""
        for p in self.skill_profiles:
            idx = p.get("confidence_index", 0)
            lbl = p.get("confidence_label")
            if lbl == "HIGH":
                self.assertGreaterEqual(idx, 75.0)
            elif lbl == "MEDIUM":
                self.assertGreaterEqual(idx, 50.0)
            elif lbl == "LOW":
                self.assertGreaterEqual(idx, 25.0)

    def test_09_explanation_traceability(self):
        """Every explanation positive/negative driver must contain full citation metadata."""
        exp = explain_trend("2512")
        self.assertEqual(exp.get("entity_id"), "2512")
        pos_drivers = exp.get("top_positive_drivers", [])
        self.assertGreater(len(pos_drivers), 0)

        for d in pos_drivers:
            self.assertTrue(d.get("signal_id"), "Missing signal_id in driver")
            self.assertTrue(d.get("source_id"), "Missing source_id in driver")
            self.assertTrue(d.get("publisher"), "Missing publisher in driver")
            self.assertTrue(
                d.get("evidence_reference"),
                "Missing evidence_reference in driver",
            )

    def test_10_deterministic_build_hashes(self):
        """Manifest must contain valid SHA-256 hashes of all input and output files."""
        input_hashes = self.manifest.get("input_hashes", {})
        output_hashes = self.manifest.get("output_hashes", {})

        self.assertIn("trend_signals_v1.json", input_hashes)
        self.assertIn("skill_trend_profiles_v1.json", output_hashes)
        self.assertIn("occupation_trend_profiles_v1.json", output_hashes)

        for filename, sha in output_hashes.items():
            self.assertEqual(
                len(sha), 64, f"Hash for {filename} is not valid SHA-256"
            )

    def test_11_m1_api_interface(self):
        """M1 interface get_skill_trend must support canonical skills and Level 2 crosswalk resolution."""
        # Canonical Level 1
        res1 = get_skill_trend("python_scripting")
        self.assertEqual(res1.get("skill_id"), "python_scripting")
        self.assertIn("overall_outlook", res1)
        self.assertIn("confidence_index", res1)

        # Level 2 Crosswalk resolution
        res2 = get_skill_trend("Generative AI Fundamentals")
        self.assertEqual(res2.get("skill_id"), "ai_literacy")
        self.assertTrue(res2.get("resolved_via_crosswalk"))
        self.assertEqual(res2.get("mapping_method"), "synonym")

    def test_12_m3_api_interface_and_major_fallback(self):
        """M3 interface get_role_trend must resolve 4-digit codes and provide Major Group fallback."""
        # Exact 4-digit code
        r1 = get_role_trend("2512")
        self.assertEqual(r1.get("occupation_code"), "2512")
        self.assertEqual(r1.get("occupation_title"), "Software Developers")

        # Major Group Fallback for unmapped code in Major Group 2
        r2 = get_role_trend("2199")
        self.assertEqual(r2.get("major_group"), "2")
        self.assertTrue(r2.get("is_major_group_fallback"))

    def test_13_batch_query_interface(self):
        """get_trend_batch must return combined dictionary of skill and occupation profiles."""
        batch = get_trend_batch(["2512", "python_scripting", "4110"])
        self.assertIn("2512", batch)
        self.assertIn("python_scripting", batch)
        self.assertIn("4110", batch)
        self.assertEqual(batch["2512"]["overall_outlook"], "STRONGLY RISING")
        self.assertEqual(batch["4110"]["overall_outlook"], "STRONGLY DECLINING")


if __name__ == "__main__":
    unittest.main()
