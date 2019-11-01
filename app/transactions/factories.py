import random
from io import BytesIO

import factory.random
from PIL import Image
from django.core.files.base import ContentFile, File

from profiles.factories import ProfileFactory
from transactions.choices import CURRENCIES
from transactions.models import Transaction


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
        sent_to_not_checked = factory.Trait(
            is_confirmed=None
        )

    created_by = factory.SubFactory(ProfileFactory)
    sent_to = factory.SubFactory(ProfileFactory)
    amount = factory.Faker('pyfloat', right_digits=2, min_value=1, max_value=100000)

    @factory.lazy_attribute
    def currency(self):
        assert 'USD' in CURRENCIES
        # 90% chance that currency is USD
        return 'USD' if random.random() < 0.9 else TransactionFactory.create_currency()

    value_in_usd = factory.LazyAttribute(lambda o: o.amount if o.currency == 'USD' else None)

    is_requester_principal = factory.Faker('pybool')
    date = factory.Faker('date_between', start_date="-3y", end_date="today")

    @factory.lazy_attribute
    def proof_receipt(self):
        return TransactionFactory.create_proof_receipt()

    @factory.lazy_attribute
    def is_confirmed(self):
        probability = random.random()
        # 10% chance for the transaction to get denied from the sent_to
        if probability < 0.1:
            return False
        # 40% chance for transaction to get confirmed from the sent_to
        if 0.1 <= probability < 0.5:
            return True
        # 50% chance for transaction to stay unconfirmed from sent_to
        return None

    @factory.lazy_attribute
    def is_flagged(self):
        probability = random.random()
        # 5% chance for the transaction to be flagged
        if probability < 0.05:
            return True

        return False

    @staticmethod
    def create_proof_receipt():
        random_rgb = factory.Faker('rgb_color').generate().split(',')
        return generate_image(color=random_rgb)

    @staticmethod
    def create_currency(ignore_usd=False):
        if ignore_usd:
            CHOICE_LIST = list(CURRENCIES)
            CHOICE_LIST.remove('USD')
            return random.choice(CHOICE_LIST)
        return random.choice(CURRENCIES)
