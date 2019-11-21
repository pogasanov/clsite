from django.test import TestCase, override_settings
from django.utils import timezone

from profiles.factories import ProfileFactory
from transactions.factories import TransactionFactory
from transactions.forms import TransactionForm, ConfirmTransactionForm


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.requester = ProfileFactory()
        cls.requestee = ProfileFactory()

        cls.data_payload = {
            'date': timezone.now(),
            'amount': 1234,
            'currency': 'USD',
            'is_requester_principal': True
        }

    def test_require_requester_and_requestee(self):
        with self.assertRaises(KeyError):
            TransactionForm()

        with self.assertRaises(KeyError):
            TransactionForm(requester=self.requester)

        with self.assertRaises(KeyError):
            TransactionForm(requestee=self.requestee)

    def test_valid_with_correct_payload(self):
        files = {
            'proof_receipt': TransactionFactory.create_proof_receipt()
        }

        form = TransactionForm(requester=self.requester, requestee=self.requestee, data=self.data_payload, files=files)
        self.assertTrue(form.is_valid())

    def test_pass_requester_requestee_to_instance(self):
        files = {
            'proof_receipt': TransactionFactory.create_proof_receipt()
        }

        form = TransactionForm(requester=self.requester, requestee=self.requestee, data=self.data_payload, files=files)
        transaction = form.save()

        self.assertIs(transaction.requester, self.requester)
        self.assertIs(transaction.requestee, self.requestee)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConfirmTransactionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_payload = {
            'submit': ConfirmTransactionForm.ACTION_CONFIRM
        }

    def setUp(self):
        self.transaction = TransactionFactory(requestee_not_checked=True)

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
