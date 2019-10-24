from django.test import TestCase, override_settings

from profiles.forms import ProfileCreationForm


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
        self.assertEqual(form.fields['agree_tos'].label, 'I agree to the T&S')
