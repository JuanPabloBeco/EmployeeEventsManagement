from django.test import TestCase
from core.models import Employee, Event
from django.test import Client

from ..utils.setup_DB import setup_DB


TEST_EMPLOYEE_1 = {
    "first_name": "JRR",
    "last_name": "Tolkien",
    "email": "jrr@tolkien.com",
}

TEST_EMPLOYEE_2 = {
    "first_name": "CS",
    "last_name": "Lewis",
    "email": "cs@lewis.com",
}

TEST_EVENT_1 = {
    "employee_id" : 1,
    "date" : "2023-08-20",
    "type" : "Birth",
}

TEST_EVENT_2 = {
    "employee_id" : 1,
    "date" : "2023-08-31",
    "type" : "Enrollment",
}


class FollowingEventsTest(TestCase):
    def setUp(self):
        setup_DB()
        pass

    def test_following_events(self):
        client = Client()


        event0 = Event.objects.create(**TEST_EVENT_1)
        event0.save()

        event1 = Event.objects.create(**TEST_EVENT_2)
        event1.save()

        data = {
            "start_date": "2023-08-20",
            "date_range": 10,
        }

        response = client.post(f'/api_v1/event/following/', data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to get employee")
        
        self.assertEqual(len(response.data), 1, "Amount of events in not retrieved correctly")

        employee_retrieved = response.data[0]
        self.assertEqual(employee_retrieved["id"], event0.id, "Id not retrieved correctly")
        self.assertEqual(employee_retrieved["date"], event0.date, "Date not retrieved correctly")
        self.assertEqual(employee_retrieved["type"], event0.type, "Type not retrieved correctly")
