from django.db import models
from school.basemodel import UUIDModel

# from sigma.utils.base_class import BaseModel


class School(UUIDModel):

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# Create your models here.
# Create your models here.
