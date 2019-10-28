from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from profiles.middlewares import InternalPagesMiddleware


class InternalPagesMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.EXPECTED_RESULT = HttpResponse('')
        cls.view = lambda x, y: cls.EXPECTED_RESULT

    def setUp(self) -> None:
        self.request = self.factory.get('/')
        self.mm = InternalPagesMiddleware()

    def test_redirected_if_anonymous_user(self):
        self.request.user = AnonymousUser()

        response = self.mm.process_view(self.request, self.view, [], {})
        self.assertNotEqual(response, self.EXPECTED_RESULT)
        self.assertTrue(response.status_code, 302)
        self.assertEqual(response._headers['location'][1], f"{reverse('login')}?next=/")
