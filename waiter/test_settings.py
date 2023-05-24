from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mytestdatabase',
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'