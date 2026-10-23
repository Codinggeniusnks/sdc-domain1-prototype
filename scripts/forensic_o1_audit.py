"""
scripts/forensic_o1_audit.py

Executes comprehensive forensic verification across all 70 audits for Stage 15B.
Outputs detailed metrics and findings.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
import numpy as np

# Add ROOT and src to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from src.workforce_gap_engine import WorkforceGapEngine

def check_upstream_hashes():
    print("=== AUDIT 1: UPSTREAM IMMUTABILITY ===")
    hashes = {
        "m2": ("artifacts/m2_v1_1_1_freeze_manifest.json", "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"),
        "m6": ("data/scenarios/scenario_build_manifest_v1_1.json", "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"),
        "m3": ("data/matching/m3_build_manifest_v1_1.json", "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c"),
        "m4": ("artifacts/m4_v1_1_freeze_manifest.json", "448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f"),
        "m5": ("artifacts/m5_v1_1_freeze_manifest.json", "94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7"),
    }
    all_match = True
    for key, (path_str, expected) in hashes.items():
        p = ROOT / path_str
        if not p.exists():
            print(f"File {path_str} MISSING!")
            all_match = False
            continue
        data = p.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        match = (actual == expected)
        print(f"{key.upper()} ({path_str}): actual={actual[:16]}... expected={expected[:16]}... MATCH={match}")
        if not match:
            all_match = False
    return all_match

def audit_deficit_distribution():
    print("\n=== AUDIT 9 & 10: DEFICIT DISTRIBUTION ===")
    engine = WorkforceGapEngine()
    wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
    with open(wf_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)["profiles"]
    print(f"Loaded {len(profiles)} synthetic profiles from {wf_path.name}")
    
    # Collect all gaps and deficits
    all_deficits = []
    gaps_by_skill = {}
    
    for p in profiles:
        gaps = engine._extract_profile_gaps(p, scenario="REFERENCE_2026")
        for s_id, g_info in gaps.items():
            d = g_info["deficit"]
            all_deficits.append(d)
            gaps_by_skill.setdefault(s_id, []).append(d)
            
    all_deficits = np.array(all_deficits)
    print(f"Total non-zero deficit instances extracted: {len(all_deficits)}")
    print(f"Min deficit: {np.min(all_deficits)}")
    print(f"Max deficit: {np.max(all_deficits)}")
    print(f"Mean deficit: {np.mean(all_deficits):.4f}")
    print(f"Std deficit: {np.std(all_deficits):.4f}")
    unique_vals = np.unique(all_deficits)
    print(f"Unique deficit values: {unique_vals} (count={len(unique_vals)})")
    
    # Check why all are 1.0
    # In synthetic workforce, confirmed_skills are binary sets. When a profile lacks a skill, user_level=0.0, required_level=1.0, deficit = 1.0 - 0.0 = 1.0.
    return {
        "min": float(np.min(all_deficits)),
        "max": float(np.max(all_deficits)),
        "mean": float(np.mean(all_deficits)),
        "std": float(np.std(all_deficits)),
        "unique_count": len(unique_vals),
        "unique_vals": [float(x) for x in unique_vals]
    }

def audit_core_first_counterexample():
    print("\n=== AUDIT 14: CORE-FIRST MATHEMATICAL AUDIT ===")
    engine = WorkforceGapEngine()
    w = engine.weights
    print(f"Configured weights: {w}")
    
    # Counterexample from prompt:
    # Skill X: CORE prevalence = 0.02, IMPORTANT = 0, deficit = 0.4, transfer = 0.1, scenario = 0, prereq = 0
    # Skill Y: CORE prevalence = 0, IMPORTANT = 0.80, deficit = 1.0, transfer = 1.0, scenario = 1.0, prereq = 1.0
    
    score_X = (
        w["core_gap_prevalence"] * 0.02 +
        w["important_gap_prevalence"] * 0.0 +
        w["average_deficit"] * 0.4 +
        w["cross_role_transferability"] * 0.1 +
        w["scenario_urgency"] * 0.0 +
        w["prerequisite_centrality"] * 0.0
    ) * 100.0
    
    score_Y = (
        w["core_gap_prevalence"] * 0.0 +
        w["important_gap_prevalence"] * 0.80 +
        w["average_deficit"] * 1.0 +
        w["cross_role_transferability"] * 1.0 +
        w["scenario_urgency"] * 1.0 +
        w["prerequisite_centrality"] * 1.0
    ) * 100.0
    
    print(f"Skill X (has CORE gap 0.02): Priority Index = {score_X:.2f}")
    print(f"Skill Y (no CORE gap, high IMPORTANT): Priority Index = {score_Y:.2f}")
    print(f"Does Skill Y outrank Skill X? {score_Y > score_X}")
    print(f"Conclusion: CORE-first is WEIGHTED PREFERENCE ONLY, NOT STRUCTURALLY GUARANTEED.")

def audit_weight_sensitivity():
    print("\n=== AUDIT 18 & 19: WEIGHT SENSITIVITY ANALYSIS ===")
    engine = WorkforceGapEngine()
    wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
    with open(wf_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)["profiles"]
    base_ranks = engine.rank_workforce_reskilling_priorities(profiles)
    base_skills = [item["skill_id"] for item in base_ranks]
    base_top5 = base_skills[:5]
    print(f"Base Top 5: {base_top5}")
    
    # Plausible perturbations: ±0.05 on components, then renormalize
    perturbations = [
        {"name": "+0.05 core, -0.05 imp", "delta": {"core_gap_prevalence": 0.05, "important_gap_prevalence": -0.05}},
        {"name": "-0.05 core, +0.05 imp", "delta": {"core_gap_prevalence": -0.05, "important_gap_prevalence": 0.05}},
        {"name": "+0.05 transfer, -0.05 def", "delta": {"cross_role_transferability": 0.05, "average_deficit": -0.05}},
        {"name": "+0.05 scen, -0.05 core", "delta": {"scenario_urgency": 0.05, "core_gap_prevalence": -0.05}},
        {"name": "+0.05 prereq, -0.05 scen", "delta": {"prerequisite_centrality": 0.05, "scenario_urgency": -0.05}},
    ]
    
    from scipy.stats import spearmanr
    results = []
    
    for pert in perturbations:
        new_w = dict(engine.weights)
        for k, d in pert["delta"].items():
            new_w[k] += d
        # normalize
        tot = sum(new_w.values())
        new_w = {k: v / tot for k, v in new_w.items()}
        
        # calculate perturbed ranks
        engine.weights = new_w
        p_ranks = engine.rank_workforce_reskilling_priorities(profiles)
        p_skills = [item["skill_id"] for item in p_ranks]
        p_top5 = p_skills[:5]
        
        # Calculate Spearman correlation of ranks
        rank_base = {s: i for i, s in enumerate(base_skills)}
        rank_pert = {s: i for i, s in enumerate(p_skills)}
        x = [rank_base[s] for s in base_skills]
        y = [rank_pert[s] for s in base_skills]
        corr, _ = spearmanr(x, y)
        
        # Count skills changing rank by >= 3 positions
        large_shifts = sum(1 for s in base_skills if abs(rank_base[s] - rank_pert[s]) >= 3)
        top5_overlap = len(set(base_top5).intersection(set(p_top5)))
        
        results.append({
            "perturbation": pert["name"],
            "top5_overlap": f"{top5_overlap}/5",
            "spearman_corr": round(corr, 4),
            "shifts_ge_3": large_shifts
        })
        print(f"Perturbation '{pert['name']}': Top 5 Overlap={top5_overlap}/5, Spearman={corr:.4f}, Large Shifts(>=3)={large_shifts}")
        
    engine.weights = engine.config["priority_weights"] # reset
    return results

def audit_privacy_small_cells():
    print("\n=== AUDIT 33, 34, 35, 40: SMALL-CELL PRIVACY AUDIT ===")
    engine = WorkforceGapEngine()
    wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
    with open(wf_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)["profiles"]
    
    # Check shared learning opportunities
    shared = engine.identify_shared_learning_opportunities(profiles)
    print(f"Total shared learning opportunities returned: {len(shared)}")
    leaked_shared = [item for item in shared if item["profiles_affected"] < 5]
    print(f"Shared learning opportunities with profiles_affected < 5: {len(leaked_shared)}")
    for item in leaked_shared[:3]:
        print(f"  LEAK: Skill={item['shared_skill']}, profiles_affected={item['profiles_affected']}")
        
    # Check role transitions
    role_summary = engine.build_role_gap_summary(profiles)
    transitions = role_summary["role_transitions"]
    leaked_trans = [t for t in transitions if t["transition_volume"] < 5]
    print(f"Total role transitions: {len(transitions)}, transitions with volume < 5: {len(leaked_trans)}")
    for t in leaked_trans[:3]:
        print(f"  LEAK: {t['current_masco']} -> {t['target_masco']}, volume={t['transition_volume']}")
        
    # Check priority skills affected_profile_count
    priorities = engine.rank_workforce_reskilling_priorities(profiles)
    leaked_pri = [p for p in priorities if 0 < p["affected_profile_count"] < 5]
    print(f"Total priority skills: {len(priorities)}, skills with affected_profile_count < 5: {len(leaked_pri)}")
    for p in leaked_pri[:3]:
        print(f"  LEAK: Skill={p['skill_id']}, affected_profile_count={p['affected_profile_count']}")

def audit_build_manifest():
    print("\n=== AUDIT 63: BUILD MANIFEST VERIFICATION ===")
    man_path = ROOT / "data/workforce/o1_build_manifest_v1.json"
    with open(man_path) as f:
        manifest = json.load(f)
    all_ok = True
    for file_key, file_info in manifest["files"].items():
        p = ROOT / file_info["path"]
        if not p.exists():
            print(f"Manifest file {p} does not exist!")
            all_ok = False
            continue
        data = p.read_bytes()
        actual_h = hashlib.sha256(data).hexdigest()
        expected_h = file_info["sha256"]
        match = (actual_h == expected_h)
        print(f"Manifest file {file_info['path']}: actual={actual_h[:16]}... expected={expected_h[:16]}... MATCH={match}")
        if not match:
            all_ok = False
    return all_ok

if __name__ == "__main__":
    check_upstream_hashes()
    audit_deficit_distribution()
    audit_core_first_counterexample()
    audit_weight_sensitivity()
    audit_privacy_small_cells()
    audit_build_manifest()
