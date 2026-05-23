from __future__ import annotations

import json
import holidays

country = 'AE'
date = '2020-07-30'
calendar = holidays.country_holidays(country, years=[2020])
print(json.dumps({'country': country, 'date': date, 'holiday': calendar.get(date)}, sort_keys=True))
