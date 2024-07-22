# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from school.models import School
from rest_framework import status
from round.models import Round
from .serializers import SchoolSerializer
from quiz.models import SchoolRegisteredForQuiz, Quiz
import uuid
from quiz.serializers import SchoolForQuizSerializer


class create_school(APIView):

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        name = data.get("name")
        state = data.get("state")
        address = data.get("address")

        if School.objects.filter(
            name=name,
            state=state,
            address=address,
        ).exists():
            response = {
                "message": "School alredy exist",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            school_created = School.objects.create(
                name=name,
                state=state,
                address=address,
            )
            serializer = SchoolSerializer(school_created)
            response = {"message": "School added", "data": serializer.data}
            return Response(data=response, status=status.HTTP_200_OK)


class Add_school_to_quiz(APIView):

    def post(self, request: Request, quiz_id: uuid):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        SchoolRegisteredForQuiz
        data = request.data
        schoolid = data.get("school_id")
        school = get_object_or_404(School, id=schoolid)
        if SchoolRegisteredForQuiz.objects.filter(
            schoolreg=school,
            quizreg=quiz,
        ).exists():
            response = {
                "message": "School alredy part of quuiz",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            school_reg = SchoolRegisteredForQuiz.objects.create(
                schoolreg=school,
                quizreg=quiz,
            )
            serializer = SchoolForQuizSerializer(school_reg)
            response = {
                "data": serializer.data,
                "message": "Success",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class fetch_registered_schools_and_unregister_school(APIView):

    def get(self, request: Request, quiz_id: uuid):
        schoolquiz = SchoolRegisteredForQuiz.objects.get(quizreg__id=quiz_id)
        if schoolquiz:
            regschool = schoolquiz.school
            serializer = SchoolSerializer(regschool)
            response = {
                "data": serializer.data,
                "message": "Success",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "No school registered",
            }
            return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request, quiz_id: uuid, school_id: uuid):
        schoolquiz = SchoolRegisteredForQuiz.objects.get(
            quizreg__id=quiz_id,
            schoolreg__id=school_id,
        )
        if schoolquiz:
            schoolquiz.delete()
            response = {
                "message": "success",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "School does not exist",
            }
            return Response(data=response, status=status.HTTP_200_OK)


class remove_school_from_round(APIView):
    def post(self, request: Request, round_id: uuid):
        data = request.data
        roundtodeleterfrom = Round.objects.get(id=round_id)
        schoolid = data.get("school_id")
        schooltodelete = School.objects.get(id=schoolid)
        if schooltodelete:
            schoolreg = roundtodeleterfrom.schooltodelete
            schoolreg.delete()


# Create your views here.
