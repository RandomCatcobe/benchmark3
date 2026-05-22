# OL-ECOM-016: Google Ads Conversion Adjustment Partial Failure

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Google Ads API
- API surface: `ConversionAdjustmentUploadService`
- Fields/concepts: `order_id`, `partial_failure`, `partial_failure_error`,
  conversion action

## Drift Category

Partial-success attribution adjustment semantics.

## Checked Situation

Google Ads API docs say conversion adjustments are uploaded after conversions
have already been reported. For `WEBPAGE` conversions, or when the original
conversion had an order ID, the adjustment must use `order_id`; the docs also
say `partial_failure` should always be set to `true` for adjustment uploads.
Examples show successful API responses still carrying partial failure details.

The silent integration risk is that an ads/ERP integration treats the upload
RPC as globally successful and ignores partial failures. Some adjustments can
apply while others fail because the original conversion was missing, discarded,
or identified by the wrong key. ROAS, refund, or cancellation reporting then
drifts while the API call itself completes.

## Why Offline Reproduction Is Not Possible

The proof requires a Google Ads account, real conversion actions, previously
recorded conversions, customer IDs, and Google Ads attribution state. Local
fixtures cannot prove which conversions exist or how Google accepts partial
adjustments in production.

## Evidence URLs

- https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments
