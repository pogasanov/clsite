from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from profiles.factories import ProfileFactory


class ProfileViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VIEW_URL = '/api/profile'
        cls.user = ProfileFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('api-profile'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cant_access(self):
        self.client.logout()

        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_profile(self):
        response = self.client.delete(self.VIEW_URL)
        self.assertEqual(response.status_code, 405)
