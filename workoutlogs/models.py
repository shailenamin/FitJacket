from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    workout_type = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout_type} - {self.created_at.strftime('%Y-%m-%d')}"
