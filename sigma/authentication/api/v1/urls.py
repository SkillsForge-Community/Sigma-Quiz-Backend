from django.urls import path

from sigma.authentication.api.v1.views import (
    ChangePasswordAPIView,
    LoginInAPIView,
    RegisterAdminAPIView,
)

app_name = "authentication"

urlpatterns = [
    path("register/admin", RegisterAdminAPIView.as_view(), name="register_admin"),
    path("login", LoginInAPIView.as_view(), name="login"),
    path("password/change", ChangePasswordAPIView.as_view(), name="change_password"),
]
