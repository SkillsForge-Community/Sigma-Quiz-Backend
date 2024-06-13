from datetime import timedelta

from .base import *  # noqa

SECRET_KEY = os.getenv("SECRET_KEY")  # noqa


THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_standardized_errors",
    "corsheaders",
]


LOCAL_APPS = [
    "sigma.authentication",
    "sigma.users",
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS  # noqa


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "sigma.utils.custom_renderer.CustomJsonResponse",
        "rest_framework.renderers.JSONRenderer",
    ],
}


# E-MAIL SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa

# SIMPLE_JWT_SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Token",),
}
