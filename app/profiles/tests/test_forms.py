from django.test import TestCase, override_settings
from django.utils.safestring import mark_safe

from profiles.factories import ProfileFactory
from profiles.forms import ProfileCreationForm, ProfileProofForm


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_payload = {
            'full_name': 'Test User',
            'email': 'test@test.com',
            'password1': 'c0mpl1xp4ssw0rd',
            'password2': 'c0mpl1xp4ssw0rd',
            'agree_tos': 'on'
        }

    def test_valid_with_correct_payload(self):
        form = ProfileCreationForm(data=self.data_payload)
        self.assertTrue(form.is_valid())

    def test_requires_full_name(self):
        INVALID_PAYLOAD = dict(self.data_payload)
        del INVALID_PAYLOAD['full_name']
        form = ProfileCreationForm(data=INVALID_PAYLOAD)
        self.assertFalse(form.is_valid())

    def test_requires_email(self):
        INVALID_PAYLOAD = dict(self.data_payload)
        del INVALID_PAYLOAD['email']
        form = ProfileCreationForm(data=INVALID_PAYLOAD)
        self.assertFalse(form.is_valid())

    def test_requires_password(self):
        INVALID_PAYLOAD = dict(self.data_payload)
        del INVALID_PAYLOAD['password1']
        form = ProfileCreationForm(data=INVALID_PAYLOAD)
        self.assertFalse(form.is_valid())

    def test_requires_password_confirm(self):
        INVALID_PAYLOAD = dict(self.data_payload)
        del INVALID_PAYLOAD['password2']
        form = ProfileCreationForm(data=INVALID_PAYLOAD)
        self.assertFalse(form.is_valid())

    def test_requires_agree_tos(self):
        INVALID_PAYLOAD = dict(self.data_payload)
        del INVALID_PAYLOAD['agree_tos']
        form = ProfileCreationForm(data=INVALID_PAYLOAD)
        self.assertFalse(form.is_valid())

    def test_full_name_placeholder(self):
        form = ProfileCreationForm()
        self.assertEqual(form.fields['full_name'].widget.attrs['placeholder'], 'Full name...')

    def test_email_placeholder(self):
        form = ProfileCreationForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email...')

    def test_password_placeholder(self):
        form = ProfileCreationForm()
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Password...')

    def test_password_repeat_placeholder(self):
        form = ProfileCreationForm()
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Repeat password...')

    def test_agree_tos_label(self):
        form = ProfileCreationForm()
        self.assertEqual(form.fields['agree_tos'].label, mark_safe(
            'I agree to the <a href="/privacy-terms-and-conditions" _target="blank">Terms and Conditions</a>'))


class ProfileProofFormTest(TestCase):
    def setUp(self):
        self.data_payload = {
            'passport_photo': ProfileFactory.create_passport_photo(),
            'bar_license_photo': ProfileFactory.create_bar_license_photo(),
        }

    def test_valid_with_correct_payload(self):
        form = ProfileProofForm(data=self.data_payload, files=self.data_payload)
        self.assertTrue(form.is_valid())

    def test_requires_passport_photo(self):
        del self.data_payload['passport_photo']
        form = ProfileProofForm(data=self.data_payload, files=self.data_payload)
        self.assertFalse(form.is_valid())
