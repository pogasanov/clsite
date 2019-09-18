from django.core.exceptions import ValidationError
from django.test import TestCase

from profiles.factories import ProfileFactory
from transactions.factories import TransactionFactory
from transactions.models import Transaction


class TransactionModelsTestCase(TestCase):
    def test_queryset_unconfirmed(self):
        TEST_BATCH_SIZE = 5

        transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, is_confirmed=None)
        TransactionFactory.create_batch(TEST_BATCH_SIZE, is_confirmed=False)
        TransactionFactory.create_batch(TEST_BATCH_SIZE, is_confirmed=True)

        # assertQuerysetEqual compare model instances by their repr
        unconfirmed_transactions = list(map(repr, transactions))

        # Via manager
        fetched_transactions = Transaction.unconfirmed.all()
        self.assertQuerysetEqual(fetched_transactions, unconfirmed_transactions, ordered=False)

        # Via queryset
        fetched_transactions = Transaction.objects.unconfirmed()
        self.assertQuerysetEqual(fetched_transactions, unconfirmed_transactions, ordered=False)

    def test_usd_value_equal_amount(self):
        TEST_AMOUNT = 473283

        transaction = TransactionFactory(currency='USD', amount=TEST_AMOUNT)

        self.assertEqual(transaction.value_in_usd, TEST_AMOUNT)

    def test_randomize_proof_receipt_filename(self):
        proof_receipt = TransactionFactory.create_proof_receipt()
        transaction = TransactionFactory(proof_receipt=proof_receipt)

        self.assertNotEqual(transaction.proof_receipt.name, proof_receipt.name)

    def test_is_ready(self):
        # Unconfirmed transactions shouldn't be ready
        transaction = TransactionFactory(is_confirmed=False)
        self.assertFalse(transaction.is_ready)

        # No value transactions shouldn't be ready
        transaction = TransactionFactory(is_confirmed=True, amount=0)
        self.assertFalse(transaction.is_ready)

        transaction = TransactionFactory(is_confirmed=True, amount=123)
        self.assertTrue(transaction.is_ready)

        # If transaction has proof_receipt, it should be confirmed by admin
        transaction = TransactionFactory(is_confirmed=True,
                                         amount=123,
                                         proof_receipt=TransactionFactory.create_proof_receipt(),
                                         is_admin_approved=False
                                         )
        self.assertFalse(transaction.is_ready)

        transaction = TransactionFactory(is_confirmed=True,
                                         amount=123,
                                         proof_receipt=TransactionFactory.create_proof_receipt(),
                                         is_admin_approved=True
                                         )
        self.assertTrue(transaction.is_ready)

    def test_is_verified(self):
        # Transaction without proof receipt shouldn't be verified
        transaction = TransactionFactory(proof_receipt=None)
        self.assertFalse(transaction.is_verified)

        transaction = TransactionFactory(proof_receipt=TransactionFactory.create_proof_receipt())
        self.assertTrue(transaction.is_verified)

    def test_requestee_eq_reqeuester_fail(self):
        profile = ProfileFactory()
        transaction = TransactionFactory(requestee=profile, requester=profile)
        with self.assertRaises(ValidationError):
            transaction.full_clean()
