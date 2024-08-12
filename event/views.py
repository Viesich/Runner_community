from unittest import runner

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import generic

from event.forms import RunnerCreationForm, RunnerUpdateForm, EventCreationForm, EventSearchForm
from event.models import Event, Runner
from django.urls import reverse_lazy, reverse


@login_required
def index(request):
    events = Event.objects.all()
    form = EventSearchForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data.get('name', '')
        location = form.cleaned_data.get('location', '')
        if name:
            events = events.filter(name__icontains=name)
        if location:
            events = events.filter(location__icontains=location)
    context = {
        "events": events,
        "search_form": form,
    }
    return render(request, 'event/index.html', context)


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:index')


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventCreationForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:index')


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event:index')


class RunnerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Runner
    context_object_name = 'runner'
    template_name = 'event/runner_detail.html'


class RunnerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Runner
    form_class = RunnerCreationForm
    success_url = reverse_lazy("event:index")


class RunnerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Runner
    form_class = RunnerUpdateForm
    template_name = 'event/runner_form.html'

    def get_success_url(self):
        runner = self.object
        return reverse('event:runner_detail', kwargs={'pk': runner.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response


class RunnerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Runner
    template_name = "event/runner_confirm_delete.html"
    success_url = reverse_lazy("event:index")
