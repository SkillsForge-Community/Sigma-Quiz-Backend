from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.QuizListCreateView.as_view(),
        name="quiz-list-create",
    ),
]
