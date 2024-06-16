from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.SchoolListCreateView.as_view(),
        name="create-school",
    ),
    path(
        "/<str:id>",
        views.SchoolRetrieveUpdateDestroyView.as_view(),
        name="school-retrieve-update-destroy",
    ),
]
