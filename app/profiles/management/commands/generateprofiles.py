from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.factories import ProfileFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('profile_count', nargs='?', type=int, default=100)

    def handle(self, *args, **options):
        try:
            ProfileFactory.create_batch(options['profile_count'])
        except IntegrityError as ie:
            raise CommandError('Unable to generate dummy profiles, truncate your database and try again.', ie)
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
