from django import forms

from .models import Mountain


class PreparationForm(forms.Form):
    mountain = forms.ModelChoiceField(queryset=Mountain.objects.all())
    difficulty = forms.ChoiceField(choices=Mountain.DIFFICULTY_CHOICES)
    duration_hours = forms.IntegerField(min_value=1, max_value=48, initial=5)
    season = forms.ChoiceField(choices=[("spring", "Весна"), ("summer", "Лето"), ("autumn", "Осень"), ("winter", "Зима")])
    people_count = forms.IntegerField(min_value=1, max_value=50, initial=2)