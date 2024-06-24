from rest_framework import serializers

from sigma.quiz.models import Quiz, SchoolRegisteredForQuiz
from sigma.quiz.serializers import SchoolForQuizSerializer
from sigma.round.models import Round, RoundForSchool
from sigma.school.models import School


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
    questions = serializers.SerializerMethodField()
    schoolParticipations = serializers.SerializerMethodField()
    quizId = serializers.UUIDField(required=False)

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
            "schoolParticipations",
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

    def get_schoolParticipations(self, instance):
        return []

    def get_questions(self, instance):
        return []

    def validate(self, data):

        instance = self.instance
        quiz_id = data.get("quizId") if "quizId" in data else instance.quiz.id
        round_number = data.get("round_number")

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "Sigma Quiz with this id does not exist",
                    "error": "Not Found",
                    "statusCode": 404,
                }
            )
        round_obj = Round.objects.filter(quiz=quiz, round_number=round_number)
        if instance:
            round_obj = round_obj.exclude(id=instance.id)
        if round_obj.exists():
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
        request = self.context.get("request", None)
        fields = list(self.Meta.fields)

        if request and request.method == "GET":
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
        elif request and request.method == "PUT":
            fields = RoundSerializer.Meta.fields
        else:
            fields.remove("schoolParticipations")
            fields.remove("questions")

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}


class RoundForSchoolSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    roundId = serializers.UUIDField(source="round.id", read_only=True)

    round = RoundSerializer(read_only=True)
    # school = SchoolSerializer(read_only=True)

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    school_id = serializers.UUIDField(write_only=True)
    schoolRegistration = serializers.SerializerMethodField()
    schoolRegistrationId = serializers.SerializerMethodField()

    class Meta:
        model = RoundForSchool
        fields = [
            "roundId",
            "schoolRegistrationId",
            "schoolRegistration",
            "round",
            "id",
            "created_at",
            "updated_at",
            "school_id",
        ]

    def get_schoolRegistration(self, instance):
        school_id = instance.school_id
        school_obj = School.objects.filter(id=school_id).first()
        school_registration_for_quiz_obj = SchoolRegisteredForQuiz.objects.filter(
            school=school_obj
        ).first()

        data = {"id": school_registration_for_quiz_obj.id}

        obj = SchoolForQuizSerializer(instance=school_registration_for_quiz_obj).data
        quiz_data = obj.get("quiz", {})
        quiz_data.pop("rounds", None)
        obj["quiz"] = quiz_data
        obj.pop("created_at")
        obj.pop("updated_at")
        data.update(obj)

        return data

    def get_schoolRegistrationId(self, instance):
        school_id = instance.school_id
        school_obj = School.objects.filter(id=school_id).first()
        school_registration_for_quiz_obj = SchoolRegisteredForQuiz.objects.filter(
            school=school_obj
        ).first()

        return school_registration_for_quiz_obj.id

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

        request = self.context.get("request", None)
        fields = list(self.Meta.fields)

        if request and request.method in ["GET", "DELETE"]:

            fields = [
                "id",
                "roundId",
                "schoolRegistrationId",
                "schoolRegistration",
            ]

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}
