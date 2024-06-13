from rest_framework import generics, permissions

from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    A view to list all user accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    A view for viewing and deleting user accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
