from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from profiles.factories import ProfileFactory, LanguageFactory, EducationFactory, WorkExperienceFactory, \
    OrganizationFactory, AwardFactory


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

    def test_update_address_data(self):
        ADDRESSES_PAYLOAD = {
            'country': 'Iran',
            'state': 'Dummy state',
            'city': 'Dummy city'
        }

        response = self.client.patch(self.VIEW_URL, {
            'addresses': [ADDRESSES_PAYLOAD]
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(ADDRESSES_PAYLOAD['country'], self.user.address.country)
        self.assertEqual(ADDRESSES_PAYLOAD['state'], self.user.address.state)
        self.assertEqual(ADDRESSES_PAYLOAD['city'], self.user.address.city)

    def test_update_and_add_language_data(self):
        self.user.language_set.all().delete()
        existing_languages = LanguageFactory.create_batch(profile=self.user, size=2)
        UPDATED_LANGUAGE_PAYLOAD = [
            {
                'id': existing_languages[0].id,
                'name': 'zh',
                'proficiency_level': 'NS'
            },
            {
                'id': existing_languages[1].id,
                'name': 'is',
                'proficiency_level': 'CF'
            },
            {
                'name': 'de',
                'proficiency_level': 'PF'
            },
            {
                'name': 'fj',
                'proficiency_level': 'CF'
            }
        ]

        response = self.client.patch(self.VIEW_URL, {
            'languages': UPDATED_LANGUAGE_PAYLOAD
        })
        self.assertEqual(response.status_code, 200)
        languages = self.user.language_set.all()
        self.assertEqual(len(languages), 4)
        for language in languages:
            if language.name == 'zh':
                self.assertEqual(language.id, existing_languages[0].id)
            if language.name == 'is':
                self.assertEqual(language.id, existing_languages[1].id)

    def test_update_and_add_education_data(self):
        self.user.education_set.all().delete()
        existing_educations = EducationFactory.create_batch(profile=self.user, size=2)
        UPDATED_EDUCATION_PAYLOAD = [
            {
                'id': existing_educations[0].id,
                'school': 'Dummy school1',
                'degree': 'Dummy degree1',
                'graduation_date': '2010-10-16'
            },
            {
                'id': existing_educations[1].id,
                'school': 'Dummy school2',
                'degree': 'Dummy degree2',
                'graduation_date': '2011-10-16'
            },
            {
                'school': 'Dummy school3',
                'degree': 'Dummy degree3',
                'graduation_date': '2012-10-16'
            },
            {
                'school': 'Dummy school4',
                'degree': 'Dummy degree4',
                'graduation_date': '2014-10-16'
            }
        ]

        response = self.client.patch(self.VIEW_URL, {
            'educations': UPDATED_EDUCATION_PAYLOAD
        })
        self.assertEqual(response.status_code, 200)
        educations = self.user.education_set.all()
        self.assertEqual(len(educations), 4)
        for education in educations:
            if education.school == 'Dummy school1':
                self.assertEqual(education.id, existing_educations[0].id)
            if education.school == 'Dummy school2':
                self.assertEqual(education.id, existing_educations[1].id)

    def test_update_and_add_work_experience_data(self):
        self.user.workexperience_set.all().delete()
        existing_workexperiences = WorkExperienceFactory.create_batch(profile=self.user, size=2)
        UPDATED_WORK_EXPERIENCE_PAYLOAD = [
            {
                'id': existing_workexperiences[0].id,
                'company_name': 'Dummy company1',
                'position': 'Dummy position1',
                'duration': {
                    'lower': '2010-6-16',
                    'upper': '2010-10-16'
                }
            },
            {
                'id': existing_workexperiences[1].id,
                'company_name': 'Dummy company2',
                'position': 'Dummy position2',
                'duration': {
                    'lower': '2011-6-16',
                    'upper': '2011-10-16'
                }
            },
            {
                'company_name': 'Dummy company3',
                'position': 'Dummy position3',
                'duration': {
                    'lower': '2012-6-16',
                    'upper': '2012-10-16'
                }
            },
            {
                'company_name': 'Dummy company4',
                'position': 'Dummy position4',
                'duration': {
                    'lower': '2013-6-16',
                    'upper': '2013-10-16'
                }
            }
        ]

        response = self.client.patch(self.VIEW_URL, {
            'work_experiences': UPDATED_WORK_EXPERIENCE_PAYLOAD
        })
        self.assertEqual(response.status_code, 200)
        work_experiences = self.user.workexperience_set.all()
        self.assertEqual(len(work_experiences), 4)
        for experience in work_experiences:
            if experience.company_name == 'Dummy company1':
                self.assertEqual(experience.id, existing_workexperiences[0].id)
            if experience.company_name == 'Dummy company2':
                self.assertEqual(experience.id, existing_workexperiences[1].id)

    def test_update_and_add_organization_data(self):
        self.user.organization_set.all().delete()
        existing_organizations = OrganizationFactory.create_batch(profile=self.user, size=2)
        UPDATED_ORGANIZATION_PAYLOAD = [
            {
                'id': existing_organizations[0].id,
                'name': 'Dummy company1',
                'position': 'Dummy position1',
                'duration': {
                    'lower': '2010-6-16',
                    'upper': '2010-10-16'
                }
            },
            {
                'id': existing_organizations[1].id,
                'name': 'Dummy company2',
                'position': 'Dummy position2',
                'duration': {
                    'lower': '2011-6-16',
                    'upper': '2011-10-16'
                }
            },
            {
                'name': 'Dummy company3',
                'position': 'Dummy position3',
                'duration': {
                    'lower': '2012-6-16',
                    'upper': '2012-10-16'
                }
            },
            {
                'name': 'Dummy company4',
                'position': 'Dummy position4',
                'duration': {
                    'lower': '2013-6-16',
                    'upper': '2013-10-16'
                }
            }
        ]

        response = self.client.patch(self.VIEW_URL, {
            'organizations': UPDATED_ORGANIZATION_PAYLOAD
        })
        self.assertEqual(response.status_code, 200)
        organizations = self.user.organization_set.all()
        self.assertEqual(len(organizations), 4)
        for organization in organizations:
            if organization.name == 'Dummy company1':
                self.assertEqual(organization.id, existing_organizations[0].id)
            if organization.name == 'Dummy company2':
                self.assertEqual(organization.id, existing_organizations[1].id)

    def test_update_and_add_award_data(self):
        self.user.award_set.all().delete()
        existing_awards = AwardFactory.create_batch(profile=self.user, size=2)
        UPDATED_AWARDS_PAYLOAD = [
            {
                'id': existing_awards[0].id,
                'title': 'Dummy title1',
                'presented_by': 'Dummy name1',
                'year': '2010'
            },
            {
                'id': existing_awards[1].id,
                'title': 'Dummy title2',
                'presented_by': 'Dummy name2',
                'year': '2011'
            },
            {
                'title': 'Dummy title3',
                'presented_by': 'Dummy name3',
                'year': '2012'
            },
            {
                'title': 'Dummy title4',
                'presented_by': 'Dummy name4',
                'year': '2013'
            }
        ]

        response = self.client.patch(self.VIEW_URL, {
            'awards': UPDATED_AWARDS_PAYLOAD
        })
        self.assertEqual(response.status_code, 200)
        awards = self.user.award_set.all()
        self.assertEqual(len(awards), 4)
        for award in awards:
            if award.title == 'Dummy title1':
                self.assertEqual(award.id, existing_awards[0].id)
            if award.title == 'Dummy title2':
                self.assertEqual(award.id, existing_awards[1].id)
