from django.test import TestCase, override_settings

from profiles.forms import ProfileCreationForm


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_payload = {
            'email': 'test@test.com',
            'password1': 'c0mpl1xp4ssw0rd',
            'password2': 'c0mpl1xp4ssw0rd',
            'agree_tos': 'on'
        }

    def test_valid_with_correct_payload(self):
        form = ProfileCreationForm(data=self.data_payload)
        self.assertTrue(form.is_valid())
