import datetime
from django.core.mail import send_mail

def my_cron_test_job():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Script executed at {timestamp}\n"

    send_mail(
        "Subject here",
        message,
        "jpbecona@outlook.com",
        ["jpbecona@gmail.com"],
        fail_silently=False,
    )