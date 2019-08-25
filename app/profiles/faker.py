import pytz
import random
import numpy as np
from io import BytesIO
from PIL import Image

from faker.providers import BaseProvider
from faker import Faker
from django.db import transaction
from django.core.files.base import ContentFile

from .models import Profile, Address, Education, Admissions, LawSchool, \
    WorkExperience, Organization, Award, Jurisdiction, Transaction
from .utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country
from .choices import CURRENCIES

SEED_VALUE = 54321
CURRENCY_CODES = [currency_code for currency_code, _ in CURRENCIES]
TRANSACTION_REVIEW_CHOICES = [review_choice for review_choice, _ in Transaction.REVIEW_CHOICES]


def random_number_exponential_delay(pr=0.25, probability_of_none=0.0):
    if random.random() < probability_of_none:
        return 0

    i = 1
    while random.random() < pr:
        i += 1

    return i

def generate_image(color=(256, 0, 0)):
    """
    Creates a random image and converts it into a model save-able file
    :param color: color (optional) to randomize the image created
    :return: returns an object of ContentFile which can be directly stored to the Model's ImageField
    """
    image = Image.new('RGBA', size=(200, 200), color=color)
    file = BytesIO(image.tobytes())
    file.name = 'test.png'
    file.seek(0)
    return ContentFile(file.read(), name='test.png')


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
            subjective_tags=[self.get_random_subjective_tag() for
                             x in range(random_number_exponential_delay(pr=0.25, probability_of_none=0.0))],
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


class TransactionProvider(BaseProvider):

    def generate_transaction(self, requester_id, requestee_id):
        profile_transaction = Transaction(
            requester_id=requester_id,
            requestee_id=requestee_id,
            amount=self.generator.pyfloat(right_digits=2, min_value=1, max_value=100000),
            currency=self.get_currency(),
            requester_review=self.get_review(),
            is_requester_principal=self.generator.pybool(),
            date=self.generator.date_between(start_date="-3y", end_date="today"),
            requester_recommendation=self.get_recommendation(),
            proof_receipt_requester=self.get_proof_receipt_requester()
            )

        self.confirm_from_requestee(profile_transaction)
        self.approve_from_admin(profile_transaction)

        return profile_transaction

    def get_currency(self):
        # 90% chance that currency is USD
        assert 'USD' in CURRENCY_CODES
        return 'USD' if random.random() < 0.9 else random.choice(CURRENCY_CODES)

    def get_review(self):
        return random.choice(TRANSACTION_REVIEW_CHOICES)

    def get_recommendation(self):
        if random.random() < 0.7:
            return ''

        return ' '.join(self.generator.paragraphs(nb=3))

    def get_proof_receipt_requester(self):
        if random.random() < 0.34:
            return generate_image(self.generator.hex_color())

    def confirm_from_requestee(self, profile_transaction):
        probability = random.random()

        if probability > 0.5:
            return

        if probability > 0.4:
            profile_transaction.is_confirmed = False
            return

        profile_transaction.is_confirmed = True
        profile_transaction.requestee_review = self.get_review()
        profile_transaction.requestee_recommendation = self.get_recommendation()

    def approve_from_admin(self, profile_transaction):
        probability = random.random()

        if not profile_transaction.proof_receipt_requester:
            return

        if probability > 0.5:
            return

        if probability > 0.4:
            profile_transaction.is_verified = False
            return

        profile_transaction.is_verified = True


def generate_profiles(count=1000):
    random.seed(SEED_VALUE)
    np.random.seed(SEED_VALUE)

    fake = Faker()
    fake.seed(SEED_VALUE)
    fake.add_provider(ProfileProvider)
    fake.add_provider(TransactionProvider)

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
        profiles = Profile.objects.bulk_create([full_profile["profile"] for full_profile in full_profiles])

        assert(len(profiles) == len(full_profiles))

        for full_profile, profile in zip(full_profiles, profiles):
            for key in full_profile.keys():
                full_profile[key].profile = profile

        # field_to_objects should have every field as full_profiles, except for "profile"
        assert(["profile"] + list(field_to_objects.keys()) == list(full_profiles[0].keys()))

        for field_name, field_objects in field_to_objects.items():
            field_objects.bulk_create([full_profile[field_name] for full_profile in full_profiles])

        transactions = generate_transactions(profiles, fake)
        Transaction.objects.bulk_create(transactions)

        print("Dummy data ingested to database successfully!")


def generate_transactions(profiles, faker):
    # Transaction related data ingestion
    transactions = []
    profile_ids = [p.id for p in profiles]
    number_of_requesters_with_transactions = round(len(profile_ids) * 0.1)

    requester_ids = random.sample(profile_ids, number_of_requesters_with_transactions)

    for requester_id in requester_ids:
        number_of_transactions = random_number_exponential_delay(pr=0.5)
        # Generating random requestee_ids. The replace=True flag ensures duplicates
        requestee_ids = list(np.random.choice(profile_ids, number_of_transactions, replace=True))

        for requestee_id in requestee_ids:
            if requester_id == requestee_id:
                continue

            transactions.append(faker.generate_transaction(requester_id=requester_id, requestee_id=requestee_id))

    return transactions
