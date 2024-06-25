from django.db import models

from sigma.quiz.models import Quiz
from sigma.school.models import School
from sigma.utils.base_class import BaseModel


class Round(BaseModel):

    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="rounds")
    name = models.CharField(max_length=100)
    round_number = models.PositiveIntegerField()
    no_of_questions = models.PositiveIntegerField()
    no_of_schools = models.PositiveIntegerField()
    marks_per_question = models.PositiveIntegerField()
    marks_per_bonus_question = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "round_number"],
                name="unique_school_quiz_round",
            )
        ]

    @property
    def quizId(self):
        return self.quiz.id

    def __str__(self):
        return f"Name: {self.name} | Round No: {self.round_number}"


class Question(BaseModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="questions")
    question_number = models.PositiveIntegerField()
    correct_answer = models.CharField(max_length=255, null=True, blank=True)
    answered_by = models.CharField(max_length=100, null=True, blank=True)
    bonus_to = models.CharField(max_length=100, null=True, blank=True)

    @property
    def roundId(self):
        return self.round.id

    def __str__(self):
        return f"Question: {self.question_number}, Round: {self.round.round_number})"


class RoundForSchool(BaseModel):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="round_for_schools")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="rounds_for_school")

    @property
    def school_id(self):
        return self.school.id

    @property
    def round_id(self):
        return self.round.id

    def __str__(self):
        return f"{self.school.name} quiz for {self.round.round_number}"
