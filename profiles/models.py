from django.db import models
from django.conf import settings
import os

from .choices import USA_STATES


def get_image_path(instance, filename):
    return os.path.join(filename)


class Profile(models.Model):
    USA_STATES = USA_STATES

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jurisdiction = models.CharField(max_length=2, choices=USA_STATES, verbose_name='Jurisdiction', blank=True)
    photo = models.ImageField(upload_to=get_image_path, default='dummy-img.png')
