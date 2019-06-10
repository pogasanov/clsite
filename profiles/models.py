from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os

from .choices import USA_STATES


def get_image_path(instance, filename):
    return os.path.join(filename)


class Profile(models.Model):
    USA_STATES = USA_STATES

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jurisdiction = models.CharField(max_length=2, choices=USA_STATES, verbose_name='Jurisdiction', blank=True)
    headline = models.CharField(max_length=120, verbose_name='Headline', blank=True)
    bio = models.TextField(verbose_name='Bio', blank=True)
    website = models.URLField(verbose_name='Website URL', blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to=get_image_path, default='dummy-img.png', storage=S3Boto3Storage())
