from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


class Runner(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'),],
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.last_name + " " + self.first_name


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
    ]

    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=100)
    distances = models.CharField(max_length=255, help_text="List distances separated by commas (eg 42, 21, 10)")
    description = models.TextField()
    event_type = models.CharField(max_length=100, choices=EVENT_TYPE_CHOICES)
    organiser = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('start_datetime',)

    def get_distances(self):
        return list(f"{d.strip()} км" for d in self.distances.split(','))

    def __str__(self):
        return self.name


class Result(models.Model):
    registration = models.ForeignKey(
        "Registration",
        on_delete=models.CASCADE,
        related_name='results',
    )
    time = models.TimeField()
    position = models.IntegerField()

    def __str__(self):
        return (
            f"{self.position} place "
            f"{self.registration.runner.last_name} "
            f"{self.registration.runner.first_name} "
            f"{self.time}"
        )


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    distance = models.IntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ('event', 'runner', 'distance')

    def __str__(self):
        return f"{self.runner.last_name} {self.runner.first_name} - {self.event.name}"

    def save(self, *args, **kwargs):
        if self.event.start_datetime <= timezone.now():
            self.status = False
        else:
            self.status = True
        super().save(*args, **kwargs)
