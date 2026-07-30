import os

# Production science database. Used as the default so an unset override keeps
# current production behavior.
PROD_SCIENCE_DB_HOST = 'gravityspyplus.ciera.northwestern.edu'


def science_db_host():
    return os.getenv('GRAVITYSPY_SCIENCE_DB_HOST', PROD_SCIENCE_DB_HOST)
