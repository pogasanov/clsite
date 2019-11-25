from django.contrib.admin import AdminSite
from django.test import TestCase, override_settings

from clsite import settings
from profiles.factories import ProfileFactory
from reviews.admin import ReviewAdmin
from reviews.factories import ReviewFactory
from reviews.models import Review


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReviewAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileFactory(is_staff=True, is_superuser=True)
        cls.admin = ReviewAdmin(Review, AdminSite())

    def setUp(self):
        self.client.login(username=self.user.email, password=settings.DEFAULT_USER_PASSWORD)

    def test_payment_direction(self):
        review = ReviewFactory(is_sender_principal=True)
        self.assertIn('custom-arrow-right', self.admin.payment_direction(review))

        review = ReviewFactory(is_sender_principal=False)
        self.assertIn('custom-arrow-left', self.admin.payment_direction(review))

        review = ReviewFactory(is_sender_principal=None)
        response = self.admin.payment_direction(review).split('  ')
        self.assertIn('custom-arrow-left', response[0])
        self.assertIn('custom-arrow-right', response[1])

    def test_rating_integer(self):
        review = ReviewFactory()
        self.assertIsInstance(self.admin.get_rating(review), int)
