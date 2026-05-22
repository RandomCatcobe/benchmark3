# Data Scope And Credential Drift Online Triage - 2026-05-22

Run ID: `ONLINE-20260522-004`

This pass follows the Google Gemini API-key case and searches for similar
online-only drift where the same credential, endpoint, or integration code can
keep succeeding while service-side permission, privacy, or field-visibility
rules change the data observed by clients.

The output remains only under `online/case-library/`. Nothing in this pass is
routed into an idea bank, `docs/case-bank/`, or offline benchmark packaging.

## De-Duplication Check

Already-covered online records include e-commerce platform retries, partial
success, API version fall-forward, and the Google Gemini API-key credential
case. This pass therefore avoids payment/order/webhook delivery cases and adds
only auth-scope or data-visibility records from different platforms.

## Output Summary

| Bucket | Count | Entries |
|---|---:|---|
| Accepted online-only cases | 4 | OL-DATA-001 through OL-DATA-004 |
| Boundary / needs stronger source | 0 | - |
| Rejected as duplicate | 0 | - |

## Primary Online Case Queue

| Case ID | Candidate | Route | Why it stays online-only |
|---|---|---|---|
| OL-DATA-001 | Discord message content fields become empty without the privileged intent | `online/case-library/cases/ol-data-001-discord-message-content-privileged-intent.md` | Requires a live Discord application, bot verification state, guild membership, app settings, and Gateway/API payloads. |
| OL-DATA-002 | Slack `users.info` / `users.list` stop returning `email` under `users:read` alone | `online/case-library/cases/ol-data-002-slack-users-email-scope-narrowing.md` | Requires Slack workspace tokens, OAuth grants, legacy grandfathering state, and live user profile data. |
| OL-DATA-003 | Jira Cloud user objects remove `username`/`userKey` and make email visibility-dependent | `online/case-library/cases/ol-data-003-atlassian-jira-user-privacy-fields.md` | Requires Jira Cloud tenant state, account IDs, privacy settings, app scopes, and live user objects. |
| OL-DATA-004 | Shopify protected customer data returns only approved fields and redacts others | `online/case-library/cases/ol-data-004-shopify-protected-customer-data-redaction.md` | Requires a Shopify app, merchant/store install, Partner Dashboard review state, API scopes, plan/store type, and customer/order data. |

## Line Ledger

| ID | Platform/API | Decision | Evidence strength | Offline reproduction | Note |
|---|---|---|---|---|---|
| OL-DATA-001 | Discord Gateway / Messages API | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs say `content`, `embeds`, `attachments`, and `components` become empty without `MESSAGE_CONTENT`. |
| OL-DATA-002 | Slack Web API user objects | `accept_online_case` | high primary-source evidence | `not_possible` | Official changelog says `users:read` is no longer sufficient for the `email` field; `users:read.email` is required. |
| OL-DATA-003 | Atlassian Jira Cloud REST APIs | `accept_online_case` | high primary-source evidence | `not_possible` | Official GDPR migration docs remove `username`/`userKey` and make `emailAddress` nullable by privacy settings. |
| OL-DATA-004 | Shopify Admin / Customer Account APIs | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs say unapproved protected customer fields are redacted and unapproved type requests can return HTTP 200 with errors. |

## Checked Sources

- Discord Message Resource: https://docs.discord.com/developers/resources/message
- Discord privileged intents: https://support-dev.discord.com/hc/en-us/articles/6207308062871-What-are-Privileged-Intents
- Slack changelog: https://docs.slack.dev/changelog/2017-04-narrowing-email-access/
- Atlassian Jira privacy migration: https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/
- Shopify protected customer data: https://shopify.dev/docs/apps/launch/protected-customer-data

## Qualification

All four are online-only data-scope drift records. They are partly documented
now, but the integration failure mode is still silent: HTTP/Gateway calls can
continue to succeed while data fields become empty, null, omitted, redacted, or
visible only after extra review/scope approval.
