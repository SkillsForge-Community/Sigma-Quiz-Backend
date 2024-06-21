from rest_framework import serializers

from sigma.quiz.models import SchoolRegisteredForQuiz
from sigma.round.models import Round
from sigma.school.serializers import SchoolSerializer

from .models import Quiz


class RoundSerializer(serializers.ModelSerializer):
    quizId = serializers.UUIDField(source="quiz.id", read_only=True)

    class Meta:
        model = Round
        fields = [
            "id",
            "quizId",
            "name",
            "round_number",
            "no_of_questions",
            "no_of_schools",
            "marks_per_question",
            "marks_per_bonus_question",
        ]


class QuizSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "year",
            "title",
            "description",
            "date",
            "id",
            "created_at",
            "updated_at",
        ]

    def get_year(self, obj):
        return str(obj.date.year)

    def to_representation(self, instance):
        request = self.context.get("request")

        if not request or request.method in ["GET", "PUT"]:
            fields = ["id", "year", "title", "description", "date"]
        else:
            fields = self.Meta.fields

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}


class SchoolForQuizSerializer(serializers.ModelSerializer):
    quizId = serializers.UUIDField(source="quiz.id", read_only=True)
    schoolId = serializers.UUIDField(source="school.id", read_only=True)

    quiz = QuizSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = SchoolRegisteredForQuiz
        fields = [
            "id",
            "schoolId",
            "quizId",
            "quiz",
            "school",
            "school_id",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Registers school for quiz"""
        register_school_for_quiz_obj = SchoolRegisteredForQuiz.objects.create(
            quiz_id=self.context["quiz_id"], school_id=validated_data["school_id"]
        )

        return register_school_for_quiz_obj

    def to_representation(self, instance):

        if not self.context.get("request"):
            self.Meta.fields = [
                "id",
                "schoolId",
                "quizId",
                "quiz",
                "school",
                "school_id",
            ]

        data = super().to_representation(instance)

        quiz = Quiz.objects.filter(id=data["quizId"]).first()
        data["quiz"]["rounds"] = RoundSerializer(quiz.rounds.all(), many=True).data

        return data
