from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from community.models import Comment, Story
from mountains.models import Equipment, Mountain


ROUTES = [
    ("Кок-Жайляу", "kok-zhailau", 2251, "easy", 4, 8, "Июнь — октябрь", "Зелёное плато над городом с широкими панорамами.", "Популярный маршрут с пологим набором высоты через лес и альпийские луга.", "Выходите пораньше в выходные; на плато часто дует ветер.", "photo-1470770841072-f978cf4d019e", True),
    ("Пик Фурманова", "furmanovka", 3053, "moderate", 6, 12, "Июль — сентябрь", "Панорамная вершина и любимый маршрут алматинцев.", "Тропа проходит через лес и альпийские луга к открытому склону с видами на город.", "На верхнем участке нет тени. Возьмите воду, кепку и тёплый слой.", "photo-1464822759023-fed622ff2c3b", True),
    ("Большой Алматинский пик", "big-almaty-peak", 3681, "hard", 9, 18, "Июль — август", "Высотный маршрут к суровой панораме над Большим Алматинским озером.", "Серьёзный выход с длинным подходом и участками осыпи. Требует хорошей формы и акклиматизации.", "Проверьте доступ у местных служб. Не выходите в одиночку и следите за самочувствием.", "photo-1464278533981-50106e6176b1", True),
    ("Кумбель", "kumbel", 3200, "moderate", 7, 14, "Июль — сентябрь", "Классический гребневой маршрут с видами на горные долины.", "Лесные участки, альпийские поляны и каменистая вершина с панорамой хребта.", "На гребне держитесь подальше от карнизов и разворачивайтесь при грозе.", "photo-1454496522488-7a8e488e8606", True),
    ("Пик Букреева", "bukreev-peak", 3010, "hard", 8, 15, "Июль — сентябрь", "Тихий маршрут к выразительной вершине у ледниковых склонов.", "Крутая горная тропа с каменистым рельефом требует уверенного шага.", "Сверьтесь с актуальным состоянием троп и не начинайте спуск в темноте.", "photo-1519681393784-d120267933ba", False),
    ("Плато Медеу", "medeu-plateau", 1691, "easy", 3, 5, "Май — октябрь", "Короткая прогулка с видом на ледовый комплекс и окружающие вершины.", "Доступный маршрут для знакомства с горным воздухом и спокойного семейного выхода.", "Возьмите воду и лёгкую куртку: погода у Медеу меняется быстро.", "photo-1500530855697-b586d89ba3ee", False),
    ("Три брата", "tri-brata", 2860, "moderate", 5.5, 10, "Июнь — сентябрь", "Три характерные скальные вершины над ущельем Алмарасан.", "Живописная тропа чередует лес и открытые склоны. Финальный подъём требует хорошей обуви.", "На открытых участках не выходите при сильном ветре и грозе.", "photo-1464278533981-50106e6176b1", False),
    ("Пик Панорама", "panorama-peak", 3270, "hard", 8, 16, "Июль — сентябрь", "Длинный выход на обзорный гребень над городом.", "Продолжительный подъём по разному рельефу с видом на главный хребет.", "Стартуйте рано, оставьте близким план маршрута и предусмотрите время на спуск.", "photo-1519681393784-d120267933ba", False),
]

ROUTE_COORDINATES = {
    "kok-zhailau": (43.1323, 77.0435), "furmanovka": (43.1590, 77.1030),
    "big-almaty-peak": (43.0530, 77.0620), "kumbel": (43.1170, 77.0460),
    "bukreev-peak": (43.0840, 77.0750), "medeu-plateau": (43.1570, 77.0580),
    "tri-brata": (43.1020, 77.0560), "panorama-peak": (43.1070, 77.0500),
}

GEAR = [
    ("Треккинговые ботинки", "clothing", True), ("Водонепроницаемая куртка", "clothing", True),
    ("Термобельё или тёплый слой", "clothing", True), ("Перчатки", "clothing", False), ("Кепка или шапка", "clothing", True),
    ("Карта маршрута", "navigation", True), ("Компас", "navigation", False), ("Заряженный телефон / GPS", "navigation", True),
    ("Вода (от 2 л)", "food", True), ("Еда для маршрута", "food", True), ("Перекус", "food", True),
    ("Аптечка первой помощи", "safety", True), ("Фонарик и запас питания", "safety", True),
    ("Пауэрбанк", "safety", True), ("Аварийный свисток", "safety", False),
    ("Палатка", "camping", False), ("Спальный мешок", "camping", False), ("Туристический коврик", "camping", False),
]

