from django.db import models
from django.utils import timezone
from django_filters.filters import Filter
from django_filters.rest_framework import DateTimeFromToRangeFilter, FilterSet


class Event(models.Model):
    session_id = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['session_id', 'category', 'name', 'data', 'timestamp']

    @property
    def type(self):
        return '_'.join([self.category, self.name])

    def __str__(self):
        return f'{self.session_id} ({self.type})'

class EventFilter(FilterSet):
    timestamp = DateTimeFromToRangeFilter()

    class Meta:
        model = Event
        fields = ['session_id', 'category', 'timestamp']