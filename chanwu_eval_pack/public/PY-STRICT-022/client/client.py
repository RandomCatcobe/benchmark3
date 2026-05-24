from __future__ import annotations

import json

from marshmallow import Schema, fields

class ProbeSchema(Schema):
    dump = fields.String()

schema = ProbeSchema()
print(json.dumps({"dump_callable": callable(schema.dump), "fields": sorted(schema.fields)}, sort_keys=True))
