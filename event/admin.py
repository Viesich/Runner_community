from tkinter import EventType

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from event.models import Event, EventRegistration, Result, Runner


admin.site.register(EventRegistration)

admin.site.register(Result)

admin.site.register(Runner, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "event_type", )
    search_fields = ('name',)
    list_filter = ('name', "date", "event_type")
