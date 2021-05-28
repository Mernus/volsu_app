import os

from minio import Minio

# Media storage
DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"

# Minio
MINIO_STORAGE_ENDPOINT = os.getenv('MINIO_STORAGE_ENDPOINT', '172.17.0.1:9000')
MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_STORAGE_ACCESS_KEY', 'access_key')
MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_STORAGE_SECRET_KEY', 'secret_key')
MINIO_STORAGE_USE_HTTPS = bool(int(os.getenv('MINIO_STORAGE_USE_HTTPS', 0)))
MINIO_STORAGE_MEDIA_BUCKET_NAME = os.getenv('MINIO_STORAGE_MEDIA_BUCKET_NAME', 'media')
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = bool(int(os.getenv('MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET', 1)))

minio_url = f"http{'s' if MINIO_STORAGE_USE_HTTPS else ''}://" \
            f"{MINIO_STORAGE_ENDPOINT}/" \
            f"{MINIO_STORAGE_MEDIA_BUCKET_NAME}/"
MINIO_URL = os.getenv('MINIO_SERVER_URL', minio_url)

# MINIO_CLIENT = Minio(endpoint=MINIO_STORAGE_ENDPOINT,
#                      access_key=MINIO_STORAGE_ACCESS_KEY,
#                      secret_key=MINIO_STORAGE_SECRET_KEY)
