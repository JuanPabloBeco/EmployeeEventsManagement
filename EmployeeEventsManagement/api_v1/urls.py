from django.urls import path, include
from rest_framework import routers

from .views.employee_view import EmployeeView
from .views.event_view import EventView
from .views.holidays_view import HolidaysView

router = routers.DefaultRouter()
router.register(r'employee', EmployeeView, basename='employee')
router.register(r'event', EventView, basename='event')
router.register(r'holiday', HolidaysView, basename='event')


urlpatterns = [
    path('', include(router.urls)),
]