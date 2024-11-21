from django.db import models


# Create your models here.

class MainCategory(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/categories_images', null=False, blank=False)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/subcategories_images', null=True, blank=True)
    MainCategory = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return self.title
