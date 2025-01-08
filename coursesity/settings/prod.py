from decouple import config
from .base import *

DEBUG = False


ADMINS = [
    ("Asante Prince", "princeaffumasante@gmail.com"),
]


ALLOWED_HOSTS = ["coursity.com", "www.coursityproject.com", "*"]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("POSTGRES_DB", "db_name"),
#         "USER": config("POSTGRES_USER", "db_user"),
#         "PASSWORD": config("POSTGRES_PASSWORD", "db_password"),
#         "HOST": "db",
#         "PORT": 5432,
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REDIS_URL = "redis://cache:6379"
CACHES["default"]["LOCATION"] = REDIS_URL
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]

# SECURITY
CSRF_COOKIE_SECURE = True  # transfer cookie over https only
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
