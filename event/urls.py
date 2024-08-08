from django.urls import path

from event.views import (
    index,
)

app_name = 'event'

urlpatterns = [
    path("", index, name="index"),

]