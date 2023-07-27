from . import settings

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nama database',
        'USER': 'username database', 
        'PASSWORD': 'password database',
        'PORT': 3306,
        'HOST': 'localhost'
    }
}

STATIC_ROOT = '/home/username/direktoi-domain/static/'
MEDIA_ROOT = '/home/username/direktoi-domain/media/'