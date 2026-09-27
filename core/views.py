from django.shortcuts import render

from community.models import Story
from mountains.models import Mountain


def home(request):
    mountains = Mountain.objects.filter(is_featured=True)[:4]
    stories = Story.objects.select_related("author", "mountain").order_by("-created_at")[:3]
    return render(request, "core/home.html", {"mountains": mountains, "stories": stories})