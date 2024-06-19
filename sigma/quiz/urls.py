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
]
