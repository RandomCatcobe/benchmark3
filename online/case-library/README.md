# Online Case Library

Standalone case library for online-only platform/API drift.

These records are deliberately not benchmark packages. They preserve checked
evidence, business impact, and the reason the case cannot be reproduced in the
repository's offline pipeline.

## Index

Current online-only records: 23.

| Case ID | Status | Decision | Case file |
|---|---|---|---|
| OL-ECOM-001 | accepted | `accept_online_case` | `cases/ol-ecom-001-jd-union-dynamic-itemid.md` |
| OL-ECOM-002 | boundary | `boundary_needs_source` | `cases/ol-ecom-002-jd-order-time-window.md` |
| OL-ECOM-003 | boundary | `boundary_needs_source` | `cases/ol-ecom-003-taobao-sold-get-window.md` |
| OL-ECOM-004 | boundary | `operational_constraint` | `cases/ol-ecom-004-taobao-callback-timeout.md` |
| OL-ECOM-005 | rejected-core | `reject_client_mapping_only` | `cases/ol-ecom-005-taobao-trade-closed-mapping.md` |
| OL-ECOM-006 | boundary | `boundary_needs_source` | `cases/ol-ecom-006-taobao-order-id-format.md` |
| OL-ECOM-007 | accepted | `accept_online_case` | `cases/ol-ecom-007-amazon-spapi-orderitemid-mismatch.md` |
| OL-ECOM-008 | accepted | `accept_online_case` | `cases/ol-ecom-008-shopify-api-version-fall-forward.md` |
| OL-ECOM-009 | accepted | `accept_online_case` | `cases/ol-ecom-009-ebay-feed-completed-with-error-result-file.md` |
| OL-ECOM-010 | accepted | `accept_online_case` | `cases/ol-ecom-010-stripe-webhook-versioned-duplicate-events.md` |
| OL-ECOM-011 | accepted | `accept_online_case` | `cases/ol-ecom-011-square-webhook-duplicate-out-of-order-delivery.md` |
| OL-ECOM-012 | accepted | `accept_online_case` | `cases/ol-ecom-012-adyen-webhook-duplicate-latest-event.md` |
| OL-ECOM-013 | accepted | `accept_online_case` | `cases/ol-ecom-013-razorpay-at-least-once-webhook-timeout.md` |
| OL-ECOM-014 | accepted | `accept_online_case` | `cases/ol-ecom-014-mollie-payment-status-webhook-fetch-required.md` |
| OL-ECOM-015 | accepted | `accept_online_case` | `cases/ol-ecom-015-klarna-non-guaranteed-payment-status-order.md` |
| OL-ECOM-016 | accepted | `accept_online_case` | `cases/ol-ecom-016-google-ads-conversion-adjustment-partial-failure.md` |
| OL-ECOM-017 | accepted | `accept_online_case` | `cases/ol-ecom-017-tiktok-events-api-dedup-event-id-window.md` |
| OL-ECOM-018 | accepted | `accept_online_case` | `cases/ol-ecom-018-hubspot-webhook-retry-and-association-double-events.md` |
| OL-ECOM-019 | accepted | `accept_online_case` | `cases/ol-ecom-019-twilio-event-streams-duplicate-out-of-order.md` |
| OL-ECOM-020 | accepted | `accept_online_case` | `cases/ol-ecom-020-mailchimp-batch-operation-async-errors.md` |
| OL-ECOM-021 | accepted | `accept_online_case` | `cases/ol-ecom-021-mailgun-webhook-retry-and-scope-dedup.md` |
| OL-ECOM-022 | accepted | `accept_online_case` | `cases/ol-ecom-022-postmark-inbound-webhook-retry-exhaustion.md` |
| OL-AI-001 | accepted | `accept_online_case` | `cases/ol-ai-001-google-api-keys-retroactive-gemini-credential.md` |

Machine-readable ledger: `cases.jsonl`.

## Shared Marker

Every record in this library has:

```yaml
offline_reproduction: not_possible
idea_bank_route: forbidden
offline_case_bank_route: forbidden
```
