from django.core.mail import send_mail
from django.conf import settings

send_mail(
    "Subject here",
    "Here is the message.",
    settings.DJANGO_EMAIL_HOST,
    ["jpbecona@gmail.com"],
    fail_silently=False,
)
