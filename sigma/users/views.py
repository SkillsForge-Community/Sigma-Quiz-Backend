from django.http import Http404  # noqa NOTE: unused import
from rest_framework import generics, permissions, status  # noqa NOTE: status unused
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

        # roles = getattr(request.user, "roles", [])

        # Simulate the roles from the headers
        roles_header = request.headers.get("X-User-Roles", "")
        roles = roles_header.split(",")

        if "super-admin" not in roles:
            return Response(
                {
                    "message": "Forbidden: super-admin Only",
                    "error": "Forbidden",
                    "statusCode": 403,
                },
                status=403,
            )
        return super().list(request, *args, **kwargs)


class UserProfileView(generics.RetrieveAPIView):
    """
    A view to retrieve the current user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveView(generics.RetrieveAPIView):
    """
    A view for viewing  user accounts.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs["id"]
        return User.objects.filter(id=user_id).first()

    def get(self, request, *args, **kwargs):
        if self.get_object() is None:
            return Response(
                {
                    "message": "User with this id does not exist",
                    "error": "Not Found",
                    "statusCode": 404,
                },
                status=404,
            )
        return super().get(request, *args, **kwargs)


class UserDestroyView(generics.DestroyAPIView):
    """
    A view for deleting user accounts.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Successful",
            },
            status=200,
        )


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
