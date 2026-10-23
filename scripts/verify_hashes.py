import hashlib
import json
from pathlib import Path

BASE = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
with open(BASE / "data/trends/processed/m2_build_manifest_v1_1.json") as f:
    manifest = json.load(f)

print("=== CHECK 12: REPRODUCIBILITY MANIFEST AUDIT ===")
all_match = True
for key, expected_hash in manifest.get("output_artifacts", {}).items():
    p = BASE / f"data/trends/processed/{key}.json"
    if not p.exists():
        print(f"Missing file: {p}")
        all_match = False
        continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    match = (h == expected_hash)
    if not match:
        all_match = False
    print(f"{key}: match={match} (current={h[:8]}..., expected={expected_hash[:8]}...)")

print(f"All output hashes match manifest? {all_match}")
