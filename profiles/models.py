from django.db import models
from django.conf import settings

from .choices import USA_STATES


class Profile(models.Model):
    USA_STATES = USA_STATES

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jurisdiction = models.CharField(max_length=2, choices=USA_STATES, verbose_name='Jurisdiction')
