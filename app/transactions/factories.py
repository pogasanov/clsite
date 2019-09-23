import random
from io import BytesIO

import factory.random
from PIL import Image
from django.core.files.base import ContentFile, File

from profiles.factories import ProfileFactory
from transactions.choices import CURRENCIES
from transactions.models import Transaction

CURRENCY_CODES = [currency_code for currency_code, _ in CURRENCIES]
TRANSACTION_REVIEW_CHOICES = [review_choice for review_choice, _ in Transaction.REVIEW_CHOICES]


def generate_image(color=(255, 0, 0)):
    # Pillow requires color to be tuple of ints
    thumb = Image.new('RGB', (200, 200), color=tuple(map(int, color)))
    thumb_io = BytesIO()
    thumb.save(thumb_io, format='JPEG')
    content = ContentFile(thumb_io.getvalue())
    return File(content.file, 'test.jpg')


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'transactions.Transaction'

    class Params:
        requestee_not_checked = factory.Trait(
            is_confirmed=None,
            requestee_review=Transaction.REVIEW_NEUTRAL,
            requestee_recommendation=''
        )

    requester = factory.SubFactory(ProfileFactory)
    requestee = factory.SubFactory(ProfileFactory)
    amount = factory.Faker('pyfloat', right_digits=2, min_value=1, max_value=100000)

    @factory.lazy_attribute
    def currency(self):
        assert 'USD' in CURRENCY_CODES
        # 90% chance that currency is USD
        return 'USD' if random.random() < 0.9 else TransactionFactory.create_currency()

    value_in_usd = factory.LazyAttribute(lambda o: o.amount if o.currency == 'USD' else None)

    requester_review = factory.Faker('random_element', elements=TRANSACTION_REVIEW_CHOICES)
    is_requester_principal = factory.Faker('pybool')
    date = factory.Faker('date_between', start_date="-3y", end_date="today")
    requester_recommendation = factory.LazyAttribute(lambda o: TransactionFactory.create_recommendation())

    @factory.lazy_attribute
    def proof_receipt(self):
        if random.random() < 0.33:
            return TransactionFactory.create_proof_receipt()

    is_proof_by_requester = factory.Maybe(
        'proof_receipt',
        yes_declaration=factory.Faker('pybool'),
        no_declaration=None
    )

    @factory.lazy_attribute
    def is_admin_approved(self):
        if not self.proof_receipt:
            return None

        probability = random.random()
        # 10% chance for transaction to get denied
        if probability < 0.1:
            return False
        # 40% chance for transaction to get approved from admin
        if 0.1 <= probability < 0.5:
            return True
        # 50% chance for transaction to stay unapproved
        return None

    @factory.lazy_attribute
    def is_confirmed(self):
        probability = random.random()
        # 10% chance for the transaction to get denied from the requestee
        if probability < 0.1:
            return False
        # 40% chance for transaction to get confirmed from the requestee
        if 0.1 <= probability < 0.5:
            return True
        # 50% chance for transaction to stay unconfirmed from requestee
        return None

    requestee_review = factory.Maybe(
        'is_confirmed',
        yes_declaration=factory.Faker('random_element', elements=TRANSACTION_REVIEW_CHOICES),
        no_declaration=''
    )
    requestee_recommendation = factory.Maybe(
        'is_confirmed',
        yes_declaration=factory.LazyFunction(lambda: TransactionFactory.create_recommendation()),
        no_declaration=''
    )

    @staticmethod
    def create_proof_receipt():
        random_rgb = factory.Faker('rgb_color').generate().split(',')
        return generate_image(color=random_rgb)

    @staticmethod
    def create_recommendation():
        if random.random() < 0.25:
            return ''
        return ' '.join(factory.Faker('paragraphs', nb=3).generate())

    @staticmethod
    def create_currency(ignore_usd=False):
        if ignore_usd:
            CHOICE_LIST = list(CURRENCY_CODES)
            CHOICE_LIST.remove('USD')
            return random.choice(CHOICE_LIST)
        return random.choice(CURRENCY_CODES)
