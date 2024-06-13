from rest_framework import generics, permissions

from sigma.authentication.api.v1.serializers import RegisterUserSerializer


class RegisterAdminAPIView(generics.CreateAPIView):

    serializer_class = RegisterUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
