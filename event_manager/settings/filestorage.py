import os

# Media storage
DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"

# Minio
MINIO_STORAGE_ENDPOINT = os.getenv('MINIO_STORAGE_ENDPOINT', '172.17.0.1:9000')
MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_STORAGE_ACCESS_KEY', 'access_key')
MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_STORAGE_SECRET_KEY', 'secret_key')
MINIO_STORAGE_USE_HTTPS = bool(int(os.getenv('MINIO_STORAGE_USE_HTTPS', 0)))
MINIO_STORAGE_MEDIA_BUCKET_NAME = os.getenv('MINIO_STORAGE_MEDIA_BUCKET_NAME', 'media')
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = bool(int(os.getenv('MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET', 1)))

# Folder with test images
MINIO_TEST_IMAGES = os.getenv('MINIO_TEST_IMAGES', 'test_images')
