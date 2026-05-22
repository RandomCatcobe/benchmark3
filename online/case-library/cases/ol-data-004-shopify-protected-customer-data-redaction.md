# OL-DATA-004: Shopify protected customer data redaction

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Shopify
- API surface: Admin API and Customer Account API protected customer resources
- Fields/concepts: protected customer data, name, address, email, phone,
  Partner Dashboard access requests, redacted fields, GraphQL errors

## Drift Category

Protected customer-data field approval and redaction semantics.

## Checked Situation

Shopify's protected customer data docs say public apps must request access to
protected customer data and individually protected fields such as name, address,
email, and phone. The docs say API responses include only approved fields,
unapproved fields are redacted, and GraphQL requests to unapproved types can
return HTTP `200 OK` with an error message in the `errors` hash.

The same app token and API query can therefore keep receiving successful HTTP
responses while customer/order fields become redacted or represented only by
GraphQL errors. Integrations that treat HTTP 200 as "customer data present" can
silently sync incomplete customer, order, shipping, or fulfillment data.

## Why Offline Reproduction Is Not Possible

The proof requires a Shopify partner app, distribution type, merchant install,
Partner Dashboard review/approval state, store plan or app type, API scopes,
and real customer/order data. Local fixtures cannot recreate Shopify's hosted
review gate or field redaction decisions.

## Evidence URLs

- https://shopify.dev/docs/apps/launch/protected-customer-data
