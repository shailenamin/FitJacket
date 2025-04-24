from django.db import models
from django.contrib.auth.models import User

class CoachingSession(models.Model):
    CATEGORY_CHOICES = [
        ('general',    'General'),
        ('strength',   'Strength'),
        ('cardio',     'Cardio'),
        ('nutrition',  'Nutrition'),
        ('flexibility','Flexibility'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_favorite = models.BooleanField(default=False)
    is_helpful = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.user.username} – {self.created_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-created_at']
