"""
WSGI config for Algorithm_Progress_Tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

# sys.path.append('/Users/trinahaque28/Desktop/cd_python/DSA_Progress_Tracker')
# sys.path.append('/Users/trinahaque28/Desktop/cd_python/myEnvironment/djangoEnv/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
#
# application = get_wsgi_application()
# application = DjangoWhiteNoise(application)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Algorithm_Progress_Tracker.settings")

application = get_wsgi_application()
