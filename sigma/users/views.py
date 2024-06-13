from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    A view to list all user accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #    return error_response

        roles = getattr(request.user, "roles", [])
        if "super-admin" not in roles:
            return Response(
                {
                    "message": "Forbidden: super-admin Only",
                    "error": "Forbidden",
                    "statusCode": 403,
                },
                status=403,
            )


class UserProfileView(generics.RetrieveAPIView):
    """
    A view to retrieve the current user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    A view for viewing and deleting user accounts.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs["pk"]
        return User.objects.filter(id=user_id).first()

    def get(self, request, *args, **kwargs):
        if self.get_object() == None:
            return Response(
                {
                    "message": "User with this id does not exist",
                    "error": "Not Found",
                    "statusCode": 404,
                },
                status=404,
            )


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
