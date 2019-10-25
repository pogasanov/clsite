from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings

from profiles.factories import ProfileFactory
from reviews.factories import ReviewFactory


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReviewModelTest(TestCase):

    def test_sender_eq_receiver_fail(self):
        profile = ProfileFactory()
        with self.assertRaises(ValidationError):
            ReviewFactory(created_by=profile, sent_to=profile)

    def test_unique_composite_key_fail(self):
        created_by = ProfileFactory()
        sent_to = ProfileFactory()
        with self.assertRaises(IntegrityError):
            for i in range(2):
                ReviewFactory(created_by=created_by, sent_to=sent_to)
