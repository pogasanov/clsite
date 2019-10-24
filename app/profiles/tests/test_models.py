from django.test import TestCase, override_settings
from django.utils import timezone

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
        filled_profile = ProfileFactory()
        self.assertTrue(filled_profile.is_filled())

        not_filled_profile = ProfileFactory()
        not_filled_profile.full_name = ''
        self.assertFalse(not_filled_profile.is_filled())

        not_filled_profile = ProfileFactory()
        not_filled_profile.jurisdiction_set.all().delete()
        self.assertFalse(not_filled_profile.is_filled())

        not_filled_profile = ProfileFactory()
        not_filled_profile.law_type_tags = ''
        self.assertFalse(not_filled_profile.is_filled())

        not_filled_profile = ProfileFactory()
        not_filled_profile.language_set.all().delete()
        self.assertFalse(not_filled_profile.is_filled())

    def test_email_confirmed_at_meta(self):
        profile = Profile.objects.first()
        field = profile._meta.get_field('email_confirmed_at')
        self.assertEqual(field.verbose_name, 'email confirmed at')
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.default, timezone.now)

    def test_email_confirmed_by_default(self):
        profile = Profile.objects.first()
        self.assertIsNotNone(profile.email_confirmed_at)

    def test_passport_photo_meta(self):
        profile = Profile.objects.first()
        field = profile._meta.get_field('passport_photo')
        self.assertEqual(field.verbose_name, 'Passport photo')
        self.assertEqual(field.upload_to, get_image_path)
        self.assertEqual(field.storage, variativeStorage())
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_bar_license_photo_meta(self):
        profile = Profile.objects.first()
        field = profile._meta.get_field('bar_license_photo')
        self.assertEqual(field.verbose_name, 'Bar license photo')
        self.assertEqual(field.upload_to, get_image_path)
        self.assertEqual(field.storage, variativeStorage())
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_register_status_correct(self):
        profile = ProfileFactory(empty_profile=True)
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_EMPTY_PROFILE)

        profile = ProfileFactory(no_attorney_proof=True)
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_NO_ATTORNEY_PROOF)

        profile = ProfileFactory(email_not_confirmed=True)
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_EMAIL_NOT_CONFIRMED)

        profile = ProfileFactory()
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_COMPLETE)

    def test_is_attorney_proof_submitted(self):
        profile = ProfileFactory(no_attorney_proof=True)
        self.assertFalse(profile.is_attorney_proof_submitted())

        profile.passport_photo = ProfileFactory.create_passport_photo()
        profile.bar_license_photo = ProfileFactory.create_bar_license_photo()
        profile.save()
        self.assertTrue(profile.is_attorney_proof_submitted())
