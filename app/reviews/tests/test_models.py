from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings

from profiles.factories import ProfileFactory
from reviews.factories import ReviewFactory
from reviews.models import Review


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReviewModelTest(TestCase):

    def test_sender_eq_receiver_fail(self):
        profile = ProfileFactory()
        with self.assertRaises(ValidationError):
            ReviewFactory(sender=profile, receiver=profile)

    def test_unique_composite_key_fail(self):
        sender = ProfileFactory()
        receiver = ProfileFactory()
        with self.assertRaises(IntegrityError):
            for i in range(2):
                ReviewFactory(sender=sender, receiver=receiver)
