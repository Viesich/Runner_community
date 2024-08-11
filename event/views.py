from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from event.forms import RunnerCreationForm
from event.models import Event, Runner
from django.urls import reverse_lazy


@login_required
def index(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, 'event/index.html', context)


class RunnerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Runner
    form_class = RunnerCreationForm
    success_url = reverse_lazy("event:index")

