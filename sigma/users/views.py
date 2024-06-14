from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    A view to list all user accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def list(self, request, *args, **kwargs):

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
        return super().list(request, *args, **kwargs)


class UserProfileView(generics.RetrieveAPIView):
    """
    A view to retrieve the current user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    A view for viewing and deleting user accounts.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    error_response = Response(
        {
            "message": "User with this id does not exist",
            "error": "Not Found",
            "statusCode": 404,
        },
        status=404,
    )

    def get_object(self):
        user_id = self.kwargs["id"]
        return User.objects.filter(id=user_id).first()

    def get(self, request, *args, **kwargs):
        if self.get_object() is None:
            return self.error_response
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return self.error_response
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Successful",
            },
            status=200,
        )
