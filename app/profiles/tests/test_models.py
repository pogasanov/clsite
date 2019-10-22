from django.test import TestCase, override_settings

from profiles.factories import ProfileFactory
from profiles.models import Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileTest(TestCase):
    def test_register_status_default(self):
        profile = ProfileFactory(empty_profile=True)
        self.assertEqual(profile.register_status, Profile.REGISTER_STATUS_EMPTY_PROFILE)
