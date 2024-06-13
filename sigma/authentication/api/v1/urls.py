from django.urls import path

from sigma.authentication.api.v1.views import RegisterAdminAPIView

app_name = "authentication"

urlpatterns = [
    path("register-admin/", RegisterAdminAPIView.as_view(), name="register_admin"),
]
