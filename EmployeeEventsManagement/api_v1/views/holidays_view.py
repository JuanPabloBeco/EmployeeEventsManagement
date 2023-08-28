from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action


from api_v1.utils.get_holidays_in_3_next_days import get_holidays_in_3_next_days
import json


class HolidaysView(
    viewsets.GenericViewSet,
):

    @action(methods=["get"], detail=False)
    def following(self, request):
        holidays = get_holidays_in_3_next_days()
        if (holidays.get("error")):
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serialized = json.dumps(holidays)
        return Response(serialized, status=status.HTTP_200_OK)
