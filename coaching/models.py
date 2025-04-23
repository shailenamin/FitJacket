from django.db import models
from django.contrib.auth.models import User

class CoachingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coaching_sessions')
    request = models.TextField(help_text="User's coaching request or question")
    response = models.TextField(help_text="AI coach response")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Coaching session for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"


class CoachingCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
