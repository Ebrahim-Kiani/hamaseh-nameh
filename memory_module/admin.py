from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.memory)
admin.site.register(models.memory_pictures)
admin.site.register(models.memory_comments)

