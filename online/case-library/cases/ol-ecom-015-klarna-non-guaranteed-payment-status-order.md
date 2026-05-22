# OL-ECOM-015: Klarna Non-Guaranteed Payment Status Order

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Klarna
- API surface: Non Guaranteed Payments and payment-status notifications
- Fields/concepts: `non_guaranteed_payment.updated`, `UNPAID`, `PAID`,
  `CLOSED`

## Drift Category

Non-final payment state and notification ordering semantics.

## Checked Situation

Klarna's non-guaranteed payment guide shows orders moving through payment status
notifications such as `UNPAID`, `PAID`, and `CLOSED`. The guide states that
`CLOSED` means Klarna will no longer process payments for the order and that
late money will be refunded. It also notes that `PAID` can be received before
`UNPAID`, and that `PAID` or `CLOSED` should be treated as definitive statuses
rather than relying on the order in which statuses are generally received.

The silent integration risk is that a merchant captures or ships after an early
status or assumes notification order. The integration keeps receiving valid
webhooks, but local fulfillment can move ahead of final settlement, or a later
definitive `CLOSED` status can invalidate the earlier local state.

## Why Offline Reproduction Is Not Possible

The proof requires a live Klarna payment flow, merchant eligibility, payment
method timing, and Klarna-hosted notifications. A local fixture can model the
state machine but not the live non-guaranteed settlement behavior.

## Evidence URLs

- https://docs.klarna.com/acquirer/klarna/web-payments/additional-resources/use-cases/non-guaranteed/
