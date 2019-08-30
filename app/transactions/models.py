import uuid

from django.db import models

from clsite.storage_backends import variativeStorage
from profiles.models import get_image_path
from transactions.choices import CURRENCIES


class Transaction(models.Model):
    REVIEW_CHOICES = (
        ('SD', 'Strongly Disagree'),
        ('D', 'Disagree'),
        ('N', 'Neutral'),
        ('A', 'Agree'),
        ('SA', 'Strongly Agree')
    )
    CURRENCY_CHOICES = CURRENCIES

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name='Transaction Date')

    requester = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requester', verbose_name='Requester')
    proof_receipt = models.ImageField(upload_to=get_image_path, storage=variativeStorage(),
                                      verbose_name='Transaction Proof', blank=True, null=True)
    is_proof_by_requester = models.NullBooleanField(default=None, verbose_name="Receipt added by requester")
    requester_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default=None, verbose_name='Requester\'s Review')
    requester_recommendation = models.TextField(null=True, blank=True,
                                                default=None, verbose_name='Requester\'s recommendation')

    requestee = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requestee', verbose_name='Requestee')
    requestee_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default=None, verbose_name='Requestee\'s Review', null=True)
    requestee_recommendation = models.TextField(null=True, blank=True,
                                                default=None, verbose_name='Requestee\'s recommendation')

    is_confirmed = models.NullBooleanField(default=None, verbose_name='Requestee Confirmed')
    is_admin_approved = models.NullBooleanField(default=None, verbose_name='Approved from Admin')
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Transaction Amount')
    value_in_usd = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Value in USD', null=True,
                                       blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD', verbose_name='Transaction Currency')
    is_requester_principal = models.BooleanField(default=False, verbose_name='Requester Payed')

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.proof_receipt:
                ext = self.proof_receipt.name.split('.')[-1]
                self.proof_receipt.name = f'{uuid.uuid4().hex}.{ext}'
            else:
                self.is_verified = False

        super(Transaction, self).save(*args, **kwargs)

    @property
    def is_ready(self):
        if self.is_confirmed:
            if self.is_proof_by_requester is None:
                return True if self.value_in_usd else False
            else:
                return True if (self.is_admin_approved and self.value_in_usd) else False
        else:
            return False

    @property
    def is_verified(self):
        if self.is_proof_by_requester is None:
            return False
        return True
