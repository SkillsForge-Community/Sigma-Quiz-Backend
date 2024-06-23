from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.QuizListCreateView.as_view(),
        name="quiz-list-create",
    ),
    path(
        "/<str:id>",
        views.QuizRetrieveUpdateDestroyView.as_view(),
        name="quiz-retrieve-update-destroy",
    ),
    path(
        "/<uuid:quiz_id>/schools",
        views.RegisterSchoolForQuizView.as_view(),
        name="list_create_school_for_quiz",
    ),
    path(
        "/<uuid:quiz_id>/schools/<uuid:school_id>/",
        views.UnRegisterSchoolForQuizView.as_view(),
        name="unregister_school_for_quiz",
    ),
]
