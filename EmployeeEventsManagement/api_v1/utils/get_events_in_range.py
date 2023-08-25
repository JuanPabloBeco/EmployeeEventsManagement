from core.models import Event
from django.db.models import Q
import datetime

def get_events_in_range(start_date, date_range):
    end_date = start_date + datetime.timedelta(days=date_range)
    filters = Q(date__gte=start_date) & Q(date__lte=end_date)
    following_events = Event.objects.filter(filters)
    return following_events
