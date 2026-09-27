from django.urls import path

from .views import forecast, place_search, weather_data

app_name = "weather"
urlpatterns = [path("", forecast, name="forecast"), path("api/", weather_data, name="api"), path("search/", place_search, name="search")]
