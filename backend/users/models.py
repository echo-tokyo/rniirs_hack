# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=30, unique=True, verbose_name='логин')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'login'

    objects = CustomUserManager()
