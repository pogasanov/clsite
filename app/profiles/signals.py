from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Profile, Language


@receiver(post_save, sender=Profile)
def create_default_language_for_profile(sender, instance, created, **kwargs):
    if created:
        Language.objects.create(profile=instance, name=settings.DEFAULT_USER_LANGUAGE)