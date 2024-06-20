from django.db import models

from sigma.school.models import School
from sigma.utils.base_class import BaseModel


class Quiz(BaseModel):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255, null=True, blank=True)
    date = models.DateField(unique=True)

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return f"Title: {self.title} | Date: {self.date}"


class SchoolRegisteredForQuiz(BaseModel):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="schoolquiz")
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="registered_school_id"
    )

    def __str__(self) -> str:
        return f"{self.school.name} is Registerd"
