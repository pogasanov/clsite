from django.db import models


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
    sender = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='sender', verbose_name='Sender')
    receiver = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='receiver', verbose_name='Receiver')
    sender_review = models.CharField(max_length=2, choices=REVIEW_CHOICES, default=REVIEW_NEUTRAL, verbose_name='Requester\'s Review')
    receiver_review = models.CharField(max_length=2, choices=REVIEW_CHOICES, default=REVIEW_NEUTRAL, verbose_name='Requester\'s Review')

