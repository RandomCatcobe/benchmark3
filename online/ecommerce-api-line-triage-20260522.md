# E-Commerce API Online Line Triage - 2026-05-22

Run ID: `ONLINE-20260522-001`

This pass continues the online-only line without reusing the 2026-05-21 JD,
Taobao, and Amazon SP-API records. The output stays under
`online/case-library/`; nothing is routed into an idea bank or the offline
case-bank.

## De-Duplication Check

Before recording new cases, this pass checked the existing online library and
repo text for these already-covered surfaces:

- JD Union dynamic `itemId`
- JD order query window
- Taobao `taobao.trades.sold.get`
- Taobao callback timeout / retry
- Taobao `TRADE_CLOSED`
- Taobao `tid` / order ID format
- Amazon SP-API `OrderItemId` Orders-vs-Finances mismatch
- Existing offline package-style online leads for BigCommerce, Mercado Libre,
  Etsy, Google Merchant, Amazon feed status, and Taobao masked/OAID/logistics
  semantics

This run therefore records different platforms or different API surfaces:
Shopify, eBay Feed, Stripe, Square, and Adyen.

## Output Summary

| Bucket | Count | Entries |
|---|---:|---|
| Accepted online-only cases | 3 | OL-ECOM-008, OL-ECOM-010, OL-ECOM-012 |
| Boundary / needs stronger source | 2 | OL-ECOM-009, OL-ECOM-011 |
| Rejected as duplicate | 0 | - |

## Primary Online Case Queue

| Case ID | Candidate | Route | Why it stays online-only |
|---|---|---|---|
| OL-ECOM-008 | Shopify unsupported API/webhook versions fall forward to supported versions while calls and deliveries still succeed | `online/case-library/cases/ol-ecom-008-shopify-api-version-fall-forward.md` | Requires Shopify's live version retirement schedule, app config, and production response/webhook headers. |
| OL-ECOM-010 | Stripe webhook events are versioned per destination and may arrive duplicate or out of order | `online/case-library/cases/ol-ecom-010-stripe-webhook-versioned-duplicate-events.md` | Requires Stripe account configuration, live event destinations, and hosted retry/delivery behavior. |
| OL-ECOM-012 | Adyen duplicate webhooks can share `eventCode` and `pspReference` while later fields differ | `online/case-library/cases/ol-ecom-012-adyen-webhook-duplicate-latest-event.md` | Requires Adyen merchant configuration and live payment lifecycle events. |

## Boundary Source Queue

| Case ID | Candidate | Route | Why it is downgraded |
|---|---|---|---|
| OL-ECOM-009 | eBay Sell Feed tasks can finish as `COMPLETED_WITH_ERROR`, requiring result-file parsing for per-record failures | `online/case-library/cases/ol-ecom-009-ebay-feed-completed-with-error-result-file.md` | Current eBay source URLs resolve as unavailable in link checks; needs refreshed official docs or live proof. |
| OL-ECOM-011 | Square webhooks can duplicate, arrive out of order, retry for up to 24 hours, and then be discarded | `online/case-library/cases/ol-ecom-011-square-webhook-duplicate-out-of-order-delivery.md` | Current Square webhook URL resolves as unavailable in link checks; needs refreshed official docs or live proof. |

## Line Ledger

| ID | Platform/API | Decision | Evidence strength | Offline reproduction | Note |
|---|---|---|---|---|---|
| OL-ECOM-008 | Shopify Admin APIs / webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs confirm API and webhook fall-forward when selected versions are unsupported and expose effective-version headers. |
| OL-ECOM-009 | eBay Sell Feed API | `boundary_needs_source` | medium-low | `not_possible` | The claim shape is plausible, but strict audit requires refreshed official eBay links or live result-file evidence before accepted status. |
| OL-ECOM-010 | Stripe webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs confirm destination-versioned event payloads, duplicate deliveries, unordered delivery, and retry behavior. |
| OL-ECOM-011 | Square webhooks | `boundary_needs_source` | medium-low | `not_possible` | The claim shape is plausible, but strict audit requires refreshed official Square links or live webhook evidence before accepted status. |
| OL-ECOM-012 | Adyen webhooks | `accept_online_case` | high primary-source evidence | `not_possible` | Official docs confirm duplicate webhook events with the same core identity but potentially different dates/fields. |

## Checked Sources

- Shopify API versioning: https://shopify.dev/docs/api/usage/versioning
- Shopify REST Admin/webhook versioning: https://shopify.dev/docs/api/admin-rest/usage/versioning
- Shopify webhook subscription versioning: https://shopify.dev/docs/apps/build/webhooks/subscribe#versioning
- eBay Seller Hub Feed flow: https://developer.ebay.com/api-docs/sell/static/feed/fx-feeds-overview.html
- eBay order feeds: https://developer.ebay.com/api-docs/sell/static/orders/generating-and-retrieving-order-reports.html
- eBay `FeedStatusEnum`: https://edp.ebay.com/api-docs/sell/feed/types/api%3AFeedStatusEnum
- Stripe webhooks: https://docs.stripe.com/webhooks
- Stripe Events API: https://docs.stripe.com/api/events
- Square webhooks: https://developer.squareup.com/docs/webhooks/overview
- Adyen webhook handling: https://docs.adyen.com/development-resources/webhooks/handle-webhook-events

## Notes

- These are deliberately not offline benchmark packages.
- All retained records set `offline_reproduction: not_possible`,
  `idea_bank_route: forbidden`, and `offline_case_bank_route: forbidden`.
- Accepted cases remain online service-contract drift or online silent
  failure-shape records. Boundary cases need refreshed official sources before
  they should be counted as accepted.
