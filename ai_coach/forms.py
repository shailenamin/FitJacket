from django import forms
from .models import CoachingSession

class CoachingForm(forms.ModelForm):
    question = forms.CharField(
        label="Ask for fitness advice",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'e.g., "How can I improve my running endurance?" or "What are some good exercises for beginners?"'
        })
    )

    class Meta:
        model = CoachingSession
        fields = ['question']
