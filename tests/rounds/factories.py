from factory import SubFactory
from factory.django import DjangoModelFactory

from sigma.round.models import Round
from tests.quiz.factories import QuizFactory


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    quiz = SubFactory(QuizFactory)
    round_number = 3
    no_of_questions = 3
    no_of_schools = 3
    marks_per_question = 4
    marks_per_bonus_question = 3
