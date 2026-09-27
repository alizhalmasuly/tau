from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, max_length=500)
    home_region = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"