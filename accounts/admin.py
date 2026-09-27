from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "home_region")
    search_fields = ("user__username", "user__email", "home_region")