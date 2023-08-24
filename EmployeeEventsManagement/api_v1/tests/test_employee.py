from django.test import TestCase
from core.models import Employee, Event
from django.test import Client

from ..util import setupDb


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

class EmployeeManagementTest(TestCase):
    def setUp(self):
        setupDb()
        pass

    def test_create_employee(self):
        client = Client()

        data = TEST_EMPLOYEE_1

        response = client.post(
            "/api_v1/employee/", data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201, "Can't create employee")

        created_employee = Employee.objects.filter(email=data["email"])
        self.assertEqual(len(created_employee), 1, "Unsuccessful employee creation")
        self.assertEqual(created_employee.first().first_name, data["first_name"], "First_name not saved correctly")
        self.assertEqual(created_employee.first().last_name, data["last_name"], "Last_name not saved correctly")
        self.assertEqual(created_employee.first().email, data["email"], "Email not saved correctly")

    def test_edit_put_employee(self):
        client = Client()

        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**original_data)

        new_data = TEST_EMPLOYEE_2

        response = client.put(f'/api_v1/employee/{employee.pk}/', data=new_data, content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to edit employee")
        
        updated_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(updated_employee.first_name, new_data["first_name"], "First_name not updated")
        self.assertEqual(updated_employee.last_name, new_data["last_name"], "Last_name not updated")
        self.assertEqual(updated_employee.email, new_data["email"], "Email not updated")

    def test_edit_patch_employee(self):
        client = Client()

        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**original_data)

        new_data = {"is_active": "False"}

        response = client.patch(f'/api_v1/employee/{employee.pk}/', data=new_data, content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to edit employee")
        
        updated_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(str(updated_employee.is_active), new_data["is_active"], "is_active not updated")

    def test_delete_employee(self):
        client = Client()

        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**original_data)

        response = client.delete(f'/api_v1/employee/{employee.pk}/',  content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to delete employee")
        
        deleted_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(str(deleted_employee.is_active), "False", "User was not deleted")

    def test_list_active_employees(self):
        client = Client()

        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2.is_active = False
        employee = Employee.objects.create(**employee_data_2)

        response = client.get(f'/api_v1/employee/active/',  content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to list active employees")
        
        active_employees = Employee.objects.filter(is_active=True)
        self.assertEqual(len(response.data), len(active_employees), "Unsuccessful employee listing")

    def test_list_active_employees(self):
        client = Client()

        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2["is_active"] = False
        employee = Employee.objects.create(**employee_data_2)

        response = client.get(f'/api_v1/employee/',  content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to list active employees")
        
        all_employees = Employee.objects.filter()
        self.assertEqual(len(response.data), len(all_employees), "Unsuccessful employee listing")

    def test_get_employee(self):
        client = Client()

        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**employee_data_1)

        response = client.get(f'/api_v1/employee/{employee.pk}/',  content_type="application/json")
        self.assertEqual(response.status_code, 200, "Failed to get employee")
        
        employee_retrieved = response.data
        self.assertEqual(employee_retrieved["first_name"], employee.first_name, "First_name not retrieved correctly")
        self.assertEqual(employee_retrieved["last_name"], employee.last_name, "Last_name not retrieved correctly")
        self.assertEqual(employee_retrieved["email"], employee.email, "Email not retrieved correctly")

    def test_search_employee(self):
        client = Client()

        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.create(**employee_data_1)

        response = client.get(f'/api_v1/employee/search/?first_name=JRR')
        #response = client.get(f'/api_v1/employee/search')
        self.assertEqual(response.status_code, 200, "Failed to get employee")
        
        employee_searched = response.data[0]
        self.assertEqual(employee_searched["first_name"], employee.first_name, "First_name not saved correctly")
        self.assertEqual(employee_searched["last_name"], employee.last_name, "Last_name not saved correctly")
        self.assertEqual(employee_searched["email"], employee.email, "Email not saved correctly")

