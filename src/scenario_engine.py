"""
scenario_engine.py

M6 Future Workforce Scenario Engine (v1.1.0)
Standalone runtime module providing scenario-adjusted workforce foresight intelligence.
Consumes frozen M2 profiles and scenario transformations.
Provides clean, decoupled query interfaces for future M3 Role Matching.
Supports version="1.1.0" (default) and version="1.0.0" (legacy).
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class ScenarioEngine:
    """
    ScenarioEngine v1.1.0
    Encapsulates multi-scenario foresight evaluation across:
    - REFERENCE_2026 (Baseline Empirical Evidence)
    - MODERATE_COPILOT (Assistive AI Adoption)
    - FAST_AGENTIC (Accelerated Agentic AI Workflows)
    
    Zero demographic inputs permitted.
    Preserves channel separation (Automation vs Augmentation vs Demand Resilience).
    Decoupled from role matching; provides inputs for future M3 composite ranking.
    """
    
    VERSION = "1.1.0"
    SUPPORTED_SCENARIOS = ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]
    FORBIDDEN_DEMOGRAPHIC_KEYS = {
        "age", "gender", "ethnicity", "race", "religion", "marital_status",
        "nationality", "disability", "socioeconomic_background"
    }

    def __init__(self, base_dir: Optional[Path] = None, version: str = "1.1.0"):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir)
            
        self.version = version
        self.data_dir = self.base_dir / "data" / "scenarios"
        self._load_data()

    def _load_data(self):
        suffix = "_v1_1.json" if self.version == "1.1.0" else "_v1.json"
        defs_path = self.data_dir / f"scenario_definitions{suffix}"
        occ_path = self.data_dir / f"occupation_scenario_profiles{suffix}"
        skill_path = self.data_dir / f"skill_scenario_profiles{suffix}"

        if not defs_path.exists():
            raise FileNotFoundError(f"Missing scenario definitions: {defs_path}")
        if not occ_path.exists():
            raise FileNotFoundError(f"Missing occupation scenario profiles: {occ_path}")
        if not skill_path.exists():
            raise FileNotFoundError(f"Missing skill scenario profiles: {skill_path}")

        with open(defs_path, "r", encoding="utf-8") as f:
            self.scenario_defs = json.load(f)

        with open(occ_path, "r", encoding="utf-8") as f:
            occ_data = json.load(f)
            self.occ_profiles = occ_data["profiles"]

        with open(skill_path, "r", encoding="utf-8") as f:
            skill_data = json.load(f)
            self.skill_profiles = skill_data["profiles"]

        # Build fast lookup indexes: (id, scenario_id) -> profile
        self._occ_index: Dict[tuple, dict] = {}
        for p in self.occ_profiles:
            self._occ_index[(p["masco_code"], p["scenario_id"])] = p

        self._skill_index: Dict[tuple, dict] = {}
        for p in self.skill_profiles:
            self._skill_index[(p["skill_id"], p["scenario_id"])] = p

    def _validate_clean_query(self, **kwargs):
        for k in kwargs:
            if k.lower() in self.FORBIDDEN_DEMOGRAPHIC_KEYS:
                raise ValueError(f"Demographic variable '{k}' is strictly prohibited in M6 Scenario Engine.")

    def list_scenarios(self) -> List[Dict[str, Any]]:
        """Returns metadata for all available scenarios."""
        return [
            {
                "scenario_id": sc["scenario_id"],
                "scenario_name": sc["scenario_name"],
                "concept": sc["concept"],
                "narrative": sc["narrative"],
                "parameter_count": len(sc["assumptions"])
            }
            for sc in self.scenario_defs["scenarios"]
        ]

    def get_role_scenario(self, masco_code: str, scenario_id: str, **kwargs) -> Dict[str, Any]:
        """
        Retrieves scenario-adjusted profile for a specific 4-digit MASCO or Major Group fallback.
        """
        self._validate_clean_query(**kwargs)
        if scenario_id not in self.SUPPORTED_SCENARIOS:
            raise ValueError(f"Unsupported scenario_id '{scenario_id}'. Supported: {self.SUPPORTED_SCENARIOS}")
            
        key = (str(masco_code), scenario_id)
        if key not in self._occ_index:
            raise KeyError(f"Occupation '{masco_code}' not found under scenario '{scenario_id}'.")
            
        return self._occ_index[key]

    def get_skill_scenario(self, skill_id: str, scenario_id: str, **kwargs) -> Dict[str, Any]:
        """
        Retrieves scenario-adjusted profile for a specific core skill.
        """
        self._validate_clean_query(**kwargs)
        if scenario_id not in self.SUPPORTED_SCENARIOS:
            raise ValueError(f"Unsupported scenario_id '{scenario_id}'. Supported: {self.SUPPORTED_SCENARIOS}")
            
        key = (str(skill_id), scenario_id)
        if key not in self._skill_index:
            raise KeyError(f"Skill '{skill_id}' not found under scenario '{scenario_id}'.")
            
        return self._skill_index[key]

    def compare_role_scenarios(self, masco_code: str, **kwargs) -> Dict[str, Any]:
        """
        Compares an occupation across all 3 scenarios.
        """
        self._validate_clean_query(**kwargs)
        scenarios_data = {}
        for sc in self.SUPPORTED_SCENARIOS:
            scenarios_data[sc] = self.get_role_scenario(masco_code, sc)
            
        ref_profile = scenarios_data["REFERENCE_2026"]
        return {
            "masco_code": masco_code,
            "occupation_title": ref_profile["occupation_title"],
            "entity_granularity": ref_profile.get("entity_granularity", "FOUR_DIGIT_OCCUPATION"),
            "major_group": ref_profile["major_group"],
            "baseline_outlook": ref_profile["baseline_outlook"],
            "scenario_outlooks": {sc: scenarios_data[sc]["scenario_outlook"] for sc in self.SUPPORTED_SCENARIOS},
            "transition_pressures": {sc: scenarios_data[sc]["transition_pressure"] for sc in self.SUPPORTED_SCENARIOS},
            "reskilling_urgencies": {sc: scenarios_data[sc]["reskilling_urgency"] for sc in self.SUPPORTED_SCENARIOS},
            "scenarios": scenarios_data
        }

    def get_scenario_delta(self, masco_code: str, scenario_id: str, baseline_scenario: str = "REFERENCE_2026", **kwargs) -> Dict[str, Any]:
        """
        Computes numerical and categorical deltas between a target scenario and baseline scenario.
        """
        self._validate_clean_query(**kwargs)
        target = self.get_role_scenario(masco_code, scenario_id)
        base = self.get_role_scenario(masco_code, baseline_scenario)
        
        return {
            "masco_code": masco_code,
            "target_scenario": scenario_id,
            "baseline_scenario": baseline_scenario,
            "outlook_shift": f"{base['scenario_outlook']} -> {target['scenario_outlook']}",
            "reskilling_urgency_shift": f"{base['reskilling_urgency']} -> {target['reskilling_urgency']}",
            "transition_pressure_delta": round(target["transition_pressure"] - base["transition_pressure"], 1),
            "automation_pressure_delta": round(target["automation_pressure"] - base["automation_pressure"], 1),
            "augmentation_opportunity_delta": round(target["augmentation_opportunity"] - base["augmentation_opportunity"], 1),
            "demand_resilience_delta": round(target["demand_resilience"] - base["demand_resilience"], 1)
        }

    def get_all_role_scenarios(self, scenario_id: Optional[str] = None, granularity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Returns all occupation profiles, optionally filtered by scenario and/or entity granularity.
        """
        profiles = self.occ_profiles
        if scenario_id is not None:
            if scenario_id not in self.SUPPORTED_SCENARIOS:
                raise ValueError(f"Unsupported scenario_id '{scenario_id}'.")
            profiles = [p for p in profiles if p["scenario_id"] == scenario_id]
        if granularity is not None:
            profiles = [p for p in profiles if p.get("entity_granularity") == granularity]
        return profiles

    def get_all_skill_scenarios(self, scenario_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all skill profiles, optionally filtered by scenario."""
        if scenario_id is not None:
            if scenario_id not in self.SUPPORTED_SCENARIOS:
                raise ValueError(f"Unsupported scenario_id '{scenario_id}'.")
            return [p for p in self.skill_profiles if p["scenario_id"] == scenario_id]
        return self.skill_profiles

    def explain_role_scenario(self, masco_code: str, scenario_id: str) -> Dict[str, Any]:
        """
        Provides fully decomposed explainability answers:
        - WHAT CHANGED?
        - WHY?
        - WHICH BASELINE M2 EVIDENCE MATTERED?
        - WHICH SCENARIO ASSUMPTIONS CAUSED THE CHANGE?
        - HOW UNCERTAIN IS IT?
        """
        p = self.get_role_scenario(masco_code, scenario_id)
        ref = self.get_role_scenario(masco_code, "REFERENCE_2026")
        
        what_changed = (
            f"Under {scenario_id}, '{p['occupation_title']}' has scenario outlook '{p['scenario_outlook']}' "
            f"with reskilling urgency '{p['reskilling_urgency']}'. "
            f"Transition pressure is {p['transition_pressure']} (delta: {p['scenario_delta_from_reference']['transition_pressure_delta']:+0.1f} vs Reference)."
        )
        
        why = (
            f"Automation pressure reached {p['automation_pressure']} while augmentation opportunity expanded to {p['augmentation_opportunity']}. "
            f"Demand resilience is {p['demand_resilience']}."
        )
        
        evidence = (
            f"M2 baseline shortage level ({ref['demand_resilience']}) and ILO 2025 task decomposition "
            f"(baseline automation: {ref['automation_pressure']}, baseline augmentation: {ref['augmentation_opportunity']}) "
            f"formed the structural anchor."
        )
        
        assumptions = (
            f"Scenario assumptions {p['scenario_assumptions_used']} modified baseline exposures via "
            f"anchor-normalized AI adoption, agentic task reach, and technology diffusion multipliers."
        )
        
        uncertainty = (
            f"Sensitivity classification is {p['sensitivity_classification']} "
            f"(downside risk stability: {p.get('sensitivity_profile', {}).get('downside_risk_stability', 'N/A')}, "
            f"movement type: {p.get('sensitivity_profile', {}).get('movement_type', 'N/A')}). "
            f"Uncertainty band for transition pressure is [{p['uncertainty_band']['lower']}, {p['uncertainty_band']['upper']}]. "
            f"Scenario confidence is {p['scenario_confidence']}."
        )
        
        return {
            "masco_code": masco_code,
            "occupation_title": p["occupation_title"],
            "entity_granularity": p.get("entity_granularity", "FOUR_DIGIT_OCCUPATION"),
            "scenario_id": scenario_id,
            "what_changed": what_changed,
            "why": why,
            "m2_evidence_that_mattered": evidence,
            "scenario_assumptions_that_caused_change": assumptions,
            "uncertainty_level": uncertainty,
            "quality_flags": p["quality_flags"],
            "disclaimer": "SCENARIO OUTPUT / ESTIMATE — NOT AN EMPIRICAL FACT OR PROBABILITY"
        }
