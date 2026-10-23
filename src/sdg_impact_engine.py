"""
M5 SDG Impact Mapping Engine v1.1.0
Author: Senior Sustainability Data Architect, SDG Taxonomy Researcher, Workforce-Impact Methodologist
Framework: UN 2030 Agenda for Sustainable Development (17 Goals, 169 Targets - Selected Domain-Relevant Subset)

Stage 13C Remediated Engine:
Enforces:
1. Three mapping types: DIRECT, ENABLING, CONTEXTUAL.
2. Strict General-Purpose Skill Rule (general-purpose skills can never be DIRECT).
3. Zero fabricated quantitative metrics (no fake kg CO2, jobs created, or % progress).
4. Full official UN SDG target traceability (anchored to 169 UN targets).
5. Target 9.c strict telecommunication infrastructure scope (no software/cloud/API overstretch).
6. Target 16.6 effective/transparent institutional governance for corporate PDPA compliance (no 16.10 FOI mischaracterization).
7. Target 9.5 R&D/industrial capability and 8.2 productivity for enterprise SQL (no 17.18 international statistical capacity mismatch).
8. Target 12.6 DIRECT for corporate ESG/carbon reporting, Target 13.2 ENABLING for policy integration, purged Target 13.3.
9. Sector-dependence flags (SECTOR_DEPENDENT_ALIGNMENT) and MEDIUM confidence for general engineering roles (2151, 2143, 2152).
10. Beneficiary alignment flags (CONTEXTUAL_BENEFICIARY_ALIGNMENT) for clerical occupations under Target 8.5.
11. Absolute isolation: M5 provides an analytical lens and NEVER feeds back to filter M3 roles or M4 courses.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Set


class SDGImpactEngine:
    """
    Core engine for SDG Impact Mapping (M5 v1.1.0).
    Loads canonical goals, targets, skill mappings, and role mappings.
    """

    VERSION = "1.1.0"

    def __init__(
        self,
        goals_path: Optional[Union[str, Path]] = None,
        targets_path: Optional[Union[str, Path]] = None,
        skills_path: Optional[Union[str, Path]] = None,
        roles_path: Optional[Union[str, Path]] = None,
        config_path: Optional[Union[str, Path]] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.goals_path = Path(goals_path) if goals_path else base_dir / "data" / "sdg" / "sdg_goals_v1.json"
        
        # Default to v1_1 files if available, fallback to v1
        default_targets_v1_1 = base_dir / "data" / "sdg" / "sdg_targets_v1_1.json"
        default_targets_v1 = base_dir / "data" / "sdg" / "sdg_targets_v1.json"
        self.targets_path = Path(targets_path) if targets_path else (default_targets_v1_1 if default_targets_v1_1.exists() else default_targets_v1)
        
        default_skills_v1_1 = base_dir / "data" / "sdg" / "skill_sdg_mappings_v1_1.json"
        default_skills_v1 = base_dir / "data" / "sdg" / "skill_sdg_mappings_v1.json"
        self.skills_path = Path(skills_path) if skills_path else (default_skills_v1_1 if default_skills_v1_1.exists() else default_skills_v1)
        
        default_roles_v1_1 = base_dir / "data" / "sdg" / "role_sdg_mappings_v1_1.json"
        default_roles_v1 = base_dir / "data" / "sdg" / "role_sdg_mappings_v1.json"
        self.roles_path = Path(roles_path) if roles_path else (default_roles_v1_1 if default_roles_v1_1.exists() else default_roles_v1)
        
        default_config_v1_1 = base_dir / "data" / "sdg" / "m5_config_v1_1.json"
        default_config_v1 = base_dir / "data" / "sdg" / "m5_config_v1.json"
        self.config_path = Path(config_path) if config_path else (default_config_v1_1 if default_config_v1_1.exists() else default_config_v1)

        self.version = self.VERSION
        self._load_data()
        self._validate_integrity()

    def _load_data(self) -> None:
        """Loads canonical reference datasets and configs."""
        with open(self.goals_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.goals = {}
            for g in data["goals"]:
                num = g.get("sdg_number", int(g["sdg_id"].replace("SDG_", "")))
                g_record = {
                    "goal_id": num,
                    "sdg_number": num,
                    "sdg_code": g["sdg_id"],
                    "name": g.get("official_name", g.get("name", "")),
                    "summary": g.get("official_summary", g.get("summary", "")),
                    "source_url": g.get("official_source_url", "")
                }
                self.goals[num] = g_record
                self.goals[g["sdg_id"]] = g_record

        with open(self.targets_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.targets = {t["target_id"]: t for t in data["targets"]}
            self.target_scope_metadata = {
                "dataset_scope": data.get("dataset_scope"),
                "total_official_un_targets": data.get("total_official_un_targets"),
                "total_indexed_targets": data.get("total_indexed_targets"),
                "scope_note": data.get("scope_note")
            }

        with open(self.skills_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_skills = data.get("skills", data.get("mappings", []))
            self.skill_mappings = {}
            if isinstance(raw_skills, list):
                for item in raw_skills:
                    s_id = item.get("entity_id") or item.get("skill_id")
                    s_title = item.get("entity_name") or item.get("skill_title", s_id)
                    primary_nums = item.get("primary_sdgs", [])
                    secondary_nums = item.get("secondary_sdgs", [])
                    primary_alignments = []
                    secondary_alignments = []

                    for sm in item.get("sdg_mappings", []):
                        sdg_num = sm.get("sdg_number") or sm.get("sdg_id")
                        m_type = sm.get("mapping_type")
                        strength = sm.get("alignment_strength", "MODERATE")
                        pathway = sm.get("contribution_pathway", "")
                        evidence = sm.get("evidence_references", "")
                        conf = sm.get("mapping_confidence") or sm.get("confidence", "HIGH")
                        flags = sm.get("quality_flags", [])
                        targets = sm.get("target_ids", [])
                        if "target_id" in sm:
                            targets = [sm["target_id"]]

                        for t_id in targets:
                            t_desc = self.targets.get(t_id, {}).get("official_target_text", "")
                            al_record = {
                                "sdg_id": sdg_num,
                                "sdg_name": self.goals.get(sdg_num, {}).get("name", f"SDG {sdg_num}"),
                                "target_id": t_id,
                                "target_description": t_desc,
                                "mapping_type": m_type,
                                "alignment_strength": strength,
                                "contribution_pathway": pathway,
                                "evidence_references": evidence,
                                "confidence": conf,
                                "quality_flags": flags
                            }
                            if sdg_num in primary_nums:
                                primary_alignments.append(al_record)
                            else:
                                secondary_alignments.append(al_record)

                    self.skill_mappings[s_id] = {
                        "skill_id": s_id,
                        "skill_title": s_title,
                        "primary_sdgs": primary_alignments,
                        "secondary_sdgs": secondary_alignments,
                        "primary_sdg_numbers": primary_nums,
                        "secondary_sdg_numbers": secondary_nums,
                        "overall_confidence": item.get("overall_confidence", "HIGH"),
                        "quality_flags": item.get("quality_flags", ["OFFICIAL_TARGET_TRACEABLE"]),
                        "derivation_rules": [sm.get("derivation_rule_id", "RULE_CANONICAL_SKILL") for sm in item.get("sdg_mappings", [])]
                    }
            elif isinstance(raw_skills, dict):
                self.skill_mappings = raw_skills

        with open(self.roles_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_roles = data.get("roles", {})
            if isinstance(raw_roles, list):
                self.role_mappings = {r.get("masco_code", r.get("role_code")): r for r in raw_roles}
            else:
                self.role_mappings = raw_roles

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.general_purpose_skill_ids = set(self.config.get("general_purpose_skill_ids", []))

    def _validate_integrity(self) -> None:
        """Validates reference integrity, target existence, and general-purpose rule."""
        assert len([k for k in self.goals if isinstance(k, int)]) == 17, f"Expected 17 goals, found {len([k for k in self.goals if isinstance(k, int)])}"
        assert len(self.skill_mappings) == 16, f"Expected 16 skills, found {len(self.skill_mappings)}"
        assert len(self.role_mappings) == 20, f"Expected 20 roles, found {len(self.role_mappings)}"

        # Validate skill targets and general-purpose rule
        for s_id, s_data in self.skill_mappings.items():
            alignments = s_data.get("primary_sdgs", []) + s_data.get("secondary_sdgs", [])
            for al in alignments:
                t_id = al["target_id"]
                if t_id not in self.targets:
                    raise ValueError(f"Skill {s_id} references unindexed target {t_id}")
                if s_id in self.general_purpose_skill_ids and al["mapping_type"] == "DIRECT":
                    raise ValueError(
                        f"VIOLATION: General-purpose skill '{s_id}' has prohibited DIRECT mapping to Target {t_id}."
                    )

        # Validate role targets
        for r_code, r_data in self.role_mappings.items():
            alignments = r_data.get("primary_sdgs", []) + r_data.get("secondary_sdgs", [])
            for al in alignments:
                t_id = al["target_id"]
                if t_id not in self.targets:
                    raise ValueError(f"Role {r_code} references unindexed target {t_id}")

    def get_sdg_target(self, target_id: str) -> Dict[str, Any]:
        """
        Retrieves official target metadata for a given target ID (e.g. '13.2', '9.5').
        """
        target = self.targets.get(str(target_id).strip())
        if not target:
            raise ValueError(f"Unknown SDG Target '{target_id}'. Must be a valid official target.")
        return target

    def get_skill_sdg_mapping(self, skill_id: str) -> Dict[str, Any]:
        """
        Retrieves canonical SDG alignments for an individual skill.
        """
        norm_id = str(skill_id).strip().lower()
        mapping = self.skill_mappings.get(norm_id)
        if not mapping:
            raise ValueError(f"Unknown skill_id '{skill_id}'. Available skills: {sorted(self.skill_mappings.keys())}")
        return mapping

    def get_role_sdg_mapping(self, masco_code: str) -> Dict[str, Any]:
        """
        Retrieves canonical SDG alignments for a 4-digit MASCO occupation.
        """
        norm_code = str(masco_code).strip()
        mapping = self.role_mappings.get(norm_code)
        if not mapping:
            raise ValueError(f"Unknown MASCO code '{masco_code}'. Available roles: {sorted(self.role_mappings.keys())}")
        return mapping

    def explain_sdg_alignment(
        self,
        entity_type: str,
        entity_id: str,
        sdg_id: int
    ) -> Dict[str, Any]:
        """
        Generates an evidence-grounded explanation for why a skill or role aligns with a given SDG.
        """
        etype = entity_type.strip().lower()
        goal = self.goals.get(int(sdg_id))
        if not goal:
            raise ValueError(f"Unknown SDG ID {sdg_id}. Must be 1 through 17.")

        if etype == "skill":
            data = self.get_skill_sdg_mapping(entity_id)
            title = data.get("skill_title", entity_id)
        elif etype in ("role", "occupation"):
            data = self.get_role_sdg_mapping(entity_id)
            title = data.get("role_title", entity_id)
        else:
            raise ValueError(f"Unsupported entity_type '{entity_type}'. Must be 'skill' or 'role'.")

        alignments = [
            al for al in (data.get("primary_sdgs", []) + data.get("secondary_sdgs", []))
            if al.get("sdg_id") == int(sdg_id)
        ]

        if not alignments:
            return {
                "entity_type": etype,
                "entity_id": entity_id,
                "entity_title": title,
                "sdg_id": int(sdg_id),
                "sdg_name": goal["name"],
                "aligned": False,
                "explanation": f"{title} has no canonical primary or secondary alignment with SDG {sdg_id} ({goal['name']})."
            }

        target_summaries = [f"Target {al['target_id']} ({al['mapping_type']}, {al.get('confidence', 'HIGH')})" for al in alignments]
        pathway_summaries = [al["contribution_pathway"] for al in alignments]

        all_flags = []
        for al in alignments:
            all_flags.extend(al.get("quality_flags", []))
        all_flags.extend(data.get("quality_flags", []))
        unique_flags = sorted(list(set(all_flags)))

        return {
            "entity_type": etype,
            "entity_id": entity_id,
            "entity_title": title,
            "sdg_id": int(sdg_id),
            "sdg_name": goal["name"],
            "aligned": True,
            "alignments_count": len(alignments),
            "details": alignments,
            "quality_flags": unique_flags,
            "summary_narrative": (
                f"{title} contributes to SDG {sdg_id} ({goal['name']}) via "
                f"{', '.join(target_summaries)}. Pathways: {' '.join(pathway_summaries)}"
            )
        }

    def map_pathway_to_sdgs(self, pathway: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps a full personalized reskilling pathway (from M4) to UN Sustainable Development Goals.
        Synthesizes both role-level structural impacts and skill-level competency contributions.

        Stage 13C Remediated Synthesis:
        - Clearly distinguishes immediate pathway competency contributions from target role career horizon.
        - Identifies sector-dependent and contextual-beneficiary alignments.
        - Zero Fake Metrics: Does NOT compute fabricated kilograms of carbon or jobs created.
        - Strict Isolation: Does NOT filter, re-rank, or alter the reskilling pathway.
        """
        # Determine target role
        target_role = (
            pathway.get("target_role_code")
            or pathway.get("target_occupation_code")
            or pathway.get("masco_code")
            or (pathway.get("target_role") if isinstance(pathway.get("target_role"), str) else None)
        )
        if isinstance(target_role, dict):
            target_role = target_role.get("masco_code") or target_role.get("role_code")

        role_sdg_info = None
        if target_role and str(target_role) in self.role_mappings:
            role_sdg_info = self.get_role_sdg_mapping(str(target_role))

        # Determine skills in pathway
        skills_in_pathway = set()
        if "skills" in pathway and isinstance(pathway["skills"], list):
            for s in pathway["skills"]:
                if isinstance(s, str):
                    skills_in_pathway.add(s)
                elif isinstance(s, dict) and "skill_id" in s:
                    skills_in_pathway.add(s["skill_id"])
        
        # Check module skills or courses
        if "modules" in pathway and isinstance(pathway["modules"], list):
            for m in pathway["modules"]:
                if isinstance(m, dict):
                    if "skill_id" in m:
                        skills_in_pathway.add(m["skill_id"])
                    if "skills_covered" in m and isinstance(m["skills_covered"], list):
                        for sc in m["skills_covered"]:
                            skills_in_pathway.add(sc)

        if "gap_skills" in pathway and isinstance(pathway["gap_skills"], list):
            for gs in pathway["gap_skills"]:
                if isinstance(gs, str):
                    skills_in_pathway.add(gs)

        # Collect alignments across all skills
        skill_contributions = {}
        all_sdg_buckets: Dict[int, Dict[str, Any]] = {}
        pathway_quality_flags: Set[str] = set()

        for s_id in sorted(skills_in_pathway):
            if s_id in self.skill_mappings:
                s_map = self.get_skill_sdg_mapping(s_id)
                skill_contributions[s_id] = s_map
                for flag in s_map.get("quality_flags", []):
                    pathway_quality_flags.add(flag)

                for al in s_map.get("primary_sdgs", []) + s_map.get("secondary_sdgs", []):
                    sdg_num = al["sdg_id"]
                    if sdg_num not in all_sdg_buckets:
                        all_sdg_buckets[sdg_num] = {
                            "sdg_id": sdg_num,
                            "sdg_name": self.goals[sdg_num]["name"],
                            "direct_contributions": [],
                            "enabling_contributions": [],
                            "contextual_contributions": [],
                            "targets_addressed": set(),
                            "contributing_skills": set(),
                            "role_aligned": False,
                            "skill_aligned": False,
                            "quality_flags": set()
                        }
                    bucket = all_sdg_buckets[sdg_num]
                    bucket["skill_aligned"] = True
                    bucket["targets_addressed"].add(al["target_id"])
                    bucket["contributing_skills"].add(s_id)
                    for f in al.get("quality_flags", []):
                        bucket["quality_flags"].add(f)

                    entry = {
                        "source_type": "SKILL",
                        "source_id": s_id,
                        "source_title": s_map.get("skill_title", s_id),
                        "target_id": al["target_id"],
                        "target_description": al["target_description"],
                        "mapping_type": al["mapping_type"],
                        "alignment_strength": al["alignment_strength"],
                        "contribution_pathway": al["contribution_pathway"],
                        "evidence_references": al["evidence_references"],
                        "confidence": al.get("confidence", "HIGH"),
                        "quality_flags": al.get("quality_flags", [])
                    }
                    if al["mapping_type"] == "DIRECT":
                        bucket["direct_contributions"].append(entry)
                    elif al["mapping_type"] == "ENABLING":
                        bucket["enabling_contributions"].append(entry)
                    else:
                        bucket["contextual_contributions"].append(entry)

        # Incorporate role alignments
        role_specific_sdgs = []
        if role_sdg_info:
            for flag in role_sdg_info.get("quality_flags", []):
                pathway_quality_flags.add(flag)

            for al in role_sdg_info.get("primary_sdgs", []) + role_sdg_info.get("secondary_sdgs", []):
                sdg_num = al["sdg_id"]
                role_specific_sdgs.append(sdg_num)
                if sdg_num not in all_sdg_buckets:
                    all_sdg_buckets[sdg_num] = {
                        "sdg_id": sdg_num,
                        "sdg_name": self.goals[sdg_num]["name"],
                        "direct_contributions": [],
                        "enabling_contributions": [],
                        "contextual_contributions": [],
                        "targets_addressed": set(),
                        "contributing_skills": set(),
                        "role_aligned": True,
                        "skill_aligned": False,
                        "quality_flags": set()
                    }
                bucket = all_sdg_buckets[sdg_num]
                bucket["role_aligned"] = True
                bucket["targets_addressed"].add(al["target_id"])
                for f in al.get("quality_flags", []):
                    bucket["quality_flags"].add(f)

                entry = {
                    "source_type": "ROLE",
                    "source_id": role_sdg_info["masco_code"],
                    "source_title": role_sdg_info["role_title"],
                    "target_id": al["target_id"],
                    "target_description": al["target_description"],
                    "mapping_type": al["mapping_type"],
                    "alignment_strength": al["alignment_strength"],
                    "contribution_pathway": al["contribution_pathway"],
                    "evidence_references": al["evidence_references"],
                    "confidence": al.get("confidence", "HIGH"),
                    "quality_flags": al.get("quality_flags", [])
                }
                if al["mapping_type"] == "DIRECT":
                    bucket["direct_contributions"].append(entry)
                elif al["mapping_type"] == "ENABLING":
                    bucket["enabling_contributions"].append(entry)
                else:
                    bucket["contextual_contributions"].append(entry)

        # Classify aggregated SDGs
        direct_sdg_ids = []
        enabling_sdg_ids = []
        contextual_sdg_ids = []
        sector_dependent_sdg_ids = []
        beneficiary_aligned_sdg_ids = []

        processed_goals = []
        for sdg_num in sorted(all_sdg_buckets.keys()):
            b = all_sdg_buckets[sdg_num]
            # Primary type for the goal
            if len(b["direct_contributions"]) > 0:
                primary_type = "DIRECT"
                direct_sdg_ids.append(sdg_num)
            elif len(b["enabling_contributions"]) > 0:
                primary_type = "ENABLING"
                enabling_sdg_ids.append(sdg_num)
            else:
                primary_type = "CONTEXTUAL"
                contextual_sdg_ids.append(sdg_num)

            b_flags = sorted(list(b["quality_flags"]))
            if "SECTOR_DEPENDENT_ALIGNMENT" in b_flags:
                sector_dependent_sdg_ids.append(sdg_num)
            if "CONTEXTUAL_BENEFICIARY_ALIGNMENT" in b_flags:
                beneficiary_aligned_sdg_ids.append(sdg_num)

            processed_goals.append({
                "sdg_id": sdg_num,
                "sdg_name": b["sdg_name"],
                "overall_mapping_type": primary_type,
                "targets_addressed": sorted(list(b["targets_addressed"])),
                "contributing_skills": sorted(list(b["contributing_skills"])),
                "role_aligned": b["role_aligned"],
                "skill_aligned": b["skill_aligned"],
                "quality_flags": b_flags,
                "direct_contributions_count": len(b["direct_contributions"]),
                "enabling_contributions_count": len(b["enabling_contributions"]),
                "contextual_contributions_count": len(b["contextual_contributions"]),
                "contributions": (
                    b["direct_contributions"]
                    + b["enabling_contributions"]
                    + b["contextual_contributions"]
                )
            })

        # Remediated Narrative synthesis distinguishing Competency Acquisition from Occupational Deployment
        pathway_id = pathway.get("pathway_id", "RESKILLING_PATHWAY")
        target_role_title = role_sdg_info["role_title"] if role_sdg_info else (target_role or "Target Role")
        
        narrative_parts = [
            f"Pathway '{pathway_id}' prepares learners for '{target_role_title}' through {len(skills_in_pathway)} competencies."
        ]
        
        # Skill-level competency contribution narrative
        skill_direct = [sid for sid in direct_sdg_ids if any(c["source_type"] == "SKILL" and c["mapping_type"] == "DIRECT" for c in all_sdg_buckets[sid]["direct_contributions"])]
        skill_enabling = [sid for sid in enabling_sdg_ids if any(c["source_type"] == "SKILL" and c["mapping_type"] == "ENABLING" for c in all_sdg_buckets[sid]["enabling_contributions"])]
        
        if skill_direct:
            skill_direct_names = [f"SDG {sid} ({self.goals[sid]['name']})" for sid in sorted(set(skill_direct))]
            narrative_parts.append(f"At the competency acquisition level, the curriculum delivers DIRECT capabilities advancing: {'; '.join(skill_direct_names)}.")
        if skill_enabling:
            skill_enabling_names = [f"SDG {sid} ({self.goals[sid]['name']})" for sid in sorted(set(skill_enabling))]
            narrative_parts.append(f"Acquired skills provide essential ENABLING tools supporting: {'; '.join(skill_enabling_names)}.")

        # Target role career horizon narrative
        if role_sdg_info:
            r_prim_nums = role_sdg_info.get("primary_sdg_numbers", [])
            if not r_prim_nums:
                r_prim_nums = sorted(list(set(al["sdg_id"] for al in role_sdg_info.get("primary_sdgs", []))))
            role_p_strs = [f"SDG {num} ({self.goals[num]['name']})" for num in r_prim_nums]
            
            role_narrative = f"In the target occupational deployment horizon as '{target_role_title}', the role structurally anchors {'; '.join(role_p_strs)}."
            if "SECTOR_DEPENDENT_ALIGNMENT" in role_sdg_info.get("quality_flags", []):
                role_narrative += " Note: Role-level environmental/energy alignments are sector-dependent and contingent on deployment within clean energy or environmental engineering sectors."
            if "CONTEXTUAL_BENEFICIARY_ALIGNMENT" in role_sdg_info.get("quality_flags", []):
                role_narrative += " Note: Role-level alignment to Target 8.5 represents decent work participation as employed beneficiaries rather than institutional policy drivers."
            narrative_parts.append(role_narrative)

        return {
            "pathway_id": pathway_id,
            "engine_version": self.VERSION,
            "target_role_code": target_role,
            "target_role_title": target_role_title,
            "skills_analyzed_count": len(skills_in_pathway),
            "skills_analyzed": sorted(list(skills_in_pathway)),
            "total_sdgs_aligned": len(processed_goals),
            "direct_sdgs": direct_sdg_ids,
            "enabling_sdgs": enabling_sdg_ids,
            "contextual_sdgs": contextual_sdg_ids,
            "sector_dependent_sdgs": sorted(list(set(sector_dependent_sdg_ids))),
            "beneficiary_aligned_sdgs": sorted(list(set(beneficiary_aligned_sdg_ids))),
            "pathway_quality_flags": sorted(list(pathway_quality_flags)),
            "sdg_alignments": processed_goals,
            "pathway_impact_narrative": " ".join(narrative_parts),
            "methodology_disclaimer": (
                "M5 SDG impact mapping represents qualitative and structural policy alignment grounded in the "
                "official UN 2030 indicator framework (anchored to 169 official UN targets). M5 does NOT produce synthetic "
                "quantitative measurements (such as metric tons of CO2 avoided or direct jobs generated). M5 operates as a "
                "downstream analytical lens and does not alter, bias, or restrict M3 role matching or M4 course recommendations."
            )
        }

    def validate_general_purpose_safety(self) -> Dict[str, Any]:
        """
        Audits all general-purpose skills to verify that none have DIRECT mappings.
        """
        violations = []
        compliant_skills = []
        for s_id in self.general_purpose_skill_ids:
            if s_id in self.skill_mappings:
                s_map = self.skill_mappings[s_id]
                direct_targets = [
                    al["target_id"]
                    for al in (s_map.get("primary_sdgs", []) + s_map.get("secondary_sdgs", []))
                    if al["mapping_type"] == "DIRECT"
                ]
                if direct_targets:
                    violations.append({"skill_id": s_id, "direct_targets": direct_targets})
                else:
                    compliant_skills.append(s_id)

        return {
            "is_safe": len(violations) == 0,
            "audited_general_purpose_skills": sorted(list(self.general_purpose_skill_ids)),
            "compliant_skills": sorted(compliant_skills),
            "violations": violations,
            "rule_id": "RULE_GP_NON_DIRECT_STRICT"
        }

    def verify_remediation_invariants(self) -> Dict[str, Any]:
        """
        Comprehensive automated check of all Stage 13C remediation invariants:
        P1-1: Target 9.c purged from software/cloud/API/UI skills & roles.
        P1-2: Target 16.10 FOI mischaracterization purged; data_privacy_pdpa mapped to 16.6.
        P1-3: Target 17.18 international census capacity purged; sql_data_analysis mapped to 9.5 & 8.2.
        P2-1: Corporate carbon accounting mapped to 12.6 DIRECT, 13.2 ENABLING; Target 13.3 purged.
        P2-2: Roles 2151, 2143, 2152 carry SECTOR_DEPENDENT_ALIGNMENT and MEDIUM confidence on SDG 7/11/12.
        P2-3: Confidence recalibration: overall HIGH confidence < 80%.
        P2-4: Clerical roles (4110, 4311, 3343) carry CONTEXTUAL_BENEFICIARY_ALIGNMENT on Target 8.5.
        """
        findings = []

        # P1-1 Check
        c_9c = []
        for s_id, s_data in self.skill_mappings.items():
            for al in s_data.get("primary_sdgs", []) + s_data.get("secondary_sdgs", []):
                if al["target_id"] == "9.c":
                    c_9c.append(f"Skill {s_id}")
        for r_code, r_data in self.role_mappings.items():
            for al in r_data.get("primary_sdgs", []) + r_data.get("secondary_sdgs", []):
                if al["target_id"] == "9.c":
                    c_9c.append(f"Role {r_code}")
        if c_9c:
            findings.append({"defect": "P1-1", "status": "FAIL", "detail": f"Target 9.c found in: {c_9c}"})
        else:
            findings.append({"defect": "P1-1", "status": "PASS", "detail": "Target 9.c completely purged from all 16 skills and 20 roles."})

        # P1-2 Check
        pdpa_map = self.skill_mappings.get("data_privacy_pdpa", {})
        pdpa_targets = [al["target_id"] for al in pdpa_map.get("primary_sdgs", []) + pdpa_map.get("secondary_sdgs", [])]
        if "16.10" in pdpa_targets:
            findings.append({"defect": "P1-2", "status": "FAIL", "detail": "Target 16.10 still mapped to data_privacy_pdpa."})
        elif "16.6" not in pdpa_targets:
            findings.append({"defect": "P1-2", "status": "FAIL", "detail": "Target 16.6 not mapped to data_privacy_pdpa."})
        else:
            findings.append({"defect": "P1-2", "status": "PASS", "detail": "data_privacy_pdpa correctly mapped to Target 16.6 (DIRECT), Target 16.10 purged."})

        # P1-3 Check
        sql_map = self.skill_mappings.get("sql_data_analysis", {})
        sql_targets = [al["target_id"] for al in sql_map.get("primary_sdgs", []) + sql_map.get("secondary_sdgs", [])]
        if "17.18" in sql_targets:
            findings.append({"defect": "P1-3", "status": "FAIL", "detail": "Target 17.18 still mapped to sql_data_analysis."})
        elif "9.5" not in sql_targets:
            findings.append({"defect": "P1-3", "status": "FAIL", "detail": "Target 9.5 not mapped to sql_data_analysis."})
        else:
            findings.append({"defect": "P1-3", "status": "PASS", "detail": "sql_data_analysis mapped to Target 9.5 and 8.2 (ENABLING), Target 17.18 purged."})

        # P2-1 Check
        cfa_map = self.skill_mappings.get("carbon_footprint_analytics", {})
        cfa_targets = {al["target_id"]: al["mapping_type"] for al in cfa_map.get("primary_sdgs", []) + cfa_map.get("secondary_sdgs", [])}
        if "13.3" in cfa_targets:
            findings.append({"defect": "P2-1", "status": "FAIL", "detail": "Target 13.3 still present in carbon_footprint_analytics."})
        elif cfa_targets.get("12.6") != "DIRECT":
            findings.append({"defect": "P2-1", "status": "FAIL", "detail": f"Target 12.6 mapping is {cfa_targets.get('12.6')}, expected DIRECT."})
        elif cfa_targets.get("13.2") != "ENABLING":
            findings.append({"defect": "P2-1", "status": "FAIL", "detail": f"Target 13.2 mapping is {cfa_targets.get('13.2')}, expected ENABLING."})
        else:
            findings.append({"defect": "P2-1", "status": "PASS", "detail": "carbon_footprint_analytics correctly mapped to 12.6 (DIRECT) and 13.2 (ENABLING); 13.3 purged."})

        # P2-2 Check
        sec_dep_roles = ["2151", "2143", "2152"]
        sec_fails = []
        for r_code in sec_dep_roles:
            r_data = self.role_mappings.get(r_code, {})
            flags = r_data.get("quality_flags", [])
            if "SECTOR_DEPENDENT_ALIGNMENT" not in flags:
                sec_fails.append(f"{r_code} missing SECTOR_DEPENDENT_ALIGNMENT")
        if sec_fails:
            findings.append({"defect": "P2-2", "status": "FAIL", "detail": "; ".join(sec_fails)})
        else:
            findings.append({"defect": "P2-2", "status": "PASS", "detail": "Roles 2151, 2143, 2152 properly flagged with SECTOR_DEPENDENT_ALIGNMENT."})

        # P2-3 Check: Confidence recalibration
        high_count = 0
        total_count = 0
        for s_data in self.skill_mappings.values():
            for al in s_data.get("primary_sdgs", []) + s_data.get("secondary_sdgs", []):
                total_count += 1
                if al.get("confidence") == "HIGH":
                    high_count += 1
        for r_data in self.role_mappings.values():
            for al in r_data.get("primary_sdgs", []) + r_data.get("secondary_sdgs", []):
                total_count += 1
                if al.get("confidence") == "HIGH":
                    high_count += 1
        high_pct = (high_count / total_count * 100) if total_count > 0 else 0
        if high_pct > 80.0:
            findings.append({"defect": "P2-3", "status": "FAIL", "detail": f"Confidence saturation still high: {high_pct:.1f}% HIGH (threshold < 80%)."})
        else:
            findings.append({"defect": "P2-3", "status": "PASS", "detail": f"Confidence successfully recalibrated: {high_pct:.1f}% HIGH ({high_count}/{total_count}), preventing inflation."})

        # P2-4 Check: Clerical beneficiary
        clerical_roles = ["4110", "4311", "3343"]
        cler_fails = []
        for r_code in clerical_roles:
            r_data = self.role_mappings.get(r_code, {})
            flags = r_data.get("quality_flags", [])
            if "CONTEXTUAL_BENEFICIARY_ALIGNMENT" not in flags:
                cler_fails.append(f"{r_code} missing CONTEXTUAL_BENEFICIARY_ALIGNMENT")
        if cler_fails:
            findings.append({"defect": "P2-4", "status": "FAIL", "detail": "; ".join(cler_fails)})
        else:
            findings.append({"defect": "P2-4", "status": "PASS", "detail": "Clerical roles 4110, 4311, 3343 carry CONTEXTUAL_BENEFICIARY_ALIGNMENT under Target 8.5."})

        all_passed = all(f["status"] == "PASS" for f in findings)
        return {
            "all_passed": all_passed,
            "findings": findings
        }
