from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.exceptions import ValidationError


# Create your models here.

class MyUserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not full_name:
            raise ValueError('Users must have a full name')

        user = self.model(

            email=self.normalize_email(email),

            full_name=full_name,

        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password=None):

        user = self.create_user(

            email=self.normalize_email(email),

            password=password,

            full_name=full_name,

        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()
    email = models.EmailField(unique=True, null=False, blank=False, verbose_name='user email')
    email_active_code = models.CharField(max_length=100, verbose_name='email active code', blank=True, null=True)
    activation_code_expiration = models.DateTimeField(null=True, blank=True)
    full_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='full name')
    is_active = models.BooleanField(default=False, verbose_name='is user active?')
    is_staff = models.BooleanField(default=False, verbose_name='is user staff?')
    avatar = models.ImageField(upload_to='images/profile_images', verbose_name='profile avatar', null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'User table'

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert email to lowercase
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Uesr'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

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