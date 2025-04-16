from django import forms
from .models import WorkoutGroup

class FriendMgmtForm(forms.Form):
    friend = forms.CharField(max_length=100,required=False)

class WorkoutGroupForm(forms.ModelForm):
    class Meta:
        model = WorkoutGroup
        fields = ['name']