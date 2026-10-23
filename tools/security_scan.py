"""Security, secret elimination, and PII scanner for competition submission."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "OpenAI API Key": re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    "Generic Secret / Token": re.compile(r'(?i)(password|secret_key|api_key|token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}["\']'),
    "Malaysian NRIC": re.compile(r"\b\d{6}-\d{2}-\d{4}\b"),
    "Private RSA/EC Key": re.compile(r"BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"),
    "AWS Key": re.compile(r"AKIA[0-9A-Z]{16}"),
}

EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".system_generated"}

def run_scan() -> int:
    root = Path(".")
    findings = []
    scanned_files = 0

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name == "security_scan.py":
            continue

        scanned_files += 1
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            for rule_name, pat in PATTERNS.items():
                matches = pat.findall(content)
                if matches:
                    findings.append((str(path), rule_name, len(matches)))
        except Exception as e:
            print(f"[WARN] Could not read {path}: {e}")

    print(f"=== Security & Secret Elimination Scan ===")
    print(f"Files Scanned: {scanned_files}")
    print(f"Violations Found: {len(findings)}")

    if findings:
        for f in findings:
            print(f"  [ALERT] {f[0]}: {f[1]} ({f[2]} occurrences)")
        return 1

    print("[SUCCESS] Zero secrets, zero PII, zero private keys detected across entire repo.")
    return 0

if __name__ == "__main__":
    sys.exit(run_scan())
