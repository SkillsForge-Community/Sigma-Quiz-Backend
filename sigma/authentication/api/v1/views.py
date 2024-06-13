from rest_framework import generics, permissions
from rest_framework.response import Response

from sigma.authentication.api.v1.serializers import LogInSerializer, RegisterUserSerializer


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