TRIPS = [
    ("Первый рассвет на Фурмановке", "furmanovka", 8, "Вышли затемно, чтобы встретить солнце над городом. Последний подъём оказался круче, чем ожидали, но панорама с вершины стоила каждого шага.", "Начинайте до рассвета только с хорошим фонарём. На открытом склоне пригодятся ветровка и запас воды.", "Ботинки, ветровка, 2 л воды, аптечка, налобный фонарь", "photo-1500530855697-b586d89ba3ee"),
    ("Кок-Жайляу без спешки", "kok-zhailau", 13, "Мы выбрали будний день и пошли в своём темпе. После лесной части открылись широкие луга, а у ручья устроили длинную остановку с чаем.", "После дождя на лесной тропе скользко. Возьмите термос и небольшой коврик для привала.", "Ботинки, вода, термос, дождевик", "photo-1470770841072-f978cf4d019e"),
    ("Выше облаков: Кумбель", "kumbel", 20, "Ветер на гребне разогнал облака и открыл весь хребет. Подъём длинный, но маршрут хорошо читается с заранее скачанной картой.", "Скачайте карту заранее и возьмите тёплый слой даже летом. Проверяйте грозовой прогноз.", "Ботинки, офлайн-карта, ветровка, 2.5 л воды", "photo-1454496522488-7a8e488e8606"),
    ("Тихое утро над Медеу", "medeu-plateau", 28, "Короткий выход оказался лучшим способом провести свободное утро. На тропе почти никого, воздух прохладный, а город просыпался далеко внизу.", "Возьмите лёгкий слой одежды: утром прохладнее, чем кажется у подножия.", "Лёгкие ботинки, вода, ветровка", "photo-1500530855697-b586d89ba3ee"),
    ("Длинный день у Большого Алматинского пика", "big-almaty-peak", 35, "Это был самый длинный выход сезона. Мы заранее проверили доступ, стартовали рано и несколько раз оценивали самочувствие группы. До главной точки дошли не все, и это было правильное решение.", "Высота требует уважения. Планируйте запасной вариант, не торопитесь и разворачивайтесь при первых симптомах.", "Высотные ботинки, каска, навигация, аптечка, запас воды", "photo-1464822759023-fed622ff2c3b"),
]


class Command(BaseCommand):
    help = "Create sample mountains, equipment, stories and comments."

    def handle(self, *args, **options):
        mountains = {}
        for route in ROUTES:
            name, slug, altitude, difficulty, hours, distance, season, short, description, safety, photo, featured = route
            mountain, _ = Mountain.objects.update_or_create(slug=slug, defaults={
                "name": name, "location": "Заилийский Алатау · Алматы", "altitude": altitude,
                "latitude": ROUTE_COORDINATES[slug][0], "longitude": ROUTE_COORDINATES[slug][1],
                "difficulty": difficulty, "duration_hours": hours, "distance_km": distance,
                "best_season": season, "short_description": short, "description": description,
                "safety_notes": safety, "image_url": f"https://images.unsplash.com/{photo}?auto=format&fit=crop&w=1200&q=85",
                "is_featured": featured,
            })
            mountains[slug] = mountain

        for index, (name, category, essential) in enumerate(GEAR):
            Equipment.objects.update_or_create(name=name, defaults={"category": category, "essential": essential, "sort_order": index})

        users = []
        for username in ("Aida", "Timur", "Mira", "Daniyar", "Alina"):
            user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username.lower()}@tau.example"})
            if created:
                user.set_password("tau-demo-2026")
                user.save()
            users.append(user)

        stories = []
        for index, (title, slug, days_ago, description, tips, equipment, photo) in enumerate(TRIPS):
            mountain = mountains[slug]
            story, _ = Story.objects.update_or_create(title=title, defaults={
                "author": users[index], "mountain": mountain, "hike_date": date.today() - timedelta(days=days_ago),
                "difficulty": mountain.difficulty, "description": description, "useful_tips": tips,
                "equipment_used": equipment, "cover_url": f"https://images.unsplash.com/{photo}?auto=format&fit=crop&w=1400&q=85",
            })
            stories.append(story)

        comments = [
            (0, 1, "Отличный совет про дополнительную воду, на открытом склоне она точно нужна."),
            (1, 2, "Подскажите, есть ли на маршруте удобное место для привала у ручья?"),
            (2, 3, "Офлайн-карта очень выручает, спасибо, что напомнили."),
            (4, 0, "Очень здравое решение не гнаться за вершиной. Безопасного вам сезона!"),
        ]
        for story_index, user_index, body in comments:
            Comment.objects.get_or_create(story=stories[story_index], author=users[user_index], body=body)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Mountain.objects.count()} mountains, {Equipment.objects.count()} gear items and {Story.objects.count()} stories."
        ))