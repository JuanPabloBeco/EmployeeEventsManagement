from django.test import TestCase
from core.models import Employee, Event
from django.test import Client

from .util import setupDb


class EmployeeManagementTest(TestCase):
    def setUp(self):
        setupDb()
        pass

    def test_create_employee(self):
        client = Client()

        data = {
            "first_name": "JRR",
            "last_name": "Tolkien",
            "email": "jrr@tolkien.com",
        }

        response = client.post(
            "/api_v1/employee/", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200, "cant create employee")
        self.assertEqual(
            response.data["success"], True, "unsuccessful employee creation"
        )

        created_employee = Employee.objects.filter(email=data["email"])

        self.assertEqual(len(created_employee), 1, "unsuccessful employee creation")
