from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    WORKOUT_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('yoga', 'Yoga'),
    ]

    name = models.CharField(max_length=255)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_CHOICES)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_event')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_date.strftime('%Y-%m-%d')}"
