import random

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.models import Profile
from reviews.factories import ReviewFactory


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
                    while True:
                        try:
                            sender, receiver = random.sample(profiles, 2)
                            ReviewFactory(sender=sender, receiver=receiver)
                        except IntegrityError as ie:
                            tried += 1
                            if tried == 10:
                                raise CommandError('Unable to generate dummy reviews. generate more profiles first', ie)
                            continue
                        break
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
