from django.contrib.admin import AdminSite, ACTION_CHECKBOX_NAME
from django.test import TestCase, override_settings
from django.urls import reverse

from clsite import settings
from profiles.factories import ProfileFactory
from transactions.admin import TransactionAdmin, TransactionApprovedFilter, TransactionValueInUSDEmptyFilter
from transactions.factories import TransactionFactory
from transactions.models import Transaction


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionApprovedFilterTest(TestCase):
    def test_queryset(self):
        TEST_BATCH_SIZE = 5

        approved_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, is_admin_approved=True)
        not_approved_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, is_admin_approved=False)
        pending_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, is_admin_approved=None,
                                                               proof_receipt=TransactionFactory.create_proof_receipt())
        not_ready_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, is_admin_approved=None,
                                                                 proof_receipt=None)

        # assertQuerysetEqual compare model instances by their repr
        approved_transactions = list(map(repr, approved_transactions))
        not_approved_transactions = list(map(repr, not_approved_transactions))
        pending_transactions = list(map(repr, pending_transactions))

        filter = TransactionApprovedFilter(None, {'is_admin_approved': 'yes'}, Transaction, TransactionAdmin)
        filter_result = filter.queryset(None, Transaction.objects.all())
        self.assertQuerysetEqual(filter_result, approved_transactions, ordered=False)

        filter = TransactionApprovedFilter(None, {'is_admin_approved': 'no'}, Transaction, TransactionAdmin)
        filter_result = filter.queryset(None, Transaction.objects.all())
        self.assertQuerysetEqual(filter_result, not_approved_transactions, ordered=False)

        filter = TransactionApprovedFilter(None, {'is_admin_approved': 'null'}, Transaction, TransactionAdmin)
        filter_result = filter.queryset(None, Transaction.objects.all())
        self.assertQuerysetEqual(filter_result, pending_transactions, ordered=False)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionValueInUSDEmptyFilterTest(TestCase):
    def test_queryset(self):
        TEST_BATCH_SIZE = 5

        non_usd_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE,
                                                               currency=TransactionFactory.create_currency(
                                                                   ignore_usd=True
                                                               ))
        usd_transactions = TransactionFactory.create_batch(TEST_BATCH_SIZE, currency='USD')

        # assertQuerysetEqual compare model instances by their repr
        non_usd_transactions = list(map(repr, non_usd_transactions))

        filter = TransactionValueInUSDEmptyFilter(None, {'value_in_usd': 'empty'}, Transaction, TransactionAdmin)
        filter_result = filter.queryset(None, Transaction.objects.all())
        print(filter_result)
        self.assertQuerysetEqual(filter_result, non_usd_transactions, ordered=False)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileFactory(is_staff=True, is_superuser=True)
        cls.admin = TransactionAdmin(Transaction, AdminSite())
        cls.CHANGELIST_URL = reverse('admin:transactions_transaction_changelist')

    def setUp(self):
        self.client.login(username=self.user.email, password=settings.DEFAULT_USER_PASSWORD)

    def test_admin_uses_correct_template(self):
        response = self.client.get(self.CHANGELIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_admin.html')

    def test_is_ready(self):
        transaction = TransactionFactory()
        self.assertEqual(self.admin.is_ready(transaction), transaction.is_ready)

    def test_is_verified(self):
        transaction = TransactionFactory()
        self.assertEqual(self.admin.is_verified(transaction), transaction.is_verified)

    def test_admin_approved(self):
        transaction = TransactionFactory(proof_receipt=None)
        self.assertEqual(self.admin.admin_approved(transaction), 'N/A')

        transaction = TransactionFactory(is_admin_approved=None,
                                         proof_receipt=TransactionFactory.create_proof_receipt())
        self.assertEqual(self.admin.admin_approved(transaction), 'Pending')

        transaction = TransactionFactory(is_admin_approved=True,
                                         proof_receipt=TransactionFactory.create_proof_receipt())
        self.assertEqual(self.admin.admin_approved(transaction), 'Approved')

        transaction = TransactionFactory(is_admin_approved=False,
                                         proof_receipt=TransactionFactory.create_proof_receipt())
        self.assertEqual(self.admin.admin_approved(transaction), 'Denied')

    def test_amount_direction(self):
        transaction = TransactionFactory(is_requester_principal=True)
        self.assertIn('custom-arrow-right', self.admin.amount_direction(transaction))

        transaction = TransactionFactory(is_requester_principal=False)
        self.assertIn('custom-arrow-left', self.admin.amount_direction(transaction))

    def test_currency_conversion(self):
        transaction = TransactionFactory(currency='USD')
        self.assertIsNone(self.admin.currency_conversion(transaction))

        transaction = TransactionFactory(currency=TransactionFactory.create_currency(ignore_usd=True))
        self.assertIn(transaction.currency, self.admin.currency_conversion(transaction))

    def test_approve_transactions(self):
        TEST_BATCH_SIZE = 10

        transactions_to_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)
        transactions_to_not_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)

        response = self.client.post(self.CHANGELIST_URL, {'action': 'approve_transactions',
                                                          ACTION_CHECKBOX_NAME: [t.id for t in transactions_to_change]})
        self.assertRedirects(response, self.CHANGELIST_URL)

        for t in transactions_to_change:
            t.refresh_from_db(fields=('is_admin_approved',))
        self.assertTrue(all([t.is_admin_approved for t in transactions_to_change if bool(t.proof_receipt)]))

        expected_admin_approved_values = []
        for t in transactions_to_not_change:
            expected_admin_approved_values.append(t.is_admin_approved)
            t.refresh_from_db(fields=('is_admin_approved',))
        self.assertEqual(expected_admin_approved_values, [t.is_admin_approved for t in transactions_to_not_change])

    def test_deny_transactions(self):
        TEST_BATCH_SIZE = 10

        transactions_to_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)
        transactions_to_not_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)

        response = self.client.post(self.CHANGELIST_URL, {'action': 'deny_transactions',
                                                          ACTION_CHECKBOX_NAME: [t.id for t in transactions_to_change]})
        self.assertRedirects(response, self.CHANGELIST_URL)

        for t in transactions_to_change:
            t.refresh_from_db(fields=('is_admin_approved',))
        self.assertTrue(all([not t.is_admin_approved for t in transactions_to_change if bool(t.proof_receipt)]))

        expected_admin_approved_values = []
        for t in transactions_to_not_change:
            expected_admin_approved_values.append(t.is_admin_approved)
            t.refresh_from_db(fields=('is_admin_approved',))
        self.assertEqual(expected_admin_approved_values, [t.is_admin_approved for t in transactions_to_not_change])
