from factory.django import DjangoModelFactory

from sigma.quiz.models import Quiz, SchoolRegisteredForQuiz


class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz


class SchoolRegisteredForQuizFactory(DjangoModelFactory):

    class Meta:
        model = SchoolRegisteredForQuiz
