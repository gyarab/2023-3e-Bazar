from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

with open("config.json") as config_file:
    config = json.load(config_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = config["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
# TODO false az bude ready
DEBUG = True

# TODO: update this just to the domovprojekt.com and turn on the cloudflare tunnel
# These are allowed hosts that can host our server
ALLOWED_HOSTS = ["192.168.88.22", "domovprojekt.com"]

# points to the media folder
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# points to where shuld be user redirected after login in/out
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

#! i aint even sure what in the hell that is
SITE_ID = 5

# installed apps in use
INSTALLED_APPS = [
    # default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # all the created apps
    "homepage",
    "profilepage",
    "chat",
    # other apps
    "widget_tweaks",
    "ckeditor",
    "ckeditor_uploader",
    # apps needed for google login
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # captcha
    "captcha",
    # paypal
    "paypal.standard.ipn",
]

# allauth settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}
SOCIALACCOUNT_LOGIN_ON_GET = True

# middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "Bazar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Bazar.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config["DATABASE_NAME"],
        "USER": config["DATABASE_USER"],
        "PASSWORD": config["DATABASE_USER_PASSWORD"],
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# language in which the app is programed
LANGUAGE_CODE = "en-us"

# time zone
TIME_ZONE = "CET"

USE_I18N = True

USE_TZ = True

# points to the static folder
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# allauth settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# ckeditor config part of settings
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "n1theme",
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format", "Font", "FontSize"],
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Cut", "Copy", "Paste", "PasteText"],
            ["Image"],
        ],
        "extraPlugins": "image2",
        "filebrowserBrowseUrl": "",
    }
}

# path to where
CKEDITOR_UPLOAD_PATH = "uploads/"

# paypal settings
PAYPAL_RECEIVER_EMAIL = config["PAYPAL_EMAIL"]
PAYPAL_TEST = True

# email backend settings
# TODO still not working
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.seznam.cz'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]

# trusted origins of the CSRF token
CSRF_TRUSTED_ORIGINS = ["http://192.168.88.22", "http://domovprojekt.com"]

# default paypal button
PAYPAL_BUY_BUTTON_IMAGE = "/media/images/paypal.jpg"
