"""
O2 Automatic Replanning & Change Detection Engine v1.0.0
SDC Domain 1 - Autonomous Replanning & Orchestration Layer

Orchestrates change detection and candidate replanning across frozen upstream
and downstream models:
  - M1 Skills Extraction (Frozen: H_blend_0.70A_0.30C1_W1.0)
  - M2 Trend Intelligence (Frozen: v1.1.1)
  - M6 Scenario Engine (Frozen: v1.1.0)
  - M3 Future-Role Matching (Frozen: v1.1.0)
  - M4 Personalised Reskilling (Frozen: v1.1.0)
  - M5 SDG Impact Mapping (Frozen: v1.1.0)
  - O6 SDG Aggregation (Frozen: v1.1.0)
  - O1 Workforce Gap & Cohort Reskilling (Frozen: v1.1.0)

Key Principles:
  1. O2 is an orchestration and change-detection layer, NOT an owner of upstream logic.
  2. Automatic != Silent Mutation: material changes yield AUTO_RECOMPUTED_CANDIDATE,
     requiring human/user acknowledgement before adoption.
  3. Strict state immutability, deterministic state fingerprints, and idempotent execution.
  4. Privacy-safe diffs adhering to O1 k=5 small-cell masking and complementary suppression.
  5. Structural changes strictly dominate score movements in materiality classification.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set


class ReplanningEngine:
    VERSION = "1.0.0"

    # Frozen Upstream & Downstream Baseline
    PINNED_VERSIONS = {
        "M1": "H_blend_0.70A_0.30C1_W1.0",
        "M2": "v1.1.1",
        "M6": "v1.1.0",
        "M3": "v1.1.0",
        "M4": "v1.1.0",
        "M5": "v1.1.0",
        "O6": "v1.1.0",
        "O1": "v1.1.0"
    }

    SUPPORTED_EVENT_TYPES = {
        "M2_TREND_SNAPSHOT_UPDATED",
        "M6_SCENARIO_CHANGED",
        "PROFILE_SKILL_STATE_UPDATED",
        "COHORT_SNAPSHOT_UPDATED",
        "MANUAL_REPLAN_REQUESTED",
        "NO_RELEVANT_CHANGE"
    }

    MATERIALITY_LEVELS = ["NONE", "MINOR", "MATERIAL", "HIGH_MATERIALITY"]

    def __init__(self, config_path: Optional[str] = None):
        self.root = Path(__file__).resolve().parent.parent
        if config_path is None:
            config_path = self.root / "data" / "replanning" / "o2_config_v1.json"
        
        self.config_path = Path(config_path)
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "engine_name": "O2 Automatic Replanning & Change Detection Engine",
                "engine_version": "1.0.0",
                "product_policy_thresholds": {
                    "match_index_materiality_threshold": 0.15,
                    "priority_index_materiality_threshold": 10.0,
                    "learning_hours_substantial_band_delta": 40.0,
                    "minimum_cohort_reporting_threshold": 5,
                    "hysteresis_margin": 0.02
                }
            }

        self.thresholds = self.config.get("product_policy_thresholds", {})
        self.processed_event_ids: Set[str] = set()
        self.audit_ledger: List[Dict[str, Any]] = []
        self._state_store: Dict[str, Dict[str, Any]] = {}

    # -------------------------------------------------------------------------
    # 1. State Snapshot & Fingerprinting
    # -------------------------------------------------------------------------

    def build_state_snapshot(
        self,
        profile_snapshot: Any,
        m2_snapshot_id: str = "M2_DEFAULT",
        m2_snapshot_data: Optional[Dict[str, Any]] = None,
        scenario_id: str = "REFERENCE_2026",
        m3_output: Optional[Dict[str, Any]] = None,
        m4_output: Optional[Dict[str, Any]] = None,
        o6_output: Optional[Dict[str, Any]] = None,
        o1_output: Optional[Dict[str, Any]] = None,
        cohort_snapshot: Optional[List[Dict[str, Any]]] = None,
        state_id: Optional[str] = None,
        created_at: Optional[str] = None,
        data_source_class: str = "SYNTHETIC_CHANGE_FIXTURE"
    ) -> Dict[str, Any]:
        """
        Builds an immutable state snapshot dictionary.
        Once created, this snapshot must never be mutated in-place.
        """
        profile_hash = self._hash_payload(profile_snapshot)
        m2_hash = self._hash_payload(m2_snapshot_data) if m2_snapshot_data else "NONE"
        cohort_hash = self._hash_payload(cohort_snapshot) if cohort_snapshot else "NONE"
        
        m3_hash = self._hash_payload(m3_output) if m3_output else "NONE"
        m4_hash = self._hash_payload(m4_output) if m4_output else "NONE"
        o6_hash = self._hash_payload(o6_output) if o6_output else "NONE"
        o1_hash = self._hash_payload(o1_output) if o1_output else "NONE"

        canonical_semantic = {
            "profile_snapshot_hash": profile_hash,
            "cohort_snapshot_hash": cohort_hash,
            "m2_version": self.PINNED_VERSIONS["M2"],
            "m2_snapshot_id": m2_snapshot_id,
            "m2_snapshot_hash": m2_hash,
            "m6_version": self.PINNED_VERSIONS["M6"],
            "m6_scenario": scenario_id,
            "m3_version": self.PINNED_VERSIONS["M3"],
            "m4_version": self.PINNED_VERSIONS["M4"],
            "m5_version": self.PINNED_VERSIONS["M5"],
            "o6_version": self.PINNED_VERSIONS["O6"],
            "o1_version": self.PINNED_VERSIONS["O1"],
            "m3_output_hash": m3_hash,
            "m4_output_hash": m4_hash,
            "o6_output_hash": o6_hash,
            "o1_output_hash": o1_hash,
            "data_source_class": data_source_class
        }
        
        fingerprint = self.compute_state_fingerprint(canonical_semantic)
        now_ts = created_at or datetime.now(timezone.utc).isoformat()
        sid = state_id or f"STATE_{fingerprint[:12]}"

        snapshot = {
            "state_id": sid,
            "created_at": now_ts,
            "state_fingerprint": fingerprint,
            "profile_snapshot_hash": profile_hash,
            "cohort_snapshot_hash": cohort_hash,
            "m2_version": self.PINNED_VERSIONS["M2"],
            "m2_snapshot_id": m2_snapshot_id,
            "m2_snapshot_hash": m2_hash,
            "m6_version": self.PINNED_VERSIONS["M6"],
            "m6_scenario": scenario_id,
            "m3_version": self.PINNED_VERSIONS["M3"],
            "m4_version": self.PINNED_VERSIONS["M4"],
            "m5_version": self.PINNED_VERSIONS["M5"],
            "o6_version": self.PINNED_VERSIONS["O6"],
            "o1_version": self.PINNED_VERSIONS["O1"],
            "m3_output_hash": m3_hash,
            "m4_output_hash": m4_hash,
            "o6_output_hash": o6_hash,
            "o1_output_hash": o1_hash,
            "data_source_class": data_source_class,
            # Payload references for inspection / candidate comparison
            "_raw_profile": profile_snapshot,
            "_raw_m3": m3_output,
            "_raw_m4": m4_output,
            "_raw_o6": o6_output,
            "_raw_o1": o1_output,
            "_raw_cohort": cohort_snapshot
        }
        self._state_store[sid] = snapshot
        return snapshot

    def compute_state_fingerprint(self, semantic_state: Dict[str, Any]) -> str:
        """
        Computes deterministic SHA-256 state fingerprint strictly over canonical
        semantic fields, excluding volatile timestamps, state_ids, or logging metadata.
        """
        canonical_keys = [
            "profile_snapshot_hash",
            "cohort_snapshot_hash",
            "m2_version",
            "m2_snapshot_id",
            "m2_snapshot_hash",
            "m6_version",
            "m6_scenario",
            "m3_version",
            "m4_version",
            "m5_version",
            "o6_version",
            "o1_version",
            "m3_output_hash",
            "m4_output_hash",
            "o6_output_hash",
            "o1_output_hash",
            "data_source_class"
        ]
        subset = {k: semantic_state.get(k, "NONE") for k in sorted(canonical_keys)}
        s = json.dumps(subset, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    # -------------------------------------------------------------------------
    # 2. Change Detection & Dependency Planning
    # -------------------------------------------------------------------------

    def detect_state_changes(
        self,
        previous_state: Dict[str, Any],
        new_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compares previous and new state snapshots to identify changed dimensions
        and attribute root causes.
        """
        prev_fp = previous_state.get("state_fingerprint")
        new_fp = new_state.get("state_fingerprint")
        
        if prev_fp == new_fp:
            return {
                "state_changed": False,
                "changed_dimensions": [],
                "root_causes": ["NO_RELEVANT_CHANGE"],
                "explanation": "State fingerprints are identical. No semantic change detected."
            }

        changed_dims = []
        root_causes = []

        # Check M2 Trend evidence
        if (previous_state.get("m2_snapshot_hash") != new_state.get("m2_snapshot_hash") or
            previous_state.get("m2_snapshot_id") != new_state.get("m2_snapshot_id")):
            changed_dims.append("M2_TREND_EVIDENCE")
            root_causes.append("TREND_CHANGE")

        # Check M6 Scenario
        if previous_state.get("m6_scenario") != new_state.get("m6_scenario"):
            changed_dims.append("M6_SCENARIO")
            root_causes.append("SCENARIO_CHANGE")

        # Check Profile Skills
        if previous_state.get("profile_snapshot_hash") != new_state.get("profile_snapshot_hash"):
            changed_dims.append("PROFILE_SKILLS")
            root_causes.append("PROFILE_CHANGE")

        # Check Cohort Composition
        if previous_state.get("cohort_snapshot_hash") != new_state.get("cohort_snapshot_hash"):
            changed_dims.append("COHORT_COMPOSITION")
            root_causes.append("COHORT_CHANGE")

        # Check outputs directly if upstream hashes are identical but outputs differ
        for mod in ["M3", "M4", "O6", "O1"]:
            h_key = f"{mod.lower()}_output_hash"
            if previous_state.get(h_key) != new_state.get(h_key):
                if mod not in [d.split("_")[0] for d in changed_dims]:
                    changed_dims.append(f"{mod}_OUTPUT")

        if len(root_causes) > 1:
            consolidated_causes = ["MULTIPLE_INPUT_CHANGES"] + root_causes
        elif len(root_causes) == 1:
            consolidated_causes = root_causes
        else:
            consolidated_causes = ["MANUAL_RECOMPUTE"]

        return {
            "state_changed": True,
            "changed_dimensions": changed_dims,
            "root_causes": consolidated_causes,
            "previous_state_fingerprint": prev_fp,
            "new_state_fingerprint": new_fp
        }

    def build_recompute_plan(
        self,
        event_type: str,
        changed_dimensions: List[str]
    ) -> Dict[str, Any]:
        """
        Determines affected modules and dependency recomputation order.
        Avoids unnecessary recomputation (e.g. cohort change does not re-run individual M3/M4).
        """
        if event_type == "NO_RELEVANT_CHANGE" or not changed_dimensions:
            return {
                "affected_modules": [],
                "recompute_order": [],
                "reason_codes": ["NO_RECOMPUTE_NEEDED"],
                "skip_individual_m3_m4": True
            }

        # Deterministic Dependency Rules
        if event_type == "COHORT_SNAPSHOT_UPDATED" and "PROFILE_SKILLS" not in changed_dimensions:
            # Cohort membership changed alone: recompute aggregate O6 and O1 only
            return {
                "affected_modules": ["O6", "O1"],
                "recompute_order": ["O6", "O1"],
                "reason_codes": ["COHORT_AGGREGATE_REFRESH"],
                "skip_individual_m3_m4": True
            }

        if event_type in ["M2_TREND_SNAPSHOT_UPDATED", "M6_SCENARIO_CHANGED", "PROFILE_SKILL_STATE_UPDATED"]:
            return {
                "affected_modules": ["M3", "M4", "O6", "O1"],
                "recompute_order": ["M3", "M4", "O6", "O1"],
                "reason_codes": [f"{event_type}_DEPENDENCY_CASCADE"],
                "skip_individual_m3_m4": False
            }

        if event_type == "MANUAL_REPLAN_REQUESTED":
            return {
                "affected_modules": ["M3", "M4", "O6", "O1"],
                "recompute_order": ["M3", "M4", "O6", "O1"],
                "reason_codes": ["MANUAL_VERIFICATION_RECOMPUTE"],
                "skip_individual_m3_m4": False
            }

        # General cascade
        return {
            "affected_modules": ["M3", "M4", "O6", "O1"],
            "recompute_order": ["M3", "M4", "O6", "O1"],
            "reason_codes": ["GENERAL_DEPENDENCY_CASCADE"],
            "skip_individual_m3_m4": False
        }

    # -------------------------------------------------------------------------
    # 3. Structured Diffs (M3, M4, O6, O1)
    # -------------------------------------------------------------------------

    def diff_m3_outputs(
        self,
        prev_m3: Optional[Any],
        new_m3: Optional[Any]
    ) -> Dict[str, Any]:
        """
        Compares M3 future-role matching outputs over time:
        top role, top-N membership, role ranks, Match Index, and ECI deltas.
        """
        if not prev_m3 or not new_m3:
            return {"status": "NO_COMPARISON_AVAILABLE", "top_role_changed": False}

        p_list = self._normalize_m3_list(prev_m3)
        n_list = self._normalize_m3_list(new_m3)

        if not p_list or not n_list:
            return {"status": "EMPTY_MATCH_LISTS", "top_role_changed": False}

        top_prev = p_list[0]
        top_new = n_list[0]
        top_role_changed = (top_prev.get("masco_code") != top_new.get("masco_code"))

        # Top 3 membership
        p_top3 = {r.get("masco_code") for r in p_list[:3]}
        n_top3 = {r.get("masco_code") for r in n_list[:3]}
        top3_membership_changed = (p_top3 != n_top3)

        # Rank and score deltas
        p_map = {r.get("masco_code"): (idx + 1, r) for idx, r in enumerate(p_list)}
        n_map = {r.get("masco_code"): (idx + 1, r) for idx, r in enumerate(n_list)}

        rank_changes = []
        match_index_deltas = {}
        eci_deltas = {}

        for code, (n_rank, n_item) in n_map.items():
            if code in p_map:
                p_rank, p_item = p_map[code]
                delta_rank = p_rank - n_rank  # positive means improved rank
                delta_score = round(n_item.get("role_match_index", 0.0) - p_item.get("role_match_index", 0.0), 2)
                delta_eci = round(n_item.get("evidence_confidence_index", 0.0) - p_item.get("evidence_confidence_index", 0.0), 2)

                if delta_rank != 0:
                    rank_changes.append({
                        "masco_code": code,
                        "title": n_item.get("occupation_title"),
                        "old_rank": p_rank,
                        "new_rank": n_rank,
                        "delta_rank": delta_rank
                    })
                match_index_deltas[code] = delta_score
                eci_deltas[code] = delta_eci

        return {
            "top_recommended_role_changed": top_role_changed,
            "top_role_previous": {
                "masco_code": top_prev.get("masco_code"),
                "title": top_prev.get("occupation_title"),
                "match_index": top_prev.get("role_match_index")
            },
            "top_role_new": {
                "masco_code": top_new.get("masco_code"),
                "title": top_new.get("occupation_title"),
                "match_index": top_new.get("role_match_index")
            },
            "top3_membership_changed": top3_membership_changed,
            "rank_changes": rank_changes,
            "match_index_deltas": match_index_deltas,
            "eci_deltas": eci_deltas,
            "eci_notice": "EVIDENCE_CONFIDENCE_CHANGE: ECI reflects empirical source data reliability, NOT career desirability.",
            "structural_change": top_role_changed or top3_membership_changed
        }

    def diff_m4_outputs(
        self,
        prev_m4: Optional[Dict[str, Any]],
        new_m4: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compares M4 reskilling pathway outputs:
        CORE/IMPORTANT/SUPPORTING gaps, pathway steps, ordering, and hours.
        """
        if not prev_m4 or not new_m4:
            return {"status": "NO_COMPARISON_AVAILABLE", "structural_change": False}

        p_steps = prev_m4.get("pathway_steps", [])
        n_steps = new_m4.get("pathway_steps", [])

        p_step_skills = [s.get("skill_id") for s in p_steps]
        n_step_skills = [s.get("skill_id") for s in n_steps]

        p_core = {s.get("skill_id") for s in p_steps if s.get("requirement_tier") == "CORE"}
        n_core = {s.get("skill_id") for s in n_steps if s.get("requirement_tier") == "CORE"}
        core_added = sorted(list(n_core - p_core))
        core_removed = sorted(list(p_core - n_core))

        p_imp = {s.get("skill_id") for s in p_steps if s.get("requirement_tier") == "IMPORTANT"}
        n_imp = {s.get("skill_id") for s in n_steps if s.get("requirement_tier") == "IMPORTANT"}
        imp_added = sorted(list(n_imp - p_imp))
        imp_removed = sorted(list(p_imp - n_imp))

        p_sup = {s.get("skill_id") for s in p_steps if s.get("requirement_tier") == "SUPPORTING"}
        n_sup = {s.get("skill_id") for s in n_steps if s.get("requirement_tier") == "SUPPORTING"}
        sup_added = sorted(list(n_sup - p_sup))
        sup_removed = sorted(list(p_sup - n_sup))

        p_core_steps = {s.get("skill_id") for s in p_steps if s.get("requirement_tier") == "CORE"}
        n_core_steps = {s.get("skill_id") for s in n_steps if s.get("requirement_tier") == "CORE"}
        required_steps_added = sorted(list(n_core_steps - p_core_steps))
        required_steps_removed = sorted(list(p_core_steps - n_core_steps))

        p_rec_steps = {s.get("skill_id") for s in p_steps if s.get("requirement_tier") in ["IMPORTANT", "SUPPORTING"]}
        n_rec_steps = {s.get("skill_id") for s in n_steps if s.get("requirement_tier") in ["IMPORTANT", "SUPPORTING"]}
        recommended_steps_added = sorted(list(n_rec_steps - p_rec_steps))
        recommended_steps_removed = sorted(list(p_rec_steps - n_rec_steps))

        steps_added = sorted(list(set(n_step_skills) - set(p_step_skills)))
        steps_removed = sorted(list(set(p_step_skills) - set(n_step_skills)))
        order_changed = (p_step_skills != n_step_skills and set(p_step_skills) == set(n_step_skills))

        # Learning hours
        p_hrs_high = prev_m4.get("total_estimated_hours_high") or 0.0
        n_hrs_high = new_m4.get("total_estimated_hours_high") or 0.0
        hrs_delta = round(n_hrs_high - p_hrs_high, 1)
        band_delta = abs(hrs_delta) >= self.thresholds.get("learning_hours_substantial_band_delta", 40.0)

        structural = bool(core_added or core_removed or required_steps_added or required_steps_removed)

        return {
            "core_gaps_added": core_added,
            "core_gaps_removed": core_removed,
            "important_gaps_added": imp_added,
            "important_gaps_removed": imp_removed,
            "supporting_gaps_added": sup_added,
            "supporting_gaps_removed": sup_removed,
            "required_steps_added": required_steps_added,
            "required_steps_removed": required_steps_removed,
            "recommended_steps_added": recommended_steps_added,
            "recommended_steps_removed": recommended_steps_removed,
            "pathway_steps_added": steps_added,
            "pathway_steps_removed": steps_removed,
            "pathway_order_changed": order_changed,
            "learning_hours_delta": hrs_delta,
            "learning_hours_band_changed": band_delta,
            "structural_change": structural
        }

    def diff_o6_outputs(
        self,
        prev_o6: Optional[Dict[str, Any]],
        new_o6: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compares O6 SDG aggregation alignment prevalence and capability coverage.
        Explicitly disclaims 'impact change', framing strictly as 'SDG ALIGNMENT CONTEXT CHANGE'.
        """
        if not prev_o6 or not new_o6:
            return {"status": "NO_COMPARISON_AVAILABLE"}

        p_prev = prev_o6.get("sdg_alignment_prevalence", {})
        n_prev = new_o6.get("sdg_alignment_prevalence", {})

        deltas = {}
        for goal, n_val in n_prev.items():
            p_val = p_prev.get(goal, 0.0)
            diff = round(n_val - p_val, 4)
            if abs(diff) > 0.0001:
                deltas[goal] = diff

        return {
            "sdg_alignment_prevalence_deltas": deltas,
            "alignment_notice": "SDG_ALIGNMENT_CONTEXT_CHANGE: Changes represent descriptive capability alignment shifts, NOT verified corporate ESG impact scores."
        }

    def diff_o1_outputs(
        self,
        prev_o1: Optional[Dict[str, Any]],
        new_o1: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compares O1 workforce gap engine outputs:
        priority skills, ranks, indices, role transitions, and cohort roadmaps.
        Respects k=5 small-cell privacy and complementary suppression.
        """
        if not prev_o1 or not new_o1:
            return {"status": "NO_COMPARISON_AVAILABLE", "privacy_safe_diffs": []}

        p_prio = prev_o1.get("priority_skills", [])
        n_prio = new_o1.get("priority_skills", [])

        p_top = p_prio[0]["skill_id"] if p_prio else None
        n_top = n_prio[0]["skill_id"] if n_prio else None
        top_skill_changed = (p_top != n_top and p_top is not None and n_top is not None)

        p_map = {item["skill_id"]: (idx + 1, item) for idx, item in enumerate(p_prio)}
        n_map = {item["skill_id"]: (idx + 1, item) for idx, item in enumerate(n_prio)}

        p_top5 = set(list(p_map.keys())[:5])
        n_top5 = set(list(n_map.keys())[:5])
        top5_membership_changed = (p_top5 != n_top5)

        rank_changes = []
        privacy_safe_diffs = []

        for skill, (n_rank, n_item) in n_map.items():
            if skill in p_map:
                p_rank, p_item = p_map[skill]
                d_rank = p_rank - n_rank
                if d_rank != 0:
                    rank_changes.append({
                        "skill_id": skill,
                        "old_rank": p_rank,
                        "new_rank": n_rank,
                        "delta_rank": d_rank
                    })
                
                # Privacy-safe comparison
                p_cnt = p_item.get("affected_profile_count")
                n_cnt = n_item.get("affected_profile_count")
                safe_msg = self.build_privacy_safe_diff(
                    prev_val=p_item.get("affected_profile_count_display"),
                    new_val=n_item.get("affected_profile_count_display"),
                    prev_count=p_cnt,
                    new_count=n_cnt
                )
                privacy_safe_diffs.append({
                    "skill_id": skill,
                    "diff_message": safe_msg
                })

        return {
            "top_priority_skill_changed": top_skill_changed,
            "top5_membership_changed": top5_membership_changed,
            "rank_changes": rank_changes,
            "privacy_safe_diffs": privacy_safe_diffs,
            "governance_notice": "Workforce gap comparisons are strictly aggregate and MUST NOT be used for individual employee appraisals, compensation, or termination."
        }

    # -------------------------------------------------------------------------
    # 4. Privacy-Safe Diff String Generator
    # -------------------------------------------------------------------------

    def build_privacy_safe_diff(
        self,
        prev_val: Optional[str] = None,
        new_val: Optional[str] = None,
        prev_count: Optional[int] = None,
        new_count: Optional[int] = None
    ) -> str:
        """
        Constructs privacy-safe change text preventing small-cell leakage.
        Rules:
          - Both < 5: 'SUPPRESSED → SUPPRESSED'
          - <5 -> >=5: 'Previously suppressed; now above reporting threshold.' (No 4->5 leak!)
          - >=5 -> <5: 'Previously reportable; now below reporting threshold.' (No 5->4 leak!)
          - Both >= 5: Standard delta display.
        """
        p_is_supp = (prev_val == "<5" or prev_count is None or (prev_count is not None and prev_count < 5))
        n_is_supp = (new_val == "<5" or new_count is None or (new_count is not None and new_count < 5))

        if p_is_supp and n_is_supp:
            return self.config.get("privacy_safe_diff_strings", {}).get(
                "suppressed_to_suppressed", "SUPPRESSED → SUPPRESSED"
            )
        elif p_is_supp and not n_is_supp:
            return self.config.get("privacy_safe_diff_strings", {}).get(
                "suppressed_to_visible", "Previously suppressed; now above reporting threshold."
            )
        elif not p_is_supp and n_is_supp:
            return self.config.get("privacy_safe_diff_strings", {}).get(
                "visible_to_suppressed", "Previously reportable; now below reporting threshold."
            )
        else:
            p_c = prev_count if prev_count is not None else int(prev_val or 0)
            n_c = new_count if new_count is not None else int(new_val or 0)
            delta = n_c - p_c
            return f"{p_c} → {n_c} ({delta:+d})"

    # -------------------------------------------------------------------------
    # 5. Deterministic Materiality Classification
    # -------------------------------------------------------------------------

    def classify_materiality(
        self,
        diffs: Dict[str, Any],
        product_policy: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Classifies change materiality strictly following the deterministic hierarchy:
          HIGH_MATERIALITY > MATERIAL > MINOR > NONE.
        Structural changes strictly dominate raw numeric movements.
        """
        policy = product_policy or self.thresholds
        m3_diff = diffs.get("M3", {})
        m4_diff = diffs.get("M4", {})
        o1_diff = diffs.get("O1", {})

        # 1. HIGH_MATERIALITY (Structural Core Shifts)
        if m3_diff.get("top_recommended_role_changed"):
            return "HIGH_MATERIALITY"
        if m4_diff.get("core_gaps_added") or m4_diff.get("core_gaps_removed"):
            return "HIGH_MATERIALITY"
        if m4_diff.get("required_steps_added") or m4_diff.get("required_steps_removed"):
            return "HIGH_MATERIALITY"
        if diffs.get("safety_status_changed"):
            return "HIGH_MATERIALITY"

        # 2. MATERIAL (Substantial Secondary Shifts)
        if m3_diff.get("top3_membership_changed"):
            return "MATERIAL"
        if m4_diff.get("important_gaps_added") or m4_diff.get("important_gaps_removed"):
            return "MATERIAL"
        if m4_diff.get("recommended_steps_added") or m4_diff.get("recommended_steps_removed"):
            return "MATERIAL"
        if m4_diff.get("pathway_order_changed"):
            return "MATERIAL"
        if o1_diff.get("top_priority_skill_changed"):
            return "MATERIAL"
        if o1_diff.get("top5_membership_changed"):
            return "MATERIAL"
        if m4_diff.get("learning_hours_band_changed"):
            return "MATERIAL"

        # 3. Check for MINOR score movements
        has_minor_movement = False
        m_deltas = m3_diff.get("match_index_deltas", {})
        for d in m_deltas.values():
            if abs(d) > policy.get("hysteresis_margin", 0.02):
                has_minor_movement = True
                break

        if m3_diff.get("eci_deltas") or m4_diff.get("learning_hours_delta", 0.0) != 0.0:
            has_minor_movement = True

        if o1_diff.get("rank_changes"):
            has_minor_movement = True

        if has_minor_movement:
            return "MINOR"

        return "NONE"

    # -------------------------------------------------------------------------
    # 6. Change Explanation Generator (Deterministic Templates)
    # -------------------------------------------------------------------------

    def build_replan_explanation(
        self,
        trigger_type: str,
        root_causes: List[str],
        affected_modules: List[str],
        diffs: Dict[str, Any],
        source_versions: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Builds a deterministic, template-driven change explanation.
        Strictly avoids LLM causal hallucinations.
        """
        templates = []
        for rc in root_causes:
            if rc == "TREND_CHANGE":
                templates.append("Macro labor market evidence updated from M2 trend snapshot. Occupational shortage and momentum indicators adjusted.")
            elif rc == "SCENARIO_CHANGE":
                templates.append("Macroeconomic AI adoption scenario selection changed. Long-term occupational disruption/augmentation assumptions updated.")
            elif rc == "PROFILE_CHANGE":
                templates.append("Learner profile skill verification state updated. Confirmed competencies and gap boundaries recalculated.")
            elif rc == "COHORT_CHANGE":
                templates.append("Employer workforce cohort composition updated. Organizational skill gap prevalences refreshed under k=5 privacy safeguards.")
            elif rc == "MANUAL_RECOMPUTE":
                templates.append("User or system requested an explicit state re-verification.")
            elif rc == "MULTIPLE_INPUT_CHANGES":
                templates.append("Multiple independent input vectors changed simultaneously.")

        m3_diff = diffs.get("M3", {})
        if m3_diff.get("top_recommended_role_changed"):
            t_old = m3_diff.get("top_role_previous", {}).get("title")
            t_new = m3_diff.get("top_role_new", {}).get("title")
            templates.append(f"Top recommended target role changed from '{t_old}' to '{t_new}'.")

        m4_diff = diffs.get("M4", {})
        if m4_diff.get("core_gaps_added"):
            added_str = ", ".join(m4_diff.get("core_gaps_added"))
            templates.append(f"New CORE skill gap(s) identified: {added_str}.")
        if m4_diff.get("core_gaps_removed"):
            rem_str = ", ".join(m4_diff.get("core_gaps_removed"))
            templates.append(f"Previously missing CORE skill(s) resolved or dismissed: {rem_str}.")

        return {
            "trigger_type": trigger_type,
            "root_causes": root_causes,
            "affected_modules": affected_modules,
            "summary_narrative": " ".join(templates),
            "source_versions": source_versions,
            "explanation_method": "DETERMINISTIC_RULE_TEMPLATE_NO_LLM"
        }

    # -------------------------------------------------------------------------
    # 7. Event Validation & Ordering
    # -------------------------------------------------------------------------

    def validate_event_order(
        self,
        event: Dict[str, Any],
        current_accepted_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates event idempotency, sequence ordering, and upstream versions.
        """
        event_id = event.get("event_id")
        if not event_id:
            return {"valid": False, "status": "INVALID_EVENT", "reason": "Missing event_id"}

        # Duplicate event check
        if event_id in self.processed_event_ids:
            return {
                "valid": False,
                "status": "DUPLICATE_EVENT",
                "reason": f"Event '{event_id}' has already been processed. Replan ignored.",
                "quality_flags": ["DUPLICATE_EVENT"]
            }

        # Upstream version check
        claimed_versions = event.get("source_versions", {})
        for mod, claimed_v in claimed_versions.items():
            expected_v = self.PINNED_VERSIONS.get(mod)
            if expected_v and claimed_v != expected_v:
                return {
                    "valid": False,
                    "status": "UNSUPPORTED_UPSTREAM_VERSION",
                    "reason": f"Module {mod} version '{claimed_v}' is unsupported. Pinned baseline is '{expected_v}'.",
                    "quality_flags": ["UNSUPPORTED_UPSTREAM_VERSION"]
                }

        # Stale event check (timestamp comparison)
        event_ts = event.get("created_at") or event.get("timestamp")
        curr_ts = current_accepted_state.get("created_at")
        if event_ts and curr_ts:
            try:
                dt_event = datetime.fromisoformat(event_ts.replace("Z", "+00:00"))
                dt_curr = datetime.fromisoformat(curr_ts.replace("Z", "+00:00"))
                if dt_event < dt_curr:
                    return {
                        "valid": False,
                        "status": "STALE_EVENT",
                        "reason": f"Event timestamp '{event_ts}' is older than current accepted state '{curr_ts}'.",
                        "quality_flags": ["STALE_EVENT"]
                    }
            except Exception:
                pass

        return {"valid": True, "status": "VALID"}

    # -------------------------------------------------------------------------
    # 8. Candidate Replanning Execution Pipeline
    # -------------------------------------------------------------------------

    def execute_candidate_replan(
        self,
        previous_state: Dict[str, Any],
        event: Dict[str, Any],
        candidate_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes end-to-end candidate replanning:
          - Validates event order
          - Detects changes
          - Builds recompute plan
          - Computes diffs (M3, M4, O6, O1)
          - Classifies materiality
          - Generates privacy-safe change representation
          - Enforces human-acknowledgement status for material changes
          - Preserves previous accepted state
        """
        # 1. Validate Event
        val_res = self.validate_event_order(event, previous_state)
        event_id = event.get("event_id", "UNKNOWN_EVENT")
        trigger_type = event.get("trigger_type", "MANUAL_REPLAN_REQUESTED")

        if not val_res["valid"]:
            status = val_res["status"]
            return {
                "replan_id": f"REPLAN_{status}_{event_id}",
                "engine_version": self.VERSION,
                "previous_state_id": previous_state.get("state_id"),
                "candidate_state_id": None,
                "trigger_type": trigger_type,
                "state_changed": False,
                "materiality": "NONE",
                "publication_status": status,
                "quality_flags": val_res.get("quality_flags", []),
                "rejection_reason": val_res.get("reason"),
                "rollback_reference": previous_state.get("state_id"),
                "generated_at": datetime.now(timezone.utc).isoformat()
            }

        # Register event ID to enforce idempotency
        self.processed_event_ids.add(event_id)

        # 2. Detect State Changes
        change_info = self.detect_state_changes(previous_state, candidate_state)
        state_changed = change_info["state_changed"]
        root_causes = change_info["root_causes"]
        changed_dims = change_info["changed_dimensions"]

        # 3. Build Recompute Plan
        plan = self.build_recompute_plan(trigger_type, changed_dims)
        affected_mods = plan["affected_modules"]
        recompute_order = plan["recompute_order"]

        # 4. Compute Structured Diffs
        diff_m3 = self.diff_m3_outputs(previous_state.get("_raw_m3"), candidate_state.get("_raw_m3"))
        diff_m4 = self.diff_m4_outputs(previous_state.get("_raw_m4"), candidate_state.get("_raw_m4"))
        diff_o6 = self.diff_o6_outputs(previous_state.get("_raw_o6"), candidate_state.get("_raw_o6"))
        diff_o1 = self.diff_o1_outputs(previous_state.get("_raw_o1"), candidate_state.get("_raw_o1"))

        all_diffs = {
            "M3": diff_m3,
            "M4": diff_m4,
            "O6": diff_o6,
            "O1": diff_o1
        }

        # 5. Classify Materiality
        if not state_changed:
            materiality = "NONE"
        else:
            materiality = self.classify_materiality(all_diffs)

        # 6. Quality Flags
        quality_flags = ["SYNTHETIC_CHANGE_FIXTURE"]
        if materiality == "NONE":
            quality_flags.append("NO_SEMANTIC_CHANGE")
        elif materiality == "MINOR":
            quality_flags.append("MINOR_SCORE_MOVEMENT_ONLY")
        elif materiality == "MATERIAL":
            if diff_m3.get("top3_membership_changed"):
                quality_flags.append("MATERIAL_ROLE_CHANGE")
            if diff_m4.get("important_gaps_added") or diff_m4.get("important_gaps_removed"):
                quality_flags.append("CORE_GAP_CHANGE")
            if diff_m4.get("pathway_order_changed"):
                quality_flags.append("PATHWAY_STRUCTURE_CHANGE")
        elif materiality == "HIGH_MATERIALITY":
            quality_flags.append("HUMAN_ACKNOWLEDGEMENT_REQUIRED")
            if diff_m3.get("top_recommended_role_changed"):
                quality_flags.append("MATERIAL_ROLE_CHANGE")
            if diff_m4.get("core_gaps_added") or diff_m4.get("core_gaps_removed"):
                quality_flags.append("CORE_GAP_CHANGE")

        if "SCENARIO_CHANGE" in root_causes:
            quality_flags.append("SCENARIO_ASSUMPTION_CHANGE")
        if "COHORT_CHANGE" in root_causes:
            quality_flags.append("COHORT_COMPOSITION_CHANGE")

        quality_flags.extend([
            "PARTIAL_DIFFERENCING_PROTECTION",
            "NOT_FOR_EMPLOYMENT_DECISIONS"
        ])

        # 7. Publication Status (Automatic != Silent Mutation)
        if materiality in ["MATERIAL", "HIGH_MATERIALITY"]:
            pub_status = "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT"
        else:
            pub_status = "CURRENT_ACCEPTED"

        # 8. Compute Changeset Hash
        changeset_hash = self._compute_changeset_hash(all_diffs)

        # 9. Build Explanation
        explanation = self.build_replan_explanation(
            trigger_type=trigger_type,
            root_causes=root_causes,
            affected_modules=affected_mods,
            diffs=all_diffs,
            source_versions=self.PINNED_VERSIONS
        )

        now_ts = datetime.now(timezone.utc).isoformat()
        replan_id = f"REPLAN_{event_id}_{candidate_state.get('state_fingerprint', '')[:8]}"

        replan_package = {
            "replan_id": replan_id,
            "engine_version": self.VERSION,
            "previous_state_id": previous_state.get("state_id"),
            "candidate_state_id": candidate_state.get("state_id"),
            "trigger_type": trigger_type,
            "root_causes": root_causes,
            "state_changed": state_changed,
            "affected_modules": affected_mods,
            "recompute_order": recompute_order,
            "materiality": materiality,
            "changes": all_diffs,
            "privacy_safe_changes": diff_o1.get("privacy_safe_diffs", []),
            "explanation": explanation,
            "publication_status": pub_status,
            "previous_state_fingerprint": previous_state.get("state_fingerprint"),
            "candidate_state_fingerprint": candidate_state.get("state_fingerprint"),
            "changeset_hash": changeset_hash,
            "source_versions": self.PINNED_VERSIONS,
            "quality_flags": sorted(list(set(quality_flags))),
            "rollback_reference": previous_state.get("state_id"),
            "generated_at": now_ts
        }

        # 10. Audit Ledger
        self.record_replan_event(replan_package)
        return replan_package

    def record_replan_event(self, replan_package: Dict[str, Any]) -> None:
        """
        Appends an immutable replanning event to the audit ledger.
        """
        ledger_entry = {
            "event_id": f"EVT_{len(self.audit_ledger) + 1:04d}",
            "replan_id": replan_package.get("replan_id"),
            "previous_state_id": replan_package.get("previous_state_id"),
            "candidate_state_id": replan_package.get("candidate_state_id"),
            "trigger_type": replan_package.get("trigger_type"),
            "root_causes": replan_package.get("root_causes"),
            "materiality": replan_package.get("materiality"),
            "affected_modules": replan_package.get("affected_modules"),
            "recompute_order": replan_package.get("recompute_order"),
            "publication_status": replan_package.get("publication_status"),
            "previous_state_fingerprint": replan_package.get("previous_state_fingerprint"),
            "candidate_state_fingerprint": replan_package.get("candidate_state_fingerprint"),
            "changeset_hash": replan_package.get("changeset_hash"),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.audit_ledger.append(ledger_entry)

    def rollback_to_previous(self, replan_package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Rollback helper identifying and returning the previous accepted state snapshot.
        """
        prev_id = replan_package.get("rollback_reference") or replan_package.get("previous_state_id")
        return self._state_store.get(prev_id)

    # -------------------------------------------------------------------------
    # Helper Utilities
    # -------------------------------------------------------------------------

    def _hash_payload(self, payload: Any) -> str:
        if payload is None:
            return "NONE"
        try:
            s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        except TypeError:
            s = str(payload)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def _compute_changeset_hash(self, diffs: Dict[str, Any]) -> str:
        s = json.dumps(diffs, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def _normalize_m3_list(self, m3_out: Any) -> List[Dict[str, Any]]:
        if isinstance(m3_out, list):
            return m3_out
        if isinstance(m3_out, dict):
            if "role_matches" in m3_out:
                return m3_out["role_matches"]
            if "ranked_roles" in m3_out:
                return m3_out["ranked_roles"]
        return []
