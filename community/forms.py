from django import forms

from .models import Comment, Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ("title", "mountain", "hike_date", "difficulty", "description", "useful_tips", "equipment_used", "cover")
        widgets = {"hike_date": forms.DateInput(attrs={"type": "date"}), "description": forms.Textarea(attrs={"rows": 6})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3})}