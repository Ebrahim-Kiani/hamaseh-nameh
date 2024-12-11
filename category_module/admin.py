from django.contrib import admin
from . import models
# Register your models here.

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'MainCategory']
    list_editable = ['MainCategory']

admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.MainCategory)