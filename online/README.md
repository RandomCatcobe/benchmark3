# Online Service Drift Pipeline

This folder is the live-service counterpart to the local/offline reproduction
pipeline in the repository.

It is for platform APIs whose behavior depends on live vendor systems,
credentials, account policy, historical orders, or hosted callbacks. These
cases are useful evidence for silent behavioral drift, but they are not
eligible for the offline benchmark case bank.

## Hard Boundary

- Do not route these cases to any idea bank.
- Do not route these cases to `docs/case-bank/`.
- Do not package these cases as offline evaluation tasks.
- Keep even fully silent live-service drift in this folder.
- Mark every case with `offline_reproduction: not_possible`.

## Lifecycle

```text
raw_online_lead
  -> source_checked
  -> online_triaged
  -> online_case_recorded
  -> blocked_offline_reproduction
```

## Artifacts

- `pipeline.md`: the online-specific pipeline contract.
- `ecommerce-api-line-triage-20260521.md`: the checked ledger for the current
  e-commerce/API batch.
- `ecommerce-api-line-triage-20260522.md`: continuation run for non-duplicate
  Shopify, eBay, Stripe, Square, and Adyen online-only cases.
- `case-library/`: standalone case library for online-only cases.

## Runs

### `ONLINE-20260521-001`

Scope: seven e-commerce platform/API drift leads covering JD Union, JD order
sync, Taobao order sync/callback/status/ID behavior, and Amazon SP-API.

Result: two accepted online-only cases, four boundary cases needing stronger
source or live proof, and one rejected-as-core-drift client mapping risk.

### `ONLINE-20260522-001`

Scope: non-duplicate online-only cases outside the previous JD/Taobao/Amazon
SP-API set, covering Shopify API version fall-forward, eBay Feed partial
success, and Stripe/Square/Adyen webhook delivery semantics.

Result: five accepted online-only records, all kept in `online/case-library/`
and marked `offline_reproduction: not_possible`.
