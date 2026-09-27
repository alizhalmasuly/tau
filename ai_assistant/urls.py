from django.urls import path

from .views import chat, chat_page

app_name = "ai_assistant"
urlpatterns = [path("", chat_page, name="chat_page"), path("chat/", chat, name="chat")]