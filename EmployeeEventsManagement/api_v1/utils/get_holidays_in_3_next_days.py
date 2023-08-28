from datetime import date, timedelta
from api_v1.api.get_holidays import get_holiday


def get_holidays_in_3_next_days(date=date.today(), country="US"):
    are_holidays = {}

    today = date
    today_str = today.strftime("%m/%d/%Y")
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%m/%d/%Y")
    day_after_tomorrow = tomorrow + timedelta(days=1)
    day_after_tomorrow_str = day_after_tomorrow.strftime("%m/%d/%Y")

    is_holiday_today = get_holiday(today)
    if not is_holiday_today.get("error"):
        are_holidays[today_str] = is_holiday_today
    else:
        return is_holiday_today

    is_holiday_tomorrow = get_holiday(tomorrow)
    if not is_holiday_tomorrow.get("error"):
        are_holidays[tomorrow_str] = is_holiday_tomorrow
    else:
        return is_holiday_tomorrow


    is_holiday_day_after_tomorrow = get_holiday(day_after_tomorrow)
    if not is_holiday_day_after_tomorrow.get("error"):
        are_holidays[day_after_tomorrow_str] = is_holiday_day_after_tomorrow
    else:
        return is_holiday_day_after_tomorrow

    return are_holidays
