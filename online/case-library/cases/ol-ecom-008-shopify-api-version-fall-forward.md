# OL-ECOM-008: Shopify API Version Fall-Forward

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Shopify
- API surface: Admin REST, Admin GraphQL, and webhooks
- Fields/concepts: requested API version, effective API version,
  `X-Shopify-API-Version`, `X-Shopify-Api-Version`

## Drift Category

Version fall-forward and payload-contract drift.

## Checked Situation

Shopify's official versioning docs say that when an app targets an inaccessible
API version, Shopify falls forward and responds using the oldest accessible
stable version. Responses include an `X-Shopify-API-Version` header showing the
version that actually fulfilled the request. The REST Admin versioning docs add
that webhook payloads can change between API versions; when the selected
webhook API version becomes unsupported, Shopify falls forward to a supported
stable version and sends a header indicating the serializer version.

The call or webhook can therefore continue to succeed while the payload shape or
semantics move to a newer contract. Clients that pin a retired version, ignore
the effective-version header, or parse old webhook payloads can silently drop
fields, mis-handle renamed structures, or apply stale business logic without a
hard HTTP failure.

This is documented, not a hidden outage. It is still an online-only drift case
because the behavior depends on Shopify's live version retirement schedule,
app/webhook configuration, and the production API version actually selected by
Shopify at delivery time.

## Why Offline Reproduction Is Not Possible

A local mock can model a response-header mismatch, but it cannot prove Shopify's
live fall-forward behavior for a real app, store, API version, and webhook
subscription after a production version becomes unsupported.

## Evidence URLs

- https://shopify.dev/docs/api/usage/versioning
- https://shopify.dev/docs/api/admin-rest/usage/versioning
- https://shopify.dev/docs/apps/build/webhooks/subscribe#versioning
