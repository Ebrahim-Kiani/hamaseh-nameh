from django.db import models
from account_module.models import User


# Create your models here.

class ContactUs(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    is_awnsered = models.BooleanField(default=False)
    admin_awnser = models.TextField(blank=True, null=True)


class UserMessages(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)


