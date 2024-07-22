from django.urls import path

from . import views

urlpatterns = [
    path(
        "<uuid:quiz_id>/quiz/<uuid:school_id>/",
        views.fetch_registered_schools_and_unregister_school.as_view(),
        name="school-list-create",
    ),
    path(
        "create_school/",
        views.create_school.as_view(),
        name="create_school",
    ),
    path(
        "school/<uuid:quiz_id>",
        views.Add_school_to_quiz.as_view(),
        name="add_school_to_quiz",
    ),
]
