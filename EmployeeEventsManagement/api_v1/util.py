from core.models import Employee, Event


def setupDb():
    employee = Employee.objects.create(
        first_name="Juan Pablo",
        last_name="Becoña",
        email="jpbecona@gmail.com",
    )
    employee.save()

    event0 = Event.objects.create(
        employee=employee,
        date="2029-08-20",
        type="Birth",
    )

