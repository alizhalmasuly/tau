import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from mountains.models import Mountain

from .services import recommend_gear


def chat_page(request):
    return render(request, "ai_assistant/chat.html", {
        "mountains": Mountain.objects.all(),
        "difficulty_choices": Mountain.DIFFICULTY_CHOICES,
    })


@require_POST
def chat(request):
    try:
        body = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid request"}, status=400)
    message = str(body.get("message", "")).strip()[:2000]
    if not message:
        return JsonResponse({"error": "Message is required"}, status=400)
    try:
        latitude = float(body.get("latitude"))
        longitude = float(body.get("longitude"))
    except (TypeError, ValueError):
        latitude = longitude = None
    if latitude is not None and not -90 <= latitude <= 90:
        latitude = None
    if longitude is not None and not -180 <= longitude <= 180:
        longitude = None
    reply = recommend_gear(
        message, mountain=str(body.get("mountain", ""))[:120], season=str(body.get("season", "summer"))[:30],
        duration=str(body.get("duration", "5"))[:30], difficulty=str(body.get("difficulty", "moderate"))[:30],
        language=(request.LANGUAGE_CODE or "ru").split("-")[0], latitude=latitude, longitude=longitude,
    )
    return JsonResponse({"reply": reply})