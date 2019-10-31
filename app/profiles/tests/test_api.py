from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from profiles.factories import ProfileFactory


class ProfileViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VIEW_URL = '/api/profile'

    def setUp(self):
        self.user = ProfileFactory()
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

    def test_contains_profile_data(self):
        response = self.client.get(self.VIEW_URL)

        self.assertContains(response, self.user.summary)
        self.assertContains(response, self.user.bio)
        self.assertContains(response, self.user.experience)
        self.assertContains(response, self.user.current_job)
        for tag in self.user.law_type_tags:
            self.assertContains(response, tag)
        for tag in self.user.subjective_tags:
            self.assertContains(response, tag)

    def test_contains_address_data(self):
        response = self.client.get(self.VIEW_URL)

        self.assertContains(response, self.user.address.country)
        self.assertContains(response, self.user.address.state)
        self.assertContains(response, self.user.address.city)

    def test_contains_language_data(self):
        response = self.client.get(self.VIEW_URL)

        for language in self.user.language_set.all():
            self.assertContains(response, language.name)
            self.assertContains(response, language.proficiency_level)

    def test_contains_education_data(self):
        response = self.client.get(self.VIEW_URL)

        for education in self.user.education_set.all():
            self.assertContains(response, education.school)
            self.assertContains(response, education.degree)
            self.assertContains(response, education.graduation_data)

    def test_contains_work_experience_data(self):
        response = self.client.get(self.VIEW_URL)

        for work_experience in self.user.workexperience_set.all():
            self.assertContains(response, work_experience.company_name)
            self.assertContains(response, work_experience.position)
            self.assertContains(response, work_experience.duration.lower)
            self.assertContains(response, work_experience.duration.upper)

    def test_contains_organization_data(self):
        response = self.client.get(self.VIEW_URL)

        for organization in self.user.organization_set.all():
            self.assertContains(response, organization.name)
            self.assertContains(response, organization.position)
            self.assertContains(response, organization.duration.lower)
            self.assertContains(response, organization.duration.upper)

    def test_contains_award_data(self):
        response = self.client.get(self.VIEW_URL)

        for award in self.user.award_set.all():
            self.assertContains(response, award.title)
            self.assertContains(response, award.presented_by)
            self.assertContains(response, award.year)

    def test_update_profile_data(self):
        NEW_SUMMARY = 'Dummy summary'
        NEW_BIO = 'Dummy summary'
        NEW_SUBJECTIVE_TAGS = ['Testing', 'Subjective', 'Tags']
        NEW_LAW_TYPE_TAGS = ['Testing', 'Law', 'Type', 'Tags']
        NEW_EXPERIENCE = '10'
        NEW_CURRENT_JOB = 'Dummy current job'

        response = self.client.patch(self.VIEW_URL, {
            'summary': NEW_SUMMARY,
            'bio': NEW_BIO,
            'subjective_tags': NEW_SUBJECTIVE_TAGS,
            'law_type_tags': NEW_LAW_TYPE_TAGS,
            'experience': NEW_EXPERIENCE,
            'current_job': NEW_CURRENT_JOB
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(NEW_SUMMARY, self.user.summary)
        self.assertEqual(NEW_BIO, self.user.bio)
        self.assertEqual(NEW_EXPERIENCE, self.user.experience)
        self.assertEqual(NEW_CURRENT_JOB, self.user.current_job)
        self.assertSequenceEqual(NEW_LAW_TYPE_TAGS, self.user.law_type_tags)
        self.assertSequenceEqual(NEW_SUBJECTIVE_TAGS, self.user.subjective_tags)

    def test_partial_update(self):
        NEW_SUMMARY = 'New summary'
        OLD_BIO = self.user.bio

        response = self.client.patch(self.VIEW_URL, {
            'summary': NEW_SUMMARY
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(NEW_SUMMARY, self.user.summary)
        self.assertEqual(OLD_BIO, self.user.bio)
