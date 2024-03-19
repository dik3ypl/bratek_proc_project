from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    verified_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    def __str__(self):
        return self.email
