from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import Event, Registration, Result, Runner, Distance


@admin.register(Runner)
class RunnerAdmin(UserAdmin):
    list_display = (
        "full_name",
        "username",
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
    )
    search_fields = ("runner__last_name", "runner__first_name", "event__name")
    list_filter = ("event__start_datetime", "event",)

    def event_date(self, obj: Registration) -> datetime:
        return obj.event.start_datetime

    event_date.short_description = "Event Date"

    def runner(self, obj: Registration) -> str:
        return f"{obj.runner.last_name} {obj.runner.first_name}"

    runner.short_description = "Runner"


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "event_name",
        "event_date",
        "runner_last_name",
        "time",
    )
    search_fields = (
        "registration__runner__last_name",
        "registration__runner__first_name",
    )
    list_filter = (
        "registration__event__start_datetime",
        "registration__event",
        "registration__distances",
    )

    def event_name(self, obj: Result) -> str:
        return obj.registration.event.name

    event_name.short_description = "Event Name"

    def event_date(self, obj: Result) -> datetime:
        return obj.registration.event.start_datetime

    event_date.short_description = "Event Date"

    def runner_last_name(self, obj: Result) -> str:
        return obj.registration.runner.last_name

    runner_last_name.short_description = "Runner Last Name"

    def distance(self, obj: Result) -> int:
        return obj.registration.distances

    distance.short_description = "Distance"
