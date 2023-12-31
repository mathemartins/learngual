"""
ASGI config for learngual project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import pathlib
import dotenv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learngual.settings')

django.setup()

from learngual.routing import ws_urlpatterns

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

CURRENT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
ENV_FILE_PATH = BASE_DIR / ".env"

dotenv.read_dotenv(str(ENV_FILE_PATH))

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})
