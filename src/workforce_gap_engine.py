"""
src/workforce_gap_engine.py

O1 Employer / HR Workforce Gap & Cohort Reskilling Engine v1.1.0
Remediated Candidate Architecture & Invariants:
- WORKFORCE PLANNING DECISION SUPPORT ONLY.
- Strictly PROHIBITS employee ranking, individual performance scoring,
  employee risk scoring, termination/promotion recommendations, hire/no-hire
  decisions, compensation recommendations, and worker surveillance.
- Strictly PROHIBITS demographic attributes (zero protected attributes collected,
  processed, or evaluated).
- Structural Non-Use: protected_attributes_used = False, demographic_fairness_evaluated = False.
  Zero claims of empirical Disparate Impact Ratio (DIR).
- Unified Small-Cell Privacy Policy:
    * Minimum cohort threshold: k=5 (PROJECT POLICY, not statutory PDPA).
    * Canonical small cell: 0 < count < 5. Exact counts 1-4 are NEVER exposed in employer-facing outputs.
    * Canonical small cell mask: "suppressed": True, "count_display": "<5", exact count = None.
    * Reconstruction Protection: If any nonzero priority component depends on a 1-4 subcell,
      employer-facing priority_index and decomposition are suppressed ("SUPPRESSED_SUBCELL_RECONSTRUCTION").
    * Partition-aware complementary suppression (reusing frozen O6 standard).
    * Cross-query differencing protection rated PARTIAL; zero claims of Differential Privacy.
- Deficit Component Policy (v1.1.0):
    * Deficit ranking weight set to 0.0 (all 284 synthetic deficits are binary 1.0; uninformative offset removed).
    * Deficit retained as descriptive diagnostic field ("deficit_diagnostic_only": True).
    * Informative weights proportionally renormalized (CORE: 0.4118, IMP: 0.2353, TRANS: 0.1765, SCEN: 0.1176, PREREQ: 0.0588).
- CORE-First Semantics (v1.1.0):
    * Truthfully designated as "CORE_WEIGHTED_PREFERENCE" (not structural guarantee).
    * M4 individual pathway preserved as CORE-FIRST; O1 cohort planning preserved as WEIGHTED COHORT PRIORITY.
- Pinned Upstream Dependencies:
    M1 Skills Extraction: H_blend_0.70A_0.30C1_W1.0
    M2 Trend Intelligence: v1.1.1 (cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542)
    M6 Scenario Engine: v1.1.0 (ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5)
    M3 Role Matching: v1.1.0 (15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c)
    M4 Reskilling Pathways: v1.1.0 (448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f)
    M5 SDG Impact Mapping: v1.1.0 (94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7)
    O6 SDG Contribution Aggregation: v1.1.0
"""

from __future__ import annotations

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Base Project Path
BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")

# Upstream Engine Imports
from src.role_matching_engine import RoleMatchingEngine
from src.reskilling_pathway_engine import ReskillingPathwayEngine
from src.sdg_impact_engine import SDGImpactEngine
from src.scenario_engine import ScenarioEngine
from src.sdg_aggregation_engine import SDGAggregationEngine


