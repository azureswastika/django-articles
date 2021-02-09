import os
from subprocess import Popen

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

if os.name == "nt":
    Popen("redis/redis-server.exe")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({"http": get_asgi_application()})
