import sys

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from profiles.factories import ProfileFactory
from profiles.models import Profile


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_credentials = {
            "full_name": "Test User",
            "email": "test_user@gmail.com",
            "password": "test_password",
        }
        cls.credentials = {
            "username": "test_user@gmail.com",  # because we overwrote username field with email field
            "password": "test_password",
        }
        cls.incorrect_credentials = {"username": "test_user@gmail.com", "password": "INCORRECT"}

        cls.new_user_data = {
            "full_name": "Test User",
            "email": "test_user_new@gmail.com",
            "password1": "test_password",
            "password2": "test_password",
            "agree_tos": "on",
        }
        cls.incorrect_new_user_data = {
            "full_name": "Test User",
            "email": "test_user@gmail.com",
            "password1": "test_password",
            "password2": "test_password",
        }
        cls.correct_update_data = {
            "full_name": "John Doe",
            "summary": "Test Summary for having 5 years of experience in the field of shipping.",
            "bio": "Test bio",
            "phone": "+7(923)111-11-11",
            "email": "test@example.com",
            "website": "http://www.test.com",
            "twitter": "Test twitter",
            "linkedin": "Test linkedin",
            "facebook": "Test facebook",
            "preferred_communication_method": 0,
            "experience": "",
            "publish_to_thb": True,
            "law_type_tags": ["Pre-nuptial Agreement", "Business Law"],
            "country": "United States of America",
            "state": "Alabama",
            "city": "City",
            "languages": [{"name": "en", "proficiency_level": "NS"}],
            "jurisdictions": [
                {"country": "United States of America", "state": "New York", "city": "New York"}
            ],
        }

    def setUp(self):
        self.user = ProfileFactory(**self.signup_credentials)
        self.user.set_password(self.signup_credentials["password"])
        self.user.save()

    def test_python_version_correct(self):
        self.assertEqual(sys.version_info.major, 3)
        self.assertEqual(sys.version_info.minor, 7)

    def test_fixtures_faker_correct(self):
        call_command("loaddata", "admin", verbosity=0)
        call_command("loaddata", "handcrafted", verbosity=0)
        call_command("generateprofiles", 100, verbosity=0)

    def test_generate_profiles_working(self):
        GENERATED_MODELS_COUNT = 25

        existing_profiles_count = Profile.objects.count()

        ProfileFactory.create_batch(GENERATED_MODELS_COUNT)

        new_profiles_count = Profile.objects.count()

        self.assertEqual(new_profiles_count, existing_profiles_count + GENERATED_MODELS_COUNT)

    def test_login(self):
        # User go to homepage
        response = self.client.get("/")
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get("/profile")
        # Expects 302 and redirected to login page
        self.assertRedirects(response, "/login?next=/profile")

        # User types incorrectly
        response = self.client.post("/login?next=/profile", self.incorrect_credentials)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_active)

        # User types correctly
        response = self.client.post("/login?next=/profile", self.credentials, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, "/profile")
        self.assertTrue(response.context["user"].is_active)

    def test_logout(self):
        # User is already logged in
        self.client.force_login(self.user)

        # User goes to profile
        response = self.client.get("/profile")
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to logout
        response = self.client.get("/logout", follow=True)
        # Expects 302 and redirected to homepage
        self.assertRedirects(response, "/")

        # User is logged out
        self.assertFalse(response.context["user"].is_active)

    def test_signup_flow(self):
        # User go to homepage
        response = self.client.get(reverse("home"))
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get(reverse("register"))
        # Expects 302 and redirected to login page
        self.assertEqual(response.status_code, 200)

        # User types incorrectly
        response = self.client.post(reverse("register"), self.incorrect_new_user_data)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_active)

        # User types correctly
        response = self.client.post(reverse("register"), self.new_user_data, follow=True)
        # Expects 302 and redirect to profile
        self.assertRedirects(response, reverse("profile"))
        self.assertTrue(response.context["user"].is_active)

        user = Profile.objects.get(email=self.new_user_data["email"])

        # Temporary hack to set email not confirmed while email story is not yet implemented
        user.email_confirmed_at = None
        user.save()

        # User tries to leave profile
        response = self.client.get(reverse("profiles"))
        # Expects 302 and redirect to profile
        self.assertRedirects(response, reverse("profile"))

        # Users fills out required fields
        response = self.client.patch(
            reverse("api-profile"), self.correct_update_data, content_type="application/json"
        )
        # Expects 200
        self.assertEqual(response.status_code, 200)

        # User tries to leave profile
        response = self.client.get(reverse("profiles"))
        # Expects 302 and redirect to profile attorney proof
        self.assertRedirects(response, reverse("profile-proof"))

        # User fills attorney proof
        response = self.client.post(
            reverse("profile-proof"),
            {
                "passport_photo": ProfileFactory.create_passport_photo(),
                "bar_license_photo": ProfileFactory.create_bar_license_photo(),
                "attorney_confirm": "on",
            },
            follow=True,
        )

        # Expects 302 and redirect to email confirmation
        self.assertRedirects(response, reverse("profile-email-confirmation"))

        # User confirms email
        user.refresh_from_db()
        user.email_confirmed_at = timezone.now()
        user.save()

        # User tries to leave profile
        response = self.client.get(reverse("profiles"))
        # Expects 200
        self.assertEqual(response.status_code, 200)
