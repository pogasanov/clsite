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
    CURRENCY_CHOICES = CURRENCIES

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name='What was the date of the transaction?')

    requester = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requester', verbose_name='Requester')
    requester_review = models.CharField(max_length=2, choices=REVIEW_CHOICES, default='',
                                        verbose_name='Requester\'s Review')
    requester_recommendation = models.TextField(blank=True, default='', verbose_name='Write a brief recommendation')

    requestee = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                  related_name='requestee', verbose_name='Requestee')
    requestee_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default='', verbose_name='Would you work with them again?')
    requestee_recommendation = models.TextField(verbose_name='Requestee\'s recommendation', default='', blank=True)

    is_confirmed = models.NullBooleanField(default=None, verbose_name='Requestee Confirmed')
    is_verified = models.NullBooleanField(default=None, verbose_name='Verified from Admin')
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Transaction Amount')
    value_in_usd = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Value in USD', null=True,
                                       blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD', verbose_name='Transaction Currency')
    is_requester_principal = models.BooleanField(default=False, verbose_name='Did one of you pay the other?')

    objects = TransactionQuerySet.as_manager()
    unconfirmed = TransactionUnconfirmedManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.proof_receipt:
                ext = self.proof_receipt.name.split('.')[-1]
                self.proof_receipt.name = f'{uuid.uuid4().hex}.{ext}'
            else:
                self.is_verified = False

        if self.currency == 'USD':
            self.value_in_usd = self.amount

        super(Transaction, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.requester == self.requestee:
            raise ValidationError('Requester and requestee cannot be the same user', code='same-requester-requestee')
