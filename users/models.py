import uuid
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,AbstractUser
)
from django.utils import timezone


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField( max_length=50)
    email = models.EmailField(max_length=255, unique=True,)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='images/profile/',null=False)
    role=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=500)
    expiry_date = models.DateTimeField(null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_out_of_credits(self):
        "Is the user out  of credits?"
        return self.credits > 0
    
    def save(self, *args, **kwargs):
        super(MyUser, self).save(*args, **kwargs)
        if self.profile:
            profile = Image.open(self.profile.path)
            output_size = (100, 100)
            profile = profile.resize(output_size)
            profile.save(self.profile.path)


# Create your models here.


class news(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to='images')
    vedio = models.FileField(upload_to='videos_uploaded', null=True)
    text = models.CharField(max_length=2000)
