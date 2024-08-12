from django.urls import path

from event.views import (
    index,
    EventCreateView,
    RunnerDetailView,
    RunnerCreateView,
    RunnerUpdateView,
    RunnerDeleteView,
)

app_name = 'event'

urlpatterns = [
    path("", index, name="index"),
    path("events/create", EventCreateView.as_view(), name="event_create"),
    path("runners/<int:pk>/detail", RunnerDetailView.as_view(), name="runner_detail"),
    path("runners/create", RunnerCreateView.as_view(), name="runner_create"),
    path("runners/<int:pk>/update", RunnerUpdateView.as_view(), name="runner_update"),
    path("runners/<int:pk>/delete", RunnerDeleteView.as_view(), name="runner_delete"),
]
