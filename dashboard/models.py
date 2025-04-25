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
    favorite = models.BooleanField(default=False)
    total_duration_seconds = models.IntegerField(default=0)
    calories_burnt_per_second = models.FloatField(default=0.0)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return self.text

    @classmethod
    def expired_goals(cls, user):
        today = timezone.now().date()

        expired = cls.objects.filter(
            user=user,
            completed=False,
            abandoned=False,
            end_date__date__lt=today
        )
        amount_expired = expired.count()
        expired.update(abandoned=True)
        return amount_expired


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    max_streak = models.PositiveIntegerField(default=0)
    total_calories_burnt = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    progress_value = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_name} ({self.progress_value}/{self.target_value})"

class WorkoutPlan(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('2-3x', '2-3 times per week'),
        ('3-4x', '3-4 times per week'),
        ('5-6x', '5-6 times per week'),
        ('weekly', 'Weekly'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='3-4x')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_weeks = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"


class WorkoutDay(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='workout_days')
    day_number = models.PositiveIntegerField()
    focus = models.CharField(max_length=100)
    instructions = models.TextField()

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.focus}"


class Exercise(models.Model):
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField(default=3)
    reps = models.CharField(max_length=50,
                            default="8-12")
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name}: {self.sets} x {self.reps}"
