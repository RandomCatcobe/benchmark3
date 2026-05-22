# OL-ECOM-013: Razorpay At-Least-Once Webhook Timeout

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Razorpay
- API surface: webhooks
- Fields/concepts: non-2xx delivery failure, 5-second timeout,
  `x-razorpay-event-id`, webhook disablement

## Drift Category

At-least-once delivery and duplicate webhook processing.

## Checked Situation

Razorpay's webhook FAQ says every event that receives a non-2xx response is
considered a delivery failure and is retried with exponential backoff for 24
hours. The same page says Razorpay uses at-least-once delivery semantics: if a
server accepts an event but does not respond within 5 seconds, the session is
marked as a timeout and the same event can be sent again. Razorpay recommends
checking `x-razorpay-event-id` to detect duplicates.

The silent integration risk is a payment/order handler that performs the
business update but responds too slowly. The original payment event and the
retry both look valid, so downstream systems can create duplicate orders,
credits, payouts, or fulfillment jobs while all webhook deliveries appear
successful after retry.

## Why Offline Reproduction Is Not Possible

The proof depends on a live Razorpay merchant account, dashboard webhook
configuration, hosted retry policy, payment/order events, and production timing.
A local replay can test idempotency but cannot prove Razorpay's delivery and
disablement behavior.

## Evidence URLs

- https://razorpay.com/docs/webhooks/faqs/?preferred-country=US
