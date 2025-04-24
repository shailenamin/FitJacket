from django.contrib.auth.models import User
from django.db import models
import datetime

class Event(models.Model):
    WORKOUT_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('yoga', 'Yoga'),
    ]

    name = models.CharField(max_length=255)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_CHOICES)
    description = models.TextField(blank=True)
    event_date = models.DateField(null=False, default=datetime.date.today)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_event')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_date.strftime('%Y-%m-%d')}"

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} joined {self.event.name}"