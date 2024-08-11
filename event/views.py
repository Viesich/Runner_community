from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from event.models import Event


@login_required
def index(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, 'event/index.html', context)


