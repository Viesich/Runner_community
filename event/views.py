from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import generic

from event.forms import (
    RunnerCreationForm,
    RunnerUpdateForm,
    EventCreationForm,
    EventSearchForm,
    # RegistrationForm
)
from event.models import Event, Runner, Registration
from django.urls import reverse_lazy, reverse


@login_required
def index(request):
    events = Event.objects.all()
    form = EventSearchForm(request.GET)
    count_participants = Registration.objects.all().count()
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
        "count_participants": count_participants,
    }
    return render(request, 'event/index.html', context)


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['runner'] = self.request.user
        return context


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


class RunnerListView(LoginRequiredMixin, generic.ListView):
    model = Runner
    context_object_name = 'runners'
    template_name = "event/runner_list.html"


class RunnerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Runner
    context_object_name = 'runner'
    template_name = 'event/runner_detail.html'


class RunnerRegisterView(generic.CreateView):
    model = Runner
    form_class = RunnerCreationForm
    template_name = 'event/runner_form.html'
    success_url = reverse_lazy('event:index')


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


class EventRegistrationListView(LoginRequiredMixin, generic.ListView):
    model = Registration
    template_name = "event/registration_list.html"
    context_object_name = 'registrations'

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return Registration.objects.filter(event_id=event_id).order_by('distance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['pk']
        event = Event.objects.get(pk=event_id)

        context.update({
            'event_type': event.event_type,
            'event_name': event.name,
            'event_date': event.start_datetime,
            'event_location': event.location,
            'distances': event.get_distances(),
            'organiser': event.organiser,
        })
        return context


class MyRegistrationsView(LoginRequiredMixin, generic.ListView):
    model = Registration
    context_object_name = 'registrations'
    template_name = "event/my-registration_list.html"

    def get_queryset(self):
        return Registration.objects.filter(runner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(id__in=context['registrations'].values('event'))
        return context

# class RegistrationCreateView(generic.CreateView):
#     model = Registration
#     form_class = RegistrationForm
#     template_name = 'event/registration_form.html'
#
#     def form_valid(self, form):
#         form.instance.runner = self.request.user
#         form.instance.event = Event.objects.get(pk=self.kwargs['event_id'])
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('event:registration_list', pk=self.kwargs['event_id'])
