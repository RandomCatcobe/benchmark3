from __future__ import annotations

import json
import holidays

country = 'TH'
date = '2023-07-31'
calendar = holidays.country_holidays(country, years=[2023])
print(json.dumps({'country': country, 'date': date, 'holiday': calendar.get(date)}, sort_keys=True))
