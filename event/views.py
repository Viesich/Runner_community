from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash

from event.forms import (
    RunnerCreationForm,
    RunnerUpdateForm,
    EventCreationForm,
    EventSearchForm,
    RegistrationForm,
)
from event.models import Event, Runner, Registration, Distance
from django.urls import reverse_lazy, reverse


class BaseEventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    context_object_name = "events"
    paginate_by = 7

    def get_queryset(self) -> Event:
        queryset = Event.objects.all()

        event_type = self.request.GET.get("event_type")
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        form = EventSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name", "")
            location = form.cleaned_data.get("location", "")
            if name:
                queryset = queryset.filter(name__icontains=name)
            if location:
                queryset = queryset.filter(location__icontains=location)
        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = EventSearchForm(self.request.GET)
        context["distances"] = Distance.objects.all()
        for event in context["events"]:
            event.registration_count = event.registrations.count()
        return context


class EventListView(BaseEventListView):
    template_name = "event/index.html"

    def get_queryset(self) -> Event:
        queryset = super().get_queryset()
        event_type = self.request.GET.get("event_type")
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset.filter(
            start_datetime__gt=timezone.now(),
            is_active=True
        )

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "events"
        return context


class ArchiveListView(BaseEventListView):
    model = Event
    template_name = "event/archive_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(start_datetime__lt=timezone.now())

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "archive"
        return context


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
    context_object_name = "event"
    template_name = "event/event_detail.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["runner"] = self.request.user
        return context


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = "event/event_form.html"
    success_url = reverse_lazy("event:index")


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventCreationForm
    template_name = "event/event_form.html"
    success_url = reverse_lazy("event:index")


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = "event/event_confirm_delete.html"
    success_url = reverse_lazy("event:index")


class RunnerListView(LoginRequiredMixin, generic.ListView):
    model = Runner
    context_object_name = "runners"
    template_name = "event/runner_list.html"
    ordering = ["last_name", "first_name"]


class RunnerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Runner
    context_object_name = "runner"
    template_name = "event/runner_detail.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        runner = self.get_object()
        context["registrations"] = Registration.objects.filter(
            runner=runner).order_by("event__start_datetime")
        return context


class RunnerRegisterView(generic.CreateView):
    model = Runner
    form_class = RunnerCreationForm
    template_name = "event/runner_form.html"
    success_url = reverse_lazy("event:index")


class RunnerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Runner
    form_class = RunnerUpdateForm
    template_name = "event/runner_form.html"

    def get_success_url(self) -> str:
        runner = self.object
        return reverse("event:runner_detail", kwargs={"pk": runner.pk})

    def form_valid(self, form: EventCreationForm) -> HttpResponse:
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response


class RunnerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Runner
    template_name = "event/runner_confirm_delete.html"
    success_url = reverse_lazy("event:index")


class EventRegistrationListView(LoginRequiredMixin, generic.ListView):
    model = Registration
    template_name = "event/registration_list.html"
    context_object_name = "registrations"

    def get_queryset(self) -> Registration:
        event_id = self.kwargs["pk"]
        return Registration.objects.filter(
            event_id=event_id).order_by("distances")

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs["pk"]
        event = Event.objects.get(pk=event_id)

        context.update(
            {
                "event_type": event.event_type,
                "event_name": event.name,
                "event_date": event.start_datetime,
                "event_location": event.location,
                "distances": event.get_distances(),
                "organiser": event.organiser,
            }
        )
        return context


class MyRegistrationsView(LoginRequiredMixin, generic.ListView):
    model = Registration
    context_object_name = "registrations"
    template_name = "event/my-registration_list.html"

    def get_queryset(self) -> Registration:
        return Registration.objects.filter(runner=self.request.user)

    def get_context_data(self, **kwargs: dict) -> dict[Event]:
        context = super().get_context_data(**kwargs)
        context["runner"] = self.request.user
        context["events"] = Event.objects.filter(
            id__in=context["registrations"].values("event")
        )
        context["runner_id"] = context["runner"].pk
        return context


class RegistrationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Registration
    form_class = RegistrationForm
    # template_name = "event/registration_form.html"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["event_id"] = self.kwargs["event_id"]
        return kwargs

    def form_valid(self, form: EventCreationForm) -> HttpResponse:
        event = get_object_or_404(Event, id=self.kwargs["event_id"])
        runner = self.request.user

        if Registration.objects.filter(event=event, runner=runner).exists():
            form.add_error(None, "You are already registered for this event.")
            return self.form_invalid(form)

        form.instance.event = event
        form.instance.runner = runner
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("event:my_registrations_list")


class RegistrationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = "event/registration_form.html"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        registration = self.get_object()
        kwargs["event_id"] = registration.event.id
        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy("event:my_registrations_list")


class RegistrationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Registration
    template_name = "event/registration_confirm_delete.html"
    success_url = reverse_lazy("event:my_registrations_list")
