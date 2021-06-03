import datetime
import os

from cryptography.hazmat.primitives.hashes import SHA3_256

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'main.pagination.BasePagination',
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M",
}

LOGIN_URL = "/login/"
SIGNUP_URL = "/signup/"
LOGOUT_URL = "/logout/"

# JWT
SIGNING_KEY_FILE = os.getenv('RSA_KEYS_FOLDER') + "id_rsa"
VERIFYING_KEY_FILE = os.getenv('RSA_KEYS_FOLDER') + "id_rsa.pub"
SIMPLE_JWT = {
    'ALGORITHM': os.getenv('JWT_ALGORITHM'),
    'AUTH_HEADER_TYPES': os.getenv('JWT_AUTH_HEADER_PREFIX'),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(seconds=1800),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=5),
    'SIGNING_KEY': open(SIGNING_KEY_FILE).read(),
    'VERIFYING_KEY': open(VERIFYING_KEY_FILE).read(),
}

# Cryptography
CRYPTOGRAPHY_DIGEST = SHA3_256
