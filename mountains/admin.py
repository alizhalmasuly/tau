from django.contrib import admin

from .models import Equipment, GearCheck, Mountain, SavedHike


@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "altitude", "difficulty", "is_featured")
    list_filter = ("difficulty", "is_featured")
    search_fields = ("name", "location")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "essential", "sort_order")
    list_filter = ("category", "essential")


admin.site.register((GearCheck, SavedHike))