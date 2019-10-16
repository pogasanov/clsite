from django.contrib.admin import AdminSite, ACTION_CHECKBOX_NAME
from django.test import TestCase, override_settings
from django.urls import reverse

from clsite import settings
from profiles.factories import ProfileFactory
from transactions.admin import TransactionAdmin, TransactionValueInUSDEmptyFilter
from transactions.factories import TransactionFactory
from transactions.models import Transaction


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

    def test_flag_transactions(self):
        TEST_BATCH_SIZE = 10

        transactions_to_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)
        transactions_to_not_change = TransactionFactory.create_batch(TEST_BATCH_SIZE)

        response = self.client.post(self.CHANGELIST_URL, {'action': 'flag_transactions',
                                                          ACTION_CHECKBOX_NAME: [t.id for t in transactions_to_change]})
        self.assertRedirects(response, self.CHANGELIST_URL)

        for t in transactions_to_change:
            t.refresh_from_db(fields=('is_flagged',))
        self.assertTrue(all([t.is_flagged for t in transactions_to_change]))

        expected_admin_approved_values = []
        for t in transactions_to_not_change:
            expected_admin_approved_values.append(t.is_flagged)
            t.refresh_from_db(fields=('is_flagged',))
        self.assertEqual(expected_admin_approved_values, [t.is_flagged for t in transactions_to_not_change])
