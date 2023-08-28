from .settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CRONJOBS = [
    ('* * * * *', 'events_daily_report.cron.events_daily_report')
]

EMAIL_DAILY_REPORT_SUBSCRIBERS = ['jpbecona@gmail.com',]