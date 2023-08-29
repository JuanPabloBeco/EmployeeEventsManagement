from rest_framework import serializers
from core.models import Event, Employee
from core.utils.get_events_in_range import get_events_in_range


    
class EmployeeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    employee = EmployeeModelSerializer(read_only=True)

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
    date_range = serializers.IntegerField(max_value=100, min_value=0)

    def get_following_events(self):
        following_events = get_events_in_range(self.validated_data["start_date"], self.validated_data["date_range"])
        return following_events