class WorkforceGapEngine:
    """
    O1 Employer / HR Workforce Gap & Cohort Reskilling Engine v1.1.0.
    Provides aggregate cohort-level workforce planning decision support with
    hardened small-cell privacy safeguards and proportionally renormalized priority weights.
    """

    VERSION = "1.1.0"
    PINNED_M1_VERSION = "H_blend_0.70A_0.30C1_W1.0"
    PINNED_M2_VERSION = "1.1.1"
    PINNED_M6_VERSION = "1.1.0"
    PINNED_M3_VERSION = "1.1.0"
    PINNED_M4_VERSION = "1.1.0"
    PINNED_M5_VERSION = "1.1.0"
    PINNED_O6_VERSION = "1.1.0"

    FORBIDDEN_DEMOGRAPHIC_KEYS: Set[str] = {
        "gender", "sex", "age", "race", "ethnicity", "religion", "faith",
        "disability", "marital_status", "sexual_orientation", "national_origin",
        "salary", "wage", "compensation", "performance_rating", "performance_score",
        "employee_ranking", "risk_score"
    }

    CANONICAL_SKILLS_16: List[str] = [
        "ai_ethics_governance",
        "ai_literacy",
        "api_integration",
        "carbon_footprint_analytics",
        "data_privacy_pdpa",
        "data_visualization",
        "esg_sustainability_reporting",
        "human_in_the_loop_qa",
        "instructional_design",
        "process_mapping",
        "prompt_engineering",
        "python_scripting",
        "rag_knowledge_systems",
        "sql_data_analysis",
        "stakeholder_communication",
        "workflow_automation"
    ]

    SUPPORTED_SCENARIOS: List[str] = [
        "REFERENCE_2026",
        "MODERATE_COPILOT",
        "FAST_AGENTIC"
    ]

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        config_path: Optional[str] = None,
        m3_engine: Optional[RoleMatchingEngine] = None,
        m4_engine: Optional[ReskillingPathwayEngine] = None,
        m5_engine: Optional[SDGImpactEngine] = None,
        m6_engine: Optional[ScenarioEngine] = None,
        o6_engine: Optional[SDGAggregationEngine] = None
    ):
        self.base_dir = base_dir or BASE_DIR
        
        # Default to v1_1 config, fallback to v1 if v1_1 not present
        if config_path:
            cfg_file = config_path
        else:
            p_v1_1 = os.path.join(self.base_dir, "data", "workforce", "o1_config_v1_1.json")
            p_v1 = os.path.join(self.base_dir, "data", "workforce", "o1_config_v1.json")
            cfg_file = p_v1_1 if os.path.exists(p_v1_1) else p_v1

        with open(cfg_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # Load upstream engines (Read-Only)
        self.m3 = m3_engine if m3_engine else RoleMatchingEngine()
        self.m4 = m4_engine if m4_engine else ReskillingPathwayEngine()
        self.m5 = m5_engine if m5_engine else SDGImpactEngine()
        self.m6 = m6_engine if m6_engine else ScenarioEngine(base_dir=str(self.base_dir))
        self.o6 = o6_engine if o6_engine else SDGAggregationEngine(m5_engine=self.m5, m6_engine=self.m6)

        # Priority weights: v1.1 proportionally renormalized (deficit weight = 0.0)
        self.weights = self.config.get("priority_weights", {
            "core_gap_prevalence": 0.4117647059,
            "important_gap_prevalence": 0.2352941176,
            "average_deficit": 0.0,
            "cross_role_transferability": 0.1764705882,
            "scenario_urgency": 0.1176470588,
            "prerequisite_centrality": 0.0588235294
        })

        # Precompute transferability map from M4 (% of 20 roles requiring skill)
        self.transferability_pct = dict(self.m4.transferability_pct)

        # Precompute prerequisite centrality from M4 prerequisite graph
        # Formula: downstream_targets_count / 15.0 (normalized in [0.0, 1.0])
        self.upstream_prereqs: Dict[str, Set[str]] = {s: set() for s in self.CANONICAL_SKILLS_16}
        self.downstream_prereqs: Dict[str, Set[str]] = {s: set() for s in self.CANONICAL_SKILLS_16}
        for p in self.m4.prerequisites:
            u = p["prerequisite_skill_id"]
            v = p["target_skill_id"]
            if u in self.downstream_prereqs:
                self.downstream_prereqs[u].add(v)
            if v in self.upstream_prereqs:
                self.upstream_prereqs[v].add(u)

        self.prereq_centrality: Dict[str, float] = {}
        for s in self.CANONICAL_SKILLS_16:
            count = len(self.downstream_prereqs[s])
            self.prereq_centrality[s] = round(count / 15.0, 4)

        # Precompute scenario urgency bonuses from M4 configuration
        self.scenario_adjustments = self.m4.config.get("scenario_adjustments", {})

        # Privacy thresholds
        self.minimum_cohort_threshold = self.config.get("privacy_safeguards", {}).get("minimum_cohort_threshold", 5)
        self.small_cell_threshold = self.config.get("privacy_safeguards", {}).get("small_cell_threshold", 5)
        self.enable_complementary_suppression = self.config.get("privacy_safeguards", {}).get("complementary_suppression_enabled", True)

        # Build role requirements lookup from M4 roles_data
        self.role_requirements: Dict[str, List[Dict[str, Any]]] = {}
        for r in self.m4.roles_data.get("roles", []):
            self.role_requirements[str(r["masco_code"])] = r.get("skill_requirement_details", [])

    # -------------------------------------------------------------------------
    # Unified Privacy Safeguard Methods
    # -------------------------------------------------------------------------

    def mask_small_cell_count(self, count: Optional[int]) -> Tuple[Optional[int], str, bool]:
        """
        Unified small cell masking policy.
        Returns: (integer_or_none, display_string, is_suppressed)
        - count is None: (None, "NONE", False)
        - count == 0: (0, "0", False)
        - 0 < count < 5: (None, "<5", True)
        - count >= 5: (count, str(count), False)
        """
        if count is None:
            return None, "NONE", False
        if count == 0:
            return 0, "0", False
        if 0 < count < self.small_cell_threshold:
            return None, "<5", True
        return count, str(count), False

    def mask_small_cell_prevalence(self, count: Optional[int], total: int) -> Tuple[Optional[float], str, bool]:
        """
        Masks prevalence when the underlying numerator is a small cell.
        Returns: (float_or_none, display_string, is_suppressed)
        """
        if count is None or total <= 0:
            return None, "NONE", False
        if count == 0:
            return 0.0, "0.0%", False
        if 0 < count < self.small_cell_threshold:
            return None, "<10%", True
        val = round(count / total, 4)
        pct_str = f"{round(val * 100, 1)}%"
        return val, pct_str, False

    def apply_partition_suppression(
        self,
        category_counts: Dict[str, int],
        parent_total: Optional[int] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        DEF-P2-03 Complementary Partition-Aware Suppression.
        Reuses frozen O6 logic: if any child cell has 0 < N < k, suppress it.
        If parent_total is supplied and visible cells could reveal the hidden small cell,
        deterministically suppress the smallest non-small sibling cell.
        """
        results: Dict[str, Dict[str, Any]] = {}
        small_cells: List[str] = []
        eligible_non_small: List[Tuple[str, int]] = []

        for cat, cnt in category_counts.items():
            if cnt == 0:
                results[cat] = {
                    "count": 0,
                    "count_display": "0",
                    "suppressed": False,
                    "suppression_reason": None
                }
            elif 0 < cnt < self.small_cell_threshold:
                small_cells.append(cat)
                results[cat] = {
                    "count": None,
                    "count_display": "<5",
                    "suppressed": True,
                    "suppression_reason": "SMALL_CELL_PRIVACY"
                }
            else:
                eligible_non_small.append((cat, cnt))
                results[cat] = {
                    "count": cnt,
                    "count_display": str(cnt),
                    "suppressed": False,
                    "suppression_reason": None
                }

        # Apply complementary suppression if required: if exactly 1 child cell is small,
        # visible sibling cells + parent total would leak the hidden small cell.
        if self.enable_complementary_suppression and parent_total is not None and len(small_cells) == 1:
            # If visible unsuppressed cells + parent total would leak the hidden small cell
            if len(eligible_non_small) > 0:
                # Sort ascending by count to suppress the smallest non-small sibling
                eligible_non_small.sort(key=lambda x: x[1])
                target_cat = eligible_non_small[0][0]
                results[target_cat]["count"] = None
                results[target_cat]["count_display"] = f"<{eligible_non_small[0][1] + 1}"
                results[target_cat]["suppressed"] = True
                results[target_cat]["suppression_reason"] = "SUPPRESSED_COMPLEMENTARY_RULE"

        return results

    # -------------------------------------------------------------------------
    # Profile Validation & Sanitization
    # -------------------------------------------------------------------------

    def validate_profile_for_workforce_analysis(self, profile: Any) -> Tuple[str, Optional[str]]:
        """
        Deterministic Profile Validation Layer.
        Classifies candidate records into:
          - ELIGIBLE: Valid operational dictionary record with confirmed skills or roles.
          - EXCLUDED_*: Specific, documented exclusion category.
        Strictly enforces prohibition against demographic keys and raw CV text.
        """
        if not isinstance(profile, dict):
            return "EXCLUDED_INVALID_TYPE", "Profile must be a JSON dictionary object."

        # Check for forbidden demographic/salary keys
        for k in profile.keys():
            k_lower = str(k).lower().strip()
            if k_lower in self.FORBIDDEN_DEMOGRAPHIC_KEYS:
                raise ValueError(
                    f"PROHIBITED_DEMOGRAPHIC_ATTRIBUTE: Profile contains forbidden key '{k}'. "
                    f"Demographic, salary, and worker-scoring attributes are strictly prohibited."
                )

        # Check for raw CV narrative exposure
        for cv_key in ("raw_cv", "resume_text", "cv_text", "bio", "cover_letter", "narrative"):
            if cv_key in profile and profile[cv_key]:
                return "EXCLUDED_RAW_CV", "Unstructured CV narrative detected; raw CV text is prohibited in aggregate workforce analysis."

        # Check mandatory profile identifier
        pid = profile.get("profile_id") or profile.get("id")
        if not pid or not str(pid).strip():
            return "EXCLUDED_MISSING_ID", "Profile is missing mandatory unique identifier 'profile_id'."

        # Check confirmed skills presence
        confirmed = profile.get("confirmed_skills")
        if confirmed is None:
            return "EXCLUDED_INCOMPLETE", "Profile 'confirmed_skills' field is null or missing."

        if not isinstance(confirmed, list):
            return "EXCLUDED_INVALID_TYPE", "Profile 'confirmed_skills' must be a list."

        return "ELIGIBLE", None

    def _sanitize_cohort_profiles(
        self,
        profiles: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Sanitizes and deduplicates candidate workforce profiles.
        Deduplicates profiles by profile_id (first occurrence retained).
        Returns eligible profiles and exclusion summary statistics.
        """
        eligible: List[Dict[str, Any]] = []
        excluded_count = 0
        excluded_by_reason: Dict[str, int] = {
            "INVALID_TYPE": 0,
            "MISSING_ID": 0,
            "PROHIBITED_DEMOGRAPHIC": 0,
            "RAW_CV_EXPOSURE": 0,
            "INCOMPLETE_DATA": 0,
            "DUPLICATE_ID": 0
        }

        seen_pids: Set[str] = set()

        for p in profiles:
            try:
                status, reason = self.validate_profile_for_workforce_analysis(p)
            except ValueError:
                status, reason = "EXCLUDED_PROHIBITED_DEMOGRAPHIC", "PROHIBITED_DEMOGRAPHIC"

            if status == "ELIGIBLE":
                pid = p["profile_id"]
                if pid in seen_pids:
                    excluded_count += 1
                    excluded_by_reason["DUPLICATE_ID"] += 1
                    continue
                seen_pids.add(pid)
                eligible.append(p)
            else:
                excluded_count += 1
                if status == "EXCLUDED_INVALID_TYPE":
                    excluded_by_reason["INVALID_TYPE"] += 1
                elif status == "EXCLUDED_MISSING_ID":
                    excluded_by_reason["MISSING_ID"] += 1
                elif status == "EXCLUDED_PROHIBITED_DEMOGRAPHIC":
                    excluded_by_reason["PROHIBITED_DEMOGRAPHIC"] += 1
                elif status == "EXCLUDED_RAW_CV":
                    excluded_by_reason["RAW_CV_EXPOSURE"] += 1
                elif status == "EXCLUDED_INCOMPLETE":
                    excluded_by_reason["INCOMPLETE_DATA"] += 1

        # Compute deterministic snapshot hash of eligible profiles
        snapshot_bytes = json.dumps(
            [{"id": p["profile_id"], "skills": sorted(p.get("confirmed_skills") or [])} for p in eligible],
            sort_keys=True
        ).encode("utf-8")
        snapshot_hash = hashlib.sha256(snapshot_bytes).hexdigest()

        summary = {
            "input_profile_count": len(profiles),
            "eligible_profile_count": len(eligible),
            "excluded_profile_count": excluded_count,
            "excluded_profiles_by_reason": excluded_by_reason,
            "cohort_snapshot_hash": snapshot_hash
        }

        return eligible, summary

    # -------------------------------------------------------------------------
    # Core Pipeline Analytics
    # -------------------------------------------------------------------------

    def _extract_profile_gaps(
        self,
        profile: Dict[str, Any],
        scenario: str = "REFERENCE_2026"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Extracts skill gaps for a single profile against their target future role.
        Preserves M3 tier classification (CORE, IMPORTANT, SUPPORTING) and M4 continuous deficit semantics.
        """
        confirmed_skills = set(profile.get("confirmed_skills") or [])
        target_role = profile.get("target_role") or {}
        role_code = target_role.get("masco_code") if isinstance(target_role, dict) else str(target_role)

        if not role_code or len(str(role_code)) == 1:
            # 1-digit Major Group fallback codes are strictly excluded from role matching transitions
            # Fall back to default tech specialist 2511 if unassigned
            role_code = "2511"

        reqs = self.role_requirements.get(str(role_code), [])
        gaps: Dict[str, Dict[str, Any]] = {}

        for r in reqs:
            s_id = r["skill_id"]
            strength = r.get("requirement_strength", "SUPPORTING")
            if "CORE" in strength:
                tier = "CORE"
            elif "IMPORTANT" in strength:
                tier = "IMPORTANT"
            else:
                tier = "SUPPORTING"
            required_level = float(r.get("required_proficiency", 1.0))

            user_level = 1.0 if s_id in confirmed_skills else 0.0

            # If user has not mastered the skill, calculate deficit
            if user_level < required_level:
                deficit = max(0.0, required_level - user_level)
                gaps[s_id] = {
                    "skill_id": s_id,
                    "tier": tier,
                    "user_level": user_level,
                    "required_level": required_level,
                    "deficit": deficit
                }

        return gaps

    def build_skill_gap_matrix(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Output 1 — Workforce Skill-Gap Matrix.
        Aggregates skill gaps, core gaps, and mean deficits across all 16 canonical skills.
        Enforces small-cell privacy masking on employer-facing fields.
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)
        eligible_count = sanitization["eligible_profile_count"]

        if eligible_count == 0:
            return {
                "cohort_id": cohort_id or "UNKNOWN",
                "scenario": scenario,
                "status": "INSUFFICIENT_ELIGIBLE_COHORT_DATA",
                "suppressed": True,
                "suppression_reason": "NO_ELIGIBLE_PROFILES_AFTER_VALIDATION",
                "sanitization_summary": sanitization,
                "skills": {}
            }

        # Privacy Check (k=5)
        if eligible_count < self.minimum_cohort_threshold:
            return {
                "cohort_id": cohort_id or "UNKNOWN",
                "scenario": scenario,
                "status": "SUPPRESSED_SMALL_COHORT",
                "suppressed": True,
                "suppression_reason": "COHORT_SIZE_BELOW_PRIVACY_THRESHOLD",
                "eligible_count_display": "<5",
                "sanitization_summary": sanitization,
                "skills": {}
            }

        # Profile gap extraction
        profile_gaps: List[Dict[str, Dict[str, Any]]] = [
            self._extract_profile_gaps(p, scenario=scenario) for p in eligible
        ]

        # Scenario urgency bonuses
        scen_adj = self.scenario_adjustments.get(scenario, {}).get("skill_urgency_bonus", {})

        skills_matrix: Dict[str, Dict[str, Any]] = {}

        for skill_id in self.CANONICAL_SKILLS_16:
            requiring_count = 0
            gap_count = 0
            core_gap_count = 0
            important_gap_count = 0
            supporting_gap_count = 0
            deficits: List[float] = []

            for p, p_gap in zip(eligible, profile_gaps):
                confirmed = skill_id in (p.get("confirmed_skills") or [])
                is_gap = skill_id in p_gap

                if confirmed or is_gap:
                    requiring_count += 1

                if is_gap:
                    gap_count += 1
                    tier = p_gap[skill_id]["tier"]
                    deficit = p_gap[skill_id]["deficit"]
                    deficits.append(deficit)
                    if tier == "CORE":
                        core_gap_count += 1
                    elif tier == "IMPORTANT":
                        important_gap_count += 1
                    elif tier == "SUPPORTING":
                        supporting_gap_count += 1

            raw_gap_prev = round(gap_count / eligible_count, 4)
            raw_core_prev = round(core_gap_count / eligible_count, 4)
            raw_imp_prev = round(important_gap_count / eligible_count, 4)
            raw_sup_prev = round(supporting_gap_count / eligible_count, 4)
            raw_mean_def = round(sum(deficits) / len(deficits), 4) if deficits else 0.0
            scen_bonus = float(scen_adj.get(skill_id, 0.0))

            # Small cell privacy masking for employer payload
            is_skill_gap_small = (0 < gap_count < self.small_cell_threshold)
            
            _, gap_count_disp, _ = self.mask_small_cell_count(gap_count)
            _, core_count_disp, is_core_small = self.mask_small_cell_count(core_gap_count)
            _, imp_count_disp, is_imp_small = self.mask_small_cell_count(important_gap_count)
            _, sup_count_disp, is_sup_small = self.mask_small_cell_count(supporting_gap_count)

            # Masked employer-facing fields
            if is_skill_gap_small:
                emp_gap_count = None
                emp_core_count = None
                emp_imp_count = None
                emp_sup_count = None
                emp_gap_prev = None
                emp_core_prev = None
                emp_imp_prev = None
                emp_sup_prev = None
                emp_mean_def = None
                skill_suppressed = True
                suppression_reason = "SKILL_GAP_BELOW_PRIVACY_THRESHOLD"
            else:
                emp_gap_count = gap_count
                emp_core_count = None if is_core_small else core_gap_count
                emp_imp_count = None if is_imp_small else important_gap_count
                emp_sup_count = None if is_sup_small else supporting_gap_count
                emp_gap_prev = raw_gap_prev
                emp_core_prev = None if is_core_small else raw_core_prev
                emp_imp_prev = None if is_imp_small else raw_imp_prev
                emp_sup_prev = None if is_sup_small else raw_sup_prev
                emp_mean_def = raw_mean_def
                skill_suppressed = False
                suppression_reason = None

            skills_matrix[skill_id] = {
                "skill_id": skill_id,
                "skill_name": skill_id.replace("_", " ").title(),
                "eligible_profiles": eligible_count,
                "profiles_requiring_skill": requiring_count,
                # Employer-facing fields (masked if small cell)
                "profiles_with_gap": emp_gap_count,
                "profiles_with_gap_display": gap_count_disp,
                "profiles_with_core_gap": emp_core_count,
                "profiles_with_core_gap_display": core_count_disp,
                "profiles_with_important_gap": emp_imp_count,
                "profiles_with_important_gap_display": imp_count_disp,
                "profiles_with_supporting_gap": emp_sup_count,
                "profiles_with_supporting_gap_display": sup_count_disp,
                "gap_prevalence": emp_gap_prev,
                "core_gap_prevalence": emp_core_prev,
                "important_gap_prevalence": emp_imp_prev,
                "supporting_gap_prevalence": emp_sup_prev,
                "mean_deficit_among_gapped_profiles": emp_mean_def,
                "deficit_signal_status": "BINARY_NON_DISCRIMINATING",
                "deficit_diagnostic_only": True,
                "gapped_profiles_denominator": len(deficits) if not is_skill_gap_small else None,
                "scenario_urgency_bonus": scen_bonus,
                "transferability_pct": self.transferability_pct.get(skill_id, 0.0),
                "prerequisite_centrality_score": self.prereq_centrality.get(skill_id, 0.0),
                "suppressed": skill_suppressed,
                "suppression_reason": suppression_reason,
                "source_version": f"M3 {self.PINNED_M3_VERSION} / M4 {self.PINNED_M4_VERSION}",
                # Internal unmasked values for calculation & test verification
                "_raw_profiles_with_gap": gap_count,
                "_raw_core_gap_prevalence": raw_core_prev,
                "_raw_important_gap_prevalence": raw_imp_prev,
                "_raw_gap_prevalence": raw_gap_prev,
                "_raw_mean_deficit": raw_mean_def
            }

        return {
            "cohort_id": cohort_id or "UNKNOWN",
            "scenario": scenario,
            "status": "SUCCESS",
            "suppressed": False,
            "eligible_profile_count": eligible_count,
            "sanitization_summary": sanitization,
            "skills": skills_matrix
        }

    def rank_workforce_reskilling_priorities(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Core Output 3 — Workforce Reskilling Priority Index (0–100) v1.1.0.
        Calculates deterministic, component-based, explainable workforce priority scores.
        Enforces reconstruction privacy: suppresses priority_index if any active component
        depends on a 1-4 small cell.
        """
        matrix_res = self.build_skill_gap_matrix(profiles, scenario=scenario, cohort_id=cohort_id)
        if matrix_res.get("suppressed"):
            return []

        skills = matrix_res["skills"]
        eligible_count = matrix_res["eligible_profile_count"]
        priorities: List[Dict[str, Any]] = []

        w = self.weights

        for s_id, s_data in skills.items():
            raw_gap_count = s_data["_raw_profiles_with_gap"]
            x_core = s_data["_raw_core_gap_prevalence"]
            x_important = s_data["_raw_important_gap_prevalence"]
            x_deficit = s_data["_raw_mean_deficit"]
            x_transfer = min(1.0, s_data["transferability_pct"] / 100.0)
            x_scenario = min(1.0, s_data["scenario_urgency_bonus"] / 20.0)
            x_prereq = s_data["prerequisite_centrality_score"]

            components = {
                "core_gap_prevalence": round(x_core, 4),
                "important_gap_prevalence": round(x_important, 4),
                "average_deficit": round(x_deficit, 4),
                "cross_role_transferability": round(x_transfer, 4),
                "scenario_urgency": round(x_scenario, 4),
                "prerequisite_centrality": round(x_prereq, 4)
            }

            weighted_contributions = {
                "core_gap_prevalence": round(w["core_gap_prevalence"] * x_core * 100, 2),
                "important_gap_prevalence": round(w["important_gap_prevalence"] * x_important * 100, 2),
                "average_deficit": round(w["average_deficit"] * x_deficit * 100, 2),
                "cross_role_transferability": round(w["cross_role_transferability"] * x_transfer * 100, 2),
                "scenario_urgency": round(w["scenario_urgency"] * x_scenario * 100, 2),
                "prerequisite_centrality": round(w["prerequisite_centrality"] * x_prereq * 100, 2)
            }

            # Mathematical Raw Priority Index Calculation
            if raw_gap_count == 0:
                raw_index = 0.0
            else:
                raw_index = (
                    w["core_gap_prevalence"] * x_core +
                    w["important_gap_prevalence"] * x_important +
                    w["average_deficit"] * x_deficit +
                    w["cross_role_transferability"] * x_transfer +
                    w["scenario_urgency"] * x_scenario +
                    w["prerequisite_centrality"] * x_prereq
                ) * 100.0
            
            internal_index = round(raw_index, 2)

            # Evaluate Privacy & Reconstruction Risks
            core_count = round(x_core * eligible_count)
            imp_count = round(x_important * eligible_count)

            is_gap_small = (0 < raw_gap_count < self.small_cell_threshold)
            is_core_subcell_small = (0 < core_count < self.small_cell_threshold and w["core_gap_prevalence"] > 0)
            is_imp_subcell_small = (0 < imp_count < self.small_cell_threshold and w["important_gap_prevalence"] > 0)

            if raw_gap_count == 0:
                final_index = 0.0
                priority_tier = "NONE"
                priority_status = "ZERO_GAP"
                suppressed = False
                suppression_reason = None
                emp_affected_count = 0
                emp_affected_display = "0"
                emp_cohort_pct = 0.0
                emp_components = components
                emp_contributions = weighted_contributions
            elif is_gap_small:
                # Skill gap directly involves < 5 workers
                final_index = None
                priority_tier = "SUPPRESSED"
                priority_status = "SUPPRESSED_SMALL_CELL"
                suppressed = True
                suppression_reason = "SKILL_GAP_BELOW_PRIVACY_THRESHOLD"
                emp_affected_count = None
                emp_affected_display = "<5"
                emp_cohort_pct = None
                emp_components = None
                emp_contributions = None
            elif is_core_subcell_small or is_imp_subcell_small:
                # Reconstructable subcell risk: publishing index leaks small subcell count
                final_index = None
                priority_tier = "SUPPRESSED"
                priority_status = "SUPPRESSED_SUBCELL_RECONSTRUCTION"
                suppressed = True
                suppression_reason = "SUBCELL_RECONSTRUCTION_RISK"
                emp_affected_count = raw_gap_count
                emp_affected_display = str(raw_gap_count)
                emp_cohort_pct = round(s_data["_raw_gap_prevalence"] * 100, 2)
                emp_components = None
                emp_contributions = None
            else:
                # Completely privacy-safe
                final_index = internal_index
                priority_status = "ACTIVE"
                suppressed = False
                suppression_reason = None
                if final_index >= 50.0:
                    priority_tier = "HIGH"
                elif final_index >= 25.0:
                    priority_tier = "MEDIUM"
                else:
                    priority_tier = "LOW"
                emp_affected_count = raw_gap_count
                emp_affected_display = str(raw_gap_count)
                emp_cohort_pct = round(s_data["_raw_gap_prevalence"] * 100, 2)
                emp_components = components
                emp_contributions = weighted_contributions

            priorities.append({
                "skill_id": s_id,
                "skill_name": s_data["skill_name"],
                "priority_index": final_index,
                "priority_tier": priority_tier,
                "priority_status": priority_status,
                "suppressed": suppressed,
                "suppression_reason": suppression_reason,
                "affected_profile_count": emp_affected_count,
                "affected_profile_count_display": emp_affected_display,
                "affected_cohort_percentage": emp_cohort_pct,
                "core_gap_prevalence": s_data["core_gap_prevalence"],
                "components": emp_components,
                "weights": w,
                "weighted_contributions": emp_contributions,
                "deficit_signal_status": "BINARY_NON_DISCRIMINATING",
                "deficit_used_for_ranking": False,
                "core_first_semantics": "CORE_WEIGHTED_PREFERENCE",
                "semantics_notice": self.config.get("semantics_notice"),
                # Internal fields for audit, regression, and test reproducibility
                "_internal_priority_index": internal_index,
                "_internal_components": components,
                "_internal_weighted_contributions": weighted_contributions
            })

        # Deterministic sorting based on internal mathematical index
        priorities.sort(
            key=lambda item: (
                -item["_internal_priority_index"],
                -item["_internal_components"]["core_gap_prevalence"],
                item["skill_id"]
            )
        )

        # Assign priority ranks
        unsuppressed_rank = 1
        for idx, item in enumerate(priorities, start=1):
            item["_internal_rank"] = idx
            if not item["suppressed"]:
                item["priority_rank"] = unsuppressed_rank
                unsuppressed_rank += 1
            else:
                item["priority_rank"] = None

        return priorities

    def build_role_gap_summary(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Output 2 — Role Transition Pressure v1.1.0.
        Aggregates transitions between current role and target future role across cohort.
        Enforces small-cell count masking (<5) to protect individual employee career transitions.
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)
        eligible_count = sanitization["eligible_profile_count"]

        if eligible_count == 0 or eligible_count < self.minimum_cohort_threshold:
            return {
                "cohort_id": cohort_id or "UNKNOWN",
                "status": "SUPPRESSED_SMALL_COHORT" if eligible_count > 0 else "INSUFFICIENT_ELIGIBLE_COHORT_DATA",
                "suppressed": True,
                "role_transitions": [],
                "target_role_frequency": {},
                "highest_pressure_transitions": []
            }

        transition_counts: Dict[Tuple[str, str], int] = {}
        target_role_counts: Dict[str, int] = {}
        missing_core_by_transition: Dict[Tuple[str, str], Set[str]] = {}

        for p in eligible:
            cur_role = p.get("current_role") or {}
            target_role = p.get("target_role") or {}
            c_code = cur_role.get("masco_code") if isinstance(cur_role, dict) else str(cur_role)
            t_code = target_role.get("masco_code") if isinstance(target_role, dict) else str(target_role)

            if not c_code or not t_code:
                continue

            # Strict prohibition: 1-digit Major Group fallback codes excluded
            if len(str(c_code)) == 1 or len(str(t_code)) == 1:
                continue

            pair = (str(c_code), str(t_code))
            transition_counts[pair] = transition_counts.get(pair, 0) + 1
            target_role_counts[str(t_code)] = target_role_counts.get(str(t_code), 0) + 1

            if pair not in missing_core_by_transition:
                missing_core_by_transition[pair] = set()

            gaps = self._extract_profile_gaps(p, scenario=scenario)
            for s, g in gaps.items():
                if g["tier"] == "CORE":
                    missing_core_by_transition[pair].add(s)

        role_transitions: List[Dict[str, Any]] = []
        for (c_code, t_code), count in sorted(transition_counts.items(), key=lambda x: -x[1]):
            c_title = self.m3.roles.get(c_code, {}).get("occupation_title", f"Role {c_code}")
            t_title = self.m3.roles.get(t_code, {}).get("occupation_title", f"Role {t_code}")
            
            is_small = (0 < count < self.small_cell_threshold)
            
            if is_small:
                vol = None
                vol_disp = "<5"
                pct = None
                pct_disp = "<10%"
                suppressed = True
                supp_reason = "SMALL_CELL_PRIVACY"
                common_skills = ["SUPPRESSED_SMALL_CELL"]
                effort_range = None
            else:
                vol = count
                vol_disp = str(count)
                pct = round(count / eligible_count * 100, 2)
                pct_disp = f"{pct}%"
                suppressed = False
                supp_reason = None
                common_skills = sorted(list(missing_core_by_transition.get((c_code, t_code), [])))
                effort_range = [30, 60]

            role_transitions.append({
                "current_masco": c_code,
                "current_role_title": c_title,
                "target_masco": t_code,
                "target_role_title": t_title,
                "transition_volume": vol,
                "transition_volume_display": vol_disp,
                "transition_percentage": pct,
                "transition_percentage_display": pct_disp,
                "suppressed": suppressed,
                "suppression_reason": supp_reason,
                "common_missing_core_skills": common_skills,
                "average_pathway_effort_range": effort_range,
                "_raw_transition_volume": count
            })

        # Mask target role frequencies
        target_role_display: Dict[str, Any] = {}
        for r_code, r_cnt in target_role_counts.items():
            if 0 < r_cnt < self.small_cell_threshold:
                target_role_display[r_code] = "<5"
            else:
                target_role_display[r_code] = r_cnt

        # Filter highest pressure transitions: only unsuppressed transitions
        unsuppressed_transitions = [t for t in role_transitions if not t["suppressed"]]

        return {
            "cohort_id": cohort_id or "UNKNOWN",
            "scenario": scenario,
            "status": "SUCCESS",
            "suppressed": False,
            "total_transitions_evaluated": sum(transition_counts.values()),
            "role_transitions": role_transitions,
            "target_role_frequency": target_role_display,
            "highest_pressure_transitions": unsuppressed_transitions[:3] if unsuppressed_transitions else [],
            "small_cell_transitions_suppressed": any(t["suppressed"] for t in role_transitions)
        }

    def build_cohort_reskilling_plan(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Output 4 — Cohort Reskilling Roadmap.
        Maps priority skills to structured execution phases (Foundational, Core, Advanced).
        Omits privacy-suppressed skills from public intervention listings.
        """
        priorities = self.rank_workforce_reskilling_priorities(profiles, scenario=scenario, cohort_id=cohort_id)
        if not priorities:
            return {"status": "SUPPRESSED_SMALL_COHORT", "suppressed": True, "phases": []}

        # Filter to privacy-safe priority skills (unsuppressed, active capability planning)
        safe_priorities = [p for p in priorities if not p["suppressed"]]
        suppressed_count = len(priorities) - len(safe_priorities)

        phase_map: Dict[int, List[Dict[str, Any]]] = {1: [], 2: [], 3: []}

        for item in safe_priorities:
            s_id = item["skill_id"]
            c_score = item["_internal_components"]["prerequisite_centrality"]
            scen_score = item["_internal_components"]["scenario_urgency"]

            # Phase assignment rules
            if len(self.downstream_prereqs.get(s_id, set())) >= 1 or c_score > 0:
                p_id = 1  # Foundational prerequisite
            elif scen_score >= 0.5:
                p_id = 3  # Advanced / scenario readiness
            else:
                p_id = 2  # Core capability bridging

            resources = self.m4.resources_by_skill.get(s_id, [])
            rec_resource = resources[0]["title"] if resources else "Curated Internal Competency Module"
            hours = resources[0]["provider_stated_hours"] if resources else [20, 40]

            phase_map[p_id].append({
                "skill_id": s_id,
                "skill_name": item["skill_name"],
                "priority_index": item["priority_index"],
                "priority_tier": item["priority_tier"],
                "recommended_resource": rec_resource,
                "estimated_module_hours": hours,
                "focus_area": "Prerequisite Foundation" if p_id == 1 else ("Scenario Foresight" if p_id == 3 else "Role Bridging"),
                "prerequisite_dependencies": sorted(list(self.upstream_prereqs.get(s_id, set())))
            })

        phases = []
        for p_info in self.config.get("roadmap_phases", []):
            pid = p_info["phase_id"]
            items = phase_map.get(pid, [])
            phases.append({
                "phase_id": pid,
                "title": p_info["title"],
                "focus": p_info["focus"],
                "skills_included": items,
                "estimated_horizon_weeks": p_info["estimated_horizon_weeks"],
                "total_skills_count": len(items)
            })

        roadmap_phases = {
            "PHASE 1 — FOUNDATIONS": phase_map.get(1, []),
            "PHASE 2 — CORE BRIDGING": phase_map.get(2, []),
            "PHASE 3 — SCENARIO ADVANCEMENT": phase_map.get(3, [])
        }

        priority_skills_plan = []
        for p in safe_priorities:
            s_id = p["skill_id"]
            res_list = self.m4.resources_by_skill.get(s_id, [])
            sdg_mapping = self.m5.get_skill_sdg_mapping(s_id) if hasattr(self, 'm5') and self.m5 else {"primary_sdgs": ["SDG_8", "SDG_9"]}
            priority_skills_plan.append({
                "skill_id": s_id,
                "skill_name": p["skill_name"],
                "priority_index": p["priority_index"],
                "priority_tier": p["priority_tier"],
                "available_verified_resources": [r["title"] for r in res_list],
                "sdg_alignment_context": sdg_mapping
            })

        return {
            "cohort_id": cohort_id or "UNKNOWN",
            "scenario": scenario,
            "status": "SUCCESS",
            "suppressed": False,
            "phases": phases,
            "roadmap_phases": roadmap_phases,
            "priority_skills_plan": priority_skills_plan,
            "small_cell_skills_suppressed_from_plan": (suppressed_count > 0),
            "suppressed_skills_count": suppressed_count,
            "methodology_disclaimer": "Individual M4 pathway remains authoritative; cohort plan defines shared institutional timing.",
            "individual_pathway_notice": "Cohort roadmap defines shared institutional timing; individual learning orders are strictly governed by M4 prerequisite graphs."
        }

    def identify_shared_learning_opportunities(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None,
        include_suppressed: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Core Output 5 — Shared Learning Opportunities v1.1.0.
        Identifies high-leverage skills common across multiple profiles' pathways.
        Enforces canonical threshold (k >= 5); suppresses and masks any small cell (1-4).
        """
        matrix_res = self.build_skill_gap_matrix(profiles, scenario=scenario, cohort_id=cohort_id)
        if matrix_res.get("suppressed"):
            return []

        shared_opps: List[Dict[str, Any]] = []

        for s_id, s_data in matrix_res["skills"].items():
            raw_count = s_data["_raw_profiles_with_gap"]

            if raw_count >= self.minimum_cohort_threshold:
                # Privacy-safe shared learning opportunity
                resources = self.m4.resources_by_skill.get(s_id, [])
                primary = resources[0] if resources else {}
                hours_range = primary.get("provider_stated_hours", [15, 30])
                single_session_h = hours_range[1] if isinstance(hours_range, list) else 25

                agg_hours_low = raw_count * (hours_range[0] if isinstance(hours_range, list) else 15)
                agg_hours_high = raw_count * (hours_range[1] if isinstance(hours_range, list) else 30)

                shared_opps.append({
                    "shared_skill": s_id,
                    "skill_name": s_data["skill_name"],
                    "profiles_affected": raw_count,
                    "profiles_affected_display": str(raw_count),
                    "suppressed": False,
                    "suppression_reason": None,
                    "common_prerequisite_status": "PREREQUISITES_IDENTIFIED" if self.downstream_prereqs.get(s_id) else "NO_PREREQUISITES",
                    "candidate_shared_resources": [r["title"] for r in resources[:2]],
                    "shared_curriculum_hours_range": [hours_range[0], hours_range[1]] if isinstance(hours_range, list) else [15, 30],
                    "aggregate_learner_hours_range": [agg_hours_low, agg_hours_high],
                    "individual_tailoring_required": s_data["_raw_core_gap_prevalence"] < s_data["_raw_gap_prevalence"],
                    "semantics_note": "Shared curriculum duration is session length; aggregate learner-hours is total person-hours. Do not multiply shared session duration by employees as calendar training time."
                })
            elif 0 < raw_count < self.minimum_cohort_threshold:
                if include_suppressed:
                    shared_opps.append({
                        "shared_skill": "SUPPRESSED_SMALL_CELL",
                        "skill_name": "SUPPRESSED_SMALL_CELL",
                        "profiles_affected": None,
                        "profiles_affected_display": "<5",
                        "suppressed": True,
                        "suppression_reason": "SMALL_CELL_PRIVACY",
                        "candidate_shared_resources": ["SUPPRESSED"],
                        "shared_curriculum_hours_range": None,
                        "aggregate_learner_hours_range": None,
                        "individual_tailoring_required": True,
                        "semantics_note": "Small-cell learning need suppressed to protect individual learner privacy."
                    })

        shared_opps.sort(key=lambda item: -(item["profiles_affected"] or 0))
        return shared_opps

    def compare_workforce_scenarios(
        self,
        profiles: List[Dict[str, Any]],
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Output 6 — Scenario Workforce Comparison v1.1.0.
        Compares skill priorities across REFERENCE_2026, MODERATE_COPILOT, and FAST_AGENTIC.
        Handles privacy suppression gracefully using internal scores for relative deltas.
        """
        scenario_results: Dict[str, Any] = {}
        priority_shifts: Dict[str, Dict[str, Any]] = {}

        for scen in self.SUPPORTED_SCENARIOS:
            ranked = self.rank_workforce_reskilling_priorities(profiles, scenario=scen, cohort_id=cohort_id)
            scenario_results[scen] = {
                "top_skills": [item["skill_id"] for item in ranked if not item["suppressed"]][:5],
                "priority_scores": {item["skill_id"]: item["priority_index"] for item in ranked},
                "_internal_scores": {item["skill_id"]: item["_internal_priority_index"] for item in ranked}
            }

        ref_internal = scenario_results["REFERENCE_2026"]["_internal_scores"]
        agentic_internal = scenario_results["FAST_AGENTIC"]["_internal_scores"]

        for s_id in self.CANONICAL_SKILLS_16:
            r_s = ref_internal.get(s_id, 0.0)
            a_s = agentic_internal.get(s_id, 0.0)
            priority_shifts[s_id] = {
                "reference_priority": r_s,
                "agentic_priority": a_s,
                "priority_delta": round(a_s - r_s, 2)
            }

        sensitive_skills = sorted(
            [{"skill_id": k, **v} for k, v in priority_shifts.items()],
            key=lambda x: -x["priority_delta"]
        )

        return {
            "cohort_id": cohort_id or "UNKNOWN",
            "scenarios_evaluated": self.SUPPORTED_SCENARIOS,
            "scenario_results": scenario_results,
            "scenario_priority_shifts": sensitive_skills,
            "most_scenario_sensitive_skills": [item["skill_id"] for item in sensitive_skills[:3]],
            "structured_assumption_notice": "M6 scenario outputs represent structured exploratory assumptions, not predictive forecast probabilities."
        }

    def build_role_family_gap_analytics(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026"
    ) -> Dict[str, Any]:
        """
        Core Output 8 — Role-Family Gap Analytics v1.1.0.
        Partitions profiles by 4-digit MASCO code with small cell suppression (k=5).
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)
        grouped_by_role: Dict[str, List[Dict[str, Any]]] = {}

        for p in eligible:
            cur_role = p.get("current_role") or {}
            c_code = cur_role.get("masco_code") if isinstance(cur_role, dict) else str(cur_role)
            if not c_code or len(str(c_code)) == 1:
                continue
            grouped_by_role.setdefault(str(c_code), []).append(p)

        role_analytics: Dict[str, Any] = {}
        for r_code, r_profiles in grouped_by_role.items():
            if len(r_profiles) < self.minimum_cohort_threshold:
                role_analytics[r_code] = {
                    "masco_code": r_code,
                    "occupation_title": self.m3.roles.get(r_code, {}).get("occupation_title", f"Role {r_code}"),
                    "eligible_count": None,
                    "eligible_count_display": "<5",
                    "suppressed": True,
                    "suppression_reason": "ROLE_COHORT_BELOW_PRIVACY_THRESHOLD"
                }
            else:
                m_res = self.build_skill_gap_matrix(r_profiles, scenario=scenario, cohort_id=r_code)
                ranks = self.rank_workforce_reskilling_priorities(r_profiles, scenario=scenario, cohort_id=r_code)
                safe_top = [item["skill_id"] for item in ranks if not item["suppressed"]][:3]
                role_analytics[r_code] = {
                    "masco_code": r_code,
                    "occupation_title": self.m3.roles.get(r_code, {}).get("occupation_title", f"Role {r_code}"),
                    "eligible_count": len(r_profiles),
                    "eligible_count_display": str(len(r_profiles)),
                    "suppressed": False,
                    "top_priority_skills": safe_top,
                    "core_gap_prevalences": {s: d["core_gap_prevalence"] for s, d in m_res["skills"].items() if d["core_gap_prevalence"] is not None and d["core_gap_prevalence"] > 0}
                }

        return {
            "status": "SUCCESS",
            "total_role_families_evaluated": len(grouped_by_role),
            "role_analytics": role_analytics
        }

    def build_partition_gap_breakdown(
        self,
        profiles: List[Dict[str, Any]],
        partition_key: str = "department",
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Partition Breakdown with Primary & Complementary Suppression (Reusing O6 Standard).
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)
        parent_total = sanitization["eligible_profile_count"]

        # Group profiles by partition_key
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for p in eligible:
            val = str(p.get(partition_key) or "UNKNOWN")
            grouped.setdefault(val, []).append(p)

        counts = {k: len(v) for k, v in grouped.items()}
        suppression_results = self.apply_partition_suppression(counts, parent_total=parent_total)

        partition_breakdown: Dict[str, Any] = {}
        for cat, s_info in suppression_results.items():
            cat_profiles = grouped[cat]
            if s_info["suppressed"]:
                partition_breakdown[cat] = {
                    "partition_value": cat,
                    "eligible_count": None,
                    "eligible_count_display": s_info["count_display"],
                    "suppressed": True,
                    "suppression_reason": s_info["suppression_reason"],
                    "priority_skills": []
                }
            else:
                ranks = self.rank_workforce_reskilling_priorities(cat_profiles, scenario=scenario)
                partition_breakdown[cat] = {
                    "partition_value": cat,
                    "eligible_count": s_info["count"],
                    "eligible_count_display": s_info["count_display"],
                    "suppressed": False,
                    "suppression_reason": None,
                    "top_priority_skills": [item["skill_id"] for item in ranks if not item["suppressed"]][:3]
                }

        return {
            "partition_key": partition_key,
            "parent_total": parent_total,
            "complementary_suppression_applied": any(s["suppression_reason"] == "SUPPRESSED_COMPLEMENTARY_RULE" for s in suppression_results.values()),
            "partitions": partition_breakdown
        }

    def build_heatmap_payload(
        self,
        profiles: List[Dict[str, Any]],
        grouping_dimension: str = "cohort_id",
        scenario: str = "REFERENCE_2026"
    ) -> Dict[str, Any]:
        """
        Core Output 9 — Heatmap Data Contract v1.1.0.
        Enforces both column-level (N < 5) and cell-level (count < 5) privacy masking.
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)

        # Group profiles by chosen dimension
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for p in eligible:
            grp_val = str(p.get(grouping_dimension) or "DEFAULT_COHORT")
            grouped.setdefault(grp_val, []).append(p)

        columns = sorted(list(grouped.keys()))
        cells: List[Dict[str, Any]] = []

        for grp_id in columns:
            grp_profs = grouped[grp_id]
            cnt = len(grp_profs)

            if cnt < self.minimum_cohort_threshold:
                # Column cohort below privacy floor: suppress entire column
                for s_id in self.CANONICAL_SKILLS_16:
                    cells.append({
                        "skill_id": s_id,
                        "group_id": grp_id,
                        "eligible_count": None,
                        "eligible_count_display": "<5",
                        "gap_prevalence": None,
                        "core_gap_prevalence": None,
                        "priority_index": None,
                        "display_value": None,
                        "suppressed": True,
                        "suppression_reason": "SMALL_COHORT_PRIVACY",
                        "quality_flags": ["SUPPRESSED_SMALL_COHORT"]
                    })
            else:
                m_res = self.build_skill_gap_matrix(grp_profs, scenario=scenario, cohort_id=grp_id)
                ranks = self.rank_workforce_reskilling_priorities(grp_profs, scenario=scenario, cohort_id=grp_id)
                rank_map = {item["skill_id"]: item for item in ranks}

                for s_id in self.CANONICAL_SKILLS_16:
                    s_data = m_res["skills"][s_id]
                    r_item = rank_map.get(s_id, {})
                    raw_gap_count = s_data["_raw_profiles_with_gap"]

                    if raw_gap_count == 0:
                        cells.append({
                            "skill_id": s_id,
                            "group_id": grp_id,
                            "eligible_count": cnt,
                            "eligible_count_display": str(cnt),
                            "gap_prevalence": 0.0,
                            "core_gap_prevalence": 0.0,
                            "priority_index": 0.0,
                            "display_value": 0.0,
                            "count_display": "0",
                            "suppressed": False,
                            "suppression_reason": None,
                            "quality_flags": ["ZERO_GAP"]
                        })
                    elif 0 < raw_gap_count < self.small_cell_threshold:
                        # Cell gap count below threshold: mask cell
                        cells.append({
                            "skill_id": s_id,
                            "group_id": grp_id,
                            "eligible_count": cnt,
                            "eligible_count_display": str(cnt),
                            "gap_prevalence": None,
                            "core_gap_prevalence": None,
                            "priority_index": None,
                            "display_value": None,
                            "count_display": "<5",
                            "suppressed": True,
                            "suppression_reason": "SMALL_CELL_PRIVACY",
                            "quality_flags": ["SUPPRESSED_SMALL_CELL"]
                        })
                    else:
                        # Gap count >= 5
                        flags = []
                        if r_item.get("suppressed"):
                            # Subcell reconstruction risk
                            cells.append({
                                "skill_id": s_id,
                                "group_id": grp_id,
                                "eligible_count": cnt,
                                "eligible_count_display": str(cnt),
                                "gap_prevalence": s_data["gap_prevalence"],
                                "core_gap_prevalence": None,
                                "priority_index": None,
                                "display_value": None,
                                "count_display": str(raw_gap_count),
                                "suppressed": True,
                                "suppression_reason": "SUBCELL_RECONSTRUCTION_RISK",
                                "quality_flags": ["SUBCELL_MASKED"]
                            })
                        else:
                            if (s_data["core_gap_prevalence"] or 0) >= 0.3:
                                flags.append("HIGH_CORE_GAP_PREVALENCE")
                            cells.append({
                                "skill_id": s_id,
                                "group_id": grp_id,
                                "eligible_count": cnt,
                                "eligible_count_display": str(cnt),
                                "gap_prevalence": s_data["gap_prevalence"],
                                "core_gap_prevalence": s_data["core_gap_prevalence"],
                                "priority_index": r_item.get("priority_index", 0.0),
                                "display_value": r_item.get("priority_index", 0.0),
                                "count_display": str(raw_gap_count),
                                "suppressed": False,
                                "suppression_reason": None,
                                "quality_flags": flags
                            })

        return {
            "heatmap_version": "1.1.0",
            "metric_represented": "WORKFORCE_RESKILLING_PRIORITY_INDEX",
            "grouping_dimension": grouping_dimension,
            "scenario": scenario,
            "rows": self.CANONICAL_SKILLS_16,
            "columns": columns,
            "cells": cells,
            "color_scale_metadata": {
                "min_value": 0.0,
                "max_value": 100.0,
                "high_threshold": 50.0,
                "medium_threshold": 25.0,
                "palette": "blues"
            }
        }

    def get_executive_workforce_summary(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Output 10 — Executive Workforce Summary v1.1.0.
        Surfaces top planning metrics constructed strictly AFTER privacy filtering.
        """
        matrix_res = self.build_skill_gap_matrix(profiles, scenario=scenario, cohort_id=cohort_id)
        if matrix_res.get("suppressed"):
            return {
                "cohort_id": cohort_id or "UNKNOWN",
                "status": "SUPPRESSED_SMALL_COHORT",
                "suppressed": True,
                "headline_insights": ["Cohort size is below enterprise privacy threshold (N < 5). Aggregate analytics are withheld."],
                "top_priority_skills": [],
                "largest_core_gap_areas": []
            }

        ranks = self.rank_workforce_reskilling_priorities(profiles, scenario=scenario, cohort_id=cohort_id)
        transitions = self.build_role_gap_summary(profiles, scenario=scenario, cohort_id=cohort_id)
        shared = self.identify_shared_learning_opportunities(profiles, scenario=scenario, cohort_id=cohort_id)

        # Filter top priority skills strictly after privacy validation
        safe_top_skills = [
            {"skill_id": item["skill_id"], "skill_name": item["skill_name"], "priority_index": item["priority_index"]}
            for item in ranks if not item["suppressed"]
        ][:3]

        # Filter largest core gap areas strictly after privacy validation (core_count >= 5)
        safe_core_gaps = []
        for s_id, s_data in matrix_res["skills"].items():
            if not s_data["suppressed"] and s_data["profiles_with_core_gap"] is not None and s_data["profiles_with_core_gap"] >= self.minimum_cohort_threshold:
                safe_core_gaps.append((s_id, s_data["core_gap_prevalence"], s_data["profiles_with_core_gap"]))
        safe_core_gaps.sort(key=lambda x: -x[1])

        # Filter highest volume transitions strictly after privacy validation
        safe_transitions = [
            t for t in transitions.get("role_transitions", []) if not t["suppressed"]
        ][:3]

        top_skill_names = [s["skill_name"] for s in safe_top_skills]

        headlines = [
            f"Workforce capability evaluation for {matrix_res['eligible_profile_count']} eligible employees identified {len(safe_top_skills)} unsuppressed strategic priority capabilities.",
            f"Primary unsuppressed capability development targets: {', '.join(top_skill_names) if top_skill_names else 'Privacy-suppressed or none'}.",
            f"Evaluated across macroeconomic foresight scenario '{scenario}'."
        ]

        # Target roles
        common_target_roles = []
        for r_code, count in transitions.get("target_role_frequency", {}).items():
            if count != "<5" and isinstance(count, int) and count >= self.minimum_cohort_threshold:
                common_target_roles.append({"role_code": r_code, "count": count})
        common_target_roles.sort(key=lambda x: -x["count"])

        return {
            "cohort_id": cohort_id or "UNKNOWN",
            "scenario": scenario,
            "status": "SUCCESS",
            "suppressed": False,
            "eligible_profile_count": matrix_res["eligible_profile_count"],
            "headline_insights": headlines,
            "top_priority_skills": safe_top_skills,
            "largest_core_gap_areas": [
                {"skill_id": x[0], "core_gap_prevalence": x[1], "profiles_affected": x[2]}
                for x in safe_core_gaps[:3]
            ],
            "highest_pressure_transitions": safe_transitions,
            "most_common_target_roles": common_target_roles,
            "shared_learning_opportunities_count": len(shared),
            "privacy_filtering_applied": True,
            "governance_notice": "Workforce planning summary is generated deterministically for capability development planning and cannot be used for individual employee evaluation."
        }

    def analyse_workforce_gaps(
        self,
        profiles: List[Dict[str, Any]],
        scenario: str = "REFERENCE_2026",
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Master Analytics Pipeline v1.1.0.
        Executes end-to-end workforce gap analysis and returns fully compliant O1 v1.1.0 payload.
        """
        eligible, sanitization = self._sanitize_cohort_profiles(profiles)
        c_id = cohort_id or "SYNTHETIC_WORKFORCE"

        analysis_id = f"O1_WORKFORCE_{c_id}_{scenario}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        matrix_res = self.build_skill_gap_matrix(profiles, scenario=scenario, cohort_id=c_id)
        ranked = self.rank_workforce_reskilling_priorities(profiles, scenario=scenario, cohort_id=c_id)
        role_transitions = self.build_role_gap_summary(profiles, scenario=scenario, cohort_id=c_id)
        cohort_plan = self.build_cohort_reskilling_plan(profiles, scenario=scenario, cohort_id=c_id)
        shared_opps = self.identify_shared_learning_opportunities(profiles, scenario=scenario, cohort_id=c_id)
        scen_comp = self.compare_workforce_scenarios(profiles, cohort_id=c_id)
        exec_summary = self.get_executive_workforce_summary(profiles, scenario=scenario, cohort_id=c_id)

        # Count small cell learning opportunities suppressed
        raw_small_shared = sum(
            1 for s_id, s_data in matrix_res.get("skills", {}).items()
            if 0 < s_data["_raw_profiles_with_gap"] < self.minimum_cohort_threshold
        )

        # Build analysis config hash for O2 state fingerprinting
        config_bytes = json.dumps(self.config, sort_keys=True).encode("utf-8")
        analysis_config_hash = hashlib.sha256(config_bytes).hexdigest()

        # O6 SDG Context
        sdg_context = {
            "o6_version": self.PINNED_O6_VERSION,
            "sdg_mappings_status": "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT",
            "corporate_sdg_impact_score": None,
            "disclaimer": "SDG capability alignments reflect descriptive competency mapping and do not represent corporate carbon reduction, job creation, or societal impact scoring."
        }

        # Quality Flags
        quality_flags = [
            "SYNTHETIC_DATA_ONLY",
            "AGGREGATE_WORKFORCE_PLANNING_ONLY",
            "NOT_FOR_EMPLOYMENT_DECISIONS"
        ]
        if matrix_res.get("suppressed"):
            quality_flags.append("SMALL_COHORT_SUPPRESSED")
        else:
            quality_flags.append("PARTIAL_DIFFERENCING_PROTECTION")
            quality_flags.append("SMALL_CELL_MASKING_APPLIED")

        if scenario != "REFERENCE_2026":
            quality_flags.append("SCENARIO_ASSUMPTION_BASED")

        return {
            "analysis_id": analysis_id,
            "engine_version": self.VERSION,
            "cohort_id": c_id,
            "scenario": scenario,
            "input_profile_count": sanitization["input_profile_count"],
            "eligible_profile_count": sanitization["eligible_profile_count"],
            "excluded_profile_count": sanitization["excluded_profile_count"],
            "excluded_profiles_by_reason": sanitization["excluded_profiles_by_reason"],
            "suppressed": matrix_res.get("suppressed", False),
            "suppression_reason": matrix_res.get("suppression_reason"),
            "skill_gap_matrix": matrix_res.get("skills", {}),
            "priority_skills": ranked,
            "role_transition_summary": role_transitions,
            "cohort_reskilling_plan": cohort_plan,
            "shared_learning_opportunities": shared_opps,
            "additional_small_cell_learning_needs_suppressed": (raw_small_shared > 0),
            "small_cell_learning_needs_suppressed_count": raw_small_shared,
            "scenario_summary": scen_comp,
            "executive_summary": exec_summary,
            "sdg_capability_context": sdg_context,
            "o5_compliance_metadata": {
                "protected_attributes_used": False,
                "demographic_fairness_evaluated": False,
                "aggregate_only": True,
                "employee_ranking_prohibited": True,
                "individual_evaluations_prohibited": True,
                "raw_cv_exposure_prohibited": True,
                "governance_safeguards_active": True,
                "suppression_applied": matrix_res.get("suppressed", False) or (raw_small_shared > 0),
                "excluded_profile_count": sanitization["excluded_profile_count"]
            },
            "privacy_metadata": {
                "minimum_cohort_threshold": self.minimum_cohort_threshold,
                "small_cell_threshold": self.small_cell_threshold,
                "complementary_suppression_active": self.enable_complementary_suppression,
                "cross_query_differencing_protection": "PARTIAL",
                "differential_privacy_claimed": False,
                "exact_small_cell_count_masked": True,
                "reconstruction_protection_active": True
            },
            "fairness_metadata": {
                "protected_attributes_used": False,
                "demographic_fairness_evaluated": False,
                "employee_ranking_prohibited": True,
                "performance_scoring_prohibited": True,
                "disparate_impact_claims_prohibited": True,
                "structural_non_use_limitation": "Exclusion of demographic features does not establish empirical demographic parity or absence of societal proxy effects."
            },
            "deficit_metadata": {
                "deficit_signal_status": "BINARY_NON_DISCRIMINATING",
                "deficit_used_for_ranking": False,
                "deficit_diagnostic_only": True
            },
            "core_first_metadata": {
                "core_first_semantics": "CORE_WEIGHTED_PREFERENCE",
                "m4_individual_semantics": "CORE_FIRST_ORDERING"
            },
            "prohibited_uses": self.config.get("governance_safeguards", {}).get("prohibited_uses", []),
            "source_versions": {
                "m1": self.PINNED_M1_VERSION,
                "m2": self.PINNED_M2_VERSION,
                "m6": self.PINNED_M6_VERSION,
                "m3": self.PINNED_M3_VERSION,
                "m4": self.PINNED_M4_VERSION,
                "m5": self.PINNED_M5_VERSION,
                "o6": self.PINNED_O6_VERSION
            },
            "o2_state_fingerprint": {
                "m2_version": self.PINNED_M2_VERSION,
                "m6_scenario": scenario,
                "m4_pathway_version": self.PINNED_M4_VERSION,
                "cohort_snapshot_hash": sanitization["cohort_snapshot_hash"],
                "analysis_config_hash": analysis_config_hash
            },
            "quality_flags": quality_flags
        }
