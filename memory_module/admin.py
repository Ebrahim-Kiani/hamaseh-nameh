from django.contrib import admin
from . import models
# Register your models here.
class MemoryAdmin(admin.ModelAdmin):

    list_display = ['title', 'user', 'status']
    list_editable = ['status']

class MemoryPicturesAdmin(admin.ModelAdmin):

    list_display = ['memory',]


admin.site.register(models.memory, MemoryAdmin)
admin.site.register(models.memory_pictures, MemoryPicturesAdmin)
admin.site.register(models.memory_comments)


