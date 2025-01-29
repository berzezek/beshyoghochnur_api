# Beshyogochnur api servise

## Instalation

```shell
python -m venv venv
source venv/bin/activate
# . .\venv\Source\activate for Windows

pip install -r requirements.txt
```

* add local_settings.py to core
```txt
# local_settings.py
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'some_strong_pass'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['host_name']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": str(BASE_DIR / "database.cnf"),
        },
    }
}

PARLER_LANGUAGES = {
    None: (
        {'code': 'uz',},
        {'code': 'ru',},
        {'code': 'en',},
    ),
    'default': {
        'fallbacks': ['uz'],          # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}

PARLER_DEFAULT_LANGUAGE_CODE = 'uz'

LANGUAGE_CODE = 'uz'  # Установите узбекский язык по умолчанию

LANGUAGES = [
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
]

USE_I18N = True
USE_L10N = True

TIME_ZONE = 'Asia/Tashkent'

CORS_ORIGIN_ALLOW_ALL = True
```

* add database.cnf to root

```txt
[client]
database = beshyogochnur
user = beshyogochnur
password = some_pass
default-character-set = utf8
```

## Usage

* Create superuser

```shell
python manage.py createsuperuser
```

* Add category, product

```shell
/admin
```

## API

* Category

```shell
/api/v1/category?lang=en
# en, ru, uz
# uz - default
```

* Product

```shell
/api/v1/products?lang=en
# en, ru, uz 
# uz - default
```