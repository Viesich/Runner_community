from datetime import datetime, date, timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from event.models import Runner, Distance, Event, Registration


class ModelsTests(TestCase):

    def test_runner_str(self) -> None:
        date_of_birth = date(
            2000,
            1,
            1,
        )
        runner = get_user_model().objects.create(
            first_name="Test_first",
            last_name="Test_last",
            city="Test_city",
            date_of_birth=date_of_birth,
            gender="Test_gender",
            password="password123",
        )
        self.assertEqual(
            str(runner),
            f"{runner.last_name} {runner.first_name}"
        )

    def test_create_runner_with_city_and_phone_number(self) -> None:
        username = "testuser"
        first_name = "Test_first"
        last_name = "Test_last"
        city = "Test_city"
        date_of_birth = date(2000, 1, 1)
        gender = "Test_gender"
        password = "password123"
        phone_number = "1234567890"
        runner = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            city=city,
            date_of_birth=date_of_birth,
            gender=gender,
            password=password,
            phone_number=phone_number,
        )
        self.assertEqual(runner.username, username)
        self.assertEqual(runner.first_name, first_name)
        self.assertEqual(runner.last_name, last_name)
        self.assertEqual(runner.city, city)
        self.assertEqual(runner.date_of_birth, date_of_birth)
        self.assertEqual(runner.gender, gender)
        self.assertEqual(runner.phone_number, phone_number)
        self.assertTrue(runner.check_password(password))

    def test_get_age(self) -> None:
        birth_date = date(1999, 8, 29)
        runner = Runner.objects.create(
            username="testuser",
            first_name="John",
            last_name="Doe",
            city="Kyiv",
            date_of_birth=birth_date,
            gender="Male",
        )
        expected_age = 25
        self.assertEqual(runner.get_age(), expected_age)

    def test_distance_str(self) -> None:
        distance = Distance.objects.create(km="20")
        self.assertEqual(str(distance), f"{distance.km} km")

    def test_event_str(self) -> None:
        distance = Distance.objects.create(km=20)
        start_date = datetime(
            2024,
            10,
            10,
            12,
            0,
            0,
        )
        event = Event.objects.create(
            name="Test",
            start_datetime=start_date,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.distances.add(distance)
        self.assertEqual(str(event), event.name)

    def test_get_distance(self) -> None:
        distance1 = Distance.objects.create(km=10)
        distance2 = Distance.objects.create(km=21)
        distance3 = Distance.objects.create(km=42)
        start_date = datetime(
            2024,
            10,
            10,
            12,
            0,
            0,
        )
        event = Event.objects.create(
            name="Test",
            start_datetime=start_date,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.distances.add(distance1, distance2, distance3)
        expected_distances = [10, 21, 42]
        self.assertEqual(event.get_distances(), expected_distances)

    def test_event_is_active_when_future_date(self) -> None:
        future_date = timezone.now() + timedelta(days=1)
        event = Event(
            name="Future Event",
            start_datetime=future_date,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.save()
        self.assertTrue(event.is_active)

    def test_event_is_inactive_when_past_date(self) -> None:
        past_date = timezone.now() - timedelta(days=1)
        event = Event(
            name="Past Event",
            start_datetime=past_date,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.save()
        self.assertFalse(event.is_active)

    def test_event_is_active_when_now(self) -> None:
        now = timezone.now()
        event = Event(
            name="Current Event",
            start_datetime=now,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.save()
        self.assertFalse(event.is_active)

    def test_registration_str(self) -> None:

        distance = Distance.objects.create(km=20)
        start_date = datetime(
            2024,
            10,
            10,
            12,
            0,
            0,
        )
        event = Event.objects.create(
            name="Test",
            start_datetime=start_date,
            location="Kyiv",
            event_type="Running",
            organiser="NewRun",
        )
        event.distances.add(distance)

        date_of_birth = date(
            2000,
            1,
            1,
        )
        runner = get_user_model().objects.create(
            first_name="Test_first",
            last_name="Test_last",
            city="Test_city",
            date_of_birth=date_of_birth,
            gender="Test_gender",
            password="password123",
        )
        registration = Registration.objects.create(
            event=event,
            runner=runner,
            distances=distance,
        )
        self.assertEqual(
            str(registration),
            f"{runner.last_name} {runner.first_name} - {event.name}"
        )
