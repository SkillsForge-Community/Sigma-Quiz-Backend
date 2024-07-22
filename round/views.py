from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response

# from django.http import JsonResponse
from quiz.models import SchoolRegisteredForQuiz, Quiz
from school.models import School

# from quiz.serializers import SchoolForQuizSerializer
import json
import uuid
from rest_framework import status
from quiz.serializers import QuizSerializer

# from quiz.models import
from round.models import Round, Question, submission, bonus
from .serializers import (
    BonusSerializer,
    SubmissionSerializer,
    QuestionSerializer,
    RoundSerializer,
)

from school.serializers import SchoolSerializer


class createquizround(APIView):

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        quizid = data.get("quizId")
        quiz1 = Quiz.objects.filter(id=quizid).first()
        quiz = SchoolRegisteredForQuiz.objects.filter(quizreg=quiz1).first()
        roundcount = Round.objects.filter(quizround=quiz).count()
        roundvalues = Round.objects.filter(quizround=quiz).first()
        if roundvalues:
            roundnumbers = [roundvalues.round_number]
            # quiz.quizreg.noofrounds
            if quiz.quizreg.noofrounds == roundcount:
                response = {
                    "message": "No of Round limit Exceeded",
                }
                return Response(
                    data=response,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                roundcount < quiz.quizreg.noofrounds
                and data.get("round_number") not in roundnumbers
            ):
                createdround = Round.objects.create(
                    quizround=quiz,
                    name=data.get("name"),
                    round_number=data.get("round_number"),
                    no_of_questions=data.get("no_of_questions"),
                    no_of_schools=data.get("no_of_schools"),
                    marks_per_question=data.get("marks_per_question"),
                    marks_per_bonus_question=data.get("marks_per_bonus_question"),
                )
                serializer = RoundSerializer(instance=createdround)
                response = {
                    "data": serializer.data,
                    "message": "Round Created ",
                }
                return Response(data=response, status=status.HTTP_200_OK)
        else:
            createdround = Round.objects.create(
                quizround=quiz,
                name=data.get("name"),
                round_number=data.get("round_number"),
                no_of_questions=data.get("no_of_questions"),
                no_of_schools=data.get("no_of_schools"),
                marks_per_question=data.get("marks_per_question"),
                marks_per_bonus_question=data.get("marks_per_bonus_question"),
            )
            print(createdround)
            serializer = RoundSerializer(instance=createdround)
            response = {
                "data": serializer.data,
                "message": "First round for quiz created ",
            }

            return Response(data=response, status=status.HTTP_200_OK)


class retrieveroundview(APIView):

    def get(self, request: Request, id: uuid):
        roundexist = Round.objects.filter(id=id).exists()
        if roundexist is True:
            round = get_object_or_404(Round, id=id)
            serializer = RoundSerializer(instance=round)
            response = {
                "data": serializer.data,
                "message": "Round Created ",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Round does not exist ",
                "status": 409,
            }
            return Response(data=response, status=status.HTTP_409_CONFLICT)


