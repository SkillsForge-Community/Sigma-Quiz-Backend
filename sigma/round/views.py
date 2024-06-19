from rest_framework import generics, permissions
from rest_framework.response import Response

from sigma.quiz.models import Quiz

from .models import Round
from .serializers import QuizRoundSerializer


class QuizRoundCreateView(generics.CreateAPIView):
    """
    A view to list and create quizzes
    """

    queryset = Round.objects.all()
    serializer_class = QuizRoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(f"{request.data}")

        if serializer.is_valid():
            data = serializer.validated_data
            quiz_id = data.get("quizId")
            quiz = Quiz.objects.get(id=quiz_id)
        else:
            errors = serializer.errors
            return Response(
                {
                    "message": (errors["message"][0]),
                    "error": (errors["error"][0]),
                    "statusCode": (int(errors["statusCode"][0])),
                },
                status=(int(errors["statusCode"][0])),
            )

        round_obj = Round.objects.create(
            quiz=quiz,
            name=data["name"],
            round_number=data["round_number"],
            no_of_questions=data["no_of_questions"],
            no_of_schools=data["no_of_schools"],
            marks_per_question=data["marks_per_question"],
            marks_per_bonus_question=data["marks_per_bonus_question"],
        )
        return Response(QuizRoundSerializer(round_obj).data, status=201)


class QuizRoundRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve a quiz round.
    """

    serializer_class = QuizRoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    error_response = Response(
        {
            "message": "Quiz Round with this id does not exist",
            "error": "Not Found",
            "statusCode": 404,
        },
        status=404,
    )

    def get_object(self):
        """retrieve quiz object"""

        round_id = self.kwargs["id"]
        return Round.objects.filter(id=round_id).first()

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
