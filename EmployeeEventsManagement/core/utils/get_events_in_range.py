from core.models import Event
from django.db.models import Q
import datetime

def get_events_in_range(start_date, date_range):
    filters = Q()

    temp_date = start_date 
    for x in range(date_range+1):
        filters |= Q(date__month=temp_date.month) & Q(date__day=temp_date.day)
        temp_date += datetime.timedelta(days=1)
    
    following_events = Event.objects.filter(filters).order_by("date")
    return following_events
