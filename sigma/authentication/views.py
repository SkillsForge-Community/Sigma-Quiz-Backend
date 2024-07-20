from rest_framework import generics, permissions, status
from rest_framework.response import Response

from sigma.authentication.serializers import (
    ChangePasswordSerializer,
    LogInSerializer,
    RegisterUserSerializer,
    ResetPasswordSerializer,
)


class RegisterAdminAPIView(generics.CreateAPIView):

    serializer_class = RegisterUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginInAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LogInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = self.request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response({"message": "Password Successfully updated"}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request, *args, **kwargs):
        user = self.request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response({"message": "Password Successfully updated"}, status=status.HTTP_200_OK)
