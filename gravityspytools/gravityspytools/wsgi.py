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

# Database and integration settings come from the deployment environment
# (e.g. Apache SetEnv); no credentials or hostnames are stored in this file.
# Both canonical and legacy names are forwarded during the migration.
env_variables_to_pass = [
    'GRAVITYSPYTOOLS_NAME',
    'GRAVITYSPYTOOLS_DATABASE_USER', 'GRAVITYSPYTOOLS_USER',
    'GRAVITYSPYTOOLS_DATABASE_PASSWD', 'GRAVITYSPYTOOLS_PASSWORD',
    'GRAVITYSPYTOOLS_HOST', 'GRAVITYSPYTOOLS_PORT',
    'GRAVITYSPY_DATABASE_USER', 'GRAVITYSPY_DATABASE_PASSWD',
    'GRAVITYSPYPLUS_DATABASE_USER', 'GRAVITYSPYPLUS_DATABASE_PASSWD',
    'GRAVITYSPY_SCIENCE_DB_HOST',
    'PANOPTES_CLIENT_ID', 'PANOPTES_CLIENT_SECRET', 'PANOPTES_PROJECT', 'REDIRECT_URI',
]

_application = get_wsgi_application()


def application(environ, start_response):
    # Forward deployment-provided variables without overwriting an existing
    # value when a request does not carry it.
    for var in env_variables_to_pass:
        if var in environ:
            os.environ[var] = environ[var]
    return _application(environ, start_response)
