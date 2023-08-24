from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from api_v1.serializers.employee_serializer import EmployeeSerializer


class EmployeeView(viewsets.ViewSet):
    @action(methods=['post'], detail=False, url_path='')
    def create_employee(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee = serializer.save()

        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)