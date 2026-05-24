from __future__ import annotations

import json

import emoji

value = "\U0001FAE9"
print(json.dumps({
    "is_emoji": emoji.is_emoji(value),
    "emoji_count": emoji.emoji_count(value),
    "demojize": emoji.demojize(value),
}, sort_keys=True))
