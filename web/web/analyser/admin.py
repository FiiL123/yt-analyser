from django.contrib import admin

from web.analyser.models import VideoRecord


@admin.register(VideoRecord)
class VideoRecordAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "time_watched"]
