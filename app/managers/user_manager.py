from django.db import models
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            phone=phone,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
