import random
from io import BytesIO
import factory.fuzzy
import factory.random

from profiles.factories import ProfileFactory
from reviews.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'reviews.Review'

    sender = factory.SubFactory(ProfileFactory)
    receiver = factory.SubFactory(ProfileFactory)
    rating = factory.fuzzy.FuzzyChoice(Review.REVIEW_CHOICES,  getter=lambda c: c[0])
    is_sender_principal = factory.fuzzy.FuzzyChoice(Review.IS_SENDER_PRINCIPAL_CHOICES,  getter=lambda c: c[0])
    work_description = factory.LazyFunction(lambda: "".join(
        factory.Faker('paragraphs', nb=3).generate()) if random.random() < 0.5 else '')
    recommendation = factory.LazyFunction(lambda: "".join(
        factory.Faker('paragraphs', nb=3).generate()) if random.random() < 0.5 else '')

    @factory.lazy_attribute
    def deleted_status(self):
        probability = random.random()
        # 30% chance for the review to be deleted
        if probability < 0.3:
            return True

        return False