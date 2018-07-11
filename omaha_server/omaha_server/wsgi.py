"""
WSGI config for omaha_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaha_server.settings")

from django.core.wsgi import get_wsgi_application

try:
  from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
  application = Sentry(get_wsgi_application())
except ImportError:
  print("[WARN] raven python module not found")
  application = get_wsgi_application()

