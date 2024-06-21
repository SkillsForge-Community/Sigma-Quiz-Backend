from datetime import datetime

from factory.django import DjangoModelFactory

from sigma.quiz.models import Quiz, SchoolRegisteredForQuiz


class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz

    date = datetime.today()


class SchoolRegisteredForQuizFactory(DjangoModelFactory):

    class Meta:
        model = SchoolRegisteredForQuiz
