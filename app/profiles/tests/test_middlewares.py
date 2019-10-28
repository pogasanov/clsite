from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from profiles.factories import ProfileFactory
from profiles.middlewares import InternalPagesMiddleware


class InternalPagesMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.EXPECTED_RESULT = HttpResponse('')

    def setUp(self) -> None:
        self.request = self.factory.get('/')
        self.view = lambda *args: self.EXPECTED_RESULT
        self.mm = InternalPagesMiddleware()

    def test_redirected_if_anonymous_user(self):
        self.request.user = AnonymousUser()

        response = self.mm.process_view(self.request, self.view, [], {})
        self.assertTrue(response.status_code, 302)
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertEqual(response._headers['location'][1], f"{reverse('login')}?next=/")

    def test_not_redirected_if_logged(self):
        user = ProfileFactory()
        self.request.user = user

        response = self.mm.process_view(self.request, self.view, [], {})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response, self.EXPECTED_RESULT)
