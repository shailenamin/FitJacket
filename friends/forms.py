from django import forms
from .models import WorkoutGroup, Challenge

class FriendMgmtForm(forms.Form):
    friend = forms.CharField(max_length=100,required=False)

class WorkoutGroupForm(forms.ModelForm):
    class Meta:
        model = WorkoutGroup
        fields = ['name']

WORKOUT_TYPES = [
        ('Strength', 'Strength'),
        ('Cardio',   'Cardio'),
        ('Yoga',     'Yoga'),
    ]
class ChallengeForm(forms.ModelForm):
    workout_type = forms.ChoiceField(choices=WORKOUT_TYPES)
    class Meta:
        model = Challenge
        fields = ['name', 'workout_type', 'description', 'challenge_end_date']
        widgets = {'challenge_end_date': forms.DateInput(attrs={'type': 'date'}),}