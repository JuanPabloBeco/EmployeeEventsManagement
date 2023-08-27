from django.db import models
from django.utils import timezone
from enum import unique, Enum
from .employee import Employee


@unique
class EventTypes(Enum):
    BIRTH = 'Birth'
    ENROLLMENT = 'Enrollment'
    OTHER = 'other'

    def as_choice(self):
        return (self.name, self.value)
    
    @classmethod
    def as_choices(cls):
        return tuple(x.as_choice() for x in cls)
    
    @classmethod
    def choices_max_len(cls):
        return max(len(x.name) for x in cls)

class Event(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='events',
    )

    type = models.CharField(choices=EventTypes.as_choices(), max_length=EventTypes.choices_max_len())
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.type} - {self.date}'
    
    class Meta:
        verbose_name = ("Event")
        verbose_name_plural = ("Events")
    