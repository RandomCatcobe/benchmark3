# OL-ECOM-021: Mailgun Webhook Retry And Scope Dedup

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Mailgun
- API surface: webhooks
- Fields/concepts: account-level webhook, domain-level webhook, retry schedule,
  delivery status events

## Drift Category

Webhook scope deduplication and retry semantics.

## Checked Situation

Mailgun's webhook docs say domain-level and account-level webhooks can both be
configured. If the same URL is configured for the same event at both levels,
Mailgun treats that as a duplicate and sends only once. The docs also describe
retry behavior: `200` is considered success, `406` is rejected without retry,
and other responses are retried on a schedule.

The silent integration risk is that a sender or CRM connector expects both
domain and account hooks to fire, or expects a failed endpoint to be retried
forever. A delivery/bounce/unsubscribe event can be legitimately delivered only
once because of scope deduplication, or eventually stop after retry exhaustion,
while the email send itself succeeded.

## Why Offline Reproduction Is Not Possible

The proof requires live Mailgun account/domain configuration, actual outbound or
inbound email events, and Mailgun's hosted delivery/retry engine. A local mock
cannot prove account-vs-domain deduplication or retry timing.

## Evidence URLs

- https://help.mailgun.com/hc/en-us/articles/202236504-Webhooks
