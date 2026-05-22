# E-Commerce API Online Line Triage - 2026-05-22 Continued

Run ID: `ONLINE-20260522-002`

This pass adds ten more online-only silent-drift/service-semantics records. It
continues from `ONLINE-20260522-001` and avoids the existing JD, Taobao, Amazon
SP-API, Shopify, eBay, Stripe, Square, and Adyen records.

The output remains only under `online/case-library/`. Nothing in this pass is
routed into an idea bank, `docs/case-bank/`, or offline benchmark packaging.

## De-Duplication Check

Already-covered online records before this run:

- OL-ECOM-001 through OL-ECOM-007: JD, Taobao, Amazon SP-API.
- OL-ECOM-008 through OL-ECOM-012: Shopify, eBay Feed, Stripe, Square, Adyen.

Already-present offline/source-check shapes also avoided:

- Walmart processed feed partial success.
- Adobe Commerce async bulk acceptance.
- Amazon feed status hides per-record business failures.
- BigCommerce, Mercado Libre, Etsy, Google Merchant, Taobao OAID/logistics, and
  other online-style records already represented in the offline case-bank as
  blocked/source-check packages.

This run therefore records different platforms or distinct API surfaces:
Razorpay, Mollie, Klarna, Google Ads, TikTok, HubSpot, Twilio, Mailchimp,
Mailgun, and Postmark.

## Output Summary

| Bucket | Count | Entries |
|---|---:|---|
| Accepted online-only cases | 10 | OL-ECOM-013 through OL-ECOM-022 |
| Boundary / needs stronger source | 0 | - |
| Rejected as duplicate | 0 | - |

## Primary Online Case Queue

| Case ID | Candidate | Route | Why it stays online-only |
|---|---|---|---|
| OL-ECOM-013 | Razorpay can resend the same webhook when the endpoint fails or times out after processing | `online/case-library/cases/ol-ecom-013-razorpay-at-least-once-webhook-timeout.md` | Requires live Razorpay merchant configuration, payment events, and hosted retry timing. |
| OL-ECOM-014 | Mollie payment status must be fetched after webhook instead of predicted locally | `online/case-library/cases/ol-ecom-014-mollie-payment-status-webhook-fetch-required.md` | Requires Mollie-hosted checkout, payment method lifecycle, and status webhooks. |
| OL-ECOM-015 | Klarna non-guaranteed payment notifications can arrive in non-intuitive order and later close | `online/case-library/cases/ol-ecom-015-klarna-non-guaranteed-payment-status-order.md` | Requires Klarna payment flow and live non-guaranteed settlement behavior. |
| OL-ECOM-016 | Google Ads conversion adjustments can partially fail while the upload call completes | `online/case-library/cases/ol-ecom-016-google-ads-conversion-adjustment-partial-failure.md` | Requires Google Ads customer state, recorded conversions, and attribution system behavior. |
| OL-ECOM-017 | TikTok Pixel and Events API deduplication depends on event ID matching and timing windows | `online/case-library/cases/ol-ecom-017-tiktok-events-api-dedup-event-id-window.md` | Requires TikTok Ads event ingestion, Pixel, Events API credentials, and hosted attribution. |
| OL-ECOM-018 | HubSpot association-change webhooks can fire two events and retries replay failed batches | `online/case-library/cases/ol-ecom-018-hubspot-webhook-retry-and-association-double-events.md` | Requires HubSpot app installation, CRM associations, and hosted retry behavior. |
| OL-ECOM-019 | Twilio Event Streams can deliver duplicate or out-of-order events | `online/case-library/cases/ol-ecom-019-twilio-event-streams-duplicate-out-of-order.md` | Requires Twilio Event Streams sinks and live event delivery behavior. |
| OL-ECOM-020 | Mailchimp batch operations can complete with errored sub-operations | `online/case-library/cases/ol-ecom-020-mailchimp-batch-operation-async-errors.md` | Requires Mailchimp account data, batch execution, and hosted batch results. |
| OL-ECOM-021 | Mailgun webhook scope deduplication and retry policy can change observed event delivery | `online/case-library/cases/ol-ecom-021-mailgun-webhook-retry-and-scope-dedup.md` | Requires live domain/account webhook configuration and Mailgun delivery events. |
| OL-ECOM-022 | Postmark inbound webhook retry exhaustion can leave inbound messages unprocessed locally | `online/case-library/cases/ol-ecom-022-postmark-inbound-webhook-retry-exhaustion.md` | Requires Postmark inbound configuration, hosted retries, and account message state. |

## Line Ledger

| ID | Platform/API | Decision | Evidence strength | Offline reproduction | Note |
|---|---|---|---|---|---|
| OL-ECOM-013 | Razorpay webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official FAQ confirms non-2xx retry, 5-second timeout, at-least-once delivery, and `x-razorpay-event-id`. |
| OL-ECOM-014 | Mollie Payments API | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs say status changes vary by method and recommend waiting for webhook then fetching status. |
| OL-ECOM-015 | Klarna Non Guaranteed Payments | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs show `UNPAID`, `PAID`, and `CLOSED`, including note that `PAID` can arrive before `UNPAID`. |
| OL-ECOM-016 | Google Ads conversion adjustments | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs require `partial_failure=true` and order ID handling for durable adjustments. |
| OL-ECOM-017 | TikTok Pixel / Events API | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs require shared `event_id` for deduplication and define matching windows. |
| OL-ECOM-018 | HubSpot Webhooks API | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs describe association-change double events and retry conditions. |
| OL-ECOM-019 | Twilio Event Streams | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs confirm retries, out-of-order delivery, duplicates, and dedup by event `id`. |
| OL-ECOM-020 | Mailchimp batch operations | `accept_online_case` | high primary-source evidence | `not_possible` | Official API reference exposes async batch status, errored operation counts, response body URLs, and batch completion webhooks. |
| OL-ECOM-021 | Mailgun webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs describe domain/account scope deduplication and retry response-code behavior. |
| OL-ECOM-022 | Postmark inbound webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs describe 10 retries, 403 stop, Inbound Error, and missed messages after retry exhaustion. |

## Checked Sources

- Razorpay webhooks FAQ: https://razorpay.com/docs/webhooks/faqs/?preferred-country=US
- Mollie payment status: https://docs.mollie.com/docs/handling-payment-status
- Mollie accepting payments: https://docs.mollie.com/docs/accepting-payments
- Klarna non-guaranteed payments: https://docs.klarna.com/acquirer/klarna/web-payments/additional-resources/use-cases/non-guaranteed/
- Google Ads conversion adjustments: https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments
- TikTok event deduplication: https://ads.tiktok.com/help/article/event-deduplication?redirected=1
- HubSpot webhooks guide: https://developers.hubspot.com/docs/api-reference/latest/webhooks/guide
- Twilio event delivery and duplication: https://www.twilio.com/docs/events/event-delivery-and-duplication
- Mailchimp batch operations: https://mailchimp.com/developer/marketing/api/batch-operations/list-batch-requests/
- Mailgun webhooks: https://help.mailgun.com/hc/en-us/articles/202236504-Webhooks
- Postmark inbound webhook retries: https://postmarkapp.com/support/article/understanding-inbound-webhook-retries-in-postmark

## Notes

- These are online-only records, not offline benchmark packages.
- Every record sets `offline_reproduction: not_possible`,
  `idea_bank_route: forbidden`, and `offline_case_bank_route: forbidden`.
- Most cases are documented service contracts rather than hidden outages. They
  are still useful because old clients can keep receiving successful HTTP
  responses while local business state silently diverges.
