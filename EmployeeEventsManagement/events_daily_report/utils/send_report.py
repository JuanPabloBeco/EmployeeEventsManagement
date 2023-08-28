from django.conf import settings
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.utils.get_events_in_range import get_events_in_range
from events_daily_report.serializer import EventSerializer

def send_report():
    now = datetime.now()
    now_in_str = now.strftime("%m/%d/%Y")

    content = get_events_in_range(now, 0)

    event_serializer = EventSerializer(content, many=True)

    html_content = render_to_string(
        "daily_report_template.html",
        {"title": f"Daily event report for {now_in_str}", "content": event_serializer.data},
    )
    text_content = strip_tags(html_content)

    host_email = getattr(settings, "EMAIL_HOST_USER", None)
    subscription_list = getattr(settings, "EMAIL_DAILY_REPORT_SUBSCRIBERS", None)

    email = EmailMultiAlternatives(
        "Events Daily report",
        text_content,
        host_email,
        subscription_list,
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

