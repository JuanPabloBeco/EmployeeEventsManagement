import os
import requests
from django.core.cache import cache
import json


def get_holiday(date, country="US", only_national=True):
    date_str = date.strftime("%m/%d/%Y")
    holiday = cache.get(f'holiday_{date_str}')
    
    if holiday:
        holiday_json = json.loads(holiday)
    else: 
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
            holiday_json = res.json()
        else: 
            return res.json()

    if only_national: holiday_json = filter_only_national(holiday_json)
    return {"holidays": holiday_json}
    
def filter_only_national(holidays):
    for holiday in holidays:
        if holiday.get(type) != "National":
            holidays.remove(holiday)
    return holidays
