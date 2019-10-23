from django.contrib.messages.storage.fallback import FallbackStorage
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

        # Set up session and messages middleware
        setattr(self.request, 'session', 'session')
        self.messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', self.messages)

    def test_not_redirected_if_profile_filled(self):
        user = ProfileFactory()
        self.request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_not_redirected_if_anonymous_user(self):
        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_not_redirected_if_request_profile_page(self):
        request = self.factory.get('/profile')
        user = ProfileFactory()
        request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(request)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_redirected_if_profile_not_filled(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/profile')

    def test_message_added_on_redirect(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        middleware = ProfileFilledMiddleware(self.get_response)
        response = middleware(self.request)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(self.messages._queued_messages), 1)
        self.assertEqual(str(self.messages._queued_messages[0].message), 'You should fill out profile')
