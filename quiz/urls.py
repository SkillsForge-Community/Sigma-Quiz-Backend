from django.urls import path

# from round.views import AddQuestionView, MarkBonusView, MarkQuestionView

from . import views

urlpatterns = [
    path(
        "createorget/",
        views.create_and_get_all_quiz.as_view(),
        name="quiz-create-get-all",
    ),
    path(
        "quiz/<uuid:id>",
        views.Fetch_single_quiz_update_it_and_delete_quiz.as_view(),
        name="quiz-retrieve-update-delete",
    ),
    path(
        "<uuid:quiz_id>/quiz",
        views.get_quiz_results.as_view(),
        name="quiz-results",
    ),
]
