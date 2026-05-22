# OL-ECOM-014: Mollie Payment Status Requires Webhook Fetch

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Mollie
- API surface: Payments API and payment status webhooks
- Fields/concepts: `open`, `pending`, `authorized`, `expired`, `failed`,
  `paid`, payment-method-specific expiry

## Drift Category

Asynchronous payment lifecycle and status-fetch semantics.

## Checked Situation

Mollie's payment-status docs describe multiple non-final and final payment
states. Some status changes have webhooks and others do not; expiry timing also
varies by payment method. The docs warn that it is not a good idea to predict
payment expiry and that the reliable approach is to wait until the webhook is
called and fetch the status.

The silent integration risk is that a checkout or ERP integration treats the
initial payment creation, redirect return, or a temporary status as final. The
API flow continues to work, but a payment can later become `expired`, `failed`,
or `paid` on a method-specific schedule. Without fetching the authoritative
status after webhook notification, local order/payment state can diverge from
Mollie.

## Why Offline Reproduction Is Not Possible

The proof requires Mollie-hosted checkout, live payment methods, payment method
expiry rules, and webhook delivery from Mollie's platform. Local fixtures cannot
prove the hosted lifecycle timing.

## Evidence URLs

- https://docs.mollie.com/docs/handling-payment-status
- https://docs.mollie.com/docs/accepting-payments
