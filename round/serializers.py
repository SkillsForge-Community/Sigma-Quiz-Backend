from rest_framework import serializers

# from sigma.quiz.models import SchoolRegisteredForQuiz
from quiz.serializers import SchoolForQuizSerializer
from round.models import Question, Round, bonus, submission
from school.serializers import SchoolSerializer

# from sigma.school.models import School
# from sigma.school.serializers import SchoolSerializer


class RoundSerializer(serializers.ModelSerializer):
    quizround = SchoolForQuizSerializer(read_only=True)

    class Meta:
        model = Round
        fields = [
            "id",
            "quizround",  # Custom field based on property in the model
            "name",
            "round_number",
            "no_of_questions",
            "no_of_schools",
            "marks_per_question",
            "marks_per_bonus_question",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    roundquestion = RoundSerializer(read_only=True)
    answered_by = SchoolSerializer(read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "roundquestion",
            "question_number",
            "questionfield",
            "correct_answer",
            "answered_by",
        )


class BonusSerializer(serializers.ModelSerializer):
    fromschool = SchoolSerializer(read_only=True)
    toschool = SchoolSerializer(read_only=True)
    round = RoundSerializer(read_only=True)
    Question = QuestionSerializer(read_only=True)

    class Meta:
        model = bonus
        fields = (
            "id",
            "fromschool",
            "toschool",
            "round",
            "question",
            "score",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    round = RoundSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = submission
        fields = (
            "id",
            "school",
            "round",
            "question",
            "score",
        )
