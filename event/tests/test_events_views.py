from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from event.models import Event, Distance

EVENT_URL = reverse("event:index")
ARCHIVE_URL = reverse("event:archive_list")


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
        start_date = datetime(
            2024,
            10,
            10,
            12,
            0,
            0,
        )
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
        marathon.distances.set(
            [distances1],
        )

        half_marathon = Event.objects.create(
            name="Half Marathon",
            start_datetime=start_date,
            location="Lviv",
            description="Test Description",
            event_type="Running",
            organiser="Run Ukraine",
        )
        half_marathon.distances.set(
            [distances2],
        )

        res = self.client.get(EVENT_URL)
        self.assertEqual(res.status_code, 200)

        events = Event.objects.all()
        self.assertEqual(list(res.context["events"]), list(events))
        self.assertTemplateUsed(res, "event/index.html")

    def test_event_list_view_status_code(self):
        response = self.client.get(EVENT_URL)
        self.assertEqual(response.status_code, 200)

    def test_event_list_view_template_used(self):
        response = self.client.get(EVENT_URL)
        self.assertTemplateUsed(response, "event/index.html")

    def test_event_list_view_search(self):
        response = self.client.get(EVENT_URL, {"name": "Marathon", "location": "Kyiv"})
        self.assertContains(response, "Marathon")
        self.assertContains(response, "Kyiv")
        self.assertNotContains(response, "Half Marathon")
        self.assertNotContains(response, "Lviv")


class PublicArchiveViewsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(ARCHIVE_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateArchiveViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

    def test_retrieve_archive(self):
        start_date = datetime(
            2024,
            7,
            10,
            12,
            0,
            0,
        )

        distances1 = Distance.objects.create(km=42)
        marathon = Event.objects.create(
            name="Marathon",
            start_datetime=start_date,
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        marathon.distances.set([distances1])

        distances2 = Distance.objects.create(km=21)
        half_marathon = Event.objects.create(
            name="Half Marathon",
            start_datetime=start_date,
            location="Lviv",
            description="Test2 Description",
            event_type="Running",
            organiser="Run Ukraine",
        )

        half_marathon.distances.set([distances2])

        res = self.client.get(ARCHIVE_URL)
        self.assertEqual(res.status_code, 200)

        events = Event.objects.all()
        self.assertEqual(list(res.context["events"]), list(events))
        self.assertTemplateUsed(res, "event/archive_list.html")

    def test_archive_list_view_status_code(self):
        response = self.client.get(ARCHIVE_URL)
        self.assertEqual(response.status_code, 200)

    def test_archive_list_view_template_used(self):
        response = self.client.get(ARCHIVE_URL)
        self.assertTemplateUsed(response, "event/archive_list.html")


class PublicEventDetailViewTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=datetime(2024, 10, 10, 12, 0, 0),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        self.event_detail_url = reverse(
            "event:event_detail", kwargs={"pk": self.event.pk}
        )

    def test_login_required(self):
        res = self.client.get(self.event_detail_url)
        self.assertNotEquals(res.status_code, 200)


class PrivateEventDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=datetime(2024, 7, 10, 12, 0, 0),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )

        self.distance = Distance.objects.create(km=42)
        self.event.distances.set([self.distance])

        self.event_detail_url = reverse(
            "event:event_detail", kwargs={"pk": self.event.pk}
        )

    def test_retrieve_event_detail(self):
        res = self.client.get(self.event_detail_url)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.context["event"], self.event)

        self.assertTemplateUsed(res, "event/event_detail.html")

        self.assertContains(res, "Marathon")
        self.assertContains(res, "Kyiv")
        self.assertContains(res, "Test Description")

    def test_event_detail_view_template_used(self):
        response = self.client.get(self.event_detail_url)
        self.assertTemplateUsed(response, "event/event_detail.html")

    def test_event_detail_view_context(self):
        response = self.client.get(self.event_detail_url)
        self.assertEqual(response.context["event"], self.event)
