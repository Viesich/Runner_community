from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from event.models import Runner, Registration, Event, Distance


class PublicRegistrationsViewsTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=datetime(2024, 10, 10, 12, 0, 0),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )

    def test_login_required(self):
        res = self.client.get(
            reverse("event:registration_list", kwargs={"pk": self.event.pk})
        )
        self.assertNotEquals(res.status_code, 200)


class PrivateRegistrationsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=datetime(2024, 10, 10, 12, 0, 0),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        self.runner1 = Runner.objects.create(
            username="runner1",
            first_name="First 1",
            last_name="Last 1",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
        )
        self.runner2 = Runner.objects.create(
            username="runner2",
            first_name="First 2",
            last_name="Last 2",
            city="Lviv",
            date_of_birth="2001-01-01",
            gender="Male",
        )
        self.distances = Distance.objects.create(km=42)
        Registration.objects.create(
            event=self.event,
            runner=self.runner1,
            registration_date=datetime(2024, 10, 10, 12, 0, 0),
            distances=self.distances,
        )
        Registration.objects.create(
            event=self.event,
            runner=self.runner2,
            registration_date=datetime(2024, 12, 10, 12, 0, 0),
            distances=self.distances,
        )

    def test_retrieve_runners(self):
        url = reverse("event:registration_list", kwargs={"pk": self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marathon")

    def test_runner_list_view_template_used(self):
        response = self.client.get(
            reverse("event:registration_list", kwargs={"pk": self.event.pk})
        )
        self.assertTemplateUsed(response, "event/registration_list.html")
