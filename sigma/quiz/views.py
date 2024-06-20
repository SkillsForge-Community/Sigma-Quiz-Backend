from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from sigma.quiz.models import SchoolRegisteredForQuiz

from .models import Quiz
from .serializers import QuizSerializer, SchoolForQuizSerializer


class QuizListCreateView(generics.ListCreateAPIView):
    """
    A view to list and create quizzes
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        date = request.data.get("date")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            return Response(
                {
                    "message": "date must be a valid ISO 8601 date string",
                    "error": "Bad Request",
                    "statusCode": 400,
                },
                status=400,
            )

        if Quiz.objects.filter(date=date).exists():
            return Response(
                {
                    "message": f"Key (date)=({date}) already exists.",
                    "error": "Conflict",
                    "statusCode": 409,
                },
                status=409,
            )

        return super().post(request, *args, **kwargs)


class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve a quiz.
    """

    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    error_response = Response(
        {
            "message": "Sigma Quiz with this id does not exis",
            "error": "Not Found",
            "statusCode": 404,
        },
        status=404,
    )

    def get_object(self):
        """retrieve quiz object"""

        quiz_id = self.kwargs["id"]
        return Quiz.objects.filter(id=quiz_id).first()

    def get(self, request, *args, **kwargs):
        """Override default get method to include custom error message"""

        if self.get_object() is None:
            return self.error_response
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Override default update method to include custom error message"""

        instance = self.get_object()
        if instance is None:
            return self.error_response
        serializer = self.serializer_class(
            instance,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        """
        Override default delete method to include custom error and
        success message
        """

        instance = self.get_object()
        if instance is None:
            return self.error_response
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Successful",
            },
            status=204,
        )


class RegisterSchoolForQuizView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolForQuizSerializer
    queryset = SchoolRegisteredForQuiz.objects.all()

    def post(self, request, *args, **kwargs):
        quiz_id = self.kwargs["quiz_id"]
        school_id = self.request.data["school_id"]
        print(school_id)

        error_data = {
            "message": "School already registered for Quiz",
            "error": "Conflict",
            "statusCode": 409,
        }

        if not self.school_registered_for_quiz(quiz_id, school_id):
            return super().post(request, *args, **kwargs)

        return Response(data=error_data, status=status.HTTP_409_CONFLICT)

    def get_serializer_context(self):
        """Modify serializer context"""
        context = super().get_serializer_context()
        context["quiz_id"] = self.kwargs["quiz_id"]
        return context

    def school_registered_for_quiz(self, quiz_id, school_id):
        """checks if school has registered for quiz"""

        return SchoolRegisteredForQuiz.objects.filter(quiz_id=quiz_id, school_id=school_id).first()


class UnRegisterSchoolForQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """unregistered school for quiz"""
        school_id = self.kwargs["school_id"]
        quiz_id = self.kwargs["quiz_id"]

        school_to_unregister_for_quiz_obj = get_object_or_404(
            SchoolRegisteredForQuiz, school_id=school_id, quiz_id=quiz_id
        )
        school_to_unregister_for_quiz_obj.delete()

        schools_remaining_for_quiz = SchoolRegisteredForQuiz.objects.all()
        serializer = SchoolForQuizSerializer(schools_remaining_for_quiz, many=True)

        response_data = {"message": "Successful", "registered_school": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
