from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from profiles.factories import ProfileFactory
from transactions.models import Transaction


class GenerateTransactionsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.TRANSACTIONS_TO_CREATE = 20

    def test_generatetransactions(self):
        PROFILES_TO_CREATE = 10

        ProfileFactory.create_batch(size=PROFILES_TO_CREATE)
        call_command('generatetransactions', transactions_count=self.TRANSACTIONS_TO_CREATE)
        transaction_count = Transaction.objects.count()

        self.assertEqual(transaction_count, self.TRANSACTIONS_TO_CREATE)

    def test_generatetransactions_without_profiles_fail(self):
        with self.assertRaises(CommandError):
            call_command('generatetransactions')

    def test_generatetransactions_with_profiles_flag(self):
        call_command('generatetransactions', generate_profiles=True, transactions_count=self.TRANSACTIONS_TO_CREATE)
