from datetime import date

from django.db import models
from school.basemodel import UUIDModel

from school.models import School

# from utils.base_class import BaseModel


class Quiz(UUIDModel):
    # year = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255, null=True, blank=True)
    date = models.DateField(default=date.today)
    noofrounds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class SchoolRegisteredForQuiz(UUIDModel):
    quizreg = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )
    schoolreg = models.ForeignKey(School, on_delete=models.CASCADE)


