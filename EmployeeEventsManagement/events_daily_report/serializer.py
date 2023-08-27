from rest_framework import serializers
from datetime import date
from core.models import Event
from core.utils.get_events_in_range import get_events_in_range


class EventSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    years_ago = serializers.SerializerMethodField()
    date = serializers.DateField(format='%m/%d/%Y')


    def get_type(self, obj):
        return obj.get_type_display() 

    def get_employee(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"

    def get_years_ago(self, obj):
        now = date.today()
        years_ago = now.year - obj.date.year
        return f"{years_ago}"

    class Meta:
        model = Event
        fields = [
            "date",
            "type",
            "years_ago",
            "employee",
        ]
