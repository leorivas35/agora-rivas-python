import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agora_rivas.infrastructure.config.settings")

application = get_wsgi_application()
