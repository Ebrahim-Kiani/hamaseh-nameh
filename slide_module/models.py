from django.db import models

# Create your models here.

class slide(models.Model):
    title = models.CharField(max_length=50, null=True, blank=False)
    image = models.ImageField(upload_to='images/slides', verbose_name='profile avatar', null=True, blank=True)
    link = models.URLField(max_length=300, verbose_name="Web Link", blank=True, null=True)