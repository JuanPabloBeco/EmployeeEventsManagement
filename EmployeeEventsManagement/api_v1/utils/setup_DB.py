from core.models import Employee, Event


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

def setup_DB():
    employee = Employee.objects.create(**TEST_EMPLOYEE_1)

    event0 = Event.objects.create(**TEST_EVENT_1)
    event1 = Event.objects.create(**TEST_EVENT_2)
    