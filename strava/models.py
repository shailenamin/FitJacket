from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StravaActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=100)
    distance = models.FloatField()
    moving_time = models.IntegerField()  # in seconds
    date = models.DateTimeField()
    strava_id = models.BigIntegerField(null=True)

    class Meta:
        unique_together = ('user', 'strava_id')