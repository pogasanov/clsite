from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from clsite import settings
from profiles.factories import ProfileFactory
from transactions.factories import TransactionFactory
from transactions.forms import ConfirmTransactionForm
from transactions.models import Transaction


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TransactionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created_by, cls.sent_to = ProfileFactory.create_batch(size=2)
        cls.TRANSACTION_URL = f'/transaction/{cls.sent_to.handle}'

        cls.data_payload = {
            'date': timezone.now().strftime('%m/%d/%Y'),
            'amount': 1234,
            'currency': 'USD',
            'is_requester_principal': True,
            'proof_receipt': TransactionFactory.create_proof_receipt()
        }

    def setUp(self):
        self.client.login(username=self.created_by.email, password=settings.DEFAULT_USER_PASSWORD)

    def test_redirect_to_login_for_not_logged_user(self):
        self.client.logout()

        response = self.client.get(self.TRANSACTION_URL)
        self.assertRedirects(response, f'/login?next={self.TRANSACTION_URL}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.TRANSACTION_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('create_transaction', kwargs={'handle': self.sent_to.handle}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.TRANSACTION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction.html')

    def test_created_by_sent_to_passed_to_form(self):
        response = self.client.get(self.TRANSACTION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance.created_by.id, self.created_by.id)
        self.assertEqual(response.context['form'].instance.sent_to.id, self.sent_to.id)

    def test_created_by_eq_sent_to_redirected_to_profile(self):
        response = self.client.get(reverse('create_transaction', kwargs={'handle': self.created_by.handle}))
        self.assertRedirects(response, reverse('profile'))

    def test_create_transaction_and_redirects_home_on_form_valid(self):
        response = self.client.post(self.TRANSACTION_URL, data=self.data_payload)
        self.assertRedirects(response, reverse('home'))

        transactions_count = Transaction.objects.count()
        self.assertEqual(transactions_count, 1)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConfirmTransactionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.transaction = TransactionFactory(sent_to_not_checked=True)
        cls.TRANSACTION_URL = f'/confirm-transaction/{cls.transaction.id}'

        cls.data_payload = {
            'submit': ConfirmTransactionForm.ACTION_CONFIRM
        }

    def setUp(self):
        self.client.login(username=self.transaction.sent_to.email, password=settings.DEFAULT_USER_PASSWORD)

    def test_redirect_to_login_for_not_logged_user(self):
        self.client.logout()

        response = self.client.get(self.TRANSACTION_URL)
        self.assertRedirects(response, f'/login?next={self.TRANSACTION_URL}')

    def test_redirect_if_not_sent_to_accessed(self):
        self.client.logout()
        self.client.login(username=self.transaction.created_by.email, password=settings.DEFAULT_USER_PASSWORD)

        response = self.client.get(self.TRANSACTION_URL)
        self.assertRedirects(response, reverse('profile'))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.TRANSACTION_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('confirm_transaction', kwargs={'transaction_id': self.transaction.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.TRANSACTION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_transaction.html')

    def test_transaction_confirmed(self):
        response = self.client.post(self.TRANSACTION_URL, data=self.data_payload)
        self.assertRedirects(response, reverse('home'))

        self.transaction.refresh_from_db()
        self.assertTrue(self.transaction.is_confirmed)

    def test_transaction_denied(self):
        denied_data_payload = dict(self.data_payload)
        denied_data_payload['submit'] = ConfirmTransactionForm.ACTION_DENY

        response = self.client.post(self.TRANSACTION_URL, data=denied_data_payload)
        self.assertRedirects(response, reverse('home'))

        self.transaction.refresh_from_db()
        self.assertFalse(self.transaction.is_confirmed)
