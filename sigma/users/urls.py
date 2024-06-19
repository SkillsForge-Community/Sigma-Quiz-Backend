from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("/me", views.UserProfileView.as_view(), name="user-profile"),
    path("/<str:id>", views.UserRetrieveDestroyView.as_view(), name="user-retrieve-destroy"),
]
