# OL-DATA-003: Atlassian Jira user privacy fields

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Atlassian Jira Cloud
- API surface: Jira Cloud REST APIs returning User objects
- Fields/concepts: `username`, `userKey`, `accountId`, `emailAddress`,
  profile visibility, GDPR migration

## Drift Category

Identity-field replacement and privacy-controlled user-object visibility.

## Checked Situation

Atlassian's Jira Cloud privacy migration guide says `username` and `userKey`
are removed from REST APIs and users are identified by `accountId` instead. It
also says other personal data such as email is restricted by profile privacy
settings, so fields such as `emailAddress` can be `null`.

The same integration code can keep querying issues, components, users, or JQL
results successfully while user identity fields vanish or email fields become
privacy-dependent. Downstream joins, sync mappings, or notification routing can
then drift from user-name/email identifiers to missing/null data without a hard
transport failure.

## Why Offline Reproduction Is Not Possible

The proof requires a Jira Cloud tenant, users with real Atlassian account IDs,
site/app permissions, profile visibility settings, and Atlassian's live REST
API behavior. Local fixtures cannot prove hosted privacy and tenant policy
state.

## Evidence URLs

- https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/
