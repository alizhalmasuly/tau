from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, False) if dictionary else False


@register.filter
def get_difficulty(translations, value):
    label = translations.get("difficulty", "Сложность")
    language = "ru" if label == "Сложность" else "kk" if label == "Қиындық" else "en"
    choices = {
        "ru": {"easy": "Лёгкий", "moderate": "Средний", "hard": "Сложный"},
        "kk": {"easy": "Жеңіл", "moderate": "Орташа", "hard": "Қиын"},
        "en": {"easy": "Easy", "moderate": "Moderate", "hard": "Challenging"},
    }
    return choices[language].get(value, value)