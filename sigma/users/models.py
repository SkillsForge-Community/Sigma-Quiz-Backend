from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from sigma.utils.base_class import BaseModel


class User(AbstractBaseUser, BaseModel, PermissionsMixin):

    ROLE_CHOICES = [
        ("quiz-master", "quiz-master"),
        ("adhoc", "adhoc"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    roles = models.CharField(max_length=20, choices=ROLE_CHOICES, default="adhoc")

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "roles"]

    def __str__(self):
        return self.email
