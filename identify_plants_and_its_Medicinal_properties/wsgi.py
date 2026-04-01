"""
WSGI config for identify_plants_and_its_Medicinal_properties project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'identify_plants_and_its_Medicinal_properties.settings')

application = get_wsgi_application()
