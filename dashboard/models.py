from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    abandoned = models.BooleanField(default=False)

    def __str__(self):
        return self.text
