"""
src/role_matching_engine.py

M3 Explainable Future-Role Matching Engine (v1.1.0)
Architecture & Principles:
- Skill-First Primacy: Demonstrable worker skill readiness dominates (w_M1 >= 55%).
- Macro Trend Grounding: Labor shortage & empirical momentum bounded (w_M2 <= 30%).
- Scenario Context: Multi-scenario AI foresight bounded (w_M6 <= 15%).
- Candidate Universe: Strictly 20 specific 4-digit MASCO occupations. Fallbacks excluded.
- Demographic Neutrality: Automatic sanitization & stripping of protected attributes.
- Decoupled Confidence: Match Strength / Transition Readiness is independent of Evidence Confidence.
- Continuous Low-Fit Gating: G(S_fit) = min(1.0, S_fit / 20.0) smoothly attenuates macro signals.
- Deterministic Tie-Breaking: final_match_index DESC, skill_fit DESC, masco_code ASC.
- Full Decomposed Explainability: Complete component breakdown; not a hiring decision.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Base Project Path
BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")


class RoleRankingResult(list):
    """
    List-compatible container for role ranking outcomes that also supports
    metadata dictionary access (status, message, warnings, role_matches).
    """
    def __init__(self, roles: List[Dict[str, Any]], status: str = "SUCCESS", message: str = "", warnings: Optional[List[str]] = None):
        super().__init__(roles)
        self.status = status
        self.message = message
        self.warnings = warnings or []

    def __getitem__(self, item: Any) -> Any:
        if isinstance(item, str):
            if item == "status":
                return self.status
            elif item == "message":
                return self.message
            elif item == "warnings":
                return self.warnings
            elif item == "role_matches":
                return list(self)
            raise KeyError(f"Invalid key '{item}' on RoleRankingResult.")
        return super().__getitem__(item)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


class RoleMatchingEngine:
    """
    Production M3 Explainable Role Matching Engine v1.1.0
    Implements multi-component explainable scoring respecting M6 downstream safety contracts.
    """

    VERSION = "1.1.0"
    CANDIDATE_GRANULARITY = "FOUR_DIGIT_OCCUPATION"
    EXCLUDED_FALLBACK_PREFIX = "MAJOR_"

    FORBIDDEN_DEMOGRAPHIC_KEYS = {
        "age", "gender", "sex", "race", "ethnicity", "religion", "marital_status",
        "nationality", "disability", "socioeconomic_background", "income",
        "postcode", "address", "school", "full_address", "family_status"
    }

    LEVEL1_SKILLS_CATALOG = {
        "ai_literacy", "prompt_engineering", "process_mapping", "sql_data_analysis",
        "python_scripting", "data_visualization", "workflow_automation", "human_in_the_loop_qa",
        "rag_knowledge_systems", "api_integration", "ai_ethics_governance", "data_privacy_pdpa",
        "esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication",
        "instructional_design"
    }

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        config_path: Optional[Path] = None,
        role_req_path: Optional[Path] = None
    ):
        self.base_dir = Path(base_dir) if base_dir else BASE_DIR
        self.data_dir = self.base_dir / "data"

        # Load scoring configuration v1.1.0 by default
        cfg_file = config_path or (self.data_dir / "matching" / "m3_scoring_config_v1_1.json")
        if not cfg_file.exists():
            cfg_file = self.data_dir / "matching" / "m3_scoring_config_v1.json"
        with open(cfg_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # Load role requirements catalog v1.1.0 by default
        req_file = role_req_path or (self.data_dir / "matching" / "role_requirements_v1_1.json")
        if not req_file.exists():
            req_file = self.data_dir / "matching" / "role_requirements_v1.json"
        with open(req_file, "r", encoding="utf-8") as f:
            self.role_catalog = json.load(f)

        # Index candidate roles by masco_code (strictly 4-digit only)
        self.roles: Dict[str, dict] = {}
        for r in self.role_catalog.get("roles", []):
            code = str(r["masco_code"])
            if r.get("entity_granularity") == self.CANDIDATE_GRANULARITY and not code.startswith(self.EXCLUDED_FALLBACK_PREFIX):
                self.roles[code] = r

        # Initialize Upstream Engines
        from src.trend_engine import TrendEngine
        from src.scenario_engine import ScenarioEngine
        self.trend_engine = TrendEngine(processed_dir=self.data_dir / "trends" / "processed", version="v1.1.1")
        self.scenario_engine = ScenarioEngine(base_dir=self.base_dir, version="1.1.0")

        self.user_confirm_weights = self.config["user_confirmation_weights"]
        self.req_strength_weights = self.config["skill_requirement_strength_weights"]
        self.guardrails = self.config["guardrails"]
        self.match_strength_tiers = self.config.get("match_strength_tiers", {})
        self.evidence_conf_cfg = self.config.get("evidence_confidence_config", {})

    def _sanitize_profile(self, profile: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """
        P2-3 Remediation: Sanitizes input profile by stripping protected demographic attributes.
        Returns a cleaned copy of the profile and a list of stripped keys.
        """
        clean_profile: Dict[str, Any] = {}
        stripped_keys: List[str] = []

        for k, v in profile.items():
            if k.lower() in self.FORBIDDEN_DEMOGRAPHIC_KEYS:
                stripped_keys.append(k)
            else:
                clean_profile[k] = v

        return clean_profile, stripped_keys

    def _normalize_user_skills(self, profile: Dict[str, Any]) -> Tuple[Dict[str, float], List[str], List[str]]:
        """
        Parses profile skills into a normalized dictionary of skill_id -> credit [0.0, 1.0].
        Respects user override hierarchy:
        DISMISSED (0.0) overrides inferred states.
        USER_CONFIRMED / USER_ADDED (1.0) > M1_CORE (0.85) > M1_SUGGESTED (0.50).
        Preserves unmapped/unknown skills in unmapped_skills.
        Returns: (skill_credits, unmapped_skills, warnings)
        """
        clean_prof, stripped_keys = self._sanitize_profile(profile)
        skill_credits: Dict[str, float] = {}
        unmapped_skills: List[str] = []
        warnings: List[str] = []

        if stripped_keys:
            warnings.append("PROTECTED_ATTRIBUTE_STRIPPED")

        # Explicit dismissals have priority over inferred suggestions
        dismissed: Set[str] = set()
        if "dismissed_skills" in clean_prof:
            dismissed = {str(s).strip().lower() for s in clean_prof["dismissed_skills"]}
            for d in dismissed:
                if d in self.LEVEL1_SKILLS_CATALOG:
                    skill_credits[d] = 0.0

        # Helper to process a skill with credit
        def _register_skill(raw_sk: str, credit: float, is_explicit_dismissal: bool = False):
            sk_id = str(raw_sk).strip().lower()
            if sk_id not in self.LEVEL1_SKILLS_CATALOG:
                unmapped_skills.append(sk_id)
                if "UNKNOWN_SKILL_NOT_SCORED" not in warnings:
                    warnings.append("UNKNOWN_SKILL_NOT_SCORED")
                return

            if is_explicit_dismissal or sk_id in dismissed:
                skill_credits[sk_id] = 0.0
                return

            # Keep highest credit if duplicate entry exists
            if sk_id in skill_credits:
                skill_credits[sk_id] = max(skill_credits[sk_id], credit)
            else:
                skill_credits[sk_id] = credit

        # Format A: dictionary of skill_id -> status string
        if "skills" in clean_prof and isinstance(clean_prof["skills"], dict):
            for sk, status in clean_prof["skills"].items():
                if status == "DISMISSED":
                    _register_skill(sk, 0.0, is_explicit_dismissal=True)
                else:
                    c = self.user_confirm_weights.get(status, self.user_confirm_weights.get("M1_CORE", 0.85))
                    _register_skill(sk, c)

        # Format B: structured keys
        if "user_confirmed_skills" in clean_prof:
            for sk in clean_prof["user_confirmed_skills"]:
                _register_skill(sk, self.user_confirm_weights["USER_CONFIRMED"])

        if "user_added_skills" in clean_prof:
            for sk in clean_prof["user_added_skills"]:
                _register_skill(sk, self.user_confirm_weights["USER_ADDED"])

        if "m1_inferred_skills" in clean_prof and isinstance(clean_prof["m1_inferred_skills"], dict):
            for sk in clean_prof["m1_inferred_skills"].get("core", []):
                _register_skill(sk, self.user_confirm_weights["M1_CORE"])
            for sk in clean_prof["m1_inferred_skills"].get("suggested", []):
                _register_skill(sk, self.user_confirm_weights["M1_SUGGESTED"])

        # Format C: flat list of skills (treated as USER_CONFIRMED by default)
        if "skills" in clean_prof and isinstance(clean_prof["skills"], list):
            for sk in clean_prof["skills"]:
                _register_skill(sk, self.user_confirm_weights["USER_CONFIRMED"])

        return skill_credits, unmapped_skills, warnings

    def get_role_skill_gaps(self, profile: Dict[str, Any], masco_code: str) -> Dict[str, Any]:
        """
        Extracts decomposed skill gaps for a candidate role without recommending courses.
        Separates gaps into CORE, IMPORTANT, and SUPPORTING categories.
        """
        code = str(masco_code).strip()
        if code not in self.roles:
            raise KeyError(f"Candidate role '{code}' not found in candidate 4-digit universe.")

        role = self.roles[code]
        user_skills, unmapped_skills, warnings = self._normalize_user_skills(profile)
        strengths = role.get("skill_requirement_strength", {})

        matched_skills = []
        missing_core = []
        missing_important = []
        missing_supporting = []

        for skill, strength in strengths.items():
            credit = user_skills.get(skill, 0.0)
            if credit >= 0.50:
                matched_skills.append({
                    "skill_id": skill,
                    "strength": strength,
                    "user_credit": credit
                })
            else:
                gap_item = {
                    "skill_id": skill,
                    "strength": strength,
                    "user_credit": credit,
                    "deficit": round(1.0 - credit, 2)
                }
                if strength == "CORE_REQUIREMENT":
                    missing_core.append(gap_item)
                elif strength == "IMPORTANT":
                    missing_important.append(gap_item)
                else:
                    missing_supporting.append(gap_item)

        total_core = sum(1 for s in strengths.values() if s == "CORE_REQUIREMENT")
        matched_core = total_core - len(missing_core)
        core_coverage_pct = round((matched_core / total_core * 100.0) if total_core > 0 else 0.0, 1)

        # Transition Distance Determination
        if core_coverage_pct >= 75.0 and len(missing_core) <= 1:
            transition_distance = "SHORT TRANSITION"
            distance_factor = 1.0
        elif core_coverage_pct >= 50.0 and len(missing_core) <= 2:
            transition_distance = "MODERATE TRANSITION"
            distance_factor = 0.75
        elif core_coverage_pct >= 25.0 or len(missing_core) <= 3:
            transition_distance = "SUBSTANTIAL TRANSITION"
            distance_factor = 0.45
        else:
            transition_distance = "LONG TRANSITION"
            distance_factor = 0.15

        return {
            "masco_code": code,
            "occupation_title": role["occupation_title"],
            "core_requirements_count": total_core,
            "matched_core_count": matched_core,
            "missing_core_count": len(missing_core),
            "core_coverage_pct": core_coverage_pct,
            "matched_skills": matched_skills,
            "missing_core_skills": missing_core,
            "missing_important_skills": missing_important,
            "missing_supporting_skills": missing_supporting,
            "total_gap_count": len(missing_core) + len(missing_important) + len(missing_supporting),
            "transition_distance": transition_distance,
            "transition_distance_factor": distance_factor
        }

    def _calculate_evidence_confidence(
        self,
        profile: Dict[str, Any],
        role: Dict[str, Any],
        m2_prof: Dict[str, Any],
        m6_prof: Dict[str, Any]
    ) -> Tuple[float, str, Dict[str, float], List[str]]:
        """
        P1-1 Remediation: Computes decoupled Evidence Confidence Index (0-100) and Label.
        Measures reliability and trustworthiness of evidence independently of Match Index.
        """
        cfg = self.evidence_conf_cfg
        comp_weights = cfg.get("component_weights", {
            "user_skill_certainty": 0.25,
            "role_completeness": 0.20,
            "mapping_confidence": 0.20,
            "m2_evidence_confidence": 0.20,
            "m6_scenario_stability": 0.15
        })

        # 1. User Skill Certainty (average certainty across user profile skills)
        user_skills, _, _ = self._normalize_user_skills(profile)
        positive_credits = [c for c in user_skills.values() if c > 0.0]
        if positive_credits:
            avg_credit = sum(positive_credits) / len(positive_credits)
            user_certainty = min(100.0, avg_credit * 100.0)
        else:
            user_certainty = 50.0  # neutral prior if zero skills present

        # 2. Role Completeness
        completeness = role.get("data_completeness", "COMPLETE")
        comp_score = cfg.get("role_completeness_scores", {}).get(completeness, 100.0)

        # 3. Mapping Confidence
        map_conf = role.get("mapping_confidence", "HIGH")
        map_score = cfg.get("mapping_confidence_scores", {}).get(map_conf, 100.0)

        # 4. M2 Evidence Confidence
        m2_conf = m2_prof.get("confidence_label", "MEDIUM")
        m2_score = cfg.get("m2_confidence_scores", {}).get(m2_conf, 75.0)

        # 5. M6 Scenario Stability
        stability = m6_prof.get("sensitivity_profile", {}).get("downside_risk_stability", "RESILIENT")
        m6_conf = m6_prof.get("scenario_confidence", "HIGH")
        if m6_conf == "MEDIUM" or stability == "VULNERABLE":
            m6_score = cfg.get("m6_stability_scores", {}).get("VULNERABLE", 55.0)
        elif stability == "MODERATE":
            m6_score = cfg.get("m6_stability_scores", {}).get("MODERATE", 80.0)
        else:
            m6_score = cfg.get("m6_stability_scores", {}).get("RESILIENT", 100.0)

        # Weighted raw composite
        raw_confidence = (
            comp_weights["user_skill_certainty"] * user_certainty +
            comp_weights["role_completeness"] * comp_score +
            comp_weights["mapping_confidence"] * map_score +
            comp_weights["m2_evidence_confidence"] * m2_score +
            comp_weights["m6_scenario_stability"] * m6_score
        )

        # 6. Quality Flag Penalties
        applied_penalties = []
        flag_penalties = cfg.get("quality_flag_penalties", {
            "PROXY_MAPPED_EVIDENCE": -5.0,
            "LOW_BASE_RESEARCH_SIGNAL": -5.0,
            "INSUFFICIENT_HISTORICAL_BASELINE": -5.0,
            "WEIGHT_SENSITIVE_RECOMMENDATION": -5.0
        })

        role_flags = set(role.get("quality_flags", []))
        m2_flags = set(m2_prof.get("quality_flags", []))
        all_flags = role_flags | m2_flags

        for flag, pen in flag_penalties.items():
            if flag in all_flags:
                raw_confidence += pen
                applied_penalties.append(flag)

        final_conf_index = round(max(0.0, min(100.0, raw_confidence)), 1)

        # Tier assignment
        tiers = cfg.get("confidence_tiers", {
            "HIGH": {"min_score": 75.0, "label": "HIGH"},
            "MEDIUM": {"min_score": 50.0, "label": "MEDIUM"},
            "LOW": {"min_score": 25.0, "label": "LOW"},
            "INSUFFICIENT": {"min_score": 0.0, "label": "INSUFFICIENT"}
        })

        if final_conf_index >= tiers["HIGH"]["min_score"]:
            conf_label = "HIGH"
        elif final_conf_index >= tiers["MEDIUM"]["min_score"]:
            conf_label = "MEDIUM"
        elif final_conf_index >= tiers["LOW"]["min_score"]:
            conf_label = "LOW"
        else:
            conf_label = "INSUFFICIENT"

        components = {
            "user_skill_certainty": round(user_certainty, 1),
            "role_completeness_score": comp_score,
            "mapping_confidence_score": map_score,
            "m2_confidence_score": m2_score,
            "m6_stability_score": m6_score
        }

        return final_conf_index, conf_label, components, applied_penalties

    def _calculate_component_scores(
        self,
        profile: Dict[str, Any],
        masco_code: str,
        scenario_id: str = "REFERENCE_2026",
        weight_config: str = "balanced_baseline"
    ) -> Dict[str, Any]:
        """Calculates decomposed score components for a specific candidate role."""
        code = str(masco_code).strip()
        role = self.roles[code]
        user_skills, unmapped_skills, warnings = self._normalize_user_skills(profile)
        strengths = role.get("skill_requirement_strength", {})

        # 1. Skill Fit Calculation
        earned_weight = 0.0
        total_req_weight = 0.0
        for skill, strength in strengths.items():
            w = self.req_strength_weights.get(strength, 0.50)
            credit = user_skills.get(skill, 0.0)
            earned_weight += w * credit
            total_req_weight += w

        current_skill_fit = round((earned_weight / total_req_weight * 100.0) if total_req_weight > 0 else 0.0, 1)

        # 2. Skill Gaps & Transition Distance
        gaps = self.get_role_skill_gaps(profile, code)
        core_coverage = gaps["core_coverage_pct"]
        gap_penalty = (
            1.0 * len(gaps["missing_core_skills"]) +
            0.5 * len(gaps["missing_important_skills"]) +
            0.2 * len(gaps["missing_supporting_skills"])
        )
        transition_factor = gaps["transition_distance_factor"]
        gap_transition_score = round(transition_factor * max(0.0, 100.0 - 15.0 * gap_penalty), 1)

        # 3. M2 Labor-Market Context
        m2_prof = self.trend_engine.get_role_trend(code)
        d_short = float(m2_prof.get("demand_shortage_level", 50.0))
        d_aug = float(m2_prof.get("augmentation_potential", 50.0))
        d_pol = float(m2_prof.get("policy_priority", 50.0))
        conf_label = m2_prof.get("confidence_label", "MEDIUM")
        m2_damping = self.guardrails["m2_confidence_damping"].get(conf_label, 0.80)

        # Weighted M2 index normalized to 0-100
        m2_raw = (0.15 * d_short + 0.05 * d_aug + 0.05 * d_pol) / 0.25
        m2_score = round(m2_raw * m2_damping, 1)

        # 4. M6 Scenario Context
        m6_prof = self.scenario_engine.get_role_scenario(code, scenario_id)
        sc_res = float(m6_prof.get("demand_resilience", 50.0))
        sc_aug = float(m6_prof.get("augmentation_opportunity", 50.0))
        sc_pres = float(m6_prof.get("transition_pressure", 50.0))

        # Net resilience: higher demand & augmentation, lower transition pressure
        sc_net = 0.50 * sc_res + 0.30 * sc_aug + 0.20 * (100.0 - sc_pres)

        # Scenario damping & flags
        sc_damping = 1.0
        if m6_prof.get("scenario_confidence") == "MEDIUM":
            sc_damping *= self.guardrails["m6_scenario_damping"]["medium_confidence_damping"]
        if m6_prof.get("sensitivity_profile", {}).get("downside_risk_stability") == "VULNERABLE":
            sc_damping *= self.guardrails["m6_scenario_damping"]["vulnerable_stability_damping"]

        m6_score = round(sc_net * sc_damping, 1)

        # 5. Composite Scoring using selected weight configuration
        w_cfg = self.config["weight_configurations"].get(weight_config, self.config["weight_configurations"]["balanced_baseline"])
        m1_w = w_cfg["m1_skill_weights"]
        m2_w = w_cfg["m2_labor_weights"]
        m6_w = w_cfg["m6_scenario_weights"]

        m1_composite = (
            (m1_w["current_skill_fit"] * current_skill_fit +
             m1_w["core_requirement_coverage"] * core_coverage +
             m1_w["gap_burden_and_transition"] * gap_transition_score) / m1_w["total_m1"]
        )

        # 6. P1-3 Remediation: Continuous Skill-Fit Gating
        # G(S_fit) = min(1.0, current_skill_fit / gating_threshold)
        # Smoothly attenuates contextual M2 and M6 signals at low skill fit without cliff
        gating_thresh = self.guardrails.get("skill_fit_gating_threshold", 20.0)
        gating_factor = min(1.0, current_skill_fit / gating_thresh) if gating_thresh > 0 else 1.0

        effective_m2 = gating_factor * m2_score
        effective_m6 = gating_factor * m6_score

        composite_raw = (
            m1_w["total_m1"] * m1_composite +
            m2_w["total_m2"] * effective_m2 +
            m6_w["total_m6"] * effective_m6
        )

        applied_guardrails = []
        if gating_factor < 1.0:
            applied_guardrails.append("LOW_FIT_CONTEXT_GATED")

        final_index = round(composite_raw, 1)

        # 7. P1-1 Remediation: Match Strength / Transition Readiness Tier
        if final_index >= 75.0 and gaps["core_coverage_pct"] >= 60.0:
            match_strength = "STRONG CURRENT FIT"
        elif final_index >= 50.0 and gaps["core_coverage_pct"] >= 30.0:
            match_strength = "GOOD FIT WITH GAPS"
        elif final_index >= 30.0:
            match_strength = "DEVELOPING TRANSITION"
        else:
            match_strength = "DISTANT TRANSITION"

        # 8. P1-1 Remediation: Decoupled Evidence Confidence
        conf_index, conf_label, conf_components, conf_flags = self._calculate_evidence_confidence(
            profile, role, m2_prof, m6_prof
        )

        return {
            "masco_code": code,
            "occupation_title": role["occupation_title"],
            "entity_granularity": role["entity_granularity"],
            "scenario_id": scenario_id,
            "weight_configuration": weight_config,
            "role_match_index": final_index,
            "match_strength_label": match_strength,
            "recommendation_confidence": match_strength,  # preserved for backward compatibility
            "evidence_confidence_index": conf_index,
            "evidence_confidence_label": conf_label,
            "evidence_confidence_components": conf_components,
            "confidence_reducing_flags": conf_flags,
            "core_requirements_count": gaps["core_requirements_count"],
            "matched_core_count": gaps["matched_core_count"],
            "missing_core_count": gaps["missing_core_count"],
            "core_coverage_pct": gaps["core_coverage_pct"],
            "components": {
                "current_skill_fit": current_skill_fit,
                "core_requirement_coverage_pct": core_coverage,
                "skill_gap_burden_score": gap_transition_score,
                "transition_distance": gaps["transition_distance"],
                "m1_worker_skill_composite": round(m1_composite, 1),
                "m2_labor_market_score": m2_score,
                "m2_effective_contribution": round(effective_m2, 1),
                "m2_confidence_label": conf_label,
                "m2_damping_factor": m2_damping,
                "m6_scenario_score": m6_score,
                "m6_effective_contribution": round(effective_m6, 1),
                "m6_scenario_outlook": m6_prof["scenario_outlook"],
                "m6_reskilling_urgency": m6_prof["reskilling_urgency"],
                "m6_damping_factor": sc_damping,
                "skill_fit_gating_factor": round(gating_factor, 3)
            },
            "gaps": gaps,
            "applied_guardrails": applied_guardrails,
            "data_completeness": role.get("data_completeness", "COMPLETE"),
            "unmapped_skills": unmapped_skills,
            "warnings": warnings
        }

    def rank_roles(
        self,
        profile: Dict[str, Any],
        scenario_id: str = "REFERENCE_2026",
        weight_config: str = "balanced_baseline"
    ) -> RoleRankingResult:
        """
        Ranks all 20 candidate 4-digit occupations for a user profile under a chosen scenario.
        Enforces:
        - P2-4: If profile has zero usable skills, returns INSUFFICIENT_PROFILE_DATA.
        - P1-3: Continuous low-fit gating (no artificial clamp jump).
        - P2-1: No 20% bubble swap post-sort.
        - P3-1: Deterministic tie-breaking: role_match_index DESC, current_skill_fit DESC, masco_code ASC.
        """
        clean_prof, stripped_keys = self._sanitize_profile(profile)
        user_skills, unmapped_skills, warnings = self._normalize_user_skills(profile)

        # P2-4 Remediation: Empty or non-competency profile
        positive_skills = {k: v for k, v in user_skills.items() if v > 0.0}
        if not positive_skills:
            return RoleRankingResult(
                roles=[],
                status="INSUFFICIENT_PROFILE_DATA",
                message="At least one confirmed, added, or inferred skill is required to generate career role matches.",
                warnings=warnings + ["INSUFFICIENT_PROFILE_DATA"]
            )

        scored_roles = []
        for code in self.roles:
            res = self._calculate_component_scores(profile, code, scenario_id=scenario_id, weight_config=weight_config)
            scored_roles.append(res)

        # P3-1 & P2-1 Remediation: Deterministic continuous ranking without bubble swap
        # Sort key: role_match_index DESC, current_skill_fit DESC, masco_code ASC
        scored_roles.sort(
            key=lambda x: (
                x["role_match_index"],
                x["components"]["current_skill_fit"],
                -int(x["masco_code"])
            ),
            reverse=True
        )

        # Assign 1-based ranks
        for rank_idx, r in enumerate(scored_roles, 1):
            r["rank"] = rank_idx

        return RoleRankingResult(roles=scored_roles, status="SUCCESS", warnings=warnings)

    def get_role_match(
        self,
        profile: Dict[str, Any],
        masco_code: str,
        scenario_id: str = "REFERENCE_2026",
        weight_config: str = "balanced_baseline"
    ) -> Dict[str, Any]:
        """Retrieves match details and components for a specific 4-digit role."""
        code = str(masco_code).strip()
        if code not in self.roles:
            raise KeyError(f"Candidate role '{code}' not found in candidate 4-digit universe.")

        clean_prof, stripped_keys = self._sanitize_profile(profile)
        user_skills, _, _ = self._normalize_user_skills(profile)
        positive_skills = {k: v for k, v in user_skills.items() if v > 0.0}
        if not positive_skills:
            # If empty, calculate single role score with zero skills
            return self._calculate_component_scores(profile, code, scenario_id=scenario_id, weight_config=weight_config)

        ranked = self.rank_roles(profile, scenario_id=scenario_id, weight_config=weight_config)
        for r in ranked:
            if r["masco_code"] == code:
                return r
        raise KeyError(f"Role '{code}' could not be matched.")

    def compare_role_scenarios(
        self,
        profile: Dict[str, Any],
        masco_code: str,
        weight_config: str = "balanced_baseline"
    ) -> Dict[str, Any]:
        """Compares match outcomes for a specific role across all 3 scenarios."""
        code = str(masco_code).strip()
        if code not in self.roles:
            raise KeyError(f"Candidate role '{code}' not found in candidate 4-digit universe.")

        results = {}
        for sc in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
            ranked = self.rank_roles(profile, scenario_id=sc, weight_config=weight_config)
            role_data = next((r for r in ranked if r["masco_code"] == code), None)
            if role_data is None:
                role_data = self._calculate_component_scores(profile, code, scenario_id=sc, weight_config=weight_config)
                role_data["rank"] = 0
            results[sc] = {
                "rank": role_data["rank"],
                "role_match_index": role_data["role_match_index"],
                "match_strength_label": role_data["match_strength_label"],
                "evidence_confidence_label": role_data["evidence_confidence_label"],
                "m6_scenario_outlook": role_data["components"]["m6_scenario_outlook"],
                "m6_reskilling_urgency": role_data["components"]["m6_reskilling_urgency"]
            }

        ref = results["REFERENCE_2026"]
        fast = results["FAST_AGENTIC"]
        rank_shift = fast["rank"] - ref["rank"]
        index_shift = round(fast["role_match_index"] - ref["role_match_index"], 1)

        return {
            "masco_code": code,
            "occupation_title": self.roles[code]["occupation_title"],
            "weight_configuration": weight_config,
            "scenarios": results,
            "fast_agentic_shift": {
                "rank_delta": rank_shift,
                "index_delta": index_shift,
                "sensitivity_note": "Positive shift indicates greater AI transformation advantage under accelerated diffusion."
            }
        }

    def explain_role_match(
        self,
        profile: Dict[str, Any],
        masco_code: str,
        scenario_id: str = "REFERENCE_2026",
        weight_config: str = "balanced_baseline"
    ) -> Dict[str, Any]:
        """
        Produces decomposed, human-readable, auditable explainability answers:
        - WHAT IS THE MATCH INDEX & MATCH STRENGTH?
        - WHAT IS THE EVIDENCE CONFIDENCE?
        - WHY DID THIS ROLE RECEIVE THIS SCORE?
        - WHICH OF THE WORKER'S SKILLS CONTRIBUTED?
        - WHAT SKILL GAPS MUST BE BRIDGED?
        - HOW MUCH DID LABOUR TRENDS (M2) AND AI SCENARIO FORESIGHT (M6) INFLUENCE THE RESULT?
        - SOURCE EVIDENCE AND CITATIONS.
        """
        m = self.get_role_match(profile, masco_code, scenario_id=scenario_id, weight_config=weight_config)
        role = self.roles[m["masco_code"]]
        comp = m["components"]
        gaps = m["gaps"]

        matched_names = [s["skill_id"].replace("_", " ").title() for s in gaps["matched_skills"]]
        missing_core_names = [s["skill_id"].replace("_", " ").title() for s in gaps["missing_core_skills"]]

        why_text = (
            f"The worker demonstrates {comp['current_skill_fit']}% weighted skill alignment with {role['occupation_title']}, "
            f"covering {gaps['matched_core_count']}/{gaps['core_requirements_count']} core requirements ({comp['core_requirement_coverage_pct']}%). "
            f"Transition distance is classified as {comp['transition_distance']}."
        )

        m2_text = (
            f"Empirical labour shortage is {comp['m2_labor_market_score']}/100 "
            f"(confidence: {comp['m2_confidence_label']}, damping: {comp['m2_damping_factor']}x, effective: {comp['m2_effective_contribution']}/100)."
        )

        m6_text = (
            f"Under {scenario_id}, scenario outlook is '{comp['m6_scenario_outlook']}' "
            f"with reskilling urgency '{comp['m6_reskilling_urgency']}', effective contribution {comp['m6_effective_contribution']}/100."
        )

        conf_text = (
            f"Evidence confidence is {m['evidence_confidence_label']} ({m['evidence_confidence_index']}/100) based on "
            f"role completeness ({m['data_completeness']}), mapping confidence ({role.get('mapping_confidence')}), "
            f"and upstream empirical data quality."
        )

        return {
            "masco_code": m["masco_code"],
            "occupation_title": role["occupation_title"],
            "scenario_id": scenario_id,
            "role_match_index": m["role_match_index"],
            "match_strength_label": m["match_strength_label"],
            "evidence_confidence_index": m["evidence_confidence_index"],
            "evidence_confidence_label": m["evidence_confidence_label"],
            "rank": m.get("rank", 0),
            "why_matched": why_text,
            "confidence_explanation": conf_text,
            "contributing_skills": matched_names if matched_names else ["None"],
            "missing_core_skills": missing_core_names if missing_core_names else ["None"],
            "missing_core_count": gaps["missing_core_count"],
            "matched_core_count": gaps["matched_core_count"],
            "total_core_count": gaps["core_requirements_count"],
            "transition_distance": comp["transition_distance"],
            "m2_labor_influence": m2_text,
            "m6_scenario_influence": m6_text,
            "evidence_citations": {
                "source_ids": role["requirement_source_ids"],
                "evidence_quote": role["requirement_evidence"],
                "source_dates": role["source_dates"]
            },
            "applied_guardrails": m["applied_guardrails"],
            "disclaimer": "DISCLAIMER: ROLE MATCH INDEX IS AN EXPLAINABLE ALIGNMENT METRIC — NOT A HIRING DECISION OR PROBABILITY OF EMPLOYMENT"
        }
