from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class RussianDefaultLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        selected = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        supported = {code for code, _ in settings.LANGUAGES}
        language = selected if selected in supported else settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = language