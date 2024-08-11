from django.urls import path

from event.views import (
    index, RunnerCreateView,
)

app_name = 'event'

urlpatterns = [
    path("", index, name="index"),
    path("runners/create", RunnerCreateView.as_view(), name="runner_create"),
]
