import random
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.models import Profile
from reviews.factories import ReviewFactory

MAX_RETRIES = 10


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('reviews_count', nargs='?', type=int, default=1000)
        parser.add_argument('--generate-profiles', action='store_true')

    def handle(self, *args, **options):
        combinations = []
        try:
            reviews_count = options['reviews_count']
            if options['generate_profiles']:
                ReviewFactory.create_batch(reviews_count)
                return

            profiles = list(Profile.objects.all())

            if not profiles:
                raise CommandError('You need to generate profiles first. Use `generateprofiles` command.')

            retries = 0
            while len(combinations) < reviews_count and retries < MAX_RETRIES:
                retries += 1
                created_by, sent_to = random.sample(profiles, 2)
                targeted_combinition = (created_by.id, sent_to.id,)

                if targeted_combinition not in combinations:
                    ReviewFactory(created_by=created_by, sent_to=sent_to)
                    combinations.append(targeted_combinition)
                    retries = 0

            if len(combinations) < reviews_count:
                self.stdout.write(
                    f'{len(combinations)} reviews generated. Unable to generate more reviews. '
                    f'You need to generate more profiles first. '
                    f'Truncate your database and use `generateprofiles` command.')

        except IntegrityError as ie:
            raise CommandError("Truncate your database and run this command again", ie)
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
