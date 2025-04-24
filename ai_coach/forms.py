# ai_coach/forms.py
from django import forms
from .models import CoachingSession

class CoachingForm(forms.ModelForm):
    class Meta:
        model = CoachingSession
        fields = ['category', 'question']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg mb-3'
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 3,
                'placeholder': 'E.g. “How do I build up my squat strength safely?”'
            }),
        }
        labels = {
            'category': 'Topic',
            'question': 'Your Question'
        }
