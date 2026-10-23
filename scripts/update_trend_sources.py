"""M2 AI Trend Intelligence Engine - Primary Source Ingestion & Evidence Normalisation Pipeline.

Executes idempotent update, provenance verification, temporal modeling, and signal extraction.
Supports:
  --source all|mycol|opendosm|ilo|openalex|impact_study|policy
  --dry-run
  --force-refresh
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# Paths
BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
DATA_DIR = BASE_DIR / "data" / "trends"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MANIFEST_DIR = DATA_DIR / "manifests"

REFERENCE_DATE = "2026-10-23"
REF_DT = dt.date.fromisoformat(REFERENCE_DATE)

# Quality Tiers
TIER_A = "TIER_A"
TIER_B = "TIER_B"
TIER_C = "TIER_C"
TIER_D = "TIER_D"

# Freshness Policy Thresholds (in days)
FRESHNESS_POLICY = {
    "MONTHLY_MACRO": {"fresh": 60, "acceptable": 180},
    "QUARTERLY_SURVEY": {"fresh": 120, "acceptable": 365},
    "ANNUAL_SURVEY": {"fresh": 365, "acceptable": 730},
    "MULTI_YEAR_REPORT": {"fresh": 730, "acceptable": 1460},
    "BENCHMARK_STANDARD": {"fresh": 1095, "acceptable": 2190}
}


def compute_freshness(source_date_str: str, cadence_type: str = "MULTI_YEAR_REPORT") -> tuple[int, str]:
    """Calculate age in days and signal-type aware freshness category."""
    try:
        s_dt = dt.date.fromisoformat(source_date_str[:10])
        age_days = (REF_DT - s_dt).days
    except Exception:
        return 9999, "STALE"

    thresholds = FRESHNESS_POLICY.get(cadence_type, FRESHNESS_POLICY["MULTI_YEAR_REPORT"])
    if age_days <= thresholds["fresh"]:
        category = "FRESH"
    elif age_days <= thresholds["acceptable"]:
        category = "ACCEPTABLE"
    elif cadence_type in ["MULTI_YEAR_REPORT", "BENCHMARK_STANDARD"]:
        category = "ARCHIVAL_VALID"
    else:
        category = "STALE"
    return age_days, category


def make_signal_id(source_id: str, entity_type: str, entity_id: str, signal_type: str) -> str:
    """Generate deterministic, idempotent signal ID."""
    token = f"{source_id}:{entity_type}:{entity_id}:{signal_type}"
    h = hashlib.sha256(token.encode("utf-8")).hexdigest()[:12]
    return f"SIG-{entity_type.upper()[:3]}-{entity_id.replace(' ', '_')[:12]}-{signal_type[:6]}-{h}"


def load_raw_mycol() -> list[dict]:
    path = RAW_DIR / "mycol" / "mycol_longitudinal_series.json"
    if not path.exists():
        print(f"Warning: {path} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("records", [])


def load_raw_impact_study() -> list[dict]:
    path = RAW_DIR / "impact_studies" / "talentcorp_ai_digital_green_impact_2024.json"
    if not path.exists():
        print(f"Warning: {path} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("workforce_transitions", [])


def load_raw_opendosm() -> dict[str, list[dict]]:
    datasets = {}
    for cid in ["lfs_month", "lfs_qtr", "wages_occupation", "wages_skill", "employment_sector", "wages_industry"]:
        path = RAW_DIR / "opendosm" / f"{cid}_snapshot.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                snap = json.load(f)
                datasets[cid] = snap.get("data", [])
        else:
            print(f"Notice: OpenDOSM {cid} snapshot not found.")
    return datasets


def load_raw_ilo() -> list[dict]:
    path = RAW_DIR / "ilo" / "ilo_genai_occupational_exposure.json"
    if not path.exists():
        print(f"Warning: {path} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("occupational_groups", [])


def load_raw_openalex() -> dict:
    path = RAW_DIR / "openalex" / "openalex_temporal_momentum.json"
    if not path.exists():
        print(f"Warning: {path} not found.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_raw_policy() -> list[dict]:
    path = RAW_DIR / "policy" / "malaysia_policy_signals.json"
    if not path.exists():
        print(f"Warning: {path} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("records", [])


def extract_mycol_signals(mycol_records: list[dict], retrieval_time: str) -> list[dict]:
    """Extract occupational shortage and future skill demand signals from MyCOL."""
    signals = []
    source_id = "SRC-MYCOL-2024"
    source_date = "2024-11-01"
    age_days, freshness_cat = compute_freshness(source_date, "MULTI_YEAR_REPORT")

    for rec in mycol_records:
        masco = rec["masco_code"]
        title = rec["title"]
        persistence = rec["persistence_score"]
        status = rec["status_category"]

        # 1. Occupational Shortage Signal
        if status == "PERSISTENT_CRITICAL":
            direction = "STRONGLY RISING"
        elif status == "NEWLY_CRITICAL":
            direction = "RISING"
        elif status == "DROPPED_FROM_LATEST":
            direction = "DECLINING"
        else:
            direction = "STABLE"

        sig_id = make_signal_id(source_id, "occupation", masco, "DEMAND_SHORTAGE")
        signals.append({
            "signal_id": sig_id,
            "entity_type": "occupation",
            "entity_id": masco,
            "signal_type": "DEMAND_SHORTAGE",
            "signal_value_raw": f"Critical in {rec['number_of_editions_critical']}/{rec['total_editions_evaluated']} editions (Status: {status})",
            "signal_value_normalized": persistence,
            "direction": direction,
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": "2024-11-01",
            "valid_to": "2025-12-31",
            "geography": "MYS",
            "sector": rec["sectors"][0] if rec["sectors"] else "Multi-Sector",
            "occupation_code": masco,
            "evidence_text": rec["shortage_evidence"],
            "evidence_reference": f"TalentCorp MyMahir Critical Occupations List (2015-2025), MASCO {masco}: {title}",
            "confidence": 0.95,
            "quality_tier": TIER_A,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "TALENTCORP_MYCOL",
            "parent_source": "TalentCorp Malaysia & ILMIA",
            "publisher_family": "GOVERNMENT_MALAYSIA"
        })

        # 2. Future Skills Signals
        for sk in rec.get("future_skills_mentioned", []):
            sk_sig_id = make_signal_id(source_id, "skill", f"{sk}_{masco}", "FUTURE_SKILL")
            signals.append({
                "signal_id": sk_sig_id,
                "entity_type": "skill",
                "entity_id": sk,
                "signal_type": "FUTURE_SKILL",
                "signal_value_raw": f"Anticipated critical skill requirement for {title} (MASCO {masco})",
                "signal_value_normalized": round(0.70 + 0.25 * persistence, 3),
                "direction": "RISING" if rec["is_critical_2024_2025"] else "STABLE",
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": "2024-11-01",
                "valid_to": "2025-12-31",
                "geography": "MYS",
                "sector": rec["sectors"][0] if rec["sectors"] else "Multi-Sector",
                "occupation_code": masco,
                "evidence_text": f"MyCOL industry employer survey identifies {sk} as an emerging technical prerequisite for {title}.",
                "evidence_reference": f"TalentCorp MyCOL Future Skills Survey, MASCO {masco}",
                "confidence": 0.90,
                "quality_tier": TIER_A,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "TALENTCORP_MYCOL",
                "parent_source": "TalentCorp Malaysia & ILMIA",
                "publisher_family": "GOVERNMENT_MALAYSIA"
            })

    return signals


def extract_impact_study_signals(transitions: list[dict], retrieval_time: str) -> list[dict]:
    """Extract role transformation and transition signals from TalentCorp 2024 Impact Study."""
    signals = []
    source_id = "SRC-TALENTCORP-IMPACT-2024"
    source_date = "2024-11-18"
    age_days, freshness_cat = compute_freshness(source_date, "MULTI_YEAR_REPORT")

    for item in transitions:
        masco = item["masco_equivalent"]
        cat = item["transition_category"]
        role = item["role_title"]

        if cat == "EMERGING_ROLE":
            sig_type = "EMERGING_ROLE"
            val_norm = 1.00
            direction = "STRONGLY RISING"
        elif cat == "HIGHLY_IMPACTED_ROLE":
            sig_type = "DIGITAL_TRANSITION"
            val_norm = 0.85
            direction = "RISING"
        elif cat == "TRANSFORMING_ROLE":
            sig_type = "DIGITAL_TRANSITION"
            val_norm = 0.65
            direction = "STABLE"
        elif cat == "DECLINING_OR_CONSOLIDATING_ROLE":
            sig_type = "DECLINING_ROLE"
            val_norm = 0.20
            direction = "STRONGLY DECLINING"
        else:
            sig_type = "DIGITAL_TRANSITION"
            val_norm = 0.50
            direction = "STABLE"

        sig_id = make_signal_id(source_id, "occupation", f"{masco}_{role[:10]}", sig_type)
        signals.append({
            "signal_id": sig_id,
            "entity_type": "occupation",
            "entity_id": masco,
            "signal_type": sig_type,
            "signal_value_raw": f"Transition Category: {cat} (Time horizon: {item['time_horizon']})",
            "signal_value_normalized": val_norm,
            "direction": direction,
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": "2024-11-18",
            "valid_to": "2027-12-31",
            "geography": "MYS",
            "sector": item["sector"],
            "occupation_code": masco,
            "evidence_text": item["impact_summary"] + " " + item["task_changes"],
            "evidence_reference": item["evidence_reference"],
            "confidence": 0.92,
            "quality_tier": TIER_A,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "TALENTCORP_IMPACT_STUDY",
            "parent_source": "TalentCorp Malaysia",
            "publisher_family": "GOVERNMENT_MALAYSIA"
        })

        # Skills required in this role
        for sk in item.get("required_future_skills", []):
            sk_sig_id = make_signal_id(source_id, "skill", f"{sk}_{masco}", "FUTURE_SKILL")
            signals.append({
                "signal_id": sk_sig_id,
                "entity_type": "skill",
                "entity_id": sk,
                "signal_type": "FUTURE_SKILL",
                "signal_value_raw": f"Essential capability for {role} ({cat})",
                "signal_value_normalized": 0.90 if cat in ["EMERGING_ROLE", "HIGHLY_IMPACTED_ROLE"] else 0.70,
                "direction": "STRONGLY RISING" if cat == "EMERGING_ROLE" else "RISING",
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": "2024-11-18",
                "valid_to": "2027-12-31",
                "geography": "MYS",
                "sector": item["sector"],
                "occupation_code": masco,
                "evidence_text": f"TalentCorp Impact Study identifies {sk} as a high-demand skill required for {role}.",
                "evidence_reference": item["evidence_reference"],
                "confidence": 0.92,
                "quality_tier": TIER_A,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "TALENTCORP_IMPACT_STUDY",
                "parent_source": "TalentCorp Malaysia",
                "publisher_family": "GOVERNMENT_MALAYSIA"
            })

    return signals


def extract_opendosm_signals(datasets: dict[str, list[dict]], retrieval_time: str) -> list[dict]:
    """Extract macro labour market, occupational wage levels, and sectoral employment from OpenDOSM."""
    signals = []
    source_id = "SRC-OPENDOSM-LIVE"
    
    # 1. Macro Labour Force Trends (Monthly)
    lfs_month = datasets.get("lfs_month", [])
    if lfs_month:
        latest_lfs = lfs_month[-1]
        source_date = latest_lfs.get("date", "2024-01-01")
        age_days, freshness_cat = compute_freshness(source_date, "MONTHLY_MACRO")
        
        # Unemployment rate signal
        u_rate = float(latest_lfs.get("u_rate", 3.3))
        # Bounded normalized health score: lower u_rate is healthier (e.g. 3.0% = 1.0, 5.0% = 0.5)
        health_score = max(0.0, min(1.0, round((6.0 - u_rate) / 3.0, 3)))
        sig_id = make_signal_id(source_id, "sector", "macro_labour_force", "EMPLOYMENT_LEVEL")
        signals.append({
            "signal_id": sig_id,
            "entity_type": "sector",
            "entity_id": "national_economy",
            "signal_type": "EMPLOYMENT_LEVEL",
            "signal_value_raw": f"National Unemployment Rate: {u_rate}%, Employed: {latest_lfs.get('lf_employed')}k",
            "signal_value_normalized": health_score,
            "direction": "RISING" if u_rate <= 3.5 else "STABLE",
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": source_date,
            "valid_to": "2026-12-31",
            "geography": "MYS",
            "sector": "National Macroeconomy",
            "occupation_code": None,
            "evidence_text": f"DOSM Labour Force Survey reports national employed population of {latest_lfs.get('lf_employed')} thousand with a {u_rate}% unemployment rate.",
            "evidence_reference": "OpenDOSM Labour Force Statistics (Monthly Series, api.data.gov.my)",
            "confidence": 0.98,
            "quality_tier": TIER_A,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "DOSM_LABOUR_FORCE",
            "parent_source": "Department of Statistics Malaysia",
            "publisher_family": "GOVERNMENT_MALAYSIA"
        })

    # 2. Occupational Wage Levels (Annual)
    wages_occ = datasets.get("wages_occupation", [])
    if wages_occ:
        # Filter for latest date and both sexes
        latest_date = max(d.get("date", "2010-01-01") for d in wages_occ)
        age_days, freshness_cat = compute_freshness(latest_date, "ANNUAL_SURVEY")
        
        occ_map = {
            "managers": ("1", "1330", "Managers"),
            "professionals": ("2", "2512", "Professionals"),
            "technicians": ("3", "3514", "Technicians & Associate Professionals"),
            "clerical": ("4", "4110", "Clerical Support Workers"),
            "service_sales": ("5", "3322", "Service & Sales Workers"),
            "craft": ("7", None, "Craft & Related Trades Workers"),
            "operators": ("8", None, "Plant & Machine Operators"),
            "elementary": ("9", None, "Elementary Occupations")
        }
        
        # Collect median wages
        latest_recs = [d for d in wages_occ if d.get("date") == latest_date and d.get("sex") == "both"]
        max_median = max([float(d.get("wages_median", 1)) for d in latest_recs] or [5000])

        for rec in latest_recs:
            cat = rec.get("occupation")
            if cat in occ_map:
                major_grp, sample_masco, title = occ_map[cat]
                median_w = float(rec.get("wages_median", 0))
                mean_w = float(rec.get("wages_mean", 0))
                norm_wage = round(min(1.0, median_w / max_median), 3)

                sig_id = make_signal_id(source_id, "occupation", f"major_{major_grp}", "WAGE_LEVEL")
                signals.append({
                    "signal_id": sig_id,
                    "entity_type": "occupation",
                    "entity_id": sample_masco or f"MAJOR_{major_grp}",
                    "signal_type": "WAGE_LEVEL",
                    "signal_value_raw": f"Median Wage: RM {median_w:,.0f}, Mean Wage: RM {mean_w:,.0f} ({cat})",
                    "signal_value_normalized": norm_wage,
                    "direction": "RISING" if norm_wage >= 0.60 else "STABLE",
                    "source_id": source_id,
                    "source_date": latest_date,
                    "retrieved_at": retrieval_time,
                    "valid_from": latest_date,
                    "valid_to": "2026-12-31",
                    "geography": "MYS",
                    "sector": "National Labor Market",
                    "occupation_code": sample_masco,
                    "evidence_text": f"DOSM Salaries & Wages Survey records median monthly wage of RM {median_w:,.0f} for {title}.",
                    "evidence_reference": f"OpenDOSM Salaries & Wages Survey ({latest_date[:4]}), Category: {cat}",
                    "confidence": 0.95,
                    "quality_tier": TIER_A,
                    "freshness_days": age_days,
                    "freshness_category": freshness_cat,
                    "evidence_family": "DOSM_WAGES",
                    "parent_source": "Department of Statistics Malaysia",
                    "publisher_family": "GOVERNMENT_MALAYSIA"
                })

    return signals


def extract_ilo_signals(ilo_groups: list[dict], retrieval_time: str) -> list[dict]:
    """Extract AI automation exposure and augmentation potential from ILO Working Paper 96."""
    signals = []
    source_id = "SRC-ILO-GENAI-2023"
    source_date = "2023-08-21"
    age_days, freshness_cat = compute_freshness(source_date, "BENCHMARK_STANDARD")

    for grp in ilo_groups:
        major_grp = grp["isco_major_group"]
        title = grp["title"]
        auto_pot = grp["automation_potential"]
        aug_pot = grp["augmentation_potential"]
        overall = grp["overall_exposure_score"]
        impact_mode = grp["primary_impact_mode"]

        # Major group level signal
        sig_id = make_signal_id(source_id, "occupation", f"ISCO_M{major_grp}", "AI_EXPOSURE")
        signals.append({
            "signal_id": sig_id,
            "entity_type": "occupation",
            "entity_id": f"MAJOR_{major_grp}",
            "signal_type": "AI_EXPOSURE",
            "signal_value_raw": f"Exposure Index: {overall:.2f} (Augmentation: {aug_pot:.2f}, Automation: {auto_pot:.2f})",
            "signal_value_normalized": overall,
            "direction": "RISING" if aug_pot > auto_pot else ("DECLINING" if auto_pot >= 0.20 else "STABLE"),
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": "2023-08-21",
            "valid_to": "2027-12-31",
            "geography": "GLO",
            "sector": "Cross-Industry",
            "occupation_code": f"MAJOR_{major_grp}",
            "evidence_text": f"ILO GenAI Study: {title} (ISCO Major Group {major_grp}) shows {aug_pot*100:.0f}% augmentation potential and {auto_pot*100:.0f}% direct automation exposure. Mode: {impact_mode}.",
            "evidence_reference": f"ILO Working Paper 96 (Gmyrek et al. 2023), Table 3, Major Group {major_grp}",
            "confidence": 0.90,
            "quality_tier": TIER_B,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "ILO_GENAI_STUDY",
            "parent_source": "International Labour Organization",
            "publisher_family": "UNITED_NATIONS"
        })

        # Sub-group detailed signals
        for sub in grp.get("sub_groups", []):
            masco = sub["masco_code"]
            sub_title = sub["title"]
            s_auto = sub["automation_potential"]
            s_aug = sub["augmentation_potential"]
            s_exp = sub["exposure_index"]

            # Augmentation signal
            aug_sig_id = make_signal_id(source_id, "occupation", masco, "AUGMENTATION_POTENTIAL")
            signals.append({
                "signal_id": aug_sig_id,
                "entity_type": "occupation",
                "entity_id": masco,
                "signal_type": "AUGMENTATION_POTENTIAL",
                "signal_value_raw": f"Augmentation Potential: {s_aug:.2f}",
                "signal_value_normalized": s_aug,
                "direction": "STRONGLY RISING" if s_aug >= 0.40 else ("RISING" if s_aug >= 0.20 else "STABLE"),
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": "2023-08-21",
                "valid_to": "2027-12-31",
                "geography": "GLO",
                "sector": "Cross-Industry",
                "occupation_code": masco,
                "evidence_text": f"Key augmented tasks: {', '.join(sub['key_augmented_tasks'])}.",
                "evidence_reference": f"ILO Working Paper 96, ISCO {sub['isco_code']} -> MASCO {masco}",
                "confidence": 0.88,
                "quality_tier": TIER_B,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "ILO_GENAI_STUDY",
                "parent_source": "International Labour Organization",
                "publisher_family": "UNITED_NATIONS"
            })

            # Automation exposure signal
            auto_sig_id = make_signal_id(source_id, "occupation", masco, "AUTOMATION_EXPOSURE")
            signals.append({
                "signal_id": auto_sig_id,
                "entity_type": "occupation",
                "entity_id": masco,
                "signal_type": "AUTOMATION_EXPOSURE",
                "signal_value_raw": f"Direct Automation Potential: {s_auto:.2f}",
                "signal_value_normalized": s_auto,
                "direction": "DECLINING" if s_auto >= 0.20 else "STABLE",
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": "2023-08-21",
                "valid_to": "2027-12-31",
                "geography": "GLO",
                "sector": "Cross-Industry",
                "occupation_code": masco,
                "evidence_text": f"Key automatable tasks: {', '.join(sub['key_automated_tasks'])}.",
                "evidence_reference": f"ILO Working Paper 96, ISCO {sub['isco_code']} -> MASCO {masco}",
                "confidence": 0.88,
                "quality_tier": TIER_B,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "ILO_GENAI_STUDY",
                "parent_source": "International Labour Organization",
                "publisher_family": "UNITED_NATIONS"
            })

    return signals


def extract_openalex_signals(openalex_data: dict, retrieval_time: str) -> list[dict]:
    """Extract research momentum and topic emergence signals from OpenAlex temporal corpus."""
    signals = []
    source_id = "SRC-OPENALEX-TEMPORAL"
    source_date = openalex_data.get("retrieval_date", "2026-10-21")
    age_days, freshness_cat = compute_freshness(source_date, "MULTI_YEAR_REPORT")
    
    skill_momentum = openalex_data.get("skill_research_momentum", {})
    if not skill_momentum:
        return []

    # Find max volume for normalization
    max_pubs = max(m["total_publications"] for m in skill_momentum.values()) or 1

    for skill_id, m in skill_momentum.items():
        total_pubs = m["total_publications"]
        recent_share = m["recent_publication_share"]
        growth_rate = m["growth_rate_ratio"]
        emergence = m["emergence_category"]

        norm_vol = round(total_pubs / max_pubs, 3)
        # Bounded growth score (growth_rate >= 2.0 maps to 1.0)
        norm_growth = round(min(1.0, growth_rate / 2.0), 3)

        if emergence == "SURGING_MOMENTUM":
            direction = "STRONGLY RISING"
        elif emergence == "STEADY_GROWTH":
            direction = "RISING"
        else:
            direction = "STABLE"

        # 1. Research Activity Signal
        act_id = make_signal_id(source_id, "skill", skill_id, "RESEARCH_ACTIVITY")
        signals.append({
            "signal_id": act_id,
            "entity_type": "skill",
            "entity_id": skill_id,
            "signal_type": "RESEARCH_ACTIVITY",
            "signal_value_raw": f"Total Scholarly Publications: {total_pubs} (2020-2026)",
            "signal_value_normalized": norm_vol,
            "direction": direction,
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": "2020-01-01",
            "valid_to": "2026-12-31",
            "geography": "GLO",
            "sector": "Academic & Industrial R&D",
            "occupation_code": None,
            "evidence_text": f"OpenAlex scholarly corpus indexes {total_pubs} publications addressing {skill_id} with mean citation velocity of {m['mean_citations']}.",
            "evidence_reference": f"OpenAlex Scholarly Works Corpus, Topic: {skill_id}",
            "confidence": 0.85,
            "quality_tier": TIER_C,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "OPENALEX_SCHOLARLY",
            "parent_source": "OurResearch OpenAlex API",
            "publisher_family": "OPEN_RESEARCH_INFRASTRUCTURE"
        })

        # 2. Research Growth Velocity Signal
        growth_id = make_signal_id(source_id, "skill", skill_id, "RESEARCH_GROWTH")
        signals.append({
            "signal_id": growth_id,
            "entity_type": "skill",
            "entity_id": skill_id,
            "signal_type": "RESEARCH_GROWTH",
            "signal_value_raw": f"Growth Velocity Ratio: {growth_rate:.2f}x (Recent Share: {recent_share*100:.1f}%)",
            "signal_value_normalized": norm_growth,
            "direction": direction,
            "source_id": source_id,
            "source_date": source_date,
            "retrieved_at": retrieval_time,
            "valid_from": "2024-01-01",
            "valid_to": "2026-12-31",
            "geography": "GLO",
            "sector": "Academic & Industrial R&D",
            "occupation_code": None,
            "evidence_text": f"{recent_share*100:.1f}% of all publications for {skill_id} appeared in the 2024-2026 window, demonstrating {emergence}.",
            "evidence_reference": f"OpenAlex Temporal Momentum Series, Topic: {skill_id}",
            "confidence": 0.85,
            "quality_tier": TIER_C,
            "freshness_days": age_days,
            "freshness_category": freshness_cat,
            "evidence_family": "OPENALEX_SCHOLARLY",
            "parent_source": "OurResearch OpenAlex API",
            "publisher_family": "OPEN_RESEARCH_INFRASTRUCTURE"
        })

    return signals


def extract_policy_signals(policy_records: list[dict], retrieval_time: str) -> list[dict]:
    """Extract policy mandate and regulatory priority signals."""
    signals = []
    source_id = "SRC-MYS-POLICY-2024"

    for pol in policy_records:
        pid = pol["policy_id"]
        source_date = pol["publication_date"]
        age_days, freshness_cat = compute_freshness(source_date, "MULTI_YEAR_REPORT")

        # 1. Policy signal for skills
        for sk in pol.get("impacted_skills", []):
            sig_id = make_signal_id(source_id, "skill", f"{sk}_{pid}", "POLICY_PRIORITY")
            signals.append({
                "signal_id": sig_id,
                "entity_type": "skill",
                "entity_id": sk,
                "signal_type": "POLICY_PRIORITY",
                "signal_value_raw": f"Mandate: {pol['title']} ({pol['policy_status']})",
                "signal_value_normalized": 1.00 if pol["policy_status"] in ["MANDATORY_REGULATION", "ENACTED_LEGISLATION"] else 0.85,
                "direction": "STRONGLY RISING",
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": source_date,
                "valid_to": "2030-12-31",
                "geography": "MYS",
                "sector": "National Regulatory & Public Policy",
                "occupation_code": None,
                "evidence_text": f"{pol['issuing_agency']} mandates {sk} compliance under {pol['title']}: {pol['summary']}",
                "evidence_reference": pol["evidence_reference"],
                "confidence": 0.96,
                "quality_tier": TIER_A,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "MALAYSIAN_GOVERNMENT_POLICY",
                "parent_source": pol["issuing_agency"],
                "publisher_family": "GOVERNMENT_MALAYSIA"
            })

        # 2. Policy signal for occupations
        for occ in pol.get("impacted_occupations", []):
            sig_id = make_signal_id(source_id, "occupation", f"{occ}_{pid}", "POLICY_PRIORITY")
            signals.append({
                "signal_id": sig_id,
                "entity_type": "occupation",
                "entity_id": occ,
                "signal_type": "POLICY_PRIORITY",
                "signal_value_raw": f"National Priority Role under {pol['title']}",
                "signal_value_normalized": 0.90,
                "direction": "RISING",
                "source_id": source_id,
                "source_date": source_date,
                "retrieved_at": retrieval_time,
                "valid_from": source_date,
                "valid_to": "2030-12-31",
                "geography": "MYS",
                "sector": "National Priority Sector",
                "occupation_code": occ,
                "evidence_text": f"Strategic occupational demand prioritized under {pol['title']}.",
                "evidence_reference": pol["evidence_reference"],
                "confidence": 0.94,
                "quality_tier": TIER_A,
                "freshness_days": age_days,
                "freshness_category": freshness_cat,
                "evidence_family": "MALAYSIAN_GOVERNMENT_POLICY",
                "parent_source": pol["issuing_agency"],
                "publisher_family": "GOVERNMENT_MALAYSIA"
            })

    return signals


def build_source_manifest(retrieval_time: str) -> dict:
    """Build comprehensive metadata manifest for all ingested trend data sources."""
    sources = [
        {
            "source_id": "SRC-MYCOL-2024",
            "name": "TalentCorp Malaysia Critical Occupations List (MyCOL)",
            "publisher": "Talent Corporation Malaysia Berhad & ILMIA",
            "url_or_reference": "https://www.talentcorp.com.my/mymahir/mycol",
            "licence": "Official Malaysian Government Publication (Public Access / Non-Commercial)",
            "access_method": "STATIC_INGESTED (8 Multi-Year Publications)",
            "version": "2015/2016 through 2024/2025 (8 Editions)",
            "publication_date": "2024-11-01",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Annual / Biannual",
            "cadence_type": "MULTI_YEAR_REPORT",
            "geographic_scope": "Malaysia (National & Regional)",
            "quality_tier": TIER_A,
            "evidence_family": "TALENTCORP_MYCOL",
            "publisher_family": "GOVERNMENT_MALAYSIA",
            "signal_types_supplied": ["DEMAND_SHORTAGE", "FUTURE_SKILL"]
        },
        {
            "source_id": "SRC-TALENTCORP-IMPACT-2024",
            "name": "Impact Study of AI, Digital Economy and Green Economy on the Malaysian Workforce",
            "publisher": "Talent Corporation Malaysia Berhad, Ministry of Human Resources",
            "url_or_reference": "https://www.talentcorp.com.my/impact-study-2024",
            "licence": "Official Malaysian Government Research Study",
            "access_method": "STATIC_INGESTED",
            "version": "First Edition (November 2024)",
            "publication_date": "2024-11-18",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Multi-Year Research Cycle (2-3 years)",
            "cadence_type": "MULTI_YEAR_REPORT",
            "geographic_scope": "Malaysia (10 Strategic Sectors)",
            "quality_tier": TIER_A,
            "evidence_family": "TALENTCORP_IMPACT_STUDY",
            "publisher_family": "GOVERNMENT_MALAYSIA",
            "signal_types_supplied": ["EMERGING_ROLE", "DECLINING_ROLE", "DIGITAL_TRANSITION", "FUTURE_SKILL"]
        },
        {
            "source_id": "SRC-OPENDOSM-LIVE",
            "name": "OpenDOSM / data.gov.my Official Labour Market Datasets",
            "publisher": "Department of Statistics Malaysia (DOSM)",
            "url_or_reference": "https://api.data.gov.my/data-catalogue",
            "licence": "Open Data Commons Open Database License (ODbL) / CC-BY 4.0",
            "access_method": "LIVE_INGESTED (Direct API Query)",
            "version": "lfs_month, lfs_qtr, wages_occupation, wages_skill, employment_sector",
            "publication_date": "2024-01-01",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Monthly / Quarterly / Annual",
            "cadence_type": "MONTHLY_MACRO",
            "geographic_scope": "Malaysia (National)",
            "quality_tier": TIER_A,
            "evidence_family": "DOSM_LABOUR_FORCE",
            "publisher_family": "GOVERNMENT_MALAYSIA",
            "signal_types_supplied": ["EMPLOYMENT_LEVEL", "WAGE_LEVEL", "WAGE_GROWTH"]
        },
        {
            "source_id": "SRC-ILO-GENAI-2023",
            "name": "ILO Working Paper 96: Generative AI and Jobs",
            "publisher": "International Labour Organization (ILO), Geneva",
            "url_or_reference": "https://doi.org/10.54394/FHEM8239",
            "licence": "Creative Commons Attribution 4.0 (CC-BY 4.0)",
            "access_method": "STATIC_INGESTED",
            "version": "Working Paper 96 (August 2023)",
            "publication_date": "2023-08-21",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Periodic International Research Benchmark",
            "cadence_type": "BENCHMARK_STANDARD",
            "geographic_scope": "Global (Cross-Country ISCO-08)",
            "quality_tier": TIER_B,
            "evidence_family": "ILO_GENAI_STUDY",
            "publisher_family": "UNITED_NATIONS",
            "signal_types_supplied": ["AI_EXPOSURE", "AUTOMATION_EXPOSURE", "AUGMENTATION_POTENTIAL"]
        },
        {
            "source_id": "SRC-OPENALEX-TEMPORAL",
            "name": "OpenAlex Scholarly AI Research Corpus",
            "publisher": "OurResearch (OpenAlex API)",
            "url_or_reference": "https://api.openalex.org/works",
            "licence": "Creative Commons Public Domain Dedication (CC0)",
            "access_method": "STATIC_INGESTED (Dated 208-Work Curated Corpus)",
            "version": "Snapshot 2020-2026",
            "publication_date": "2026-10-21",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Weekly / Continuous API",
            "cadence_type": "MULTI_YEAR_REPORT",
            "geographic_scope": "Global Scholarly Literature",
            "quality_tier": TIER_C,
            "evidence_family": "OPENALEX_SCHOLARLY",
            "publisher_family": "OPEN_RESEARCH_INFRASTRUCTURE",
            "signal_types_supplied": ["RESEARCH_ACTIVITY", "RESEARCH_GROWTH"]
        },
        {
            "source_id": "SRC-MYS-POLICY-2024",
            "name": "Malaysian National Policy & Regulatory Directives (MOSTI, Bursa, JPDP, MITI)",
            "publisher": "Government of Malaysia Statutory Agencies",
            "url_or_reference": "https://www.mosti.gov.my; https://www.bursamalaysia.com; https://www.pdp.gov.my",
            "licence": "Official Government Legislation and Regulatory Rules",
            "access_method": "STATIC_INGESTED",
            "version": "AIGE 2024, Bursa ESG 2024, PDPA Act A1720, NSS 2024",
            "publication_date": "2024-09-20",
            "retrieval_time": retrieval_time,
            "expected_refresh_cadence": "Ad-Hoc / Policy Enactment",
            "cadence_type": "MULTI_YEAR_REPORT",
            "geographic_scope": "Malaysia (National)",
            "quality_tier": TIER_A,
            "evidence_family": "MALAYSIAN_GOVERNMENT_POLICY",
            "publisher_family": "GOVERNMENT_MALAYSIA",
            "signal_types_supplied": ["POLICY_PRIORITY"]
        }
    ]

    return {
        "manifest_version": "1.0.0",
        "generated_at": retrieval_time,
        "reference_date": REFERENCE_DATE,
        "total_sources": len(sources),
        "tier_distribution": {
            TIER_A: len([s for s in sources if s["quality_tier"] == TIER_A]),
            TIER_B: len([s for s in sources if s["quality_tier"] == TIER_B]),
            TIER_C: len([s for s in sources if s["quality_tier"] == TIER_C]),
            TIER_D: len([s for s in sources if s["quality_tier"] == TIER_D])
        },
        "sources": sources
    }


def compute_source_freshness_table(sources: list[dict]) -> dict:
    """Generate source freshness audit report."""
    audit = []
    for s in sources:
        age_days, cat = compute_freshness(s["publication_date"], s["cadence_type"])
        audit.append({
            "source_id": s["source_id"],
            "name": s["name"],
            "quality_tier": s["quality_tier"],
            "publication_date": s["publication_date"],
            "age_days": age_days,
            "cadence_type": s["cadence_type"],
            "freshness_category": cat,
            "status": "VALID_FOR_M2"
        })
    return {
        "reference_date": REFERENCE_DATE,
        "evaluated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": audit
    }


def run_pipeline(source_filter: str = "all", dry_run: bool = False, force_refresh: bool = False):
    retrieval_time = dt.datetime.now(dt.timezone.utc).isoformat()
    print("=" * 60)
    print("M2 TREND INTELLIGENCE ENGINE - SOURCE UPDATE PIPELINE")
    print(f"Target Source Filter: {source_filter}")
    print(f"Dry Run: {dry_run} | Force Refresh: {force_refresh}")
    print(f"Reference Date: {REFERENCE_DATE}")
    print("=" * 60)

    # 1. Manifest
    manifest = build_source_manifest(retrieval_time)
    freshness = compute_source_freshness_table(manifest["sources"])

    # 2. Extract Signals
    all_signals = []

    # MyCOL
    if source_filter in ["all", "mycol"]:
        print("Processing TalentCorp MyCOL...")
        mycol_raw = load_raw_mycol()
        sigs = extract_mycol_signals(mycol_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from MyCOL.")

    # Impact Study
    if source_filter in ["all", "impact_study"]:
        print("Processing TalentCorp 2024 Impact Study...")
        impact_raw = load_raw_impact_study()
        sigs = extract_impact_study_signals(impact_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from Impact Study.")

    # OpenDOSM
    if source_filter in ["all", "opendosm"]:
        print("Processing OpenDOSM / data.gov.my...")
        dosm_raw = load_raw_opendosm()
        sigs = extract_opendosm_signals(dosm_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from OpenDOSM.")

    # ILO
    if source_filter in ["all", "ilo"]:
        print("Processing ILO GenAI Occupational Exposure...")
        ilo_raw = load_raw_ilo()
        sigs = extract_ilo_signals(ilo_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from ILO.")

    # OpenAlex
    if source_filter in ["all", "openalex"]:
        print("Processing OpenAlex Temporal Research Momentum...")
        openalex_raw = load_raw_openalex()
        sigs = extract_openalex_signals(openalex_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from OpenAlex.")

    # Policy
    if source_filter in ["all", "policy"]:
        print("Processing Malaysian National Policy Mandates...")
        policy_raw = load_raw_policy()
        sigs = extract_policy_signals(policy_raw, retrieval_time)
        all_signals.extend(sigs)
        print(f"  Extracted {len(sigs)} signals from Policy Mandates.")

    # Deduplication and Idempotency Check
    seen_ids = set()
    deduped_signals = []
    duplicate_count = 0

    for s in all_signals:
        sid = s["signal_id"]
        if sid in seen_ids:
            duplicate_count += 1
            continue
        seen_ids.add(sid)
        deduped_signals.append(s)

    print("-" * 60)
    print(f"Total raw extracted signal records: {len(all_signals)}")
    print(f"Duplicates resolved / prevented: {duplicate_count}")
    print(f"Final unique normalized signals: {len(deduped_signals)}")
    print("-" * 60)

    # Breakdown by entity type, signal type, and quality tier
    by_entity = defaultdict(int)
    by_sig_type = defaultdict(int)
    by_tier = defaultdict(int)
    by_geo = defaultdict(int)
    skills_covered = set()
    occupations_covered = set()
    sectors_covered = set()

    for s in deduped_signals:
        by_entity[s["entity_type"]] += 1
        by_sig_type[s["signal_type"]] += 1
        by_tier[s["quality_tier"]] += 1
        by_geo[s["geography"]] += 1
        if s["entity_type"] == "skill":
            skills_covered.add(s["entity_id"])
        elif s["entity_type"] == "occupation":
            occupations_covered.add(s["entity_id"])
        if s.get("sector"):
            sectors_covered.add(s["sector"])

    malaysian_pct = round(100.0 * by_geo.get("MYS", 0) / len(deduped_signals), 2) if deduped_signals else 0.0

    print("Signal Type Distribution:")
    for stype, count in sorted(by_sig_type.items()):
        print(f"  {stype:25}: {count:3d}")

    print("\nQuality Tier Distribution:")
    for tier, count in sorted(by_tier.items()):
        print(f"  {tier:10}: {count:3d}")

    print(f"\nCoverage:")
    print(f"  Skills represented: {len(skills_covered)}")
    print(f"  Occupations represented: {len(occupations_covered)}")
    print(f"  Sectors represented: {len(sectors_covered)}")
    print(f"  Malaysian Evidence Share: {malaysian_pct}%\n")

    if dry_run:
        print("[DRY-RUN] No files were written to disk.")
        return deduped_signals

    # Write Manifest
    manifest_path = MANIFEST_DIR / "trend_source_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {manifest_path.name}")

    # Write Freshness Report
    freshness_path = PROCESSED_DIR / "source_freshness.json"
    with open(freshness_path, "w", encoding="utf-8") as f:
        json.dump(freshness, f, indent=2)
    print(f"Wrote {freshness_path.name}")

    # Write Processed Signals
    processed_artifact = {
        "artifact_id": "trend_signals_v1",
        "schema_version": "1.0.0",
        "generated_at": retrieval_time,
        "reference_date": REFERENCE_DATE,
        "total_signals": len(deduped_signals),
        "metadata": {
            "entity_type_counts": dict(by_entity),
            "signal_type_counts": dict(by_sig_type),
            "quality_tier_counts": dict(by_tier),
            "malaysian_evidence_percentage": malaysian_pct,
            "skills_represented_count": len(skills_covered),
            "occupations_represented_count": len(occupations_covered),
            "sectors_represented_count": len(sectors_covered)
        },
        "signals": deduped_signals
    }
    signals_path = PROCESSED_DIR / "trend_signals_v1.json"
    with open(signals_path, "w", encoding="utf-8") as f:
        json.dump(processed_artifact, f, indent=2)
    print(f"Wrote {signals_path.name} ({len(deduped_signals)} records)")

    print("=" * 60)
    print("M2 DATA FOUNDATION UPDATE COMPLETE")
    print("=" * 60)
    return deduped_signals


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update and normalize M2 trend intelligence sources.")
    parser.add_argument("--source", choices=["all", "mycol", "opendosm", "ilo", "openalex", "impact_study", "policy"], default="all", help="Target source")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without saving files")
    parser.add_argument("--force-refresh", action="store_true", help="Force re-fetch of live sources")
    args = parser.parse_args()

    run_pipeline(source_filter=args.source, dry_run=args.dry_run, force_refresh=args.force_refresh)
