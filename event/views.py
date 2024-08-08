from django.shortcuts import render

from event.models import Event


def index(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, 'event/index.html', context)


