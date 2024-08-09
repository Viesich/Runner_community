from tkinter import EventType

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import Event, EventRegistration, Result, Runner


admin.site.register(Result)


@admin.register(Runner)
class RunnerAdmin(UserAdmin):
    list_display = ("full_name", "gender", "date_of_birth", "phone_number",) + UserAdmin.list_display[1:]
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("date_of_birth", "gender", "phone_number",)}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "date_of_birth",
                        "gender",
                        "phone_number",
                    )
                },
            ),
        )
    )

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    full_name.short_description = 'Full Name'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "event_type", )
    search_fields = ('name',)
    list_filter = ('name', "date", "event_type")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event__date', 'event', 'distance', 'runner', )
    search_fields = ('runner', )
    list_filter = ('event__date', 'event', 'distance')
