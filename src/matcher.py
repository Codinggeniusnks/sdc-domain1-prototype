"""Explainable, deterministic role matcher, reskilling pathway builder, and scenario comparator.

Design Principles (Prompts 3, 4, 5):
- Simple, inspectable scoring formula:
    Total Score = 0.55 * Skill Readiness + 0.25 * Dated Signal Momentum + 0.20 * Scenario & Interest Fit
- Strictly constrained to SKILLS_CATALOG and ROLES_CATALOG; never invents roles, skills, courses, or stats.
- Explicit 'insufficient_evidence' state when profile skills are sparse (< 2 recognized skills)
  or when validated market signals are empty, stale, or malformed.
"""

from __future__ import annotations

from signals import validate_signals
from taxonomy import ROLES_CATALOG, SCENARIOS, SKILLS_CATALOG


def normalize_profile_skills(raw_skills: list[str] | str | None) -> list[str]:
    """Map user-supplied skill IDs or free-text skill phrases strictly to SKILLS_CATALOG keys."""
    if not raw_skills:
        return []
    if isinstance(raw_skills, str):
        tokens = [t.strip() for t in raw_skills.replace(";", ",").split(",") if t.strip()]
    elif isinstance(raw_skills, list):
        tokens = [str(t).strip() for t in raw_skills if str(t).strip()]
    else:
        return []

    recognized: list[str] = []
    for token in tokens:
        low = token.lower()
        if low in SKILLS_CATALOG and low not in recognized:
            recognized.append(low)
            continue
        for skill_id, info in SKILLS_CATALOG.items():
            if skill_id in recognized:
                continue
            if low == info["name"].lower() or any(
                kw in low or low in kw for kw in info["keywords"] if len(low) >= 3
            ):
                recognized.append(skill_id)
    return recognized


def build_reskilling_pathway(
    missing_req: list[str],
    missing_sup: list[str],
) -> dict:
    """Build an ordered, low-cost/free reskilling pathway for a role's missing skills."""
    target_skills = list(missing_req)
    # Include up to 2 supporting skills after required skills if pathway is short
    for s in missing_sup:
        if len(target_skills) >= 5:
            break
        if s not in target_skills:
            target_skills.append(s)

    steps: list[dict] = []
    for skill_id in target_skills:
        info = SKILLS_CATALOG.get(skill_id)
        if not info:
            continue
        step_meta = info["pathway_step"]
        steps.append(
            {
                "skill_id": skill_id,
                "skill_name": info["name"],
                "priority": "Required Gap" if skill_id in missing_req else "Recommended Stretch Skill",
                "stage": step_meta["stage"],
                "objective": step_meta["objective"],
                "resource_title": step_meta["resource_title"],
                "resource_url": step_meta["resource_url"],
                "cost_tier": step_meta["cost_tier"],
                "estimated_hours": step_meta["estimated_hours"],
                "estimated_weeks": step_meta["estimated_weeks"],
                "verification_status": step_meta["verification_status"],
                "sdg_tags": info["sdg_tags"],
            }
        )

    # Order by stage (1 -> 2 -> 3), with Required Gaps first within each stage
    steps.sort(key=lambda x: (0 if x["priority"] == "Required Gap" else 1, x["stage"], x["skill_name"]))
    for idx, st in enumerate(steps, start=1):
        st["step_number"] = idx

    total_hours = sum(s["estimated_hours"] for s in steps)
    total_weeks = sum(s["estimated_weeks"] for s in steps)
    return {
        "steps": steps,
        "total_estimated_hours": total_hours,
        "total_estimated_weeks": total_weeks,
        "disclaimer": (
            "Estimated study time assumes ~6–8 hours/week of self-paced learning. "
            "Where a specific commercial course is not verified, a transparent skill objective "
            "and verified public platform (e.g. AI Untuk Rakyat, HRD Corp e-LATiH, UN CC:e-Learn) are shown."
        ),
    }


