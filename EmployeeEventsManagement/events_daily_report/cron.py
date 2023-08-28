import datetime
from events_daily_report.utils.send_report import send_report


def events_daily_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Script executed at {timestamp}\n"
    send_report()
