from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Runner(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def get_age(self) -> int:
        today = datetime.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month and today.
                day < self.date_of_birth.day
        ):
            age -= 1
        return age


class Distance(models.Model):
    km = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.km} km"


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ("Running", "Running"),
        ("Cycling", "Cycling"),
        ("Swimming", "Swimming"),
    ]

    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=100)
    distances = models.ManyToManyField(Distance, related_name="events")
    description = models.TextField()
    event_type = models.CharField(max_length=100, choices=EVENT_TYPE_CHOICES)
    organiser = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("start_datetime",)

    def get_distances(self) -> list[str]:
        return [distance.km for distance in self.distances.all()]

    def update_is_active_status(self) -> None:
        if self.start_datetime <= timezone.now():
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    def save(self, *args: tuple, **kwargs: dict) -> None:
        if self.start_datetime <= timezone.now():
            self.is_active = False
        else:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Registration(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    runner = models.ForeignKey(
        Runner, on_delete=models.CASCADE, related_name="registrations"
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    distances = models.ForeignKey(Distance, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"{self.runner.last_name} "
            f"{self.runner.first_name} - "
            f"{self.event.name}"
        )
