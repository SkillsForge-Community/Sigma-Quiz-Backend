from rest_framework import serializers
from quiz.models import SchoolRegisteredForQuiz, Quiz
from school.serializers import SchoolSerializer

# from sigma.round.models import Round


class QuizSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "noofrounds",
            "date",
            "created_at",
        ]


class SchoolForQuizSerializer(serializers.ModelSerializer):
    quizreg = QuizSerializer(read_only=True)
    schoolreg = SchoolSerializer(read_only=True)

    class Meta:
        model = SchoolRegisteredForQuiz
        fields = ["quizreg", "schoolreg"]
