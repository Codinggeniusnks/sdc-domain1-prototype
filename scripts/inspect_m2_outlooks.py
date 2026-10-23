import json
from pathlib import Path

base = Path('C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype')
with open(base / 'data/trends/processed/occupation_trend_profiles_v1_1_1.json', 'r', encoding='utf-8') as f:
    occs = json.load(f)['profiles']
with open(base / 'data/trends/processed/skill_trend_profiles_v1_1_1.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)['profiles']

print('Occupation baseline outlooks:', sorted(set(o['overall_outlook'] for o in occs)))
for o in occs:
    print(f"{o['occupation_code']} ({o['occupation_title'][:30]}): M2={o['overall_outlook']}, auto={o['automation_exposure']}, aug={o['augmentation_potential']}, ai={o['ai_exposure']}")

print('\nSkill baseline outlooks:', sorted(set(s['overall_outlook'] for s in skills)))
for s in skills:
    print(f"{s['skill_id']}: M2={s['overall_outlook']}, auto={s['automation_index']}, aug={s['augmentation_index']}")