class delete_round_view(APIView):
    def delete(self, request: Request, id: uuid):
        round = Round.objects.get(id=id)
        if round:
            round.delete()
            response = {
                "message": "Rounds deleted",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Rounds does not exist",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class get_quiz_round(APIView):

    def get(self, request: Request, quiz_id: uuid):
        quizround = Round.objects.filter(quizround__quizreg__id=quiz_id)
        print(quizround)
        if quizround:
            serializer = RoundSerializer(quizround, many=True)
            response = {
                "data": serializer.data,
                "message": "Rounds created ",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Quiz does not exist ",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class get_quiz_result(APIView):

    def get(self, request: Request, quiz_id: uuid):
        quizround = Round.objects.filter(quizround__quizreg__id=quiz_id)
        # presentquiz = Quiz.objects.get(id=quiz_id)
        # question = Question.objects.get(round=quizround)
        combined_data = {}
        y = 0
        roundids = []
        for i in quizround:
            roundids.append(i.id)
        for i in roundids:
            bonusround = bonus.objects.filter(round__id=i)
            sub = submission.objects.filter(roundsub__id=i)
            if sub.exists() and bonusround.exists():
                submission_serializer = SubmissionSerializer(sub, many=True)
                y += 1
                x = "Round" + str(y)
                combined_data[x] = submission_serializer.data
                print(submission_serializer.data)
                # combined_data[x] = serializer.data
                for i in sub:
                    for j in bonusround:
                        if i.question == j.question:
                            combined_data["bonusto"] = BonusSerializer(
                                bonusround,
                                many=True,
                            ).data
                return Response(data=combined_data, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "no submission for participant ",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class markquestion(APIView):
    serializer_class = QuestionSerializer

    def post(self, request: Request, question_id: uuid):
        data = request.data
        schoolid = data.get("school_id")
        ans_status = data.get("answered_correctly")
        request.session["ans_status"] = ans_status
        school = School.objects.get(id=schoolid)
        schoolquiz = School.objects.get(
            id=schoolid,
        )
        question = Question.objects.get(
            id=question_id,
        )
        questionjson = Question.objects.filter(
            id=question_id,
        )
        if ans_status is True and question.answered_by is None:
            question.answered_by = school
            question.ans_status = ans_status
            question.save()
            submit_status = submission.objects.filter(
                school=school,
                roundsub=question.roundquestion,
            ).exists()
            if submit_status is False:
                submit = submission.objects.create(
                    school=schoolquiz,
                    roundsub=question.roundquestion,
                    score=1,
                    question=question,
                )
                serilizer = SubmissionSerializer(submit)
                response = {
                    "message": "Question marked",
                    "data": serilizer.data,
                    "statusCode": 200,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                submit = submission.objects.get(
                    school=schoolquiz,
                    roundsub=question.roundquestion,
                )
                submit.score += 1
                # x = question.answered_by
                submit.save()
                serilizer = SubmissionSerializer(submit)
                print(serilizer.data)
                response = {
                    "message": "Question marked",
                    "data": serilizer.data,
                    "statusCode": 200,
                }

            return Response(data=response, status=status.HTTP_200_OK)
            # return Response(data=response, status=status.HTTP_200_OK)
        elif ans_status is True and question.answered_by == school:
            response = {
                "message": "Question marked as Answered by This School",
                "error": "Conflict",
                "statusCode": 409,
            }
            return Response(data=response, status=status.HTTP_409_CONFLICT)
        if ans_status is False:
            question.answered_by = school
            question.ans_status = ans_status
            question.save()
            # sch = SchoolSerializer(school)
            # serializer = self.serializer_class(instance=question)
            serializer = QuestionSerializer(questionjson, many=True)
            print(serializer.data)
            # response = json.dumps(serializer.data)
            response = serializer.data
            # Return the JSON response
            # cjson_data = json.dumps()
            # print(serializer.data)

            #
            # print(response)
            return Response(
                data=response,
                status=status.HTTP_200_OK,
            )


class AddQuestionView(APIView):

    def post(self, request: Request, round_id: uuid):
        data = json.loads(request.body)
        questions = data.get("question_field", {})
        newlevel = Round.objects.get(id=round_id)
        x = 0
        print(len(questions))
        if len(questions) == newlevel.no_of_questions:
            for i in questions:
                value = questions[i]
                x = x + 1
                Question.objects.create(
                    roundquestion=newlevel,
                    question_number=x,
                    questionfield=i,
                    correct_answer=value,
                )
            allquest = Question.objects.filter(roundquestion=newlevel)
            response = {
                "message": "Questions Added",
                "data": QuestionSerializer(instance=allquest, many=True).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Length of Question not equal to the one in round",
            }
            return Response(
                data=response,
                status=status.HTTP_400_BAD_REQUEST,
            )


class getQuestionView(APIView):

    def get(self, request: Request, round_id: uuid):
        qround = Round.objects.get(id=round_id)
        if qround:
            query = Question.objects.filter(roundquestion=qround)
            serializer = QuestionSerializer(query, many=True)
            response = {
                "data": serializer.data,
            }
            return Response(
                data=response,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            response = {
                "message": "Round does not exxist",
            }
            return Response(
                data=response,
                status=status.HTTP_400_BAD_REQUEST,
            )


class MarkBonusView(APIView):

    def post(self, request: Request, question_id: uuid):
        data = request.data
        schoolid = data.get("school_id")
        school = School.objects.get(id=schoolid)
        question = Question.objects.get(id=question_id)
        fromschool = School.objects.get(id=question.answered_by.id)
        bonusround = Round.objects.get(id=question.roundquestion.id)
        submit_status = submission.objects.filter(
            school__id=schoolid,
            roundsub=bonusround,
        ).exists()
        bonus.objects.create(
            fromschool=fromschool,
            toschool=school,
            round=bonusround,
            question=question,
            score=2,
        )
        if submit_status is False:
            submission.objects.create(
                school=school,
                roundsub=bonusround,
                score=2,
                question=question,
            )
        else:
            submit = submission.objects.get(
                school__id=schoolid,
                roundsub=question.roundquestion,
            )
            submit.score += 2
            submit.save()
            subserializer = SubmissionSerializer(instance=submit)
            response = {"data": subserializer.data}
            return Response(data=response, status=status.HTTP_200_OK)


# Create your views here.


# Create your views here.
