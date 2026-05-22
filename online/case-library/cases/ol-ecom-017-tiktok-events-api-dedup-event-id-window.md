# OL-ECOM-017: TikTok Events API Dedup Event ID Window

Status: accepted

Decision: `accept_online_case`

Offline reproduction: `not_possible`

Idea-bank route: forbidden

## Platform And Surface

- Platform: TikTok Ads Manager / Events API
- API surface: TikTok Pixel and Events API event deduplication
- Fields/concepts: `event_id`, event name, Pixel, Events API, 48-hour window

## Drift Category

Cross-channel conversion deduplication semantics.

## Checked Situation

TikTok's event deduplication guide says deduplication is required when both the
Pixel and Events API share duplicate copies of the same conversion. It says the
same Event ID must be shared through both channels for deduplication to occur,
and it describes duplicate matching windows for Pixel, Events API, and
Pixel-plus-Events-API overlap.

The silent integration risk is that both browser and server channels keep
returning accepted events, but mismatched or missing `event_id` causes one
purchase to be counted twice, or a delayed server event to be merged against
the wrong first event. Ad reporting and optimization drift while the transport
requests succeed.

## Why Offline Reproduction Is Not Possible

The proof requires a TikTok Ads account, a pixel, Events API credentials,
production event ingestion, and TikTok's hosted deduplication window. A local
mock cannot prove attribution-side counting behavior.

## Evidence URLs

- https://ads.tiktok.com/help/article/event-deduplication?redirected=1
