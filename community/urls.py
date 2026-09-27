from django.urls import path

from . import views

app_name = "community"
urlpatterns = [
    path("", views.story_list, name="list"),
    path("new/", views.create_story, name="create"),
    path("<int:pk>/", views.story_detail, name="detail"),
    path("<int:pk>/like/", views.toggle_like, name="like"),
]