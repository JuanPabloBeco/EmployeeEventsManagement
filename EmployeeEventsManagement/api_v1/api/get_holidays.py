import os
import requests
from django.core.cache import cache
import json


def get_holiday(date, country="US"):
    date_str = date.strftime("%m/%d/%Y")
    holiday = cache.get(f'holiday_{date_str}')
    
    if not holiday:

        url = "https://holidays.abstractapi.com/v1/"
        params = {
            "api_key": os.environ.get("HOLIDAY_API_KEY"),
            "country": country,
            "year": date.year,
            "month": date.month,
            "day": date.day,
        }
        res = requests.get(url, params=params)

        if res.status_code == 200:
            cache.set(f'holiday_{date_str}', res.text)
        holiday = res.text
        
    holiday_json = json.loads(holiday)
    return holiday_json
