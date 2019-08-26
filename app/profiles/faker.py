from faker.providers import BaseProvider
from faker import Faker
import numpy as np
from django.db import transaction
import random
import pytz

from .models import Profile, Address, Education, Admissions, LawSchool, WorkExperience, Organization, Award, Jurisdiction
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

SEED_VALUE = 54321

def random_number_exponential_delay(pr=0.25, probability_of_none=0.0):
    if random.random() < probability_of_none:
        return 0
    i = 1
    while random.random() < pr:
        i += 1
    return i


class ProfileProvider(BaseProvider):
    def profile(self, id=1):
        full_name = self.generator.first_name() + " " + self.generator.last_name()
        return Profile(
            # Abstract user fields
            # Password is 'password'
            handle='-'.join(full_name.lower().split(' ')) + str(id),
            email=self.generator.email(),
            full_name=full_name,
            password='pbkdf2_sha256$150000$2bhhJByaRefj$YjOjogq8+zzorhEeQgTyLYFSZD+tOLgYNeOWbSYhIVg=',
            date_joined=self.generator.date_time(tzinfo=pytz.UTC),

            # Contacts
            phone=self.generator.msisdn(),
            bio="<p>" + "</p><p>".join(self.generator.paragraphs(nb=3)) + "</p>",
            experience=self.generator.pyint(min_value=0, max_value=30, step=1),
            current_job=self.generator.job(),
            size_of_clients=self.generator.pyint(min_value=0, max_value=3, step=1),
            preferred_communication_method=self.generator.pyint(min_value=0, max_value=3, step=1),
            law_type_tags=[self.get_random_law_type_tag() for x in range(random_number_exponential_delay(pr=0.25))],
            subjective_tags=[self.get_random_subjective_tag() for x in range(random_number_exponential_delay(pr=0.25, probability_of_none=0.0))],
            summary=self.generator.catch_phrase(),
            website=self.generator.uri(),
            twitter=self.generator.word(),
            linkedin=self.generator.word(),
            facebook=self.generator.word()
        )

    def get_random_law_type_tag(self):
        return random.choice(LAW_TYPE_TAGS_CHOICES)[0]

    def get_random_subjective_tag(self):
        return random.choice(SUBJECTIVE_TAGS_CHOICES)[0]

    def get_random_country_state_city(self):
        random_country = random.choice(COUNTRIES_CHOICES)[0]

        states_choices = _get_states_for_country(random_country)  # get all states for the country

        random_state = random.choice(states_choices)[0] if states_choices else None  # return None if country has no state
        random_city = self.generator.city() if random_state else None

        return random_country, random_state, random_city


    def address(self, profile=None):
        country, state, city  = self.get_random_country_state_city()
        return Address(
            profile=profile,
            city=city,
            country=country,
            state=state,
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
        country, state, city  = self.get_random_country_state_city()
        return Admissions(
            profile=profile,
            country=country,
            state=state,
            city=city,
            year=self.generator.pyint(min_value=1990, max_value=2019, step=1)
        )

    def law_school(self, profile=None):
        country, state, city  = self.get_random_country_state_city()
        return LawSchool(
            profile=profile,
            school=self.generator.company(),
            country=country,
            state=state,
            city=city
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
            year=self.generator.pyint(min_value=1990, max_value=2019, step=1),
            description="\n".join(self.generator.paragraphs(nb=3))
        )

    def jurisdiction(self, profile=None):
        country, state, city  = self.get_random_country_state_city()
        return Jurisdiction(
            profile=profile,
            country=country,
            state=state,
            city=city
        )

    def full_profile(self, id=1):
        return {
            "profile": self.profile(id),
            "address": self.address(),
            "education": self.education(),
            "admission": self.admission(),
            "law_school": self.law_school(),
            "work_experience": self.work_experience(),
            "organization": self.organization(),
            "award": self.award(),
            "jurisdiction": self.jurisdiction()
        }


def generate_profiles(count=1000):
    random.seed(SEED_VALUE)
    np.random.seed(SEED_VALUE)
    fake = Faker()
    fake.seed(SEED_VALUE)
    fake.add_provider(ProfileProvider)

    law_tags_previous_count = 4
    subjective_tags_previous_count = 4

    full_profiles = []
    field_to_objects = {
            "address": Address.objects,
            "education": Education.objects,
            "admission": Admissions.objects,
            "law_school": LawSchool.objects,
            "work_experience": WorkExperience.objects,
            "organization": Organization.objects,
            "award": Award.objects,
            "jurisdiction": Jurisdiction.objects
    }
    full_profiles = [fake.full_profile(i) for i in range(count)]
    with transaction.atomic():
        ids = Profile.objects.bulk_create([full_profile["profile"] for full_profile in full_profiles])
        assert(len(ids) == len(full_profiles))
        for full_profile, id in zip(full_profiles, ids):
            for object in full_profile.keys():
                full_profile[object].profile = id
        # field_to_objects should have every field as full_profiles, except for "profile"
        assert(["profile"] + list(field_to_objects.keys()) == list(full_profiles[0].keys()))
        for field_name, field_objects in field_to_objects.items():
            field_objects.bulk_create([full_profile[field_name] for full_profile in full_profiles])

        print("Dummy data ingested to database successfully!")
