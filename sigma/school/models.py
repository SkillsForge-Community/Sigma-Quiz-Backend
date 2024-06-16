from django.db import models

from sigma.utils.base_class import BaseModel


class School(BaseModel):

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
