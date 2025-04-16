from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Goal(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    abandoned = models.BooleanField(default=False)

    def __str__(self):
        return self.text
