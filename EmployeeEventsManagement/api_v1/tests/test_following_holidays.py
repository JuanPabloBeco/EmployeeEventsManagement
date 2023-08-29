from django.test import TestCase
from django.test import Client
from core.models import Employee, Event

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from ..utils.setup_DB import setup_DB
import json


class FollowingHolidaysTest(TestCase):
    def setUp(self):
        setup_DB()
        self.client = Client()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        pass

    def test_following_holidays(self):
        response = self.client.get(
            f'/api_v1/holiday/following/', 
            headers={"Authorization": f"Token {self.token.key}"},
        )

        self.assertEqual(response.status_code, 200, "Failed to get holidays")

        holidays_retrieved = response.data
        self.assertEqual(len(holidays_retrieved), 3, "Amount of days of the answer not filled correctly")

    def test_following_holidays_no_token(self):
        response = self.client.get(
            f'/api_v1/holiday/following/', 
        )

        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")
        