from django.test import TestCase, override_settings, RequestFactory

from profiles.factories import ProfileFactory
from profiles.middlewares import ProfileFilledMiddleware


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileFilledMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.EXPECTED_RESULT = object()
        cls.get_response = lambda x, y: cls.EXPECTED_RESULT

    def setUp(self) -> None:
        self.request = self.factory.get('/')

    def test_not_redirected_if_profile_filled(self):
        user = ProfileFactory()
        self.request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_redirected_if_profile_not_filled(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/profile')
