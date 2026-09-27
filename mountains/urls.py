from django.urls import path

from . import views

app_name = "mountains"
urlpatterns = [
    path("api/search/", views.mountain_search_api, name="search_api"),
    path("api/trails/", views.mountain_trails_api, name="trails_api"),
    path("", views.mountain_list, name="list"),
    path("prepare/", views.prepare, name="prepare"),
    path("<slug:slug>/", views.mountain_detail, name="detail"),
    path("<slug:slug>/save/", views.toggle_saved, name="toggle_saved"),
]