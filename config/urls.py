from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path("", include("core.urls")),
    path("mountains/", include("mountains.urls")),
    path("accounts/", include("accounts.urls")),
    path("stories/", include("community.urls")),
    path("weather/", include("weather.urls")),
    path("assistant/", include("ai_assistant.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)