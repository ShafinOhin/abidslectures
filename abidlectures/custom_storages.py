
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting
from django.utils.deconstruct import deconstructible

@deconstructible
class PrivStorage(S3Boto3Storage):

    custom_domain = None
    signature_version = 's3'
    bucket_name = settings.AWS_PRIVSTORAGE_BUCKET_NAME
    location = settings.STATICFILES_LOCATION

s3_priv_storage = PrivStorage()