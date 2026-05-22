# OL-ECOM-011: Square Webhook Duplicate And Out-Of-Order Delivery

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Square
- API surface: Square Webhooks
- Concepts: notification URL, timely `2xx` acknowledgement, duplicate event,
  retry window, delivery order

## Drift Category

Webhook retry and event-order semantics.

## Checked Situation

Square's official webhook overview says webhook endpoints should respond with a
`2xx` status as soon as possible. If the application does not acknowledge a
notification in a timely manner, Square sends a duplicate event and the app has
10 seconds to respond. The docs also state that event notifications usually
arrive quickly, but delivery order is not guaranteed. If Square does not receive
a timely `2xx`, it retries with exponential backoff for up to 24 hours and then
discards the notification.

The silent integration risk is that order, inventory, payment, or POS handlers
that assume exactly-once ordered events can keep returning successful HTTP
responses while applying stale state, double-processing the same payment, or
missing a final state after retry exhaustion.

## Why Offline Reproduction Is Not Possible

The proof requires a live Square application, real webhook subscriptions, live
event production, and Square's hosted retry/delivery behavior. Local mocks can
exercise idempotency but cannot prove platform delivery timing.

## Evidence URLs

- https://developer.squareup.com/docs/webhooks/overview
