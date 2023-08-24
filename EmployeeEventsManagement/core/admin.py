from django.contrib import admin

from .models import Event, Employee


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "first_name",
        "last_name",
        "id",
        "email",
    )
    ordering = (
        "first_name",
        "last_name",
        "id",
        "email",
    )
    list_filter = (
        "email",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                )
            },
        ),
    )


admin.site.register(Employee, EmployeeAdmin)

class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = (
        "type",
        "get_first_name",
        "get_last_name",
        "date",
        "id",
    )
    def get_first_name(self, obj):
        return obj.employee.first_name
    get_first_name.admin_order_field  = 'first name'  #Allows column order sorting
    get_first_name.short_description = 'Employee first Name'  #Renames column head

    def get_last_name(self, obj):
        return obj.employee.last_name
    get_last_name.admin_order_field  = 'last name'  #Allows column order sorting
    get_last_name.short_description = 'Employee last Name'  #Renames column head

    search_fields = (
        "id",
        "type",
        "date",
    )
    list_filter = (
        "type",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "employee",
                    "type",
                    "date"
                )
            },
        ),
    )

admin.site.register(Event, EventAdmin)
