from django.test import TestCase, override_settings
from django.urls import reverse

from profiles.forms import ProfileCreationForm


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.REGISTER_URL = '/register'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_view_uses_correct_form(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertIsInstance(response.context['form'], ProfileCreationForm)
