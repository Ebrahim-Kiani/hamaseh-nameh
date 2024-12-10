from django.db import models


# Create your models here.
class VideoCategory(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='images/subcategories_images', null=True, blank=True)
    def __str__(self):
        return self.title

class video(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="title")
    video_link = models.URLField(max_length=300, null=True, blank=True, verbose_name="video link")
    image = models.ImageField(upload_to='images/videos_images', null=False, blank=False, verbose_name="image")
    video_category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, blank=False, null=False)

