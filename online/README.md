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
- `ecommerce-api-line-triage-20260522-002.md`: second continuation run with
  ten more non-duplicate payment, ads, CRM, communication, and email platform
  records.
- `google-gemini-api-key-triage-20260522.md`: online-only security/auth scope
  record for Google API keys gaining Gemini credential semantics.
- `data-scope-auth-triage-20260522.md`: online-only data-scope and
  credential/permission drift records for Discord, Slack, Atlassian, and
  Shopify.
- `case-library/`: standalone case library for online-only cases.
- `research/`: L3+/S3+ online-only candidate ledgers that are not migrated into
  the case library or offline benchmark packages.

## Runs

### `ONLINE-20260521-001`

Scope: seven e-commerce platform/API drift leads covering JD Union, JD order
sync, Taobao order sync/callback/status/ID behavior, and Amazon SP-API.

Result: one accepted online-only case, four boundary cases needing stronger
source or live proof, one operational-constraint case, and one
rejected-as-core-drift client mapping risk.

### `ONLINE-20260522-001`

Scope: non-duplicate online-only cases outside the previous JD/Taobao/Amazon
SP-API set, covering Shopify API version fall-forward, eBay Feed partial
success, and Stripe/Square/Adyen webhook delivery semantics.

Result after strict source downgrade: three accepted online-only records and two
boundary/source-needed records, all kept in `online/case-library/` and marked
`offline_reproduction: not_possible`.

### `ONLINE-20260522-002`

Scope: ten further non-duplicate online-only cases covering Razorpay, Mollie,
Klarna, Google Ads, TikTok, HubSpot, Twilio, Mailchimp, Mailgun, and Postmark.

Result: ten accepted online-only records, all kept in `online/case-library/`
and marked `offline_reproduction: not_possible`.

### `ONLINE-20260522-003`

Scope: one non-duplicate online-only security/authentication-scope case covering
Google API keys and Gemini API access.

Result: one accepted online-only record, kept in `online/case-library/` and
marked `offline_reproduction: not_possible`.

### `ONLINE-20260522-004`

Scope: four non-duplicate online-only data-scope and credential/permission
cases covering Discord, Slack, Atlassian Jira Cloud, and Shopify.

Result: four accepted online-only records, all kept in `online/case-library/`
and marked `offline_reproduction: not_possible`.
