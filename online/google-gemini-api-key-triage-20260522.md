# Google Gemini API Key Online Triage - 2026-05-22

Run ID: `ONLINE-20260522-003`

This pass checks a single online-only security/authentication-scope drift lead
from Truffle Security's 2026-02-25 write-up on Google API keys and Gemini.

The output remains only under `online/case-library/`. Nothing in this pass is
routed into an idea bank, `docs/case-bank/`, or offline benchmark packaging.

## De-Duplication Check

No existing online case covered Google Cloud API key credential semantics,
Gemini API key scoping, leaked-key blocking, or retroactive credential
privilege expansion. Existing Google-related records cover Google Ads
conversion adjustment partial failure and Google Merchant product status, which
are different API surfaces and failure modes.

## Output Summary

| Bucket | Count | Entries |
|---|---:|---|
| Accepted online-only cases | 1 | OL-AI-001 |
| Boundary / needs stronger source | 0 | - |
| Rejected as duplicate | 0 | - |

## Primary Online Case Queue

| Case ID | Candidate | Route | Why it stays online-only |
|---|---|---|---|
| OL-AI-001 | Google API keys can retroactively become Gemini credentials when Generative Language API is enabled | `online/case-library/cases/ol-ai-001-google-api-keys-retroactive-gemini-credential.md` | Requires real Google Cloud projects, live API keys, key restrictions, Gemini data, and Google's live leaked-key blocking state. |

## Line Ledger

| ID | Platform/API | Decision | Evidence strength | Offline reproduction | Note |
|---|---|---|---|---|---|
| OL-AI-001 | Google Cloud / Gemini API keys | `accept_online_case` | high mixed primary-source and researcher evidence | `not_possible` | Truffle reported live key privilege expansion; Google Gemini docs now acknowledge leaked-key blocking and a move toward AI Studio keys limited by default. |

## Checked Sources

- Truffle Security disclosure: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
- Google Gemini troubleshooting / blocked leaked keys: https://ai.google.dev/gemini-api/docs/troubleshooting
- Firebase API-key guidance: https://firebase.google.com/support/guides/security-checklist
- Maps JavaScript API-key setup: https://developers.google.com/maps/documentation/javascript/get-api-key?setupProd=configure

## Qualification

This counts under the online boundary as an authorization-scope drift. It is
not a package-version case and should not be promoted into offline benchmark
packaging. It is also now partly documented after disclosure; the silent part is
the pre-disclosure, retroactive privilege expansion of previously public keys.
