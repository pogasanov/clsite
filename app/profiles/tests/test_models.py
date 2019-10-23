from django.test import TestCase, override_settings

from clsite.storage_backends import variativeStorage
from profiles.factories import ProfileFactory
from profiles.models import Profile, get_image_path


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProfileFactory()

    def test_register_status_default(self):
        profile = ProfileFactory(empty_profile=True)
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_EMPTY_PROFILE)

    def test_is_filled(self):
        profile = ProfileFactory(empty_profile=True)
        self.assertFalse(profile.is_filled())

        profile.full_name = 'Dummy full name'
        profile.save()
        self.assertTrue(profile.is_filled())

    def test_email_confirmed_at_meta(self):
        profile = Profile.objects.first()
        self.assertEqual(profile._meta.get_field('email_confirmed_at').verbose_name, 'email confirmed at')
        self.assertTrue(profile._meta.get_field('email_confirmed_at').null)
        self.assertTrue(profile._meta.get_field('email_confirmed_at').blank)

    def test_email_confirmed_by_default(self):
        profile = Profile.objects.first()
        self.assertIsNotNone(profile.email_confirmed_at)

    def test_passport_photo_meta(self):
        profile = Profile.objects.first()
        self.assertEqual(profile._meta.get_field('passport_photo').verbose_name, 'Passport photo')
        self.assertEqual(profile._meta.get_field('passport_photo').upload_to, get_image_path)
        self.assertEqual(profile._meta.get_field('passport_photo').storage, variativeStorage())
        self.assertTrue(profile._meta.get_field('passport_photo').null)
        self.assertTrue(profile._meta.get_field('passport_photo').blank)

    def test_bar_license_photo_meta(self):
        profile = Profile.objects.first()
        self.assertEqual(profile._meta.get_field('bar_license_photo').verbose_name, 'Bar license photo')
        self.assertEqual(profile._meta.get_field('bar_license_photo').upload_to, get_image_path)
        self.assertEqual(profile._meta.get_field('bar_license_photo').storage, variativeStorage())
        self.assertTrue(profile._meta.get_field('bar_license_photo').null)
        self.assertTrue(profile._meta.get_field('bar_license_photo').blank)
