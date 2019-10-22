from django.test import TestCase, override_settings


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.REGISTER_URL = '/register'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEqual(response.status_code, 200)
