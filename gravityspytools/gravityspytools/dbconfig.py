import os

# Production science database. Used as the default so an unset override keeps
# current production behavior.
PROD_SCIENCE_DB_HOST = 'gravityspyplus.ciera.northwestern.edu'

_REQUIRED = object()


class DatabaseConfigError(Exception):
    pass


def science_db_host():
    return os.getenv('GRAVITYSPY_SCIENCE_DB_HOST', PROD_SCIENCE_DB_HOST)


# Production hosts, used when GRAVITYSPY_ALLOWED_HOSTS is unset.
DEFAULT_ALLOWED_HOSTS = [
    'gravityspy.ciera.northwestern.edu',
    'gravityspytools.ciera.northwestern.edu',
    '127.0.0.1',
]


def allowed_hosts():
    raw = os.getenv('GRAVITYSPY_ALLOWED_HOSTS')
    if not raw:
        return list(DEFAULT_ALLOWED_HOSTS)
    return [host.strip() for host in raw.split(',') if host.strip()]


def require_env(canonical, legacy=(), default=_REQUIRED):
    # First non-empty value wins, so empty placeholders (e.g. set by wsgi.py)
    # do not mask a real value provided under a legacy name.
    for name in (canonical,) + tuple(legacy):
        value = os.environ.get(name)
        if value:
            return value
    if default is not _REQUIRED:
        return default
    # Name the variable, never a value, so credentials cannot leak into logs.
    raise DatabaseConfigError(
        'Missing required database configuration: set {0}'.format(canonical)
    )
