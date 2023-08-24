from django.urls import path, include
from rest_framework import routers

from .views.employee_view import EmployeeView

router = routers.DefaultRouter()
router.register(r'employee', EmployeeView, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]