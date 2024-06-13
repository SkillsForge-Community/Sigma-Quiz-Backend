from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = User
