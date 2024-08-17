from django.http import HttpResponse, HttpRequest
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from event.forms import (
    RunnerCreationForm,
    RunnerUpdateForm,
    EventCreationForm,
    EventSearchForm,
    RegistrationForm,
    # RegistrationUpdateForm,
)
from event.models import Event, Runner, Registration, Distance
from django.urls import reverse_lazy, reverse


@login_required
def index(request: HttpRequest) -> HttpResponse:
    events = Event.objects.all()
    form = EventSearchForm(request.GET)
    distances = Distance.objects.all()
    if form.is_valid():
        name = form.cleaned_data.get("name", "")
        location = form.cleaned_data.get("location", "")
        if name:
            events = events.filter(name__icontains=name)
        if location:
            events = events.filter(location__icontains=location)
    context = {
        "events": events,
        "search_form": form,
        "distances": distances,
    }
    return render(request, "event/index.html", context)


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


class RunnerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Runner
    context_object_name = "runner"
    template_name = "event/runner_detail.html"


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

    def get_object(self, queryset: Runner = None) -> Runner:
        obj = super().get_object(queryset)
        if obj != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def form_valid(self, form: EventCreationForm) -> HttpResponse:
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response


class RunnerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Runner
    template_name = "event/runner_confirm_delete.html"
    success_url = reverse_lazy("event:index")

    def get_object(self, queryset: Runner = None) -> Runner:
        obj = super().get_object(queryset)
        if obj != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj


class EventRegistrationListView(LoginRequiredMixin, generic.ListView):
    model = Registration
    template_name = "event/registration_list.html"
    context_object_name = "registrations"

    def get_queryset(self) -> Registration:
        event_id = self.kwargs["pk"]
        return (
            Registration.objects
            .filter(event_id=event_id)
            .order_by("distances")
        )

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
        kwargs['event_id'] = self.kwargs['event_id']
        return kwargs

    def form_valid(self, form):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
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
    template_name = 'event/registration_form.html'

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        registration = self.get_object()
        kwargs['event_id'] = registration.event.id
        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy("event:my_registrations_list")
