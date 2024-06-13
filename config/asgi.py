"""
ASGI config for sigma project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

from django.core.asgi import get_asgi_application  # noqa

os.environ["DJANGO_SETTINGS_MODULE"] = os.getenv("DJANGO_SETTINGS_MODULE")

application = get_asgi_application()
