# OL-ECOM-001: JD Union Dynamic Item ID

Status: boundary

Decision: `boundary_needs_source`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: JD Union / JD Open Platform
- API surface: `jd.union.open.goods.*`, `jd.union.open.goods.itemid.get`
- Fields/concepts: `itemId`, JD main-site SKU ID, scene ID

## Drift Category

ID format and ID semantics drift.

## Checked Situation

JD Union item IDs were reported as moving from static numeric IDs to dynamic
strings with an A/B segment structure. The 2024-03 notice mirrors say JD Union
APIs began supporting both main-site SKU IDs and Union item IDs from
2024-03-06, and later rollout steps restricted some media accounts to the new
full item ID. The 2024-08 notice mirror says all media open-platform APIs would
support only complete Union item ID input/output from 2024-09-30.

Under the strict audit posture, this remains a boundary case rather than an
accepted online case. The current evidence trail is composed of notice mirrors
and secondary articles; no primary JD official document or live proof was
confirmed in this pass. The plausible risk remains that old clients storing IDs
as integers, deduplicating on the full value, or joining records on static item
IDs can continue running while producing duplicate products or failed
associations, but the source chain is not strong enough to carry accepted
status.

## Why Offline Reproduction Is Not Possible

The observed behavior depends on JD Union account type, live API permissions,
scene ID policy, and vendor rollout timing. A local fixture could demonstrate
the failure shape, but it would not reproduce the service drift.

## Evidence URLs

- https://cloud.tencent.com/developer/article/2566489
- https://www.taokeshow.com/55048.html
- https://www.taokeshow.com/60150.html
- https://www.dingdanxia.com/article/231.html

## Next Source Task

Find the primary JD Union announcement or official open-platform API
documentation confirming the rollout dates, accepted input/output ID forms, and
account-scope behavior.
