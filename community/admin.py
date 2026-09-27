from django.contrib import admin

from .models import Comment, Story


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "mountain", "hike_date", "created_at")
    list_filter = ("difficulty", "hike_date")
    search_fields = ("title", "description", "author__username")
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("story", "author", "created_at")
    search_fields = ("body", "author__username", "story__title")