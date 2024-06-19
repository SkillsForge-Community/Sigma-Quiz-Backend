from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizSerializer


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
