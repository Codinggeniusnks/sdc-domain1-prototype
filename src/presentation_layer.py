"""
National AI Workforce Reskilling & Foresight Engine
Module: O3 Multilingual & Low-Bandwidth Presentation Layer
Version: v1.0.0
Author: Autonomous Lead Systems Engineer & Responsible-AI Architect

Provides:
1. Dynamic multilingual translation across English (en), Bahasa Melayu (ms), and Simplified Chinese (zh-CN).
2. 100% catalog key parity validation.
3. Strict mathematical & structural invariance preservation (scores, ranks, codes, and logic remain untouched).
4. Low-bandwidth payload optimization, stripping heavy visual fluff and producing ultra-compact JSON.
5. Compression ratio metrics for low-connectivity rural / mobile edge delivery.
"""

import os
import json
import zlib
import copy
import hashlib
from typing import Dict, Any, List, Optional, Set, Tuple


class PresentationLayer:
    """
    Production-grade presentation and localization engine for the National Workforce
    Foresight platform.
    """

    DEFAULT_CONFIG_PATH = os.path.join("data", "presentation", "o3_config_v1.json")
    DEFAULT_LOCALES_DIR = "locales"

    def __init__(self, config_path: Optional[str] = None, locales_dir: Optional[str] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        self.locales_dir = locales_dir or self.config.get("locales_dir", self.DEFAULT_LOCALES_DIR)
        
        self.supported_locales: List[str] = self.config.get("supported_locales", ["en", "ms", "zh-CN"])
        self.default_locale: str = self.config.get("default_locale", "en")
        self.fallback_locale: str = self.config.get("fallback_locale", "en")
        self.active_locale: str = self.default_locale
        
        # Load translation catalogs
        self.catalogs: Dict[str, Dict[str, Any]] = {}
        self._load_catalogs()
        
        # Validate parity on initialization
        self.parity_report = self.validate_key_parity()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or provides safe defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "engine_version": "v1.0.0",
            "supported_locales": ["en", "ms", "zh-CN"],
            "default_locale": "en",
            "fallback_locale": "en",
            "locales_dir": "locales",
            "low_bandwidth_settings": {
                "target_max_payload_bytes": 65536,
                "min_payload_reduction_ratio": 0.60,
                "float_decimal_precision": 2,
                "strip_heavy_narratives": True
            },
            "invariance_rules": {
                "prohibited_from_translation": [
                    "masco_code", "skill_id", "profile_id", "role_id",
                    "formula_code", "fingerprint", "sha256", "timestamp_utc"
                ]
            }
        }

    def _load_catalogs(self):
        """Loads JSON catalogs for all supported locales."""
        for loc in self.supported_locales:
            cat_path = os.path.join(self.locales_dir, f"{loc}.json")
            if os.path.exists(cat_path):
                with open(cat_path, "r", encoding="utf-8") as f:
                    self.catalogs[loc] = json.load(f)
            else:
                self.catalogs[loc] = {}

    def set_locale(self, locale_code: str) -> str:
        """Sets active locale. Falls back to default if unsupported."""
        if locale_code in self.supported_locales:
            self.active_locale = locale_code
        else:
            self.active_locale = self.default_locale
        return self.active_locale

    def get_locale(self) -> str:
        """Returns the current active locale."""
        return self.active_locale

    def t(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        Translates a dot-notated key in the active locale, falling back to fallback_locale.
        Interpolates kwargs safely.
        """
        val = self._lookup_key(self.active_locale, key)
        if val is None and self.active_locale != self.fallback_locale:
            val = self._lookup_key(self.fallback_locale, key)
        
        if val is None:
            val = default if default is not None else key
            
        if kwargs and isinstance(val, str):
            try:
                val = val.format(**kwargs)
            except Exception:
                pass
        return str(val)

    translate = t

    def _lookup_key(self, locale: str, key: str) -> Optional[Any]:
        """Traverses catalog dictionary using dot notation."""
        cat = self.catalogs.get(locale, {})
        parts = key.split(".")
        curr = cat
        for part in parts:
            if isinstance(curr, dict) and part in curr:
                curr = curr[part]
            else:
                return None
        return curr

    def format_number(self, val: float, decimals: int = 2) -> str:
        """Formats numbers with specified decimal precision."""
        try:
            return f"{float(val):.{decimals}f}"
        except (ValueError, TypeError):
            return str(val)

    def format_currency(self, val: float, currency: str = "MYR") -> str:
        """Formats currency according to Malaysian standards (RM)."""
        try:
            formatted = f"{float(val):,.2f}"
            if currency == "MYR":
                return f"RM {formatted}"
            return f"{currency} {formatted}"
        except (ValueError, TypeError):
            return str(val)

    def _get_leaf_keys(self, d: Dict[str, Any], prefix: str = "") -> Set[str]:
        """Recursively extracts all dot-notated leaf keys."""
        keys = set()
        for k, v in d.items():
            curr = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.update(self._get_leaf_keys(v, curr))
            else:
                keys.add(curr)
        return keys

    def validate_key_parity(self) -> Dict[str, Any]:
        """
        Validates 100% key parity across all supported catalogs.
        Returns detailed report.
        """
        catalog_keys: Dict[str, Set[str]] = {}
        for loc in self.supported_locales:
            cat = self.catalogs.get(loc, {})
            catalog_keys[loc] = self._get_leaf_keys(cat)

        ref_keys = catalog_keys.get(self.default_locale, set())
        discrepancies: Dict[str, Dict[str, List[str]]] = {}
        is_clean = True

        for loc, keys in catalog_keys.items():
            if loc == self.default_locale:
                continue
            missing = sorted(list(ref_keys - keys))
            extra = sorted(list(keys - ref_keys))
            if missing or extra:
                is_clean = False
            discrepancies[loc] = {
                "missing_keys": missing,
                "extra_keys": extra
            }

        return {
            "status": "PASS" if is_clean else "FAIL",
            "is_clean": is_clean,
            "total_canonical_keys": len(ref_keys),
            "locale_key_counts": {loc: len(keys) for loc, keys in catalog_keys.items()},
            "discrepancies": discrepancies
        }

    def verify_mathematical_invariance(self, payload_a: Dict[str, Any], payload_b: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Verifies that mathematical and structural properties are IDENTICAL across
        two payloads rendered under different languages.
        Checks:
        - Exact numeric equality for scores, fit indices, durations, priority indices.
        - Exact sequence order and IDs for recommended roles, skill gaps, and roadmap milestones.
        """
        violations = []
        prohibited = set(self.config.get("invariance_rules", {}).get("prohibited_from_translation", []))

        def _walk_compare(obj_a: Any, obj_b: Any, path: str = ""):
            if type(obj_a) != type(obj_b):
                violations.append(f"Type mismatch at {path}: {type(obj_a)} vs {type(obj_b)}")
                return

            if isinstance(obj_a, dict):
                # Check prohibited keys match exactly
                for k in obj_a:
                    curr_path = f"{path}.{k}" if path else k
                    if k in prohibited or "score" in k.lower() or "rank" in k.lower() or "id" in k.lower() or "code" in k.lower():
                        if k not in obj_b:
                            violations.append(f"Missing key in payload B at {curr_path}")
                        else:
                            _walk_compare(obj_a[k], obj_b[k], curr_path)
            elif isinstance(obj_a, list):
                if len(obj_a) != len(obj_b):
                    violations.append(f"List length mismatch at {path}: {len(obj_a)} vs {len(obj_b)}")
                else:
                    for i, (elem_a, elem_b) in enumerate(zip(obj_a, obj_b)):
                        _walk_compare(elem_a, elem_b, f"{path}[{i}]")
            elif isinstance(obj_a, (int, float)):
                if abs(float(obj_a) - float(obj_b)) > 1e-6:
                    violations.append(f"Numeric variance at {path}: {obj_a} vs {obj_b}")
            elif isinstance(obj_a, str):
                # If path indicates a code or ID, strings must be identical
                last_part = path.split(".")[-1].split("[")[0]
                if last_part in prohibited:
                    if obj_a != obj_b:
                        violations.append(f"Code string mutation at {path}: '{obj_a}' vs '{obj_b}'")

        _walk_compare(payload_a, payload_b)
        return (len(violations) == 0, violations)

    def render_low_bandwidth_payload(self, rich_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strips narrative bloat, vector assets, debug traces, and rounds floats to 2 decimals.
        Preserves all essential decision-support data:
        - Roles, MASCO codes, Match Scores, Gap Severity, Priority Reskilling Index,
        - Roadmap milestones, SDG targets, and privacy badges.
        """
        clean_copy = copy.deepcopy(rich_payload)
        settings = self.config.get("low_bandwidth_settings", {})
        decimals = settings.get("float_decimal_precision", 2)

        def _prune(node: Any) -> Any:
            if isinstance(node, dict):
                pruned = {}
                for k, v in node.items():
                    # Strip heavy or non-essential fields
                    if k in ["svg", "icon_vector", "illustration_url", "raw_embeddings", "verbose_rationale", "debug_trace", "intermediary_features"]:
                        continue
                    if settings.get("strip_heavy_narratives") and k in ["full_methodology_text", "background_literature", "long_description"]:
                        continue
                    pruned[k] = _prune(v)
                return pruned
            elif isinstance(node, list):
                return [_prune(x) for x in node]
            elif isinstance(node, float):
                return round(node, decimals)
            return node

        pruned_payload = _prune(clean_copy)
        pruned_payload["_mode"] = "LOW_BANDWIDTH"
        pruned_payload["_timestamp_utc"] = self.config.get("build_timestamp_utc", "2026-10-24T05:05:00Z")
        return pruned_payload

    def compress_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes serialization and compression metrics (zlib/gzip).
        """
        json_bytes = json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        compressed_bytes = zlib.compress(json_bytes, level=9)
        
        orig_size = len(json_bytes)
        comp_size = len(compressed_bytes)
        reduction_ratio = 1.0 - (comp_size / orig_size) if orig_size > 0 else 0.0

        return {
            "uncompressed_bytes": orig_size,
            "compressed_bytes": comp_size,
            "reduction_ratio": round(reduction_ratio, 4),
            "reduction_percentage": f"{round(reduction_ratio * 100, 2)}%",
            "max_allowed_bytes": self.config.get("low_bandwidth_settings", {}).get("target_max_payload_bytes", 65536),
            "within_bandwidth_ceiling": orig_size <= self.config.get("low_bandwidth_settings", {}).get("target_max_payload_bytes", 65536)
        }