def _score_single_role(
    role_id: str,
    role_info: dict,
    profile_skills: set[str],
    profile_interests: set[str],
    valid_signals: list[dict],
    scenario_id: str,
) -> dict:
    scenario = SCENARIOS.get(scenario_id, SCENARIOS["moderate_copilot"])
    skill_boosts = scenario.get("skill_boosts", {})

    req_list = role_info["required_skills"]
    sup_list = role_info["supporting_skills"]

    matched_req = [s for s in req_list if s in profile_skills]
    missing_req = [s for s in req_list if s not in profile_skills]
    matched_sup = [s for s in sup_list if s in profile_skills]
    missing_sup = [s for s in sup_list if s not in profile_skills]

    req_ratio = len(matched_req) / max(len(req_list), 1)
    sup_ratio = len(matched_sup) / max(len(sup_list), 1)
    skill_readiness_score = round((0.75 * req_ratio + 0.25 * sup_ratio) * 100, 1)

    # Dated signal momentum calculation
    role_skill_set = set(req_list) | set(sup_list)
    supporting_signals: list[dict] = []
    weighted_signal_points = 0.0

    for sig in valid_signals:
        sig_skills = [s for s in sig.get("extracted_skills", []) if s in role_skill_set]
        role_tagged = role_id in sig.get("related_roles", [])
        if sig_skills or role_tagged:
            boost = max([skill_boosts.get(s, 1.0) for s in sig_skills] + [1.0])
            points = (len(sig_skills) * 10.0 + (8.0 if role_tagged else 0.0)) * boost
            weighted_signal_points += points
            supporting_signals.append(
                {
                    "id": sig["id"],
                    "title": sig["title"],
                    "published_date": sig["published_date"],
                    "retrieved_date": sig["retrieved_date"],
                    "source_name": sig["source_name"],
                    "source_url": sig["source_url"],
                    "is_fallback": sig.get("is_fallback", False),
                    "matched_skills": [SKILLS_CATALOG[s]["name"] for s in sig_skills],
                }
            )

    # Cap signal momentum at 100
    signal_momentum_score = round(min(100.0, weighted_signal_points * 1.15), 1)

    # Scenario & interest fit score
    role_scenario_mult = role_info.get("scenario_weights", {}).get(scenario_id, 1.0)
    interest_bonus = 12.0 if role_info["category"].lower() in profile_interests else 0.0
    # Boost if scenario-boosted skills are required by this role
    scenario_skill_alignment = sum(skill_boosts.get(s, 1.0) - 1.0 for s in req_list) * 25.0
    raw_scenario_score = min(100.0, (role_scenario_mult * 65.0) + scenario_skill_alignment + interest_bonus)
    scenario_fit_score = round(raw_scenario_score, 1)

    if len(supporting_signals) == 0:
        # Role has zero supporting dated signals -> penalize and flag sparse role evidence
        total_score = round(0.55 * skill_readiness_score + 0.20 * scenario_fit_score, 1)
        evidence_status = "sparse_role_signals"
    else:
        total_score = round(
            0.55 * skill_readiness_score
            + 0.25 * signal_momentum_score
            + 0.20 * scenario_fit_score,
            1,
        )
        evidence_status = "supported"

    pathway = build_reskilling_pathway(missing_req, missing_sup)

    return {
        "role_id": role_id,
        "title": role_info["title"],
        "category": role_info["category"],
        "summary": role_info["summary"],
        "total_score": total_score,
        "evidence_status": evidence_status,
        "score_breakdown": {
            "skill_readiness_score": skill_readiness_score,
            "signal_momentum_score": signal_momentum_score,
            "scenario_fit_score": scenario_fit_score,
            "formula": "0.55 × Skill Readiness + 0.25 × Signal Momentum + 0.20 × Scenario Fit",
        },
        "matched_required_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in matched_req],
        "missing_required_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in missing_req],
        "matched_supporting_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in matched_sup],
        "missing_supporting_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in missing_sup],
        "supporting_signals": supporting_signals,
        "pathway": pathway,
        "sdg_links": role_info["sdg_links"],
        "uncertainty_note": role_info["uncertainty_note"],
    }


