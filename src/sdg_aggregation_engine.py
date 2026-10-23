"""
sdg_aggregation_engine.py

O6 SDG Contribution Aggregation Engine v1.1.0
Author: Senior Sustainability Analytics Engineer, Privacy-Preserving Workforce Analyst,
        Enterprise Workforce Intelligence Architect and Responsible-AI Auditor.

Framework: UN 2030 Agenda for Sustainable Development (17 Goals, 169 Targets)
Consumes Frozen Upstream Systems:
- M5 SDG Impact Mapping Engine v1.1.0 (Read-Only)
- M6 Scenario Engine v1.1.0 (Read-Only)
- M4 Personalised Reskilling Pathway Engine v1.1.0 (Read-Only)
- M3 Role Matching Engine v1.1.0 (Read-Only)

Core Principle:
O6 is a DESCRIPTIVE ALIGNMENT ANALYTICS ENGINE, NOT an impact-measurement system.
Reports descriptive workforce sustainability capability and alignment prevalence
across individual, company cohort, and regional levels.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from datetime import datetime

from src.sdg_impact_engine import SDGImpactEngine
from src.scenario_engine import ScenarioEngine


class SDGAggregationEngine:
    """
    O6 SDG Contribution Aggregation Engine v1.1.0
    Encapsulates privacy-preserving multi-level aggregation of SDG alignment intelligence.
    Remediated in Stage 14C to resolve:
    - DEF-P1-01: Profile validation & denominator integrity
    - DEF-P2-01: Fairness claim semantics (demographic-feature exclusion, no empirical DIR claim)
    - DEF-P2-02: Differencing & partition-aware complementary suppression
    - DEF-P2-03: Canonical counting unit (i, t, tau) for mapping shares
    - DEF-P3-01: Pathway alignment coverage scope and disclaimers
    - DEF-P3-02: Regional representativeness runtime disclaimer
    """

    VERSION = "1.1.0"
    PINNED_M5_VERSION = "1.1.0"
    PINNED_M4_VERSION = "1.1.0"
    PINNED_M3_VERSION = "1.1.0"
    PINNED_M6_VERSION = "1.1.0"

    FORBIDDEN_DEMOGRAPHIC_KEYS = {
        "race", "religion", "gender", "ethnicity", "income", "school",
        "postcode", "family_background", "age", "marital_status",
        "nationality", "disability"
    }

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        m5_engine: Optional[SDGImpactEngine] = None,
        m6_engine: Optional[ScenarioEngine] = None,
        minimum_cohort_size: Optional[int] = None
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        if config_path:
            self.config_path = Path(config_path)
        else:
            default_v1_1 = base_dir / "data" / "aggregation" / "o6_config_v1_1.json"
            default_v1_0 = base_dir / "data" / "aggregation" / "o6_config_v1.json"
            self.config_path = default_v1_1 if default_v1_1.exists() else default_v1_0

        # Load O6 Configuration
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "version": self.VERSION,
                "engine_name": "O6 SDG Contribution Aggregation Engine",
                "privacy_safeguards": {
                    "minimum_cohort_size": 5,
                    "suppression_code": "SUPPRESSED_SMALL_COHORT",
                    "complementary_suppression_code": "SUPPRESSED_COMPLEMENTARY_RULE",
                    "enable_complementary_suppression": True,
                    "privacy_protection_level": "PROTOTYPE_PARTITION_SUPPRESSION",
                    "cross_query_differencing_protection": "PARTIAL"
                }
            }

        # Privacy configuration
        cfg_min_cohort = self.config.get("privacy_safeguards", {}).get("minimum_cohort_size", 5)
        self.minimum_cohort_size = minimum_cohort_size if minimum_cohort_size is not None else cfg_min_cohort
        self.suppression_code = self.config.get("privacy_safeguards", {}).get("suppression_code", "SUPPRESSED_SMALL_COHORT")
        self.complementary_suppression_code = self.config.get("privacy_safeguards", {}).get("complementary_suppression_code", "SUPPRESSED_COMPLEMENTARY_RULE")
        self.enable_complementary_suppression = self.config.get("privacy_safeguards", {}).get("enable_complementary_suppression", True)

        # Initialize M5 engine (Read-Only)
        self.m5 = m5_engine if m5_engine else SDGImpactEngine()
        if getattr(self.m5, "VERSION", "1.1.0") != self.PINNED_M5_VERSION:
            raise ValueError(f"M5 version mismatch: Expected {self.PINNED_M5_VERSION}, found {self.m5.VERSION}")

        # Initialize M6 engine (Read-Only)
        self.m6 = m6_engine if m6_engine else ScenarioEngine(base_dir=base_dir, version=self.PINNED_M6_VERSION)

        # Precompute canonical skill-to-SDG set for capability coverage denominator
        self._canonical_sdg_skills: Dict[int, Set[str]] = {sdg_id: set() for sdg_id in range(1, 18)}
        for skill_id, skill_data in self.m5.skill_mappings.items():
            for al in skill_data.get("primary_sdgs", []) + skill_data.get("secondary_sdgs", []):
                self._canonical_sdg_skills[al["sdg_id"]].add(skill_id)

    def _validate_clean_profile(self, profile: Dict[str, Any]) -> None:
        """Enforces zero demographic attributes policy."""
        if not isinstance(profile, dict):
            return
        for k in profile:
            if k.lower() in self.FORBIDDEN_DEMOGRAPHIC_KEYS:
                raise ValueError(
                    f"Demographic variable '{k}' is strictly prohibited in O6 SDG Aggregation Engine. "
                    "Protected attributes must never be collected or aggregated."
                )

    def validate_profile_for_aggregation(self, profile: Any) -> Tuple[str, Optional[str]]:
        """
        DEF-P1-01 Deterministic Profile Validation Layer.
        Classifies each candidate profile record into:
        - ('ELIGIBLE', None)
        - ('EXCLUDED_INVALID_TYPE', 'INVALID_PROFILE_TYPE')
        - ('EXCLUDED_INCOMPLETE', 'INCOMPLETE_PROFILE_DATA')
        """
        # 1. Type validation
        if not isinstance(profile, dict):
            return ("EXCLUDED_INVALID_TYPE", "INVALID_PROFILE_TYPE")

        # 2. Demographic policy check (raises ValueError if forbidden demographic key present)
        self._validate_clean_profile(profile)

        # 3. Stable synthetic profile identifier check
        pid = profile.get("profile_id")
        if not pid or not isinstance(pid, str) or not pid.strip():
            return ("EXCLUDED_INCOMPLETE", "INCOMPLETE_PROFILE_DATA")

        # 4. Content completeness check
        # A profile must contain at least one operational attribute:
        # role data, confirmed skills collection, target role, or reskilling pathway.
        # Empty dict {} or profiles with zero operational competencies are incomplete.
        has_role = bool(profile.get("current_role"))
        has_skills = bool(profile.get("confirmed_skills"))
        has_target_role = bool(profile.get("target_role"))
        has_pathway = bool(profile.get("reskilling_pathway"))

        if not (has_role or has_skills or has_target_role or has_pathway):
            return ("EXCLUDED_INCOMPLETE", "INCOMPLETE_PROFILE_DATA")

        return ("ELIGIBLE", None)

    def aggregate_individual_alignment(
        self,
        profile: Dict[str, Any],
        time_dimension: str = "CURRENT"
    ) -> Dict[str, Any]:
        """
        Level 1: INDIVIDUAL ALIGNMENT VIEW
        Aggregates qualitative SDG alignments for a single synthetic profile.

        Descriptive counts only:
        - NO personal SDG impact score.
        - NO employee ranking by sustainability virtue.
        - NO comparison of 'better/worse person'.
        """
        status, reason = self.validate_profile_for_aggregation(profile)
        if status != "ELIGIBLE":
            raise ValueError(f"Cannot aggregate individual alignment for ineligible profile: {reason}")

        pid = profile.get("profile_id", "UNKNOWN_PROFILE")
        cohort_id = profile.get("cohort_id", "UNKNOWN_COHORT")
        region_id = profile.get("region_id", "UNKNOWN_REGION")

        time_dim = time_dimension.upper()
        if time_dim not in ("CURRENT", "POST_PATHWAY"):
            raise ValueError(f"Unsupported time_dimension '{time_dimension}'. Must be 'CURRENT' or 'POST_PATHWAY'.")

        # Extract current role and confirmed skills with safe defaults (DEF-P1-01)
        cur_role_data = profile.get("current_role") or {}
        cur_masco = cur_role_data.get("masco_code") if isinstance(cur_role_data, dict) else str(cur_role_data)
        confirmed_skills = set(list(profile.get("confirmed_skills") or []))

        # Extract reskilling pathway with safe defaults
        pathway_data = profile.get("reskilling_pathway") or {}
        pathway_skills = set(list(pathway_data.get("planned_skills") or []))

        target_role_data = profile.get("target_role") or {}
        target_masco = target_role_data.get("masco_code") if isinstance(target_role_data, dict) else str(target_role_data)

        # Active competency set for the selected time dimension
        active_skills = set(confirmed_skills)
        active_role_masco = cur_masco

        if time_dim == "POST_PATHWAY":
            # Scenario: assumes planned pathway skills have been acquired
            active_skills.update(pathway_skills)
            if target_masco and target_masco in self.m5.role_mappings:
                active_role_masco = target_masco

        # Unique relations set for DEF-P2-03: (profile_id, target_id, mapping_type)
        unique_relations: Set[Tuple[str, str, str]] = set()

        # Query M5 Role Mapping
        role_alignment_records = []
        role_sdgs: Set[int] = set()
        role_quality_flags: Set[str] = set()
        if active_role_masco and str(active_role_masco) in self.m5.role_mappings:
            r_map = self.m5.get_role_sdg_mapping(str(active_role_masco))
            role_quality_flags.update(r_map.get("quality_flags", []))
            for al in r_map.get("primary_sdgs", []) + r_map.get("secondary_sdgs", []):
                role_sdgs.add(al["sdg_id"])
                t_id = al["target_id"]
                m_type = al["mapping_type"]
                unique_relations.add((pid, t_id, m_type))
                role_alignment_records.append({
                    "sdg_id": al["sdg_id"],
                    "sdg_name": self.m5.goals[al["sdg_id"]]["name"],
                    "target_id": t_id,
                    "mapping_type": m_type,
                    "alignment_strength": al.get("alignment_strength", "MODERATE"),
                    "confidence": al.get("confidence", "HIGH"),
                    "contribution_pathway": al.get("contribution_pathway", ""),
                    "evidence_references": al.get("evidence_references", ""),
                    "source": "ROLE",
                    "masco_code": active_role_masco
                })

        # Query M5 Skill Mappings
        skill_alignment_records = []
        skill_sdgs: Set[int] = set()
        skills_by_sdg: Dict[int, List[str]] = {s: [] for s in range(1, 18)}
        skill_quality_flags: Set[str] = set()

        for s_id in sorted(active_skills):
            if s_id in self.m5.skill_mappings:
                s_map = self.m5.get_skill_sdg_mapping(s_id)
                skill_quality_flags.update(s_map.get("quality_flags", []))
                for al in s_map.get("primary_sdgs", []) + s_map.get("secondary_sdgs", []):
                    sdg_num = al["sdg_id"]
                    t_id = al["target_id"]
                    m_type = al["mapping_type"]
                    skill_sdgs.add(sdg_num)
                    skills_by_sdg[sdg_num].append(s_id)
                    unique_relations.add((pid, t_id, m_type))
                    skill_alignment_records.append({
                        "sdg_id": sdg_num,
                        "sdg_name": self.m5.goals[sdg_num]["name"],
                        "target_id": t_id,
                        "mapping_type": m_type,
                        "alignment_strength": al.get("alignment_strength", "MODERATE"),
                        "confidence": al.get("confidence", "HIGH"),
                        "contribution_pathway": al.get("contribution_pathway", ""),
                        "evidence_references": al.get("evidence_references", ""),
                        "source": "SKILL",
                        "skill_id": s_id
                    })

        # Pathway-specific alignment statistics
        pathway_aligned_skills = set()
        for ps in pathway_skills:
            if ps in self.m5.skill_mappings:
                ps_map = self.m5.get_skill_sdg_mapping(ps)
                if ps_map.get("primary_sdgs") or ps_map.get("secondary_sdgs"):
                    pathway_aligned_skills.add(ps)

        pathway_alignment_prevalence = (
            len(pathway_aligned_skills) / len(pathway_skills)
            if pathway_skills else 0.0
        )

        # Consolidate all alignments
        all_alignments = role_alignment_records + skill_alignment_records
        all_aligned_sdgs = sorted(list(role_sdgs.union(skill_sdgs)))

        # Deduplicate targets covered
        all_targets_covered = sorted(list(set(al["target_id"] for al in all_alignments)))

        # Mapping type counts based on unique (i, t, tau) relations
        direct_rel_count = sum(1 for r in unique_relations if r[2] == "DIRECT")
        enabling_rel_count = sum(1 for r in unique_relations if r[2] == "ENABLING")
        contextual_rel_count = sum(1 for r in unique_relations if r[2] == "CONTEXTUAL")

        mapping_type_counts = {
            "DIRECT": direct_rel_count,
            "ENABLING": enabling_rel_count,
            "CONTEXTUAL": contextual_rel_count
        }

        # Confidence counts
        confidence_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for al in all_alignments:
            conf = al.get("confidence", "HIGH")
            if conf in confidence_counts:
                confidence_counts[conf] += 1

        # Aggregate Quality Flags
        quality_flags = set(["SYNTHETIC_DATA_ONLY", "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT"])
        quality_flags.update(role_quality_flags)
        quality_flags.update(skill_quality_flags)
        if confidence_counts["MEDIUM"] > 0:
            quality_flags.add("MEDIUM_CONFIDENCE_MAPPING_PRESENT")
        if time_dim == "POST_PATHWAY":
            quality_flags.add("PROJECTED_CAPABILITY_SCENARIO")

        # Compile individual view
        sdg_summaries = []
        for sdg_num in all_aligned_sdgs:
            goal_meta = self.m5.goals[sdg_num]
            matching_als = [al for al in all_alignments if al["sdg_id"] == sdg_num]
            sdg_targets = sorted(list(set(al["target_id"] for al in matching_als)))
            sdg_types = sorted(list(set(al["mapping_type"] for al in matching_als)))
            sdg_skills = sorted(list(set(skills_by_sdg[sdg_num])))
            sdg_summaries.append({
                "sdg_id": sdg_num,
                "sdg_code": f"SDG_{sdg_num}",
                "sdg_name": goal_meta["name"],
                "target_ids": sdg_targets,
                "mapping_types": sdg_types,
                "contributing_skills": sdg_skills,
                "role_contributes": any(al["source"] == "ROLE" for al in matching_als)
            })

        return {
            "aggregation_level": "INDIVIDUAL",
            "profile_id": pid,
            "cohort_id": cohort_id,
            "region_id": region_id,
            "time_dimension": time_dim,
            "time_dimension_semantics": (
                "CONFIRMED_CAPABILITIES" if time_dim == "CURRENT"
                else "PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED"
            ),
            "descriptive_metrics": {
                "aligned_sdg_count": len(all_aligned_sdgs),
                "aligned_target_count": len(all_targets_covered),
                "direct_mapping_count": mapping_type_counts["DIRECT"],
                "enabling_mapping_count": mapping_type_counts["ENABLING"],
                "contextual_mapping_count": mapping_type_counts["CONTEXTUAL"],
                "unique_relations_count": len(unique_relations),
                "pathway_alignment_prevalence": round(pathway_alignment_prevalence, 4)
            },
            "aligned_sdgs": all_aligned_sdgs,
            "targets_covered": all_targets_covered,
            "sdg_details": sdg_summaries,
            "mapping_type_counts": mapping_type_counts,
            "confidence_counts": confidence_counts,
            "active_role": {
                "masco_code": active_role_masco,
                "role_title": self.m5.role_mappings.get(str(active_role_masco), {}).get("role_title", "Unknown Role")
            },
            "active_skills_count": len(active_skills),
            "pathway_skills_count": len(pathway_skills),
            "quality_flags": sorted(list(quality_flags)),
            "governance_safeguards": {
                "individual_sdg_score_computed": False,
                "employee_sustainability_ranking_computed": False,
                "hr_decision_use_prohibited": True
            },
            "m5_version": self.PINNED_M5_VERSION,
            "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
            "data_source_class": "SYNTHETIC_DEMO",
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    def aggregate_cohort_alignment(
        self,
        profiles: List[Dict[str, Any]],
        cohort_id: Optional[str] = None,
        time_dimension: str = "CURRENT",
        scenario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Level 2 & 3: WORKFORCE COHORT / REGIONAL AGGREGATION VIEW
        Aggregates descriptive sustainability alignment across multiple profiles.
        Enforces:
        - DEF-P1-01: Profile validation & eligible denominator integrity
        - DEF-P2-01: Demographic-feature exclusion (no empirical DIR claim)
        - DEF-P2-02: Differencing & privacy limitation metadata
        - DEF-P2-03: Canonical counting unit (i, t, tau) for mapping shares
        - DEF-P3-01: Pathway alignment coverage scope and disclaimers
        - DEF-P3-02: Regional representativeness runtime disclaimer
        """
        time_dim = time_dimension.upper()
        if time_dim not in ("CURRENT", "POST_PATHWAY"):
            raise ValueError(f"Unsupported time_dimension '{time_dimension}'. Must be 'CURRENT' or 'POST_PATHWAY'.")

        raw_count = len(profiles) if isinstance(profiles, list) else 0

        # DEF-P1-01 Deterministic Profile Validation & Denominator Integrity Layer
        seen_pids = set()
        eligible_profiles = []
        excluded_by_reason: Dict[str, int] = {
            "INCOMPLETE_PROFILE_DATA": 0,
            "INVALID_PROFILE_TYPE": 0,
            "DUPLICATE_PROFILE_ID": 0
        }

        if isinstance(profiles, list):
            for p in profiles:
                status, reason = self.validate_profile_for_aggregation(p)
                if status != "ELIGIBLE":
                    reason_key = reason or "INCOMPLETE_PROFILE_DATA"
                    excluded_by_reason[reason_key] = excluded_by_reason.get(reason_key, 0) + 1
                    continue

                pid = p["profile_id"]
                if pid in seen_pids:
                    excluded_by_reason["DUPLICATE_PROFILE_ID"] = excluded_by_reason.get("DUPLICATE_PROFILE_ID", 0) + 1
                    continue

                seen_pids.add(pid)
                eligible_profiles.append(p)

        eligible_count = len(eligible_profiles)
        excluded_count = raw_count - eligible_count
        duplicate_detected = excluded_by_reason.get("DUPLICATE_PROFILE_ID", 0) > 0

        cid = cohort_id or (eligible_profiles[0].get("cohort_id", "WORKFORCE_COHORT") if eligible_profiles else "EMPTY_COHORT")

        # Quality flags initialization
        cohort_quality_flags: Set[str] = set(["SYNTHETIC_DATA_ONLY", "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT"])
        if duplicate_detected:
            cohort_quality_flags.add("DUPLICATE_PROFILE_DETECTED")
        if excluded_count > 0:
            cohort_quality_flags.add("EXCLUDED_FROM_DENOMINATOR")
        if scenario_id:
            cohort_quality_flags.add("SCENARIO_CONTEXT_PRESENT")
        if time_dim == "POST_PATHWAY":
            cohort_quality_flags.add("PROJECTED_CAPABILITY_SCENARIO")

        # Base privacy metadata dictionary
        privacy_safeguards_meta = {
            "minimum_cohort_size": self.minimum_cohort_size,
            "privacy_protection_level": "PROTOTYPE_PARTITION_SUPPRESSION",
            "cross_query_differencing_protection": "PARTIAL",
            "privacy_limitations": [
                "Arbitrary adaptive query-history reconstruction is not fully prevented in this prototype.",
                "Production deployment with sensitive real-world data would require stronger disclosure controls such as query-history enforcement and/or formally calibrated privacy mechanisms."
            ],
            "differencing_warning": "Protection applies to engine-generated partition outputs. Arbitrary repeated/adaptive cross-query differencing is not fully prevented in this prototype.",
            "differential_privacy_claimed": False
        }

        # -------------------------------------------------------------
        # CASE 1: EMPTY RAW COHORT (raw_count == 0)
        # -------------------------------------------------------------
        if raw_count == 0:
            return {
                "aggregation_level": "WORKFORCE_COHORT",
                "cohort_id": cid,
                "input_profile_count": 0,
                "eligible_profile_count": 0,
                "excluded_profile_count": 0,
                "excluded_profiles_by_reason": excluded_by_reason,
                "cohort_size": 0,
                "eligible_count": 0,
                "suppressed": True,
                "suppression_reason": "INSUFFICIENT_COHORT_DATA",
                "privacy_threshold": self.minimum_cohort_size,
                "privacy_safeguards": privacy_safeguards_meta,
                "quality_flags": sorted(list(cohort_quality_flags.union({"INSUFFICIENT_COHORT_DATA"}))),
                "sdg_alignment_prevalence": None,
                "target_prevalence": None,
                "mapping_type_distribution": None,
                "capability_coverage": None,
                "pathway_alignment_coverage": None,
                "role_alignment_distribution": None,
                "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
                "data_source_class": "SYNTHETIC_DEMO",
                "governance_safeguards": {
                    "hr_decision_use_prohibited": True,
                    "employee_ranking_prohibited": True,
                    "synthetic_impact_quantification_prohibited": True
                },
                "m5_version": self.PINNED_M5_VERSION,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }

        # -------------------------------------------------------------
        # CASE 2: ALL-INVALID COHORT (raw_count > 0 but eligible_count == 0)
        # -------------------------------------------------------------
        if eligible_count == 0:
            return {
                "aggregation_level": "WORKFORCE_COHORT",
                "cohort_id": cid,
                "input_profile_count": raw_count,
                "eligible_profile_count": 0,
                "excluded_profile_count": excluded_count,
                "excluded_profiles_by_reason": excluded_by_reason,
                "cohort_size": raw_count,
                "eligible_count": 0,
                "suppressed": True,
                "suppression_reason": "INSUFFICIENT_ELIGIBLE_COHORT_DATA",
                "privacy_threshold": self.minimum_cohort_size,
                "privacy_safeguards": privacy_safeguards_meta,
                "quality_flags": sorted(list(cohort_quality_flags.union({"INSUFFICIENT_ELIGIBLE_COHORT_DATA"}))),
                "sdg_alignment_prevalence": None,
                "target_prevalence": None,
                "mapping_type_distribution": None,
                "capability_coverage": None,
                "pathway_alignment_coverage": None,
                "role_alignment_distribution": None,
                "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
                "data_source_class": "SYNTHETIC_DEMO",
                "governance_safeguards": {
                    "hr_decision_use_prohibited": True,
                    "employee_ranking_prohibited": True,
                    "synthetic_impact_quantification_prohibited": True
                },
                "m5_version": self.PINNED_M5_VERSION,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }

        # -------------------------------------------------------------
        # CASE 3: SMALL COHORT SUPPRESSION (0 < eligible_count < k)
        # -------------------------------------------------------------
        if eligible_count < self.minimum_cohort_size:
            return {
                "aggregation_level": "WORKFORCE_COHORT",
                "cohort_id": cid,
                "input_profile_count": raw_count,
                "eligible_profile_count": eligible_count,
                "excluded_profile_count": excluded_count,
                "excluded_profiles_by_reason": excluded_by_reason,
                "cohort_size": raw_count,
                "eligible_count": eligible_count,
                "suppressed": True,
                "suppression_reason": self.suppression_code,
                "privacy_threshold": self.minimum_cohort_size,
                "privacy_safeguards": privacy_safeguards_meta,
                "privacy_policy_note": (
                    "Project-defined privacy safeguard using minimum cohort-size suppression / k-anonymity-style aggregation. "
                    f"Cohorts with fewer than {self.minimum_cohort_size} profiles are suppressed to prevent inferential disclosure."
                ),
                "quality_flags": sorted(list(cohort_quality_flags.union({"SMALL_COHORT_SUPPRESSED"}))),
                "sdg_alignment_prevalence": None,
                "target_prevalence": None,
                "mapping_type_distribution": None,
                "capability_coverage": None,
                "pathway_alignment_coverage": None,
                "role_alignment_distribution": None,
                "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
                "data_source_class": "SYNTHETIC_DEMO",
                "governance_safeguards": {
                    "hr_decision_use_prohibited": True,
                    "employee_ranking_prohibited": True,
                    "synthetic_impact_quantification_prohibited": True
                },
                "m5_version": self.PINNED_M5_VERSION,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }

        # -------------------------------------------------------------
        # METRIC COMPUTATIONS (Eligible Cohort >= minimum_cohort_size)
        # -------------------------------------------------------------
        profile_evals = [self.aggregate_individual_alignment(p, time_dimension=time_dim) for p in eligible_profiles]

        # Propagate quality flags from individuals
        for pe in profile_evals:
            for flag in pe["quality_flags"]:
                if flag in (
                    "SECTOR_DEPENDENT_ALIGNMENT", "CONTEXT_DEPENDENT_ALIGNMENT",
                    "CONTEXTUAL_BENEFICIARY_ALIGNMENT", "MEDIUM_CONFIDENCE_MAPPING_PRESENT"
                ):
                    clean_flag = flag if flag.endswith("_PRESENT") else f"{flag}_PRESENT"
                    cohort_quality_flags.add(clean_flag)

        # Metric A: SDG Alignment Prevalence (SAP)
        # Denominator contract: MUST use eligible_count!
        sdg_profile_counts: Dict[int, int] = {sdg_id: 0 for sdg_id in range(1, 18)}
        for pe in profile_evals:
            for sdg_num in pe["aligned_sdgs"]:
                sdg_profile_counts[sdg_num] += 1

        sdg_alignment_prevalence = {}
        for sdg_num, count in sdg_profile_counts.items():
            ratio = count / eligible_count
            sdg_alignment_prevalence[f"SDG_{sdg_num}"] = {
                "sdg_id": sdg_num,
                "sdg_name": self.m5.goals[sdg_num]["name"],
                "aligned_profile_count": count,
                "prevalence_ratio": round(ratio, 4),
                "prevalence_percentage": round(ratio * 100, 2)
            }

        # Metric B: Target Prevalence Index (TPI)
        # Denominator contract: MUST use eligible_count!
        target_profile_counts: Dict[str, int] = {t_id: 0 for t_id in self.m5.targets.keys()}
        for pe in profile_evals:
            for t_id in pe["targets_covered"]:
                if t_id in target_profile_counts:
                    target_profile_counts[t_id] += 1

        target_prevalence = {}
        for t_id, count in sorted(target_profile_counts.items()):
            if count > 0:  # Expose only represented targets
                ratio = count / eligible_count
                target_prevalence[t_id] = {
                    "target_id": t_id,
                    "sdg_id": self.m5.targets[t_id].get("sdg_number") or self.m5.targets[t_id].get("goal_id"),
                    "aligned_profile_count": count,
                    "prevalence_ratio": round(ratio, 4),
                    "prevalence_percentage": round(ratio * 100, 2)
                }

        # Metric C: DIRECT / ENABLING / CONTEXTUAL Ratio
        # DEF-P2-03 Canonical counting unit: UNIQUE PROFILE-TARGET-MAPPING_TYPE RELATION (i, t, tau)
        cohort_relations: Set[Tuple[str, str, str]] = set()
        for p in eligible_profiles:
            pid = p["profile_id"]
            # Active role
            cur_role = p.get("current_role") or {}
            cur_masco = cur_role.get("masco_code") if isinstance(cur_role, dict) else str(cur_role)
            target_role = p.get("target_role") or {}
            target_masco = target_role.get("masco_code") if isinstance(target_role, dict) else str(target_role)

            active_masco = (
                target_masco if time_dim == "POST_PATHWAY" and target_masco in self.m5.role_mappings
                else cur_masco
            )

            if active_masco and str(active_masco) in self.m5.role_mappings:
                r_map = self.m5.get_role_sdg_mapping(str(active_masco))
                for al in r_map.get("primary_sdgs", []) + r_map.get("secondary_sdgs", []):
                    cohort_relations.add((pid, al["target_id"], al["mapping_type"]))

            # Active skills
            skills_set = set(list(p.get("confirmed_skills") or []))
            if time_dim == "POST_PATHWAY":
                pw_skills = list(p.get("reskilling_pathway", {}).get("planned_skills") or [])
                skills_set.update(pw_skills)

            for s_id in skills_set:
                if s_id in self.m5.skill_mappings:
                    s_map = self.m5.get_skill_sdg_mapping(s_id)
                    for al in s_map.get("primary_sdgs", []) + s_map.get("secondary_sdgs", []):
                        cohort_relations.add((pid, al["target_id"], al["mapping_type"]))

        total_relations = len(cohort_relations)
        if total_relations == 0:
            mapping_type_distribution = {
                "status": "NO_ALIGNMENT_RELATIONS",
                "direct_count": 0,
                "enabling_count": 0,
                "contextual_count": 0,
                "total_mappings_evaluated": 0,
                "direct_share": 0.0,
                "enabling_share": 0.0,
                "contextual_share": 0.0,
                "counting_unit": "UNIQUE_PROFILE_TARGET_MAPPING_TYPE_RELATION",
                "counting_unit_formula": "(i, t, tau) unique tuple per profile-target-type",
                "semantics_note": "Describes evidence tier of competency mappings. Does not measure strength of societal impact."
            }
        else:
            total_direct = sum(1 for r in cohort_relations if r[2] == "DIRECT")
            total_enabling = sum(1 for r in cohort_relations if r[2] == "ENABLING")
            total_contextual = sum(1 for r in cohort_relations if r[2] == "CONTEXTUAL")

            direct_share = round(total_direct / total_relations, 4)
            enabling_share = round(total_enabling / total_relations, 4)
            contextual_share = round(total_contextual / total_relations, 4)

            # Enforce strictly sum to 1.0
            sum_shares = direct_share + enabling_share + contextual_share
            if sum_shares != 1.0 and total_contextual > 0:
                contextual_share = round(1.0 - direct_share - enabling_share, 4)
            elif sum_shares != 1.0 and total_enabling > 0:
                enabling_share = round(1.0 - direct_share - contextual_share, 4)

            mapping_type_distribution = {
                "direct_count": total_direct,
                "enabling_count": total_enabling,
                "contextual_count": total_contextual,
                "total_mappings_evaluated": total_relations,
                "direct_share": direct_share,
                "enabling_share": enabling_share,
                "contextual_share": contextual_share,
                "counting_unit": "UNIQUE_PROFILE_TARGET_MAPPING_TYPE_RELATION",
                "counting_unit_formula": "(i, t, tau) unique tuple per profile-target-type",
                "semantics_note": "Describes evidence tier of competency mappings. Does not measure strength of societal impact."
            }

        # Metric D: Capability Coverage
        # Role mappings must NOT enter skill capability-coverage numerator!
        cohort_skills_present: Set[str] = set()
        for p in eligible_profiles:
            cohort_skills_present.update(list(p.get("confirmed_skills") or []))
            if time_dim == "POST_PATHWAY":
                pw_skills = list(p.get("reskilling_pathway", {}).get("planned_skills") or [])
                cohort_skills_present.update(pw_skills)

        capability_coverage = {}
        for sdg_num in range(1, 18):
            canon_skills = self._canonical_sdg_skills[sdg_num]
            skills_held = sorted(list(canon_skills.intersection(cohort_skills_present)))
            total_canon = len(canon_skills)
            ratio = len(skills_held) / total_canon if total_canon > 0 else 0.0
            capability_coverage[f"SDG_{sdg_num}"] = {
                "sdg_id": sdg_num,
                "skills_present_in_cohort": skills_held,
                "skills_present_count": len(skills_held),
                "canonical_sdg_skills_total": total_canon,
                "capability_coverage_ratio": round(ratio, 4),
                "capability_coverage_percentage": round(ratio * 100, 2)
            }

        # Metric E: Pathway Alignment Coverage
        # DEF-P3-01: Explicit scope and disclaimers for planned curriculum steps
        all_planned_pathway_skills = []
        for p in eligible_profiles:
            pw_skills = list(p.get("reskilling_pathway", {}).get("planned_skills") or [])
            all_planned_pathway_skills.extend(pw_skills)

        aligned_pathway_skills_count = sum(
            1 for s in all_planned_pathway_skills
            if s in self.m5.skill_mappings and (
                self.m5.skill_mappings[s].get("primary_sdgs") or self.m5.skill_mappings[s].get("secondary_sdgs")
            )
        )
        total_planned_pathway_skills = len(all_planned_pathway_skills)
        pathway_alignment_ratio = (
            aligned_pathway_skills_count / total_planned_pathway_skills
            if total_planned_pathway_skills > 0 else 0.0
        )

        pathway_alignment_coverage = {
            "total_planned_pathway_skill_instances": total_planned_pathway_skills,
            "sdg_aligned_pathway_skill_instances": aligned_pathway_skills_count,
            "pathway_alignment_coverage_ratio": round(pathway_alignment_ratio, 4),
            "pathway_alignment_coverage_percentage": round(pathway_alignment_ratio * 100, 2),
            "pathway_alignment_coverage_scope": "PLANNED_CURRICULUM_SKILL_STEPS",
            "pathway_alignment_coverage_disclaimer": "Coverage reflects planned reskilling curriculum alignment, not verified course completion, skill mastery, or realised SDG impact.",
            "semantics_note": "Describes proportion of planned reskilling curriculum with sustainability relevance. Not a measure of course completion, skill mastery, educational attainment, or realized environmental impact."
        }

        # Metric F: Role Alignment Distribution
        role_counts: Dict[str, int] = {}
        for p in eligible_profiles:
            cur_role = p.get("current_role") or {}
            cur_masco = cur_role.get("masco_code") if isinstance(cur_role, dict) else str(cur_role)
            target_role = p.get("target_role") or {}
            target_masco = target_role.get("masco_code") if isinstance(target_role, dict) else str(target_role)

            active_m = (
                target_masco if time_dim == "POST_PATHWAY" and target_masco in self.m5.role_mappings
                else cur_masco
            )
            if active_m:
                role_counts[str(active_m)] = role_counts.get(str(active_m), 0) + 1

        role_alignment_distribution = {}
        for masco_code, count in sorted(role_counts.items()):
            r_info = self.m5.role_mappings.get(masco_code, {})
            primary_sdgs = [al["sdg_id"] for al in r_info.get("primary_sdgs", [])]
            secondary_sdgs = [al["sdg_id"] for al in r_info.get("secondary_sdgs", [])]
            flags = r_info.get("quality_flags", [])
            role_alignment_distribution[masco_code] = {
                "masco_code": masco_code,
                "role_title": r_info.get("role_title", "Unknown Role"),
                "profile_count": count,
                "prevalence_share": round(count / eligible_count, 4),
                "primary_sdgs": primary_sdgs,
                "secondary_sdgs": secondary_sdgs,
                "quality_flags": flags
            }

        # Confidence Distribution
        total_high = sum(pe["confidence_counts"]["HIGH"] for pe in profile_evals)
        total_med = sum(pe["confidence_counts"]["MEDIUM"] for pe in profile_evals)
        total_low = sum(pe["confidence_counts"]["LOW"] for pe in profile_evals)
        total_conf = total_high + total_med + total_low

        confidence_distribution = {
            "high_confidence_count": total_high,
            "medium_confidence_count": total_med,
            "low_confidence_count": total_low,
            "high_confidence_share": round(total_high / total_conf, 4) if total_conf > 0 else 0.0,
            "medium_confidence_share": round(total_med / total_conf, 4) if total_conf > 0 else 0.0,
            "low_confidence_share": round(total_low / total_conf, 4) if total_conf > 0 else 0.0
        }

        # -------------------------------------------------------------
        # INTERFACE HOOKS
        # -------------------------------------------------------------
        # O1 Employer Workforce-Gap Hook
        skill_gap_counts: Dict[str, int] = {}
        core_gap_counts: Dict[str, int] = {}
        for p in eligible_profiles:
            pw = p.get("reskilling_pathway") or {}
            for s in list(pw.get("planned_skills") or []):
                skill_gap_counts[s] = skill_gap_counts.get(s, 0) + 1
            for s in list(pw.get("core_gaps") or []):
                core_gap_counts[s] = core_gap_counts.get(s, 0) + 1

        o1_interface_hook = {
            "cohort_skill_gap_counts": dict(sorted(skill_gap_counts.items(), key=lambda x: x[1], reverse=True)),
            "cohort_core_gap_counts": dict(sorted(core_gap_counts.items(), key=lambda x: x[1], reverse=True)),
            "role_distribution": role_counts,
            "sdg_aligned_gap_skills": [
                s for s in skill_gap_counts if s in self.m5.skill_mappings and (
                    self.m5.skill_mappings[s].get("primary_sdgs") or self.m5.skill_mappings[s].get("secondary_sdgs")
                )
            ]
        }

        # O2 Replanning/Refresh Hook
        profiles_repr = json.dumps([p.get("profile_id") for p in eligible_profiles], sort_keys=True)
        o2_interface_hook = {
            "input_profiles_hash": hashlib.sha256(profiles_repr.encode("utf-8")).hexdigest(),
            "m5_version": self.PINNED_M5_VERSION,
            "m4_version": self.PINNED_M4_VERSION,
            "m3_version": self.PINNED_M3_VERSION,
            "m6_version": self.PINNED_M6_VERSION,
            "refresh_supported": True
        }

        # DEF-P2-01: Corrected O5 Fairness Hook (Structural Protected-Attribute Non-Use)
        o5_fairness_hook = {
            "protected_attributes_used": False,
            "demographic_fairness_evaluated": False,
            "fairness_scope": "STRUCTURAL_PROTECTED_ATTRIBUTE_NON_USE",
            "future_fairness_audit_hook": True,
            "occupational_group_representation": role_counts,
            "total_unique_skills_represented": len(cohort_skills_present),
            "fairness_policy_note": (
                "Protected demographic attributes are excluded from O6 inputs and aggregation logic. "
                "Because the synthetic Stage 14 dataset contains no demographic group labels, "
                "empirical demographic disparity metrics such as Disparate Impact Ratio are not evaluated."
            )
        }

        # Generate unique aggregation ID
        agg_id_src = f"{cid}_{time_dim}_{eligible_count}_{datetime.utcnow().isoformat()}"
        agg_id = "AGG_" + hashlib.sha256(agg_id_src.encode("utf-8")).hexdigest()[:12]

        return {
            "aggregation_id": agg_id,
            "aggregation_level": "WORKFORCE_COHORT",
            "cohort_id": cid,
            "input_profile_count": raw_count,
            "eligible_profile_count": eligible_count,
            "excluded_profile_count": excluded_count,
            "excluded_profiles_by_reason": excluded_by_reason,
            "cohort_size": raw_count,
            "eligible_count": eligible_count,
            "suppressed": False,
            "suppression_reason": None,
            "privacy_threshold": self.minimum_cohort_size,
            "privacy_safeguards": privacy_safeguards_meta,
            "time_dimension": time_dim,
            "time_dimension_label": (
                "CURRENT_CAPABILITIES" if time_dim == "CURRENT"
                else "PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED"
            ),
            "sdg_alignment_prevalence": sdg_alignment_prevalence,
            "target_prevalence": target_prevalence,
            "mapping_type_distribution": mapping_type_distribution,
            "capability_coverage": capability_coverage,
            "pathway_alignment_coverage": pathway_alignment_coverage,
            "role_alignment_distribution": role_alignment_distribution,
            "confidence_distribution": confidence_distribution,
            "o1_interface_hook": o1_interface_hook,
            "o2_interface_hook": o2_interface_hook,
            "o5_fairness_hook": o5_fairness_hook,
            "scenario_context": {
                "scenario_id": scenario_id or "EMPIRICAL_BASELINE",
                "label": "Empirical workforce profile composition"
            },
            "quality_flags": sorted(list(cohort_quality_flags)),
            "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
            "data_source_class": "SYNTHETIC_DEMO",
            "governance_safeguards": {
                "hr_decision_use_prohibited": True,
                "hr_decision_clause": "O6 workforce analytics must NEVER be used to hire, fire, promote, penalize, or score individual employees.",
                "employee_sustainability_ranking_prohibited": True,
                "synthetic_impact_quantification_prohibited": True
            },
            "source_versions": {
                "m5_sdg_mapping": self.PINNED_M5_VERSION,
                "m4_reskilling_pathways": self.PINNED_M4_VERSION,
                "m3_role_matching": self.PINNED_M3_VERSION,
                "m6_scenarios": self.PINNED_M6_VERSION,
                "o6_aggregation_engine": self.VERSION
            },
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    def aggregate_partition_breakdown(
        self,
        profiles: List[Dict[str, Any]],
        partition_key: str,
        cohort_id: Optional[str] = None,
        time_dimension: str = "CURRENT"
    ) -> Dict[str, Any]:
        """
        DEF-P2-02 Partition-Aware Complementary Suppression.
        When producing a complete mutually exclusive partition breakdown across an attribute
        (e.g., region_id, cohort_id), if any single cell is suppressed for small size (0 < N < k),
        apply complementary suppression to the next smallest non-small cell to prevent direct
        subtraction recovery from the parent total.
        """
        parent_agg = self.aggregate_cohort_alignment(
            profiles,
            cohort_id=cohort_id or "PARENT_COHORT",
            time_dimension=time_dimension
        )

        if parent_agg.get("suppressed"):
            return {
                "aggregation_level": "PARTITION_BREAKDOWN",
                "partition_key": partition_key,
                "parent_cohort": parent_agg,
                "partitions": {},
                "complementary_suppression_applied": False,
                "suppressed": True,
                "suppression_reason": parent_agg.get("suppression_reason")
            }

        # Group profiles by partition_key
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for p in profiles:
            if isinstance(p, dict):
                val = str(p.get(partition_key, "UNKNOWN"))
            else:
                val = "INVALID_TYPE"
            if val not in grouped:
                grouped[val] = []
            grouped[val].append(p)

        # Aggregate each partition cell
        cell_aggs: Dict[str, Dict[str, Any]] = {}
        small_cells = []
        eligible_non_small_cells = []

        for p_val, p_profiles in grouped.items():
            agg = self.aggregate_cohort_alignment(
                p_profiles,
                cohort_id=f"{cohort_id}_{p_val}" if cohort_id else p_val,
                time_dimension=time_dimension
            )
            cell_aggs[p_val] = agg
            elig = agg.get("eligible_profile_count", 0)
            if agg.get("suppressed") and elig > 0 and elig < self.minimum_cohort_size:
                small_cells.append(p_val)
            elif not agg.get("suppressed"):
                eligible_non_small_cells.append((p_val, elig))

        # Check for complementary suppression necessity
        # If there are small suppressed cells, and displaying remaining unsuppressed cells would allow
        # algebraic differencing (e.g., Parent - Visible = Suppressed), suppress at least one additional
        # non-small cell (the smallest among eligible non-small siblings).
        complementary_applied = False
        complementary_suppressed_cells = []

        if self.enable_complementary_suppression and len(small_cells) > 0:
            # If exactly 1 small cell or if unsuppressed cells can leak the small cell sum:
            if len(eligible_non_small_cells) > 0:
                # Sort non-small cells by eligible count ascending
                eligible_non_small_cells.sort(key=lambda x: x[1])
                # Suppress the smallest non-small sibling
                target_cell_val = eligible_non_small_cells[0][0]
                target_agg = cell_aggs[target_cell_val]

                # Mask out statistical distributions
                target_agg["suppressed"] = True
                target_agg["suppression_reason"] = self.complementary_suppression_code
                target_agg["sdg_alignment_prevalence"] = None
                target_agg["target_prevalence"] = None
                target_agg["mapping_type_distribution"] = None
                target_agg["capability_coverage"] = None
                target_agg["pathway_alignment_coverage"] = None
                target_agg["role_alignment_distribution"] = None
                target_agg["quality_flags"] = sorted(list(set(target_agg.get("quality_flags", [])).union({"COMPLEMENTARY_SUPPRESSION_APPLIED"})))

                complementary_applied = True
                complementary_suppressed_cells.append(target_cell_val)

        return {
            "aggregation_level": "PARTITION_BREAKDOWN",
            "partition_key": partition_key,
            "cohort_id": cohort_id or "PARENT_COHORT",
            "parent_eligible_count": parent_agg["eligible_profile_count"],
            "parent_cohort": parent_agg,
            "partition_cells": cell_aggs,
            "small_cells_suppressed": small_cells,
            "complementary_suppression_applied": complementary_applied,
            "complementary_suppressed_cells": complementary_suppressed_cells,
            "privacy_safeguards": {
                "minimum_cohort_size": self.minimum_cohort_size,
                "privacy_protection_level": "PROTOTYPE_PARTITION_SUPPRESSION",
                "cross_query_differencing_protection": "PARTIAL",
                "differencing_warning": "Protection applies to engine-generated partition outputs. Arbitrary repeated/adaptive cross-query differencing is not fully prevented in this prototype.",
                "differential_privacy_claimed": False
            },
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    def aggregate_region_alignment(
        self,
        profiles: List[Dict[str, Any]],
        region_id: str,
        time_dimension: str = "CURRENT",
        scenario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Level 3: REGIONAL / SYNTHETIC POPULATION VIEW
        Filters profiles to the specified synthetic demo region and aggregates.
        """
        region_profiles = [p for p in profiles if isinstance(p, dict) and p.get("region_id") == region_id]
        res = self.aggregate_cohort_alignment(
            region_profiles,
            cohort_id=f"REGION_{region_id}",
            time_dimension=time_dimension,
            scenario_id=scenario_id
        )
        res["aggregation_level"] = "REGIONAL_SYNTHETIC"
        res["region_id"] = region_id
        res["representativeness_disclaimer"] = (
            "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce."
        )
        res["data_source_class"] = "SYNTHETIC_DEMO"
        return res

    def compare_scenarios(
        self,
        profiles: List[Dict[str, Any]],
        cohort_id: Optional[str] = None,
        time_dimension: str = "CURRENT"
    ) -> Dict[str, Any]:
        """
        Scenario Capability View (Metric G)
        Compares workforce cohort foresight across REFERENCE_2026, MODERATE_COPILOT, FAST_AGENTIC.
        Consumes M6 scenario outlook without modifying M5 qualitative mappings.
        """
        scenarios = ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]
        comparison_results = {}

        # Evaluate base cohort aggregation
        base_agg = self.aggregate_cohort_alignment(profiles, cohort_id=cohort_id, time_dimension=time_dimension)
        if base_agg.get("suppressed"):
            return {
                "comparison_level": "SCENARIO_COMPARISON",
                "cohort_id": cohort_id,
                "suppressed": True,
                "suppression_reason": base_agg.get("suppression_reason")
            }

        # Analyze scenario-specific role pressures from M6
        roles_present = list(base_agg["role_alignment_distribution"].keys())

        for sc_id in scenarios:
            scenario_role_pressures = {}
            for masco in roles_present:
                try:
                    s_prof = self.m6.get_role_scenario(masco, sc_id)
                    scenario_role_pressures[masco] = {
                        "masco_code": masco,
                        "automation_risk_score": s_prof.get("automation_risk_score"),
                        "augmentation_potential_score": s_prof.get("augmentation_potential_score"),
                        "demand_resilience_score": s_prof.get("demand_resilience_score")
                    }
                except Exception:
                    scenario_role_pressures[masco] = None

            comparison_results[sc_id] = {
                "scenario_id": sc_id,
                "scenario_meta": next((s for s in self.m6.list_scenarios() if s["scenario_id"] == sc_id), {}),
                "role_scenario_foresight": scenario_role_pressures,
                "aligned_sdg_prevalence": base_agg["sdg_alignment_prevalence"]
            }

        return {
            "comparison_level": "SCENARIO_COMPARISON",
            "cohort_id": cohort_id or "WORKFORCE_COHORT",
            "eligible_count": base_agg["eligible_count"],
            "scenarios_evaluated": scenarios,
            "results": comparison_results,
            "structured_assumption_notice": (
                "Scenario comparisons represent structured macroeconomic and technological assumptions from M6. "
                "They do not alter underlying M5 qualitative target definitions or statutory alignments."
            ),
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    # -------------------------------------------------------------
    # DEDICATED QUERY HELPERS
    # -------------------------------------------------------------
    def get_sdg_prevalence(
        self,
        profiles: List[Dict[str, Any]],
        sdg_id: int,
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Returns prevalence statistics for a specific SDG."""
        agg = self.aggregate_cohort_alignment(profiles, cohort_id=cohort_id)
        if agg.get("suppressed"):
            return {"sdg_id": sdg_id, "suppressed": True, "suppression_reason": agg.get("suppression_reason")}
        return agg["sdg_alignment_prevalence"].get(f"SDG_{sdg_id}", {})

    def get_target_prevalence(
        self,
        profiles: List[Dict[str, Any]],
        target_id: str,
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Returns prevalence statistics for a specific SDG target."""
        agg = self.aggregate_cohort_alignment(profiles, cohort_id=cohort_id)
        if agg.get("suppressed"):
            return {"target_id": target_id, "suppressed": True, "suppression_reason": agg.get("suppression_reason")}
        return agg["target_prevalence"].get(target_id, {"target_id": target_id, "aligned_profile_count": 0, "prevalence_ratio": 0.0})

    def get_capability_coverage(
        self,
        profiles: List[Dict[str, Any]],
        sdg_id: int,
        cohort_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Returns capability coverage statistics for a specific SDG."""
        agg = self.aggregate_cohort_alignment(profiles, cohort_id=cohort_id)
        if agg.get("suppressed"):
            return {"sdg_id": sdg_id, "suppressed": True, "suppression_reason": agg.get("suppression_reason")}
        return agg["capability_coverage"].get(f"SDG_{sdg_id}", {})
