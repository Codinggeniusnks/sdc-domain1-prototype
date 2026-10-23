"""M2 AI Trend Intelligence Engine - Core Scoring, Explainability, and Query Service.

Version: 1.1.0 (Remediated)
Provides:
- Decomposed 10-dimensional trend profiles for Skills and Occupations.
- Level vs. Momentum separation.
- Exposure vs. Decline separation (Automation vs. Augmentation).
- Transparent, citation-grounded explainability with source traceability.
- Recalibrated evidence confidence scoring (0-100 and categorical label).
- Explicit OpenDOSM wage granularity metadata (MAJOR_GROUP_CONTEXT).
- Dual ILO benchmark support (ILO WP 140 [2025] primary, ILO WP 96 [2023] historical).
- Clean decoupled interfaces for M1 (Skills Extraction) and M3 (Role Matching).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Optional

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
DATA_DIR = BASE_DIR / "data" / "trends"
PROCESSED_DIR = DATA_DIR / "processed"
MANIFEST_DIR = DATA_DIR / "manifests"

REFERENCE_DATE = "2026-10-23"


class TrendEngine:
    def __init__(self, processed_dir: Optional[Path] = None, version: str = "v1.1.1"):
        self.processed_dir = processed_dir or PROCESSED_DIR
        self.version = version

        # Version-aware paths
        if version in ["v1.1.1", "1.1.1"]:
            self.signals_path = self.processed_dir / "trend_signals_v1_1.json"
            self.skill_profiles_path = self.processed_dir / "skill_trend_profiles_v1_1_1.json"
            self.occ_profiles_path = self.processed_dir / "occupation_trend_profiles_v1_1_1.json"
            self.scoring_config_path = self.processed_dir / "m2_scoring_config_v1_1_1.json"
            self.confidence_config_path = self.processed_dir / "m2_confidence_config_v1_1_1.json"
            self.build_manifest_path = self.processed_dir / "m2_build_manifest_v1_1_1.json"
        elif version in ["v1.1", "1.1", "v1.1.0", "1.1.0"]:
            self.signals_path = self.processed_dir / "trend_signals_v1_1.json"
            self.skill_profiles_path = self.processed_dir / "skill_trend_profiles_v1_1.json"
            self.occ_profiles_path = self.processed_dir / "occupation_trend_profiles_v1_1.json"
            self.scoring_config_path = self.processed_dir / "m2_scoring_config_v1_1.json"
            self.confidence_config_path = self.processed_dir / "m2_confidence_config_v1_1.json"
            self.build_manifest_path = self.processed_dir / "m2_build_manifest_v1_1.json"
        else:
            self.signals_path = self.processed_dir / "trend_signals_v1.json"
            self.skill_profiles_path = self.processed_dir / "skill_trend_profiles_v1.json"
            self.occ_profiles_path = self.processed_dir / "occupation_trend_profiles_v1.json"
            self.scoring_config_path = self.processed_dir / "m2_scoring_config_v1.json"
            self.confidence_config_path = self.processed_dir / "m2_confidence_config_v1.json"
            self.build_manifest_path = self.processed_dir / "m2_build_manifest_v1.json"

        self.skill_crosswalk_path = self.processed_dir / "skill_source_crosswalk.json"
        self.occ_crosswalk_path = self.processed_dir / "occupation_source_crosswalk.json"
        self.freshness_path = self.processed_dir / "source_freshness.json"
        self.manifest_path = MANIFEST_DIR / "trend_source_manifest.json"

        self._load_store()

    def _load_store(self):
        """Load signals, crosswalks, manifests, and profiles."""
        if self.signals_path.exists():
            with open(self.signals_path, "r", encoding="utf-8") as f:
                self.signals_artifact = json.load(f)
            self.signals = self.signals_artifact.get("signals", [])
        else:
            self.signals = []

        with open(self.skill_crosswalk_path, "r", encoding="utf-8") as f:
            self.skill_crosswalk = json.load(f)

        with open(self.occ_crosswalk_path, "r", encoding="utf-8") as f:
            self.occ_crosswalk = json.load(f)

        with open(self.freshness_path, "r", encoding="utf-8") as f:
            self.source_freshness = json.load(f)

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self.source_manifest = json.load(f)

        # Pre-computed profiles
        self.skill_profiles = {}
        if self.skill_profiles_path.exists():
            with open(self.skill_profiles_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.skill_profiles = {p["skill_id"]: p for p in data.get("profiles", [])}

        self.occ_profiles = {}
        if self.occ_profiles_path.exists():
            with open(self.occ_profiles_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.occ_profiles = {p["occupation_code"]: p for p in data.get("profiles", [])}

    def get_skill_trend(self, skill_id: str) -> dict[str, Any]:
        """M1 Interface: Fetch decomposed trend vector, outlook, and confidence for a canonical skill."""
        query_key = str(skill_id).strip()
        if query_key in self.skill_profiles:
            return self.skill_profiles[query_key]

        # Case-insensitive / normalized lookup
        norm_key = query_key.lower().replace("_", " ")
        for k, p in self.skill_profiles.items():
            if k.lower() == query_key.lower() or k.lower().replace("_", " ") == norm_key:
                return p

        # Check if skill is Level 2 and can be resolved via crosswalk
        for s in self.skill_crosswalk.get("level_2_expanded_skills", []):
            src_name = s.get("source_skill", "").strip()
            if (
                src_name.lower() == query_key.lower()
                or src_name.lower().replace("_", " ") == norm_key
                or query_key.lower() in src_name.lower()
            ):
                canon_id = s.get("canonical_id")
                if canon_id and canon_id in self.skill_profiles:
                    profile = dict(self.skill_profiles[canon_id])
                    profile["queried_source_skill"] = query_key
                    profile["resolved_via_crosswalk"] = True
                    profile["mapping_method"] = s.get("method")
                    return profile

        return {
            "skill_id": skill_id,
            "error": "INSUFFICIENT_DATA",
            "message": f"No trend intelligence signals available for skill: {skill_id}",
            "overall_outlook": "MIXED / UNCERTAIN",
            "confidence_label": "INSUFFICIENT",
            "confidence_index": 0
        }

    def get_role_trend(self, masco_code: str) -> dict[str, Any]:
        """M3 Interface: Fetch decomposed occupational profile for a MASCO 2020 4-digit code."""
        code_str = str(masco_code).strip()
        if code_str in self.occ_profiles:
            return self.occ_profiles[code_str]

        # Check major group fallback
        major_key = f"MAJOR_{code_str[0]}" if code_str and code_str[0].isdigit() else ""
        if major_key in self.occ_profiles:
            fallback = dict(self.occ_profiles[major_key])
            fallback["queried_code"] = code_str
            fallback["is_major_group_fallback"] = True
            fallback["wage_granularity"] = "MAJOR_GROUP_CONTEXT"
            return fallback

        return {
            "occupation_code": code_str,
            "error": "INSUFFICIENT_DATA",
            "message": f"No occupational trend signals available for MASCO: {code_str}",
            "overall_outlook": "MIXED / UNCERTAIN",
            "confidence_label": "INSUFFICIENT",
            "confidence_index": 0
        }

    def get_trend_batch(self, entity_ids: list[str]) -> dict[str, dict[str, Any]]:
        """Batch query interface for M3 role/skill candidate ranking."""
        results = {}
        for eid in entity_ids:
            if eid in self.skill_profiles:
                results[eid] = self.get_skill_trend(eid)
            elif eid in self.occ_profiles:
                results[eid] = self.get_role_trend(eid)
            else:
                sk = self.get_skill_trend(eid)
                if sk.get("error") is None:
                    results[eid] = sk
                else:
                    results[eid] = self.get_role_trend(eid)
        return results

    def explain_trend(self, entity_id: str) -> dict[str, Any]:
        """Generate human- and machine-readable explainability report with citation traceability."""
        profile = None
        if entity_id in self.skill_profiles:
            profile = self.skill_profiles[entity_id]
        elif entity_id in self.occ_profiles:
            profile = self.occ_profiles[entity_id]

        if not profile:
            return {
                "entity_id": entity_id,
                "error": "NOT_FOUND",
                "explanation": "No trend profile found for the requested entity."
            }

        return {
            "entity_id": entity_id,
            "title_or_name": profile.get("skill_name") or profile.get("occupation_title"),
            "overall_outlook": profile.get("overall_outlook"),
            "confidence": f"{profile.get('confidence_label')} ({profile.get('confidence_index')}/100)",
            "conflict_status": profile.get("conflict_status", "NO_CONFLICT"),
            "conflict_notes": profile.get("conflict_notes", ""),
            "wage_granularity": profile.get("wage_granularity"),
            "wage_context_code": profile.get("wage_context_code"),
            "wage_context_label": profile.get("wage_context_label"),
            "top_positive_drivers": profile.get("top_positive_drivers", []),
            "top_negative_drivers": profile.get("top_negative_drivers", []),
            "uncertainties": profile.get("uncertainties", []),
            "quality_flags": profile.get("quality_flags", []),
            "citation_list": profile.get("top_positive_drivers", []) + profile.get("top_negative_drivers", []),
            "last_updated": profile.get("last_updated")
        }

    def get_source_freshness(self) -> dict[str, Any]:
        """Return engine freshness audit table."""
        return self.source_freshness


# Module singleton instance
_engine_instance: Optional[TrendEngine] = None


def get_trend_engine(version: str = "v1.1") -> TrendEngine:
    global _engine_instance
    if _engine_instance is None or _engine_instance.version != version:
        _engine_instance = TrendEngine(version=version)
    return _engine_instance


def get_skill_trend(skill_id: str, version: str = "v1.1") -> dict[str, Any]:
    return get_trend_engine(version=version).get_skill_trend(skill_id)


def get_role_trend(masco_code: str, version: str = "v1.1") -> dict[str, Any]:
    return get_trend_engine(version=version).get_role_trend(masco_code)


def get_trend_batch(ids: list[str], version: str = "v1.1") -> dict[str, dict[str, Any]]:
    return get_trend_engine(version=version).get_trend_batch(ids)


def explain_trend(entity_id: str, version: str = "v1.1") -> dict[str, Any]:
    return get_trend_engine(version=version).explain_trend(entity_id)


def get_source_freshness() -> dict[str, Any]:
    return get_trend_engine().get_source_freshness()
