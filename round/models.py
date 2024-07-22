from django.db import models
from django.db import models
from school.basemodel import UUIDModel
from quiz.models import SchoolRegisteredForQuiz
from school.models import School

# from sigman.users.models im
# from school.models import School

# from sigma.utils.base_class import BaseModel


class Round(UUIDModel):
    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    quizround = models.ForeignKey(
        SchoolRegisteredForQuiz,
        on_delete=models.CASCADE,
        related_name="rounds",
    )
    name = models.CharField(max_length=100)
    round_number = models.PositiveIntegerField()
    no_of_questions = models.PositiveIntegerField()
    no_of_schools = models.PositiveIntegerField()
    marks_per_question = models.PositiveIntegerField()
    marks_per_bonus_question = models.PositiveIntegerField()


class Question(UUIDModel):
    roundquestion = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_number = models.PositiveIntegerField(null=True)
    questionfield = models.CharField(max_length=255, null=True, blank=True)
    correct_answer = models.CharField(max_length=255, null=True, blank=True)
    ans_status = models.BooleanField(
        default=False,
    )
    answered_by = models.ForeignKey(School, null=True, on_delete=models.CASCADE)


class bonus(UUIDModel):
    fromschool = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="fromschool",
    )
    toschool = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="toschool",
    )
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()


class submission(UUIDModel):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )
    roundsub = models.ForeignKey(Round, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()


# Create your models here.
