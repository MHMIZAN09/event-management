from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        return self.date >= timezone.localdate()


class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return self.name
