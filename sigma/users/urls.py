from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("test/", views.UserCreateView.as_view(), name="user-create"),
    path("me/", views.UserProfileView.as_view(), name="user-profile"),
    path("<str:id>/", views.UserDestroyView.as_view(), name="user-delete"),
    path("<str:id>/", views.UserRetrieveView.as_view(), name="user-detail"),
]
