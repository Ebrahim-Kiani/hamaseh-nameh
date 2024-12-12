from django.contrib import admin
from . import models


# Register your models here.
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'user_full_name', 'status', 'SubCategory']
    list_filter = ['SubCategory']
    list_editable = ['status']

    def user_full_name(self, obj):
        return obj.user.full_name if obj.user and hasattr(obj.user, 'full_name') else "—"

    user_full_name.short_description = 'User Full Name'


class MemoryPicturesAdmin(admin.ModelAdmin):
    list_display = ['memory', ]


admin.site.register(models.memory, MemoryAdmin)
admin.site.register(models.memory_pictures, MemoryPicturesAdmin)
admin.site.register(models.memory_comments)
