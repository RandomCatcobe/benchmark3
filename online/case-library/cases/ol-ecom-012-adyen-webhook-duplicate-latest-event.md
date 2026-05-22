# OL-ECOM-012: Adyen Duplicate Webhook Latest-Event Semantics

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Adyen
- API surface: Adyen webhooks
- Fields/concepts: `eventCode`, `pspReference`, `eventDate`,
  `sequenceNumber`, acknowledgement-before-processing

## Drift Category

Duplicate webhook and latest-event reconciliation semantics.

## Checked Situation

Adyen's official webhook handling guide says endpoints should store the webhook
message, acknowledge it with a successful HTTP response, and only then apply
business logic. If Adyen does not receive a response within 10 seconds, the
message is marked failing and moved into retry handling. The guide also says
webhook payloads include timestamps, and some contain sequence numbers for
ordering.

Most importantly for silent drift, Adyen documents duplicate webhook events:
the duplicates can share the same `eventCode` and `pspReference` while
`eventDate` and other fields differ. The recommended handling is to use the
details from the latest webhook event. A client that deduplicates only on
`pspReference`, or treats the first event as final, can keep acknowledging
webhooks while preserving stale payment state.

## Why Offline Reproduction Is Not Possible

The proof requires a live Adyen merchant account, webhook configuration,
payment lifecycle events, and Adyen's retry/delivery behavior. A local replay
can model duplicate messages, but not the hosted production semantics.

## Evidence URLs

- https://docs.adyen.com/development-resources/webhooks/handle-webhook-events
