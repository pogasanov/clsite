from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'test_user',
            'password': 'test_password'
        }
        cls.incorrect_credentials = {
            'username': 'test_user',
            'password': 'INCORRECT'
        }

        cls.new_user_data = {
            'username': 'test_user_new',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        cls.incorrect_new_user_data = {
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'test_password'
        }

    def setUp(self):
        get_user_model().objects.create_user(**self.credentials)

    def test_login(self):
        # User go to homepage
        response = self.client.get('/')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get('/profile')
        # Expects 302 and redirected to login page
        self.assertRedirects(response, '/login?next=/profile')

        # User types incorrectly
        response = self.client.post('/login?next=/profile', self.incorrect_credentials)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

        # User types correctly
        response = self.client.post('/login?next=/profile', self.credentials, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, '/profile')
        self.assertTrue(response.context['user'].is_active)

    def test_register(self):
        # User go to homepage
        response = self.client.get('/')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get('/register')
        # Expects 302 and redirected to login page
        self.assertEqual(response.status_code, 200)

        # User types incorrectly
        response = self.client.post('/register', self.incorrect_new_user_data)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

        # User types correctly
        response = self.client.post('/register', self.new_user_data, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, '/profile')
        self.assertTrue(response.context['user'].is_active)
