from __future__ import annotations

import json
import holidays

country = 'PK'
date = '2023-04-21'
calendar = holidays.country_holidays(country, years=[2023])
print(json.dumps({'country': country, 'date': date, 'holiday': calendar.get(date)}, sort_keys=True))
