# OL-ECOM-020: Mailchimp Batch Operation Async Errors

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Mailchimp Marketing API
- API surface: batch operations and batch webhooks
- Fields/concepts: `/batches`, `status`, `finished_operations`,
  `errored_operations`, `response_body_url`

## Drift Category

Async batch completion and per-operation error visibility.

## Checked Situation

Mailchimp's Marketing API exposes batch operations for running many operations
with a single call. The API has endpoints to start a batch, get batch status,
and configure batch webhooks that fire when a batch completes processing. Batch
summary fields include counts such as finished and errored operations, plus a
response body URL.

The silent integration risk is a marketing or commerce sync job that treats
the accepted batch request or terminal batch status as full success. Some
member updates, ecommerce-store mutations, or campaign operations can fail
inside the batch while the batch itself completes and only the status summary or
response body reveals the row-level errors.

## Why Offline Reproduction Is Not Possible

The proof requires a Mailchimp account, live audience or ecommerce data, batch
operation processing, and Mailchimp-hosted completion webhooks/result files. A
local fixture can model partial errors but cannot prove Mailchimp's live batch
outcome.

## Evidence URLs

- https://mailchimp.com/developer/marketing/api/batch-operations/list-batch-requests/
