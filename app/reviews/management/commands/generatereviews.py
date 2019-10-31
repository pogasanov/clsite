import random

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.models import Profile
from reviews.factories import ReviewFactory
from reviews.models import Review


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('reviews_count', nargs='?', type=int, default=1000)
        parser.add_argument('--generate-profiles', action='store_true')

    def handle(self, *args, **options):
        try:
            if options['generate_profiles']:
                ReviewFactory.create_batch(options['reviews_count'])
            else:
                profiles = list(Profile.objects.all())
                if not profiles:
                    raise CommandError('You need to generate profiles first. Use generateprofiles command.')
                for _ in range(options['reviews_count']):
                    tried = 0
                    # try again maximum 10 times before raising the error in case of integrity error on same values
                    while True:
                        try:
                            created_by, sent_to = random.sample(profiles, 2)
                            ReviewFactory(created_by=created_by, sent_to=sent_to)
                        except IntegrityError as ie:
                            tried += 1
                            if tried == 10:
                                review_count = Review.objects.count()
                                return str(review_count) + ' reviews generated. Unable to generate more reviews. ' \
                                                           'You need to generate more profiles first. ' \
                                                           'Truncate your database and use `generateprofiles` command.'
                            continue
                        break
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
