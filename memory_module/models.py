from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from category_module.models import SubCategory
from account_module.models import User


# Create your models here.

class memory(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    main_picture = models.OneToOneField('memory_pictures', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='main_picture_of')

    def __str__(self):
        return self.title


class memory_pictures(models.Model):
    memory = models.ForeignKey(memory, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='images/memory_images', null=False, blank=False)

    def __str__(self):
        return f'memory title:{self.memory.title}, user:{self.memory.user.email}'


# Set first picture as main picture for memory model(if user saved any picture!!)
@receiver(post_save, sender=memory_pictures)
def set_main_picture(sender, instance, created, **kwargs):
    if created and not instance.memory.main_picture and instance.memory.pictures.filter(pk=instance.pk).exists():
        instance.memory.main_picture = instance
        instance.memory.save()


class memory_comments(models.Model):
    title = models.CharField(max_length=300)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    memory = models.ForeignKey(memory, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.title}, user:{self.user}, memory:{self.memory}'
