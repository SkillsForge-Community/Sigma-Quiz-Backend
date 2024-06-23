from django.urls import path, re_path

from . import views

urlpatterns = [
    path(
        "rounds/",
        views.QuizRoundCreateView.as_view(),
        name="quiz-round-create",
    ),
    path(
        "rounds/<uuid:id>",
        views.QuizRoundRetrieveUpdateDestroyView.as_view(),
        name="quiz-round-retrieve-update-destroy",
    ),
    path(
        "<uuid:quiz_id>/rounds",
        views.QuizRoundsListView.as_view(),
        name="quiz-round-list",
    ),
    path(
        "rounds/<uuid:round_id>/schools",
        views.RoundForSchoolView.as_view(),
        name="round_for_school",
    ),
    path(
        "rounds/<uuid:round_id>/schools/<uuid:school_id>",
        views.RemoveSchoolFromRoundView.as_view(),
        name="remove_schoool_from_round",
    ),
]
