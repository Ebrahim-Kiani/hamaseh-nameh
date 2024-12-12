from django.db import models


# Create your models here.

class Introduction(models.Model):
    software_name = models.CharField(max_length=300, blank=True, null=True)
    software_description = models.TextField(blank=True, null=True)
    apk_download = models.FileField(upload_to='apk_file')
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
