from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from event.forms import (
    RunnerCreationForm,
    RunnerUpdateForm,
    RegistrationCreationForm,
    EventCreationForm,
    EventSearchForm,
    RegistrationForm,
)
from event.models import Runner, Event, Distance, Registration


class RunnerCreationFormTests(TestCase):
    def test_runner_creation_form_valid_data(self):
        form_data = {
            "username": "new_user",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "city": "Test_city",
            "date_of_birth": "2000-01-01",
            "gender": "Male",
            "password1": "user12test",
            "password2": "user12test",
            "phone_number": "1234567890",
        }
        form = RunnerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_runner_creation_form_passwords_not_matching(self):
        form_data = {
            "username": "new_user",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "city": "Test_city",
            "date_of_birth": "2000-01-01",
            "gender": "Male",
            "password1": "user12test",
            "password2": "wrongpassword",
            "phone_number": "1234567890",
        }
        form = RunnerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class RunnerUpdateFormTests(TestCase):
    def setUp(self):
        self.runner = Runner.objects.create(
            username="runner_test",
            first_name="Test",
            last_name="Runner",
            date_of_birth="2000-01-01",
            city="Test City",
            gender="Male",
            phone_number="1234567890",
        )

    def test_runner_update_form_valid_data(self):
        form_data = {
            "username": "runner_test",
            "first_name": "Updated First",
            "last_name": "Updated Last",
            "date_of_birth": "1995-01-01",
            "city": "Updated City",
            "gender": "Female",
            "phone_number": "0987654321",
        }
        form = RunnerUpdateForm(instance=self.runner, data=form_data)
        self.assertTrue(form.is_valid())


class RegistrationCreationFormTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=timezone.now(),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        self.distance1 = Distance.objects.create(km=5)
        self.distance2 = Distance.objects.create(km=10)
        self.event.distances.add(self.distance1, self.distance2)

    def test_registration_creation_form_valid_event_id(self):
        form = RegistrationCreationForm(event_id=self.event.id)
        self.assertIn(self.distance1, form.fields["distances"].queryset)
        self.assertIn(self.distance2, form.fields["distances"].queryset)

    def test_registration_creation_form_invalid_event_id(self):
        form = RegistrationCreationForm(event_id=999)
        self.assertEqual(form.fields["distances"].queryset.count(), 0)


class EventCreationFormTests(TestCase):
    def setUp(self):
        self.distance1 = Distance.objects.create(km=5)
        self.distance2 = Distance.objects.create(km=10)

    def test_event_creation_form_valid_data(self):
        form_data = {
            "name": "New Event",
            "start_datetime": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            "location": "Test Location",
            "description": "This is a test event",
            "event_type": "Running",
            "organiser": "Test Organiser",
            "is_active": True,
            "distances": [self.distance1.id, self.distance2.id],
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class EventSearchFormTests(TestCase):
    def test_event_search_form_valid_data(self):
        form_data = {"name": "Marathon", "location": "Kyiv"}
        form = EventSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_search_form_empty_data(self):
        form = EventSearchForm(data={})
        self.assertTrue(form.is_valid())


class RegistrationFormTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Marathon",
            start_datetime=timezone.now(),
            location="Kyiv",
            description="Test Description",
            event_type="Running",
            organiser="New Run",
        )
        self.distance = Distance.objects.create(km=5)
        self.event.distances.add(self.distance)

    def test_registration_form_valid_event_id(self):
        form = RegistrationForm(event_id=self.event.id)
        self.assertEqual(
            list(form.fields["distances"].queryset), list(self.event.distances.all())
        )
