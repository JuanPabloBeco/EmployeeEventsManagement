from core.models import Employee, Event


def setup_DB():
    employee = Employee.objects.create(
        first_name="Juan Pablo",
        last_name="Becoña",
        email="jpbecona@gmail.com",
    )
    employee.save()

