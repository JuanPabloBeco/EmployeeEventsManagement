from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 


from api_v1.utils.get_holidays_in_3_next_days import get_holidays_in_3_next_days
import json


class HolidaysView(
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)  

    @action(methods=["get"], detail=False)
    def following(self, request):
        holidays = get_holidays_in_3_next_days()
        if (holidays.get("error")):
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(holidays, status=status.HTTP_200_OK)
