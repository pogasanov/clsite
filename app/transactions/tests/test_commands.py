from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from profiles.factories import ProfileFactory
from transactions.models import Transaction


class TransactionCommandsTestCase(TestCase):
    def test_generatetransactions(self):
        TRANSACTIONS_TO_CREATE = 100

        ProfileFactory.create_batch(size=10)
        call_command('generatetransactions', transactions_count=TRANSACTIONS_TO_CREATE)
        transaction_count = Transaction.objects.count()

        self.assertEqual(transaction_count, TRANSACTIONS_TO_CREATE)

    def test_generatetransactions_without_profiles_fail(self):
        with self.assertRaises(CommandError):
            call_command('generatetransactions')

    def test_generatetransactions_with_profiles_flag(self):
        call_command('generatetransactions', generate_profiles=True)
