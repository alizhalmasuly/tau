from django.urls import path

from .views import forecast, weather_data

app_name = "weather"
urlpatterns = [path("", forecast, name="forecast"), path("api/", weather_data, name="api")]