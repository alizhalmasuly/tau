from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from community.models import Story
from mountains.models import SavedHike

from .forms import ProfileForm, SignUpForm
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("accounts:profile")
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    stories = Story.objects.filter(author=request.user).select_related("mountain")
    saved_hikes = SavedHike.objects.filter(user=request.user).select_related("mountain")
    gear_checks = request.user.gear_checks.select_related("equipment").filter(have_it=True)
    return render(request, "accounts/profile.html", {
        "profile": profile_obj, "stories": stories, "saved_hikes": saved_hikes, "gear_checks": gear_checks,
    })


def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=profile_user)
    stories = Story.objects.filter(author=profile_user).select_related("mountain")
    return render(request, "accounts/public_profile.html", {
        "profile_user": profile_user, "profile": profile_obj, "stories": stories,
    })


@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль обновлён")
        return redirect("accounts:profile")
    return render(request, "accounts/edit_profile.html", {"form": form})