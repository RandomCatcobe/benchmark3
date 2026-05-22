# OL-ECOM-018: HubSpot Webhook Retry And Association Double Events

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: HubSpot
- API surface: Webhooks API
- Fields/concepts: webhook subscriptions, throttling, retry, timeout,
  `associationChange`

## Drift Category

Webhook batching, retry, and association-event cardinality semantics.

## Checked Situation

HubSpot's webhook guide says subscriptions apply to all customers who installed
the integration. It also states that all `associationChange` webhook
subscriptions fire two events for both sides of an association. For delivery
failures, HubSpot retries failed notifications up to 10 times when it cannot
connect, when the service takes longer than five seconds, or when the service
responds with 4xx/5xx.

The silent integration risk is an integration that assumes one association
change equals one event, or that a slow but eventually successful handler means
HubSpot will not retry. The same CRM association can produce two valid events,
and retries can replay a batch, causing duplicate local links or repeated ERP
sync work while HTTP delivery continues to look valid.

## Why Offline Reproduction Is Not Possible

The proof requires a HubSpot app, installed customer accounts, real CRM object
associations, HubSpot webhook throttling, and hosted retry behavior. A local
mock can test idempotency but not the production subscription semantics.

## Evidence URLs

- https://developers.hubspot.com/docs/api-reference/latest/webhooks/guide
