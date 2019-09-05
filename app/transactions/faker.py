import random
from io import BytesIO

import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from faker.providers import BaseProvider

from clsite.utils import random_number_exponential_delay
from .choices import CURRENCIES
from .models import Transaction

CURRENCY_CODES = [currency_code for currency_code, _ in CURRENCIES]
TRANSACTION_REVIEW_CHOICES = [review_choice for review_choice, _ in Transaction.REVIEW_CHOICES]


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


class TransactionProvider(BaseProvider):

    def generate_transaction(self, requester_id, requestee_id):
        amount = self.generator.pyfloat(right_digits=2, min_value=1, max_value=100000)
        currency = self.get_currency()

        profile_transaction = Transaction(
            requester_id=requester_id,
            requestee_id=requestee_id,
            amount=amount,
            currency=currency,
            requester_review=self.get_review(),
            is_requester_principal=self.generator.pybool(),
            date=self.generator.date_between(start_date="-3y", end_date="today"),
            requester_recommendation=self.get_recommendation(),
            proof_receipt_requester=self.get_proof_receipt_requester(),
            value_in_usd=amount if currency == 'USD' else None
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
        if random.random() < 0.25:
            return

        return ' '.join(self.generator.paragraphs(nb=3))

    def get_proof_receipt_requester(self):
        if random.random() < 0.33:
            return generate_image(self.generator.hex_color())

    def confirm_from_requestee(self, profile_transaction):
        probability = random.random()

        # 50% chance for transaction to stay unconfirmed from requestee
        if probability > 0.5:
            return
        # 10% chance for the transaction to get denied from the requestee
        elif 0.4 < probability <= 0.5:
            profile_transaction.is_confirmed = False
            return
        # 40% chance for transaction to get confirmed from the requestee
        else:
            profile_transaction.is_confirmed = True
            profile_transaction.requestee_review = self.get_review()
            profile_transaction.requestee_recommendation = self.get_recommendation()

    def approve_from_admin(self, profile_transaction):
        if not profile_transaction.proof_receipt_requester:
            return

        probability = random.random()

        # 50% chance for transaction to stay unapproved
        if probability > 0.5:
            return
        # 10% chance for transaction to get denied
        elif 0.4 < probability <= 0.5:
            profile_transaction.is_verified = False
            return
        # 40% chance for transaction to get approved from admin
        else:
            profile_transaction.is_verified = True


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
