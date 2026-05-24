# Online L3+ Candidate Research

This folder is a research ledger for online-only L3+/S3+ candidates.

It is intentionally not a migration into `online/case-bank/`, `docs/case-bank/`,
or any offline benchmark package. The current target is:

- existing high-evidence accepted online records after strict downgrade: 19
- new keepable L3+/S3+ candidates in `l3_candidate_ledger.jsonl`: 73
- boundary/source-needed L3 candidates in `l3_candidate_ledger.jsonl`: 5
- strict-audited current total: 92 keepable online L3+/S3+ examples
- original target remains 100 after replacement candidates are added

Rows use `recommended_status: "online_keep"` only when the candidate has a
primary official source and is framed as live-service drift rather than a hard
break or client-only mapping issue.

## 2026-05-24 strict S4 / strong S3 pass

`s4_strong_s3_candidate_ledger_20260524.jsonl` is a stricter follow-up ledger:

- exactly 100 new online-only candidates
- current strict-audited evidence levels: 100 `STRONG_S3`, 0 `S4`
- `S4` is reserved for rows with attached live proof, credentialed probe
  evidence, or user-supplied production logs
- 89 rows use `recommended_status: "online_keep"`
- 11 rows are downgraded to `recommended_status: "boundary_needs_source"`
  because the current source URL is unavailable or no longer directly supports
  the claim
- no migration into any formal case-bank package
