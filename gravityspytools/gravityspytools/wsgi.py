"""
WSGI config for gravityspytools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "gravityspytools.settings"
os.environ['HTTPS'] = "on"
os.environ['GRAVITYSPYTOOLS_NAME'] = ''
os.environ['GRAVITYSPYTOOLS_USER'] = ''
os.environ['GRAVITYSPYTOOLS_PASSWORD'] = ''
os.environ['GRAVITYSPYTOOLS_HOST'] = ''
os.environ['GRAVITYSPYTOOLS_PORT'] = ''

_application = get_wsgi_application()

env_variables_to_pass = ['GRAVITYSPY_DATABASE_USER', 'GRAVITYSPY_DATABASE_PASSWD', 'PANOPTES_CLIENT_ID', 'PANOPTES_CLIENT_SECRET', 'PANOPTES_PROJECT', 'REDIRECT_URI']
def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)
