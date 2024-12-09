from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from category_module.models import SubCategory
from account_module.models import User


# Create your models here.

class memory(models.Model):
    ISFAHAN_COUNTIES = [
        ("سراسر کشور", "سراسر کشور"),
        ("آران و بیدگل", "آران و بیدگل"),
        ("اردستان", "اردستان"),
        ("اصفهان", "اصفهان"),
        ("برخوار", "برخوار"),
        ("بوئین و میاندشت", "بوئین و میاندشت"),
        ("تیران و کرون", "تیران و کرون"),
        ("چادگان", "چادگان"),
        ("خمینی‌شهر", "خمینی‌شهر"),
        ("خوانسار", "خوانسار"),
        ("خور و بیابانک", "خور و بیابانک"),
        ("دهاقان", "دهاقان"),
        ("سمیرم", "سمیرم"),
        ("شاهین‌شهر و میمه", "شاهین‌شهر و میمه"),
        ("شهرضا", "شهرضا"),
        ("فریدن", "فریدن"),
        ("فریدون‌شهر", "فریدون‌شهر"),
        ("فلاورجان", "فلاورجان"),
        ("کاشان", "کاشان"),
        ("گلپایگان", "گلپایگان"),
        ("لنجان", "لنجان"),
        ("مبارکه", "مبارکه"),
        ("نایین", "نایین"),
        ("نجف‌آباد", "نجف‌آباد"),
        ("نطنز", "نطنز"),
    ]

    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    main_picture = models.OneToOneField(
        'memory_pictures', on_delete=models.SET_NULL, null=True, blank=True, related_name='main_picture_of'
    )
    status = models.BooleanField(null=True, blank=True, default=None)
    average_rating = models.FloatField(default=0.0)
    county = models.CharField(max_length=20, choices=ISFAHAN_COUNTIES, null=False, blank=False, default="سراسر کشور")


    def save(self, *args, **kwargs):
        # Calculate the average rating before saving the object
        if self.pk:  # Only calculate for existing objects (not new ones)
            self.average_rating = self.ratings.aggregate(Avg('value'))['value__avg'] or 0.0

        super(memory, self).save(*args, **kwargs)  # Call the parent class save method

    def __str__(self):
        return self.title


class Rating(models.Model):
    memory = models.ForeignKey(memory, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveIntegerField()  # Assume 1 to 5
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('memory', 'user')

    def save(self, *args, **kwargs):
        # First, save the rating object
        super(Rating, self).save(*args, **kwargs)

        # Now, update the average rating of the associated memory object
        self.memory.save()

class memory_pictures(models.Model):
    memory = models.ForeignKey(memory, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='images/memory_images', null=False, blank=False)

    def __str__(self):
        return f'memory title:{self.memory.title}, user:{self.memory.user.phone}'


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


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    memory = models.ForeignKey('memory', on_delete=models.CASCADE, related_name='bookmarked_by')


    class Meta:
        unique_together = ('user', 'memory')  # Prevent duplicate bookmarks

    def __str__(self):
        return f"{self.user} bookmarked {self.memory}"