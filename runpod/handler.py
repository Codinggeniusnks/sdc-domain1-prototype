"""RunPod serverless handler (Optional Batch Signal Taxonomy Extractor).

For the Preliminary Round, AI Skills Compass runs 100% self-contained on Replit CPU in <10ms
with zero GPU dependency required. If deployed as a RunPod Serverless Endpoint (Min Workers = 0)
for bulk corpus ingestion or sponsor Proof-of-Use verification, this handler extracts only
canonical skills from the reviewed taxonomy and never invents unconstrained skills or jobs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from signals import extract_taxonomy_entities


def handler(job: dict) -> dict:
    job_input = job.get("input", {}) if isinstance(job, dict) else {}
    text = str(job_input.get("text") or job_input.get("prompt") or "").strip()
    skills, roles = extract_taxonomy_entities(text)
    return {
        "output": {
            "status": "ok" if skills else "insufficient_evidence",
            "extracted_skills": skills,
            "related_roles": roles,
            "mode": "runpod_serverless_taxonomy_constrained",
        }
    }


if __name__ == "__main__":
    try:
        import runpod  # type: ignore

        if os.getenv("RUNPOD_SERVERLESS_MODE") == "1":
            runpod.serverless.start({"handler": handler})
        else:
            sample = handler({"input": {"text": "Agentic AI workflow evaluation and SQL data analysis"}})
            print("RunPod handler local dry-run:", sample)
    except ImportError:
        sample = handler({"input": {"text": "Agentic AI workflow evaluation and SQL data analysis"}})
        print("RunPod package not installed; handler local dry-run succeeded:", sample)
