from faker.providers import BaseProvider
from faker import Faker
from django.db import transaction
import random

from .models import Profile, Address, Education, Admissions, LawSchool, WorkExperience, Organization, Award, Jurisdiction
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

SEED_VALUE = 54321

# selection occurrence percentage
PERCENTAGE_ZERO = 0.05
PERCENTAGE_ONE = 0.65
PERCENTAGE_TWO = 0.20
PERCENTAGE_THREE = 0.05
PERCENTAGE_FOUR = 0.01

ZERO_SELECTION = 0
ONE_SELECTION = 1
TWO_SELECTIONS = 2
THREE_SELECTIONS = 3
FOUR_SELECTIONS = 4


class ProfileProvider(BaseProvider):
    def profile(self, law_tags_count, subjective_tags_count):
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
            law_type_tags=[self.get_random_law_type_tag() for x in list(range(law_tags_count))],
            subjective_tags=[self.get_random_subjective_tag() for x in list(range(subjective_tags_count))],
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

    def full_profile(self, law_tags_count, subjective_tags_count):
        profile = self.profile(law_tags_count, subjective_tags_count)
        address = self.address()
        education = self.education()
        admission = self.admission()
        law_school = self.law_school()
        work_experience = self.work_experience()
        organization = self.organization()
        award = self.award()
        jurisdiction = self.jurisdiction()
        return profile, address, education, admission, law_school, work_experience, organization, award, jurisdiction


def get_selection_randomization(count):
    indices_list = range(count)

    zero_selection_indices = random.sample(indices_list, int(PERCENTAGE_ZERO * count))
    indices_list = list(set(indices_list) - set(zero_selection_indices))

    one_selection_indices = random.sample(indices_list, int(PERCENTAGE_ONE * count))
    indices_list = list(set(indices_list) - set(one_selection_indices))

    two_selections_indices = random.sample(indices_list, int(PERCENTAGE_TWO * count))
    indices_list = list(set(indices_list) - set(two_selections_indices))

    three_selections_indices = random.sample(indices_list, int(PERCENTAGE_THREE * count))
    indices_list = list(set(indices_list) - set(three_selections_indices))

    four_selection_indices = random.sample(indices_list, int(PERCENTAGE_FOUR * count))

    return {
        ZERO_SELECTION: zero_selection_indices,
        ONE_SELECTION: one_selection_indices,
        TWO_SELECTIONS: two_selections_indices,
        THREE_SELECTIONS: three_selections_indices,
        FOUR_SELECTIONS: four_selection_indices
    }


def generate_profiles(count=100):
    random.seed(SEED_VALUE)
    fake = Faker()
    fake.seed(SEED_VALUE)
    fake.add_provider(ProfileProvider)

    law_tags_randomization = get_selection_randomization(count)
    subjective_tags_randomization = get_selection_randomization(count)
    law_tags_count = 0
    subjective_tags_count = 0

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
        for index in range(count):

            for key, value in law_tags_randomization.items():
                if index in value:
                    law_tags_count = key
                    break
            for key, value in subjective_tags_randomization.items():
                if index in value:
                    subjective_tags_count = key
                    break

            full_profile = fake.full_profile(law_tags_count, subjective_tags_count)
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
