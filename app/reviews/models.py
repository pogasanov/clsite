from django.db import models
import datetime
from django.core.exceptions import ValidationError


class Review(models.Model):
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
    IS_SENDER_PRINCIPAL_YES = True
    IS_SENDER_PRINCIPAL_NO = False
    IS_SENDER_PRINCIPAL_NONE = None
    IS_SENDER_PRINCIPAL_CHOICES = (
        (IS_SENDER_PRINCIPAL_YES, 'I paid them for work.'),
        (IS_SENDER_PRINCIPAL_NO, 'They paid me for work.'),
        (IS_SENDER_PRINCIPAL_NONE, 'We have paid each other for work.'),

    )
    sender = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='sender',
                               verbose_name='Sender')
    receiver = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='receiver',
                                 verbose_name='Receiver')
    is_sender_principal = models.NullBooleanField(default=None, choices=IS_SENDER_PRINCIPAL_CHOICES,
                                                  verbose_name='Sender Principal')
    work_description = models.TextField(null=False, blank=False)
    rating = models.CharField(max_length=2, choices=REVIEW_CHOICES, default=REVIEW_NEUTRAL,
                              verbose_name='Rating')
    recommendation = models.TextField(null=False, blank=False)
    deleted_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValidationError('Sender and receiver cannot be the same user', code='same-sender-receiver')
        super(Review, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('sender', 'receiver'),)
