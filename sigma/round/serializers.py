from rest_framework import serializers

from sigma.quiz.models import Quiz, SchoolRegisteredForQuiz
from sigma.quiz.serializers import SchoolForQuizSerializer
from sigma.round.models import Round, RoundForSchool
from sigma.school.models import School
from sigma.school.serializers import SchoolSerializer


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


class QuizRoundSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    quizId = serializers.UUIDField()

    class Meta:
        model = Round
        fields = [
            "quizId",
            "name",
            "round_number",
            "no_of_questions",
            "no_of_schools",
            "marks_per_question",
            "marks_per_bonus_question",
            "quiz",
            "id",
            "created_at",
            "updated_at",
            "questions",
        ]

    def get_quiz(self, instance):
        quiz_obj = instance.quiz
        return {
            "id": quiz_obj.id,
            "year": quiz_obj.year,
            "title": quiz_obj.title,
            "description": quiz_obj.description,
            "date": quiz_obj.date,
        }

    def validate(self, data):

        quiz_id = data.get("quizId")
        round_number = data.get("round_number")

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "Sigma Quiz with this id does not exis",
                    "error": "Not Found",
                    "statusCode": 404,
                }
            )
        if Round.objects.filter(quiz=quiz, round_number=round_number).exists():
            raise serializers.ValidationError(
                {
                    "message": f'Key ("quizId", round_number)=({quiz_id}, '
                    f"{round_number}) already exists.",
                    "error": "Conflict",
                    "statusCode": 409,
                }
            )

        return data

    def to_representation(self, instance):
        request = self.context.get("request")
        if request.method in ["GET"]:
            fields = [
                "id",
                "quizId",
                "name",
                "round_number",
                "no_of_questions",
                "no_of_schools",
                "marks_per_question",
                "marks_per_bonus_question",
                "schoolParticipations",
                "questions",
            ]
        else:
            fields = self.Meta.fields

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}


class RoundForSchoolSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    roundId = serializers.UUIDField(source="round.id", read_only=True)

    round = RoundSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    school_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = RoundForSchool
        fields = ["id", "roundId", "round", "school", "school_id", "created_at", "updated_at"]

    def validate(self, attrs):
        """validates round for school"""
        if not self.is_school_registered_for_quiz(attrs["school_id"]):
            raise serializers.ValidationError("School Not Registered for Quiz", code="Not Found")

        return attrs

    def is_school_registered_for_quiz(self, school_id):
        """checks if school has registered for quiz"""

        return SchoolRegisteredForQuiz.objects.filter(school_id=school_id).first()

    def create(self, validated_data):
        """create round for school"""

        round_for_school = RoundForSchool.objects.create(
            round_id=self.context["round_id"], school_id=validated_data["school_id"]
        )

        return round_for_school

    def to_representation(self, instance):
        data = super().to_representation(instance)

        school = School.objects.filter(id=data["school"]["id"]).first()
        school_registration_for_quiz_obj = SchoolRegisteredForQuiz.objects.filter(
            school=school
        ).first()

        data["SchoolRegistrationId"] = school_registration_for_quiz_obj.id
        data["SchoolRegistration"] = SchoolForQuizSerializer(
            instance=school_registration_for_quiz_obj
        ).data

        if hasattr("school", "created_at") and hasattr("school", "updated_at"):
            data["school"].pop("created_at")
            data["school"].pop("updated_at")
            return data

        return data
