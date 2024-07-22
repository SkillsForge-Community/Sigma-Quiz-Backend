# from django.shortcuts import render
# from django.shortcuts import render

# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from quiz.models import SchoolRegisteredForQuiz

# from quiz.serializers import SchoolForQuizSerializer
from rest_framework import status
from quiz.models import Quiz
from round.serializers import SubmissionSerializer, BonusSerializer
from round.models import Round, bonus, submission
from .serializers import QuizSerializer
import uuid


class create_and_get_all_quiz(APIView):
    serializer_class = QuizSerializer

    def get(self, request: Request, *args, **kwargs):
        quizs = Quiz.objects.all()
        serializer = QuizSerializer(instance=quizs, many=True)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        title = data.get("title")
        date = data.get("date")
        description = data.get("description")
        noofrounds = data.get("noofrounds")
        
        if Quiz.objects.filter(
            title=title,
            date=date,
            description=description,
            noofrounds=noofrounds
        ).exists():
            response = {
                "message": "Quiz alredy exist",
            }
        else:
            newquiz = Quiz.objects.create(
                title=title,
                date=date,
                description=description,
                noofrounds=noofrounds,
            )
            serializer = QuizSerializer(newquiz)
            response = {
                "data": serializer.data,
                "message": "Succesfull",
            }
        return Response(data=response, status=status.HTTP_200_OK)


class Fetch_single_quiz_update_it_and_delete_quiz(APIView):
    serializer_class = QuizSerializer

    def get(self, request: Request, id: uuid):
        quiz = get_object_or_404(Quiz, id=id)

        #  like = get_object_or_404(Like, post=post)
        serializer = self.serializer_class(instance=quiz)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, id: uuid):
        quiz = get_object_or_404(Quiz, id=id)
        data = request.data
        title = data.get("title")
        date = data.get("date")
        description = data.get("description")

        if quiz:
            quiz.title = title
            quiz.date = date
            quiz.description = description
            quiz.save()
            serializer = QuizSerializer(quiz)
            response = {
                "data": serializer.data,
                "message": "Update Succesfull",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Quiz does not exist",
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, id: uuid):
        quiz = get_object_or_404(Quiz, id=id)
        if quiz:
            quiz.delete()
            serializer = QuizSerializer(quiz)
            response = {
                "data": serializer.data,
                "message": "Succesfull",
            }
        else:
            response = {
                "message": "Quiz does not exiist",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class get_quiz_results(APIView):

    def get(self, request: Request, quiz_id: int):
        quiz = Quiz.objects.get(id=quiz_id)
        subs = submission.objects.get(school__quiz=quiz)
        schoolreg = SchoolRegisteredForQuiz.objects.get(quiz=quiz)
        round = Round.objects.get(quiz=schoolreg)
        getbonus = bonus.objects.get(round=round)
        subserializer = SubmissionSerializer(subs)
        bonuserializer = BonusSerializer(getbonus)
        response = {
            "message": "Quiz does not exiist",
            "submissions": subserializer.data,
            "bonus": bonuserializer,
        }
        return Response(data=response, status=status.HTTP_200_OK)

# Create your views here.


# Create your views here.
