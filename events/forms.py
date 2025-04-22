from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
        required=True,
    )

    class Meta:
        model = Event
        fields = ['name', 'workout_type', 'description', 'event_date']