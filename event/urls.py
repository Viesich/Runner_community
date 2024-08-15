from django.urls import path

from event.views import (
    index,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    RunnerListView,
    RunnerDetailView,
    RunnerUpdateView,
    RunnerDeleteView,
    EventRegistrationListView,
    MyRegistrationsView,
    RunnerRegisterView,
)

app_name = 'event'

urlpatterns = [
    path("", index, name="index"),
    path("events/<int:pk>/detail", EventDetailView.as_view(), name="event_detail"),
    path("events/create", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/update", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete", EventDeleteView.as_view(), name="event_delete"),
    path('register/', RunnerRegisterView.as_view(), name='register_runner'),
    path("runners/", RunnerListView.as_view(), name="runner_list"),
    path("runners/<int:pk>/detail", RunnerDetailView.as_view(), name="runner_detail"),
    path("runners/<int:pk>/update", RunnerUpdateView.as_view(), name="runner_update"),
    path("runners/<int:pk>/delete", RunnerDeleteView.as_view(), name="runner_delete"),
    path('events/<int:pk>/registrations/', EventRegistrationListView.as_view(), name='registration_list'),
    # path('events/<int:pk>/registrations/create/', EventRegistrationCreate.as_view(), name='registration_create'),
    path('my-registrations/', MyRegistrationsView.as_view(), name='my_registrations'),

    # path('registrations/<int:event_id>/create/', RegistrationCreateView.as_view(), name='registration_create'),
]
