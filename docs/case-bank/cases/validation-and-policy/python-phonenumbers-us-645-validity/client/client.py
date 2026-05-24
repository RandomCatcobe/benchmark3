from __future__ import annotations

import json

import phonenumbers

number = phonenumbers.parse("+16455550123", "US")
print(json.dumps({
    "valid": phonenumbers.is_valid_number(number),
    "region": phonenumbers.region_code_for_number(number),
    "type": phonenumbers.number_type(number),
}, sort_keys=True))
