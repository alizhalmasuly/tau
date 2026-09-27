from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from mountains.models import Mountain
from .services import get_weather

def forecast(request):
    mountains = Mountain.objects.all()
    selected = mountains.filter(slug=request.GET.get("route", "")).first() or mountains.first()
    return render(request, "weather/forecast.html", {"mountains": mountains, "selected": selected})


@require_GET
def weather_data(request):
    try:
        latitude = float(request.GET.get("lat", ""))
        longitude = float(request.GET.get("lon", ""))
    except (TypeError, ValueError):
        return JsonResponse({"available": False, "error": "invalid_coordinates"}, status=400)
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        return JsonResponse({"available": False, "error": "invalid_coordinates"}, status=400)
    return JsonResponse(get_weather(
        latitude=latitude,
        longitude=longitude,
        language=(request.LANGUAGE_CODE or "ru").split("-")[0],
    ))