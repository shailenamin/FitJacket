# events/models.py

from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    WORKOUT_TYPES = [
        ('strength', 'Strength'),
        ('cardio',   'Cardio'),
        ('yoga',     'Yoga'),
    ]

    name          = models.CharField(max_length=255)
    workout_type  = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    description   = models.TextField(blank=True)
    event_date    = models.DateField(null=True, blank=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participation(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    event     = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering        = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"
