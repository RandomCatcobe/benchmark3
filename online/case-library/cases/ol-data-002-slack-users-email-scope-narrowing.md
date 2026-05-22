# OL-DATA-002: Slack user email scope narrowing

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Slack
- API surface: Web API `users.info`, `users.list`, user objects
- Fields/concepts: `email`, `users:read`, `users:read.email`, bot tokens,
  grandfathered OAuth grants

## Drift Category

OAuth scope narrowing and user-profile field visibility drift.

## Checked Situation

Slack's changelog says apps must request `users:read.email` to access the
`email` field in user objects returned by `users.info` and `users.list`;
`users:read` alone is no longer sufficient. It also says older grandfathered
apps and bot-token behavior would lose email access.

The same method call can continue to return a valid user object while the
`email` field disappears for tokens that previously relied on broad or
grandfathered access. Integrations that key CRM/user provisioning by email can
silently stop matching people even though the API response itself is not a
global failure.

## Why Offline Reproduction Is Not Possible

The proof requires a real Slack workspace, OAuth grant history, token type,
app creation date, workspace users, and Slack's live field-authorization logic.
Local fixtures cannot recreate grandfathering or production OAuth enforcement.

## Evidence URLs

- https://docs.slack.dev/changelog/2017-04-narrowing-email-access/
