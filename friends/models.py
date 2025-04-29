from django.contrib.auth.models import User
from django.db import models

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"

class WorkoutGroup(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMember(models.Model):
    group = models.ForeignKey(WorkoutGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class GroupInvite(models.Model):
    group = models.ForeignKey(WorkoutGroup, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_group_invites')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_group_invites')
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Challenge(models.Model):
    WORKOUT_TYPES = [
        ('Strength', 'Strength'),
        ('Cardio',   'Cardio'),
        ('Yoga',     'Yoga'),
    ]

    name          = models.CharField(max_length=255)
    group = models.ForeignKey(WorkoutGroup, on_delete=models.CASCADE)
    workout_type  = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    description   = models.TextField(blank=True)
    challenge_end_date    = models.DateField(null=True, blank=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChallangeParticipation(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challengeParticipators')
    challenge     = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenges')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')
        ordering        = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"