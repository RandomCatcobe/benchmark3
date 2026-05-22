# OL-ECOM-019: Twilio Event Streams Duplicate And Out-Of-Order Events

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Twilio
- API surface: Event Streams webhook sink
- Fields/concepts: event `id`, retry, exponential backoff, out-of-order
  delivery, sink response code

## Drift Category

Event stream retry, deduplication, and ordering semantics.

## Checked Situation

Twilio's Event Streams docs say failed deliveries are retried with exponential
backoff and jitter until delivery succeeds or four hours pass. The same page
says Event Streams might deliver events out of order, and that duplicate events
can occur due to retries, incident remediation, or internal temporary errors.
Twilio recommends deduplicating by event `id`, and returning `200` even when a
duplicate is discarded so the webhook sink does not retry again.

The silent integration risk is a messaging, fulfillment, or notification
pipeline that assumes status callbacks arrive once and in order. Valid Twilio
events can replay or arrive after newer events, causing stale delivery status,
duplicate notification work, or wrong customer communication state.

## Why Offline Reproduction Is Not Possible

The proof requires a live Twilio account, Event Streams configuration, event
sinks, Twilio-hosted retries, and real communication events. Local replay can
exercise handler behavior but not Twilio's delivery timing.

## Evidence URLs

- https://www.twilio.com/docs/events/event-delivery-and-duplication
