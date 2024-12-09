from django.contrib import admin
from . import models
# Register your models here.
class SlideAdmin(admin.ModelAdmin):

    list_display = ['title', 'link']


admin.site.register(models.slide, SlideAdmin)
