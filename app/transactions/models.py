import uuid

from django.core.exceptions import ValidationError
from django.db import models

from clsite.storage_backends import variativeStorage
from profiles.models import get_image_path
from transactions.choices import CURRENCIES


class TransactionQuerySet(models.QuerySet):
    def unconfirmed(self):
        return self.filter(is_confirmed=None)


class TransactionUnconfirmedManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db).unconfirmed()


class Transaction(models.Model):
    IS_REQUESTER_PRINCIPAL_YES = True
    IS_REQUESTER_PRINCIPAL_NO = False
    IS_REQUESTER_PRINCIPAL_CHOICES = (
        (IS_REQUESTER_PRINCIPAL_YES, 'Requester payed'),
        (IS_REQUESTER_PRINCIPAL_NO, 'Requestee payed')
    )

    CURRENCY_CHOICES = [(c, c) for c in CURRENCIES]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date = models.DateField(verbose_name='Transaction Date')
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Transaction Amount')
    value_in_usd = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Value in USD', null=True,
                                       blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD', verbose_name='Currency')

    proof_receipt = models.ImageField(upload_to=get_image_path, storage=variativeStorage(),
                                      verbose_name='Transaction Proof')

    requester = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requester', verbose_name='Requester')

    requestee = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requestee', verbose_name='Requestee')

    is_confirmed = models.NullBooleanField(default=None, verbose_name='Requestee Confirmed')
    is_flagged = models.BooleanField(default=False, verbose_name='Flagged')
    is_requester_principal = models.BooleanField(choices=IS_REQUESTER_PRINCIPAL_CHOICES,
                                                 default=IS_REQUESTER_PRINCIPAL_NO,
                                                 verbose_name='Requester Payed')

    objects = TransactionQuerySet.as_manager()
    unconfirmed = TransactionUnconfirmedManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.proof_receipt:
                ext = self.proof_receipt.name.split('.')[-1]
                self.proof_receipt.name = f'{uuid.uuid4().hex}.{ext}'

        if self.currency == 'USD':
            self.value_in_usd = self.amount

        super(Transaction, self).save(*args, **kwargs)

    @property
    def is_ready(self):
        return bool(self.value_in_usd and self.is_confirmed and not self.is_flagged)

    def clean(self):
        super().clean()
        if self.requester == self.requestee:
            raise ValidationError('Requester and requestee cannot be the same user', code='same-requester-requestee')
