from django.test import TestCase, override_settings
from django.utils import timezone

from profiles.factories import ProfileFactory
from transactions.factories import TransactionFactory
from transactions.forms import TransactionForm, ConfirmTransactionForm


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created_by = ProfileFactory()
        cls.sent_to = ProfileFactory()

        cls.data_payload = {
            'date': timezone.now(),
            'amount': 1234,
            'currency': 'USD',
            'is_requester_principal': True
        }

    def test_require_created_by_and_sent_to(self):
        with self.assertRaises(KeyError):
            TransactionForm()

        with self.assertRaises(KeyError):
            TransactionForm(created_by=self.created_by)

        with self.assertRaises(KeyError):
            TransactionForm(sent_to=self.sent_to)

    def test_valid_with_correct_payload(self):
        files = {
            'proof_receipt': TransactionFactory.create_proof_receipt()
        }

        form = TransactionForm(created_by=self.created_by, sent_to=self.sent_to, data=self.data_payload, files=files)
        self.assertTrue(form.is_valid())

    def test_pass_created_by_sent_to_to_instance(self):
        files = {
            'proof_receipt': TransactionFactory.create_proof_receipt()
        }

        form = TransactionForm(created_by=self.created_by, sent_to=self.sent_to, data=self.data_payload, files=files)
        transaction = form.save()

        self.assertIs(transaction.created_by, self.created_by)
        self.assertIs(transaction.sent_to, self.sent_to)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConfirmTransactionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_payload = {
            'submit': ConfirmTransactionForm.ACTION_CONFIRM
        }

    def setUp(self):
        self.transaction = TransactionFactory(sent_to_not_checked=True)

    def test_valid_with_correct_payload(self):
        form = ConfirmTransactionForm(data=self.data_payload, instance=self.transaction)
        self.assertTrue(form.is_valid())

    def test_is_confirmed_true_on_confirm(self):
        form = ConfirmTransactionForm(data=self.data_payload, instance=self.transaction)

        transaction = form.save()

        self.assertTrue(transaction.is_confirmed)

    def test_is_confirmed_false_on_deny(self):
        denied_data_payload = dict(self.data_payload)
        denied_data_payload['submit'] = ConfirmTransactionForm.ACTION_DENY
        form = ConfirmTransactionForm(data=denied_data_payload, instance=self.transaction)

        transaction = form.save()

        self.assertFalse(transaction.is_confirmed)
