from rest_framework import serializers

from sigma.quiz.models import Quiz

from .models import Round


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
