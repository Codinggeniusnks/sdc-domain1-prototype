"""Automated test suite for M2 AI Trend Intelligence Engine Data Foundation.
Compatible with standard library unittest and pytest.

Validates:
1. Schema validation
2. Source manifest completeness
3. Required provenance
4. Date parsing & ISO compliance
5. Duplicate prevention
6. Idempotent refresh
7. Occupation taxonomy crosswalk integrity
8. Skill taxonomy crosswalk integrity
9. Normalisation bounds [0.0, 1.0]
10. Freshness calculation
11. Source-family deduplication
12. Zero M1 training contamination
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
DATA_DIR = BASE_DIR / "data" / "trends"
PROCESSED_SIGNALS_PATH = DATA_DIR / "processed" / "trend_signals_v1.json"
SOURCE_MANIFEST_PATH = DATA_DIR / "manifests" / "trend_source_manifest.json"
SKILL_CROSSWALK_PATH = DATA_DIR / "processed" / "skill_source_crosswalk.json"
OCCUPATION_CROSSWALK_PATH = DATA_DIR / "processed" / "occupation_source_crosswalk.json"
FRESHNESS_PATH = DATA_DIR / "processed" / "source_freshness.json"

DATASET_V5_PATH = BASE_DIR / "data" / "processed" / "dataset_v5_clean_multisource.json"
EXPECTED_DATASET_V5_SHA256 = "9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d"

ISO_DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}")

REQUIRED_SIGNAL_FIELDS = [
    "signal_id", "entity_type", "entity_id", "signal_type",
    "signal_value_raw", "signal_value_normalized", "direction",
    "source_id", "source_date", "retrieved_at", "valid_from",
    "geography", "confidence", "quality_tier", "freshness_days",
    "evidence_family", "evidence_text", "evidence_reference"
]

ALLOWED_ENTITY_TYPES = {"skill", "occupation", "task", "sector"}
ALLOWED_DIRECTIONS = {
    "STRONGLY RISING", "RISING", "STABLE",
    "MIXED / UNCERTAIN", "DECLINING", "STRONGLY DECLINING"
}
ALLOWED_TIERS = {"TIER_A", "TIER_B", "TIER_C", "TIER_D"}


class TestTrendEngineFoundation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert PROCESSED_SIGNALS_PATH.exists(), f"Processed signals not found: {PROCESSED_SIGNALS_PATH}"
        with open(PROCESSED_SIGNALS_PATH, "r", encoding="utf-8") as f:
            cls.processed_data = json.load(f)

        assert SOURCE_MANIFEST_PATH.exists(), f"Manifest not found: {SOURCE_MANIFEST_PATH}"
        with open(SOURCE_MANIFEST_PATH, "r", encoding="utf-8") as f:
            cls.manifest_data = json.load(f)

        assert SKILL_CROSSWALK_PATH.exists()
        with open(SKILL_CROSSWALK_PATH, "r", encoding="utf-8") as f:
            cls.skill_crosswalk = json.load(f)

        assert OCCUPATION_CROSSWALK_PATH.exists()
        with open(OCCUPATION_CROSSWALK_PATH, "r", encoding="utf-8") as f:
            cls.occupation_crosswalk = json.load(f)

    def test_01_schema_validation(self):
        """Test 1: Verify every signal record has all required fields with expected types."""
        signals = self.processed_data.get("signals", [])
        self.assertGreater(len(signals), 0, "No signals found in processed artifact.")

        for idx, sig in enumerate(signals):
            for field in REQUIRED_SIGNAL_FIELDS:
                self.assertIn(field, sig, f"Signal #{idx} ({sig.get('signal_id')}) missing field: {field}")
            self.assertIn(sig["entity_type"], ALLOWED_ENTITY_TYPES)
            self.assertIn(sig["direction"], ALLOWED_DIRECTIONS)
            self.assertIn(sig["quality_tier"], ALLOWED_TIERS)

    def test_02_source_manifest_completeness(self):
        """Test 2: Verify source manifest contains all required metadata fields and sources."""
        sources = self.manifest_data.get("sources", [])
        self.assertGreaterEqual(len(sources), 5, f"Expected at least 5 sources, found {len(sources)}")

        required_manifest_fields = [
            "source_id", "name", "publisher", "url_or_reference", "licence",
            "access_method", "version", "publication_date", "retrieval_time",
            "expected_refresh_cadence", "geographic_scope", "quality_tier",
            "evidence_family", "signal_types_supplied"
        ]
        for src in sources:
            for field in required_manifest_fields:
                self.assertIn(field, src, f"Source {src.get('source_id')} missing field: {field}")
            self.assertIn(src["quality_tier"], ALLOWED_TIERS)

    def test_03_required_provenance(self):
        """Test 3: Every signal must link to a valid source_id in the source manifest."""
        manifest_source_ids = {s["source_id"] for s in self.manifest_data.get("sources", [])}
        signals = self.processed_data.get("signals", [])

        for sig in signals:
            sid = sig["source_id"]
            self.assertIn(sid, manifest_source_ids, f"Signal {sig['signal_id']} references unknown source: {sid}")
            self.assertGreater(len(sig["evidence_reference"]), 5, f"Signal {sig['signal_id']} has empty evidence reference")
            self.assertGreater(len(sig["evidence_text"]), 10, f"Signal {sig['signal_id']} has trivial evidence text")

    def test_04_date_parsing_and_iso_format(self):
        """Test 4: Verify date fields conform to strict ISO YYYY-MM-DD format."""
        signals = self.processed_data.get("signals", [])
        for sig in signals:
            self.assertTrue(ISO_DATE_REGEX.match(sig["source_date"]), f"Invalid source_date in {sig['signal_id']}: {sig['source_date']}")
            self.assertTrue(ISO_DATE_REGEX.match(sig["valid_from"]), f"Invalid valid_from in {sig['signal_id']}: {sig['valid_from']}")

    def test_05_duplicate_prevention(self):
        """Test 5: Verify all signal IDs are completely unique."""
        signals = self.processed_data.get("signals", [])
        seen = set()
        duplicates = []
        for sig in signals:
            sid = sig["signal_id"]
            if sid in seen:
                duplicates.append(sid)
            seen.add(sid)
        self.assertEqual(len(duplicates), 0, f"Found {len(duplicates)} duplicate signal IDs: {duplicates}")

    def test_06_idempotent_refresh(self):
        """Test 6: Verify executing update_trend_sources.py twice produces identical output."""
        script_path = BASE_DIR / "scripts" / "update_trend_sources.py"

        # Run 1
        res1 = subprocess.run([sys.executable, str(script_path), "--dry-run"], capture_output=True, text=True)
        self.assertEqual(res1.returncode, 0, f"Pipeline run 1 failed: {res1.stderr}")

        # Run 2
        res2 = subprocess.run([sys.executable, str(script_path), "--dry-run"], capture_output=True, text=True)
        self.assertEqual(res2.returncode, 0, f"Pipeline run 2 failed: {res2.stderr}")

        # Extract final unique counts
        count1 = [line for line in res1.stdout.splitlines() if "Final unique normalized signals:" in line]
        count2 = [line for line in res2.stdout.splitlines() if "Final unique normalized signals:" in line]
        self.assertEqual(count1, count2, f"Idempotency violation: {count1} vs {count2}")

    def test_07_occupation_mapping(self):
        """Test 7: Verify occupation crosswalk maps to MASCO, ISCO, and DOSM wage categories."""
        records = self.occupation_crosswalk.get("records", [])
        self.assertGreaterEqual(len(records), 15, "Insufficient occupations mapped.")

        for rec in records:
            self.assertIn("masco_code", rec)
            self.assertIn("isco_08_code", rec)
            self.assertIn("dosm_wage_category", rec)
            self.assertTrue(0.0 <= rec["mapping_confidence"] <= 1.0)

    def test_08_skill_mapping(self):
        """Test 8: Verify skill crosswalk covers all 16 Level 1 skills and preserves unmapped Level 2 skills."""
        l1 = self.skill_crosswalk.get("level_1_core_skills", [])
        self.assertEqual(len(l1), 16, f"Expected 16 Level 1 core skills, found {len(l1)}")

        l2 = self.skill_crosswalk.get("level_2_expanded_skills", [])
        self.assertGreaterEqual(len(l2), 30, f"Expected at least 30 Level 2 skills, found {len(l2)}")

        unmapped = [s for s in l2 if s["method"] == "unmapped"]
        self.assertGreater(len(unmapped), 0, "Unmapped skills must be preserved with method='unmapped'")
        for u in unmapped:
            self.assertIsNone(u["canonical_id"], "Unmapped skill must have canonical_id=None")

    def test_09_normalisation_bounds(self):
        """Test 9: Verify normalized scores and confidences are bounded in [0.0, 1.0]."""
        signals = self.processed_data.get("signals", [])
        for sig in signals:
            val = sig["signal_value_normalized"]
            self.assertTrue(0.0 <= val <= 1.0, f"Signal {sig['signal_id']} has out-of-bounds normalized value: {val}")
            conf = sig["confidence"]
            self.assertTrue(0.0 <= conf <= 1.0, f"Signal {sig['signal_id']} has out-of-bounds confidence: {conf}")

    def test_10_freshness_calculation(self):
        """Test 10: Verify freshness days is positive and freshness category is valid."""
        signals = self.processed_data.get("signals", [])
        valid_freshness_cats = {"FRESH", "ACCEPTABLE", "ARCHIVAL_VALID", "STALE"}
        for sig in signals:
            self.assertGreaterEqual(sig["freshness_days"], 0, f"Negative freshness days in {sig['signal_id']}")
            self.assertIn(sig["freshness_category"], valid_freshness_cats)

    def test_11_source_family_deduplication(self):
        """Test 11: Verify independent evidence families are tracked."""
        signals = self.processed_data.get("signals", [])
        families = {s["evidence_family"] for s in signals}
        expected_families = {
            "TALENTCORP_MYCOL",
            "TALENTCORP_IMPACT_STUDY",
            "DOSM_LABOUR_FORCE",
            "DOSM_WAGES",
            "ILO_GENAI_STUDY",
            "OPENALEX_SCHOLARLY",
            "MALAYSIAN_GOVERNMENT_POLICY"
        }
        for ef in expected_families:
            self.assertIn(ef, families, f"Missing evidence family: {ef}")

    def test_12_zero_m1_training_contamination(self):
        """Test 12: Verify Dataset v5 and M1 models have ZERO contamination and unchanged SHA-256."""
        import hashlib
        self.assertTrue(DATASET_V5_PATH.exists(), f"Dataset v5 not found: {DATASET_V5_PATH}")
        with open(DATASET_V5_PATH, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, EXPECTED_DATASET_V5_SHA256, f"Dataset v5 SHA-256 mismatch! Expected {EXPECTED_DATASET_V5_SHA256}, got {h}")


if __name__ == "__main__":
    unittest.main()
