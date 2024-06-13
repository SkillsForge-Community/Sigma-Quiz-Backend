from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
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
        error_response = Response(
            {
                "message": "Forbidden: super-admin Only",
                "error": "Forbidden",
                "statusCode": 403,
            },
            status=403,
        )

        # if not request.user.is_authenticated:
        #    return error_response

        roles = getattr(request.user, "roles", [])
        if "super-admin" not in roles:
            return error_response

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {
                    "message": "User with this id does not exist",
                    "error": "Not Found",
                    "statusCode": 404,
                },
                status=404,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
