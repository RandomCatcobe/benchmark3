# OL-AI-001: Google API keys retroactively gain Gemini credential semantics

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Google Cloud / Google AI Studio / Gemini API
- API surface: Google API keys (`AIza...`) and Generative Language API endpoints
- Fields/concepts: API key restrictions, enabled APIs, leaked key blocking,
  Files API, cached contents, models endpoint

## Drift Category

Authorization-scope and credential-semantics drift.

## Checked Situation

Firebase and Maps documentation historically treated many Google API keys as
client-embeddable project identifiers rather than secrets. Firebase says API
keys for Firebase services identify the project/app and do not need to be
treated as secrets when restricted to Firebase services. Maps JavaScript setup
docs tell developers to include an API key in browser requests.

Truffle Security reported that when the Generative Language API is enabled on a
Google Cloud project, existing Google API keys in that project can become valid
Gemini credentials. In the reported scenario, a key originally embedded for a
public Maps-style use can access Gemini API surfaces such as files, cached
contents, or model listing. The application code and key string do not change;
the vendor-side enabled-service state and credential meaning change underneath
the integrator.

Google's Gemini troubleshooting docs now acknowledge a vulnerability around
publicly exposed API keys and say Google is blocking known leaked keys from
Gemini API access, moving toward AI Studio keys that are limited by default,
and planning proactive communication for affected keys.

This counts as an online-only silent-drift case because the same credential
shape can move from public identifier to sensitive authentication token without
a local code change or a hard API error. It is not a normal offline benchmark
candidate because the proof depends on live Google Cloud project state.

## Why Offline Reproduction Is Not Possible

The proof requires real Google Cloud projects, historical API keys, service
enablement state, key restrictions, Gemini account data such as uploaded files
or cached contents, and Google's live leaked-key blocking pipeline. The
repository cannot safely include real API keys or deterministically recreate
vendor-side privilege assignment.

## Evidence URLs

- https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
- https://ai.google.dev/gemini-api/docs/troubleshooting
- https://firebase.google.com/support/guides/security-checklist
- https://developers.google.com/maps/documentation/javascript/get-api-key?setupProd=configure
