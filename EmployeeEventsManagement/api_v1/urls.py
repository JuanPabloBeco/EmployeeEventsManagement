from django.urls import path, include
from rest_framework import routers

from .views.employee_view import EmployeeView
from .views.event_view import EventView

router = routers.DefaultRouter()
router.register(r'employee', EmployeeView, basename='employee')
router.register(r'event', EventView, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]