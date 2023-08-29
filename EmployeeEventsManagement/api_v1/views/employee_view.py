from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_object_or_404
from django.db.models import Q

from api_v1.serializers.employee_serializer import EmployeeSerializer, EmployeeFilterSerializer
from api_v1.utils.validate_pk import validate_pk
from core.models import Event, Employee


class EmployeeView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)  

    @action(methods=["delete"], detail=True, url_path="")
    def delete(self, request, pk=None):
        try:
            pk = validate_pk(pk)
            employee = get_object_or_404(Employee, pk=pk)
            employee.is_active = False  # Logically delete the employee
            employee.save()

            content = {"success": True}
            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='search')
    def search_employees(self, request):
        try:
            query_params = request.query_params
            filters = Q()

            serializer = EmployeeFilterSerializer(data=query_params)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            is_active = serializer.data.get('is_active', 'true').lower()
            if is_active == 'false':
                filters &= Q(is_active=False)
            elif is_active == 'true' or is_active == '':
                filters &= Q(is_active=True)
            else:
                return Response({'error': 'Invalid value for is_active parameter'}, status=status.HTTP_400_BAD_REQUEST)

            if 'first_name' in query_params:
                filters &= Q(first_name__icontains=query_params['first_name'])
            if 'last_name' in query_params:
                filters &= Q(last_name__icontains=query_params['last_name'])
            if 'email' in query_params:
                filters &= Q(email__icontains=query_params['email'])

            employees = Employee.objects.filter(filters)
            serialized_data = self.serializer_class(employees, many=True).data

            return Response(serialized_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="active")
    def active(self, request):
        employees = Employee.objects.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
