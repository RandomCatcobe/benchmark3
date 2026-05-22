# OL-ECOM-010: Stripe Versioned And Duplicate Webhook Events

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Stripe
- API surface: webhook event destinations and Event objects
- Fields/concepts: event destination API version, event ordering, duplicate
  event delivery, retry behavior

## Drift Category

Webhook payload versioning, duplicate delivery, and ordering semantics.

## Checked Situation

Stripe's webhook docs describe event destinations receiving asynchronous Event
objects over HTTPS. The same official page says Stripe does not guarantee event
delivery order, webhook endpoints might receive the same event more than once,
and manual resends do not cancel automatic retries. It also states that the
Event sent to a destination is structured for that destination's specified
version.

The silent integration risk is a payment or subscription system that assumes a
single ordered stream and parses payloads as though they always match the
client's current API version. The endpoint can keep returning `2xx` while a
duplicate or older/newer-shaped event overwrites a newer state, double-creates
fulfillment work, or applies stale subscription state.

## Why Offline Reproduction Is Not Possible

The meaningful proof depends on a live Stripe account, event destination
configuration, Stripe's delivery retries, and real payment/subscription events.
A local replay can test handler idempotency, but cannot prove Stripe's live
delivery timing or destination-version behavior.

## Evidence URLs

- https://docs.stripe.com/webhooks
- https://docs.stripe.com/api/events
