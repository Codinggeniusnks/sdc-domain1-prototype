# O2 Audit Ledger & Cryptographic Traceability — v1.0.0

## 1. Executive Summary
To satisfy enterprise governance, auditability, and regulatory oversight under the Malaysian Personal Data Protection Act (PDPA 2010), O2 maintains an immutable, append-only **Audit Ledger** recording every change detection and replanning event.

## 2. Audit Ledger Record Schema
Each ledger entry contains the following verified cryptographic schema:

```json
{
  "event_id": "EVT_0001",
  "replan_id": "REPLAN_EVT_0001_a4f8b2c1",
  "previous_state_id": "STATE_7a36d160",
  "candidate_state_id": "STATE_9b42e811",
  "trigger_type": "M2_TREND_SNAPSHOT_UPDATED",
  "root_causes": ["TREND_CHANGE"],
  "materiality": "HIGH_MATERIALITY",
  "affected_modules": ["M3", "M4", "O6", "O1"],
  "recompute_order": ["M3", "M4", "O6", "O1"],
  "publication_status": "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT",
  "previous_state_fingerprint": "a4f8b2c1d9e7...",
  "candidate_state_fingerprint": "9b42e811f5a0...",
  "changeset_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "created_at": "2026-10-24T05:02:00Z"
}
```

## 3. Cryptographic Changeset Hash
For absolute audit reproducibility, O2 generates a SHA-256 `changeset_hash` over the canonical serialized diff structure:
$$	ext{ChangesetHash} = 	ext{SHA-256}\left( 	ext{JSON}_{	ext{canonical}}\left( 	ext{AllDiffs} ight) ight)$$
Identical before/after transitions produce identical changeset hashes, enabling external auditors (e.g. O5) to verify change histories without re-running underlying models.
