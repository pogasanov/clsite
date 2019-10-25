import random
import factory.fuzzy
import factory.random
from datetime import datetime, timedelta
import pytz

from profiles.factories import ProfileFactory
from reviews.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'reviews.Review'

    created_by = factory.SubFactory(ProfileFactory)
    sent_to = factory.SubFactory(ProfileFactory)
    rating = factory.fuzzy.FuzzyChoice(Review.REVIEW_CHOICES, getter=lambda c: c[0])
    is_sender_principal = factory.fuzzy.FuzzyChoice(Review.IS_SENDER_PRINCIPAL_CHOICES, getter=lambda c: c[0])
    work_description_private = factory.LazyFunction(lambda: "".join(factory.Faker('paragraphs', nb=3).generate()))
    recommendation = factory.LazyFunction(lambda: "".join(factory.Faker('paragraphs', nb=3).generate()))
    created_at = factory.fuzzy.FuzzyDateTime(datetime.now(tz=pytz.UTC) - timedelta(days=30), datetime.now(tz=pytz.UTC))

    @factory.lazy_attribute
    def is_deleted(self):
        probability = random.random()
        # 10% chance for the review to be deleted
        if probability < 0.1:
            return True
        return False
