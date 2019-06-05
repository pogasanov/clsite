from django.test import TestCase
from django.contrib.auth import get_user_model


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
