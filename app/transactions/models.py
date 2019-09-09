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
    REVIEW_STRONGLY_DISAGREE = 'SD'
    REVIEW_DISAGREE = 'D'
    REVIEW_NEUTRAL = 'N'
    REVIEW_AGREE = 'A'
    REVIEW_STRONGLY_AGREE = 'SA'
    REVIEW_CHOICES = (
        (REVIEW_STRONGLY_DISAGREE, 'Strongly Disagree'),
        (REVIEW_DISAGREE, 'Disagree'),
        (REVIEW_NEUTRAL, 'Neutral'),
        (REVIEW_AGREE, 'Agree'),
        (REVIEW_STRONGLY_AGREE, 'Strongly Agree')
    )

    IS_REQUESTER_PRINCIPAL_REQUESTER = True
    IS_REQUESTER_PRINCIPAL_REQUESTEE = False
    IS_REQUESTER_PRINCIPAL_CHOICES = (
        (IS_REQUESTER_PRINCIPAL_REQUESTER, 'I paid them'),
        (IS_REQUESTER_PRINCIPAL_REQUESTEE, 'They paid me')
    )

    CURRENCY_CHOICES = CURRENCIES

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date = models.DateField(verbose_name='Transaction Date')
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Transaction Amount')
    value_in_usd = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Value in USD', null=True,
                                       blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD', verbose_name='Transaction Currency')

    proof_receipt = models.ImageField(upload_to=get_image_path, storage=variativeStorage(),
                                      verbose_name='Transaction Proof', blank=True, null=True)
    is_proof_by_requester = models.NullBooleanField(default=None, verbose_name="Receipt added by requester")

    requester = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requester', verbose_name='Requester')
    requester_review = models.CharField(max_length=2, choices=REVIEW_CHOICES, default=REVIEW_NEUTRAL,
                                        verbose_name='Requester\'s Review')
    requester_recommendation = models.TextField(blank=True, default='', verbose_name='Requester\'s recommendation')

    requestee = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requestee', verbose_name='Requestee')
    requestee_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default=REVIEW_NEUTRAL, verbose_name='Requestee\'s recommendation')
    requestee_recommendation = models.TextField(verbose_name='Requestee\'s recommendation', default='', blank=True)

    is_confirmed = models.NullBooleanField(default=None, verbose_name='Requestee Confirmed')
    is_admin_approved = models.NullBooleanField(default=None, verbose_name='Approved from Admin')
    is_requester_principal = models.BooleanField(choices=IS_REQUESTER_PRINCIPAL_CHOICES,
                                                 default=IS_REQUESTER_PRINCIPAL_REQUESTEE,
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
        if self.is_confirmed:
            if self.proof_receipt:
                return bool(self.is_admin_approved and self.value_in_usd)
            else:
                return bool(self.value_in_usd)
        return False

    @property
    def is_verified(self):
        return bool(self.proof_receipt)

    def clean(self):
        super().clean()
        if self.requester == self.requestee:
            raise ValidationError('Requester and requestee cannot be the same user', code='same-requester-requestee')