def rank_roles_for_profile(
    profile: dict | None,
    signals_payload: list[dict] | dict | None,
    scenario_id: str = "moderate_copilot",
    min_profile_skills: int = 2,
    reference_date: str | None = None,
) -> dict:
    """Evaluate a synthetic user profile against dated market signals and rank future roles."""
    if scenario_id not in SCENARIOS:
        scenario_id = "moderate_copilot"
    active_scenario = SCENARIOS[scenario_id]

    # 1. Validate market signals first (Malformed / empty / stale guardrail)
    if isinstance(signals_payload, dict) and "signals" in signals_payload:
        raw_signals = signals_payload.get("signals", [])
        source_mode = signals_payload.get("source_mode", "fallback_snapshot")
        is_fallback = bool(signals_payload.get("is_fallback", True))
        banner_label = signals_payload.get("banner_label", "")
    else:
        raw_signals = signals_payload if isinstance(signals_payload, list) else []
        source_mode = "direct_list"
        is_fallback = any(isinstance(s, dict) and s.get("is_fallback", False) for s in raw_signals)
        banner_label = "Direct Signal List"

    sig_validation = validate_signals(raw_signals, reference_date=reference_date)
    if sig_validation["status"] != "ok":
        return {
            "status": "insufficient_evidence",
            "reason": "signal_evidence_insufficient",
            "message": (
                "Insufficient Evidence: Market signal feed is empty, malformed, or older than the freshness threshold. "
                "AI Skills Compass refuses to generate confident role rankings without verified dated signals."
            ),
            "source_mode": source_mode,
            "is_fallback": is_fallback,
            "banner_label": banner_label,
            "signal_validation": sig_validation,
            "recognized_skills": [],
            "ranked_roles": [],
            "scenario": active_scenario,
            "scenario_comparison": [],
        }

    # 2. Validate user profile skills (Empty / sparse profile guardrail)
    if not isinstance(profile, dict):
        profile = {}
    recognized_ids = normalize_profile_skills(profile.get("skills", []))
    raw_interests = profile.get("interests", [])
    interest_set = {str(i).strip().lower() for i in raw_interests} if isinstance(raw_interests, list) else set()

    if len(recognized_ids) < min_profile_skills:
        return {
            "status": "insufficient_evidence",
            "reason": "sparse_profile_skills",
            "message": (
                f"Insufficient Evidence: Profile contains {len(recognized_ids)} recognized skill(s) "
                f"(minimum {min_profile_skills} required for reliable role matching). Please select or add at least "
                f"{min_profile_skills} skills from the reviewed catalog rather than relying on guesswork."
            ),
            "source_mode": source_mode,
            "is_fallback": is_fallback,
            "banner_label": banner_label,
            "signal_validation": sig_validation,
            "recognized_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in recognized_ids],
            "ranked_roles": [],
            "scenario": active_scenario,
            "scenario_comparison": [],
        }

    # 3. Score and rank roles under the active scenario
    valid_signals = sig_validation["valid_signals"]
    skill_set = set(recognized_ids)
    scored_roles = [
        _score_single_role(r_id, r_info, skill_set, interest_set, valid_signals, scenario_id)
        for r_id, r_info in ROLES_CATALOG.items()
    ]
    scored_roles.sort(
        key=lambda r: (
            r["total_score"],
            r["score_breakdown"]["skill_readiness_score"],
            r["score_breakdown"]["signal_momentum_score"],
        ),
        reverse=True,
    )

    top_score = scored_roles[0]["total_score"] if scored_roles else 0.0
    for idx, role in enumerate(scored_roles, start=1):
        role["rank"] = idx
        bd = role["score_breakdown"]
        matched_count = len(role["matched_required_skills"])
        total_req = matched_count + len(role["missing_required_skills"])
        sig_count = len(role["supporting_signals"])
        if idx == 1:
            role["why_ranked_here"] = (
                f"Ranked #1 ({role['total_score']}/100) because your profile already matches "
                f"{matched_count}/{total_req} required core skills (Readiness: {bd['skill_readiness_score']}%), "
                f"backed by {sig_count} dated market signal(s) (Momentum: {bd['signal_momentum_score']}%) "
                f"and {active_scenario['name']} weighting ({bd['scenario_fit_score']}%)."
            )
        else:
            gap_to_top = round(top_score - role["total_score"], 1)
            role["why_ranked_here"] = (
                f"Ranked #{idx} ({role['total_score']}/100, {gap_to_top} pts behind #1): matches "
                f"{matched_count}/{total_req} required skills (Readiness: {bd['skill_readiness_score']}%) "
                f"with {sig_count} dated signal(s) (Momentum: {bd['signal_momentum_score']}%) "
                f"and Scenario Fit of {bd['scenario_fit_score']}%."
            )

    # 4. Compute multi-scenario comparison matrix (Must-Have Feature 6: Handling Uncertainty)
    scenario_comparison: list[dict] = []
    for sc_id, sc_meta in SCENARIOS.items():
        sc_roles = [
            _score_single_role(r_id, r_info, skill_set, interest_set, valid_signals, sc_id)
            for r_id, r_info in ROLES_CATALOG.items()
        ]
        sc_roles.sort(key=lambda r: r["total_score"], reverse=True)
        scenario_comparison.append(
            {
                "scenario_id": sc_id,
                "scenario_name": sc_meta["name"],
                "badge": sc_meta["badge"],
                "assumptions": sc_meta["assumptions"],
                "uncertainty_level": sc_meta["uncertainty_level"],
                "top_role": sc_roles[0]["title"],
                "top_role_score": sc_roles[0]["total_score"],
                "runner_up_role": sc_roles[1]["title"],
                "runner_up_score": sc_roles[1]["total_score"],
            }
        )

    return {
        "status": "ok",
        "reason": "matched",
        "message": (
            "Recommendations are decision-support estimates grounded in your synthetic profile and dated signals. "
            "Human career judgment remains in charge."
        ),
        "source_mode": source_mode,
        "is_fallback": is_fallback,
        "banner_label": banner_label,
        "signal_validation": sig_validation,
        "recognized_skills": [{"id": s, "name": SKILLS_CATALOG[s]["name"]} for s in recognized_ids],
        "ranked_roles": scored_roles,
        "scenario": active_scenario,
        "scenario_comparison": scenario_comparison,
    }
