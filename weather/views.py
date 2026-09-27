from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from urllib.error import URLError

from mountains.models import Mountain
from .services import find_place, get_weather

def forecast(request):
    selected = Mountain.objects.filter(slug=request.GET.get("route", "")).first() or Mountain.objects.first()
    return render(request, "weather/forecast.html", {"selected": selected})


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


@require_GET
def place_search(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"error": "query_too_short"}, status=400)
    try:
        results = find_place(query, (request.LANGUAGE_CODE or "ru").split("-")[0])
    except (URLError, TimeoutError, OSError, ValueError):
        return JsonResponse({"error": "search_unavailable"}, status=502)
    if results is None:
        return JsonResponse({"error": "rate_limited"}, status=429)
    return JsonResponse({"results": results})
