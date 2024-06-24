from rest_framework import serializers

from sigma.quiz.models import SchoolRegisteredForQuiz
from sigma.round.models import Round

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

    quiz = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()
    school_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = SchoolRegisteredForQuiz
        fields = [
            "school_id",
            "quizId",
            "schoolId",
            "school",
            "quiz",
            "id",
            "created_at",
            "updated_at",
        ]

    def get_quiz(self, instance):
        quiz_obj = instance.quiz
        rounds = quiz_obj.rounds.all()
        rounds_data = RoundSerializer(rounds, many=True).data

        return {
            "id": quiz_obj.id,
            "year": quiz_obj.year,
            "title": quiz_obj.title,
            "description": quiz_obj.description,
            "date": quiz_obj.date,
            "rounds": rounds_data,
        }

    def get_school(self, instance):
        school_obj = instance.school
        return {
            "id": school_obj.id,
            "name": school_obj.name,
            "state": school_obj.state,
            "address": school_obj.address,
        }

    def create(self, validated_data):
        """Registers school for quiz"""
        register_school_for_quiz_obj = SchoolRegisteredForQuiz.objects.create(
            quiz_id=self.context["quiz_id"], school_id=validated_data["school_id"]
        )

        return register_school_for_quiz_obj

    def to_representation(self, instance):

        request = self.context.get("request", None)
        fields = list(self.Meta.fields)
        representation = super().to_representation(instance)

        if request and request.method in ["GET", "DELETE"]:
            quiz_data = representation.get("quiz", {})
            quiz_data.pop("rounds", None)
            representation["quiz"] = quiz_data

            fields = [
                "id",
                "quizId",
                "schoolId",
                "quiz",
                "school",
            ]

        return {field: representation[field] for field in fields if field in representation}
