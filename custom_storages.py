
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting
from django.utils.deconstruct import deconstructible
from django import template

@deconstructible
class PrivStorage(S3Boto3Storage):

    custom_domain = None
    signature_version = 's3'
    bucket_name = settings.AWS_PRIVSTORAGE_BUCKET_NAME
    location = settings.STATICFILES_LOCATION

s3_priv_storage = PrivStorage()


from django.conf import settings

register = template.Library()
@register.filter
def cdn_url(value):
    if settings.DEVELOPMENT:
        return value
    if settings.AWS_S3_ENDPOINT_URL in value:
        cdn_domain = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN
        new_url = value.replace(settings.AWS_S3_ENDPOINT_URL, cdn_domain)
        return new_url
    else:
        return value