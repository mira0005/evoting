from . import settings

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'evoting',
        'USER': 'root', 
        'PASSWORD': '',
        'PORT': 3306,
        'HOST': 'localhost'
    }
}

STATIC_ROOT = settings.BASE_DIR / "website/static/"
MEDIA_ROOT = settings.BASE_DIR / "website/media/"