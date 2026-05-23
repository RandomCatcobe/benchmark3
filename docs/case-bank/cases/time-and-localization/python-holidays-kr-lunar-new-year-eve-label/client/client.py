from __future__ import annotations

import json
import holidays

country = 'KR'
date = '2020-01-24'
calendar = holidays.country_holidays(country, years=[2020])
print(json.dumps({'country': country, 'date': date, 'holiday': calendar.get(date)}, sort_keys=True))
