from faker.providers import BaseProvider
from faker import Faker
import numpy as np
from django.db import transaction
import random

from .models import Profile, Address, Education, Admissions, LawSchool, WorkExperience, Organization, Award, Jurisdiction
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

SEED_VALUE = 54321

# selection occurrence percentage
PERCENTAGE_ZERO = 0.09
PERCENTAGE_ONE = 0.65
PERCENTAGE_TWO = 0.20
PERCENTAGE_THREE = 0.05
PERCENTAGE_FOUR = 0.01

ZERO_SELECTION = 0
ONE_SELECTION = 1
TWO_SELECTIONS = 2
THREE_SELECTIONS = 3
FOUR_SELECTIONS = 4

STATE_PROBABILITY_MATRIX = [PERCENTAGE_ZERO, PERCENTAGE_ONE, PERCENTAGE_TWO, PERCENTAGE_THREE, PERCENTAGE_FOUR]
STATE_TRANSITION_MATRIX = [
    ['00', '01', '02', '03', '04'],
    ['10', '11', '12', '13', '14'],
    ['20', '21', '22', '23', '24'],
    ['30', '31', '32', '33', '34'],
    ['40', '41', '42', '43', '44']
]

def get_current_count_markov_chain(previous_state):
    next_transition = np.random.choice(
        STATE_TRANSITION_MATRIX[previous_state],
        replace=True,
        p=STATE_PROBABILITY_MATRIX
    )
    return int(next_transition[-1])


class ProfileProvider(BaseProvider):
    def profile(self):
        subjective_tags_current_count = get_current_count_markov_chain(subjective_tags_previous_count)
        law_tags_current_count = get_current_count_markov_chain(law_tags_previous_count)
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
            law_type_tags=[self.get_random_law_type_tag() for x in range(law_tags_count)],
            subjective_tags=[self.get_random_subjective_tag() for x in range(subjective_tags_count)],
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
            year=self.generator.pyint(min=1990, max=2019, step=1)
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
            year=self.generator.pyint(min=1990, max=2019, step=1),
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

    def full_profile(self):
        return {
            "profile": self.profile(),
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
    with transaction.atomic():
        full_profiles.append(fake.full_profile())
        ids = Profile.objects.bulk_create([full_profile["profile"] for full_profile in full_profiles])
        assert(len(ids) == len(full_profiles))
        for full_profile, id in zip(full_profiles, ids):
            full_profile.profile = id
        # field_to_objects should have every field as full_profiles, except for "profile"
        assert(set(field_to_objects.keys() + "profile") == set(full_profiles[0].keys()))
        for field_name, field_objects in field_to_objects.items():
            field_objects.bulk_create([full_profile[field_name] for full_profile in full_profiles])
