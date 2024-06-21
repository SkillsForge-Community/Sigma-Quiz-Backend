from django.urls import path

from . import views

urlpatterns = [
    path("", views.QuizRoundCreateView.as_view(), name="quiz-round-create"),
    path(
        "<str:id>",
        views.QuizRoundRetrieveUpdateDestroyView.as_view(),
        name="quiz-round-retrieve-update-destroy",
    ),
    path(
        "rounds/<uuid:round_id>/schools",
        views.RoundForSchoolView.as_view(),
        name="round_for_school",
    ),
]
