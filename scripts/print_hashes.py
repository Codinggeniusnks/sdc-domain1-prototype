import hashlib
from pathlib import Path
import json

base = Path('C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype')
files = {
    'm2_freeze_manifest': 'artifacts/m2_v1_1_1_freeze_manifest.json',
    'occupation_trend_profiles_v1_1_1': 'data/trends/processed/occupation_trend_profiles_v1_1_1.json',
    'skill_trend_profiles_v1_1_1': 'data/trends/processed/skill_trend_profiles_v1_1_1.json',
    'scenario_definitions_v1_1': 'data/scenarios/scenario_definitions_v1_1.json',
    'occupation_scenario_profiles_v1_1': 'data/scenarios/occupation_scenario_profiles_v1_1.json',
    'skill_scenario_profiles_v1_1': 'data/scenarios/skill_scenario_profiles_v1_1.json',
    'scenario_build_manifest_v1_1': 'data/scenarios/scenario_build_manifest_v1_1.json',
    'build_scenario_profiles_v1_1_py': 'scripts/build_scenario_profiles_v1_1.py',
    'scenario_engine_py': 'src/scenario_engine.py',
    'test_scenario_engine_v1_1_py': 'tests/test_scenario_engine_v1_1.py'
}

hashes = {}
for k, v in files.items():
    h = hashlib.sha256((base / v).read_bytes()).hexdigest()
    hashes[k] = h
    print(f'"{k}": "{h}",')
