from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from event.models import Runner

RUNNER_URL = reverse("event:runner_list")


class PublicRunnersViewsTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(RUNNER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateRunnersViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

    def test_retrieve_runners(self) -> None:
        Runner.objects.create(
            username="runner1",
            first_name="First 1",
            last_name="Last 1",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
        )

        Runner.objects.create(
            username="runner2",
            first_name="First 2",
            last_name="Last 2",
            city="Lviv",
            date_of_birth="1999-01-01",
            gender="Female",
        )

        res = self.client.get(RUNNER_URL)
        self.assertEqual(res.status_code, 200)

        runners = Runner.objects.all()
        self.assertEqual(list(res.context["runners"]), list(runners))
        self.assertTemplateUsed(res, "event/runner_list.html")

    def test_runner_list_view_status_code(self) -> None:
        response = self.client.get(RUNNER_URL)
        self.assertEqual(response.status_code, 200)

    def test_runner_list_view_template_used(self) -> None:
        response = self.client.get(RUNNER_URL)
        self.assertTemplateUsed(response, "event/runner_list.html")


class PublicRunnerDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.runner = Runner.objects.create(
            username="Testuser",
            first_name="Test",
            last_name="User",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
        )
        self.runner_detail_url = reverse(
            "event:runner_detail", kwargs={"pk": self.runner.pk}
        )

    def test_login_required(self) -> None:
        res = self.client.get(self.runner_detail_url)
        self.assertNotEquals(res.status_code, 200)


class PrivateRunnerDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            date_of_birth="2000-01-01",
        )
        self.client.force_login(self.user)

        self.runner = Runner.objects.create(
            username="Testuser",
            first_name="Test",
            last_name="User",
            city="Kyiv",
            date_of_birth="2000-01-01",
            gender="Male",
        )
        self.runner_detail_url = reverse(
            "event:runner_detail", kwargs={"pk": self.runner.pk}
        )

    def test_retrieve_runner_detail(self) -> None:
        res = self.client.get(self.runner_detail_url)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.context["runner"], self.runner)

        self.assertTemplateUsed(res, "event/runner_detail.html")

        self.assertContains(res, "Testuser")
        self.assertContains(res, "Test")
        self.assertContains(res, "User")

    def test_runner_detail_view_template_used(self) -> None:
        response = self.client.get(self.runner_detail_url)
        self.assertTemplateUsed(response, "event/runner_detail.html")

    def test_runner_detail_view_context(self) -> None:
        response = self.client.get(self.runner_detail_url)
        self.assertEqual(response.context["runner"], self.runner)
