from django.contrib import admin
from . import models
# Register your models here.
class VideoAdmin(admin.ModelAdmin):

    list_display = ['title', 'video_category']

class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(models.video, VideoAdmin)
admin.site.register(models.VideoCategory, VideoCategoryAdmin)

