import os
from pathlib import Path
from dotenv import load_dotenv
import django_heroku

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&u@2d$fi47oaawy#os8ak*nn7zx_g7e$!ci*w=&i(8#j^xs@%^"

IS_HEROKU_APP = os.getenv("HEROKU_APP")

# SECURITY WARNING: don't run with debug turned on in production!
if IS_HEROKU_APP:
    DEBUG = False
else:
    DEBUG = True

HOST_NAME = os.getenv("HOST_NAME")
CSRF_TRUSTED_ORIGINS = [f"https://{HOST_NAME}", "http://tripway.cc"]

if IS_HEROKU_APP:
    ALLOWED_HOSTS = [f"{HOST_NAME}"]
else:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        HOST_NAME,
    ]

SITE_ID = 5

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.line",
    "members",
    "schedules",
    "trips",
    "spots",
    "payments",
    "comments",
    "notifies",
    "blogs",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    'ckeditor_uploader',
    "django_ckeditor_5",
]
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_5_CONFIGS = {
    'blog': {
        'toolbar': [
            'heading', '|', 'fontSize', 'fontColor', 'fontBackgroundColor', '|',
            'bold', 'italic', 'underline', 'link', 'bulletedList', 
            'numberedList', 'blockQuote', '|',
            'alignment', 'indent', 'outdent', '|', 'undo', 'redo'
        ],
        'language': 'de'
    }
}


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "line": {
        "APP": {
            "client_id": os.getenv("LINE_CLIENT_ID"),
            "secret": os.getenv("LINE_CLIENT_SECRET"),
        },
        "SCOPE": ["profile", "openid", "email"],
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifies.context_processors.notification_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if IS_HEROKU_APP:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "TripWay",
            "USER": os.getenv("YOUR_USER_NAME"),
            "PASSWORD": os.getenv("YOUR_PASSWORD"),
            "HOST": "localhost",
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
if IS_HEROKU_APP:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "members.Member"

AUTHENTICATION_BACKENDS = (
    "members.backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_URL = "/members/login/"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_LOGIN_ON_GET = True


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = os.getenv("AWS_S3_SIGNATURE_NAME", "s3v4")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

django_heroku.settings(config=locals(), staticfiles=False, logging=False)
