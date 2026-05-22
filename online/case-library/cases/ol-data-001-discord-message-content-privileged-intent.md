# OL-DATA-001: Discord message content privileged intent empties fields

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: Discord
- API surface: Gateway message events and Message Resource API payloads
- Fields/concepts: `MESSAGE_CONTENT`, `content`, `embeds`, `attachments`,
  `components`, `poll`, verified apps

## Drift Category

Message-content visibility and privileged-intent data gating.

## Checked Situation

Discord's Message Resource docs say apps without the `MESSAGE_CONTENT`
privileged intent receive empty values in message content fields, including
`content`, `embeds`, `attachments`, and `components`; `poll` can be omitted.
Discord's privileged-intent docs also say message content access is not tied to
a separate event type but gates content data across APIs.

The same bot token, channel subscription, and message-event code can keep
receiving `MESSAGE_CREATE` or message API payloads with exit-free delivery, but
the fields application logic depends on become empty or omitted unless the app
has the approved privileged intent.

## Why Offline Reproduction Is Not Possible

The proof requires a live Discord application, app verification state, Developer
Portal intent settings, guild membership, live message payloads, and Discord's
hosted Gateway/API authorization checks. Local fixtures can simulate empty
fields but cannot prove Discord's production gating behavior.

## Evidence URLs

- https://docs.discord.com/developers/resources/message
- https://support-dev.discord.com/hc/en-us/articles/6207308062871-What-are-Privileged-Intents
