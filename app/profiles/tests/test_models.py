from django.test import TestCase, override_settings

from profiles.factories import ProfileFactory
from profiles.models import Profile


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
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile._meta.get_field('email_confirmed_at').verbose_name, 'email confirmed at')
        self.assertTrue(profile._meta.get_field('email_confirmed_at').null)
        self.assertTrue(profile._meta.get_field('email_confirmed_at').blank)
