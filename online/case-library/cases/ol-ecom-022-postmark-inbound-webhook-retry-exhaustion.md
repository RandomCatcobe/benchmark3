# OL-ECOM-022: Postmark Inbound Webhook Retry Exhaustion

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Postmark
- API surface: inbound webhooks
- Fields/concepts: `200 OK`, `403 Forbidden`, retry schedule, Inbound Error

## Drift Category

Inbound webhook retry exhaustion and missed message semantics.

## Checked Situation

Postmark's support documentation says inbound webhooks are retried when the
server does not return `200 OK`. It describes 10 retries over roughly 10.5
hours, with retries stopping immediately for `403 Forbidden`. After all retries
are exhausted, the message is marked as an Inbound Error, and long endpoint
downtime can cause messages to be missed unless they are manually retried.

The silent integration risk is an order, support, or reply-processing system
that treats Postmark inbound webhook delivery as durable. The inbound email
exists in Postmark, but a slow, down, or misconfigured endpoint can lose the
event after retry exhaustion while the local application never sees the reply.

## Why Offline Reproduction Is Not Possible

The proof requires live Postmark inbound configuration, real inbound mail,
Postmark-hosted retries, and account UI state. A local fixture can test handler
responses but cannot prove retry exhaustion in production.

## Evidence URLs

- https://postmarkapp.com/support/article/understanding-inbound-webhook-retries-in-postmark
