from django.urls import path

from round.views import AddQuestionView, MarkBonusView, markquestion

from . import views

urlpatterns = [
    path(
        "rounds/",
        views.createquizround.as_view(),
        name="quiz-round-create",
    ),
    path(
        "rounds/<uuid:id>",
        views.retrieveroundview.as_view(),
        name="quiz-round-retrieve-update-destroy",
    ),
    path(
        "<uuid:quiz_id>/rounds",
        views.get_quiz_round.as_view(),
        name="quiz-round-list",
    ),
    path(
        "rounds/<uuid:quiz_id>/results",
        views.get_quiz_result.as_view(),
        name="round_for_school",
    ),
    path(
        "sigma_quiz/<uuid:quiz_id>/results",
        views.get_quiz_result.as_view(),
        name="get_quiz_results",
    ),
    path(
        "<uuid:question_id>/bonus",
        views.MarkBonusView.as_view(),
        name="Mark_Bonus",
    ),
    path(
        "<uuid:question_id>/mark",
        views.markquestion.as_view(),
        name="Mark_Question",
    ),
    path(
        "delete/rounds/<uuid:id>",
        views.delete_round_view.as_view(),
        name="delete_Question",
    ),
    path(
        "<uuid:round_id>/question",
        views.AddQuestionView.as_view(),
        name="Add_Question",
    ),
    path(
        "<uuid:round_id>/get_question",
        views.getQuestionView.as_view(),
        name="get_Question",
    ),
    path(
        "<uuid:round_id>/round",
        views.retrieveroundview.as_view(),
        name="get",
    ),
]
