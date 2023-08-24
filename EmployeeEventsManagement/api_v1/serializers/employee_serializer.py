from core.models import Employee
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 
            'first_name',
            'last_name',
            'email',
            'is_active',
            ]

class EmployeeFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_is_active(self, value):
        if value not in [True, False, None]:
            raise serializers.ValidationError("Invalid value for is_active parameter")
        return value