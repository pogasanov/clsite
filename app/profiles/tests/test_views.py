from django.test import TestCase, override_settings
from django.urls import reverse

from profiles.factories import ProfileFactory
from profiles.forms import ProfileCreationForm
from profiles.models import Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.REGISTER_URL = '/register'
        cls.NEW_PROFILE_EMAIL = 'test@test.com'
        cls.data_payload = {
            'email': cls.NEW_PROFILE_EMAIL,
            'password1': 'c0mpl1xp4ssw0rd',
            'password2': 'c0mpl1xp4ssw0rd',
            'agree_tos': 'on'
        }

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_view_uses_correct_form(self):
        response = self.client.get(self.REGISTER_URL)
        self.assertIsInstance(response.context['form'], ProfileCreationForm)

    def test_redirected_to_profile_after_register(self):
        response = self.client.post(self.REGISTER_URL, data=self.data_payload)
        self.assertRedirects(response, '/profile')

    def test_user_created(self):
        profiles_count_before = Profile.objects.count()

        response = self.client.post(self.REGISTER_URL, data=self.data_payload)
        self.assertRedirects(response, '/profile')

        profiles_after = Profile.objects.all()
        self.assertEqual(profiles_count_before + 1, profiles_after.count())

        last_profile = profiles_after.last()
        self.assertEqual(last_profile.email, self.NEW_PROFILE_EMAIL)

    def test_user_logged_on_register(self):
        response = self.client.post(self.REGISTER_URL, data=self.data_payload, follow=True)
        self.assertRedirects(response, '/profile')

        self.assertTrue(response.context['user'].is_active)

    def test_redirected_to_profile_if_profile_is_not_filled(self):
        user = ProfileFactory(empty_profile=True)
        self.client.force_login(user)

        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/profile')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VIEW_URL = '/profile'

    def setUp(self):
        self.user = ProfileFactory()
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('profile-proof'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.VIEW_URL)
        self.assertTemplateUsed(response, 'profile-page.html')

    def test_anonymous_user_cant_access(self):
        self.client.logout()

        response = self.client.get(self.VIEW_URL)
        self.assertRedirects(response, f"{reverse('login')}?next={self.VIEW_URL}")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileProofViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VIEW_URL = '/profile/proof'

    def setUp(self):
        self.data_payload = {
            'passport_photo': ProfileFactory.create_passport_photo(),
            'bar_license_photo': ProfileFactory.create_bar_license_photo()
        }
        self.user = ProfileFactory(no_attorney_proof=True)
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('profile-proof'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.VIEW_URL)
        self.assertTemplateUsed(response, 'profiles/profile_proof.html')

    def test_anonymous_user_cant_access(self):
        self.client.logout()

        response = self.client.get(self.VIEW_URL)
        self.assertRedirects(response, f"{reverse('login')}?next={self.VIEW_URL}")

    def test_redirects_if_profile_is_not_filled(self):
        user = ProfileFactory(empty_profile=True)
        self.client.force_login(user)

        response = self.client.get(self.VIEW_URL)
        self.assertRedirects(response, '/profile')

    def test_view_object_is_current_user(self):
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.context['object'], self.user)

    def test_shows_correct_fields(self):
        response = self.client.get(self.VIEW_URL)
        self.assertIn('passport_photo', response.context['form'].fields)
        self.assertIn('bar_license_photo', response.context['form'].fields)

    def test_redirects_to_itself_when_submitted(self):
        response = self.client.post(self.VIEW_URL, data=self.data_payload)
        self.assertRedirects(response, self.VIEW_URL)

    def test_save_changes_on_valid_payload(self):
        self.assertFalse(self.user.passport_photo)
        self.assertFalse(self.user.bar_license_photo)

        self.client.post(self.VIEW_URL, data=self.data_payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.passport_photo)
        self.assertTrue(self.user.bar_license_photo)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileEmailConfirmationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VIEW_URL = '/profile/email'
        cls.user = ProfileFactory(email_not_confirmed=True)

    def setUp(self):
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('profile-email-confirmation'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.VIEW_URL)
        self.assertTemplateUsed(response, 'profiles/profile_email_confirmation.html')

    def test_anonymous_user_cant_access(self):
        self.client.logout()

        response = self.client.get(self.VIEW_URL)
        self.assertRedirects(response, f"{reverse('login')}?next={self.VIEW_URL}")

    def test_user_with_confirmed_email_cant_access(self):
        user = ProfileFactory()
        self.client.force_login(user)

        response = self.client.get(reverse('profile-email-confirmation'))
        self.assertRedirects(response, reverse('profile'))
