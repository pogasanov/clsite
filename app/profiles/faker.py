from faker.providers import BaseProvider
from faker import Faker
from django.db import transaction

from .models import (Profile, Address, Education, Admissions,
                    LawSchool, WorkExperience, Organization, Award, Language)


class ProfileProvider(BaseProvider):
    def profile(self):
        return Profile(
            # Abstract user fields
            # Password is 'password'
            handle=self.generator.user_name(),
            email=self.generator.email(),
            first_name=self.generator.first_name(),
            last_name=self.generator.last_name(),
            password='pbkdf2_sha256$150000$2bhhJByaRefj$YjOjogq8+zzorhEeQgTyLYFSZD+tOLgYNeOWbSYhIVg=',
            date_joined=self.generator.date_object(),

            # Contacts
            phone=self.generator.msisdn(),
            bio="<p>" + \
                "</p><p>".join(self.generator.paragraphs(nb=3)) + "</p>",
            experience=self.generator.pyint(min=0, max=30, step=1),
            current_job=self.generator.job(),
            size_of_clients=self.generator.pyint(min=0, max=3, step=1),
            preferred_communication_method=self.generator.pyint(
                min=0, max=3, step=1),
            license_status=self.generator.pyint(min=0, max=1, step=1),
            clients=[self.generator.company()],

            jurisdiction=[self.generator.state_abbr()],
            headline=self.generator.catch_phrase(),
            website=self.generator.uri(),
            twitter=self.generator.word(),
            linkedin=self.generator.word(),
            facebook=self.generator.word()
        )

    def address(self, profile=None):
        return Address(
            profile=profile,
            city=self.generator.city(),
            state=self.generator.state_abbr(),
            zipcode=self.generator.postalcode(),
            street=self.generator.street_address(),
            building=self.generator.building_number()
        )

    def education(self, profile=None):
        return Education(
            profile=profile,
            school=self.generator.company(),
            degree=' '.join(self.generator.words()),
            graduation_date=self.generator.date_object()
        )

    def admission(self, profile=None):
        return Admissions(
            profile=profile,
            state=self.generator.state_abbr(),
            year=self.generator.pyint(min=1990, max=2019, step=1)
        )

    def law_school(self, profile=None):
        return LawSchool(
            profile=profile,
            school=self.generator.company(),
            state=self.generator.state_abbr()
        )

    def work_experience(self, profile=None):
        end_duration = self.generator.date_object()
        return WorkExperience(
            profile=profile,
            company_name=self.generator.company(),
            position=self.generator.job(),
            duration=f"[{self.generator.date(pattern='%Y-%m-%d', end_datetime=end_duration)},{end_duration})",
            responsibility="\n".join(self.generator.paragraphs(nb=3))
        )

    def organization(self, profile=None):
        end_duration = self.generator.date_object()
        return Organization(
            profile=profile,
            name=self.generator.company(),
            position=self.generator.job(),
            duration=f"[{self.generator.date(pattern='%Y-%m-%d', end_datetime=end_duration)},{end_duration})",
        )

    def award(self, profile=None):
        return Award(
            profile=profile,
            title=self.generator.word(),
            presented_by=self.generator.company(),
            year=self.generator.pyint(min=1990, max=2019, step=1),
            description="\n".join(self.generator.paragraphs(nb=3))
        )
    
    def language(self, profile=None):
        return Language(
            profile=profile,
            name=self.generator.name_abbr(),
            proficiency_level=self.generator.proficiency_level_abbr()
        )

    def full_profile(self):
        profile = self.profile()
        address = self.address()
        education = self.education()
        admission = self.admission()
        law_school = self.law_school()
        work_experience = self.work_experience()
        organization = self.organization()
        award = self.award()
        language = self.language()
        return (profile, address, education, admission, law_school, 
                work_experience, organization, award, language)


def generate_profiles(count=100):
    fake = Faker()
    fake.add_provider(ProfileProvider)
    profiles = []
    addresses = []
    educations = []
    admissions = []
    law_schools = []
    work_experiences = []
    organizations = []
    awards = []
    languages = []
    with transaction.atomic():
        for _ in range(count):
            full_profile = fake.full_profile()
            profiles.append(full_profile[0])
            addresses.append(full_profile[1])
            educations.append(full_profile[2])
            admissions.append(full_profile[3])
            law_schools.append(full_profile[4])
            work_experiences.append(full_profile[5])
            organizations.append(full_profile[6])
            awards.append(full_profile[7])
            languages.append(full_profile[8])
        ids = Profile.objects.bulk_create(profiles)
        for i in range(count):
            addresses[i].profile = ids[i]
            educations[i].profile = ids[i]
            admissions[i].profile = ids[i]
            law_schools[i].profile = ids[i]
            work_experiences[i].profile = ids[i]
            organizations[i].profile = ids[i]
            awards[i].profile = ids[i]
            languages[i].profile = ids[i]

        Address.objects.bulk_create(addresses)
        Education.objects.bulk_create(educations)
        Admissions.objects.bulk_create(admissions)
        LawSchool.objects.bulk_create(law_schools)
        WorkExperience.objects.bulk_create(work_experiences)
        Organization.objects.bulk_create(organizations)
        Award.objects.bulk_create(awards)
        Language.objects.bulk_create(languages)
