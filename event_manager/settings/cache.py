import os

# Redis
REDIS_URL = os.getenv('STACKHERO_REDIS_URL_TLS')

# Cache and sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'MAX_ENTRIES': 10000
        },
        "KEY_PREFIX": "emanager",
        "TIMEOUT": 432000,
    }
}
