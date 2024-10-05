from decouple import config
from .base import *

DEBUG = False


ADMINS = [
    ("Asante Prince", "princeaffumasante@gmail.com"),
]


ALLOWED_HOSTS = ["coursity.com", "www.coursityproject.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

REDIS_URL = "redis://cache:6379"
CACHES["default"]["LOCATION"] = REDIS_URL
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]
