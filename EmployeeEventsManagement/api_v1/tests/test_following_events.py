from django.test import TestCase
from django.test import Client
from core.models import Employee, Event

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from ..utils.setup_DB import setup_DB



class FollowingEventsTest(TestCase):
    def setUp(self):
        setup_DB()

        self.client = Client()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        pass

    def test_following_events(self):
        event0 = Event.objects.get(id=1)
        event1 = Event.objects.get(id=2)

        data = {
            "start_date": "2023-08-20",
            "date_range": 10,
        }

        response = self.client.post(
            f'/api_v1/event/following/', 
            data=data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"}
        )
        self.assertEqual(response.status_code, 200, "Failed to get events")
        
        self.assertEqual(len(response.data), 1, "Amount of events in not retrieved correctly")

        events_retrieved = response.data[0]
        self.assertEqual(events_retrieved["id"], event0.id, "Id not retrieved correctly")
        self.assertEqual(events_retrieved["date"], event0.date, "Date not retrieved correctly")
        self.assertEqual(events_retrieved["type"], event0.type, "Type not retrieved correctly")

    def test_following_events_no_token(self):
        data = {
            "start_date": "2023-08-20",
            "date_range": 10,
        }

        response = self.client.post(
            f'/api_v1/event/following/', 
            data=data, 
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")
        