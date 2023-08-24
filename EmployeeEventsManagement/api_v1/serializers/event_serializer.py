from core.models import Event
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 
            'date',
            'type',
            'employee__first_name',
            'employee__last_name',
            ]
