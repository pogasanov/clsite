from faker.providers import BaseProvider
from faker import Faker
from django.db import transaction
import random

from .models import Profile, Address, Education, Admissions, LawSchool, WorkExperience, Organization, Award, Jurisdiction
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

SEED_VALUE = 54321


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
            bio="<p>" + "</p><p>".join(self.generator.paragraphs(nb=3)) + "</p>",
            experience=self.generator.pyint(min=0, max=30, step=1),
            current_job=self.generator.job(),
            size_of_clients=self.generator.pyint(min=0, max=3, step=1),
            preferred_communication_method=self.generator.pyint(min=0, max=3, step=1),
            license_status=self.generator.pyint(min=0, max=1, step=1),
            law_type_tags=[self.get_random_law_type_tag()],
            subjective_tags=[self.get_random_subjective_tag()],
            summary=self.generator.catch_phrase(),
            headline=self.generator.catch_phrase(),
            website=self.generator.uri(),
            twitter=self.generator.word(),
            linkedin=self.generator.word(),
            facebook=self.generator.word()
        )

    def get_random_law_type_tag(self):
        return random.choice(LAW_TYPE_TAGS_CHOICES)[0]

    def get_random_subjective_tag(self):
        return random.choice(SUBJECTIVE_TAGS_CHOICES)[0]

    def get_random_country(self):
        return random.choice(COUNTRIES_CHOICES)[0]

    def get_random_state(self, country):
        states_choices = _get_states_for_country(country)
        return random.choice(states_choices)[0] if states_choices else None  # return None if country has no state

    def address(self, profile=None):
        random_country = self.get_random_country()
        return Address(
            profile=profile,
            city=self.generator.city(),
            country=random_country,
            state=self.get_random_state(random_country),
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
        random_country = self.get_random_country()
        return Admissions(
            profile=profile,
            country=random_country,
            state=self.get_random_state(random_country),
            city=self.generator.city(),
            year=self.generator.pyint(min=1990, max=2019, step=1)
        )

    def law_school(self, profile=None):
        random_country = self.get_random_country()
        return LawSchool(
            profile=profile,
            school=self.generator.company(),
            country=random_country,
            state=self.get_random_state(random_country),
            city=self.generator.city()
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

    def jurisdiction(self, profile=None):
        random_country = self.get_random_country()
        return Jurisdiction(
            profile=profile,
            country=random_country,
            state=self.get_random_state(random_country),
            city=self.generator.city()
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
        jurisdiction = self.jurisdiction()
        return profile, address, education, admission, law_school, work_experience, organization, award, jurisdiction


def generate_profiles(count=100):
    random.seed(SEED_VALUE)
    fake = Faker()
    fake.seed(SEED_VALUE)
    fake.add_provider(ProfileProvider)
    profiles = []
    addresses = []
    educations = []
    admissions = []
    law_schools = []
    work_experiences = []
    organizations = []
    awards = []
    jurisdictions = []
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
            jurisdictions.append(full_profile[8])
        ids = Profile.objects.bulk_create(profiles)
        for i in range(count):
            addresses[i].profile = ids[i]
            educations[i].profile = ids[i]
            admissions[i].profile = ids[i]
            law_schools[i].profile = ids[i]
            work_experiences[i].profile = ids[i]
            organizations[i].profile = ids[i]
            awards[i].profile = ids[i]
            jurisdictions[i].profile = ids[i]
        Address.objects.bulk_create(addresses)
        Education.objects.bulk_create(educations)
        Admissions.objects.bulk_create(admissions)
        LawSchool.objects.bulk_create(law_schools)
        WorkExperience.objects.bulk_create(work_experiences)
        Organization.objects.bulk_create(organizations)
        Award.objects.bulk_create(awards)
        Jurisdiction.objects.bulk_create(jurisdictions)
