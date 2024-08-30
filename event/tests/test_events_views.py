from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

import event.models
from event.models import Event, Distance

EVENT_URL = reverse("event:index")


class PublicEventsViewsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(EVENT_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateEventsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

    def test_retrieve_events(self):
        start_date = datetime(2024, 10, 10, 12, 0, 0,)
        distances1 = Distance.objects.create(km=42)
        distances2 = Distance.objects.create(km=21)
        marathon = Event.objects.create(
            name="Marathon",
            start_datetime=start_date,
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        marathon.distances.set([distances1])

        half_marathon = Event.objects.create(
            name="Half Marathon",
            start_datetime=start_date,
            location="Lviv",
            description="Test Description",
            event_type="Running",
            organiser="Run Ukraine",
        )
        half_marathon.distances.set([distances2])

        res = self.client.get(EVENT_URL)
        self.assertEqual(res.status_code, 200)

        events = Event.objects.all()
        self.assertEqual(
            list(res.context["events"]),
            list(events)
        )
        self.assertTemplateUsed(res, "event/index.html")

