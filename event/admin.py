from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import Event, Registration, Result, Runner


@admin.register(Runner)
class RunnerAdmin(UserAdmin):
    list_display = ("full_name", "username", "gender", "date_of_birth", "phone_number",) + UserAdmin.list_display[1:]
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
    list_display = ("date", "name", "event_type", "location")
    search_fields = ('name',)
    list_filter = ('name', "date", "event_type")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'event', 'distance', 'runner',)
    search_fields = ('runner__last_name', 'runner__first_name', 'event__name')
    list_filter = ('event__date', 'event', 'distance')

    def event_date(self, obj):
        return obj.event.date

    event_date.short_description = 'Event Date'

    def runner(self, obj):
        return f"{obj.runner.last_name} {obj.runner.first_name}"

    runner.short_description = 'Runner'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'runner_last_name', 'distance', 'time', 'position')
    search_fields = ('registration__runner__last_name', 'registration__runner__first_name',)
    list_filter = ('registration__event__date', 'registration__event', 'registration__distance')

    def event_name(self, obj):
        return obj.registration.event.name

    event_name.short_description = 'Event Name'

    def event_date(self, obj):
        return obj.registration.event.date

    event_date.short_description = 'Event Date'

    def runner_last_name(self, obj):
        return obj.registration.runner.last_name

    runner_last_name.short_description = 'Runner Last Name'

    def distance(self, obj):
        return obj.registration.distance

    distance.short_description = 'Distance'
