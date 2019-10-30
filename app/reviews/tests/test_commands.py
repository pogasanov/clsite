from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings, TransactionTestCase

from profiles.factories import ProfileFactory
from reviews.models import Review


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GenerateReviewsCommandTest(TransactionTestCase):
    REVIEWS_TO_CREATE = 20

    def test_generatereviews(self):
        PROFILES_TO_CREATE = 10

        ProfileFactory.create_batch(PROFILES_TO_CREATE)
        call_command('generatereviews', reviews_count=self.REVIEWS_TO_CREATE)
        review_count = Review.objects.count()
        self.assertEqual(review_count, self.REVIEWS_TO_CREATE)

    def test_generatereviews_without_profiles_fail(self):
        with self.assertRaises(CommandError):
            call_command('generatereviews')

    def test_generatereviews_with_profiles_flag(self):
        call_command('generatereviews', generate_profiles=True, reviews_count=self.REVIEWS_TO_CREATE)
