from django.test import TestCase
from core.models import Employee, Event
from django.test import Client

from ..utils.setup_DB import setup_DB
import json


class FollowingHolidaysTest(TestCase):
    def setUp(self):
        setup_DB()
        pass

    def test_following_events(self):
        client = Client()

        response = client.get(f'/api_v1/holiday/following/')
        self.assertEqual(response.status_code, 200, "Failed to get holidays")

        holidays_retrieved = json.loads(response.data)
        self.assertEqual(len(holidays_retrieved), 3, "Amount of days of the answer not filled correctly")
