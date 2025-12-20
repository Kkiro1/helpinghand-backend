from .settings import *  # noqa

# Make CI deterministic and fast
DEBUG = False
SECRET_KEY = "ci-secret-key"
ALLOWED_HOSTS = ["*"]

# Use in-memory sqlite for CI tests (fast + no files)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Faster password hashing in CI
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Avoid external email usage
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
