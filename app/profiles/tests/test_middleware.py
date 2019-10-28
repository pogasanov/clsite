from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from profiles.factories import ProfileFactory
from profiles.middleware import InternalPagesMiddleware


class InternalPagesMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.EXPECTED_RESULT = HttpResponse('')

    def setUp(self) -> None:
        self.request = self.factory.get('/')
        self._get_messages_container(self.request)
        self.view = lambda *args: self.EXPECTED_RESULT
        self.mm = InternalPagesMiddleware(self.view)

    def _get_messages_container(self, request):
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return messages

    def test_redirected_if_anonymous_user_and_path_not_exempt(self):
        self.request.user = AnonymousUser()

        with self.settings(PUBLIC_PAGES=()):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 302)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response._headers['location'][1], f"{reverse('login')}?next=/")

    def test_not_redirected_if_anonymous_user_and_path_exempt(self):
        self.request.user = AnonymousUser()

        with self.settings(PUBLIC_PAGES=('/',)):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_not_redirected_if_logged_and_signup_complete(self):
        user = ProfileFactory()
        self.request.user = user

        with self.settings(PUBLIC_PAGES=()):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response, self.EXPECTED_RESULT)

    def test_redirected_if_logged_and_profile_empty(self):
        user = ProfileFactory(empty_profile=True)
        self.request.user = user

        with self.settings(PUBLIC_PAGES=()):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 302)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response._headers['location'][1], reverse('profile'))

    def test_redirected_if_logged_and_no_attorney_proof(self):
        user = ProfileFactory(no_attorney_proof=True)
        self.request.user = user

        with self.settings(PUBLIC_PAGES=()):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 302)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response._headers['location'][1], reverse('profile-proof'))

    def test_redirected_if_logged_and_email_not_confirmed(self):
        user = ProfileFactory(email_not_confirmed=True)
        self.request.user = user

        with self.settings(PUBLIC_PAGES=()):
            response = self.mm(self.request)
        self.assertTrue(response.status_code, 302)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response._headers['location'][1], reverse('profile-email-confirmation'))
