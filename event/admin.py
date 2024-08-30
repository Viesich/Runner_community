from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import Event, Registration, Runner, Distance


@admin.register(Runner)
class RunnerAdmin(UserAdmin):
    list_display = (
        "username",
        "city",
        "gender",
        "date_of_birth",
        "phone_number",
    ) + UserAdmin.list_display[1:]
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "date_of_birth",
                        "city",
                        "gender",
                        "phone_number",
                    )
                },
            ),
        )
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

    verbose_name = "Runner"
    verbose_name_plural = "Runners"

    def full_name(self, obj: Runner) -> str:
        return f"{obj.last_name} {obj.first_name}"

    full_name.short_description = "Full Name"


@admin.register(Distance)
class DistanceAdmin(admin.ModelAdmin):
    list_display = ("km",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("start_datetime", "name", "event_type", "location")
    search_fields = ("name",)
    list_filter = ("name", "start_datetime", "event_type")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "event_date",
        "event",
        "runner",
        "distances",
    )
    search_fields = (
        "event__name",
        "runner__last_name",
        "runner__first_name",

    )
    list_filter = ("event__start_datetime", "runner", "distances", )

    def event_date(self, obj: Registration) -> datetime:
        return obj.event.start_datetime

    event_date.short_description = "Event Date"

    def runner(self, obj: Registration) -> str:
        return f"{obj.runner.last_name} {obj.runner.first_name}"

    runner.short_description = "Runner"

