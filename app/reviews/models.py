from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Review(models.Model):
    REVIEW_STRONGLY_DISAGREE = 1
    REVIEW_DISAGREE = 2
    REVIEW_NEUTRAL = 3
    REVIEW_AGREE = 4
    REVIEW_STRONGLY_AGREE = 5
    REVIEW_CHOICES = (
        (REVIEW_STRONGLY_DISAGREE, 'Strongly Disagree'),
        (REVIEW_DISAGREE, 'Disagree'),
        (REVIEW_NEUTRAL, 'Neutral'),
        (REVIEW_AGREE, 'Agree'),
        (REVIEW_STRONGLY_AGREE, 'Strongly Agree')
    )
    IS_SENDER_PRINCIPAL_YES = True
    IS_SENDER_PRINCIPAL_NO = False
    ARE_BOTH_PRINCIPAL = None
    IS_SENDER_PRINCIPAL_CHOICES = (
        (IS_SENDER_PRINCIPAL_YES, 'I paid them for work.'),
        (IS_SENDER_PRINCIPAL_NO, 'They paid me for work.'),
        (ARE_BOTH_PRINCIPAL, 'We have paid each other for work.'),

    )
    created_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='sender',
                                   verbose_name='Sender')
    sent_to = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='receiver',
                                verbose_name='Receiver')
    is_sender_principal = models.NullBooleanField(default=None, choices=IS_SENDER_PRINCIPAL_CHOICES,
                                                  verbose_name='Sender Principal')
    work_description_private = models.TextField(null=False, blank=False)
    rating = models.IntegerField(choices=REVIEW_CHOICES, default=REVIEW_NEUTRAL, verbose_name='Rating')
    recommendation = models.TextField(null=False, blank=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.created_by == self.sent_to:
            raise ValidationError('Review Creator and review receiver cannot be same.')
        super(Review, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('created_by', 'sent_to'),)
