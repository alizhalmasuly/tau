from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, StoryForm
from .models import Story


def story_list(request):
    stories = Story.objects.select_related("author", "mountain").prefetch_related("likes")
    return render(request, "community/list.html", {"stories": stories})


def story_detail(request, pk):
    story = get_object_or_404(Story.objects.select_related("author", "mountain"), pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.author = request.user
            comment.save()
            return redirect("community:detail", pk=story.pk)
    liked = request.user.is_authenticated and story.likes.filter(pk=request.user.pk).exists()
    return render(request, "community/detail.html", {"story": story, "form": form, "liked": liked})


@login_required
def create_story(request):
    form = StoryForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        story = form.save(commit=False)
        story.author = request.user
        story.save()
        messages.success(request, "Ваша история опубликована")
        return redirect("community:detail", pk=story.pk)
    return render(request, "community/create.html", {"form": form})


@login_required
@require_POST
def toggle_like(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.likes.filter(pk=request.user.pk).exists():
        story.likes.remove(request.user)
    else:
        story.likes.add(request.user)
    return redirect("community:detail", pk=pk)