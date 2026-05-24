from __future__ import annotations

import json

import unicodedata
from email_validator import validate_email

result = validate_email('"Cafe\u0301" <me@example.com>', allow_display_name=True, check_deliverability=False)
name = result.display_name
print(json.dumps({"display_name": name, "is_nfc": unicodedata.is_normalized("NFC", name)}, sort_keys=True))
