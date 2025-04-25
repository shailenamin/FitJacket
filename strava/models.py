from django.db import models

# Create your models here.

class StravaActivity(models.Model):
    name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=100)
    distance = models.FloatField()
    moving_time = models.IntegerField()  # in seconds
    date = models.DateTimeField()