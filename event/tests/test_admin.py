from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from event.models import Distance, Event


class AdminSiteRunnerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.admin_user)
        self.runner = get_user_model().objects.create_user(
            username="runner",
            first_name="Test",
            last_name="Runner",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
            password="testrunner",
            phone_number="0123456789"
        )

    def test_runner_fields_displayed_in_changelist(self) -> None:
        url = reverse("admin:event_runner_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.runner.username)
        self.assertContains(res, self.runner.city)
        self.assertContains(res, self.runner.gender)
        self.assertContains(res, "Jan. 1, 2000")
        self.assertContains(res, self.runner.phone_number)

    def test_runner_fields_displayed_in_change(self) -> None:
        url = reverse("admin:event_runner_change", args=[self.runner.id])
        res = self.client.get(url)
        self.assertContains(res, self.runner.date_of_birth)
        self.assertContains(res, self.runner.city)
        self.assertContains(res, self.runner.gender)
        self.assertContains(res, self.runner.phone_number)

    def test_runner_add_fields_displayed_add(self) -> None:
        url = reverse("admin:event_runner_add")
        res = self.client.get(url)
        self.assertContains(res, "id_first_name")
        self.assertContains(res, "id_last_name")
        self.assertContains(res, "id_date_of_birth")
        self.assertContains(res, "id_gender")
        self.assertContains(res, "id_phone_number")


class AdminSiteDistanceTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="runner",
            first_name="Test",
            last_name="Runner",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
            password="testrunner",
            phone_number="0123456789"
        )
        self.client.force_login(self.admin_user)
        self.distance = Distance.objects.create(km=20)

    def test_distance_fields_displayed_in_changelist(self) -> None:
        url = reverse("admin:event_distance_changelist")
        res = self.client.get(url)
        self.assertContains(res, str(self.distance.km))


# class EventAdminTests(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             username="admin",
#             password="testadmin",
#             date_of_birth="2000-01-01",
#         )
#         self.client.force_login(self.admin_user)
#
#         self.event1 = Event.objects.create(
#             name="Marathon",
#             start_datetime=datetime(2024, 10, 1, 9, 0, 0),
#             location="Lviv",
#             description="Annual city marathon.",
#             event_type="Running",
#             organiser="Run Ukraine"
#         )
#         self.event2 = Event.objects.create(
#             name="Triathlon",
#             start_datetime=datetime(2024, 11, 15, 10, 0, 0),
#             location="Odesa",
#             description="Summer triathlon event.",
#             event_type="Swimming",
#             organiser="Triathlon Federation"
#         )
#
#     def test_event_search(self) -> None:
#         url = reverse("admin:event_event_changelist")
#         res = self.client.get(url, {"q": "Marathon"})
#         print(Event.objects.filter(name__icontains="Marathon").query)
#         self.assertContains(res, self.event1.name)
#         self.assertNotContains(res, self.event2.name)
#
#     def test_event_search_no_results(self) -> None:
#         url = reverse("admin:event_event_changelist")
#         res = self.client.get(url, {"q": "Cycling"})
#         print(Event.objects.filter(name__icontains="Cycling").query)
#         self.assertNotContains(res, self.event1.name)
#         self.assertNotContains(res, self.event2.name)
