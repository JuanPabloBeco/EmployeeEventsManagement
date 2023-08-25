from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from api_v1.serializers.event_serializer import EventSerializer, FollowingEventsSerializer
from core.models import Event, Employee  # Make sure to import your Employee model


class EventView(viewsets.GenericViewSet):
    @action(methods=['post'], detail=False)
    def following(self, request):
        serializer = FollowingEventsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        events = serializer.get_following_events()

        event_serializer = EventSerializer(events, many=True)

        return Response(event_serializer.data, status=status.HTTP_200_OK)
