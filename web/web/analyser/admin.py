from django.contrib import admin

from web.analyser.models import Creator, VideoRecord


@admin.register(VideoRecord)
class VideoRecordAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "time_watched"]
    search_fields = ["title", "creator"]


@admin.register(Creator)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["name", "times_watched"]
    ordering = ("-times_watched",)
    search_fields = ["name"]
