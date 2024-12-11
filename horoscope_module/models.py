from django.db import models


# Create your models here.

class Horoscope(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="عنوان تفأل")
    description = models.TextField(null=True, blank=True,verbose_name="متن" )

    class Meta:
        verbose_name = 'جدول فال ها'
        verbose_name_plural = 'فال ها'
