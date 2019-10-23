from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.test import TestCase, override_settings, RequestFactory

from profiles.factories import ProfileFactory
from profiles.mixins import profile_filled

EXPECTED_RESULT = HttpResponse('')


@profile_filled
def profile_filled_view(request):
    return EXPECTED_RESULT


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileFilledDecoratorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    def setUp(self) -> None:
        self.request = self.factory.get('/')
        self.view = profile_filled_view

        # Set up session and messages middleware
        setattr(self.request, 'session', 'session')
        self.messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', self.messages)

    def test_not_redirected_if_profile_filled(self):
        user = ProfileFactory()
        self.request.user = user

        response = profile_filled_view(self.request)

        self.assertEqual(response, EXPECTED_RESULT)

    def test_not_redirected_if_anonymous_user(self):
        self.request.user = AnonymousUser()

        response = self.view(self.request)
        self.assertEqual(response, EXPECTED_RESULT)

    def test_redirected_if_profile_not_filled(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        response = self.view(self.request)
        self.assertNotEqual(response, EXPECTED_RESULT)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], '/profile')

    def test_message_added_on_redirect(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        response = self.view(self.request)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(self.messages._queued_messages), 1)
        self.assertEqual(str(self.messages._queued_messages[0].message), 'You should fill out profile')
