from django import forms
from .models import WorkoutPlan, Goal


class WorkoutPlanGeneratorForm(forms.Form):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (new to working out)'),
        ('intermediate', 'Intermediate (some experience)'),
        ('advanced', 'Advanced (experienced)'),
    ]

    FREQUENCY_CHOICES = [
        ('2-3x', '2-3 times per week'),
        ('3-4x', '3-4 times per week'),
        ('5-6x', '5-6 times per week'),
    ]

    DURATION_CHOICES = [
        (4, '4 weeks'),
        (8, '8 weeks'),
        (12, '12 weeks'),
    ]

    EQUIPMENT_CHOICES = [
        ('none', 'None (body weight only)'),
        ('minimal', 'Minimal (dumbbells, resistance bands)'),
        ('full', 'Full gym access'),
    ]

    fitness_goals = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select goals for your workout plan"
    )

    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        initial='beginner'
    )

    workout_frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        initial='3-4x'
    )

    plan_duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        initial=4
    )

    equipment_access = forms.ChoiceField(
        choices=EQUIPMENT_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        initial='minimal'
    )

    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Any injuries, limitations, or specific requests?"
    )

    def __init__(self, user, *args, **kwargs):
        super(WorkoutPlanGeneratorForm, self).__init__(*args, **kwargs)
        self.fields['fitness_goals'].queryset = Goal.objects.filter(
            user=user,
            completed=False,
            abandoned=False
        )
