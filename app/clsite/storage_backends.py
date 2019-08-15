from django.conf import settings
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage


def variativeStorage():
    """Return S3Boto3Storage if access key is defined.
    Fallback to default storage.
    """
    if hasattr(settings, 'AWS_ACCESS_KEY_ID') and settings.AWS_ACCESS_KEY_ID:
        return S3Boto3Storage()
    return default_storage
