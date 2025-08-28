from django.contrib import admin

from .models import Quote, Source, Vote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "text",
        "weight",
        "views",
        "likes_count",
        "dislikes_count",
    )

    def likes_count(self, obj):
        return obj.likes_count()

    likes_count.short_description = "Лайки"

    def dislikes_count(self, obj):
        return obj.dislikes_count()

    dislikes_count.short_description = "Дизлайки"


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("category", "name")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "user", "value")
