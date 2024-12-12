from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.exceptions import ValidationError


# Create your models here.

class MyUserManager(BaseUserManager):

    def create_user(self, phone, full_name, password=None, **extra_fields):
        """
        Create and return a regular user with the given phone, full_name, and password.
        """
        if not phone:
            raise ValueError("The phone number must be set")
        if not full_name:
            raise ValueError("The full name must be set")

        extra_fields.setdefault('is_active', True)  # Default to active users
        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password=None, **extra_fields):
        """
        Create and return a superuser with the given phone, full_name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone=phone, full_name=full_name, password=password, **extra_fields)

    def get_by_natural_key(self, phone):
        return self.get(**{self.model.USERNAME_FIELD: phone})


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()
    phone = models.CharField(max_length=13, unique=True, null=False, blank=False, verbose_name='user phone')
    #email_active_code = models.CharField(max_length=100, verbose_name='email active code', blank=True, null=True)
    activation_code_expiration = models.DateTimeField(null=True, blank=True)
    full_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='full name')
    is_active = models.BooleanField(default=True, verbose_name='is user active?')
    is_staff = models.BooleanField(default=False, verbose_name='is user staff?')
    avatar = models.ImageField(upload_to='images/profile_images', verbose_name='profile avatar', null=True, blank=True)

    Content_Rating = models.FloatField(default=0.0)  # Field to store the user's rating
    View_Rating = models.FloatField(default=0.0)  # Field to store the user's rating
    Total_Rating = models.FloatField(default=0.0)  # Field to store the user's rating

    First_login = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']




    class Meta:
        verbose_name = 'Uesr'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        # Update Total_Rating to be the sum of Content_Rating and View_Rating
        self.Total_Rating = round(self.Content_Rating + self.View_Rating,1)
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.phone

    def clean_email(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("کاربر با این شماره وجود دارد!")
        return phone

class DiscountCode(models.Model):
    code = models.CharField(max_length=5, unique=True, blank=True, null=True)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_valid = models.BooleanField(default=True)
    user = models.ManyToManyField(User, related_name="DiscoountCodes")

    class Meta:
        verbose_name = 'Discount Code table'

    def __str__(self):
        return f'discount code is : {self.discount_percent}'

    def save(self, *args, **kwargs):
        self.code = get_random_string(5)
        super().save(*args, **kwargs)


class Province(models.Model):
    name = models.CharField(max_length=225, default='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        ordering = ['name']


class City(models.Model):
    province = models.ForeignKey(
        Province,
        verbose_name = 'province',
        related_name = 'cities',
        on_delete = models.CASCADE
    )
    name = models.CharField(max_length=255, default='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name= 'Address table'


    def __str__(self):
        return f'User: {self.user}, City: {self.City}'