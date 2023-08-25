from rest_framework import serializers
from datetime import datetime, timedelta
from core.models import Event, Employee
from api_v1.utils.get_events_in_range import get_events_in_range


class EventSerializer(serializers.ModelSerializer):
    #employee = serializers.PrimaryKeyRelatedField(many=True, queryset=Employee.objects.all())

    class Meta:
        model = Event
        fields = [
            "id",
            "date",
            "type",
            "employee",
        ]


class FollowingEventsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    date_range = serializers.IntegerField()

    def get_following_events(self):
        following_events = get_events_in_range(self.validated_data["start_date"], self.validated_data["date_range"])
        return following_events
