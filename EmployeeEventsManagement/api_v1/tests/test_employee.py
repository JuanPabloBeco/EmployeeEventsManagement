from django.test import TestCase
from django.test import Client

from core.models import Employee, Event

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

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

class EmployeeManagementTest(TestCase):
    def setUp(self):
        setup_DB()
        self.client = Client()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        pass
    
    def test_create_employee(self):
        employee_data = TEST_EMPLOYEE_2

        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 201, "Can't create employee")

        created_employee = Employee.objects.filter(email=employee_data["email"])
        self.assertEqual(len(created_employee), 1, "Unsuccessful employee creation")
        self.assertEqual(created_employee.first().first_name, employee_data["first_name"], "First_name not saved correctly")
        self.assertEqual(created_employee.first().last_name, employee_data["last_name"], "Last_name not saved correctly")
        self.assertEqual(created_employee.first().email, employee_data["email"], "Email not saved correctly")

    def test_create_employee_wrong_data(self):
        employee_data = {**TEST_EMPLOYEE_1}

        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Two employees with the same email created")

        employee_data = {**TEST_EMPLOYEE_2}
        employee_data["first_name"] = False
        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid first_name created")

        employee_data["last_name"] = False
        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid last_name created")

        employee_data["email"] = "abcd"
        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid email created")
        
    def test_create_employee_no_token(self):
        employee_data = TEST_EMPLOYEE_1

        response = self.client.post(
            "/api_v1/employee/", 
            data=employee_data, 
            content_type="application/json", 
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_edit_put_employee(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = TEST_EMPLOYEE_2
        

        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to edit employee")
        
        updated_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(updated_employee.first_name, new_data["first_name"], "First_name not updated")
        self.assertEqual(updated_employee.last_name, new_data["last_name"], "Last_name not updated")
        self.assertEqual(updated_employee.email, new_data["email"], "Email not updated")

    def test_edit_put_employee_wrong_data(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = {**TEST_EMPLOYEE_2}

        new_data["first_name"] = False
        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid first_name edited")

        new_data["last_name"] = False
        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid last_name edited")

        new_data["email"] = "abcd"
        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid email edited")

        new_data["is_active"] = "test"
        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid is_active edited")
        
    def test_edit_put_employee_no_token(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = TEST_EMPLOYEE_2

        response = self.client.put(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data, 
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_edit_patch_employee(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = {"is_active": "False"}

        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to edit employee")
        
        updated_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(str(updated_employee.is_active), new_data["is_active"], "is_active not updated")

    def test_edit_patch_employee_wrong_data(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = {"first_name": False}
        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid first_name edited")

        new_data = {"last_name": False}
        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid last_name edited")

        new_data = {"email": "abcd"}
        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid email edited")

        new_data = {"is_active": "test"}
        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Employee with invalid is_active edited")
        
    def test_edit_patch_employee_no_token(self):
        original_data = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**original_data)

        new_data = {"is_active": "False"}

        response = self.client.patch(
            f'/api_v1/employee/{employee.pk}/', 
            data=new_data,
            content_type="application/json",
        )
        
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_delete_employee(self):
        original_data = TEST_EMPLOYEE_2
        employee = Employee.objects.create(**original_data)

        response = self.client.delete(
            f'/api_v1/employee/{employee.pk}/',
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to delete employee")
        
        deleted_employee = Employee.objects.get(pk=employee.pk)
        self.assertEqual(str(deleted_employee.is_active), "False", "User was not deleted")

    def test_delete_employee_wrong_data(self):
        response = self.client.delete(
            f'/api_v1/employee/test/',
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Deleting with invalid id")

        response = self.client.delete(
            f'/api_v1/employee/1000/',
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 404, "Deleting with wrong id")

    def test_delete_employee_no_token(self):
        original_data = TEST_EMPLOYEE_2
        employee = Employee.objects.create(**original_data)

        response = self.client.delete(
            f'/api_v1/employee/{employee.pk}/',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_list_active_employees(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2["is_active"] = False
        employee = Employee.objects.create(**employee_data_2)

        response = self.client.get(
            f'/api_v1/employee/active/',
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to list active employees")
        
        active_employees = Employee.objects.filter(is_active=True)
        self.assertEqual(len(response.data), len(active_employees), "Unsuccessful employee listing")

    def test_list_active_employees_no_token(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2["is_active"] = False
        employee = Employee.objects.create(**employee_data_2)

        response = self.client.get(
            f'/api_v1/employee/active/',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_list_all_employees(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2["is_active"] = False
        employee = Employee.objects.create(**employee_data_2)

        response = self.client.get(
            f'/api_v1/employee/',
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to list all employees")
        
        all_employees = Employee.objects.filter()
        self.assertEqual(len(response.data), len(all_employees), "Unsuccessful employee listing")

    def test_list_all_employees_no_token(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)
        employee_data_2 = TEST_EMPLOYEE_2
        employee_data_2["is_active"] = False
        employee = Employee.objects.create(**employee_data_2)

        response = self.client.get(
            f'/api_v1/employee/',
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_get_employee_wrong_data(self):
        response = self.client.get(
            f'/api_v1/employee/1000/',
            content_type="application/json",
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 404, "Get employee with wrong id")

    def test_get_employee_no_token(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)

        response = self.client.get(
            f'/api_v1/employee/{employee.pk}/',
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

    def test_search_employee(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)

        response = self.client.get(
            f'/api_v1/employee/search/?first_name={employee.first_name}',
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 200, "Failed to search employees")
        
        employee_searched = response.data[0]
        self.assertEqual(employee_searched["first_name"], employee.first_name, "First_name not saved correctly")
        self.assertEqual(employee_searched["last_name"], employee.last_name, "Last_name not saved correctly")
        self.assertEqual(employee_searched["email"], employee.email, "Email not saved correctly")

    def test_search_employee_wrong_data(self):
        employee_data_1 = TEST_EMPLOYEE_1
        employee = Employee.objects.get(**employee_data_1)

        response = self.client.get(
            f'/api_v1/employee/search/?is_active=test',
            headers={"Authorization": f"Token {self.token.key}"},
        )
        self.assertEqual(response.status_code, 400, "Two employees with the same email created")

    def test_search_employee_no_token(self):
        response = self.client.get(
            f'/api_v1/employee/search/?first_name=JRR',
        )
        self.assertEqual(response.status_code, 401, "Failed unauthorize endpoint access")

