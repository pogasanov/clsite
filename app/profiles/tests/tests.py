import sys

from django.core.management import call_command
from django.test import TestCase, override_settings

from profiles.factories import ProfileFactory
from profiles.models import Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_credentials = {
            'full_name': 'Test User',
            'email': 'test_user@gmail.com',
            'password': 'test_password'
        }
        cls.credentials = {
            'username': 'test_user@gmail.com',  # because we overwrote username field with email field
            'password': 'test_password'
        }
        cls.incorrect_credentials = {
            'username': 'test_user@gmail.com',
            'password': 'INCORRECT'
        }

        cls.new_user_data = {
            'full_name': 'Test User',
            'email': 'test_user_new@gmail.com',
            'password1': 'test_password',
            'password2': 'test_password',
            'agree_tos': 'on'
        }
        cls.incorrect_new_user_data = {
            'full_name': 'Test User',
            'email': 'test_user@gmail.com',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        cls.correct_update_data = {
            'profile-full_name': 'John Doe',
            'profile-languages': 'ru,en',
            'profile-summary': 'Test Summary for having 5 years of experience in the field of shipping.',
            'profile-bio': 'Test bio',
            'profile-phone': '+7(923)111-11-11',
            'profile-email': 'test@example.com',
            'profile-website': 'http://www.test.com',
            'profile-twitter': 'Test twitter',
            'profile-linkedin': 'Test linkedin',
            'profile-facebook': 'Test facebook',
            'profile-preferred_communication_method': 0,
            'profile-experience': '',
            'profile-publish_to_thb': True,

            'address-country': 'United States of America',
            'address-state': 'Alabama',
            'address-city': 'City',
            'address-zipcode': '12345',
            'address-street': 'Street',
            'address-building': 'z',

            'lawschool-school': 'school',
            'lawschool-country': 'United States of America',
            'lawschool-state': 'Alabama',

            'jurisdiction-0-id': '',
            'jurisdiction-0-country': 'United States of America',
            'jurisdiction-0-state': 'Arizona',
            'jurisdiction-0-city': 'City',

            'language-0-name': 'en',
            'language-0-proficiency_level': 'NS',

            'education-TOTAL_FORMS': 0,
            'education-INITIAL_FORMS': 0,
            'admissions-TOTAL_FORMS': 0,
            'admissions-INITIAL_FORMS': 0,
            'workexperience-TOTAL_FORMS': 0,
            'workexperience-INITIAL_FORMS': 0,
            'organization-TOTAL_FORMS': 0,
            'organization-INITIAL_FORMS': 0,
            'award-TOTAL_FORMS': 0,
            'award-INITIAL_FORMS': 0,
            'jurisdiction-TOTAL_FORMS': 1,
            'jurisdiction-INITIAL_FORMS': 0,
            'language-TOTAL_FORMS': 1,
            'language-INITIAL_FORMS': 0

        }
        cls.incorrect_update_data = {
            'profile-full_name': 'John Doe',
            'profile-bio': 'Test bio',
            'profile-website': 'http://www.test.com',
            'profile-twitter': 'Test twitter',
            'profile-linkedin': 'Test linkedin',
            'profile-facebook': 'Test facebook',

            'education-TOTAL_FORMS': 0,
            'education-INITIAL_FORMS': 0,
            'admissions-TOTAL_FORMS': 0,
            'admissions-INITIAL_FORMS': 0,
            'workexperience-TOTAL_FORMS': 0,
            'workexperience-INITIAL_FORMS': 0,
            'organization-TOTAL_FORMS': 0,
            'organization-INITIAL_FORMS': 0,
            'award-TOTAL_FORMS': 0,
            'award-INITIAL_FORMS': 0,
            'jurisdiction-country': 'Invalid Jurisdiciton',
            'jurisdiction-TOTAL_FORMS': 0,
            'jurisdiction-INITIAL_FORMS': 0,
            'language-TOTAL_FORMS': 0,
            'language-INITIAL_FORMS': 0
        }
        cls.user = ProfileFactory(**cls.signup_credentials)
        cls.user.set_password(cls.signup_credentials['password'])
        cls.user.save()

    def test_python_version_correct(self):
        self.assertEqual(sys.version_info.major, 3)
        self.assertEqual(sys.version_info.minor, 7)

    def test_fixtures_faker_correct(self):
        call_command('loaddata', 'admin', verbosity=0)
        call_command('loaddata', 'handcrafted', verbosity=0)
        call_command('generateprofiles', 100, verbosity=0)

    def test_generate_profiles_working(self):
        GENERATED_MODELS_COUNT = 25

        existing_profiles_count = Profile.objects.count()

        ProfileFactory.create_batch(GENERATED_MODELS_COUNT)

        new_profiles_count = Profile.objects.count()

        self.assertEqual(new_profiles_count, existing_profiles_count + GENERATED_MODELS_COUNT)

    def test_login(self):
        users = Profile.objects.all()

        # User go to homepage
        response = self.client.get('/')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get('/profile')
        # Expects 302 and redirected to login page
        self.assertRedirects(response, '/login?next=/profile')

        # User types incorrectly
        response = self.client.post('/login?next=/profile', self.incorrect_credentials)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

        # User types correctly
        response = self.client.post('/login?next=/profile', self.credentials, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, '/profile')
        self.assertTrue(response.context['user'].is_active)

    def test_logout(self):
        # User is already logged in
        self.client.force_login(self.user)

        # User goes to profile
        response = self.client.get('/profile')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to logout
        response = self.client.get('/logout', follow=True)
        # Expects 302 and redirected to homepage
        self.assertRedirects(response, '/')

        # User is logged out
        self.assertFalse(response.context['user'].is_active)

    def test_register(self):
        # User go to homepage
        response = self.client.get('/')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User goes to profile
        response = self.client.get('/register')
        # Expects 302 and redirected to login page
        self.assertEqual(response.status_code, 200)

        # User types incorrectly
        response = self.client.post('/register', self.incorrect_new_user_data)
        # expects 200 and not authenticated
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

        # User types correctly
        response = self.client.post('/register', self.new_user_data, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, '/profile')
        self.assertTrue(response.context['user'].is_active)

    def test_update_profile(self):
        # User go to homepage
        response = self.client.get('/')
        # Expects 200 and rendered page
        self.assertEqual(response.status_code, 200)

        # User types correctly
        response = self.client.post('/login?next=/profile', self.credentials, follow=True)
        # Expects 302 and redirect to profile)
        self.assertRedirects(response, '/profile')
        self.assertTrue(response.context['user'].is_active)

        # Try to Update the data with incorrect parameters
        response = self.client.post('/profile', self.incorrect_update_data, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), 'Invalid data provided!')

        # Update the data with correct parameters
        response = self.client.post('/profile', self.correct_update_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'Your data has been updated successfully!')

        # Go to profile view page to see the updated data
        response = self.client.get('/profile/' + '-'.join(self.signup_credentials['full_name'].lower().split(' ')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].full_name, self.correct_update_data['profile-full_name'])
        self.assertEqual(response.context['user'].summary, self.correct_update_data['profile-summary'])
        self.assertEqual(response.context['user'].bio, self.correct_update_data['profile-bio'])
        self.assertEqual(response.context['user'].website, self.correct_update_data['profile-website'])
        self.assertEqual(response.context['user'].twitter, self.correct_update_data['profile-twitter'])
        self.assertEqual(response.context['user'].linkedin, self.correct_update_data['profile-linkedin'])
        self.assertEqual(response.context['user'].facebook, self.correct_update_data['profile-facebook'])
