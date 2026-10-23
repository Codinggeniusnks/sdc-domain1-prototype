# O4 Credential Verification & Evidence Contract v1.0.0

## 1. Scope & Objective
This contract defines the schema and verification protocols for evidence submitted by learners to upgrade milestone completion from `COMPLETED_SELF_REPORTED` to `COMPLETED_VERIFIED`.

## 2. Evidence Data Schema
A valid credential evidence object must contain:

```json
{
  "credential_id": "STRING (Mandatory: unique credential reference)",
  "issuer": "STRING (Mandatory: accredited university, agency, or platform)",
  "issue_date": "STRING (Mandatory: ISO 8601 date YYYY-MM-DD)",
  "verification_uri": "STRING (Optional: web verification URL)",
  "sha256": "STRING (Optional: 64-hex cryptographic hash of certificate payload)"
}
```

## 3. Cryptographic Verification Rules
- If `sha256` is provided, it is checked against regular expression `^[a-fA-F0-9]{64}$`.
- Malformed or truncated hashes are rejected with an explicit error code.
- Verified credentials cannot be modified or replaced without opening an audited amendment record.

## 4. Employer Privacy Separation
- Individual evidence payloads (certificates, hashes, issuer details) remain strictly private to the learner.
- Employers viewing O1 cohort aggregates can only observe that $N$ workers in a team have attained verified status for a milestone, subject to small-cell suppression when $N < 5$.
