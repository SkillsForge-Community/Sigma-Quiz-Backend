from django.urls import path

from . import views

urlpatterns = [
    path(
        "school",
        views.SchoolListCreateView.as_view(),
        name="create-school",
    ),
    path(
        "school/<str:id>",
        views.SchoolRetrieveUpdateDestroyView.as_view(),
        name="school-retrieve-update-destroy",
    ),
]
