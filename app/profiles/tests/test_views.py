from django.test import TestCase, override_settings
from django.urls import reverse

from profiles.forms import ProfileCreationForm
from profiles.models import Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.REGISTER_URL = '/register'
        cls.NEW_PROFILE_EMAIL = 'test@test.com'
        cls.data_payload = {
            'email': cls.NEW_PROFILE_EMAIL,
            'password1': 'c0mpl1xp4ssw0rd',
            'password2': 'c0mpl1xp4ssw0rd',
            'agree_tos': 'on'
        }

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

    def test_user_created(self):
        profiles_count_before = Profile.objects.count()

        response = self.client.post(self.REGISTER_URL, data=self.data_payload)
        self.assertRedirects(response, '/profile')

        profiles_after = Profile.objects.all()
        self.assertEqual(profiles_count_before + 1, profiles_after.count())

        last_profile = profiles_after.last()
        self.assertEqual(last_profile.email, self.NEW_PROFILE_EMAIL)

    def test_user_logged_on_register(self):
        response = self.client.post(self.REGISTER_URL, data=self.data_payload, follow=True)
        self.assertRedirects(response, '/profile')

        self.assertTrue(response.context['user'].is_active)
